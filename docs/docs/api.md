# Demucs - API

We provide a REST API to programmatically make requests to the service.

The API endpoint is: [`https://demucs-api-hwbhnojdya-uc.a.run.app`](https://demucs-api-hwbhnojdya-uc.a.run.app)

??? note "API service"
    The API runs on Google Cloud Run and you can read about our [implementation here](/docs/arch/cloud-run).

## Predict endpoint

The `/predict` is a `POST` endpoint that receives a JSON object in the body.

The endpoint received a base64 encoded versions of a song.

- The JSON body object should have one item called `instances` which contains a list of child objects
- The child object should contain one item called `b64`
- The value of `b64` should be a base64 encoded version of the song.

And example request body would be as follows:

```json
{
  "instances": [
    {
      "b64": "SUQzBAAAAAACfFRYWFg[...]"
    }
  ]
}

```

The response will also be JSON object containing 4 base64 encoded mp3 songs in a similar format:

```json
{
    "drums": "[... base64 string ...]",
    "bass": "[... base64 string ...]",
    "other": "[... base64 string ...]",
    "vocals": "[... base64 string ...]"
}
```

## OpenAPI

The API has an [OpenAPI](https://www.openapis.org/) UI that can be acceded at the `/docs` endpoint:
[`https://demucs-api-hwbhnojdya-uc.a.run.app/docs`](https://demucs-api-hwbhnojdya-uc.a.run.app/docs)

From here is also possible to test the API.

<figure markdown>
![](/docs/public/images/open-api.png)
</figure>


## Postman Collection

We provide a Postman Collection with a small 3 second mix fragment to test the API.
Access it here: [Demucs postman collection](https://www.postman.com/danielfrg/workspace/demucs-service/request/17206474-3bd1a96b-b99e-4612-a004-75304cd6f01f).

<figure markdown>
![](/docs/public/images/postman.png)
</figure>


## Base64 encode an mp3 file

You can easily convert an `.mp3` file to base64 using this command:

```shell
base64 mixture.mp3 > mixture.b64.txt
```
