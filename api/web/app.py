from clients.dynamodb import DynamoDBClient
from clients.firehose import FirehoseClient
from clients.mongo import MongoDBClient
from clients.s3 import S3Client, S3ParquetClient, get_firehose_output_s3_key
from flask import Flask, jsonify, request

app = Flask(__name__)


# Assuming environment is set here

# POST
@app.route("/api/ingest_data/mongo", methods=["POST"])
def ingest_json_mongo():
    """
    :return: json
    """
    data_json = request.json
    mongo_client = MongoDBClient(database="test", collection="test")
    object_id_1 = mongo_client.save(data_json)
    return jsonify({"Data ingested": f"{object_id_1}"})


@app.route("/api/ingest_data/firehose", methods=["POST"])
def ingest_bytes_json_firehose():
    """
    :return: json
    """
    data_bytes = request.data
    firehose_client = FirehoseClient(delivery_stream_name="api_to_s3_ingest")
    response = firehose_client.put_record(record=data_bytes)
    return jsonify({"Data ingested": f"{response}"})


@app.route("/api/ingest_data/smoke_test", methods=["POST"])
def ingest_bytes_json_smoke_test():
    """
    :return: json
    """
    data_bytes = request.data
    s3_client = S3Client(bucket="test-bucket")
    response = s3_client.upload_record(
        record=data_bytes, get_key_func=get_firehose_output_s3_key, prefix="test-prefix"
    )
    return jsonify({"Data ingested": f"{response}"})


@app.route("/api/read_data/s3", methods=["GET", "POST"])
def read_data_s3():
    """
    :return: json
    """

    if request.method == "POST":
        id_key = request.args.get("id_key")
        password = request.args.get("password")

        # authenticate
        # TODO

        # read
        s3_parquet_client = S3ParquetClient()
        response = s3_parquet_client.read(
            path=f"s3://test-bucket/aggregated/mobile_data.parquet/id_key={id_key}"
        )

        return response

    elif request.method == "GET":

        id_key = request.args.get("id_key")
        s3_parquet_client = S3ParquetClient()
        response = s3_parquet_client.read(
            path=f"s3://test-bucket/aggregated/mobile_data.parquet/id_key={id_key}"
        )
        return response

    else:
        return {"ERROR": f"Bad request method: {request.method}"}


@app.route("/api/read_data/ddb", methods=["GET", "POST"])
def read_data():
    """
    :return: json
    """

    if request.method == "POST":
        user_id = request.args.get("user_id")
        password = request.args.get("password")

        # authenticate
        # TODO

        # read
        dynamodb_client = DynamoDBClient(table_name="user_table")
        response = dynamodb_client.get_item({"user_id": user_id})
        return response

    elif request.method == "GET":

        user_id = request.args.get("user_id")
        # read
        dynamodb_client = DynamoDBClient(table_name="user_table")
        response = dynamodb_client.get_item({"user_id": user_id})
        return response

    else:
        return {"ERROR": f"Bad request method: {request.method}"}


# running web web in local machine
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)
