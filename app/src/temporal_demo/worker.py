from __future__ import annotations

import asyncio
import logging

from temporalio.worker import Worker

from temporal_demo.activities import build_greeting
from temporal_demo.client import connect_temporal_client
from temporal_demo.config import TEMPORAL_CONNECT_DELAY_SECONDS, TEMPORAL_TASK_QUEUE
from temporal_demo.workflows import GreetingWorkflow


logger = logging.getLogger(__name__)


async def main() -> None:
    while True:
        try:
            client = await connect_temporal_client()
            worker = Worker(
                client,
                task_queue=TEMPORAL_TASK_QUEUE,
                workflows=[GreetingWorkflow],
                activities=[build_greeting],
            )
            await worker.run()
            return
        except Exception as exc:
            logger.warning("Worker startup failed, retrying: %s", exc)
            await asyncio.sleep(TEMPORAL_CONNECT_DELAY_SECONDS)


if __name__ == "__main__":
    asyncio.run(main())
