# architecture_suite_sdk (Python)

A unified Python client for the architecture_suite platform, generated from the combined OpenAPI specs of all services.

## Installation
```sh
pip install .
```

## Usage Example
```python
from architecture_suite_sdk import ApiClient, Configuration, ModelApi

config = Configuration(host="http://localhost:8080")
with ApiClient(config) as api_client:
    model_api = ModelApi(api_client)
    tree = model_api.get_model_tree()
    print(tree)
```

## Authentication
- Pass your Bearer token via `Configuration(api_key={'Authorization': 'Bearer <token>'})`

## Endpoints
- All orchestrator and element service endpoints are available as methods.
