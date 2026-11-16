#!/bin/sh
# First install on a machine that chezmoi does not manage yet, in one command:
#   git clone https://github.com/tsubasahomma/dotfiles.git ~/.local/share/chezmoi &&
#     sh ~/.local/share/chezmoi/.first-install.sh
# It runs the documented steps in order: check prerequisites, install the pinned
# mise, install the pinned chezmoi through mise, init, apply, then diagnose.
# It stops at the first failure and never re-initializes a machine that already
# has a chezmoi config. The leading dot keeps chezmoi from deploying it.
# It runs from a clone, not `curl | sh`, so what runs is the commit you checked out.
# [Reference]: docs/operations.md#first-install
# [Reference]: https://www.chezmoi.io/reference/commands/init/

set -eu

fatal() {
  echo "[Fatal] $*" >&2
  exit 1
}

step() {
  echo "[First install] $*" >&2
}

[ "$#" -eq 0 ] || fatal "Usage: $0 (no arguments)"
[ -n "${HOME:-}" ] || fatal "HOME is required."

SOURCE_DIR=$(
  unset CDPATH
  cd "$(dirname "$0")" && pwd -P
) || fatal "Unable to resolve the source directory."

CONFIG_FILE="${XDG_CONFIG_HOME:-$HOME/.config}/chezmoi/chezmoi.toml"
if [ -e "$CONFIG_FILE" ]; then
  fatal "$CONFIG_FILE already exists. This entry is for the first install only; follow docs/operations.md for a managed machine."
fi

step "1/6 Checking prerequisites."
for command in git curl python3 ssh-keygen; do
  command -v "$command" > /dev/null 2>&1 || fatal "$command is required on PATH. See docs/operations.md#first-install."
done
python3 -c 'import sys; sys.exit(sys.version_info < (3, 9))' ||
  fatal "Python 3.9 or newer is required as python3."

step "2/6 Installing the pinned mise."
sh "$SOURCE_DIR/.bootstrap-mise.sh" --install
MISE_BIN="$HOME/.local/bin/mise"

step "3/6 Installing the pinned chezmoi from $SOURCE_DIR/.mise.toml."
# Trust this one file for these commands only; nothing records the trust.
MISE_TRUSTED_CONFIG_PATHS="$SOURCE_DIR/.mise.toml"
export MISE_TRUSTED_CONFIG_PATHS
"$MISE_BIN" -C "$SOURCE_DIR" install aqua:twpayne/chezmoi
CHEZMOI_BIN=$("$MISE_BIN" -C "$SOURCE_DIR" which chezmoi) ||
  fatal "mise did not resolve the pinned chezmoi."
unset MISE_TRUSTED_CONFIG_PATHS

step "4/6 Initializing the chezmoi config."
"$CHEZMOI_BIN" init --source "$SOURCE_DIR"

step "5/6 Applying the source state."
"$CHEZMOI_BIN" apply --source "$SOURCE_DIR"

step "6/6 Running the local diagnostics."
# Diagnostics must not install tools; set this before mise starts.
MISE_AUTO_INSTALL=false MISE_TASK_RUN_AUTO_INSTALL=false MISE_NOT_FOUND_AUTO_INSTALL=false \
  "$MISE_BIN" exec -- "$HOME/.local/bin/dotfiles-diagnose"

step "Done. Open a new shell to load the managed environment."
