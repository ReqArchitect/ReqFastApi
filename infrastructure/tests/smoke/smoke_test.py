import requests

def test_orchestrator_health():
    resp = requests.get('http://orchestrator-service/health')
    assert resp.status_code == 200

def test_ui_landing():
    resp = requests.get('http://unified-model-ui/')
    assert resp.status_code == 200
# Add more synthetic transactions for critical flows
