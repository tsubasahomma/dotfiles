#!/bin/sh
# Pre-source-state bootstrap ensures mise exists before managed scripts need it.
# POSIX shell keeps this path available before the managed shell environment exists.
# [Reference]: https://www.chezmoi.io/reference/configuration-file/hooks/
# [Reference]: https://mise.jdx.dev/installing-mise.html

set -eu

if [ "${CI:-false}" = "true" ]; then
  exit 0
fi

LOCAL_BIN="$HOME/.local/bin"
MISE_BIN="$LOCAL_BIN/mise"

mkdir -p "$LOCAL_BIN"

export PATH="$LOCAL_BIN:$PATH"

if command -v mise > /dev/null 2>&1; then
  exit 0
fi

if [ -f "$MISE_BIN" ]; then
  chmod +x "$MISE_BIN"
  exit 0
fi

if ! command -v curl > /dev/null 2>&1; then
  echo "[Fatal] curl is required to bootstrap mise." >&2
  exit 1
fi

echo "[Bootstrap] Installing mise at $MISE_BIN." >&2
curl -fsSL https://mise.run | MISE_INSTALL_PATH="$MISE_BIN" sh
chmod +x "$MISE_BIN"
