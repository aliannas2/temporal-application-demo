# temporal-demo Helm chart

This chart deploys the same stack currently defined in the Kubernetes manifest:

- postgres
- temporal (`temporalio/server`) with schema/bootstrap jobs (`temporalio/admin-tools`)
- temporal-ui
- web
- worker

Current stable auth baseline:

- Frontend TLS enabled
- `tls.requireClientAuth=false`
- App uses TLS server validation with CA cert
- App client certificate presentation is optional via `tls.useClientCert` (default `false`)
- Internal host verification toggles are enabled for local stability:
   - `tls.internodeDisableHostVerification=true`
   - `tls.frontendDisableHostVerification=true`

## TLS Secret

Create a Kubernetes secret named `temporal-tls-certs` (or set `tls.existingSecret`) with keys:

- `ca.crt`
- `server.crt`
- `server.key`
- `client.crt`
- `client.key`

The chart reads server-side certs (`ca.crt`, `server.crt`, `server.key`) for Temporal frontend TLS.
Client cert files are mounted for optional client-auth usage by demo clients.

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

By default, `helm/env.tpl` sets `TEMPORAL_TLS_REQUIRE_CLIENT_AUTH=false` to keep the local demo stable.

## Alternative

If you already manage a Kubernetes Secret with certs, set:

- tls.existingSecret

Then leave `tls.create=false`.

## Notes

- Namespace bootstrap is handled by the `temporal-bootstrap-namespace` Job; no manual namespace creation step is required in the normal chart flow.
- If you set `tls.requireClientAuth=true`, also review cert SANs and internode/frontend TLS policy before rollout.
