#!/bin/sh
service nginx start
cd /app/dev
python -m flask db upgrade
python app.py
