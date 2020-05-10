from clients.firehose import FirehoseClient
from clients.s3 import S3Client, S3ParquetClient
from clients.dynamodb import DynamoDBClient
from tests.config import endpoint_url_localstack, endpoint_url_minio, endpoint_url_dynamodb


class WrongDatabase(Exception):
    pass


class PatchedFirehoseClient(FirehoseClient):
    """
    Class that patches the FirehoseClient for testing.
    The _set_secrets method is overridden and sets the secrets with a set of fixed credentials.
    These credentials match the ones specified in conftest.py.
    """
    def __init__(self):
        super(PatchedFirehoseClient, self).__init__(
            delivery_stream_name='api_to_s3_ingest')

    def _set_secrets(self):
        secrets = {
            "endpoint_url": endpoint_url_localstack,
            "region_name": "eu-west-1",
            "aws_access_key_id": "test",
            "aws_secret_access_key": "test"
        }

        self.secrets = secrets


class PatchedS3Client(S3Client):
    """
    Class that patches the S3Client for testing.
    The _set_secrets method is overridden and sets the secrets with a set of fixed credentials.
    These credentials match the ones specified in conftest.py.
    """
    def __init__(self):
        super(PatchedS3Client, self).__init__(
            bucket="test-bucket")

    def _set_secrets(self):
        secrets = {
            "endpoint_url": endpoint_url_minio,
            "region_name": "eu-west-1",
            "aws_access_key_id": "testtest",
            "aws_secret_access_key": "testtest"
        }

        self.secrets = secrets


class PatchedS3ParquetClient(S3ParquetClient):
    """
    Class that patches the S3ParquetClient for testing.
    The _set_secrets method is overridden and sets the secrets with a set of fixed credentials.
    These credentials match the ones specified in conftest.py.
    """
    def __init__(self):
        super(PatchedS3ParquetClient, self).__init__()

    def _set_secrets(self):
        secrets = {
            "endpoint_url": endpoint_url_minio,
            "region_name": "eu-west-1",
            "aws_access_key_id": "testtest",
            "aws_secret_access_key": "testtest"
        }

        self.secrets = secrets


class PatchedDynamoDBClient(DynamoDBClient):
    """
    Class that patches the DynamoDBClient for testing.
    The _set_secrets method is overridden and sets the secrets with a set of fixed credentials.
    These credentials match the ones specified in conftest.py.
    """
    def __init__(self):
        super(PatchedDynamoDBClient, self).__init__(table_name="user_table")

    def _set_secrets(self):
        secrets = {
            "endpoint_url": endpoint_url_dynamodb,
            "region_name": "eu-west-1",
            "aws_access_key_id": "test",
            "aws_secret_access_key": "test"
        }

        self.secrets = secrets
