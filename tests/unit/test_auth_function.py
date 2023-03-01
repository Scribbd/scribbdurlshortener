
from authorizers.gnupg.src import authorizer


def test_lambda_handler_auth_event(apigw_auth_event, lambda_context):
    """Test authorizer, set the following environment variables for it to function on your machine:
    KEYID
    GRACE_PERIOD = 999999999999
    GPG_HOME
    GPG_BIN
    PUBLIC_KEY_URL
    """
    ret = authorizer.lambda_handler(apigw_auth_event, lambda_context)
    assert ret["isAuthorized"]
