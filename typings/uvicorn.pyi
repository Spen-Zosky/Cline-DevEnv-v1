"""
Type stubs for the uvicorn module.
"""
from typing import Any, Callable, Dict, List, Optional, Union, Type

def run(
    app: Union[str, Callable],
    host: str = "127.0.0.1",
    port: int = 8000,
    uds: Optional[str] = None,
    fd: Optional[int] = None,
    loop: Optional[str] = None,
    http: Optional[str] = None,
    ws: Optional[str] = None,
    lifespan: Optional[str] = None,
    env_file: Optional[str] = None,
    log_config: Optional[Union[Dict[str, Any], str]] = None,
    log_level: Optional[str] = None,
    access_log: bool = True,
    proxy_headers: bool = True,
    server_header: bool = True,
    date_header: bool = True,
    forwarded_allow_ips: Optional[str] = None,
    root_path: str = "",
    limit_concurrency: Optional[int] = None,
    limit_max_requests: Optional[int] = None,
    backlog: int = 2048,
    timeout_keep_alive: int = 5,
    timeout_notify: int = 30,
    callback_notify: Optional[Callable[..., Any]] = None,
    ssl_keyfile: Optional[str] = None,
    ssl_certfile: Optional[Union[str, List[str]]] = None,
    ssl_keyfile_password: Optional[str] = None,
    ssl_version: int = 17,
    ssl_cert_reqs: int = 0,
    ssl_ca_certs: Optional[str] = None,
    ssl_ciphers: str = "TLSv1",
    headers: Optional[List[List[str]]] = None,
    use_colors: Optional[bool] = None,
    app_dir: Optional[str] = None,
    factory: bool = False,
    reload: bool = False,
    reload_dirs: Optional[Union[List[str], str]] = None,
    reload_delay: float = 0.25,
    reload_includes: Optional[Union[List[str], str]] = None,
    reload_excludes: Optional[Union[List[str], str]] = None,
    workers: Optional[int] = None,
    interface: str = "auto",
) -> None:
    """Run a ASGI application using Uvicorn."""
    ...

class Config:
    """Uvicorn configuration class."""
    
    def __init__(
        self,
        app: Union[str, Callable],
        host: str = "127.0.0.1",
        port: int = 8000,
        uds: Optional[str] = None,
        fd: Optional[int] = None,
        loop: Optional[str] = None,
        http: Optional[str] = None,
        ws: Optional[str] = None,
        lifespan: Optional[str] = None,
        env_file: Optional[str] = None,
        log_config: Optional[Union[Dict[str, Any], str]] = None,
        log_level: Optional[str] = None,
        access_log: bool = True,
        proxy_headers: bool = True,
        server_header: bool = True,
        date_header: bool = True,
        forwarded_allow_ips: Optional[str] = None,
        root_path: str = "",
        limit_concurrency: Optional[int] = None,
        limit_max_requests: Optional[int] = None,
        backlog: int = 2048,
        timeout_keep_alive: int = 5,
        timeout_notify: int = 30,
        callback_notify: Optional[Callable[..., Any]] = None,
        ssl_keyfile: Optional[str] = None,
        ssl_certfile: Optional[Union[str, List[str]]] = None,
        ssl_keyfile_password: Optional[str] = None,
        ssl_version: int = 17,
        ssl_cert_reqs: int = 0,
        ssl_ca_certs: Optional[str] = None,
        ssl_ciphers: str = "TLSv1",
        headers: Optional[List[List[str]]] = None,
        use_colors: Optional[bool] = None,
        app_dir: Optional[str] = None,
        factory: bool = False,
        reload: bool = False,
        reload_dirs: Optional[Union[List[str], str]] = None,
        reload_delay: float = 0.25,
        reload_includes: Optional[Union[List[str], str]] = None,
        reload_excludes: Optional[Union[List[str], str]] = None,
        workers: Optional[int] = None,
        interface: str = "auto",
    ) -> None:
        """Initialize Uvicorn configuration."""
        ...
    
    def load(self) -> None:
        """Load the application."""
        ...
    
    def setup_event_loop(self) -> None:
        """Setup the event loop."""
        ...
    
    def bind_socket(self) -> None:
        """Bind the socket."""
        ...
    
    def install_signal_handlers(self) -> None:
        """Install signal handlers."""
        ...
    
    def run(self) -> None:
        """Run the application."""
        ...
