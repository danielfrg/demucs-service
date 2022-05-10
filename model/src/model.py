import hashlib
import os
import sys
from pathlib import Path

import torch as th
import torchaudio as ta
from demucs.apply import apply_model
from demucs.pretrained import get_model
from demucs.separate import load_track

from config import settings


class Demucs(object):
    def __init__(self, output_dir, model_id="mdx_extra_q", load=False):
        # Model options
        self.model = None
        self.model_id = model_id
        self.shifts = 0
        self.split = True
        self.overlap = 0.25
        self.mp3 = True
        self.float32 = False
        self.mp3_bitrate = 320
        self.verbose = True

        self.output_dir = output_dir

        if load:
            self.load()

    def load(self):
        if self.model is None:
            print("Loading model...")
            th.hub.set_dir(settings.models)
            self.model = get_model(self.model_id)
            self.device = "cuda" if th.cuda.is_available() else "cpu"

            if not th.cuda.is_available():
                self.device = "cpu"
            else:
                self.device = "cuda"
            self.model.to(self.device)
        return True

    def separate(self, fpath):
        """
        Returns
        -------
            dictionary of {source_name: fname}
                fname is a file inside the output_dir argument
                e.g. {"bass": "bass.mp3", "drums": "drums.mp3"}
        """
        track = Path(fpath)
        unique_id = hash_file(fpath)

        output_dir = os.path.join(self.output_dir, unique_id)
        os.makedirs(output_dir, exist_ok=True)
        out = Path(output_dir)

        wav = load_track(track, self.model.audio_channels, self.model.samplerate)

        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()
        # sources = apply_model(
        #     self.model,
        #     wav,
        #     shifts=self.shifts,
        #     split=self.split,
        #     overlap=self.overlap,
        #     progress=True,
        # )
        sources = apply_model(
            self.model,
            wav[None],
            device=self.device,
            shifts=self.shifts,
            split=self.split,
            overlap=self.overlap,
            progress=True,
            # num_workers=self.jobs,
        )[0]
        sources = sources * ref.std() + ref.mean()

        track_folder = out
        # track_folder = out / track.name.rsplit(".", 1)[0]
        track_folder.mkdir(exist_ok=True)

        generated_files = {}
        for source, name in zip(sources, self.model.sources):
            source = source / max(1.01 * source.abs().max(), 1)
            if self.mp3 or not self.float32:
                source = (source * 2**15).clamp_(-(2**15), 2**15 - 1).short()
            source = source.cpu()
            stem = str(track_folder / name)
            if self.mp3:
                save_mp3(
                    source,
                    stem + ".mp3",
                    bitrate=self.mp3_bitrate,
                    samplerate=self.model.samplerate,
                    channels=self.model.audio_channels,
                    verbose=self.verbose,
                )
            else:
                wavname = str(track_folder / f"{name}.wav")
                ta.save(wavname, source, sample_rate=self.model.samplerate)

            generated_files[name] = stem + ".mp3"

        return generated_files

    def cached(self, fpath):
        """
        Checks if this file has already been processed and all output files are
        on the filesystem

        Returns
        -------
            tuple of (exists, unique_id)
        """
        unique_id = hash_file(fpath)
        sources = ["bass", "drums", "other", "vocals"]
        source_exists = []
        output = {}

        for source in sources:
            output[source] = f"{source}.mp3"

            source_exists.append(os.path.exists(fpath))
            fpath = os.path.join(self.output_dir, f"{unique_id}/{source}.mp3")
            output[source] = fpath

        return all(source_exists), unique_id


def save_mp3(wav, path, bitrate=320, samplerate=44100, channels=2, verbose=False):
    """
    Encode and save an mp3 file
    """
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


def hash_file(fpath):
    """Generate a hash a file"""
    hasher = hashlib.sha256()

    with open(fpath, "rb") as f:
        while True:
            data = f.read(65536)
            if not data:
                break
            hasher.update(data)

    signature = hasher.hexdigest()
    return signature


if __name__ == "__main__":
    outdir = os.path.join(settings.data, "separated")
    model = Demucs(output_dir=outdir, load=True)
    print(model)

    # Separate mp3
    # sep = model.separate(settings.data / "sample" / "mixture.mp3")
    # print(sep)

    # Separate base64 encoded mp3
    import base64
    from tempfile import NamedTemporaryFile

    file_content = ""
    with open(settings.data / "sample" / "mixture.b64", "rb") as f:
        file_content = f.read()

    with NamedTemporaryFile(delete=False) as tmp:
        file_content = base64.b64decode(file_content)
        tmp.write(file_content)
        tmp.flush()

        fpath = Path(tmp.name)
        print(fpath)
        sep = model.separate(fpath)
        print(sep)
