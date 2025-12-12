"""
Object Storage Service using boto3 for MinIO/S3.
Handles file uploads and retrieval.
"""
import logging
from typing import BinaryIO
from datetime import datetime
import uuid

import boto3
from botocore.client import Config
from botocore.exceptions import ClientError

from app.core.config import settings

logger = logging.getLogger(__name__)


class S3Service:
    """Service for interacting with S3-compatible storage (MinIO)."""

    def __init__(self):
        """Initialize S3 client with configuration from settings."""
        self.client = boto3.client(
            's3',
            endpoint_url=settings.S3_ENDPOINT_URL,
            aws_access_key_id=settings.S3_ACCESS_KEY,
            aws_secret_access_key=settings.S3_SECRET_KEY,
            config=Config(signature_version='s3v4'),
            region_name='us-east-1'  # MinIO requires a region
        )
        self.bucket_name = settings.S3_BUCKET_NAME

    def upload_file(
        self,
        file_obj: BinaryIO,
        filename: str,
        content_type: str = "application/octet-stream"
    ) -> str:
        """
        Upload a file to S3.

        Args:
            file_obj: File-like object to upload
            filename: Original filename
            content_type: MIME type of the file

        Returns:
            S3 key (path) of the uploaded file

        Raises:
            ClientError: If upload fails
        """
        # Generate unique key with timestamp and UUID to prevent collisions
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]

        # Preserve file extension
        if '.' in filename:
            name, ext = filename.rsplit('.', 1)
            s3_key = f"documents/{timestamp}_{unique_id}_{name}.{ext}"
        else:
            s3_key = f"documents/{timestamp}_{unique_id}_{filename}"

        try:
            self.client.upload_fileobj(
                file_obj,
                self.bucket_name,
                s3_key,
                ExtraArgs={
                    'ContentType': content_type,
                    'Metadata': {
                        'original_filename': filename
                    }
                }
            )
            logger.info(f"Successfully uploaded file to {s3_key}")
            return s3_key

        except ClientError as e:
            logger.error(f"Failed to upload file to S3: {e}")
            raise

    def get_presigned_url(self, s3_key: str, expiration: int = 3600) -> str:
        """
        Generate a presigned URL for downloading a file.

        Args:
            s3_key: S3 key of the file
            expiration: URL expiration time in seconds (default: 1 hour)

        Returns:
            Presigned URL string
        """
        try:
            url = self.client.generate_presigned_url(
                'get_object',
                Params={
                    'Bucket': self.bucket_name,
                    'Key': s3_key
                },
                ExpiresIn=expiration
            )
            return url
        except ClientError as e:
            logger.error(f"Failed to generate presigned URL: {e}")
            raise

    def delete_file(self, s3_key: str) -> bool:
        """
        Delete a file from S3.

        Args:
            s3_key: S3 key of the file to delete

        Returns:
            True if successful, False otherwise
        """
        try:
            self.client.delete_object(
                Bucket=self.bucket_name,
                Key=s3_key
            )
            logger.info(f"Successfully deleted file {s3_key}")
            return True
        except ClientError as e:
            logger.error(f"Failed to delete file from S3: {e}")
            return False


# Singleton instance
s3_service = S3Service()
