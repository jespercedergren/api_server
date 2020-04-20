import pytest
import time
import os
import subprocess
from tests.config import logstash_service


@pytest.mark.skip(reason="Not implemented.")
class TestLogstashS3:
    @pytest.fixture()
    def add_data(self, setup_s3_bucket_minio):

        url = f"http://{logstash_service}:8082"

        start = time.perf_counter()
        project_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(["python3.7", f"{project_dir}/../../helpers/async_populate.py", "--url", url])
        #subprocess.Popen(["python3.7", f"{project_dir}/async_populate.py", "--url", url])

        return start

    def test_read_from_s3(self, add_data, spark_session_minio):
        start = add_data
        spark = spark_session_minio

        #df = spark.read.parquet("s3://test-bucket")

        elapsed = time.perf_counter() - start
        print(f"Executed in {elapsed:0.2f} seconds.")

        assert True
