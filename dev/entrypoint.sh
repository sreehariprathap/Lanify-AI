#!/bin/sh
set -e

# Start nginx
service nginx start || echo "Failed to start nginx"

# Change to application directory
cd /app/dev

# Run database migrations
python -m flask db upgrade

# Start the application
python app.py
