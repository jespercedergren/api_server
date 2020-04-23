## API
This is a lightweight Flask API that accepts post requests on:
- ```<host_ip>:80/api/ingest_data/mongo```
- ```<host_ip>:80/api/ingest_data/firehose```
- ```<host_ip>:80/api/ingest_data/smoke_test``` (testing only)
- ```<host_ip>:80/api/read_data/s3``` (POST/GET)
- ```<host_ip>:80/api/read_data/ddb``` (POST/GET)
 
A Nginx HTTPS reverse proxy is used as an intermediary proxy service which takes a client request, 
passes it on to the Flask web server, and subsequently delivers the web server’s response back to the client.

The proxy server redirects all incomming connections on port ```80``` to the web server, listening on port ```8000```.

The app in the web server imports from the client module that encapsulates all the logic to connect to other services for data and credential storage. 

### Deployment
Clone the repo, run docker-compose in the api folder.

```docker-compose -f api/docker-compose.yml up```

Environment variables are set in the .env file next to the docker compose file. 
The variable ENVIRONMENT should be set when testing. 
The set value of ```test_docker``` implies that the environment is a testing environment within docker, i.e when testing
the API service in docker. 

It should be noted that the ```clients``` module is bind mounted into the web service so it can be used in the API.

# TODO
 - Separate/make ```clients``` installable.
 - Terraform for infra in testing and production.