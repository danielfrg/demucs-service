# Demucs Architecture

The Demucs service runs in the [Google Cloud Platform](https://cloud.google.com/).

Services used:

- [Firebase](firebase): Hosting and authentication
- [Cloud Build](cloud-build): CI/CD
- [Cloud Run](cloud-run): Serverless prediction API
- [Artifact Registry](artifact-registry): Serverless prediction API

Technologies:

- [Astro and Svelte for the website](webapp)
- [PyTorch and FastAPI for the model API](model-api)

In GCP we have a single project to organize all the cloud resources, APIs, users
storage and more.

## Source

The code for the different parts of the service can be found on Github:
[danielfrg/demucs-service](https://github.com/danielfrg/demucs-service).
