import json
from dataclasses import dataclass

import pytest


@pytest.fixture
def lambda_context():
    @dataclass
    class LambdaContext:
        function_name: str = "test"
        memory_limit_in_mb: int = 128
        invoked_function_arn: str = "arn:aws:lambda:eu-west-1:809313241:function:test"
        aws_request_id: str = "52fdfc07-2182-154f-163f-5f0f9a621d72"

    return LambdaContext()


@pytest.fixture()
def apigw_auth_event():
    """Generates API GW Event"""
    with open("authorizer/event/request.json", "r", encoding="UTF-8") as fp:
        return json.load(fp)
        


