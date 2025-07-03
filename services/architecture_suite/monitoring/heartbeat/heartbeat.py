import time
import requests
from prometheus_client import start_http_server, Gauge

HEALTH_URL = "http://architecture-suite:8000/health"
HEARTBEAT_METRIC = Gauge('architecture_suite_heartbeat_success', 'Heartbeat success for architecture_suite')

if __name__ == "__main__":
    start_http_server(9101)
    fail_count = 0
    while True:
        try:
            resp = requests.get(HEALTH_URL, timeout=5)
            if resp.status_code == 200:
                HEARTBEAT_METRIC.set(1)
                fail_count = 0
            else:
                HEARTBEAT_METRIC.set(0)
                fail_count += 1
        except Exception:
            HEARTBEAT_METRIC.set(0)
            fail_count += 1
        if fail_count >= 3:
            print("ALERT: architecture_suite heartbeat failed 3 times consecutively!")
        time.sleep(60)
