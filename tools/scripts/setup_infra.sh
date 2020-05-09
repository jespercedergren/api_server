echo "setting up infra"
#docker exec -it docker_test /bin/bash -c ""
docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/tests",target=/tests --mount type=bind,src="$(pwd)/tests/setup/setup_infra.py",target=/tests/setup/setup_infra.py docker_test_base pipenv run python /tests/setup/setup_infra.py