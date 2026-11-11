#!/bin/sh
# Source reads only check for mise. Installation requires an explicit --install.
# No arguments must stay read-only: previously generated configs use that form.
# POSIX shell keeps this path available before the managed shell environment exists.
# [Reference]: https://www.chezmoi.io/reference/configuration-file/hooks/
# [Reference]: https://mise.jdx.dev/installing-mise.html

set -eu

fatal() {
  echo "[Fatal] $*" >&2
  exit 1
}

[ "$#" -le 1 ] || fatal "Usage: $0 [--check|--install]"
case "${1---check}" in
  --check | --install) mode=${1---check} ;;
  *) fatal "Usage: $0 [--check|--install]" ;;
esac

[ -n "${HOME:-}" ] || fatal "HOME is required to locate mise."

SCRIPT_DIR=$(
  unset CDPATH
  cd "$(dirname "$0")" && pwd -P
) || fatal "Unable to resolve bootstrap source directory."

LOCAL_BIN="$HOME/.local/bin"
MISE_BIN="$LOCAL_BIN/mise"

if [ "$mode" = "--check" ]; then
  # Do not execute mise (even --version), read the pin, mkdir, chmod or fetch.
  # A usable file/symlink is enough here; tool compatibility is a separate check.
  if [ -f "$MISE_BIN" ] && [ -x "$MISE_BIN" ]; then
    exit 0
  fi
  fatal "Executable mise required at $MISE_BIN. Nothing was changed. If absent, run: sh \"$SCRIPT_DIR/.bootstrap-mise.sh\" --install. If present but unusable, inspect its owner/type/mode and repair it explicitly."
fi

VERSION_FILE="$SCRIPT_DIR/.mise-version"

[ -r "$VERSION_FILE" ] || fatal "mise version pin not readable: $VERSION_FILE"
MISE_VERSION=$(
  awk '
    /^[0-9]+[.][0-9]+[.][0-9]+$/ {
      version = $0
      count += 1
      next
    }
    {
      count += 1
      invalid = 1
    }
    END {
      if (count == 1 && invalid != 1) {
        print version
      } else {
        exit 1
      }
    }
  ' "$VERSION_FILE"
) || fatal ".mise-version must contain exactly one plain mise version like 2026.5.4."

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
  fatal "mise at $MISE_BIN is $current_version; pin is $MISE_VERSION. Existing mise was preserved. Decide whether to adopt its version in .mise-version or replace it explicitly through its owner before retrying."
elif [ "$target_exists" = "true" ]; then
  fatal "Existing mise at $MISE_BIN is not executable or did not report a version. Inspect its owner/type/mode and repair it explicitly; nothing was replaced."
else
  echo "[Bootstrap] Installing mise $MISE_VERSION at $MISE_BIN." >&2
fi

if ! command -v curl > /dev/null 2>&1; then
  fatal "curl is required to bootstrap mise."
fi

mkdir -p "$LOCAL_BIN" || fatal "Unable to create $LOCAL_BIN."
[ -d "$LOCAL_BIN" ] || fatal "$LOCAL_BIN is not a directory."
[ -w "$LOCAL_BIN" ] || fatal "$LOCAL_BIN is not writable."

tmp_installer=$(mktemp "${TMPDIR:-/tmp}/mise-install.XXXXXX") || fatal "Unable to create temporary installer file."
trap 'rm -f "$tmp_installer"' 0 HUP INT TERM

curl -fsSL https://mise.run -o "$tmp_installer" || fatal "Failed to download mise installer."
MISE_INSTALL_PATH="$MISE_BIN" MISE_VERSION="$MISE_VERSION" sh "$tmp_installer" || fatal "mise installer failed."
chmod +x "$MISE_BIN" || fatal "Unable to make $MISE_BIN executable."

installed_version=$(mise_reported_version) || fatal "Installed mise did not report a version."
if [ "$installed_version" != "$MISE_VERSION" ]; then
  fatal "Installed mise version $installed_version does not match $MISE_VERSION."
fi
