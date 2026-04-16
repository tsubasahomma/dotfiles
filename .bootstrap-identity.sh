#!/bin/sh
# [Architecture]: Tier -1 & 0 Bootstrapping (Sovereign Provisioning)
# [Rationale]: Pure POSIX script to ensure 'op' and 'mise' exist. Enforces strict silent idempotency.
# [Reference]: https://www.chezmoi.io/reference/configuration-file/hooks/

set -eu

if [ "${CI:-false}" = "true" ]; then
  exit 0
fi

# --- Environment Setup ---
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"
export PATH="$LOCAL_BIN:$PATH"

TOOLS_YAML="$(dirname "$0")/.chezmoidata/tools.yaml"

# --- Utility Functions ---
get_tool_version() {
  awk "/^ *\"$1\":/ {gsub(/\"/, \"\", \$2); print \$2}" "$TOOLS_YAML"
}

get_tool_hash() {
  awk "/^ *${1}_hashes:/{f=1} f && /^ *\"?$2\"?:/{gsub(/\"/, \"\", \$2); print \$2; exit}" "$TOOLS_YAML"
}

verify_hash() {
  file_path=$1
  expected_hash=$2
  if [ -z "$expected_hash" ]; then
    echo "⚠️  [Warning] No hash found for $file_path. Skipping verification." >&2
    return 0
  fi
  actual_hash=$(sha256sum "$file_path" 2> /dev/null | cut -d' ' -f1 || shasum -a 256 "$file_path" | cut -d' ' -f1)
  if [ "$actual_hash" != "$expected_hash" ]; then
    echo "❌ [Fatal] Hash mismatch for $file_path." >&2
    exit 1
  fi
}

install_op() {
  OP_VERSION=$(get_tool_version "op")
  OS_ID=$(uname -s | tr '[:upper:]' '[:lower:]')
  ARCH_ID=$(uname -m)
  [ "$ARCH_ID" = "x86_64" ] && ARCH_ID="amd64"
  [ "$ARCH_ID" = "aarch64" ] || [ "$ARCH_ID" = "arm64" ] && ARCH_ID="arm64"

  PLATFORM_KEY="${OS_ID}-${ARCH_ID}"
  OP_HASH=$(get_tool_hash "op" "$PLATFORM_KEY")

  echo "🔐 [Tier 0] Provisioning 1Password CLI v${OP_VERSION}..." >&2
  URL="https://cache.agilebits.com/dist/1P/op2/pkg/v${OP_VERSION}/op_${OS_ID}_${ARCH_ID}_v${OP_VERSION}.zip"
  curl -fsSL "$URL" -o /tmp/op.zip
  verify_hash "/tmp/op.zip" "$OP_HASH"

  if command -v unzip > /dev/null 2>&1; then
    unzip -q -o /tmp/op.zip -d /tmp/op_ext
  else
    python3 -m zipfile -e /tmp/op.zip /tmp/op_ext
  fi
  mv /tmp/op_ext/op "$LOCAL_BIN/op"
  chmod +x "$LOCAL_BIN/op"
  rm -rf /tmp/op.zip /tmp/op_ext
}

install_mise() {
  MISE_VERSION=$(get_tool_version "mise")
  OS_ID=$(uname -s | tr '[:upper:]' '[:lower:]')
  [ "$OS_ID" = "darwin" ] && OS_ID="macos"
  ARCH_ID=$(uname -m)
  [ "$ARCH_ID" = "x86_64" ] && ARCH_ID="x64"
  [ "$ARCH_ID" = "aarch64" ] || [ "$ARCH_ID" = "arm64" ] && ARCH_ID="arm64"

  PLATFORM_KEY="${OS_ID}-${ARCH_ID}"
  MISE_HASH=$(get_tool_hash "mise" "$PLATFORM_KEY")

  echo "📦 [Tier 0] Provisioning mise v${MISE_VERSION}..." >&2
  URL="https://github.com/jdx/mise/releases/download/v${MISE_VERSION}/mise-v${MISE_VERSION}-${OS_ID}-${ARCH_ID}"
  curl -fsSL "$URL" -o "$LOCAL_BIN/mise"
  verify_hash "$LOCAL_BIN/mise" "$MISE_HASH"
  chmod +x "$LOCAL_BIN/mise"
}

# --- Execution ---
MUTATED=false

if [ ! -x "$LOCAL_BIN/op" ]; then
  install_op
  MUTATED=true
fi

if [ ! -x "$LOCAL_BIN/mise" ]; then
  install_mise
  MUTATED=true
fi

if [ "$MUTATED" = "true" ]; then
  echo "✅ [Tier 0] Bootstrap binaries converged." >&2
fi
