#!/bin/sh
# [Architecture]: Tier -1 & 0 Bootstrapping (Assertion Gate & Identity Provisioning)
# [Rationale]: Pure POSIX script executed via hooks.read-source-state.pre.
# [Fix]: Silent-by-default to prevent stdout pollution during 'chezmoi status'.

set -eu

if [ "${CI:-false}" = "true" ]; then
  exit 0
fi

# --- Tier -1: Silent Assertion Gate ---
if ! command -v curl > /dev/null 2>&1; then
  echo "❌ [Fatal] 'curl' is missing." >&2
  echo "👉 Action Required: Install curl via your OS package manager and retry." >&2
  exit 1
fi

if ! command -v unzip > /dev/null 2>&1 && ! command -v python3 > /dev/null 2>&1; then
  echo "❌ [Fatal] Neither 'unzip' nor 'python3' is available for archive extraction." >&2
  echo "👉 Action Required: Install unzip via your OS package manager and retry." >&2
  exit 1
fi

LOCAL_BIN="$HOME/.local/bin"
OP_BIN="$LOCAL_BIN/op"

# --- Tier 0: Identity Provisioning ---
if [ ! -x "$OP_BIN" ]; then
  # [Rationale]: Output ONLY occurs during active provisioning, redirected to stderr.
  echo "🔐 [Tier 0] Provisioning 1Password CLI (Identity Anchor)..." >&2
  mkdir -p "$LOCAL_BIN"

  OS_ID=$(uname -s | tr '[:upper:]' '[:lower:]')
  ARCH_ID=$(uname -m)
  if [ "$ARCH_ID" = "x86_64" ]; then
    ARCH_ID="amd64"
  elif [ "$ARCH_ID" = "aarch64" ] || [ "$ARCH_ID" = "arm64" ]; then
    ARCH_ID="arm64"
  fi

  TOOLS_YAML="$(dirname "$0")/.chezmoidata/tools.yaml"
  if [ ! -f "$TOOLS_YAML" ]; then
    echo "❌ [Fatal] tools.yaml not found at $TOOLS_YAML" >&2
    exit 1
  fi

  OP_VERSION=$(awk '/^ *"op":/ {gsub(/"/, "", $2); print $2}' "$TOOLS_YAML")
  OP_HASH=$(awk "/^ *op_hashes:/{f=1} f && /^ *${OS_ID}-${ARCH_ID}:/{gsub(/\"/, \"\", \$2); print \$2; exit}" "$TOOLS_YAML")

  if [ -z "$OP_VERSION" ]; then
    echo "❌ [Fatal] Could not parse op version from tools.yaml" >&2
    exit 1
  fi

  OP_URL="https://cache.agilebits.com/dist/1P/op2/pkg/v${OP_VERSION}/op_${OS_ID}_${ARCH_ID}_v${OP_VERSION}.zip"
  curl -fsSL "$OP_URL" -o /tmp/op.zip

  if [ -n "$OP_HASH" ]; then
    ACTUAL_HASH=$(sha256sum /tmp/op.zip 2> /dev/null | cut -d' ' -f1 || shasum -a 256 /tmp/op.zip | cut -d' ' -f1)
    if [ "$ACTUAL_HASH" != "$OP_HASH" ]; then
      echo "❌ [Fatal] 1Password CLI hash mismatch." >&2
      echo "Expected: $OP_HASH" >&2
      echo "Actual:   $ACTUAL_HASH" >&2
      rm -f /tmp/op.zip
      exit 1
    fi
  else
    echo "⚠️  [Warning] Hash for ${OS_ID}-${ARCH_ID} not found. Bypassing verification." >&2
  fi

  if command -v unzip > /dev/null 2>&1; then
    unzip -q -o /tmp/op.zip -d /tmp/op_ext
  else
    python3 -m zipfile -e /tmp/op.zip /tmp/op_ext
  fi

  mv /tmp/op_ext/op "$OP_BIN"
  chmod +x "$OP_BIN"
  rm -rf /tmp/op.zip /tmp/op_ext

  echo "✅ [Tier 0] 1Password CLI provisioned successfully." >&2
fi
