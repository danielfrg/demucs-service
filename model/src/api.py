import base64
import logging
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

import torch as th
from fastapi import FastAPI, Request
from fastapi.logger import logger as fp_logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from config import settings
from model import Demucs

autoload = settings.docker
outdir = os.path.join(settings.data, "separated")
model = Demucs(output_dir=outdir, load=False)

fp_logger.setLevel(logging.DEBUG)
logger = logging.getLogger(__name__)

th.hub.set_dir(settings.models)

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", status_code=200, response_class=HTMLResponse)
def root():
    return 'See <a href="/docs">/docs</a> for API documentation'


@app.get(
    os.environ.get("AIP_HEALTH_ROUTE", "/health"),
    status_code=200,
)
def health():
    """health check to ensure HTTP server is ready to handle
    prediction requests
    """
    return {"status": "healthy"}


@app.get(
    os.environ.get("AIP_PREDICT_ROUTE", "/predict"),
    status_code=200,
    response_class=HTMLResponse,
)
async def predict_get():
    return "/predict is a POST endpoint"


@app.post(os.environ.get("AIP_PREDICT_ROUTE", "/predict"), status_code=200)
async def predict(request: Request):
    body = await request.json()
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

        generated_files = model.separate(fpath)
        return generated_files
