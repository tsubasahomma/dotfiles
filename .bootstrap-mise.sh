#!/bin/sh
# Pre-source-state bootstrap ensures pinned mise exists before managed scripts need it.
# POSIX shell keeps this path available before the managed shell environment exists.
# [Reference]: https://www.chezmoi.io/reference/configuration-file/hooks/
# [Reference]: https://mise.jdx.dev/installing-mise.html

set -eu

fatal() {
  echo "[Fatal] $*" >&2
  exit 1
}

[ -n "${HOME:-}" ] || fatal "HOME is required to bootstrap mise."

SCRIPT_DIR=$(
  unset CDPATH
  cd "$(dirname "$0")" && pwd -P
) || fatal "Unable to resolve bootstrap source directory."
VERSION_FILE="$SCRIPT_DIR/.mise-version"

[ -r "$VERSION_FILE" ] || fatal "mise version pin not readable: $VERSION_FILE"
IFS= read -r MISE_VERSION < "$VERSION_FILE" || MISE_VERSION=""

case "$MISE_VERSION" in
  "" | *[!0123456789.]*)
    fatal "Invalid mise version pin in $VERSION_FILE."
    ;;
esac

LOCAL_BIN="$HOME/.local/bin"
MISE_BIN="$LOCAL_BIN/mise"

mkdir -p "$LOCAL_BIN" || fatal "Unable to create $LOCAL_BIN."
[ -d "$LOCAL_BIN" ] || fatal "$LOCAL_BIN is not a directory."
[ -w "$LOCAL_BIN" ] || fatal "$LOCAL_BIN is not writable."

target_exists=false
if ls -ld "$MISE_BIN" > /dev/null 2>&1; then
  target_exists=true
fi

if [ -L "$MISE_BIN" ]; then
  fatal "Refusing to repair symlink at $MISE_BIN."
fi

if [ "$target_exists" = "true" ] && [ ! -f "$MISE_BIN" ]; then
  fatal "Refusing to repair non-file at $MISE_BIN."
fi

mise_reported_version() {
  if [ ! -x "$MISE_BIN" ]; then
    return 1
  fi

  mise_version_output=$("$MISE_BIN" --version 2> /dev/null) || return 1
  mise_version=${mise_version_output%% *}
  [ -n "$mise_version" ] || return 1
  printf '%s\n' "$mise_version"
}

current_version=""
if current_version=$(mise_reported_version); then
  if [ "$current_version" = "$MISE_VERSION" ]; then
    exit 0
  fi
  echo "[Bootstrap] mise at $MISE_BIN is $current_version; repairing to $MISE_VERSION." >&2
elif [ "$target_exists" = "true" ]; then
  echo "[Bootstrap] mise at $MISE_BIN is not executable or did not report a version; repairing to $MISE_VERSION." >&2
else
  echo "[Bootstrap] Installing mise $MISE_VERSION at $MISE_BIN." >&2
fi

if [ "$target_exists" = "true" ] && [ ! -w "$MISE_BIN" ]; then
  fatal "Cannot repair $MISE_BIN because it is not writable."
fi

if ! command -v curl > /dev/null 2>&1; then
  fatal "curl is required to bootstrap mise."
fi

tmp_installer=$(mktemp "${TMPDIR:-/tmp}/mise-install.XXXXXX") || fatal "Unable to create temporary installer file."
trap 'rm -f "$tmp_installer"' 0 HUP INT TERM

curl -fsSL https://mise.run -o "$tmp_installer" || fatal "Failed to download mise installer."
MISE_INSTALL_PATH="$MISE_BIN" MISE_VERSION="$MISE_VERSION" sh "$tmp_installer" || fatal "mise installer failed."
chmod +x "$MISE_BIN" || fatal "Unable to make $MISE_BIN executable."

installed_version=$(mise_reported_version) || fatal "Installed mise did not report a version."
if [ "$installed_version" != "$MISE_VERSION" ]; then
  fatal "Installed mise version $installed_version does not match $MISE_VERSION."
fi
