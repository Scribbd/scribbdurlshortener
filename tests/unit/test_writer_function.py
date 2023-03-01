
import base64

from apibackend.shortener.src import writer

def test_validate_signature(apigw_post_event):
    encoded_header = apigw_post_event["headers"]["authorization"]
    header = base64.b64decode(encoded_header).decode("utf-8")
    body = base64.b64decode(apigw_post_event["body"]).decode("utf-8")
    assert writer.verify_request(header, body)

def test_invalid_signature(apigw_post_event):
    encoded_header = apigw_post_event["headers"]["authorization"]
    header = base64.b64decode(encoded_header).decode("utf-8")
    body = '{"Fake":"body"}'
    assert not writer.verify_request(header, body)