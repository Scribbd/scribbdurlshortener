import os
import pickle
import base64

from aws_lambda_powertools import Logger, Tracer
from aws_lambda_powertools.logging import correlation_paths
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.data_classes import event_source
from aws_lambda_powertools.utilities.data_classes.api_gateway_proxy_event import APIGatewayProxyEventV2


### COLD BOOT SCRIPT ###
logger = Logger(log_uncaught_exceptions=True)
tracer = Tracer()

### MAIN HANDLER ###
@event_source(data_class=APIGatewayProxyEventV2)
@tracer.capture_lambda_handler
@logger.inject_lambda_context(log_event=True, correlation_id_path=correlation_paths.API_GATEWAY_HTTP)
def lambda_handler(event: APIGatewayProxyEventV2, context: LambdaContext) -> dict:
    pass