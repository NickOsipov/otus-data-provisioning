#!/bin/bash
set -e

# Activate virtual environment
source /app/.venv/bin/activate

# Start Jupyter notebook using python module
python -m jupyter notebook --ip=0.0.0.0 --port=8888 --no-browser --allow-root --NotebookApp.token=''