from tests.patches import PatchedMongoDBClient
import pytest
import subprocess
import time
import os
from tests.config import server_service


class TestAPIMongo:
    @pytest.fixture()
    def add_data(self, clean_mongo_database, setup_secrets_localstack):

        mongo_client = PatchedMongoDBClient()
        url = f"http://{server_service}:80/api/ingest_data/mongo"

        resp = mongo_client.find({})
        assert len(resp) == 0

        start = time.perf_counter()
        project_dir = os.path.dirname(os.path.abspath(__file__))
        subprocess.Popen(["python3.7", f"{project_dir}/../../helpers/async_populate.py", "--url", url])
        #subprocess.Popen(["python3.7", f"{project_dir}/async_populate.py", "--url", url])

        return start, mongo_client

    def test_read_from_mongo(self, add_data):
        start = add_data[0]
        mongo_client = add_data[1]

        response = []

        while len(response) < 100:
            response = mongo_client.find({})

        elapsed = time.perf_counter() - start
        print(f"Executed in {elapsed:0.2f} seconds.")

        assert len(response) == 100
