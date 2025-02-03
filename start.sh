#!/bin/bash

echo "[[ Running tests... ]]"
pytest

echo "[[ Starting API... ]]"
cd ./src
uvicorn api:app --host 0.0.0.0 --port 8000 --reload
