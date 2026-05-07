#!/bin/sh
# Migration shim for already-rendered chezmoi configs that still point here.
# New hook wiring uses .bootstrap-mise.sh.

set -eu

SCRIPT_DIR=$(CDPATH= cd "$(dirname "$0")" && pwd)
exec "$SCRIPT_DIR/.bootstrap-mise.sh" "$@"
