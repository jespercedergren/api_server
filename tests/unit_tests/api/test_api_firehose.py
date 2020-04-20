import pytest
import time
import os
import subprocess
from tests.config import server_service
from tests.helpers.common import get_all_s3_keys, read_s3_stream


class TestAPIFirehose:
    @pytest.fixture()
    def add_data(self, setup_s3_bucket_localstack, setup_firehose_delivery_stream_localstack, setup_secrets_localstack):

        url = f"http://{server_service}:80/api/ingest_data/firehose"

        start = time.perf_counter()
        # run as python script
        project_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(["python3.7", f"{project_dir}/../../helpers/async_populate.py", "--url", url])

        return start

    def test_read_from_s3(self, add_data):
        start = add_data

        n_keys = 0

        bucket_keys = get_all_s3_keys()
        while n_keys < 100:
            bucket_keys = get_all_s3_keys()
            n_keys = len(bucket_keys["test-bucket"])

        for bucket, keys in bucket_keys.items():
            for key in keys:
                if "test-prefix" in key:
                    data_json = read_s3_stream("test-bucket", bucket_keys["test-bucket"][0])

        print(data_json)

        elapsed = time.perf_counter() - start
        print(f"Executed in {elapsed:0.2f} seconds.")

        assert len(bucket_keys["test-bucket"]) == 100
