build: clean deps

build_dev_schema: clean

.PHONY: update
update:
	pipenv update --dev --python 3.7

.PHONY: clean
clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type f -name "*.cover" -delete

.PHONY: deps
deps:
	pipenv sync --dev --python 3.7

.PHONY: pythonpath
pythonpath:
	echo "PYTHONPATH=${PWD}/api/:${PWD}/web/:${PWD}/tests/" >> .env

.PHONY: pre_commit_py37
pre_commit_py37:
	pipenv run pre-commit

.PHONY: docker_build_test_base
docker_build_test_base:
	./tools/scripts/docker_build_test_base.sh

.PHONY: spin_down_docker_build_test_base
spin_down_docker_build_test_base:
	docker-compose -f tools/docker/docker_images/docker-compose-docker-images.yaml down

.PHONY: spin_up_docker_build_test_base
spin_up_docker_build_test_base:
	docker-compose -f tools/docker/docker_images/docker-compose-docker-images.yaml up

.PHONY: docker_build_all
docker_build_all:
	./tools/scripts/docker_build_all.sh

.PHONY: verify_ports
verify_ports:
	./tools/scripts/verify_ports.sh

.PHONY: setup_infra
setup_infra:
	./tools/scripts/setup_infra.sh

.PHONY: run_tests_clean
run_tests_clean:
	./tools/scripts/run_tests_clean.sh ${test_name}

.PHONY: run_tests
run_tests:
	./tools/scripts/run_tests.sh ${test_name}

.PHONY: test_container
test_container:
	./tools/scripts/test_container.sh ${container_argument}

.PHONY: clear-tools-docker-images
clear-tools-docker-images:
	docker rmi -f docker_images_python_spark_hadoop_base docker_images_python_base docker_images_test