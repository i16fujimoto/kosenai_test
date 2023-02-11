import warnings
from typing import Union, Optional
from pathlib import Path

import boto3
import os
from os.path import join, dirname
from dotenv import load_dotenv

BUCKET_NAME = "static"

# 環境変数を設定
load_dotenv(verbose=True)

dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)


s3 = boto3.resource(
    service_name="s3",
    endpoint_url="http://minio:9000",
    aws_access_key_id=os.environ["MINIO_ACCESS_KEY"],
    aws_secret_access_key=os.environ["MINIO_SECRET_KEY"],
    region_name="",
)


def fetch_file_from_s3(key: str) -> Optional[str]:
    obj = s3.Object(BUCKET_NAME, key)
    try:
        return obj.get()["Body"].read().hex()
    except Exception:
        warnings.warn(f"Could not fetch a file named '{key}' from bucket '{BUCKET_NAME}', returning None instead.")
        return None


def push_file_to_s3(filepath: Union[Path, str]) -> None:
    if isinstance(filepath, str):
        filepath = Path(filepath)

    bucket = s3.Bucket(BUCKET_NAME)
    bucket.upload_file(str(filepath), filepath.name)
