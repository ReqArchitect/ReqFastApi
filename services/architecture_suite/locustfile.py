from locust import HttpUser, task, between
import random
import uuid

class ArchitectureSuiteUser(HttpUser):
    wait_time = between(0.01, 0.05)

    @task(2)
    def get_package(self):
        package_id = str(uuid.uuid4())
        self.client.get(f"/architecture-packages/{package_id}")

    @task(1)
    def post_package(self):
        payload = {
            "tenant_id": str(uuid.uuid4()),
            "user_id": str(uuid.uuid4()),
            "business_case_id": str(uuid.uuid4()),
            "initiative_id": str(uuid.uuid4()),
            "kpi_id": str(uuid.uuid4()),
            "business_model_id": str(uuid.uuid4()),
            "name": "LoadTest",
            "description": "Load test package"
        }
        headers = {"Authorization": "Bearer testtoken"}
        self.client.post("/architecture-packages/?correlation_id=" + str(uuid.uuid4()), json=payload, headers=headers)

    @task(1)
    def get_impact_summary(self):
        package_id = str(uuid.uuid4())
        self.client.get(f"/architecture-packages/{package_id}/impact-summary")
