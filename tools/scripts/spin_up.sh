# spin down services
./tools/scripts/spin_down.sh

# spin up services
docker-compose -f ./api/docker-compose.yml up --build -d
docker-compose -f ./tools/docker/server/docker-compose.yml up --build -d

# waiting for server to be open
./tools/scripts/wait_for_it.sh localhost:4566 -t 0
echo "localstack:4566 is open"

./tools/scripts/wait_for_it.sh localhost:9000 -t 0
echo "minio:9000 is open"

./tools/scripts/wait_for_it.sh localhost:8000 -t 0
echo "dynamodb:8000 is open"


echo "just a minute, waiting for all services..."
sleep 60
echo "done"
