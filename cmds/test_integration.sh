#!/bin/bash

# Clean Docker
docker-compose down && docker image prune -a -f && docker volume prune -f && docker system prune -f

# Copy Docker
rm -rf docker-compose.yml && cat docker/test/docker-compose.yml >> docker-compose.yml

# Copy .env
rm -rf .env && cat ./env/test/.env >> .env

# Make script executable
chmod +x ./scripts/test/postgresql/init.sh

# Up Docker
docker-compose up -d --remove-orphans

# Run integration test
poetry run pytest test/integration/
