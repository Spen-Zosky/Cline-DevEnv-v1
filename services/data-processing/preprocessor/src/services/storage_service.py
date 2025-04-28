"""
Storage Service

This module provides storage operations for the Data Preprocessor Service.
"""

import os
import io
import json
import asyncio
from typing import Dict, List, Optional, Any, Union, BinaryIO, cast
import typing
if typing.TYPE_CHECKING:
    from minio import Minio as MinioClient
from datetime import datetime
import pandas as pd
import numpy as np
from minio import Minio
from minio.error import MinioException
from loguru import logger

from config import settings


class StorageService:
    """Service for storage operations."""
    
    def __init__(self):
        """Initialize the storage service."""
        self.minio_client: Optional["MinioClient"] = None
    
    async def initialize(self):
        """Initialize the storage service."""
        try:
            # Initialize MinIO client
            self.minio_client = Minio(
                settings.MINIO_ENDPOINT,
                access_key=settings.MINIO_ACCESS_KEY,
                secret_key=settings.MINIO_SECRET_KEY,
                secure=settings.MINIO_SECURE
            )
            
            # Create buckets if they don't exist
            await self._create_buckets()
            
            logger.info("Storage service initialized")
        except Exception as e:
            logger.error(f"Failed to initialize storage service: {str(e)}")
            raise
    
    def close(self):
        """Close the storage service."""
        # MinIO client doesn't need to be closed
        pass
    
    async def check_connection(self) -> bool:
        """
        Check if the storage service is connected.
        
        Returns:
            bool: True if connected, False otherwise
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Ensure MinIO client is initialized
            assert self.minio_client is not None, "MinIO client is not initialized"
            
            # Check if buckets exist
            raw_bucket_exists = self.minio_client.bucket_exists(settings.MINIO_RAW_BUCKET)
            processed_bucket_exists = self.minio_client.bucket_exists(settings.MINIO_PROCESSED_BUCKET)
            
            return raw_bucket_exists and processed_bucket_exists
        except Exception as e:
            logger.error(f"Storage connection check failed: {str(e)}")
            return False
    
    async def _create_buckets(self):
        """Create required buckets if they don't exist."""
        try:
            # Ensure MinIO client is initialized
            assert self.minio_client is not None, "MinIO client is not initialized"
            
            # Create raw data bucket if it doesn't exist
            if not self.minio_client.bucket_exists(settings.MINIO_RAW_BUCKET):
                self.minio_client.make_bucket(settings.MINIO_RAW_BUCKET)
                logger.info(f"Created MinIO bucket: {settings.MINIO_RAW_BUCKET}")
            
            # Create processed data bucket if it doesn't exist
            if not self.minio_client.bucket_exists(settings.MINIO_PROCESSED_BUCKET):
                self.minio_client.make_bucket(settings.MINIO_PROCESSED_BUCKET)
                logger.info(f"Created MinIO bucket: {settings.MINIO_PROCESSED_BUCKET}")
        except Exception as e:
            logger.error(f"Failed to create buckets: {str(e)}")
            raise
    
    async def list_objects(self, bucket: str, prefix: str = "", recursive: bool = True) -> List[Dict[str, Any]]:
        """
        List objects in a bucket.
        
        Args:
            bucket: The bucket to list objects from
            prefix: The prefix to filter objects by
            recursive: Whether to list objects recursively
            
        Returns:
            List of objects
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Ensure MinIO client is initialized
            assert self.minio_client is not None, "MinIO client is not initialized"
            
            # List objects
            objects = self.minio_client.list_objects(bucket, prefix=prefix, recursive=recursive)
            
            # Convert to list of dictionaries
            result = []
            for obj in objects:
                result.append({
                    "name": obj.object_name,
                    "size": obj.size,
                    "last_modified": obj.last_modified
                })
            
            return result
        except Exception as e:
            logger.error(f"Failed to list objects: {str(e)}")
            raise
    
    async def get_object(self, bucket: str, object_name: str) -> BinaryIO:
        """
        Get an object from a bucket.
        
        Args:
            bucket: The bucket to get the object from
            object_name: The name of the object to get
            
        Returns:
            The object data
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Ensure MinIO client is initialized
            assert self.minio_client is not None, "MinIO client is not initialized"
            
            # Get object
            response = self.minio_client.get_object(bucket, object_name)
            
            return response
        except Exception as e:
            logger.error(f"Failed to get object {object_name}: {str(e)}")
            raise
    
    async def put_object(
        self,
        bucket: str,
        object_name: str,
        data: Union[bytes, BinaryIO],
        length: int,
        content_type: str = "application/octet-stream"
    ) -> Dict[str, Any]:
        """
        Put an object in a bucket.
        
        Args:
            bucket: The bucket to put the object in
            object_name: The name of the object to put
            data: The data to put
            length: The length of the data
            content_type: The content type of the data
            
        Returns:
            Information about the uploaded object
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Ensure MinIO client is initialized
            assert self.minio_client is not None, "MinIO client is not initialized"
            
            # Put object
            etag = self.minio_client.put_object(
                bucket,
                object_name,
                data,
                length,
                content_type
            )
            
            return {
                "bucket": bucket,
                "object_name": object_name,
                "etag": etag,
                "size": length,
                "content_type": content_type
            }
        except Exception as e:
            logger.error(f"Failed to put object {object_name}: {str(e)}")
            raise
    
    async def remove_object(self, bucket: str, object_name: str) -> bool:
        """
        Remove an object from a bucket.
        
        Args:
            bucket: The bucket to remove the object from
            object_name: The name of the object to remove
            
        Returns:
            True if the object was removed, False otherwise
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Ensure MinIO client is initialized
            assert self.minio_client is not None, "MinIO client is not initialized"
            
            # Remove object
            self.minio_client.remove_object(bucket, object_name)
            
            return True
        except Exception as e:
            logger.error(f"Failed to remove object {object_name}: {str(e)}")
            return False
    
    async def get_presigned_url(
        self,
        bucket: str,
        object_name: str,
        expires: int = 3600,
        response_headers: Optional[Dict[str, str]] = None
    ) -> str:
        """
        Get a presigned URL for an object.
        
        Args:
            bucket: The bucket containing the object
            object_name: The name of the object
            expires: The expiration time in seconds
            response_headers: Response headers to include
            
        Returns:
            The presigned URL
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Ensure MinIO client is initialized
            assert self.minio_client is not None, "MinIO client is not initialized"
            
            # Get presigned URL
            url = self.minio_client.presigned_get_object(
                bucket,
                object_name,
                expires=expires,
                response_headers=response_headers
            )
            
            return url
        except Exception as e:
            logger.error(f"Failed to get presigned URL for {object_name}: {str(e)}")
            raise
    
    async def save_dataframe(
        self,
        df: pd.DataFrame,
        bucket: str,
        object_name: str,
        format: str = "parquet",
        **kwargs
    ) -> Dict[str, Any]:
        """
        Save a pandas DataFrame to storage.
        
        Args:
            df: The DataFrame to save
            bucket: The bucket to save to
            object_name: The name of the object to save
            format: The format to save in (parquet, csv, json)
            **kwargs: Additional arguments to pass to the save function
            
        Returns:
            Information about the saved object
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Create a buffer to write to
            buffer = io.BytesIO()
            
            # Save DataFrame to buffer in the specified format
            if format.lower() == "parquet":
                df.to_parquet(buffer, **kwargs)
                content_type = "application/octet-stream"
            elif format.lower() == "csv":
                df.to_csv(buffer, index=False, **kwargs)
                content_type = "text/csv"
            elif format.lower() == "json":
                # to_json doesn't directly support BytesIO, so we need to get the string first
                json_str = df.to_json(orient="records", **kwargs)
                buffer.write(json_str.encode('utf-8'))
                content_type = "application/json"
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            # Get buffer size
            buffer.seek(0)
            size = buffer.getbuffer().nbytes
            
            # Upload buffer to MinIO
            result = await self.put_object(
                bucket,
                object_name,
                buffer,
                size,
                content_type
            )
            
            return result
        except Exception as e:
            logger.error(f"Failed to save DataFrame to {object_name}: {str(e)}")
            raise
    
    async def load_dataframe(
        self,
        bucket: str,
        object_name: str,
        format: Optional[str] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Load a pandas DataFrame from storage.
        
        Args:
            bucket: The bucket to load from
            object_name: The name of the object to load
            format: The format to load from (parquet, csv, json)
            **kwargs: Additional arguments to pass to the load function
            
        Returns:
            The loaded DataFrame
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Determine format from object name if not specified
            if not format:
                if object_name.endswith(".parquet"):
                    format = "parquet"
                elif object_name.endswith(".csv"):
                    format = "csv"
                elif object_name.endswith(".json"):
                    format = "json"
                else:
                    raise ValueError(f"Could not determine format from object name: {object_name}")
            
            # Get object
            response = await self.get_object(bucket, object_name)
            
            # Load DataFrame from the specified format
            if format.lower() == "parquet":
                df = pd.read_parquet(io.BytesIO(response.read()), **kwargs)
            elif format.lower() == "csv":
                df = pd.read_csv(io.BytesIO(response.read()), **kwargs)
            elif format.lower() == "json":
                df = pd.read_json(io.BytesIO(response.read()), **kwargs)
            else:
                raise ValueError(f"Unsupported format: {format}")
            
            return df
        except Exception as e:
            logger.error(f"Failed to load DataFrame from {object_name}: {str(e)}")
            raise
        finally:
            if 'response' in locals():
                response.close()
    
    async def save_json(
        self,
        data: Dict[str, Any],
        bucket: str,
        object_name: str
    ) -> Dict[str, Any]:
        """
        Save JSON data to storage.
        
        Args:
            data: The data to save
            bucket: The bucket to save to
            object_name: The name of the object to save
            
        Returns:
            Information about the saved object
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Convert data to JSON string
            json_str = json.dumps(data)
            
            # Convert JSON string to bytes
            json_bytes = json_str.encode('utf-8')
            
            # Upload JSON to MinIO
            result = await self.put_object(
                bucket,
                object_name,
                io.BytesIO(json_bytes),
                len(json_bytes),
                "application/json"
            )
            
            return result
        except Exception as e:
            logger.error(f"Failed to save JSON to {object_name}: {str(e)}")
            raise
    
    async def load_json(self, bucket: str, object_name: str) -> Dict[str, Any]:
        """
        Load JSON data from storage.
        
        Args:
            bucket: The bucket to load from
            object_name: The name of the object to load
            
        Returns:
            The loaded JSON data
        """
        try:
            # Check if MinIO client is initialized
            if not self.minio_client:
                await self.initialize()
            
            # Get object
            response = await self.get_object(bucket, object_name)
            
            # Load JSON data
            data = json.loads(response.read().decode('utf-8'))
            
            return data
        except Exception as e:
            logger.error(f"Failed to load JSON from {object_name}: {str(e)}")
            raise
        finally:
            if 'response' in locals():
                response.close()
