import boto3
from src.config.serttings import settings

class S3Client:

    def __init__(self):
        self.s3_client = boto3.client(
            "s3",
            region_name=settings.REGION_NAME,
            aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
            aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
        )

    def generate_presigned_url(self, bucket_name, object_key, expiration=3600, operation_name="get_object"):
        return self.s3_client.generate_presigned_url(
            operation_name,
            Params={"Bucket": bucket_name, "Key": object_key},
            ExpiresIn=expiration,
        )