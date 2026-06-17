# temporal-demo Helm chart

This chart deploys the same stack currently defined in the Kubernetes manifest:

- postgres
- temporal
- temporal-ui
- web
- worker

## TLS Secret

Create a Kubernetes secret named `temporal-tls-certs` (or set `tls.existingSecret`) with keys:

- `ca.crt`
- `server.crt`
- `server.key`
- `client.crt`
- `client.key`

## Optional env.tpl Overrides

1. Set your values in `helm/env.tpl`.

2. Load env vars in your shell:

   set -a
   source helm/env.tpl
   set +a

3. Install/upgrade chart using values template processed by envsubst:

   envsubst < helm/temporal-demo/values-env.tpl.yaml | \
   helm upgrade --install temporal-demo helm/temporal-demo \
     -n temporal-demo --create-namespace \
     -f helm/temporal-demo/values.yaml \
     -f -

## Alternative

If you already manage a Kubernetes Secret with certs, set:

- tls.existingSecret

Then leave `tls.create=false`.
