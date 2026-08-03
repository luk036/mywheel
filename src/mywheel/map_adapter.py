from typing import ItemsView, Iterator, List, Mapping, TypeVar, ValuesView

T = TypeVar("T")

__all__ = ["MapAdapter"]


class MapAdapter(Mapping[int, T]):
    __slots__ = ("lst",)

    def __init__(self, lst: List[T]) -> None:
        self.lst = lst

    def __getitem__(self, key: int) -> T:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> a[2]
            3
        """
        return self.lst.__getitem__(key)

    def __setitem__(self, key: int, new_value: T) -> None:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> a[2] = 7
            >>> print(a[2])
            7
        """
        self.lst.__setitem__(key, new_value)

    def __delitem__(self, _: int) -> None:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> del a[0]
            Traceback (most recent call last):
            ...
            NotImplementedError
        """
        raise NotImplementedError()

    def __iter__(self) -> Iterator:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> for i in a:
            ...     print(i)
            0
            1
            2
            3
        """
        return iter(range(len(self.lst)))

    def __contains__(self, value: object) -> bool:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> 2 in a
            True
        """
        return isinstance(value, int) and value < len(self.lst) and value >= 0

    def __len__(self) -> int:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> len(a)
            4
        """
        return len(self.lst)

    def values(self) -> ValuesView[T]:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> for i in a.values():
            ...     print(i)
            1
            4
            3
            6
        """
        return super().values()

    def items(self) -> ItemsView[int, T]:
        """
        Examples:
            >>> a = MapAdapter([1, 4, 3, 6])
            >>> for i, v in a.items():
            ...     print(f"{i}: {v}")
            0: 1
            1: 4
            2: 3
            3: 6
        """
        return super().items()


if __name__ == "__main__":
    map_adapter = MapAdapter([0] * 8)
    for i in map_adapter:
        map_adapter[i] = i * i
    for i, v in map_adapter.items():
        print(f"{i}: {v}")
    print(3 in map_adapter)
