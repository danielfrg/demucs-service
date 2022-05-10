FROM python:3.8.12-buster

RUN apt-get update && apt-get install -y build-essential unzip wget python-dev ffmpeg libsndfile-dev

ENV TINI_VERSION v0.19.0
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /tini
RUN chmod +x /tini
ENTRYPOINT ["/tini", "--"]

# Location for the serialized models
RUN mkdir -p /models
COPY models /models

# Location for the output files
RUN mkdir -p /data

# Source code
RUN mkdir -p /app
WORKDIR /app

# Python dependencies
ARG POETRY_VERSION=1.1.8
RUN pip install "poetry==$POETRY_VERSION"

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock
RUN poetry export --without-hashes --no-interaction --no-ansi -f requirements.txt -o requirements.txt
RUN pip install -r requirements.txt

COPY src /app
COPY js/out /app/js/out

ENV ENV_FOR_DYNACONF=docker
CMD /usr/local/bin/uvicorn api:app --host 0.0.0.0 --log-level debug
