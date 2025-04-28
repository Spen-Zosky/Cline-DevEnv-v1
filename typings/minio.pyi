"""
Type stubs for the minio module.
"""
from typing import Dict, List, Optional, Any, Union, BinaryIO, Iterator


class Object:
    """Object information."""
    bucket_name: str
    object_name: str
    last_modified: str
    etag: str
    size: int
    content_type: str
    is_dir: bool


class Minio:
    """MinIO client."""
    
    def __init__(
        self,
        endpoint: str,
        access_key: Optional[str] = None,
        secret_key: Optional[str] = None,
        session_token: Optional[str] = None,
        secure: bool = True,
        region: Optional[str] = None,
        http_client: Optional[Any] = None,
        credentials: Optional[Any] = None,
    ) -> None:
        """Initialize MinIO client."""
        ...
    
    def bucket_exists(self, bucket_name: str) -> bool:
        """Check if a bucket exists."""
        ...
    
    def make_bucket(self, bucket_name: str, location: str = "us-east-1") -> None:
        """Create a bucket."""
        ...
    
    def list_buckets(self) -> List[Any]:
        """List all buckets."""
        ...
    
    def remove_bucket(self, bucket_name: str) -> None:
        """Remove a bucket."""
        ...
    
    def list_objects(
        self,
        bucket_name: str,
        prefix: str = "",
        recursive: bool = False,
        start_after: str = "",
        include_user_meta: bool = False,
        include_version: bool = False,
    ) -> Iterator[Object]:
        """List objects in a bucket."""
        ...
    
    def get_object(
        self,
        bucket_name: str,
        object_name: str,
        offset: int = 0,
        length: int = 0,
        request_headers: Optional[Dict[str, str]] = None,
        ssec: Optional[Any] = None,
        version_id: Optional[str] = None,
        extra_query_params: Optional[Dict[str, str]] = None,
    ) -> BinaryIO:
        """Get an object from a bucket."""
        ...
    
    def put_object(
        self,
        bucket_name: str,
        object_name: str,
        data: Union[bytes, BinaryIO],
        length: int,
        content_type: str = "application/octet-stream",
        metadata: Optional[Dict[str, str]] = None,
        sse: Optional[Any] = None,
        progress: Optional[Any] = None,
        part_size: int = 0,
        num_parallel_uploads: int = 3,
        tags: Optional[Dict[str, str]] = None,
        retention: Optional[Any] = None,
        legal_hold: bool = False,
    ) -> str:
        """Put an object in a bucket."""
        ...
    
    def remove_object(
        self,
        bucket_name: str,
        object_name: str,
        version_id: Optional[str] = None,
        bypass_governance_mode: bool = False,
    ) -> None:
        """Remove an object from a bucket."""
        ...
    
    def presigned_get_object(
        self,
        bucket_name: str,
        object_name: str,
        expires: int = 604800,
        response_headers: Optional[Dict[str, str]] = None,
        request_date: Optional[Any] = None,
        version_id: Optional[str] = None,
        extra_query_params: Optional[Dict[str, str]] = None,
    ) -> str:
        """Get a presigned URL for an object."""
        ...
