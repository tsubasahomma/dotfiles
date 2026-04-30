#!/bin/sh
# Tier -1 and Tier 0 bootstrap ensure mise exists before chezmoi hooks run.
# POSIX shell keeps this path available before the managed shell environment exists.
# [Reference]: https://mise.jdx.dev/getting-started.html
# [Reference]: https://mise.jdx.dev/configuration.html#mise-trusted-config-paths

set -eu

if [ "${CI:-false}" = "true" ]; then
  exit 0
fi

# --- Phase: Tier -1 (Environment Discovery) ---
LOCAL_BIN="$HOME/.local/bin"
MISE_SHIMS="$HOME/.local/share/mise/shims"
mkdir -p "$LOCAL_BIN"

# Add mise shims and the local bin directory for hook execution.
export PATH="$MISE_SHIMS:$LOCAL_BIN:$PATH"

# Resolve the mise binary before installing it as a fallback.
if command -v mise > /dev/null 2>&1; then
  MISE_BIN=$(command -v mise)
else
  MISE_BIN="$LOCAL_BIN/mise"
  if [ ! -f "$MISE_BIN" ]; then
    echo "📦 [Tier 0] Provisioning Hermetic mise..." >&2
    if ! command -v curl > /dev/null 2>&1; then
      echo "❌ [Assertion Failure] 'curl' is required to bootstrap mise." >&2
      exit 1
    fi
    curl -fsSL https://mise.run | MISE_INSTALL_PATH="$MISE_BIN" sh
    chmod +x "$MISE_BIN"
  fi
fi

# --- Phase: Tier 0 (Environment Convergence) ---
# Suppress interactive prompts during bootstrap.
export MISE_YES=1
export MISE_QUIET=1

# Trust the source directory before running install.
# This prevents interactive "Trust this file?" prompts.
export MISE_TRUSTED_CONFIG_PATHS="$HOME/.local/share/chezmoi"

# Use a temporary mise config so bootstrap dependencies stay isolated.
_MISE_SANDBOX=$(mktemp -d)
trap 'rm -rf "$_MISE_SANDBOX"' EXIT
export MISE_GLOBAL_CONFIG_FILE="$_MISE_SANDBOX/config.toml"

# Trust the repository source state before installing tools.
"$MISE_BIN" trust "$HOME/.local/share/chezmoi"

# Stay silent on success; only errors should produce output.
env XDG_CONFIG_HOME="$_MISE_SANDBOX" "$MISE_BIN" install
