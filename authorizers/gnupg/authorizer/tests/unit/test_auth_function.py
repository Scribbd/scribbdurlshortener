import json

from src import authorizer


def test_lambda_handler_auth_event(apigw_auth_event, lambda_context):
    ret = authorizer.lambda_handler(apigw_auth_event, lambda_context)
    assert ret["isAuthorized"]

