import os
import subprocess
import sys
from pathlib import Path

import julius
import torch as th
import torchaudio as ta
from demucs.audio import AudioFile, convert_audio_channels
from demucs.pretrained import load_pretrained
from demucs.utils import apply_model

from config import settings


track = Path("../data/tracks/mixture.mp3")
out = Path(os.path.join(settings.data, "separated"))

shifts = 0
split = True
overlap = 0.25
model_id = "demucs_quantized"
mp3 = True
float32 = False
mp3_bitrate = 320
verbose = True

th.hub.set_dir(settings.models)
model = load_pretrained(model_id)

if not th.cuda.is_available():
    device = "cpu"
else:
    device = "cuda"
model.to(device)


def load_track(track, device, audio_channels, samplerate):
    errors = {}
    wav = None

    try:
        wav = (
            AudioFile(track)
            .read(streams=0, samplerate=samplerate, channels=audio_channels)
            .to(device)
        )
    except FileNotFoundError:
        errors["ffmpeg"] = "Ffmpeg is not installed."
    except subprocess.CalledProcessError:
        errors["ffmpeg"] = "FFmpeg could not read the file."

    if wav is None:
        try:
            wav, sr = ta.load(str(track))
        except RuntimeError as err:
            errors["torchaudio"] = err.args[0]
        else:
            wav = convert_audio_channels(wav, audio_channels)
            wav = wav.to(device)
            wav = julius.resample_frac(wav, sr, samplerate)

    if wav is None:
        print(
            f"Could not load file {track}. " "Maybe it is not a supported file format? "
        )
        for backend, error in errors.items():
            print(
                f"When trying to load using {backend}, got the following error: {error}"
            )
        sys.exit(1)
    return wav


def encode_mp3(wav, path, bitrate=320, samplerate=44100, channels=2, verbose=False):
    try:
        import lameenc
    except ImportError:
        print(
            "Failed to call lame encoder. Maybe it is not installed? "
            "On windows, run `python.exe -m pip install -U lameenc`, "
            "on OSX/Linux, run `python3 -m pip install -U lameenc`, "
            "then try again.",
            file=sys.stderr,
        )
        sys.exit(1)
    encoder = lameenc.Encoder()
    encoder.set_bit_rate(bitrate)
    encoder.set_in_sample_rate(samplerate)
    encoder.set_channels(channels)
    encoder.set_quality(2)  # 2-highest, 7-fastest
    if not verbose:
        encoder.silence()
    wav = wav.transpose(0, 1).numpy()
    mp3_data = encoder.encode(wav.tobytes())
    mp3_data += encoder.flush()
    with open(path, "wb") as f:
        f.write(mp3_data)


wav = load_track(track, device, model.audio_channels, model.samplerate)

ref = wav.mean(0)
wav = (wav - ref.mean()) / ref.std()
sources = apply_model(
    model, wav, shifts=shifts, split=split, overlap=overlap, progress=True
)
sources = sources * ref.std() + ref.mean()

track_folder = out / track.name.rsplit(".", 1)[0]
track_folder.mkdir(exist_ok=True)

for source, name in zip(sources, model.sources):
    source = source / max(1.01 * source.abs().max(), 1)
    if mp3 or not float32:
        source = (source * 2 ** 15).clamp_(-(2 ** 15), 2 ** 15 - 1).short()
    source = source.cpu()
    stem = str(track_folder / name)
    if mp3:
        encode_mp3(
            source,
            stem + ".mp3",
            bitrate=mp3_bitrate,
            samplerate=model.samplerate,
            channels=model.audio_channels,
            verbose=verbose,
        )
    else:
        wavname = str(track_folder / f"{name}.wav")
        ta.save(wavname, source, sample_rate=model.samplerate)
