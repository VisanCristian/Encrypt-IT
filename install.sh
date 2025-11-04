#!/bin/bash

# Stop on errors
set -e

if ! command -v python3 &> /dev/null
then
    echo "Python3 could not be found. PLease install python3 first!"
    exit 1
fi

# Create a virtual environment to run the script

if [ ! -d ".venv" ]; then
  echo "Creating virtual environment..."
  python3 -m venv .venv
fi

# Activating the virtual environment

echo "Activating virtual environment..."

source .venv/bin/activate

# Upgrade pip

echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements

if [ -f "requirements.txt " ]; then
  echo "Installing requirements from requirements.txt..."
  pip install -r requirements.txt
else
  echo "requirements.txt not found!"
  exit 1
fi

echo "Setup complete! You can now run the program with:"
echo " source .venv/bin/activate"
echo " python main.py"