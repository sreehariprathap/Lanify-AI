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

# Start the backend
ENTRYPOINT ["sh", "entrypoint.sh"]
