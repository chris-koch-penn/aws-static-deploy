import boto3
import os

def boto_client(service):
    key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    return boto3.client(service, region_name="us-east-1", aws_access_key_id=key_id, 
                                aws_secret_access_key=secret_key)