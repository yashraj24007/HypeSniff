#!/usr/bin/env bash
# Build script for Render: install dependencies and pre-render notebook

set -e  # Exit on error

echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "Installing ipykernel for notebook execution..."
pip install ipykernel

echo "Pre-rendering notebook to HTML..."
python -m nbconvert --to html --execute DAV_project_1_v2.ipynb --output notebook_output.html --ExecutePreprocessor.timeout=600

echo "Build complete!"
