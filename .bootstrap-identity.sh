#!/bin/sh
# [Architecture]: Tier -1 & 0 Bootstrapping (Sovereign Provisioning)
# [Reference]: https://www.chezmoi.io/reference/configuration-file/hooks/
# [Reference]: https://mise.jdx.dev/getting-started.html
# [Rationale]: Pure POSIX script to ensure 'mise' exists. Enforces strict silent idempotency.

set -eu

if [ "${CI:-false}" = "true" ]; then
  exit 0
fi #

# --- Phase: Tier -1 (Assertion Gate) ---
if ! command -v curl > /dev/null 2>&1; then
  echo "❌ [Assertion Failure] 'curl' is required to bootstrap the sovereign infrastructure." >&2
  exit 1
fi

# --- Phase: Tier 0 (Environment Setup) ---
LOCAL_BIN="$HOME/.local/bin"
mkdir -p "$LOCAL_BIN"
export PATH="$LOCAL_BIN:$PATH"

# [Architecture]: Deterministic Binary Placement
# [Rationale]: Explicitly sets MISE_INSTALL_PATH to avoid location drift depending on shell state.
MISE_BIN="$LOCAL_BIN/mise"

if ! command -v mise > /dev/null 2>&1; then
  echo "📦 [Tier 0] Provisioning Hermetic mise..." >&2
  curl -fsSL https://mise.run | MISE_INSTALL_PATH="$MISE_BIN" sh
fi

# [Architecture]: Synchronous & Silent Tier 0 Convergence
# [Rationale]:
# MISE_YES=1 bypasses interactive prompts.
# MISE_QUIET=1 suppresses output if the toolchain is already converged.
export MISE_YES=1
export MISE_QUIET=1

# Ensure the binary is executable and run the Tier 0 install defined in .mise.toml
chmod +x "$MISE_BIN"
"$MISE_BIN" install
