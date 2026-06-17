# Temporal Application Demo

This project provides a minimal Temporal application in a containerized environment with two browser-facing interfaces:

- A demo web app on port 8081 that lets you start, inspect, signal, and cancel workflows.
- The official Temporal UI on port 8233 for execution history and cluster visibility.
- A native Temporal TLS-protected gRPC endpoint on port 7233 for SDK clients.

## Stack

- Temporal server + bootstrap tooling
	- Docker Compose: `temporalio/auto-setup:1.26.2`
	- Kubernetes/Helm: `temporalio/server:1.26.2` with `temporalio/admin-tools:1.26.2` init/bootstrap
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

- Stable baseline (current Kubernetes/Argo deploy):
	- Frontend TLS enabled
	- `requireClientAuth=false`
	- Temporal server runs `frontend,history,matching` services (internal Temporal `worker` service disabled for local stability)
	- App validates server certificate with the demo CA
	- App client certificate usage is optional and disabled by default (`TEMPORAL_TLS_USE_CLIENT_CERT=false`)
- Temporal endpoint: `localhost:7233`

Generate the certificates once before starting the stack:

```bash
./generate-certs.sh
```

Compose and Kubernetes manifests mount the generated certificates into:

- the Temporal server (for native TLS/mTLS)
- the Python web app
- the worker
- Temporal UI

The Python client always validates the Temporal frontend certificate against the generated CA. It presents a client certificate only when `TEMPORAL_TLS_USE_CLIENT_CERT=true`.

To rotate the certificates:

1. Delete `.certs/`
2. Run `./generate-certs.sh`
3. Run `docker compose up -d --build`

This PoC uses Temporal-native frontend TLS settings and removes the proxy from the auth path.

Note: strict `requireClientAuth=true` is intentionally not the default for this local demo because it can destabilize bootstrap/internode behavior in lightweight setups. For production-grade client-certificate enforcement, use dedicated cert SAN planning and explicit internode/frontend policies.

## Minikube image refresh

When you change code under `app/`, rebuild and load the app image into Minikube before restarting `web`/`worker`:

```bash
minikube image build -t temporal-demo-app:latest ./app
kubectl -n temporal-demo rollout restart deploy/web deploy/worker
kubectl -n temporal-demo rollout status deploy/web --timeout=600s
kubectl -n temporal-demo rollout status deploy/worker --timeout=600s
```

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
