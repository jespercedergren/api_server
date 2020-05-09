# spin down services
#./tools/scripts/spin_down.sh

# waiting for server to be open
./tools/scripts/wait_for_it.sh localhost:4566 -t 0
echo "localstack:4566 is open"

./tools/scripts/wait_for_it.sh localhost:9000 -t 0
echo "minio:9000 is open"

./tools/scripts/wait_for_it.sh localhost:8000 -t 0
echo "dynamodb:8000 is open"

./tools/scripts/wait_for_it.sh localhost:27017 -t 0
echo "mongo:27017 is open"

echo "just a minute, waiting for all services..."
sleep 60
echo "done"
