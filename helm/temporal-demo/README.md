# temporal-demo Helm chart

This chart deploys the same stack currently defined in the Kubernetes manifest:

- postgres
- temporal
- temporal-proxy (token-enforced gRPC ingress)
- temporal-ui
- web
- worker

## Token via env.tpl

1. Set your token in `helm/env.tpl`.

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

If you already manage a Kubernetes Secret with the token, set:

- auth.existingSecret
- auth.secretKey

and leave auth.token empty.
