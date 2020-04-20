# spin down services
docker-compose -f ../server/docker-compose.yml down --remove-orphans
docker-compose -f ../../api/docker-compose.yml down --remove-orphans

# spin up services
docker-compose -f ../../api/docker-compose.yml up -d
docker-compose -f ../server/docker-compose.yml up -d

sleep 5

# unit tests
docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/../../clients",target=/clients --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/unit_tests/
#docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/unit_tests/
#docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/unit_tests/test_s3_localstack.py
#docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/unit_tests/test_s3_minio.py

# integration tests
#docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/../../clients",target=/clients --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/integration_tests/
docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/..",target=/tests test_base python3.7 -m pytest tests/integration_tests/

# spin down services
docker-compose -f ../server/docker-compose.yml down --remove-orphans
docker-compose -f ../../api/docker-compose.yml down --remove-orphans