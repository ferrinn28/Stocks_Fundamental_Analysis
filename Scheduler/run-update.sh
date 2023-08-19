#!/usr/bin/env bash
set -e
source "/ferrin/update-data/venv/bin/activate"

# Print Python interpreter and virtual environment path
# echo "Python Interpreter: $(which python)"
# echo "Virtual Environment Path: $VIRTUAL_ENV"

# Run Python Script
python3 /ferrin/update-data/update-db-idxhidiv20.py > update-idxhidiv20.log

# Deactivate virtual environment (optional)
deactivate

echo "The program is already running"
