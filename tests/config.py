from tests import test_env


if test_env == "docker":
    endpoint_url_minio = "http://minio:9000"
    endpoint_url_localstack = "http://localstack:4566"
    endpoint_url_localstack_spark_s3 = "http://localstack:4572"
    endpoint_url_dynamodb = "http://dynamodb:8000"
    host_postgres = "postgres"
    host_mongo = "mongo"
    server_service = "server"
    logstash_service = "logstash"


elif test_env == "local" or test_env == "circle":
    endpoint_url_minio = "http://127.0.0.1:9000"
    endpoint_url_localstack = "http://localhost:4566"
    endpoint_url_localstack_spark_s3 = "http://127.0.0.1:4572"
    endpoint_url_dynamodb = "http://localhost:8001"
    host_postgres = "localhost"
    host_mongo = "localhost"
    server_service = "0.0.0.0"
    logstash_service = "0.0.0.0"



credential_minio = "testtest"
minio_config = {
    "s3": {"endpoint_url": endpoint_url_minio,
           "aws_access_key_id": credential_minio,
           "aws_secret_access_key": credential_minio},
    "s3_buckets": ["test-bucket"],
    "spark": {"fs.s3a.endpoint": endpoint_url_minio,
              "fs.s3a.access.key": credential_minio,
              "fs.s3a.secret.key": credential_minio},
}

credential = "test"
region_name = "eu-west-1"
secrets = {"firehose_client": {"endpoint_url": "http://localstack:4566", "region_name": region_name,
                     "aws_access_key_id": credential, "aws_secret_access_key": credential},
           "mongo_client": {"host": "mongo", "user": "test", "password": "test", "port": "27017"},
           "s3_client": {"endpoint_url": "http://minio:9000", "region_name": region_name,
                     "aws_access_key_id": credential_minio, "aws_secret_access_key": credential_minio},
           "dynamodb_client": {"endpoint_url": "http://dynamodb:8000", "region_name": region_name,
                     "aws_access_key_id": credential, "aws_secret_access_key": credential}
           }

#role_arn = "arn:aws:iam::000000000000:role/super_role"
#role_arn = "arn:aws:iam::*"

localstack_config = {
    "spark": {"fs.s3a.access.key": credential,
              "fs.s3a.secret.key": credential,
              "fs.s3a.endpoint": endpoint_url_localstack_spark_s3},
    "firehose": {"endpoint_url": endpoint_url_localstack,
                 "region_name": region_name,
                 "aws_access_key_id": credential,
                 "aws_secret_access_key": credential},
    "firehose_delivery_stream": {"RoleArn": "arn:aws:iam::000000000000:role/firehose",
                                 "BucketArn": "arn:aws:s3:::test-bucket",
                                 "Prefix": "test-prefix",
                                 "Name": "api_to_s3_ingest"},
    "s3": {"endpoint_url": endpoint_url_localstack,
           "aws_access_key_id": credential,
           "aws_secret_access_key": credential},

    "s3_buckets": ["test-bucket"],

    "secretsmanager": {"endpoint_url": endpoint_url_localstack,
                       "region_name": region_name,
                       "aws_access_key_id": credential,
                       "aws_secret_access_key": credential},
    "secrets": secrets
}

dynamodb_config = {
    "client": {"endpoint_url": endpoint_url_dynamodb,
               "region_name": region_name,
                "aws_access_key_id": credential,
               "aws_secret_access_key": credential},
    "table": {"AttributeDefinitions": [{"AttributeName": "user_id", "AttributeType": "S"}],
              "TableName": "user_table",
              "KeySchema": [{"AttributeName": "user_id", "KeyType": "HASH"}],
              "ProvisionedThroughput": {'ReadCapacityUnits': 10, 'WriteCapacityUnits': 10}
}
}

postgres_config = \
    { "secrets": {
    'host': host_postgres,
    'dbname': 'test',
    'user': 'test',
    'password': 'test',
    'port': '54320'
}
}

mongo_config = {
    "secrets": {
    'host': host_mongo,
    'user': 'test',
    'password': 'test',
    'port': '27017'
}
}

