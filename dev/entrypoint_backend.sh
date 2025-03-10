#!/bin/sh
cd /app/dev
flask db upgrade
python app.py
