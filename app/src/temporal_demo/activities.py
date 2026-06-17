from __future__ import annotations

from temporalio import activity


@activity.defn
async def build_greeting(name: str, completed_steps: int) -> str:
    return f"Hello {name}, your Temporal workflow finished after {completed_steps} steps."
