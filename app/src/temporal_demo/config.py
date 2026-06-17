from __future__ import annotations

import os


TEMPORAL_TARGET_HOST = os.getenv("TEMPORAL_TARGET_HOST", "localhost:7233")
TEMPORAL_TASK_QUEUE = os.getenv("TEMPORAL_TASK_QUEUE", "demo-task-queue")
TEMPORAL_AUTH_TOKEN = os.getenv("TEMPORAL_AUTH_TOKEN", "")
TEMPORAL_CONNECT_RETRIES = int(os.getenv("TEMPORAL_CONNECT_RETRIES", "20"))
TEMPORAL_CONNECT_DELAY_SECONDS = float(os.getenv("TEMPORAL_CONNECT_DELAY_SECONDS", "3"))

