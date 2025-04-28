"""
Type stubs for the dotenv module.
"""
from typing import Any, Dict, Optional, Union, IO

def load_dotenv(
    dotenv_path: Optional[Union[str, IO[str]]] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    override: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = None,
) -> bool:
    """Load environment variables from a .env file."""
    ...

def dotenv_values(
    dotenv_path: Optional[Union[str, IO[str]]] = None,
    stream: Optional[IO[str]] = None,
    verbose: bool = False,
    interpolate: bool = True,
    encoding: Optional[str] = None,
) -> Dict[str, str]:
    """Parse a .env file and return a dictionary of the values."""
    ...

def find_dotenv(
    filename: str = ".env",
    raise_error_if_not_found: bool = False,
    usecwd: bool = False,
) -> str:
    """Search for a .env file and return the path."""
    ...

def set_key(
    dotenv_path: str,
    key_to_set: str,
    value_to_set: str,
    quote_mode: str = "always",
    export: bool = False,
    encoding: Optional[str] = None,
) -> None:
    """Set a key-value pair in a .env file."""
    ...

def unset_key(
    dotenv_path: str,
    key_to_unset: str,
    quote_mode: str = "always",
    encoding: Optional[str] = None,
) -> None:
    """Unset a key in a .env file."""
    ...

def get_key(
    dotenv_path: str,
    key_to_get: str,
    encoding: Optional[str] = None,
) -> Optional[str]:
    """Get the value of a key from a .env file."""
    ...
