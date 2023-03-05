import base64
from unittest.mock import Mock, patch

from apibackend.shortener.src import writer

@patch("writer.boto3.resource")
def test_validate_signature(resource, apigw_post_event):
    encoded_header = apigw_post_event["headers"]["authorization"]
    header = base64.b64decode(encoded_header).decode("utf-8")
    body = base64.b64decode(apigw_post_event["body"]).decode("utf-8")
    assert writer.verify_request(header, body)

@patch("writer.boto3.resource")
def test_invalid_signature(resource, apigw_post_event):
    encoded_header = apigw_post_event["headers"]["authorization"]
    header = base64.b64decode(encoded_header).decode("utf-8")
    body = '{"Fake":"body"}'
    assert not writer.verify_request(header, body)