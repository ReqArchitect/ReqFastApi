import asyncio
import os
import json
import logging

async def listen_architecture_events():
    import aioredis
    redis_url = os.getenv("REDIS_URL", "redis://localhost:6379/0")
    redis = await aioredis.from_url(redis_url, decode_responses=True)
    pubsub = redis.pubsub()
    await pubsub.subscribe("architecture_suite_events")
    logger = logging.getLogger("architecture_suite.events")
    logger.setLevel(logging.INFO)
    while True:
        message = await pubsub.get_message(ignore_subscribe_messages=True, timeout=1.0)
        if message and message['type'] == 'message':
            try:
                payload = json.loads(message['data'])
                logger.info(f"Received event: {payload}")
                logger.info(f"Correlation ID: {payload.get('correlation_id')}")
                logger.info(f"Timestamp: {payload.get('timestamp')}, Tenant: {payload.get('tenant_id')}")
            except Exception as e:
                logger.error(f"Malformed event: {e}")
        await asyncio.sleep(0.1)

if __name__ == "__main__":
    asyncio.run(listen_architecture_events())
