from __future__ import annotations

from contextlib import asynccontextmanager
from typing import Any
from uuid import uuid4

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field
from temporalio.client import Client, WorkflowHandle
from temporalio.common import WorkflowIDReusePolicy
from temporalio.service import RPCError

from temporal_demo.client import connect_temporal_client
from temporal_demo.config import TEMPORAL_TARGET_HOST, TEMPORAL_TASK_QUEUE
from temporal_demo.workflows import GreetingWorkflow


templates = Jinja2Templates(directory="/app/src/temporal_demo/templates")


class StartWorkflowRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)
    total_steps: int = Field(default=5, ge=1, le=20)
    delay_seconds: int = Field(default=2, ge=1, le=30)


class UpdateNameRequest(BaseModel):
    name: str = Field(min_length=1, max_length=80)


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.temporal_client = await connect_temporal_client()
    yield


app = FastAPI(title="Temporal Demo", lifespan=lifespan)


def get_client(request: Request) -> Client:
    return request.app.state.temporal_client


async def get_handle(client: Client, workflow_id: str) -> WorkflowHandle[Any, Any]:
    return client.get_workflow_handle(workflow_id)


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        name="index.html",
        request=request,
        context={
            "temporal_target_host": TEMPORAL_TARGET_HOST,
            "task_queue": TEMPORAL_TASK_QUEUE,
        },
    )


@app.post("/api/workflows")
async def start_workflow(payload: StartWorkflowRequest, request: Request) -> dict[str, Any]:
    client = get_client(request)
    workflow_id = f"greeting-{uuid4()}"
    handle = await client.start_workflow(
        GreetingWorkflow.run,
        args=[payload.name, payload.total_steps, payload.delay_seconds],
        id=workflow_id,
        task_queue=TEMPORAL_TASK_QUEUE,
        id_reuse_policy=WorkflowIDReusePolicy.ALLOW_DUPLICATE,
    )
    return {
        "workflow_id": workflow_id,
        "run_id": handle.result_run_id,
        "message": "Workflow started",
    }


@app.get("/api/workflows/{workflow_id}")
async def describe_workflow(workflow_id: str, request: Request) -> dict[str, Any]:
    client = get_client(request)
    handle = await get_handle(client, workflow_id)

    try:
        description = await handle.describe()
    except RPCError as exc:
        raise HTTPException(status_code=404, detail="Workflow not found") from exc

    status: dict[str, Any] = {
        "workflow_id": workflow_id,
        "run_id": description.execution.run_id,
        "status": description.status.name,
    }

    try:
        status["details"] = await handle.query(GreetingWorkflow.get_status)
    except RPCError:
        status["details"] = None

    if description.status.name == "COMPLETED":
        try:
            status["result"] = await handle.result()
        except RPCError:
            status["result"] = None

    return status


@app.post("/api/workflows/{workflow_id}/signal")
async def signal_workflow(workflow_id: str, payload: UpdateNameRequest, request: Request) -> dict[str, str]:
    client = get_client(request)
    handle = await get_handle(client, workflow_id)

    try:
        await handle.signal(GreetingWorkflow.update_name, payload.name)
    except RPCError as exc:
        raise HTTPException(status_code=404, detail="Workflow not found or not signalable") from exc

    return {"message": "Signal delivered"}


@app.post("/api/workflows/{workflow_id}/cancel")
async def cancel_workflow(workflow_id: str, request: Request) -> dict[str, str]:
    client = get_client(request)
    handle = await get_handle(client, workflow_id)

    try:
        await handle.cancel()
    except RPCError as exc:
        raise HTTPException(status_code=404, detail="Workflow not found or not cancellable") from exc

    return {"message": "Cancellation requested"}
