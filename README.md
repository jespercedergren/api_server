# api_server

This project is built to facilitate an API that can handle POST and GET requests from different devices.

It composes of mainly:

* A server
* A web
* docker to facilitate and replicate the environment locally
* Unit and Integration tests

To understand how to run, and test this `API` please continue this `README` sections.

To understand more specifically about certain parts of the `API` please read under: `Components`.

# Requirements

* python3.7
* pipenv
* docker && docker-compose

# Setup

This projects expects you to run everything from towards or within the docker container. However you might want to be able to do things locally as well.
The setup will be split up into two parts that address this.

## Locally

This project utilises `pipenv`.

Locally:
```bash
make build
```

pythonpath:

```bash
make pythonpath
```

## Docker

```bash
This is being done automatically when the container is being built, please look under section Container below.
```

If there is a need to modify the `Pipfile`, make your changes and then run (`from the root of the project`):

```bash
make update
```

Container (remember the container needs to be built to be able to run this, see `Container` part below):
```bash
make container-update
```

This will update the `Pipfile.lock` which does not need to be recreated unless
new packages are added.

### Ubuntu (specific)

```bash
apt-get --yes install python3-dev
apt-get --yes install libsnappy-dev
```

### MAC (specific)

```bash
brew install pre-commit
brew install snappy
```

If you see an error `xcrun: error: invalid active developer path`, run this command:

```bash
xcode-select --install
```

Otherwise the `pipenv` might fail and you can't udpate the `Pipfile.lock`.

# Docker deployment

```bash
make docker_build_all
```

# Components

## api_server/api

This is a lightweight Flask API that accepts post requests on:
- ```<host_ip>:80/api/ingest_data/mongo```
- ```<host_ip>:80/api/ingest_data/firehose```
- ```<host_ip>:80/api/ingest_data/smoke_test``` (smoke testing only)
- ```<host_ip>:80/api/read_data/s3``` (POST/GET)
- ```<host_ip>:80/api/read_data/ddb``` (POST/GET)

A Nginx HTTPS reverse proxy is used as an intermediary proxy service which takes a client request,
passes it on to the Flask web server, and subsequently delivers the web server’s response back to the client.

The proxy server redirects all incomming connections on port ```80``` to the web server, listening on port ```8000```.

The app in the web server imports from the client module that encapsulates all the logic to connect to other services for data and credential storage.

### .env
Environment variables are set in the .env.api.example file next to the docker compose file.
The variable `ENVIRONMENT` should be set when testing.
The set value of ```test_docker``` implies that the environment is a testing environment within docker, i.e when testing
the API service in docker.

### server

### web

## tests

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


## tools

