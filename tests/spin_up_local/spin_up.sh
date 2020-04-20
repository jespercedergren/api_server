# spin down services
docker-compose -f ../server/docker-compose.yml down --remove-orphans
docker-compose -f ../../api/docker-compose.yml down --remove-orphans

# spin up services
docker-compose -f ../../api/docker-compose.yml up --build -d
docker-compose -f ../server/docker-compose.yml up --build -d

# waiting for server to be open
./wait_for_it.sh localhost:4566 -t 0
echo "localstack:4566 is open"

./wait_for_it.sh localhost:9000 -t 0
echo "minio:9000 is open"

./wait_for_it.sh localhost:27017 -t 0
echo "mongo:27017 is open"

echo "just a moment..."
sleep 10
