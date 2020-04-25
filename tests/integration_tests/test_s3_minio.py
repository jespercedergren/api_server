import pytest
import time
from tests.helpers.io import save_parquet

#@pytest.mark.skip(reason="Skipping.")
class TestS3Minio:
    @pytest.fixture(scope="session")
    def add_data(self, setup_s3_bucket_minio, spark_session_minio):
        spark = spark_session_minio

        start = time.perf_counter()

        import pandas as pd
        pd_df = pd.DataFrame([[1, 2], [3, 4]], columns=["a", "b"])
        df = spark.createDataFrame(pd_df)

        save_parquet(df, "s3://test-bucket/test.parquet")

        return start

    def test_read_from_s3(self, add_data, spark_session_minio):
        start = add_data
        spark = spark_session_minio

        df = spark.read.parquet("s3://test-bucket/test.parquet")
        df.show()

        elapsed = time.perf_counter() - start
        print(f"Executed in {elapsed:0.2f} seconds.")
        assert True

