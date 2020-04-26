build: clean deps

build_dev_schema: clean

.PHONY: clean
clean:
	-find . -type f -name "*.pyc" -delete
	-find . -type f -name "*.cover" -delete

.PHONY: docker_build_test_base
docker_build_test_base:
	./tools/scripts/docker_build_test_base.sh

.PHONY: docker_build_all
docker_build_all:
	./tools/scripts/docker_build_all.sh

.PHONY: spin_down
spin_down:
	./tools/scripts/spin_down.sh

.PHONY: spin_up
spin_up:
	./tools/scripts/spin_up.sh

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
