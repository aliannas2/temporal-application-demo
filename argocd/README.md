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

4. Create the default namespace once (Temporal auto-setup with TLS does not always create it):

    kubectl -n temporal-demo exec deploy/temporal -- \
       temporal operator namespace create default --retention 3d \
       --address temporal:7233 \
       --tls-ca-path /etc/temporal/certs/ca.crt \
       --tls-cert-path /etc/temporal/certs/client.crt \
       --tls-key-path /etc/temporal/certs/client.key \
       --tls-server-name temporal

## Apply ApplicationSet

kubectl apply -f argocd/appset-temporal-demo.yaml

## Verify

kubectl -n argocd get applications
kubectl -n temporal-demo get pods,svc,ingress
