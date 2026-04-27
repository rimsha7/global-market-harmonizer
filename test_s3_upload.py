import os
from dotenv import load_dotenv
import boto3
from botocore.exceptions import ClientError, NoCredentialsError

load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION", "us-east-1")
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")

def validate_env():
    required_vars = {
        "AWS_ACCESS_KEY_ID": AWS_ACCESS_KEY_ID,
        "AWS_SECRET_ACCESS_KEY": AWS_SECRET_ACCESS_KEY,
        "S3_BUCKET_NAME": S3_BUCKET_NAME,
    }

    missing = [key for key, value in required_vars.items() if not value]
    if missing:
        raise EnvironmentError(f"Missing environment variables: {', '.join(missing)}")

def create_test_file():
    file_name = "sample_test.txt"
    with open(file_name, "w", encoding="utf-8") as f:
        f.write("S3 upload test successful.")
    return file_name

def upload_test_file(file_name: str):
    s3_client = boto3.client(
        "s3",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_DEFAULT_REGION,
    )

    s3_key = "test/sample_test.txt"

    try:
        s3_client.upload_file(file_name, S3_BUCKET_NAME, s3_key)
        print(f"Upload successful: s3://{S3_BUCKET_NAME}/{s3_key}")
    except FileNotFoundError:
        print("Local test file not found.")
    except NoCredentialsError:
        print("AWS credentials not found.")
    except ClientError as e:
        print(f"AWS ClientError: {e}")

if __name__ == "__main__":
    validate_env()
    test_file = create_test_file()
    upload_test_file(test_file)