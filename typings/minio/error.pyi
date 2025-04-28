"""
Type stubs for the minio.error module.
"""
from typing import Dict, List, Optional, Any


class MinioException(Exception):
    """Base exception for all Minio exceptions."""
    
    def __init__(self, message: str, **kwargs: Any) -> None:
        """Initialize MinioException."""
        ...


class InvalidResponseError(MinioException):
    """Raised when an invalid response is received."""
    ...


class InvalidArgumentError(MinioException):
    """Raised when an invalid argument is passed."""
    ...


class InvalidEndpointError(MinioException):
    """Raised when an invalid endpoint is provided."""
    ...


class NoSuchBucketError(MinioException):
    """Raised when a bucket does not exist."""
    ...


class BucketAlreadyOwnedByYouError(MinioException):
    """Raised when a bucket already exists and is owned by you."""
    ...


class BucketAlreadyExistsError(MinioException):
    """Raised when a bucket already exists."""
    ...


class NoSuchKeyError(MinioException):
    """Raised when a key does not exist."""
    ...


class AccessDeniedError(MinioException):
    """Raised when access is denied."""
    ...


class InvalidBucketNameError(MinioException):
    """Raised when an invalid bucket name is provided."""
    ...


class SignatureDoesNotMatchError(MinioException):
    """Raised when a signature does not match."""
    ...


class NoSuchUploadError(MinioException):
    """Raised when an upload does not exist."""
    ...


class IncompleteBodyError(MinioException):
    """Raised when a body is incomplete."""
    ...


class InternalError(MinioException):
    """Raised when an internal error occurs."""
    ...


class InvalidXMLError(MinioException):
    """Raised when an invalid XML is provided."""
    ...


class InvalidObjectNameError(MinioException):
    """Raised when an invalid object name is provided."""
    ...


class ServerError(MinioException):
    """Raised when a server error occurs."""
    ...


class S3Error(MinioException):
    """Raised when an S3 error occurs."""
    
    def __init__(
        self,
        code: str,
        message: str,
        resource: str = "",
        request_id: str = "",
        host_id: str = "",
        response: Optional[Any] = None,
    ) -> None:
        """Initialize S3Error."""
        ...
