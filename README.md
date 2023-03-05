# Scribbd Url-Shortener
A bare-bones private url-shortener, hosted in AWS, built with [aws-sam](https://aws.amazon.com/serverless/sam/).

This is the technical documentation. If you wish for some more reading, start [here](docs/article.md)

![Design of the URL Shortener. It is a serverless application that uses Route53, API-gateway with a custom authorizer based on GnuPG, two backend lambdas: a reader for unprotected GET calls with only read permissions to the DynamoDB Table. And a protected write functions with CRUD access.](docs/img/URLShort.jpg)

## Usage
Install the tools and programs defined in [Development](#development), you do not need to install the python dependencies for just deploying. To deploy the stack, use the following command: `sam build --use-container && sam deploy --guided`. You will be asked to fill in general parameters used by SAM, and the following parameters specific to this application:

| Parameter             | Description                                                                   |
|-----------------------|-------------------------------------------------------------------------------|
| Arch                  | Allowed values: "arm64", "x86_x64". Set architecture used in Lambda functions.|
| AuthorizerGracePerios | Time in seconds that a signature is valid.                                    |
| CertificateArn        | The ACM certificate associated with your domain                               |
| DomainName            | The R53 Domain with no trialing '.'                                           |
| Environment           | Allowed values: "Dev", "Prd". When set to Prd it will limit CORS, and disable the default API endpoint.|
| PowerToolsVersion     | The version of the Python Lambda Powertools, get the most recent version [here](https://awslabs.github.io/aws-lambda-powertools-python/2.9.1/#install). |
| PublicKeyURL          | A URL to an asc-file with your public keys.                                    |

### Using the API
An [OpenAPI specification](docs/OpenAPI3Export.yaml) is available containing further documentation. However, basically you can create a POST, PUT, and DELETE request with the following body: 

```json
{
    "target": "URL"
}
```

The request path determines the slug you wish to create, update, or delete. Sending a POST request to `example.com/test` will create a redirect on that URL.

Sign the body as instructed [below](#how-to-sign-your-request). And send it with your favorite tool or package to your endpoint. This repository has an [example post-script](post.py) available.

GET requests don't require a body and respond with either with a NotFound-error or a redirect.

## GnuPG Authorizer
This custom authorizer requires the following environment variable to be set to function: 
- `PUBLIC_KEY_URL`: The URL should serve an asc-file. An option for this is [Keybase](https://keybase.io/).

For more information about environment variables, look into the [gnupg-authorizer readme](authorizers/gnupg/README.md).

### How to sign your request
The following explains the basic workflow with the GnuPG authorizer:
- Create a json-body with one element "target", give it a valid URL.
- Sign the body with GnuPG (or others) with `gpg --sign --clearsign` [man](https://www.gnupg.org/documentation/manpage.html).
- Encode the resulting text in base64.
- Use the encoded signature in the header as `authorization` and the unsigned json-body as body.

## Development
The following programs should be installed:
- [Python](https://www.python.org/downloads/)
- [Pipenv](https://pipenv.pypa.io/en/latest/install/#installing-pipenv)
- A docker-cli compatible container-engine (`sam build` requires a complete docker cli implementation, podman will not work)
- [SAM-cli](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)
- [AWS-cli](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html)

Set up your dev environment with: `pipenv install --dev`

I use [direnv](https://direnv.net/) to set the environment variables. 
```bash
export AWS_REGION=
export AWS_PROFILE=

export PUBLIC_KEY_URL=
export ENDPOINT=
export KEYID=
export GRACE_PERIOD=99999999999
export GPG_HOME=~/.gnupg
export GPG_BIN=gpg
export SLUG_TABLE=
```
