import os
import pickle
import base64

import gnupg
import requests
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_authorizer_event import APIGatewayAuthorizerEventV2, APIGatewayAuthorizerResponseV2

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()
COLD_PREFIX: str = "WARMUP:"

PUBLIC_KEY_URL: str = os.getenv("PUBLIC_KEY_URL")
logger.info(f"{COLD_PREFIX} Getting public keys from {PUBLIC_KEY_URL}")
asc_file = requests.get(PUBLIC_KEY_URL)

gpg: gnupg.GPG = gnupg.GPG(gnupghome="/tmp/")
import_results: gnupg.ImportResult = gpg.import_keys(asc_file.text)
logger.info(f"{COLD_PREFIX} Imported keys count {import_results.count}")
logger.info(f"{COLD_PREFIX} Imported key fingerprints: {import_results.fingerprints}")
logger.debug(f"{COLD_PREFIX} GPG response objecstrt:", pickle.dumps(import_results))

@event_source(data_class=APIGatewayAuthorizerEventV2)
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True, correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def lambda_handler(event: APIGatewayAuthorizerEventV2, context: LambdaContext) -> dict:
    authorization_header: str = event.headers.get("Authorization")
    signature = base64.b64decode(authorization_header, validate=True)
    verified = gpg.verify(signature)

    return APIGatewayAuthorizerResponseV2(authorize=verified.valid).asdict()