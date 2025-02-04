#!/bin/bash

echo "[[ Running tests... ]]"
python -m pytest -s

echo "[[ Starting API... ]]"
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
