./tools/scripts/docker_build_test_base.sh
docker-compose -f api/docker-compose.yml up --build
docker-compose -f tools/docker/server/docker-compose.yml up --build
