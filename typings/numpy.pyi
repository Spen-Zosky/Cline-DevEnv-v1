"""
Type stubs for the numpy module.
"""
from typing import Any, Callable, Dict, List, Optional, Tuple, Union, overload, TypeVar, Generic
import datetime

# Type variables
T = TypeVar('T')
DType = TypeVar('DType')
Shape = Tuple[int, ...]


class ndarray(Generic[DType]):
    """N-dimensional array."""
    
    shape: Shape
    dtype: DType
    size: int
    ndim: int
    
    def __init__(self, shape: Shape, dtype: DType = None, buffer: Any = None, offset: int = 0, strides: Any = None, order: str = 'C') -> None:
        """Initialize ndarray."""
        ...
    
    def __getitem__(self, key: Any) -> 'ndarray[DType]':
        """Get item."""
        ...
    
    def __setitem__(self, key: Any, value: Any) -> None:
        """Set item."""
        ...
    
    def astype(self, dtype: Any, order: str = 'K', casting: str = 'unsafe', subok: bool = True, copy: bool = True) -> 'ndarray[Any]':
        """Cast array to a specified type."""
        ...
    
    def copy(self, order: str = 'C') -> 'ndarray[DType]':
        """Return a copy of the array."""
        ...
    
    def fill(self, value: Any) -> None:
        """Fill the array with a scalar value."""
        ...
    
    def reshape(self, *shape: Any) -> 'ndarray[DType]':
        """Return a new array with a new shape."""
        ...
    
    def transpose(self, *axes: Any) -> 'ndarray[DType]':
        """Return a view of the array with axes transposed."""
        ...
    
    def flatten(self, order: str = 'C') -> 'ndarray[DType]':
        """Return a copy of the array collapsed into one dimension."""
        ...
    
    def ravel(self, order: str = 'C') -> 'ndarray[DType]':
        """Return a flattened array."""
        ...
    
    def squeeze(self, axis: Optional[Union[int, Tuple[int, ...]]] = None) -> 'ndarray[DType]':
        """Remove single-dimensional entries from the shape of an array."""
        ...
    
    def sum(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype: Optional[Any] = None, out: Optional['ndarray[Any]'] = None, keepdims: bool = False, initial: Optional[Any] = None, where: Optional['ndarray[Any]'] = None) -> Union['ndarray[Any]', Any]:
        """Return the sum of the array elements over the given axis."""
        ...
    
    def mean(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype: Optional[Any] = None, out: Optional['ndarray[Any]'] = None, keepdims: bool = False, where: Optional['ndarray[Any]'] = None) -> Union['ndarray[Any]', Any]:
        """Return the average of the array elements along the given axis."""
        ...
    
    def std(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype: Optional[Any] = None, out: Optional['ndarray[Any]'] = None, ddof: int = 0, keepdims: bool = False, where: Optional['ndarray[Any]'] = None) -> Union['ndarray[Any]', Any]:
        """Return the standard deviation of the array elements along the given axis."""
        ...
    
    def min(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, out: Optional['ndarray[Any]'] = None, keepdims: bool = False, initial: Optional[Any] = None, where: Optional['ndarray[Any]'] = None) -> Union['ndarray[Any]', Any]:
        """Return the minimum of the array elements along the given axis."""
        ...
    
    def max(self, axis: Optional[Union[int, Tuple[int, ...]]] = None, out: Optional['ndarray[Any]'] = None, keepdims: bool = False, initial: Optional[Any] = None, where: Optional['ndarray[Any]'] = None) -> Union['ndarray[Any]', Any]:
        """Return the maximum of the array elements along the given axis."""
        ...
    
    def argmin(self, axis: Optional[int] = None, out: Optional['ndarray[Any]'] = None) -> Union['ndarray[Any]', Any]:
        """Return indices of the minimum values along the given axis."""
        ...
    
    def argmax(self, axis: Optional[int] = None, out: Optional['ndarray[Any]'] = None) -> Union['ndarray[Any]', Any]:
        """Return indices of the maximum values along the given axis."""
        ...
    
    def tolist(self) -> List[Any]:
        """Return the array as a (possibly nested) list."""
        ...
    
    def tobytes(self, order: str = 'C') -> bytes:
        """Construct Python bytes containing the raw data bytes in the array."""
        ...


# Common functions
def array(object: Any, dtype: Optional[Any] = None, copy: bool = True, order: str = 'K', subok: bool = False, ndmin: int = 0) -> ndarray[Any]:
    """Create an array."""
    ...

def zeros(shape: Union[int, Shape], dtype: Optional[Any] = None, order: str = 'C') -> ndarray[Any]:
    """Return a new array of given shape and type, filled with zeros."""
    ...

def ones(shape: Union[int, Shape], dtype: Optional[Any] = None, order: str = 'C') -> ndarray[Any]:
    """Return a new array of given shape and type, filled with ones."""
    ...

def empty(shape: Union[int, Shape], dtype: Optional[Any] = None, order: str = 'C') -> ndarray[Any]:
    """Return a new array of given shape and type, without initializing entries."""
    ...

def eye(N: int, M: Optional[int] = None, k: int = 0, dtype: Optional[Any] = None, order: str = 'C') -> ndarray[Any]:
    """Return a 2-D array with ones on the diagonal and zeros elsewhere."""
    ...

def identity(n: int, dtype: Optional[Any] = None) -> ndarray[Any]:
    """Return the identity array."""
    ...

def arange(start: Union[int, float], stop: Optional[Union[int, float]] = None, step: Union[int, float] = 1, dtype: Optional[Any] = None) -> ndarray[Any]:
    """Return evenly spaced values within a given interval."""
    ...

def linspace(start: Union[int, float], stop: Union[int, float], num: int = 50, endpoint: bool = True, retstep: bool = False, dtype: Optional[Any] = None, axis: int = 0) -> Union[ndarray[Any], Tuple[ndarray[Any], float]]:
    """Return evenly spaced numbers over a specified interval."""
    ...

def concatenate(arrays: Union[List[ndarray[Any]], Tuple[ndarray[Any], ...]], axis: int = 0, out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Join a sequence of arrays along an existing axis."""
    ...

def vstack(tup: Union[List[ndarray[Any]], Tuple[ndarray[Any], ...]]) -> ndarray[Any]:
    """Stack arrays in sequence vertically (row wise)."""
    ...

def hstack(tup: Union[List[ndarray[Any]], Tuple[ndarray[Any], ...]]) -> ndarray[Any]:
    """Stack arrays in sequence horizontally (column wise)."""
    ...

def stack(arrays: Union[List[ndarray[Any]], Tuple[ndarray[Any], ...]], axis: int = 0, out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Join a sequence of arrays along a new axis."""
    ...

def split(ary: ndarray[Any], indices_or_sections: Union[int, List[int], ndarray[Any]], axis: int = 0) -> List[ndarray[Any]]:
    """Split an array into multiple sub-arrays."""
    ...

def random_sample(size: Optional[Union[int, Shape]] = None) -> Union[float, ndarray[Any]]:
    """Return random floats in the half-open interval [0.0, 1.0)."""
    ...

def randn(*args: int) -> Union[float, ndarray[Any]]:
    """Return a sample (or samples) from the "standard normal" distribution."""
    ...

def randint(low: int, high: Optional[int] = None, size: Optional[Union[int, Shape]] = None, dtype: Optional[Any] = None) -> Union[int, ndarray[Any]]:
    """Return random integers from low (inclusive) to high (exclusive)."""
    ...

def seed(seed: Optional[int] = None) -> None:
    """Seed the generator."""
    ...

def mean(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype: Optional[Any] = None, out: Optional[ndarray[Any]] = None, keepdims: bool = False) -> Union[ndarray[Any], Any]:
    """Compute the arithmetic mean along the specified axis."""
    ...

def std(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype: Optional[Any] = None, out: Optional[ndarray[Any]] = None, ddof: int = 0, keepdims: bool = False) -> Union[ndarray[Any], Any]:
    """Compute the standard deviation along the specified axis."""
    ...

def min(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, out: Optional[ndarray[Any]] = None, keepdims: bool = False, initial: Optional[Any] = None, where: Optional[ndarray[Any]] = None) -> Union[ndarray[Any], Any]:
    """Return the minimum of an array or minimum along an axis."""
    ...

def max(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, out: Optional[ndarray[Any]] = None, keepdims: bool = False, initial: Optional[Any] = None, where: Optional[ndarray[Any]] = None) -> Union[ndarray[Any], Any]:
    """Return the maximum of an array or maximum along an axis."""
    ...

def argmin(a: ndarray[Any], axis: Optional[int] = None, out: Optional[ndarray[Any]] = None) -> Union[ndarray[Any], Any]:
    """Return indices of the minimum values along the given axis."""
    ...

def argmax(a: ndarray[Any], axis: Optional[int] = None, out: Optional[ndarray[Any]] = None) -> Union[ndarray[Any], Any]:
    """Return indices of the maximum values along the given axis."""
    ...

def sum(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype: Optional[Any] = None, out: Optional[ndarray[Any]] = None, keepdims: bool = False, initial: Optional[Any] = None, where: Optional[ndarray[Any]] = None) -> Union[ndarray[Any], Any]:
    """Sum of array elements over a given axis."""
    ...

def prod(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, dtype: Optional[Any] = None, out: Optional[ndarray[Any]] = None, keepdims: bool = False, initial: Optional[Any] = None, where: Optional[ndarray[Any]] = None) -> Union[ndarray[Any], Any]:
    """Product of array elements over a given axis."""
    ...

def abs(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Calculate the absolute value element-wise."""
    ...

def sqrt(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Return the non-negative square-root of an array, element-wise."""
    ...

def exp(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Calculate the exponential of all elements in the input array."""
    ...

def log(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Natural logarithm, element-wise."""
    ...

def sin(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Trigonometric sine, element-wise."""
    ...

def cos(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Cosine element-wise."""
    ...

def tan(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Compute tangent element-wise."""
    ...

def arcsin(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Inverse sine, element-wise."""
    ...

def arccos(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Trigonometric inverse cosine, element-wise."""
    ...

def arctan(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Trigonometric inverse tangent, element-wise."""
    ...

def degrees(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Convert angles from radians to degrees."""
    ...

def radians(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Convert angles from degrees to radians."""
    ...

def dot(a: ndarray[Any], b: ndarray[Any], out: Optional[ndarray[Any]] = None) -> Union[ndarray[Any], Any]:
    """Dot product of two arrays."""
    ...

def matmul(a: ndarray[Any], b: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Matrix product of two arrays."""
    ...

def transpose(a: ndarray[Any], axes: Optional[Union[Tuple[int, ...], List[int]]] = None) -> ndarray[Any]:
    """Permute the dimensions of an array."""
    ...

def reshape(a: ndarray[Any], newshape: Union[int, Shape], order: str = 'C') -> ndarray[Any]:
    """Gives a new shape to an array without changing its data."""
    ...

def ravel(a: ndarray[Any], order: str = 'C') -> ndarray[Any]:
    """Return a contiguous flattened array."""
    ...

def flatten(a: ndarray[Any], order: str = 'C') -> ndarray[Any]:
    """Return a copy of the array collapsed into one dimension."""
    ...

def squeeze(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None) -> ndarray[Any]:
    """Remove single-dimensional entries from the shape of an array."""
    ...

def expand_dims(a: ndarray[Any], axis: int) -> ndarray[Any]:
    """Expand the shape of an array."""
    ...

def where(condition: ndarray[Any], x: Union[ndarray[Any], Any], y: Union[ndarray[Any], Any]) -> ndarray[Any]:
    """Return elements chosen from x or y depending on condition."""
    ...

def isnan(x: ndarray[Any]) -> ndarray[Any]:
    """Test element-wise for NaN and return result as a boolean array."""
    ...

def isinf(x: ndarray[Any]) -> ndarray[Any]:
    """Test element-wise for positive or negative infinity."""
    ...

def isfinite(x: ndarray[Any]) -> ndarray[Any]:
    """Test element-wise for finiteness (not infinity or not Not a Number)."""
    ...

def logical_and(x1: ndarray[Any], x2: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Compute the truth value of x1 AND x2 element-wise."""
    ...

def logical_or(x1: ndarray[Any], x2: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Compute the truth value of x1 OR x2 element-wise."""
    ...

def logical_not(x: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Compute the truth value of NOT x element-wise."""
    ...

def logical_xor(x1: ndarray[Any], x2: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Compute the truth value of x1 XOR x2, element-wise."""
    ...

def all(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, out: Optional[ndarray[Any]] = None, keepdims: bool = False) -> Union[ndarray[Any], bool]:
    """Test whether all array elements along a given axis evaluate to True."""
    ...

def any(a: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None, out: Optional[ndarray[Any]] = None, keepdims: bool = False) -> Union[ndarray[Any], bool]:
    """Test whether any array element along a given axis evaluates to True."""
    ...

def sort(a: ndarray[Any], axis: int = -1, kind: Optional[str] = None, order: Optional[Union[str, List[str]]] = None) -> ndarray[Any]:
    """Return a sorted copy of an array."""
    ...

def argsort(a: ndarray[Any], axis: int = -1, kind: Optional[str] = None, order: Optional[Union[str, List[str]]] = None) -> ndarray[Any]:
    """Returns the indices that would sort an array."""
    ...

def unique(ar: ndarray[Any], return_index: bool = False, return_inverse: bool = False, return_counts: bool = False, axis: Optional[int] = None) -> Union[ndarray[Any], Tuple[ndarray[Any], ...]]:
    """Find the unique elements of an array."""
    ...

def tile(A: ndarray[Any], reps: Union[int, Shape]) -> ndarray[Any]:
    """Construct an array by repeating A the number of times given by reps."""
    ...

def repeat(a: ndarray[Any], repeats: Union[int, ndarray[Any]], axis: Optional[int] = None) -> ndarray[Any]:
    """Repeat elements of an array."""
    ...

def roll(a: ndarray[Any], shift: Union[int, Shape], axis: Optional[Union[int, Shape]] = None) -> ndarray[Any]:
    """Roll array elements along a given axis."""
    ...

def rot90(m: ndarray[Any], k: int = 1, axes: Tuple[int, int] = (0, 1)) -> ndarray[Any]:
    """Rotate an array by 90 degrees in the plane specified by axes."""
    ...

def flip(m: ndarray[Any], axis: Optional[Union[int, Tuple[int, ...]]] = None) -> ndarray[Any]:
    """Reverse the order of elements in an array along the given axis."""
    ...

def fliplr(m: ndarray[Any]) -> ndarray[Any]:
    """Flip array in the left/right direction."""
    ...

def flipud(m: ndarray[Any]) -> ndarray[Any]:
    """Flip array in the up/down direction."""
    ...

def meshgrid(*xi: ndarray[Any], copy: bool = True, sparse: bool = False, indexing: str = 'xy') -> List[ndarray[Any]]:
    """Return coordinate matrices from coordinate vectors."""
    ...

def mgrid() -> Any:
    """nd_grid instance which returns a dense multi-dimensional 'meshgrid'."""
    ...

def ogrid() -> Any:
    """nd_grid instance which returns an open multi-dimensional 'meshgrid'."""
    ...

def diag(v: ndarray[Any], k: int = 0) -> ndarray[Any]:
    """Extract a diagonal or construct a diagonal array."""
    ...

def diagflat(v: ndarray[Any], k: int = 0) -> ndarray[Any]:
    """Create a two-dimensional array with the flattened input as a diagonal."""
    ...

def tril(m: ndarray[Any], k: int = 0) -> ndarray[Any]:
    """Lower triangle of an array."""
    ...

def triu(m: ndarray[Any], k: int = 0) -> ndarray[Any]:
    """Upper triangle of an array."""
    ...

def vander(x: ndarray[Any], N: Optional[int] = None, increasing: bool = False) -> ndarray[Any]:
    """Generate a Vandermonde matrix."""
    ...

def histogram(a: ndarray[Any], bins: Union[int, ndarray[Any], List[float]], range: Optional[Tuple[float, float]] = None, normed: Optional[bool] = None, weights: Optional[ndarray[Any]] = None, density: Optional[bool] = None) -> Tuple[ndarray[Any], ndarray[Any]]:
    """Compute the histogram of a set of data."""
    ...

def histogram2d(x: ndarray[Any], y: ndarray[Any], bins: Union[int, Tuple[int, int], ndarray[Any], Tuple[ndarray[Any], ndarray[Any]]] = 10, range: Optional[Union[Tuple[Tuple[float, float], Tuple[float, float]], Tuple[Optional[Tuple[float, float]], Optional[Tuple[float, float]]]]] = None, normed: Optional[bool] = None, weights: Optional[ndarray[Any]] = None, density: Optional[bool] = None) -> Tuple[ndarray[Any], ndarray[Any], ndarray[Any]]:
    """Compute the bi-dimensional histogram of two data samples."""
    ...

def histogramdd(sample: ndarray[Any], bins: Union[int, Tuple[int, ...], List[ndarray[Any]], Tuple[ndarray[Any], ...]] = 10, range: Optional[Union[List[Tuple[float, float]], Tuple[Tuple[float, float], ...]]] = None, normed: Optional[bool] = None, weights: Optional[ndarray[Any]] = None, density: Optional[bool] = None) -> Tuple[ndarray[Any], List[ndarray[Any]]]:
    """Compute the multidimensional histogram of some data."""
    ...

def bincount(x: ndarray[Any], weights: Optional[ndarray[Any]] = None, minlength: int = 0) -> ndarray[Any]:
    """Count number of occurrences of each value in array of non-negative ints."""
    ...

def digitize(x: ndarray[Any], bins: ndarray[Any], right: bool = False) -> ndarray[Any]:
    """Return the indices of the bins to which each value in input array belongs."""
    ...

def correlate(a: ndarray[Any], v: ndarray[Any], mode: str = 'valid') -> ndarray[Any]:
    """Cross-correlation of two 1-dimensional sequences."""
    ...

def convolve(a: ndarray[Any], v: ndarray[Any], mode: str = 'full') -> ndarray[Any]:
    """Returns the discrete, linear convolution of two one-dimensional sequences."""
    ...

def outer(a: ndarray[Any], b: ndarray[Any], out: Optional[ndarray[Any]] = None) -> ndarray[Any]:
    """Compute the outer product of two vectors."""
    ...

def inner(a: ndarray[Any], b: ndarray[Any]) -> Union[ndarray[Any], Any]:
    """Inner product of two arrays."""
    ...

def tensordot(a: ndarray[Any], b: ndarray[Any], axes: Union[int, Tuple[int, int]] = 2) -> ndarray[Any]:
    """Compute tensor dot product along specified axes."""
    ...

def kron(a: ndarray[Any], b: ndarray[Any]) -> ndarray[Any]:
    """Kronecker product of two arrays."""
    ...

def einsum(subscripts: str, *operands: ndarray[Any], out: Optional[ndarray[Any]] = None, dtype: Optional[Any] = None, order: str = 'K', casting: str = 'safe', optimize: Union[bool, str, int] = False) -> ndarray[Any]:
    """Evaluates the Einstein summation convention on the operands."""
    ...

# Module-like objects
class LinAlg:
    """Linear algebra functions."""
    ...

linalg = LinAlg()

class FFT:
    """Discrete Fourier Transform."""
    ...

fft = FFT()

class Polynomial:
    """Polynomial functions."""
    ...

polynomial = Polynomial()

class Random:
    """Random sampling (numpy.random)."""
    ...

random = Random()

class MaskedArray:
    """Masked array operations."""
    ...

ma = MaskedArray()

def newaxis() -> None:
    """None object, can be used to add a new axis to an array."""
    ...

def inf() -> float:
    """IEEE 754 floating point representation of (positive) infinity."""
    ...

def nan() -> float:
    """IEEE 754 floating point representation of Not a Number (NaN)."""
    ...

def pi() -> float:
    """The mathematical constant π."""
    ...

def e() -> float:
    """The mathematical constant e."""
    ...

def euler_gamma() -> float:
    """The Euler-Mascheroni constant γ."""
    ...
