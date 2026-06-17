from __future__ import annotations

import asyncio
import logging

from temporalio.client import Client

from temporal_demo.config import (
    TEMPORAL_AUTH_TOKEN,
    TEMPORAL_CONNECT_DELAY_SECONDS,
    TEMPORAL_CONNECT_RETRIES,
    TEMPORAL_TARGET_HOST,
)


logger = logging.getLogger(__name__)


async def connect_temporal_client() -> Client:
    last_error: Exception | None = None
    rpc_metadata = {}

    if TEMPORAL_AUTH_TOKEN:
        rpc_metadata["authorization"] = f"Bearer {TEMPORAL_AUTH_TOKEN}"

    for attempt in range(1, TEMPORAL_CONNECT_RETRIES + 1):
        try:
            return await Client.connect(TEMPORAL_TARGET_HOST, rpc_metadata=rpc_metadata)
        except Exception as exc:
            last_error = exc
            logger.warning(
                "Temporal connection attempt %s/%s failed: %s",
                attempt,
                TEMPORAL_CONNECT_RETRIES,
                exc,
            )
            await asyncio.sleep(TEMPORAL_CONNECT_DELAY_SECONDS)

    assert last_error is not None
    raise last_error