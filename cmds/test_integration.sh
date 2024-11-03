#!/bin/bash

# Remove python cache
find . | grep -E "(/__pycache__$|\.pyc$|\.pyo$)" | xargs rm -rf

# Clean Docker
docker-compose down && docker image prune -a -f && docker volume rm $(docker volume ls -q) && docker system prune -f

# Copy Docker
rm -rf docker-compose.yml || true
cat docker/test/docker-compose.yml >> docker-compose.yml

# Copy .env
rm -rf .env || true
cat ./env/test/.env >> .env

# Make script executable
chmod +x ./scripts/test/postgresql/init.sh

# Up Docker
docker-compose up -d --remove-orphans

# Run integration test
poetry run pytest test/integration/
