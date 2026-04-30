#!/usr/bin/env bash
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

python_cmd="${PYTHON:-python3}"
"$python_cmd" -m pip install --user .

echo "Installed SpotiTerm."
echo "Run: spotiterm \"night drive\""
echo "If spotiterm is not found, add Python's user bin directory to PATH."
