import pytest
import os
import boto3
import json
from pyspark.sql import SparkSession
from tests.config import minio_config, localstack_config, mongo_config, postgres_config
from tests.server.setup.postgres import PostgresSetup
from tests.server.setup.mongo import MongoDBSetup
from clients.mongo import get_client_arg_from_secrets


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
            print(f"Secret {secret_name} already exists...")
            pass

    yield sm

    for secret in sm.list_secrets()["SecretList"]:
        secret_id = secret["Name"]
        sm.delete_secret(SecretId=secret_id, ForceDeleteWithoutRecovery=True)


@pytest.fixture(scope="function")
def setup_s3_bucket_localstack():

    s3_resource = boto3.resource("s3", **localstack_config["s3"])

    for bucket_name in localstack_config["s3_buckets"]:
        try:
            s3_resource.create_bucket(Bucket=bucket_name)
        except s3_resource.exceptions.ResourceExistsException:
            print(f"Bucket {bucket_name} already exists...")
            pass

    yield s3_resource

    for bucket in s3_resource.buckets.all():
        for key in bucket.objects.iterator():
            try:
                key.delete()
            except s3_resource.exceptions.NoSuchBucket:
                print(f"Bucket {bucket} does not exist...")
        bucket.delete()


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
    print('Delete Spark session...')
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

    for delivery_stream_name in firehose_client.list_delivery_streams()["DeliveryStreamNames"]:
        firehose_client.delete_delivery_stream(DeliveryStreamName=delivery_stream_name)


@pytest.fixture(scope="session")
def setup_s3_bucket_minio():

    s3_resource = boto3.resource("s3", **minio_config["s3"])

    for bucket_name in minio_config["s3_buckets"]:
        try:
            s3_resource.create_bucket(Bucket=bucket_name)
        except s3_resource.meta.client.exceptions.BucketAlreadyOwnedByYou:
            print(f"Bucket {bucket_name} already exists...")

    yield s3_resource

    for bucket in s3_resource.buckets.all():
        for key in bucket.objects.iterator():
            try:
                key.delete()
            except s3_resource.exceptions.NoSuchBucket:
                print(f"Bucket does not exist...")
        bucket.delete()


@pytest.fixture(scope="session")
def spark_session_minio():
    """
    Set up a spark session with all the settings.
    """
    os.environ["PYSPARK_SUBMIT_ARGS"] = '--packages "org.apache.hadoop:hadoop-aws:2.7.3" pyspark-shell'
    #os.environ["PYSPARK_SUBMIT_ARGS"] = '--packages "io.delta:delta-core_2.11:0.5.0" pyspark-shell'
    spark = SparkSession.builder.getOrCreate()

    print(spark)
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
    #hadoop_conf.set("spark.sql.parquet.cacheMetadata", "true")

    yield spark
    print('Delete Spark session...')
    spark.stop()
    del spark


@pytest.fixture(scope="module")
def mongo_db_setup():
    """
    Create a database setup class and return
    :return:
    """

    client_arg = get_client_arg_from_secrets(mongo_config["secrets"])

    # DataBaseSetup class can handle database state, i.e. post data, reset data etc
    db_instance = MongoDBSetup(client_arg)
    yield db_instance


@pytest.fixture
def clean_mongo_database(mongo_db_setup):
    mongo_db_setup.reset_db()
    return mongo_db_setup


@pytest.fixture(scope="module")
def postgres_setup():
    """
    Create a database setup class and return
    :return:
    """

    # DataBaseSetup class can handle database state, i.e. post data, reset data etc
    db_instance = PostgresSetup(**postgres_config["secrets"])
    yield db_instance

    # Clean up
    db_instance.close_connection()
    del db_instance


@pytest.fixture
def clean_postgres_database(postgres_setup):
    postgres_setup.setup_tables()
    return postgres_setup
