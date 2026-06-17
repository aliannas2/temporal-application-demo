# Set your variables, export them, render values, then install.
# Example:
#   set -a
#   source helm/env.tpl
#   set +a
#   envsubst < helm/temporal-demo/values-env.tpl.yaml > /tmp/temporal-demo-values.yaml
#   helm upgrade --install temporal-demo helm/temporal-demo -n temporal-demo --create-namespace -f helm/temporal-demo/values.yaml -f /tmp/temporal-demo-values.yaml

TEMPORAL_TLS_SECRET_NAME=temporal-tls-certs
TEMPORAL_TLS_REQUIRE_CLIENT_AUTH=false
