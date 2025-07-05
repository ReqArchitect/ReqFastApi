import pytest
from architecture_suite_sdk import ApiClient, Configuration, ModelApi

MOCK_HOST = "http://localhost:4010"  # Prism or WireMock mock server

def test_get_model_tree():
    config = Configuration(host=MOCK_HOST)
    with ApiClient(config) as api_client:
        model_api = ModelApi(api_client)
        resp = model_api.get_model_tree()
        assert resp is not None
