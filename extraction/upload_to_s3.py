import boto3
from botocore.exceptions import BotoCoreError, ClientError
from extraction.config import (
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_DEFAULT_REGION,
    S3_BUCKET_NAME
)

def create_s3_client():
    return boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION
    )
def upload_file_to_s3(local_file_path: str, s3_key: str):
    s3_client = create_s3_client()

    try:
        s3_client.upload_file(local_file_path, S3_BUCKET_NAME, s3_key)
        print(f"[SUCCESS] Upload to s3://{S3_BUCKET_NAME}/{s3_key}")
    except (BotoCoreError, ClientError) as e:
        print(f"[ERROR] Failed to upload {local_file_path}: {e}")
        raise