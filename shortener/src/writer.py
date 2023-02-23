import os

import boto3
import json

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Response, content_types
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext

DYNAMODB_TABLE_NAME = os.getenv("SLUG_TABLE")
VALIDATOR_FUNCTION_NAME = os.getenv("VALIDATOR_FUNCTION_NAME")

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()
app = APIGatewayHttpResolver()
lambda_client = boto3.client('lambda')
slug_table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)


@app.post("/<slug>")
@tracer.capture_method
def post_method(slug: str) -> dict:
    pass


@app.put("/<slug>")
@tracer.capture_method
def put_method(slug: str) -> dict:
    pass


@app.delete("/<slug>")
@tracer.capture_method
def delete_method(slug: str) -> dict:
    pass


@event_source(data_class=APIGatewayProxyEventV2)
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True, correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def lambda_handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> dict:
    logger.info("Validating signature.")
    response = lambda_client.invoke(
        FunctionName=VALIDATOR_FUNCTION_NAME,
        InvocationType='RequestResponse',
        ClientContext=json.dumps(context),
        Payload=json.dumps(event)
    )
    valid = response[""]
    logger.info(f"Signature validation; {valid}")
    if response.fail:
        return {
            "statusCode": 401,
            "body": json.dumps({
                "code": "401",
                "message": "Validation failed"
            })
        }

    return app.resolve(event, context)
