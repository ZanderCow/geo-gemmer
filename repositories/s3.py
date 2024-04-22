import boto3
from contextlib import contextmanager
import os


@contextmanager
def get_s3_client():
    """Yield a boto3 S3 client and automatically close the session after use."""
    session = boto3.Session()  # You can configure your credentials and region here
    s3 = session.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'), 
        )
    
    try:
        yield s3
    finally:
        # Here you can handle cleanup, though there's typically no need to explicitly close AWS sessions
        # Boto3 manages connection pooling automatically.
        # If needed, additional cleanup can go here.
        pass