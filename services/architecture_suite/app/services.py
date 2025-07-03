import os
import redis
import json
from datetime import datetime
from uuid import UUID

REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")
redis_client = redis.Redis.from_url(REDIS_URL, decode_responses=True)

SERVICE_VERSION = "1.0.0"


# Event emission for ArchitecturePackage
async def emit_event(event_type: str, source_service: str, entity_id: UUID, tenant_id: UUID, correlation_id: UUID):
    event = {
        "event_type": event_type,
        "source_service": source_service,
        "entity_id": str(entity_id),
        "tenant_id": str(tenant_id),
        "correlation_id": str(correlation_id),
        "timestamp": datetime.utcnow().isoformat() + "Z"
    }
    # Use aioredis for async pub/sub
    try:
        import aioredis
        redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
        redis = await aioredis.from_url(redis_url, decode_responses=True)
        await redis.publish(f"{source_service}_events", json.dumps(event))
        await redis.close()
    except ImportError:
        # fallback to sync for test/dev
        redis_client.publish(f"{source_service}_events", json.dumps(event))

def get_service_version():
    return SERVICE_VERSION
