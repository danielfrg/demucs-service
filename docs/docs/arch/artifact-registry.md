# Artifact Registry

<figure markdown>
![](https://assets.website-files.com/60c912417dc3bac5c9fa2616/6160c8309a2337582561d572_gar.png){: style="height:100px"}
</figure>

[Artifact Registry](https://cloud.google.com/artifact-registry) provides hosting
for different types of artifacts  in our case we use it to host Docker images
for the model API.

<figure markdown>
![](/docs/public/images/artifact-registry.png)
</figure>

## Building the image

The process of building this image and pushing it to the registry
is automated via [Cloud Run](/docs/arch/cloud-run).
