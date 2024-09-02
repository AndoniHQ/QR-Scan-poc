import os
import boto3
from botocore.client import Config

S3_ENDPOINT = os.environ.get("S3_ENDPOINT")
S3_PORT = os.environ.get("S3_PORT")
S3_USER = os.environ.get("S3_USER")
S3_PASS = os.environ.get("S3_PASS")
S3_BUCKET = os.environ.get("S3_BUCKET")

s3_client = boto3.client(
    's3',
    endpoint_url=f"http://{S3_ENDPOINT}:{S3_PORT}",
    aws_access_key_id=S3_USER,
    aws_secret_access_key=S3_PASS,
    config=Config(signature_version='s3v4'),
    region_name='us-east-1'
)