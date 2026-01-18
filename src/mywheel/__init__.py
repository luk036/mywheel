from importlib.metadata import PackageNotFoundError, version

from .array_like import RepeatArray, ShiftArray
from .bpqueue import BPQueue, BPQueueIterator, Item
from .dllist import Dllink, Dllist, DllIterator
from .map_adapter import MapAdapter
from .robin import Robin, RobinIterator, SlNode

try:
    # Change here if project is renamed and does not equal the package name
    dist_name = __name__
    __version__ = version(dist_name)
except PackageNotFoundError:  # pragma: no cover
    __version__ = "unknown"
finally:
    del version, PackageNotFoundError

__all__ = [
    # Round robin
    "Robin",
    "RobinIterator",
    "SlNode",
    # Doubly linked list
    "Dllist",
    "Dllink",
    "DllIterator",
    # Bounded priority queue
    "BPQueue",
    "BPQueueIterator",
    "Item",
    # Map adapter
    "MapAdapter",
    # Array-like utilities
    "RepeatArray",
    "ShiftArray",
]
