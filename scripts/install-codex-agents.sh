#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/integrations/codex/agents"
DEST="${CODEX_HOME:-$HOME/.codex}/agents"

if [[ ! -d "$SRC" ]]; then
  echo "Codex agent source directory not found: $SRC" >&2
  exit 1
fi

python3 - "$SRC" <<'PY'
import pathlib, sys, tomllib
root = pathlib.Path(sys.argv[1])
files = sorted(root.glob("*.toml"))
if not files:
    raise SystemExit("No Codex agent TOML files found")
required = {"name", "description", "developer_instructions"}
for path in files:
    data = tomllib.loads(path.read_text(encoding="utf-8"))
    missing = required - data.keys()
    if missing:
        raise SystemExit(f"{path.name}: missing {sorted(missing)}")
print(f"Validated {len(files)} Codex agents")
PY

mkdir -p "$DEST"
cp "$SRC"/*.toml "$DEST"/
echo "Installed Luna Codex agents to $DEST"
