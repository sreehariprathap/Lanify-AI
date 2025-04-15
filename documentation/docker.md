# Lanify-AI Docker Guide

This README provides comprehensive instructions for Docker operations in the Lanify-AI project, including building, pushing, running, and stopping containers.

## Prerequisites
- Docker installed
- Docker Compose installed

## Project Structure
lanify-AI/
├── dev/
│   ├── Dockerfile              # Main multi-stage Dockerfile
│   ├── entrypoint.sh           # Container startup script
│   ├── nginx.conf              # NGINX configuration
│   ├── requirements.txt        # Python dependencies
│   ├── lanifyAI/               # Frontend source code
│   ├── ai_models/              # ML models and training pipeline
│   └── docker/
│       └── docker-compose.yml  # Service orchestration

## Docker Operations

### Building the Application Image
Navigate to the `dev` directory and build the Docker image:

```bash
# Replace with your build command if different
docker build -t lanify-ai .
```

#### Tagging for Container Registry
*(Add tagging instructions here.)*

#### Pushing to Container Registry
*(Add pushing instructions here.)*

### Starting the Services
Navigate to the Docker Compose directory and start all services:

```bash
docker-compose up -d
```

This command starts:
- The Lanify application on port 3000
- PostgreSQL database on port 5432
- MLflow tracking server on port 5000

#### Viewing Running Containers
Use the following command to view all running containers:

```bash
docker ps
```

#### Viewing Service Logs
To view logs for all services, run:

```bash
docker-compose logs
```

To follow logs for a specific service, run:

```bash
docker-compose logs -f <service_name>
```

### Stopping the Services
Stop all services while preserving volumes:

```bash
docker-compose down
```

Stop all services and remove volumes:

```bash
docker-compose down -v
```

## MLflow Integration

### MLflow Configuration
MLflow is configured in the `docker-compose.yml` file as a separate service. Due to compatibility issues with the original image reference, use one of these alternatives:
- **Option 1:** Use GitHub Container Registry
- **Option 2:** Build from a Python image

### Accessing MLflow UI
Once the services are running, access the MLflow UI at:
```
http://<host>:5000
```

### Integrating with Training Pipeline
The training pipeline automatically logs metrics and models to MLflow. No additional configuration is needed as long as the MLflow server is running and accessible.

## Troubleshooting

### Container Fails to Start
Check the logs for detailed error messages.

### MLflow Connection Issues
- Verify that the MLflow container is running.
- Ensure your training code uses the correct tracking URI.

### Database Connection Issues
- Check if PostgreSQL is running.
- Verify connection parameters in your application configuration.

## Advanced Operations

### Accessing Container Shell
To open a shell into a running container, use:

```bash
docker exec -it <container_name> /bin/bash
```

### Inspecting Container Resources
*(Add instructions as necessary.)*

### Updating Services
To update a service after making changes, run:

```bash
docker-compose up -d --build <service_name>
```

This command rebuilds and restarts only the specified service.
