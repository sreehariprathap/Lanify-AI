#######################################################################
# Dockerfile Documentation
#
# This Dockerfile uses a multi-stage build process to create a container
# image that integrates a Node.js frontend and a Python backend with NGINX.
#
# Stage 1 - Frontend Build:
# • Based on the official Node.js 20-alpine image.
# • Sets the working directory to /app/frontend.
# • Copies package.json and package-lock.json to leverage Docker caching.
# • Installs Node.js dependencies using npm ci.
# • Copies the remainder of the frontend source code.
# • Executes the build process using the "npm run build" command.
#
# Stage 2 - Final Image Setup:
# • Uses the python:3.9-slim image as the base.
# • Sets the working directory to /app/dev.
# • Installs NGINX from the package manager.
# • Copies the Python requirements and installs backend dependencies.
# • Copies a custom NGINX configuration file to /etc/nginx/conf.d/app.conf.
# • Adds remaining backend application files and removes the frontend source
#   code directory as it's no longer needed.
# • Copies the frontend build output from the first stage to /app/frontend.
# • Exposes port 3000.
# • Sets the entry point to run "entrypoint.sh", which starts the backend service.
#######################################################################
# Stage 1: Build the frontend
FROM node:20-alpine AS frontend-build

WORKDIR /app/frontend

# Copy package.json and package-lock.json first for caching
COPY lanifyAI/package*.json ./

RUN npm ci

# Copy the rest of the frontend code
COPY ./lanifyAI .

# Build the application
RUN npm run build

# Stage 2
FROM python:3.9-slim

WORKDIR /app/dev

# Install nginx
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy nginx configuration
COPY nginx.conf /etc/nginx/conf.d/app.conf

COPY . .
RUN rm -rf lanifyAI

# Copy frontend build output
COPY --from=frontend-build /app/frontend/dist /app/frontend

EXPOSE 3000
EXPOSE 5000

# Start the backend
ENTRYPOINT ["sh", "entrypoint.sh"]
