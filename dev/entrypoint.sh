#!/bin/sh
set -e

# Start nginx
service nginx start || echo "Failed to start nginx"

# Start MLflow UI in the background
mlflow ui --backend-store-uri /app/mlruns --host 0.0.0.0 --port 5000 &

# Change to application directory
cd /app/dev

# Run database migrations
python -m flask db upgrade

# Start the application
python app.py
