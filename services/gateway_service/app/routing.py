ROUTING_TABLE = {
    "/orchestrator": "http://orchestrator_service:8001",
    "/ai_modeling": "http://ai_modeling_service:8002",
    "/usage": "http://usage_service:8003",
    "/onboarding": "http://onboarding_state_service:8004",
    "/audit_log": "http://audit_log_service:8005",
}

def resolve_service(path: str) -> str:
    for prefix, url in ROUTING_TABLE.items():
        if path.startswith(prefix):
            return url
    return None
