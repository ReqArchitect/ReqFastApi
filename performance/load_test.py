from locust import HttpUser, task, between
import random

class WebsiteUser(HttpUser):
    wait_time = between(1, 5)

    @task(3)
    def get_model_tree(self):
        self.client.get("/orchestrator/model/tree")

    @task(2)
    def get_element_details(self):
        element = random.choice(["Capability", "Resource", "BusinessRole"])
        self.client.get(f"/orchestrator/model/{element}/00000000-0000-0000-0000-000000000001/full-details")

    @task(1)
    def bulk_import(self):
        # Simulate a bulk import (stub)
        self.client.post("/orchestrator/model/bulk-import", json={"count": 10})
