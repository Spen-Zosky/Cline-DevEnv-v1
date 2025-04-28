"""
Type stubs for the fastapi.middleware.cors module.
"""
from typing import Any, Callable, Dict, List, Optional, Sequence, Set, Tuple, Union

class CORSMiddleware:
    """CORS middleware class."""
    
    def __init__(
        self,
        app: Any,
        allow_origins: Sequence[str] = (),
        allow_methods: Sequence[str] = ("GET",),
        allow_headers: Sequence[str] = (),
        allow_credentials: bool = False,
        allow_origin_regex: Optional[str] = None,
        expose_headers: Sequence[str] = (),
        max_age: int = 600,
    ) -> None:
        """Initialize CORSMiddleware."""
        ...
    
    async def __call__(self, scope: Dict[str, Any], receive: Callable, send: Callable) -> None:
        """Call the middleware."""
        ...
