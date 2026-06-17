#!/usr/bin/env sh

set -eu

CERT_DIR="${1:-.certs}"

mkdir -p "$CERT_DIR"

openssl req -x509 -nodes -newkey rsa:4096 \
  -keyout "$CERT_DIR/ca.key" \
  -out "$CERT_DIR/ca.crt" \
  -days 365 \
  -subj "/CN=temporal-demo-ca"

openssl req -nodes -newkey rsa:4096 \
  -keyout "$CERT_DIR/server.key" \
  -out "$CERT_DIR/server.csr" \
  -subj "/CN=temporal"

cat > "$CERT_DIR/server.ext" <<'EOF'
subjectAltName=DNS:temporal,DNS:localhost,IP:127.0.0.1
extendedKeyUsage=serverAuth
EOF

openssl x509 -req \
  -in "$CERT_DIR/server.csr" \
  -CA "$CERT_DIR/ca.crt" \
  -CAkey "$CERT_DIR/ca.key" \
  -CAcreateserial \
  -out "$CERT_DIR/server.crt" \
  -days 365 \
  -extfile "$CERT_DIR/server.ext"

openssl req -nodes -newkey rsa:4096 \
  -keyout "$CERT_DIR/client.key" \
  -out "$CERT_DIR/client.csr" \
  -subj "/CN=temporal-demo-client"

cat > "$CERT_DIR/client.ext" <<'EOF'
extendedKeyUsage=clientAuth
EOF

openssl x509 -req \
  -in "$CERT_DIR/client.csr" \
  -CA "$CERT_DIR/ca.crt" \
  -CAkey "$CERT_DIR/ca.key" \
  -CAcreateserial \
  -out "$CERT_DIR/client.crt" \
  -days 365 \
  -extfile "$CERT_DIR/client.ext"

rm -f \
  "$CERT_DIR/server.csr" \
  "$CERT_DIR/client.csr" \
  "$CERT_DIR/server.ext" \
  "$CERT_DIR/client.ext" \
  "$CERT_DIR/ca.srl"

chmod 600 "$CERT_DIR/ca.key" "$CERT_DIR/server.key" "$CERT_DIR/client.key"

printf 'Generated mTLS assets in %s\n' "$CERT_DIR"