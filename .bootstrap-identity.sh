#!/bin/sh
# [Architecture]: Tier -1 & 0 Bootstrapping (Sovereign Provisioning)
# [Rationale]: Pure POSIX script to ensure 'mise' exists and is correctly resolved.
# [Reference]: https://mise.jdx.dev/getting-started.html
# [Reference]: https://www.chezmoi.io/user-guide/advanced/install-your-password-manager-on-init/

set -eu

if [ "${CI:-false}" = "true" ]; then
  exit 0
fi

# --- Phase: Tier -1 (Environment Discovery) ---
LOCAL_BIN="$HOME/.local/bin"
MISE_SHIMS="$HOME/.local/share/mise/shims"
mkdir -p "$LOCAL_BIN"

# [Architecture]: Inject shims and local bin into PATH for hook execution.
export PATH="$MISE_SHIMS:$LOCAL_BIN:$PATH"

# [Architecture]: Deterministic Binary Discovery
# [Rationale]: Prioritize existing system/local mise before attempting installation.
if command -v mise >/dev/null 2>&1; then
  MISE_BIN=$(command -v mise)
else
  MISE_BIN="$LOCAL_BIN/mise"
  if [ ! -f "$MISE_BIN" ]; then
    echo "📦 [Tier 0] Provisioning Hermetic mise..." >&2
    if ! command -v curl >/dev/null 2>&1; then
      echo "❌ [Assertion Failure] 'curl' is required to bootstrap mise." >&2
      exit 1
    fi
    curl -fsSL https://mise.run | MISE_INSTALL_PATH="$MISE_BIN" sh
    chmod +x "$MISE_BIN"
  fi
fi

# --- Phase: Tier 0 (Environment Convergence) ---
export MISE_YES=1
export MISE_QUIET=1

# [Architecture]: Strict Dependency Isolation (Sandboxing)
# [Rationale]: Breaks the circular dependency deadlock. By temporarily re-routing
# XDG_CONFIG_HOME to an ephemeral directory, mise is forced to evaluate ONLY the
# deterministic Tier 0 .mise.toml in the current working directory.
_MISE_SANDBOX=$(mktemp -d)
trap 'rm -rf "$_MISE_SANDBOX"' EXIT

# [Architecture]: Tier 0 (Bootstrap Isolation)
# [Rationale]: Force mise to ignore any existing global configuration by
# re-routing MISE_GLOBAL_CONFIG_FILE to a non-existent path in the sandbox.
# This ensures target-side "poisoned" configs cannot break the bootstrap.
export MISE_GLOBAL_CONFIG_FILE="$_MISE_SANDBOX/config.toml"

# [Rationale]: Silicon on success. No echo is emitted unless an error occurs.
env XDG_CONFIG_HOME="$_MISE_SANDBOX" "$MISE_BIN" install
