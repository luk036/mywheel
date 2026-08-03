from __future__ import annotations

from itertools import repeat
from typing import Any, Iterable, Iterator, SupportsIndex, overload

__all__ = ["RepeatArray", "ShiftArray"]


class RepeatArray:
    __slots__ = ("value", "size")

    def __init__(self, value: Any, size: int) -> None:
        """


        Examples:
            >>> repeat_array = RepeatArray(1, 5)
            >>> repeat_array.value
            1
            >>> repeat_array.size
            5

        """
        self.value = value
        self.size = size

    def __getitem__(self, _key: Any) -> Any:  # key is ignored
        """


        Examples:
            >>> repeat_array = RepeatArray(1, 5)
            >>> repeat_array[0]
            1
            >>> repeat_array[1]
            1
            >>> repeat_array[2]
            1
            >>> repeat_array[3]
            1
            >>> repeat_array[4]
            1

        """
        return self.value

    def __len__(self) -> int:
        """


        Examples:
            >>> repeat_array = RepeatArray(1, 5)
            >>> len(repeat_array)
            5

        """
        return self.size

    def __iter__(self) -> Iterator[Any]:
        """


        Examples:
            >>> repeat_array = RepeatArray(1, 5)
            >>> for i in repeat_array:
            ...     print(i)
            1
            1
            1
            1
            1
        """
        return repeat(self.value, self.size)

    def get(self, _item: Any) -> Any:  # defaultvalue is ignored
        """



        Examples:
            >>> repeat_array = RepeatArray(1, 5)
            >>> repeat_array.get(0)
            1
            >>> repeat_array.get(1)
            1
            >>> repeat_array.get(2)
            1
            >>> repeat_array.get(3)
            1
            >>> repeat_array.get(4)
            1

        """
        return self.value


class ShiftArray(list):
    """The `ShiftArray` class is a subclass of the built-in `list` class that allows
    indexing and setting values with an arbitrary starting index.
    """

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        """

        Examples:
            >>> shift_array = ShiftArray([1, 2, 3])
            >>> shift_array.start
            0
            >>> shift_array[0]
            1
            >>> shift_array = ShiftArray([1, 2, 3, 4, 5])
            >>> shift_array.set_start(3)
            >>> shift_array[6]
            4
            >>> shift_array[7]
            5
            >>> shift_array[3]
            1
            >>> shift_array[4]
            2
            >>> shift_array[5]
            3
        """
        super().__init__(*args, **kwargs)
        self.start = 0

    def set_start(self, start: int) -> None:
        """


        Examples:
            >>> shift_array = ShiftArray([1, 2, 3, 4, 5])
            >>> shift_array.set_start(3)
            >>> shift_array[6]
            4
            >>> shift_array[7]
            5
            >>> shift_array[3]
            1
            >>> shift_array[4]
            2
            >>> shift_array[5]
            3
        """
        self.start = start

    @overload
    def __getitem__(self, key: SupportsIndex, /) -> Any:
        ...

    @overload
    def __getitem__(self, key: slice, /) -> list[Any]:
        ...

    def __getitem__(self, key: SupportsIndex | slice, /) -> Any:
        """


        Examples:
            >>> shift_array = ShiftArray([1, 2, 3, 4, 5])
            >>> shift_array.set_start(3)
            >>> shift_array[6]
            4
            >>> shift_array[7]
            5
            >>> shift_array[3]
            1
            >>> shift_array[4]
            2
            >>> shift_array[5]
            3
            >>> shift_array[2]
            Traceback (most recent call last):
            ...
            IndexError: Index out of range
            >>> shift_array[8]
            Traceback (most recent call last):
            ...
            IndexError: Index out of range

        """
        if isinstance(key, slice):
            return list.__getitem__(self, key)
        k = int(key)
        if not (0 <= k - self.start < len(self)):
            raise IndexError("Index out of range")
        return list.__getitem__(self, k - self.start)

    @overload
    def __setitem__(self, key: SupportsIndex, value: Any, /) -> None:
        ...

    @overload
    def __setitem__(self, key: slice, value: Iterable[Any], /) -> None:
        ...

    def __setitem__(self, key: SupportsIndex | slice, newValue: Any, /) -> None:
        """


        Examples:
            >>> shift_array = ShiftArray([1, 2, 3, 4, 5])
            >>> shift_array.set_start(3)
            >>> shift_array[6]
            4
            >>> shift_array[6] = 8
            >>> shift_array[6]
            8
            >>> shift_array[3] = 99
            >>> shift_array[3]
            99
            >>> shift_array
            [99, 2, 3, 8, 5]
        """
        if isinstance(key, slice):
            list.__setitem__(self, key, newValue)
            return
        list.__setitem__(self, int(key) - self.start, newValue)

    def items(self) -> Iterator[tuple[int, Any]]:
        """


        Examples:
            >>> shift_array = ShiftArray([1, 2, 3, 4, 5])
            >>> shift_array.set_start(3)
            >>> for i, v in shift_array.items():
            ...     print(i, v)
            3 1
            4 2
            5 3
            6 4
            7 5

        """
        return iter((i + self.start, v) for i, v in enumerate(self))


# The main function is used to test the classes
if __name__ == "__main__":
    arr = RepeatArray(1, 10)
    print(arr[4])
    for i in arr:
        print(i)

    shift_arr = ShiftArray([9, 4, 1, 3, 8, 7, 6, 5])
    shift_arr.set_start(10)
    print(shift_arr[14])
    for i in shift_arr:
        print(i)
