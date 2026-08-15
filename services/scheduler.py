import asyncio
import logging

import redis.asyncio as redis

from core.config import settings

logger = logging.getLogger(__name__)


class SchedulerService:
    def __init__(self):
        self.redis = redis.from_url(settings.redis_url)
        self.is_running = False

    async def start(self):
        self.is_running = True
        logger.info("Scheduler service started.")
        asyncio.create_task(self._process_jobs())

    async def stop(self):
        self.is_running = False
        await self.redis.close()
        logger.info("Scheduler service stopped.")

    async def schedule_job(self, queue_name: str, payload: str):
        await self.redis.lpush(queue_name, payload)
        logger.info(f"Job scheduled in queue '{queue_name}'.")

    async def _process_jobs(self):
        while self.is_running:
            try:
                # BRPOP blocks until an item is available, timeout=1s
                result = await self.redis.brpop("devmate_jobs", timeout=1)
                if result:
                    queue, payload = result
                    logger.info(f"Processing job from devmate_jobs: {payload}")
                    # Simulate processing
                    await asyncio.sleep(0.1)
            except Exception as e:
                logger.error(f"Error in scheduler loop: {e}")
                await asyncio.sleep(1)


scheduler = SchedulerService()
