# Demucs Architecture

The Demucs service runs in the [Google Cloud Platform](https://cloud.google.com/).

<figure markdown>
![gcp](https://www.freecodecamp.org/news/content/images/2020/10/gcp.png){: style="height:200px"}
</figure>


Services used:

- [Firebase](firebase): Hosting and authentication
- [Cloud Build](cloud-build): CI/CD
- [Secret Manager](cloud-build/#secret-manager)
- [Cloud Run](cloud-run): Serverless model API
- [Artifact Registry](artifact-registry): Hosting for the artifacts

Technologies:

- [Astro and Svelte for the website](webapp)
- [PyTorch and FastAPI for the model API](model-api)

In GCP we have a single project to organize all the cloud resources, APIs, users
storage and more.

## Source

The code for the different parts of the service can be found on Github:
[danielfrg/demucs-service](https://github.com/danielfrg/demucs-service).
