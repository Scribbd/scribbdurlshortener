import base64
import json
import os
import re
from http import HTTPStatus

import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError
from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import (APIGatewayHttpResolver,
                                                 Response, content_types)
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import \
    APIGatewayProxyEventV2
from aws_lambda_powertools.utilities.typing import LambdaContext

DYNAMODB_TABLE_NAME: str = os.getenv("SLUG_TABLE")
VALIDATOR_FUNCTION_NAME: str = os.getenv("VALIDATOR_FUNCTION_NAME")

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()
app = APIGatewayHttpResolver()
slug_table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE_NAME)
regex = re.compile(
    r"^Hash: SHA256$\n\n(^{\n?[\s\"a-zA-Z:,/.{}]*\n?})\n^-----BEGIN PGP SIGNATURE-----$",
    flags=re.MULTILINE
)


@app.post("/<slug>")
@tracer.capture_method
def post_method(slug: str) -> dict:
    try:
        slug_table.put_item(Item={
            "id": slug,
            "target": app.current_event.json_body.get("target")
        }, ConditionExpression=Attr("id").not_exists()
        )
    except ClientError as error:
        if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        return serve_error("Slug already has a registered target.")


@app.put("/<slug>")
@tracer.capture_method
def put_method(slug: str) -> dict:
    try:
        slug_table.update_item(Item={
            "id": slug,
            "target": app.current_event.json_body.get("target")
        }, ConditionExpression=Attr("id").exists()
        )
    except ClientError as error:
        if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        return serve_error("Slug has no registered target to update")


@app.delete("/<slug>")
@tracer.capture_method
def delete_method(slug: str) -> dict:
    try:
        slug_table.delete_item(
            Key={"id": slug}, ConditionExpression=Attr("id").exists())
    except ClientError as error:
        if error.response['Error']['Code'] != 'ConditionalCheckFailedException':
            raise
        return serve_error("No slug to delete")


@tracer.capture_method
def serve_error(message: str) -> Response:
    return Response(
        status_code=HTTPStatus.INTERNAL_SERVER_ERROR.value,
        content_type=content_types.APPLICATION_JSON,
        body=json.dumps({
            "code": HTTPStatus.INTERNAL_SERVER_ERROR.value,
            "message": message
        })
    )


@tracer.capture_method
def verify_request(header: str, body: str) -> bool:
    matched = regex.findall(header)
    logger.info("Verifying body: %s with header: %s", body, matched)
    return json.loads(matched[0]) == json.loads(body)


@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True, correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def lambda_handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> dict:
    logger.info("Validating request.")
    encoded_header = event.headers.get("authorization")
    header = base64.b64decode(encoded_header).decode("utf-8")
    if not verify_request(header, event.decoded_body):
        logger.warn("Request is not valid!")
        return Response(
            status_code=HTTPStatus.BAD_REQUEST.value,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps({
                "code": HTTPStatus.BAD_REQUEST.value,
                "message": "Bad Request"
            })
        )#
    logger.info("Request is valid. Resolving event.")
    return app.resolve(event, context)
