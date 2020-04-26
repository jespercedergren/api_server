# spin down services
docker-compose -f ./tools/docker/server/docker-compose.yml down --remove-orphans
docker-compose -f ./api/docker-compose.yml down --remove-orphans
