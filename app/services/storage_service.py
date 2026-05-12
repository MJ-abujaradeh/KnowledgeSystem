import boto3 
from botocore.exceptions import ClientError
from app.config import Config

class S3StorageService:
    def __init__(self):
        self.s3 = boto3.client(
            "s3",
            aws_access_key_id = Config.AWS_ACCESS_KEY,
            aws_secret_access_key = Config.AWS_SECRET_KEY
        )

        self.bucket_name = Config.AWS_BUCKET_NAME

    def upload_file(self, fileObj, fileName):
        try:
            self.s3.upload_fileobj(fileObj, self.bucket_name, fileName)
            return None;

        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False;

    def get_file(self, fileName):
        try:
            response = self.s3.get_object(Bucket=self.bucket_name, Key=fileName)
            return response['Body'].read()
        except ClientError as e:
            print(f"Error retrieving file from S3: {e}")
            return None