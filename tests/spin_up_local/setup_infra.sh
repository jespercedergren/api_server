echo "setting up infra"
docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$(pwd)/../../clients",target=/clients --mount type=bind,src="$(pwd)/..",target=/tests --mount type=bind,src="$(pwd)/setup_infra.py",target=/setup_infra.py test_base python3.7 /setup_infra.py
