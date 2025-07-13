def emit_creation_event(entity: str, uuid: str, tenant_id: str, user_id: str, redis_client):
    event = {
        "event_type": f"{entity}.created",
        "source_id": uuid,
        "tenant_id": tenant_id,
        "user_id": user_id
    }
    redis_client.publish(f"{entity}_events", event)
