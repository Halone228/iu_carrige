import boto3
from os import getenv

s3_client = boto3.client(
    "s3",
    endpoint_url=f"http://localhost:4566",
    aws_access_key_id=getenv("AWS_ACCESS_KEY_ID", 'test'),
    aws_secret_access_key=getenv("AWS_SECRET_ACCESS_KEY", 'test')
)

s3_client.create_bucket(Bucket=getenv("BUCKET_NAME", "test"))
