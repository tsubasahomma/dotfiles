#!/bin/sh
# [Architecture]: Tier -1 & 0 Bootstrapping (Assertion Gate & Identity Provisioning)
# [Rationale]: Pure POSIX script executed via hooks.read-source-state.pre.
# Template variables are NOT supported here.

set -eu

if [ "${CI:-false}" = "true" ]; then
  exit 0
fi

echo "🛡️  [Tier -1] Executing Assertion Gate (Minimal Prepared OS Check)..."

if ! command -v curl > /dev/null 2>&1; then
  echo "❌ [Fatal] 'curl' is missing."
  echo "👉 Action Required: Install curl via your OS package manager and retry."
  exit 1
fi

if ! command -v unzip > /dev/null 2>&1 && ! command -v python3 > /dev/null 2>&1; then
  echo "❌ [Fatal] Neither 'unzip' nor 'python3' is available for archive extraction."
  echo "👉 Action Required: Install unzip via your OS package manager and retry."
  exit 1
fi

echo "✅ [Tier -1] Minimal requirements met."

LOCAL_BIN="$HOME/.local/bin"
OP_BIN="$LOCAL_BIN/op"

if [ ! -x "$OP_BIN" ]; then
  echo "🔐 [Tier 0] Provisioning 1Password CLI (Identity Anchor)..."
  mkdir -p "$LOCAL_BIN"

  # Determine OS and Architecture
  OS_ID=$(uname -s | tr '[:upper:]' '[:lower:]')
  ARCH_ID=$(uname -m)
  if [ "$ARCH_ID" = "x86_64" ]; then
    ARCH_ID="amd64"
  elif [ "$ARCH_ID" = "aarch64" ] || [ "$ARCH_ID" = "arm64" ]; then
    ARCH_ID="arm64"
  fi

  # Parse tools.yaml directly using awk
  TOOLS_YAML="$(dirname "$0")/.chezmoidata/tools.yaml"
  if [ ! -f "$TOOLS_YAML" ]; then
    echo "❌ [Fatal] tools.yaml not found at $TOOLS_YAML"
    exit 1
  fi

  OP_VERSION=$(awk '/^ *op:/{f=1} f && /^ *version:/{print $2; exit}' "$TOOLS_YAML" | tr -d '"')
  OP_HASH=$(awk "/^ *op:/{f=1} f && /^ *${OS_ID}-${ARCH_ID}:/{print \$2; exit}" "$TOOLS_YAML" | tr -d '"')

  if [ -z "$OP_VERSION" ]; then
    echo "❌ [Fatal] Could not parse op version from tools.yaml"
    exit 1
  fi

  OP_URL="https://cache.agilebits.com/dist/1P/op2/pkg/v${OP_VERSION}/op_${OS_ID}_${ARCH_ID}_v${OP_VERSION}.zip"
  curl -fsSL "$OP_URL" -o /tmp/op.zip

  # Hash Verification
  if [ -n "$OP_HASH" ]; then
    ACTUAL_HASH=$(sha256sum /tmp/op.zip 2> /dev/null | cut -d' ' -f1 || shasum -a 256 /tmp/op.zip | cut -d' ' -f1)
    if [ "$ACTUAL_HASH" != "$OP_HASH" ]; then
      echo "❌ [Fatal] 1Password CLI hash mismatch."
      echo "Expected: $OP_HASH"
      echo "Actual:   $ACTUAL_HASH"
      rm -f /tmp/op.zip
      exit 1
    fi
  else
    echo "⚠️  [Warning] Hash for ${OS_ID}-${ARCH_ID} not found. Bypassing verification."
  fi

  if command -v unzip > /dev/null 2>&1; then
    unzip -q -o /tmp/op.zip -d /tmp/op_ext
  else
    python3 -m zipfile -e /tmp/op.zip /tmp/op_ext
  fi

  mv /tmp/op_ext/op "$OP_BIN"
  chmod +x "$OP_BIN"
  rm -rf /tmp/op.zip /tmp/op_ext

  echo "✅ [Tier 0] 1Password CLI provisioned successfully."
fi
