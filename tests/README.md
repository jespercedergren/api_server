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

The tests run using asyncio to asynchronously send json data to a specified url. 

### Mocked services
The server with the mocked services are spun up using docker compose in the server folder.
The services are attached to the same docker network as the api ```api_default```.
Localstack are used to mock the AWS services, where all services used are available on port ```4566```.
When reading from localstack s3 using Spark is set to use port ```4573```.
  
Minio is also included as an alternative for s3.

Logstash is used for experimental purposes and is configured to send json content to Mongo directly or via the API, 
listening on ports ```8081``` and ```8083``` respectively.

### Running tests
The tests can be run using pytest which requires all services to be spun up. 
All services can be spun up with ```spin_up_local/spin_up.sh```. 
The infrastructure can be set up manually with ```spin_up_local/setup_infra.sh```.

For tests in docker the test image in ```docker_images``` needs to be built. 

It can also be run by running the shell script ```run_all_tests.sh``` in ```docker_tests``` 
which spins up and tears down the services automatically.  

The docker tests connects the test container built in ```docker_images``` to the network ```api_default```. 
It also bind mounts the whole ```test```  and ```client``` folders into the container.
