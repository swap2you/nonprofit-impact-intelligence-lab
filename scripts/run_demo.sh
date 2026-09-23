#!/usr/bin/env bash
set -e
python scripts/generate_data.py
uvicorn api.main:app --reload &
streamlit run app/dashboard.py
