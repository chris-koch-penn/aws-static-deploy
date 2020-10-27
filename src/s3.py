import os
from pathlib import Path
from shared import boto_client, quit_on_error
from rich.progress import track
import json
import mimetypes

client = boto_client("s3")


def check_if_bucket_exists(domain):
    try:
        client.head_bucket(Bucket=domain)
        return True
    except:
        return False


def create_bucket(domain):
    try:
        return client.create_bucket(ACL="public-read", Bucket=domain)
    except Exception as e:
        print(e)
        return quit_on_error("Failed to create website.")


def set_bucket_website_config(domain, index_path="index.html", error_path="error.html"):
    try:
        # Set the website policy on the selected bucket
        return client.put_bucket_website(
            Bucket=domain,
            WebsiteConfiguration={
                "ErrorDocument": {"Key": error_path},
                "IndexDocument": {"Suffix": index_path},
            },
        )
    except Exception as e:
        print(e)
        return quit_on_error("Failed to configure website.")


def sync_website(domain, rootdir, files):
    try:
        # Iterate through list to upload objects to S3
        for filename in track(files):
            f = filename.replace(str(rootdir[2:]), "").strip(".").strip("/")
            print(f)
            mt = mimetypes.guess_type(f)[0]
            mt = mt if mt is not None else "text/plain"
            client.upload_file(
                filename,
                domain,
                f,
                ExtraArgs={"ACL": "public-read", "ContentType": mt},
            )
    except Exception as e:
        print(e)
        return quit_on_error("Failed to sync website.")


def glob_files(rootdir, exclude_types=[], extra_include_types=[]):
    exclude_types = [".DS_Store", ".git", ".gitignore"] + exclude_types
    exclude_types = set([ext.replace(".", "") for ext in exclude_types])
    extra_include_types = set([ext.replace(".", "") for ext in extra_include_types])
    include = set(
        [
            "",
            "a",
            "avi",
            "css",
            "csv",
            "data",
            "doc",
            "docx",
            "eot",
            "gif",
            "htm",
            "html",
            "jpg",
            "jpeg",
            "js",
            "json",
            "mid",
            "midi",
            "mp3",
            "mp4",
            "mov",
            "qt",
            "pdf",
            "png",
            "rar",
            "svg",
            "tiff",
            "tar",
            "ttf",
            "txt",
            "wasm",
            "wav",
            "woff",
            "xlsx",
            "zip",
        ]
    )
    include = include.union(extra_include_types).difference(exclude_types)
    files = [
        str(p)
        for p in Path(rootdir).glob("**/*")
        if valid_path(include, exclude_types, p)
    ]
    total_size = sum([os.path.getsize(f) for f in files])
    GB = 1000 * 1000 * 1000
    if total_size > GB:
        gbs = round(total_size / GB, 2)
        msg = (
            f"Websites uploaded to SDS can't be larger than 1GB - your website is {gbs} GBs. "
            + "Check to see if you are running this command in the correct directory. "
            + "If there are file types that are not necessary for your build, exclude "
            + "them using the exclude_file_types option in your sds.config.json file."
        )
        return quit_on_error(msg)
    return files


def valid_path(include, exclude_types, filename):
    return (
        filename.suffix[1:] in include
        and filename.is_file()
        and filename.name[1:] not in exclude_types
        and filename.suffix[1:] not in exclude_types
    )


def list_files(domain):
    try:
        return [k["Key"] for k in client.list_objects_v2(Bucket=domain)["Contents"]]
    except:
        return []


def set_public_policy(domain):
    policy = {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "PublicReadGetObject",
                "Effect": "Allow",
                "Principal": "*",
                "Action": ["s3:GetObject"],
                "Resource": [f"arn:aws:s3:::{domain}/*"],
            }
        ],
    }
    return client.put_bucket_policy(Bucket=domain, Policy=json.dumps(policy))