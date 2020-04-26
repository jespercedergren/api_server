# Tests

The tests can be run using pytest both on a local machine and in docker.

### Environment
In the ```__init__.py``` file the variable ```test_env``` is set to indicate whether the tests should run on a local machine
or whether the tests are running in docker.
The test_env can be set to either ```local``` or ```docker```.

### Config
Depending on what value the test_env has the endpoint_urls and hosts are set differently in config.py.
This enables tests to communicate with the mocked services from within our outside the docker network.
It also enables the necessary infrastructure within the mocked services to be set up and torn down as defined in
conftest.py.

The API tests run using asyncio to asynchronously send json data to a specified url.

### Mocked services
The server with the mocked services are spun up using docker compose in ```tools/docker/server```.
The services are attached to the same docker network as the api ```api_default```.
Localstack are used to mock the AWS services, where all services used are available on port ```4566```.
When reading from localstack s3 using Spark is set to use port ```4573```.

Minio is also included as an alternative for s3.

Logstash is used for experimental purposes and is configured to send json content to Mongo directly or via the API,
listening on ports ```8081``` and ```8083``` respectively.

### Running tests
For tests in docker the test image in ```tools/docker/docker_images``` needs to be built.
The tests can be run using pytest which requires all services to be spun up. 
The docker test containers connects to the network ```api_default```.

All necessary config for the tests are set in ```config.py```.

The infrastructure for the tests are setup using calling the fixtures defined in ```conftest.py```.
The infra can be manually set up with ```setup/setup_infra.py```.


### Steps for testing
1. Build API images, and test images with Python, Spark and Hadoop.
If no changes are made to the images this is only required once.

```make build_all```

Run tests (spins up and down required docker services.)

```make run_tests_clean [test_name]=<optional_test_name>```


For local or ad hoc testing all services can be spun up and configured using the following steps: 

1. Spin up all services. 

```make spin_up```

(Optional) - Setup infra for ad hoc testing (local tests will setup infra dynamically).

```make setup_infra```

2. Local tests can be run with

```make run_tests [test_name]=<optional_test_name>```

Running test container ad hoc with a specified command can be done by: 

```make test_container [container_argument]=<container_argument>```
