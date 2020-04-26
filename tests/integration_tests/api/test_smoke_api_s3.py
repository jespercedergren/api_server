import os
import subprocess
import time

import pytest

from tests.config import server_service
from tests.helpers.common import get_all_s3_keys, read_s3_stream
from tests.constants import PYTHON


class TestAPIS3:
    @pytest.fixture()
    def add_data(self, setup_secrets_localstack, setup_s3_bucket_minio):

        url = f"http://{server_service}:80/api/ingest_data/smoke_test"

        start = time.perf_counter()
        # run as python script
        project_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(
            [PYTHON, f"{project_dir}/../../helpers/async_populate.py", "--url", url]
        )

        return start

    def test_read_from_s3(self, add_data):
        start = add_data

        n_keys = 0

        bucket_keys = get_all_s3_keys(s3_host="minio")

        while n_keys < 100:
            bucket_keys = get_all_s3_keys(s3_host="minio")
            n_keys = len(bucket_keys["test-bucket"])

        data_list = []
        for bucket, keys in bucket_keys.items():
            for key in keys:
                if "test-prefix" in key:
                    data_json = read_s3_stream("test-bucket", key, s3_host="minio")
                    data_list.append(data_json)

        # test data list is as expected
        from tests.helpers.async_populate import payloads as expected_data_list

        assert sum([x in expected_data_list for x in data_list]) == 100
        assert sum([x in data_list for x in expected_data_list]) == 100

        elapsed = time.perf_counter() - start
        print(f"Executed in {elapsed:0.2f} seconds.")
