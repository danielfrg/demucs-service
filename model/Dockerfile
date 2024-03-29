FROM condaforge/mambaforge:4.12.0-0

# RUN apt-get update && apt-get install -y build-essential unzip wget python-dev ffmpeg libsndfile-dev

# Conda env
COPY environment.yml environment.yml
RUN mamba env create

RUN echo "source activate demucs-api" > ~/.bashrc
ENV PATH /opt/conda/envs/demucs-api/bin:$PATH
RUN ln /opt/conda/envs/demucs-api/lib/libopenh264.so.6 /opt/conda/envs/demucs-api/lib/libopenh264.so.5

# Download models
RUN mkdir -p /data
RUN mkdir -p /models
RUN mkdir -p /app

COPY src/config.py /app/config.py
COPY src/download.py /app/download.py
RUN python /app/download.py

# Copy source code
COPY src /app
WORKDIR /app

EXPOSE 8080
ENV demucs_models=/models
ENV demucs_data=/data
ENV AIP_HTTP_PORT=8080
ENV AIP_HEALTH_ROUTE=/health
ENV AIP_PREDICT_ROUTE=/predict

CMD uvicorn api:app --host 0.0.0.0 --port $AIP_HTTP_PORT --log-level debug
