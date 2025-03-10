#!/bin/sh
cd /app/dev
python -m flask db upgrade
python app.py
