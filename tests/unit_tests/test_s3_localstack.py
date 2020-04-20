import pytest
import time
import pandas as pd
from tests.helpers.io import save_parquet


#http://localhost:4566 com.amazonaws.AmazonClientException: Unable to execute HTTP request: test-bucket.localhost: nodename nor servname provided, or not known
#http://127.0.0.1:4566 java.io.IOException: Bucket test-bucket does not exist


#@pytest.mark.skip(reason="Not used.")
#@pytest.mark.skip(reason="Skipping.")
class TestS3Localstack:
    @pytest.fixture()
    def add_data(self, setup_s3_bucket_localstack, spark_session_localstack):
        spark = spark_session_localstack

        start = time.perf_counter()

        pd_df = pd.DataFrame([[1, 2], [3, 4]], columns=["a", "b"])
        df = spark.createDataFrame(pd_df)

        save_parquet(df, "s3a://test-bucket/test.parquet")

        return start

    def test_read_from_s3(self, add_data, spark_session_localstack):
        start = add_data
        spark = spark_session_localstack

        df = spark.read.parquet("s3://test-bucket/test.parquet")

        elapsed = time.perf_counter() - start
        print(f"Executed in {elapsed:0.2f} seconds.")
        assert True

