"""
Type stubs for the loguru module.
"""
from typing import Any, Callable, Dict, List, Optional, TextIO, Tuple, Union, overload
import sys
import logging
import datetime


class Logger:
    """Loguru logger."""
    
    def __init__(self) -> None:
        """Initialize Logger."""
        ...
    
    def add(
        self,
        sink: Union[TextIO, str, Callable[[Dict[str, Any]], None], logging.Handler],
        *,
        level: Optional[Union[str, int]] = None,
        format: Optional[str] = None,
        filter: Optional[Union[str, Callable[[Dict[str, Any]], bool]]] = None,
        colorize: Optional[bool] = None,
        serialize: Optional[bool] = None,
        backtrace: Optional[bool] = None,
        diagnose: Optional[bool] = None,
        enqueue: Optional[bool] = None,
        catch: Optional[bool] = None,
        rotation: Optional[Union[str, int, datetime.time, datetime.timedelta, Callable[..., bool]]] = None,
        retention: Optional[Union[str, int, datetime.timedelta]] = None,
        compression: Optional[Union[str, Callable[[str], None]]] = None,
        delay: Optional[bool] = None,
        mode: Optional[str] = None,
        buffering: Optional[int] = None,
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> int:
        """Add a sink to the logger."""
        ...
    
    def remove(self, handler_id: Optional[int] = None) -> None:
        """Remove a sink from the logger."""
        ...
    
    def catch(
        self,
        exception: Union[Callable[..., Any], Tuple[Callable[..., Any], ...], None] = None,
        *,
        level: Optional[Union[str, int]] = None,
        reraise: Optional[bool] = None,
        onerror: Optional[Callable[..., Any]] = None,
        exclude: Optional[Union[type, Tuple[type, ...]]] = None,
        default: Optional[Any] = None,
        message: Optional[str] = None,
    ) -> Callable[..., Any]:
        """Catch exceptions and log them."""
        ...
    
    def opt(
        self,
        *,
        exception: Optional[Union[bool, Tuple[type, ...]]] = None,
        record: Optional[bool] = None,
        lazy: Optional[bool] = None,
        colors: Optional[bool] = None,
        raw: Optional[bool] = None,
        capture: Optional[bool] = None,
        depth: Optional[int] = None,
        ansi: Optional[bool] = None,
    ) -> "Logger":
        """Set options for the logger."""
        ...
    
    def bind(self, **kwargs: Any) -> "Logger":
        """Bind contextual variables to the logger."""
        ...
    
    def contextualize(self, **kwargs: Any) -> "Logger":
        """Contextualize the logger."""
        ...
    
    def patch(self, patcher: Callable[[Dict[str, Any]], Dict[str, Any]]) -> "Logger":
        """Patch the logger."""
        ...
    
    def level(self, name: str, no: int = 0, color: Optional[str] = None, icon: Optional[str] = None) -> "Logger":
        """Add a new level to the logger."""
        ...
    
    def disable(self, name: str) -> None:
        """Disable a logger."""
        ...
    
    def enable(self, name: str) -> None:
        """Enable a logger."""
        ...
    
    def configure(
        self,
        *,
        handlers: List[Dict[str, Any]] = [],
        levels: List[Dict[str, Any]] = [],
        extra: Dict[str, Any] = {},
        patcher: Optional[Callable[[Dict[str, Any]], Dict[str, Any]]] = None,
        activation: List[Tuple[str, bool]] = [],
    ) -> List[int]:
        """Configure the logger."""
        ...
    
    def debug(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log a debug message."""
        ...
    
    def info(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log an info message."""
        ...
    
    def warning(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log a warning message."""
        ...
    
    def error(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log an error message."""
        ...
    
    def critical(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log a critical message."""
        ...
    
    def exception(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log an exception message."""
        ...
    
    def log(self, __level: Union[str, int], __message: str, *args: Any, **kwargs: Any) -> None:
        """Log a message with the specified level."""
        ...
    
    def trace(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log a trace message."""
        ...
    
    def success(self, __message: str, *args: Any, **kwargs: Any) -> None:
        """Log a success message."""
        ...


# Create a global logger instance
logger = Logger()
