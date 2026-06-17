# Argo CD setup for Temporal demo

This folder contains an Argo CD ApplicationSet that deploys all stack resources via Helm charts:

- helm/temporal-demo (Temporal server, UI, web, worker, postgres)
- helm/temporal-ingress (ingress resources for UI and gRPC endpoint)

## Prerequisites

1. Argo CD is installed and running in namespace argocd.
2. Minikube ingress addon is enabled:

   minikube addons enable ingress

3. Create TLS Secret before syncing the apps:

    kubectl -n temporal-demo create secret generic temporal-tls-certs \
       --from-file=ca.crt=.certs/ca.crt \
       --from-file=server.crt=.certs/server.crt \
       --from-file=server.key=.certs/server.key \
       --from-file=client.crt=.certs/client.crt \
       --from-file=client.key=.certs/client.key \
     --dry-run=client -o yaml | kubectl apply -f -

4. Ensure the ApplicationSet is configured with stable TLS defaults (already set in this repo):

   - `tls.requireClientAuth=false` for the temporal-demo application
   - direct gRPC ingress/backend to `temporal:7233`
   - no proxy/token auth dependency in the datapath

## Apply ApplicationSet

kubectl apply -f argocd/appset-temporal-demo.yaml

The chart creates the default Temporal namespace via the `temporal-bootstrap-namespace` Job.

## Verify

kubectl -n argocd get applications
kubectl -n temporal-demo get pods,svc,ingress
kubectl -n temporal-demo get jobs

Optional functional check from the web pod:

kubectl -n temporal-demo exec deploy/web -- \
   python -c "import json, urllib.request; data=json.dumps({'name':'DocCheck','total_steps':1,'delay_seconds':1}).encode(); req=urllib.request.Request('http://127.0.0.1:8080/api/workflows', data=data, headers={'Content-Type':'application/json'}, method='POST'); resp=urllib.request.urlopen(req, timeout=20); print(resp.status); print(resp.read().decode())"
