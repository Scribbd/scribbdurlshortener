import json
import os
from http import HTTPStatus

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.event_handler import APIGatewayHttpResolver, Response, content_types
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities import parameters
from aws_lambda_powertools.utilities.parameters.exceptions import \
    GetParameterError
from aws_lambda_powertools.utilities.typing import LambdaContext

DYNAMODB_TABLE = os.getenv("SLUG_TABLE")

logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()
app = APIGatewayHttpResolver()
dynamodb = parameters.DynamoDBProvider(table_name=DYNAMODB_TABLE)

@app.get("/<slug>")
def get_method(slug: str) -> Response:
    logger.info(f"Looking up {slug} in {DYNAMODB_TABLE}")
    try:
        target = dynamodb.get(slug)
    except GetParameterError:
        logger.info(f"Did not find {slug} in {DYNAMODB_TABLE}.")
        return Response(
            status_code=HTTPStatus.NOT_FOUND.value,
            content_type=content_types.APPLICATION_JSON,
            body=json.dumps({
                "code": 404,
                "message": "Slug has no target."
            })
        )
    logger.info(f"Found: {target}")
    return Response(
        status_code=HTTPStatus.PERMANENT_REDIRECT.value,
        content_type=content_types.TEXT_HTML,
        headers={"location": target},
        body="redirecting"
    )

@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True, correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
