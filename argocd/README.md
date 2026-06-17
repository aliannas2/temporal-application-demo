# Argo CD setup for Temporal demo

This folder contains an Argo CD ApplicationSet that deploys all stack resources via Helm charts:

- helm/temporal-demo (Temporal server, proxy, UI, web, worker, postgres)
- helm/temporal-ingress (ingress resources for UI and gRPC endpoint)

## Prerequisites

1. Argo CD is installed and running in namespace argocd.
2. Minikube ingress addon is enabled:

   minikube addons enable ingress

3. Create token Secret before syncing the apps:

   kubectl -n temporal-demo create secret generic temporal-auth \
     --from-literal=token='<your-token>' \
     --dry-run=client -o yaml | kubectl apply -f -

## Apply ApplicationSet

kubectl apply -f argocd/appset-temporal-demo.yaml

## Verify

kubectl -n argocd get applications
kubectl -n temporal-demo get pods,svc,ingress
