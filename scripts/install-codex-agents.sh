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
cp "${files[@]}" "$DEST"/
echo "Installed Luna Codex agents to $DEST"
