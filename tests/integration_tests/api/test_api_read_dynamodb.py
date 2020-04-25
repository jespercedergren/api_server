import pytest
import time
import requests

from tests.config import server_service
from tests.patches import PatchedDynamoDBClient


class TestAPIReadDynamoDB:
    @pytest.fixture(scope="session")
    def add_data(self, setup_secrets_localstack, setup_table_dynamodb):
        start = time.perf_counter()

        item_1 = {"user_id": "111", "app": "system", "permissions": "all", "other": 1}
        item_2 = {"user_id": "222", "app": "fake_app", "permissions": "basic", "other": 1}
        dynamodb_client = PatchedDynamoDBClient()
        dynamodb_client.put_item(item_1)
        dynamodb_client.put_item(item_2)

        return start, item_1, item_2

    def test_post_api_read_ddb(self, add_data):

        start = add_data[0]
        expected_data = add_data[1]
        expected_data_2 = add_data[2]

        # POST
        # get data via API
        with requests.session() as session:
            response = session.get(f"http://{server_service}:80/api/read_data/ddb",
                                    params={"user_id": "111", "password": "fake_password"})
        data = response.json()

        with requests.session() as session:
            response = session.get(f"http://{server_service}:80/api/read_data/ddb",
                                    params={"user_id": "222", "password": "fake_password"})
        data_2 = response.json()

        # test
        assert data == expected_data
        assert data_2 == expected_data_2

    def test_get_api_read_ddb(self, add_data):
        start = add_data[0]
        expected_data = add_data[1]
        expected_data_2 = add_data[2]

        # GET
        # get data via API
        with requests.session() as session:
            response = session.get(f"http://{server_service}:80/api/read_data/ddb",
                                   params={"user_id": "111"})
        data = response.json()

        with requests.session() as session:
            response = session.get(f"http://{server_service}:80/api/read_data/ddb",
                                   params={"user_id": "222"})
        data_2 = response.json()

        # test
        assert expected_data == data
        assert expected_data_2 == data_2

    def test_get_api_read_ddb_multi(self, add_data):

        expected_data = add_data[1]

        responses = []
        s = time.perf_counter()
        for i in range(100):
            with requests.session() as session:
                response = session.get(f"http://{server_service}:80/api/read_data/ddb",
                                       params={"user_id": "111"})
                responses.append(response)

        elapsed = time.perf_counter() - s
        print(f"{__file__} executed in {elapsed:0.2f} seconds.")
        data = [resp.json() for resp in responses]

        assert sum([x == expected_data for x in data]) == len(data)
