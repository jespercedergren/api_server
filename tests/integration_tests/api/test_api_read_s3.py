import time

import pandas as pd
import pytest
import requests

from tests.config import server_service
from tests.helpers.common import pd_equals
from tests.helpers.io import save_parquet


# TODO fix and unskip tests
class TestAPIReadS3:
    @pytest.fixture(scope="session")
    def add_data(self, setup_secrets_localstack, setup_s3_bucket_minio, spark_session_minio):
        spark = spark_session_minio
        start = time.perf_counter()

        input_data_pd = pd.DataFrame(
            [["system", "all", "1"], ["fake_app", "basic", "1"]],
            columns=["app", "permissions", "other"],
        )
        input_data_df = spark.createDataFrame(input_data_pd)

        id_key = 1
        save_parquet(
            input_data_df, f"s3a://test-bucket/aggregated/mobile_data.parquet/id_key={id_key}"
        )

        return start, input_data_pd

    @pytest.mark.skip(reason="Not implemented.")
    def test_post_api_read_s3(self, add_data):

        start = add_data[0]
        expected_data_pd = add_data[1]

        cols = list(expected_data_pd.columns)

        # POST
        # get data via API
        with requests.session() as session:
            response = session.get(
                f"http://{server_service}:80/api/read_data/s3",
                params={"id_key": 1, "password": "fake_password"},
            )
        data = response.json()
        print(data)
        data_pd = pd.DataFrame(data)[cols]
        # test
        assert pd_equals(expected_data_pd, data_pd)

    @pytest.mark.skip(reason="Not implemented.")
    def test_get_api_read_s3(self, add_data):
        start = add_data[0]
        expected_data_pd = add_data[1]

        cols = list(expected_data_pd.columns)

        # GET
        # get data via API
        s = time.perf_counter()
        for i in range(10):
            with requests.session() as session:
                response = session.get(
                    f"http://{server_service}:80/api/read_data/s3", params={"id_key": 1}
                )
        data = response.json()
        print(data)
        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
        data_pd = pd.DataFrame(data)[cols]

        # test
        assert pd_equals(expected_data_pd, data_pd)
