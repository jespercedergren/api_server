import boto3
from mypy_boto3 import s3
from mypy_boto3 import secretsmanager
from mypy_boto3 import firehose


def cleanup_buckets(s3_resource: s3.S3ServiceResource):
    for bucket in s3_resource.buckets.all():
        for key in bucket.objects.iterator():
            try:
                key.delete()
            except s3_resource.exceptions.NoSuchBucket:
                print(f"Bucket does not exist...")
        bucket.delete()


def cleanup_secrets(sm_client: secretsmanager.Client):
    for secret in sm_client.list_secrets()["SecretList"]:
        secret_id = secret["Name"]
        sm_client.delete_secret(SecretId=secret_id, ForceDeleteWithoutRecovery=True)


def cleanup_delivery_streams(firehose_client: firehose.Client):
    for delivery_stream_name in firehose_client.list_delivery_streams()["DeliveryStreamNames"]:
        firehose_client.delete_delivery_stream(DeliveryStreamName=delivery_stream_name)
