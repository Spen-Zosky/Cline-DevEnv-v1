"""
Type stubs for the fastapi.responses module.
"""
from typing import Any, Dict, List, Optional, Union, Type, TypeVar, Generic
import json

T = TypeVar('T')

class Response:
    """Base response class."""
    
    media_type: Optional[str] = None
    
    def __init__(
        self,
        content: Any = None,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[Any] = None,
    ) -> None:
        """Initialize Response."""
        ...
    
    def render(self, content: Any) -> bytes:
        """Render the content."""
        ...
    
    def set_cookie(
        self,
        key: str,
        value: str = "",
        max_age: Optional[int] = None,
        expires: Optional[int] = None,
        path: str = "/",
        domain: Optional[str] = None,
        secure: bool = False,
        httponly: bool = False,
        samesite: Optional[str] = None,
    ) -> None:
        """Set a cookie in the response."""
        ...
    
    def delete_cookie(
        self,
        key: str,
        path: str = "/",
        domain: Optional[str] = None,
    ) -> None:
        """Delete a cookie."""
        ...


class JSONResponse(Response):
    """JSON response class."""
    
    media_type: str = "application/json"
    
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[Any] = None,
    ) -> None:
        """Initialize JSONResponse."""
        ...
    
    def render(self, content: Any) -> bytes:
        """Render the content."""
        ...


class HTMLResponse(Response):
    """HTML response class."""
    
    media_type: str = "text/html"
    
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[Any] = None,
    ) -> None:
        """Initialize HTMLResponse."""
        ...


class PlainTextResponse(Response):
    """Plain text response class."""
    
    media_type: str = "text/plain"
    
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[Any] = None,
    ) -> None:
        """Initialize PlainTextResponse."""
        ...


class RedirectResponse(Response):
    """Redirect response class."""
    
    def __init__(
        self,
        url: str,
        status_code: int = 307,
        headers: Optional[Dict[str, str]] = None,
        background: Optional[Any] = None,
    ) -> None:
        """Initialize RedirectResponse."""
        ...


class StreamingResponse(Response):
    """Streaming response class."""
    
    def __init__(
        self,
        content: Any,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[Any] = None,
    ) -> None:
        """Initialize StreamingResponse."""
        ...


class FileResponse(Response):
    """File response class."""
    
    def __init__(
        self,
        path: str,
        status_code: int = 200,
        headers: Optional[Dict[str, str]] = None,
        media_type: Optional[str] = None,
        background: Optional[Any] = None,
        filename: Optional[str] = None,
        stat_result: Optional[Any] = None,
        method: Optional[str] = None,
    ) -> None:
        """Initialize FileResponse."""
        ...
