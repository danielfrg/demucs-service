# Cloud Build

<figure markdown>
![](https://miro.medium.com/max/256/0*u3LacWYz2vFH3OSH.png){: style="height:100px"}
</figure>

[Cloud Build](https://cloud.google.com/build) is used for CI/CD.
It is setup with triggers from [Github](https://github.com/danielfrg/demucs-service)
and we have to workflows that deploy to:

- [Firebase](/docs/arch/firebase)
- [Cloud Run](/docs/arch/cloud-run)

<figure markdown>
![](/docs/public/images/cloud-build-dashboard.png)
<figcaption>Cloud Build Dashboard</figcaption>
</figure>

<figure markdown>
![](/docs/public/images/cloud-build-list.png)
<figcaption>Cloud Build list of builds</figcaption>
</figure>

## Workflows

Each workflow has is based on its own `cloudbuild.yml`

<figure markdown>
![](/docs/public/images/cloud-build-triggers.png)
<figcaption>Cloud Build Triggers</figcaption>
</figure>

## Website

```yaml title="cloudbuild.yml"
steps:
  # ----------------------------------------------------------------------------
  # Build website

  - name: node
    entrypoint: npm
    args: ["install"]

  - name: node
    entrypoint: npm
    args: ["run", "build"]
    env:
      - "PUBLIC_VERSION=${SHORT_SHA}"
    secretEnv: ["PUBLIC_FIREBASE_API_KEY"]

  # ----------------------------------------------------------------------------
  # Build docs

  - name: python
    dir: docs
    entrypoint: pip
    args: ["install", "-r", "requirements.txt", "--user"]

  - name: python
    dir: docs
    entrypoint: python
    args: ["-m", "mkdocs", "build"]

  # ----------------------------------------------------------------------------
  # Deploy to Firebase

  - name: us-central1-docker.pkg.dev/demucs-service/firebase/firebase
    args: ["deploy", "--project=demucs-service", "--only=hosting"]
```

### Secret Manager


This workflow also uses [Secret Manager](https://cloud.google.com/secret-manager)
to pass the Firebase API key to the build process.

??? Note
    The Firebase API key is not needed to be kept secret. We do that
    to show whats possible with the build process.

<figure markdown>
![firebase](/docs/public/images/secret-manager.png)
<figcaption>Secret Manager</figcaption>
</figure>

```yaml title="cloudbuild.yml"
availableSecrets:
  secretManager:
    - versionName: projects/demucs-service/secrets/FIREBASE_API_KEY/versions/1
      env: "PUBLIC_FIREBASE_API_KEY"
```

## Model API to Cloud Run

This workflow was initially created by Cloud Run itself and moved to
the Github repository to take advantage of version control.

The workflow builds a docker image, pushes it to the registry and deploys it
to Cloud Run

```yaml title="Build Docker image"
steps:
  - name: gcr.io/cloud-builders/docker
    args:
      - build
      - "--no-cache"
      - "-t"
      - "${_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_IMAGE}:$COMMIT_SHA"
      - model
      - "-f"
      - model/Dockerfile
    id: Build
```

```yaml title="Push Docker image"
  - name: gcr.io/cloud-builders/docker
    args:
      - push
      - "${_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_IMAGE}:$COMMIT_SHA"
    id: Push
```

```yaml title="Deploy to Cloud Run"
  - name: "gcr.io/google.com/cloudsdktool/cloud-sdk:slim"
    args:
      - run
      - services
      - update
      - $_SERVICE_NAME
      - "--platform=managed"
      - "--image=${_LOCATION}-docker.pkg.dev/${PROJECT_ID}/${_REPOSITORY}/${_IMAGE}:$COMMIT_SHA"
      - >-
        --labels=managed-by=gcp-cloud-build-deploy-cloud-run,commit-sha=$COMMIT_SHA,gcb-build-id=$BUILD_ID,gcb-trigger-id=$_TRIGGER_ID,$_LABELS
      - "--region=$_DEPLOY_REGION"
      - "--quiet"
    id: Deploy
    entrypoint: gcloud
```
