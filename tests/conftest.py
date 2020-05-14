import pytest
import os
import boto3
import json
import logging
from pyspark.sql import SparkSession

from tests.config import minio_config, localstack_config, dynamodb_config
from tests.helpers.infra import cleanup_buckets
from tests.helpers.infra import cleanup_secrets
from tests.helpers.infra import cleanup_delivery_streams


@pytest.fixture(scope='session', autouse=True)
def set_environment():
    pass


@pytest.fixture(scope="session")
def setup_secrets_localstack():

    sm = boto3.client("secretsmanager", **localstack_config["secretsmanager"])

    for secret_name, secret_dict in localstack_config["secrets"].items():
        try:
            sm.create_secret(Name=secret_name, SecretString=json.dumps(secret_dict))
        except sm.exceptions.ResourceExistsException:
            logging.info(f"Secret {secret_name} already exists...")
            pass

    yield sm

    cleanup_secrets(sm)


@pytest.fixture(scope="function")
def setup_s3_bucket_localstack():

    s3_resource = boto3.resource("s3", **localstack_config["s3"])

    cleanup_buckets(s3_resource)

    for bucket_name in localstack_config["s3_buckets"]:
        try:
            s3_resource.create_bucket(Bucket=bucket_name)
        except s3_resource.exceptions.ResourceExistsException:
            logging.info(f"Bucket {bucket_name} already exists...")
            pass

    yield s3_resource

    cleanup_buckets(s3_resource)

@pytest.fixture(scope="module")
def spark_session_localstack():
    """
    Set up a spark session with all the settings.
    """
    os.environ["PYSPARK_SUBMIT_ARGS"] = '--packages "org.apache.hadoop:hadoop-aws:2.7.3" pyspark-shell'
    #os.environ["PYSPARK_SUBMIT_ARGS"] = '--packages "io.delta:delta-core_2.11:0.5.0" pyspark-shell'
    spark = SparkSession.builder.getOrCreate()

    # Setup spark to use s3, and point it to the moto server.
    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoop_conf.set("fs.s3a.access.key", localstack_config["spark"]["fs.s3a.access.key"])
    hadoop_conf.set("fs.s3a.secret.key", localstack_config["spark"]["fs.s3a.secret.key"])
    hadoop_conf.set("fs.s3a.endpoint", localstack_config["spark"]["fs.s3a.endpoint"]) #127.0.0.1:4572 works
    hadoop_conf.set('fs.s3a.path.style.access', 'true')
    hadoop_conf.set("spark.sql.parquet.binaryAsString", "true'")
    spark.conf.set("spark.driver.maxResultSize", "5g")

    yield spark
    logging.info('Delete Spark session...')
    spark.stop()
    del spark


@pytest.fixture(scope="module")
def setup_firehose_delivery_stream_localstack():

    firehose_client = boto3.client("firehose", **localstack_config["firehose"])

    delivery_stream_name = localstack_config["firehose_delivery_stream"]["Name"]
    role_arn = localstack_config["firehose_delivery_stream"]["RoleArn"]
    bucket_arn = localstack_config["firehose_delivery_stream"]["BucketArn"]
    prefix = localstack_config["firehose_delivery_stream"]["Prefix"]

    s3_destination_configuration = {"RoleARN": role_arn, "BucketARN": bucket_arn, "Prefix": prefix}

    extended_s3_destination_config = {
        'RoleARN': role_arn,
        'BucketARN': bucket_arn,
        'DataFormatConversionConfiguration': {
            'InputFormatConfiguration': {
                'Deserializer': {
                    'HiveJsonSerDe': {
                    }
                }
            },
            'OutputFormatConfiguration': {
                'Serializer': {
                    'ParquetSerDe': {
                    }
                }
            },
            'SchemaConfiguration': {
            },
            'Enabled': True
        }
    }

    stream_setup = {"DeliveryStreamName": delivery_stream_name,
                    "S3DestinationConfiguration": s3_destination_configuration,
                    "ExtendedS3DestinationConfiguration": extended_s3_destination_config}

    firehose_client.create_delivery_stream(**stream_setup)
    yield firehose_client

    cleanup_delivery_streams(firehose_client)


@pytest.fixture(scope="session")
def setup_s3_bucket_minio():

    s3_resource = boto3.resource("s3", **minio_config["s3"])

    cleanup_buckets(s3_resource)

    for bucket_name in minio_config["s3_buckets"]:
        try:
            s3_resource.create_bucket(Bucket=bucket_name)
        except s3_resource.meta.client.exceptions.BucketAlreadyOwnedByYou:
            logging.info(f"Bucket {bucket_name} already exists...")

    yield s3_resource

    cleanup_buckets(s3_resource)


@pytest.fixture(scope="session")
def setup_table_dynamodb():

    try:
        dynamodb_client = boto3.client("dynamodb", **dynamodb_config["client"])
        dynamodb_client.create_table(**dynamodb_config["table"])
    except dynamodb_client.exceptions.ResourceInUseException as e:
        logging.info(f"DynamoDB table {dynamodb_config['table']['TableName']} already exists...")

    yield dynamodb_client

    dynamodb_client.delete_table(TableName=dynamodb_config['table']['TableName'])

@pytest.fixture(scope="session")
def spark_session_minio():
    """
    Set up a spark session with all the settings.
    """
    os.environ["PYSPARK_SUBMIT_ARGS"] = '--packages "org.apache.hadoop:hadoop-aws:2.7.3" pyspark-shell'
    #os.environ["PYSPARK_SUBMIT_ARGS"] = '--packages "io.delta:delta-core_2.11:0.5.0" pyspark-shell'
    spark = SparkSession.builder.getOrCreate()

    # Setup spark to use s3, and point it to the moto server.
    hadoop_conf = spark.sparkContext._jsc.hadoopConfiguration()
    hadoop_conf.set("fs.s3.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    hadoop_conf.set("fs.s3a.access.key", minio_config["spark"]["fs.s3a.access.key"])
    hadoop_conf.set("fs.s3a.secret.key", minio_config["spark"]["fs.s3a.secret.key"])
    hadoop_conf.set("fs.s3a.endpoint", minio_config["spark"]["fs.s3a.endpoint"])
    hadoop_conf.set('fs.s3a.path.style.access', 'true')
    hadoop_conf.set("spark.sql.parquet.binaryAsString", "true'")
    spark.conf.set("spark.driver.maxResultSize", "5g")

    hadoop_conf.set("spark.shuffle.service.enabled",  "true")
    hadoop_conf.set("fs.s3a.fast.upload", "true")

    yield spark
    logging.info('Delete Spark session...')
    spark.stop()
    del spark
