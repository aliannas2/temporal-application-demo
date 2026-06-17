# Temporal Application Demo

This project provides a minimal Temporal application in a containerized environment with two browser-facing interfaces:

- A demo web app on port 8081 that lets you start, inspect, signal, and cancel workflows.
- The official Temporal UI on port 8233 for execution history and cluster visibility.
- A native Temporal TLS-protected gRPC endpoint on port 7233 for SDK clients.

## Stack

- Temporal server via `temporalio/auto-setup`
- Temporal UI via `temporalio/ui`
- Python worker and API built with `temporalio`, `FastAPI`, and `Uvicorn`
- PostgreSQL backing store for Temporal

## Start

```bash
./generate-certs.sh
docker compose up --build
```

The certificate generator creates a local CA, a server certificate for Temporal frontend, and a client certificate shared by the demo web app, worker, and Temporal UI.

When using native TLS with this local `auto-setup` image, create the default namespace once:

```bash
docker compose exec temporal \
	temporal operator namespace create default --retention 3d \
	--address temporal:7233 \
	--tls-ca-path /etc/temporal/certs/ca.crt \
	--tls-cert-path /etc/temporal/certs/client.crt \
	--tls-key-path /etc/temporal/certs/client.key \
	--tls-server-name temporal
```

## Endpoints

- Demo web app: `http://localhost:8081`
- Temporal UI: `http://localhost:8233`
- Temporal gRPC endpoint: `localhost:7233`

## Authentication

Temporal frontend is configured natively with TLS certificates and the Python SDK connects using `TLSConfig`.

- Required client assets for this demo client: CA cert, client cert, and client private key
- Temporal endpoint: `localhost:7233`

Generate the certificates once before starting the stack:

```bash
./generate-certs.sh
```

Compose mounts the generated certificates into:

- the Temporal server (for native TLS/mTLS)
- the Python web app
- the worker
- Temporal UI

The Python client uses `temporalio.client.TLSConfig` to present the client certificate and validate the Temporal frontend certificate against the generated CA.

To rotate the certificates:

1. Delete `.certs/`
2. Run `./generate-certs.sh`
3. Run `docker compose up -d --build`

This PoC uses Temporal-native frontend TLS settings from the server config template (`global.tls.frontend`) and removes the proxy from the auth path.

Note: in the `temporalio/auto-setup` local image, strict `requireClientAuth` is coupled with internode behavior and can break bootstrap. For production-grade client-certificate enforcement, use a full Temporal server config (for example in Helm) where internode and frontend TLS client-auth policies are set explicitly.

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
