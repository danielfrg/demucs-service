# Cloud Run

<figure markdown>
![](https://seeklogo.com/images/G/google-cloud-run-logo-895F1305FF-seeklogo.com.png){: style="height:100px"}
</figure>

[Cloud Run](https://cloud.google.com/run) is the serverless service that
runs the [model API](/docs/arch/model-api) when a new request comes from the [Web app](/docs/arch/webapp).

<figure markdown>
![](/docs/public/images/cloud-run-dashboard.png)
</figure>

## Dockerfile

Cloud runs deploys a containerized version of the model API.

```dockerfile title="Dockerfile"
FROM condaforge/mambaforge:4.12.0-0

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
```

## Deployment

Building and deployment of the docker image is automated via [Cloud Run](/docs/arch/cloud-run).
