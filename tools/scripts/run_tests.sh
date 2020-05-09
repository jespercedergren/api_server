test_arg=$1

test_folder="$(pwd)/tests"

if [ "$test_arg" == "" ] ; then
  echo "Running unit and integration tests."
  # unit tests
  docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$test_folder",target=/tests test_base pipenv run -m pytest tests/unit_tests/ -s
  # integration tests
  docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$test_folder",target=/tests test_base pipenv run -m pytest tests/integration_tests/ -s
else
  echo "Running $test_arg."
  docker run -it -e test_env='docker' --network api_default --mount type=bind,src="$test_folder",target=/tests test_base pipenv run -m pytest "tests/$test_arg" -s
fi
