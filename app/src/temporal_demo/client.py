from __future__ import annotations

import asyncio
import logging

from temporalio.client import Client, TLSConfig

from temporal_demo.config import (
    TEMPORAL_CONNECT_DELAY_SECONDS,
    TEMPORAL_CONNECT_RETRIES,
    TEMPORAL_MTLS_ENABLED,
    TEMPORAL_TARGET_HOST,
    TEMPORAL_TLS_CA_CERT_PATH,
    TEMPORAL_TLS_CLIENT_CERT_PATH,
    TEMPORAL_TLS_CLIENT_KEY_PATH,
    TEMPORAL_TLS_DOMAIN,
)


logger = logging.getLogger(__name__)


def _read_tls_file(path: str) -> bytes:
    with open(path, "rb") as cert_file:
        return cert_file.read()


async def connect_temporal_client() -> Client:
    last_error: Exception | None = None
    connect_kwargs = {}

    if TEMPORAL_MTLS_ENABLED:
        connect_kwargs["tls"] = TLSConfig(
            domain=TEMPORAL_TLS_DOMAIN or None,
            server_root_ca_cert=_read_tls_file(TEMPORAL_TLS_CA_CERT_PATH),
            client_cert=_read_tls_file(TEMPORAL_TLS_CLIENT_CERT_PATH),
            client_private_key=_read_tls_file(TEMPORAL_TLS_CLIENT_KEY_PATH),
        )

    for attempt in range(1, TEMPORAL_CONNECT_RETRIES + 1):
        try:
            return await Client.connect(TEMPORAL_TARGET_HOST, **connect_kwargs)
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