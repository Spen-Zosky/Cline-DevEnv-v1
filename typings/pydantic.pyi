from typing import Any, Callable, Dict, List, Optional, Type, TypeVar, Union, overload

T = TypeVar('T')

class BaseModel:
    """Base class for pydantic models."""
    
    class Config:
        """Configuration for the model."""
        allow_population_by_field_name: bool = False
        arbitrary_types_allowed: bool = False
        json_encoders: Dict[Type[Any], Callable[[Any], Any]] = {}
    
    def __init__(self, **data: Any) -> None: ...
    
    def dict(self, **kwargs: Any) -> Dict[str, Any]: ...
    
    def json(self, **kwargs: Any) -> str: ...
    
    @classmethod
    def parse_obj(cls: Type[T], obj: Any) -> T: ...
    
    @classmethod
    def parse_raw(cls: Type[T], b: Union[str, bytes], **kwargs: Any) -> T: ...
    
    @classmethod
    def parse_file(cls: Type[T], path: Union[str, bytes], **kwargs: Any) -> T: ...
    
    @classmethod
    def from_orm(cls: Type[T], obj: Any) -> T: ...
    
    @classmethod
    def schema(cls, **kwargs: Any) -> Dict[str, Any]: ...
    
    @classmethod
    def schema_json(cls, **kwargs: Any) -> str: ...
    
    @classmethod
    def __get_validators__(cls) -> List[Callable[[Any], Any]]: ...
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: Any) -> Any: ...

def Field(
    default: Any = ...,
    *,
    default_factory: Optional[Callable[[], Any]] = None,
    alias: Optional[str] = None,
    title: Optional[str] = None,
    description: Optional[str] = None,
    exclude: Optional[Union[bool, Callable[[Any, str], bool]]] = None,
    include: Optional[Union[bool, Callable[[Any, str], bool]]] = None,
    const: Optional[bool] = None,
    gt: Optional[float] = None,
    ge: Optional[float] = None,
    lt: Optional[float] = None,
    le: Optional[float] = None,
    multiple_of: Optional[float] = None,
    min_items: Optional[int] = None,
    max_items: Optional[int] = None,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    regex: Optional[str] = None,
    **extra: Any,
) -> Any: ...

def validator(*fields: str, **kwargs: Any) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...
