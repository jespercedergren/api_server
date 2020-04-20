from clients.postgres import PostgresClient
from clients.mongo import MongoDBClient
from clients.firehose import FirehoseClient
from clients.s3 import S3Client, S3ParquetClient
from tests.config import endpoint_url_localstack, endpoint_url_minio, host_mongo, host_postgres


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


class PatchedMongoDBClient(MongoDBClient):
    """
    Class that patches the MongoDBClient for testing.
    The _set_secrets method is overridden and sets the secrets with a set of fixed credentials.
    These credentials match the ones specified in conftest.py.
    """
    def __init__(self):
        super(PatchedMongoDBClient, self).__init__(
            database='test',
            collection='test')

    def _set_secrets(self):
        secrets = {
            'host': host_mongo,
            'user': 'test',
            'password': 'test',
            'port': '27017'
        }

        client_arg = 'mongodb://%(user)s:%(password)s@%(host)s:%(port)s' % {
            'user': secrets['user'],
            'password': secrets['password'],
            'host': secrets['host'],
            'port': secrets['port']
        }

        self.secrets = client_arg


class PatchedPostgresClient(PostgresClient):
    """
    Class that patches the PostgresClient for testing.
    The _set_secrets method is overridden and sets the secrets with a set of fixed credentials.
    These credentials match the ones specified in conftest.py.
    """
    def __init__(self):
        super(PatchedPostgresClient, self).__init__()
        if self._get_secrets()['dbname'] != 'test':
            raise WrongDatabase('Not connected to test database')

    def _set_secrets(self):
        self.secrets = {
            'host': host_postgres,
            'dbname': 'test',
            'user': 'test',
            'password': 'test',
            'port': '5432'
        }
