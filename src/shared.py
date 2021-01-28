import boto3
import os
from rich import print

def boto_client(service):
    key_id = os.environ.get("AWS_ACCESS_KEY_ID", "")
    secret_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
    return boto3.client(service, region_name="us-east-1", aws_access_key_id=key_id, 
                                aws_secret_access_key=secret_key)


def quit_on_error(msg):
    print("[red]" + msg + "[red]")
    exit(0)


def extract_zoneid(hosted_zone):
    # try:
    uid = hosted_zone["Id"]
    res = uid.replace("/hostedzone/", "")
    return res
    # except:
        # return False