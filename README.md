# Temporal Application Demo

This project provides a minimal Temporal application in a containerized environment with two browser-facing interfaces:

- A demo web app on port 8081 that lets you start, inspect, signal, and cancel workflows.
- The official Temporal UI on port 8233 for execution history and cluster visibility.
- A token-protected gRPC ingress on port 7233 for authenticated Temporal SDK clients.

## Stack

- Temporal server via `temporalio/auto-setup`
- Temporal UI via `temporalio/ui`
- Python worker and API built with `temporalio`, `FastAPI`, and `Uvicorn`
- PostgreSQL backing store for Temporal

## Start

```bash
docker compose up --build
```

Docker Compose reads `TEMPORAL_AUTH_TOKEN` from `.env` in the project root.

## Endpoints

- Demo web app: `http://localhost:8081`
- Temporal UI: `http://localhost:8233`
- Temporal gRPC endpoint: `localhost:7233`

## Authentication

Temporal client traffic from the Python app and worker goes through a token-enforcing proxy.

- Required header: `Authorization: Bearer <TEMPORAL_AUTH_TOKEN>`
- Proxy endpoint: `localhost:7233`

Set the token once in `.env`:

```bash
TEMPORAL_AUTH_TOKEN=demo-temporal-token
```

Compose injects that value into:

- the Python web app
- the worker
- the gRPC auth proxy

To rotate the token:

1. Update `.env`
2. Run `docker compose up -d --build`

## Demo flow

1. Open the demo web app.
2. Start a workflow by providing a name, step count, and delay.
3. Copy or reuse the generated workflow ID.
4. Inspect the workflow to view live state.
5. Send a signal to change the workflow name while it is running.
6. Optionally cancel the workflow.

## Services

- `web`: FastAPI app exposing the browser UI and HTTP API
- `worker`: Temporal worker running the workflow and activity
- `temporal`: Temporal server
- `temporal-ui`: Official Temporal Web UI
- `postgres`: Database for Temporal persistence
