# Makefile
.PHONY: build run up stop clean logs sh restart

# Docker-related variables
DOCKER_COMPOSE = docker-compose
DOCKERFILE = Dockerfile

# Build the Docker image
build:
	$(DOCKER_COMPOSE) build

# Run the Docker container
run:
	$(DOCKER_COMPOSE) up -d

# Build and run the Docker container
up:
	$(DOCKER_COMPOSE) up --build -d

# Stop and remove the Docker container
stop:
	$(DOCKER_COMPOSE) down

# Clean up Docker images and volumes
clean:
	$(DOCKER_COMPOSE) down -v --rmi all

# View the logs
logs:
	$(DOCKER_COMPOSE) logs --tail=100 -f

# Container shell
sh:
	$(DOCKER_COMPOSE) exec app sh

# Restart the container
restart: clean up