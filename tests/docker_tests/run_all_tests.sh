# spin down services
docker-compose -f ../server/docker-compose.yml down --remove-orphans
docker-compose -f ../../api/docker-compose.yml down --remove-orphans

# spin up services
docker-compose -f ../../api/docker-compose.yml up -d
docker-compose -f ../server/docker-compose.yml up -d

sleep 10

# unit tests
#docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/../../clients",target=/clients --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/unit_tests/

# integration tests
#docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/integration_tests/
docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/integration_tests/api/test_api_read_s3.py -s
docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/integration_tests/api/test_api_read_dynamodb.py -s

# spin down services
docker-compose -f ../server/docker-compose.yml down --remove-orphans
docker-compose -f ../../api/docker-compose.yml down --remove-orphans