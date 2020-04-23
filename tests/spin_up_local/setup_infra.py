import boto3
import json
from tests.server.setup.mongo import MongoDBSetup
from clients.mongo import get_client_arg_from_secrets
from tests.config import localstack_config, minio_config, dynamodb_config, mongo_config


def setup_secrets_localstack():

    print("Setting up secrets manager")

    sm = boto3.client("secretsmanager", **localstack_config["secretsmanager"])

    try:
        for secret_name, secret_dict in localstack_config["secrets"].items():
            sm.create_secret(Name=secret_name, SecretString=json.dumps(secret_dict))
    except sm.exceptions.ResourceExistsException:
        print(f"Secret {secret_name} already exists...")
        pass


def setup_s3_bucket_localstack():

    print("Setting up s3 buckets localstack")

    s3_resource = boto3.resource("s3", **localstack_config["s3"])

    for bucket_name in localstack_config["s3_buckets"]:
        try:
            s3_resource.create_bucket(Bucket=bucket_name)
        except s3_resource.exceptions.ResourceExistsException:
            print(f"Bucket {bucket_name} already exists...")
            pass


def setup_firehose_delivery_stream_localstack():

    print("Setting up firehose delivery stream")

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


def setup_table_dynamodb():
    dynamodb_client = boto3.client("dynamodb", **dynamodb_config["client"])
    dynamodb_client.create_table(**dynamodb_config["table"])


def setup_s3_bucket_minio():

    print("Setting up s3 buckets minio")

    s3_resource = boto3.resource("s3", **minio_config["s3"])

    for bucket_name in minio_config["s3_buckets"]:
        try:
            s3_resource.create_bucket(Bucket=bucket_name)
        except s3_resource.meta.client.exceptions.BucketAlreadyOwnedByYou:
            print(f"Bucket {bucket_name} already exists...")


def mongo_db_setup():
    """
    Create a database setup class and return
    :return:
    """

    print("Setting up mongo")

    client_arg = get_client_arg_from_secrets(mongo_config["secrets"])

    # DataBaseSetup class can handle database state, i.e. post data, reset data etc
    db_instance = MongoDBSetup(client_arg)
    return db_instance


def clean_mongo_database(mongo_db_setup):
    mongo_db_setup.reset_db()


if __name__ == "__main__":
    setup_secrets_localstack()
    setup_s3_bucket_localstack()
    setup_s3_bucket_minio()
    setup_firehose_delivery_stream_localstack()
    clean_mongo_database(mongo_db_setup())