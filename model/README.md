# Demucs Model API

Run locally

```shell
uvicorn api:app --host 0.0.0.0 --port 8080 --reload
```

Generate sample:

```shell
base64 mixture.mp3 > mixture.b64 | base64 --decode > decode.mp3
```
