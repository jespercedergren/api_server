docker-compose -f ../../api/docker-compose.yml build
docker-compose -f ../serveri/docker-compose.yml build
docker build -t spark_hadoop_python_base ../docker_images/spark_hadoop_python_base
docker build -t test_base ../docker_images/test
