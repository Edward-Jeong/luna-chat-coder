#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/integrations/codex/agents"
DEST="${CODEX_HOME:-$HOME/.codex}/agents"

if [[ ! -d "$SRC" ]]; then
  echo "Codex agent source directory not found: $SRC" >&2
  exit 1
fi

shopt -s nullglob
files=("$SRC"/*.toml)
if (( ${#files[@]} == 0 )); then
  echo "No Codex agent TOML files found" >&2
  exit 1
fi

for file in "${files[@]}"; do
  for required in name description developer_instructions; do
    if ! grep -Eq "^[[:space:]]*${required}[[:space:]]*=" "$file"; then
      echo "$(basename "$file"): missing $required" >&2
      exit 1
    fi
  done
done

echo "Validated ${#files[@]} Codex agents"
mkdir -p "$DEST"
installed=0
preserved=0
for file in "${files[@]}"; do
  target="$DEST/$(basename "$file")"
  if [[ -e "$target" || -L "$target" ]]; then
    echo "Preserved existing: $target"
    preserved=$((preserved + 1))
    continue
  fi
  # Exclusive creation also protects a file created after the existence check.
  if (set -o noclobber; cat "$file" > "$target"); then
    installed=$((installed + 1))
  elif [[ -e "$target" || -L "$target" ]]; then
    echo "Installation failed or target appeared during installation: $target" >&2
    exit 1
  else
    echo "Could not install: $target" >&2
    exit 1
  fi
done
echo "Installed $installed; preserved $preserved existing Luna Codex agents in $DEST"
