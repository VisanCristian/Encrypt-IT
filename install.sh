#!/usr/bin/env bash
set -euo pipefail

# Always run from the repo root (the script's directory)
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Python3 could not be found. Please install Python 3 first!"
  exit 1
fi

# Create virtual environment if missing
if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  # Note for Debian/Ubuntu/Mint users: if this fails, install python3-venv (e.g., sudo apt install python3-venv)
  python3 -m venv .venv
fi

# Use venv's python directly (no activation needed inside the script)
VENV_PY="./.venv/bin/python"

echo "Upgrading pip..."
"$VENV_PY" -m pip install --upgrade pip

if [ -f "requirements.txt" ]; then
  echo "Installing requirements from requirements.txt..."
  "$VENV_PY" -m pip install -r requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

echo "Setup complete! You can now run the program with:"
echo "  source .venv/bin/activate"
echo "  python3 main.py"
