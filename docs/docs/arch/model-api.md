# Model API

The API run in Python and mainly uses [PyTorch](https://pytorch.org/) and
[Fast API](https://fastapi.tiangolo.com/).

## Wrapper

This is a programmatic wrapper around the `demucs` library:

The key code:

```python title="model.py" hl_lines="10 23 75-77"
import torch as th
import torchaudio as ta
from demucs.apply import apply_model
from demucs.pretrained import get_model
from demucs.separate import load_track


class Demucs(object):
    def load(self):
        if self.model is None: # (1)
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

    def separate(self, fpath):  # (2)
        track = Path(fpath)
        unique_id = hash_file(fpath)

        output_dir = os.path.join(self.output_dir, unique_id)
        os.makedirs(output_dir, exist_ok=True)
        out = Path(output_dir)

        wav = load_track(track, self.model.audio_channels, self.model.samplerate)

        ref = wav.mean(0)
        wav = (wav - ref.mean()) / ref.std()

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

        # Base64 encode the files

        for source, fpath in generated_files.items():  # (3)
            with open(fpath, "rb") as f:
                generated_files[source] = base64.b64encode(f.read()).decode("utf-8")

        return generated_files
```

1. Singleton object to only load the model once
2. Path to the input file
3. Returns base 64 encoded version of the files

[Full source](https://github.com/danielfrg/demucs-service/blob/main/model/src/model.py)

## REST API

```python title="api.py"
from fastapi import FastAPI
from model import Demucs

model = Demucs(load=False) # (1)

app = FastAPI()

@app.post(os.environ.get("AIP_PREDICT_ROUTE", "/predict"), status_code=200)
async def predict(request: Request):
    body = await request.json() # (2)
    instances = body["instances"]

    for instance in instances:
        return infer(instance["b64"])


def infer(file_content):
    model.load()

    with NamedTemporaryFile(delete=False) as tmp:
        file_content = base64.b64decode(file_content)
        tmp.write(file_content)
        tmp.flush()

        fpath = Path(tmp.name)

        # exists, unique_id = model.cached(fpath)

        generated_files = model.separate(fpath)  # (2)
        return generated_files
```

1. Load model wrapper
2. Parse request body
3. Call the model wrapper

[Full source](https://github.com/danielfrg/demucs-service/blob/main/model/src/api.py)
