from __future__ import annotations

from dataclasses import asdict, dataclass
from datetime import timedelta

from temporalio import workflow

with workflow.unsafe.imports_passed_through():
    from temporal_demo.activities import build_greeting


@dataclass
class GreetingStatus:
    workflow_id: str
    name: str
    current_step: int
    total_steps: int
    completed: bool
    message: str | None


@workflow.defn
class GreetingWorkflow:
    def __init__(self) -> None:
        self._name = ""
        self._current_step = 0
        self._total_steps = 0
        self._completed = False
        self._message: str | None = None

    @workflow.run
    async def run(self, name: str, total_steps: int = 5, delay_seconds: int = 2) -> str:
        self._name = name
        self._total_steps = total_steps

        for step in range(1, total_steps + 1):
            self._current_step = step
            await workflow.sleep(delay_seconds)

        self._message = await workflow.execute_activity(
            build_greeting,
            self._name,
            self._current_step,
            start_to_close_timeout=timedelta(seconds=10),
        )
        self._completed = True
        return self._message

    @workflow.query
    def get_status(self) -> dict[str, object]:
        return asdict(
            GreetingStatus(
                workflow_id=workflow.info().workflow_id,
                name=self._name,
                current_step=self._current_step,
                total_steps=self._total_steps,
                completed=self._completed,
                message=self._message,
            )
        )

    @workflow.signal
    def update_name(self, new_name: str) -> None:
        self._name = new_name
