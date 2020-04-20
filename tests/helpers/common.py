import numpy as np
import boto3
import json
from tests.config import endpoint_url_localstack, endpoint_url_minio


def get_all_s3_keys(s3_host="localstack"):
    if s3_host == "localstack":
        s3_res = boto3.resource("s3", endpoint_url=endpoint_url_localstack, region_name="eu-west-1",
                                aws_access_key_id="test", aws_secret_access_key="test")
    elif s3_host == "minio":
        s3_res = boto3.resource("s3", endpoint_url=endpoint_url_minio, region_name="eu-west-1",
                                aws_access_key_id="testtest", aws_secret_access_key="testtest")
    bucket_keys = {}

    for bucket in s3_res.buckets.all():
        keys = []
        for key in bucket.objects.iterator():
            keys.append(key.key)
        bucket_keys[bucket.name] = keys

    return bucket_keys


def read_s3_stream(bucket, key, s3_host="localstack"):
    if s3_host == "localstack":
        s3_client = boto3.client("s3", endpoint_url=endpoint_url_localstack, region_name="eu-west-1",
                                 aws_access_key_id="test", aws_secret_access_key="test")
    elif s3_host == "minio":
        s3_client = boto3.client("s3", endpoint_url=endpoint_url_minio, region_name="eu-west-1",
                                aws_access_key_id="testtest", aws_secret_access_key="testtest")

    return json.loads(s3_client.get_object(Bucket=bucket, Key=key)["Body"].read().decode('utf-8'))


def pd_equals(df1, df2, use_numpy=False, return_early=False, decimals=None):
    """
    Function to check whether all elements in pandas dataframes are equal to each other.
    Handles when both dfs are nan at the same elements.
    :param df1:
    :param df2:
    :return:
    """

    if decimals:
        df1 = df1.copy().round(decimals)
        df2 = df2.copy().round(decimals)

    all_equals = (df1 == df2)
    nans1 = (df1 != df1)
    nans2 = (df2 != df2)
    both_nans = (nans1 & nans2)

    union_equals_and_both_nans = (all_equals | both_nans)

    if return_early:
        return union_equals_and_both_nans

    if use_numpy:
        import numpy as np
        return np.all(union_equals_and_both_nans)
    else:
        return union_equals_and_both_nans.all().all()
