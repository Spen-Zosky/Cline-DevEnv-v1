"""
Type stubs for the bson module.
"""
from typing import Any, Dict, List, Optional, Union, Tuple, Callable, TypeVar, Generic, Iterator, Mapping, Sequence

T = TypeVar('T')

class ObjectId:
    """MongoDB ObjectId type."""
    
    def __init__(self, oid: Optional[Union[str, bytes, 'ObjectId']] = None) -> None:
        """Initialize ObjectId."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this ObjectId."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this ObjectId."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this ObjectId is equal to another ObjectId."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this ObjectId is not equal to another ObjectId."""
        ...
    
    def __lt__(self, other: Any) -> bool:
        """Check if this ObjectId is less than another ObjectId."""
        ...
    
    def __le__(self, other: Any) -> bool:
        """Check if this ObjectId is less than or equal to another ObjectId."""
        ...
    
    def __gt__(self, other: Any) -> bool:
        """Check if this ObjectId is greater than another ObjectId."""
        ...
    
    def __ge__(self, other: Any) -> bool:
        """Check if this ObjectId is greater than or equal to another ObjectId."""
        ...
    
    def __hash__(self) -> int:
        """Return a hash of this ObjectId."""
        ...
    
    def binary(self) -> bytes:
        """Return the binary representation of this ObjectId."""
        ...
    
    def generation_time(self) -> Any:
        """Return the generation time of this ObjectId."""
        ...
    
    @classmethod
    def from_datetime(cls, generation_time: Any) -> 'ObjectId':
        """Create a dummy ObjectId instance with a specific generation time."""
        ...
    
    @classmethod
    def is_valid(cls, oid: Union[str, bytes, 'ObjectId']) -> bool:
        """Check if a string or bytes is a valid ObjectId."""
        ...


class Binary:
    """BSON binary data type."""
    
    def __init__(self, data: bytes, subtype: int = 0) -> None:
        """Initialize Binary."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this Binary."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this Binary."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this Binary is equal to another Binary."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this Binary is not equal to another Binary."""
        ...
    
    def __lt__(self, other: Any) -> bool:
        """Check if this Binary is less than another Binary."""
        ...
    
    def __le__(self, other: Any) -> bool:
        """Check if this Binary is less than or equal to another Binary."""
        ...
    
    def __gt__(self, other: Any) -> bool:
        """Check if this Binary is greater than another Binary."""
        ...
    
    def __ge__(self, other: Any) -> bool:
        """Check if this Binary is greater than or equal to another Binary."""
        ...
    
    def __hash__(self) -> int:
        """Return a hash of this Binary."""
        ...


class Code:
    """BSON code type."""
    
    def __init__(self, code: str, scope: Optional[Dict[str, Any]] = None) -> None:
        """Initialize Code."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this Code."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this Code."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this Code is equal to another Code."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this Code is not equal to another Code."""
        ...


class DBRef:
    """BSON DBRef type."""
    
    def __init__(self, collection: str, id: Any, database: Optional[str] = None, **kwargs: Any) -> None:
        """Initialize DBRef."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this DBRef."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this DBRef."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this DBRef is equal to another DBRef."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this DBRef is not equal to another DBRef."""
        ...


class Decimal128:
    """BSON Decimal128 type."""
    
    def __init__(self, value: Union[str, Any]) -> None:
        """Initialize Decimal128."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this Decimal128."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this Decimal128."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this Decimal128 is equal to another Decimal128."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this Decimal128 is not equal to another Decimal128."""
        ...
    
    def to_decimal(self) -> Any:
        """Return a Decimal instance with the same value as this Decimal128."""
        ...
    
    @classmethod
    def from_decimal(cls, value: Any) -> 'Decimal128':
        """Create a Decimal128 instance from a Decimal."""
        ...


class Int64:
    """BSON int64 type."""
    
    def __init__(self, value: int) -> None:
        """Initialize Int64."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this Int64."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this Int64."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this Int64 is equal to another Int64."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this Int64 is not equal to another Int64."""
        ...
    
    def __lt__(self, other: Any) -> bool:
        """Check if this Int64 is less than another Int64."""
        ...
    
    def __le__(self, other: Any) -> bool:
        """Check if this Int64 is less than or equal to another Int64."""
        ...
    
    def __gt__(self, other: Any) -> bool:
        """Check if this Int64 is greater than another Int64."""
        ...
    
    def __ge__(self, other: Any) -> bool:
        """Check if this Int64 is greater than or equal to another Int64."""
        ...
    
    def __hash__(self) -> int:
        """Return a hash of this Int64."""
        ...


class MaxKey:
    """BSON MaxKey type."""
    
    def __str__(self) -> str:
        """Return a string representation of this MaxKey."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this MaxKey."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this MaxKey is equal to another MaxKey."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this MaxKey is not equal to another MaxKey."""
        ...
    
    def __lt__(self, other: Any) -> bool:
        """Check if this MaxKey is less than another MaxKey."""
        ...
    
    def __le__(self, other: Any) -> bool:
        """Check if this MaxKey is less than or equal to another MaxKey."""
        ...
    
    def __gt__(self, other: Any) -> bool:
        """Check if this MaxKey is greater than another MaxKey."""
        ...
    
    def __ge__(self, other: Any) -> bool:
        """Check if this MaxKey is greater than or equal to another MaxKey."""
        ...
    
    def __hash__(self) -> int:
        """Return a hash of this MaxKey."""
        ...


class MinKey:
    """BSON MinKey type."""
    
    def __str__(self) -> str:
        """Return a string representation of this MinKey."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this MinKey."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this MinKey is equal to another MinKey."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this MinKey is not equal to another MinKey."""
        ...
    
    def __lt__(self, other: Any) -> bool:
        """Check if this MinKey is less than another MinKey."""
        ...
    
    def __le__(self, other: Any) -> bool:
        """Check if this MinKey is less than or equal to another MinKey."""
        ...
    
    def __gt__(self, other: Any) -> bool:
        """Check if this MinKey is greater than another MinKey."""
        ...
    
    def __ge__(self, other: Any) -> bool:
        """Check if this MinKey is greater than or equal to another MinKey."""
        ...
    
    def __hash__(self) -> int:
        """Return a hash of this MinKey."""
        ...


class Regex:
    """BSON regular expression type."""
    
    def __init__(self, pattern: str, flags: Optional[str] = None) -> None:
        """Initialize Regex."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this Regex."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this Regex."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this Regex is equal to another Regex."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this Regex is not equal to another Regex."""
        ...
    
    def try_compile(self) -> Any:
        """Try to compile this BSON regex."""
        ...


class Timestamp:
    """BSON timestamp type."""
    
    def __init__(self, time: int, inc: int) -> None:
        """Initialize Timestamp."""
        ...
    
    def __str__(self) -> str:
        """Return a string representation of this Timestamp."""
        ...
    
    def __repr__(self) -> str:
        """Return a string representation of this Timestamp."""
        ...
    
    def __eq__(self, other: Any) -> bool:
        """Check if this Timestamp is equal to another Timestamp."""
        ...
    
    def __ne__(self, other: Any) -> bool:
        """Check if this Timestamp is not equal to another Timestamp."""
        ...
    
    def __lt__(self, other: Any) -> bool:
        """Check if this Timestamp is less than another Timestamp."""
        ...
    
    def __le__(self, other: Any) -> bool:
        """Check if this Timestamp is less than or equal to another Timestamp."""
        ...
    
    def __gt__(self, other: Any) -> bool:
        """Check if this Timestamp is greater than another Timestamp."""
        ...
    
    def __ge__(self, other: Any) -> bool:
        """Check if this Timestamp is greater than or equal to another Timestamp."""
        ...
    
    def __hash__(self) -> int:
        """Return a hash of this Timestamp."""
        ...


def encode(obj: Any, check_keys: bool = False, codec_options: Any = None) -> bytes:
    """Encode a document to BSON."""
    ...

def decode(data: bytes, codec_options: Any = None) -> Dict[str, Any]:
    """Decode BSON to a document."""
    ...

def decode_all(data: bytes, codec_options: Any = None) -> List[Dict[str, Any]]:
    """Decode BSON to multiple documents."""
    ...

def decode_iter(data: bytes, codec_options: Any = None) -> Iterator[Dict[str, Any]]:
    """Decode BSON to an iterator of documents."""
    ...

def is_valid(bson: bytes) -> bool:
    """Check if the given bytes are valid BSON."""
    ...

def dumps(obj: Any, check_keys: bool = False, codec_options: Any = None) -> bytes:
    """Encode a document to BSON."""
    ...

def loads(data: bytes, codec_options: Any = None) -> Dict[str, Any]:
    """Decode BSON to a document."""
    ...
