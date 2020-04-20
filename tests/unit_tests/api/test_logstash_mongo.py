from tests.patches import PatchedMongoDBClient
import pytest
import subprocess
import os
import time
from tests.config import logstash_service

@pytest.mark.skip(reason="Not implemented.")
class TestLogstashMongo:
    @pytest.fixture()
    def add_data(self, clean_mongo_database):

        mongo_client = PatchedMongoDBClient()
        resp = mongo_client.find({})
        assert len(resp) == 0

        url = f"http://{logstash_service}:8081"

        start = time.perf_counter()
        #subprocess.Popen(["python", "async_populate.py", "--url", url])
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
