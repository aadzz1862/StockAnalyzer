#!/usr/bin/env bash
set -e

# Create virtual environment if not present
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# Activate the virtual environment
source venv/bin/activate

# Ensure pip is up to date
pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt

# Initialize the database
python init_db.py

echo "Environment setup complete."
