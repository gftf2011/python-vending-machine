docker-compose down && docker image prune -a -f && docker volume rm $(docker volume ls -q) && docker system prune -f