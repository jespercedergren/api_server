import boto3


def cleanup_buckets(s3_resource: boto3.resource):
    for bucket in s3_resource.buckets.all():
        for key in bucket.objects.iterator():
            try:
                key.delete()
            except s3_resource.exceptions.NoSuchBucket:
                print(f"Bucket does not exist...")
        bucket.delete()


def cleanup_secrets(sm_client: boto3.client):
    for secret in sm_client.list_secrets()["SecretList"]:
        secret_id = secret["Name"]
        sm_client.delete_secret(SecretId=secret_id, ForceDeleteWithoutRecovery=True)


def cleanup_delivery_streams(firehose_client: boto3.client):
    for delivery_stream_name in firehose_client.list_delivery_streams()["DeliveryStreamNames"]:
        firehose_client.delete_delivery_stream(DeliveryStreamName=delivery_stream_name)
