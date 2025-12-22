from itertools import repeat


class RepeatArray:
    """The RepeatArray class creates a list-like object that repeats a given value for a specified number
    of times.

    .. svgbob::
       :align: center

        +---+---+---+---+---+
        | V | V | V | V | V |
        +---+---+---+---+---+
          0   1   2   3   4
    """

    def __init__(self, value, size):
        """
        The function initializes an object with a value and size attribute.

        :param value: The value parameter is used to store the value of an object. It can be of any data type, such as an integer, string, or even another object
        :param size: The `size` parameter represents the size of an object or data structure.

        Examples:
            >>> repeat_array = RepeatArray(1, 5)
            >>> repeat_array.value
            1
            >>> repeat_array.size
            5

        """
        self.value = value
        self.size = size

    def __getitem__(self, _key):  # key is ignored
        """
        The `__getitem__` function returns the value of the object regardless of the key provided.

        :param _key: The parameter `_key` in the __getitem__ method is used to indicate that the key argument is
                     ignored. It is a convention in Python to use `_key` as a placeholder for variables that are not used or
                     not important in a particular context. In this case, the key argument is not used in the method implementation
        :return: The value stored in the `self.value` attribute.

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

    def __len__(self):
        """
        The function returns the size of an object.

        :return: The size of the object.

        Examples:
            >>> repeat_array = RepeatArray(1, 5)
            >>> len(repeat_array)
            5

        """
        return self.size

    def __iter__(self):
        """
        The function returns an iterator that repeats the value of the object a specified number of times.

        :return: The `repeat` function is being returned.

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

    def get(self, _item):  # defaultvalue is ignored
        """
        The `get` function returns the value of the object.

        :param _item: The underscore `_item` is a convention in Python to indicate that a parameter is not going to
                      be used in the function. In this case, the parameter is ignored and not used in the function logic

        :return: The value of the `self.value` attribute is being returned.

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


# The ShiftArray class is a subclass of the list class that allows for indexing and setting values
# with an arbitrary starting index.
class ShiftArray(list):
    """ShiftArray
    The `ShiftArray` class is a subclass of the built-in `list` class in Python. It extends the
    functionality of a list by allowing the user to set a starting index for the list.
    list with arbitrary range
    """

    def __init__(self, *args, **kwargs):
        """
        The function is a constructor that initializes an object with a start value of 0 and calls the
        constructor of the parent class "list".

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

    def set_start(self, start):
        """
        The function sets the value of the "start" attribute.

        :param start: The `start` parameter is a value that will be assigned to the `start` attribute of the object

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

    def __getitem__(self, key):
        """
        The `__getitem__` function returns the item at the specified index, adjusted by the `start` attribute.

        :param key: The `key` parameter is the index or slice object used to access the elements of the list. It can be an integer index or a slice object that specifies a range of indices
        :return: The method is returning the item at the specified index in the list.

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
        if not (0 <= key - self.start < len(self)):
            raise IndexError("Index out of range")
        return list.__getitem__(self, key - self.start)

    def __setitem__(self, key, newValue):
        """
        The `__setitem__` function is used to set the value of an item in a list-like object, adjusting the
        index based on the start value.

        :param key: The key parameter represents the index of the element in the list that you want to set a new value for
        :param newValue: The `newValue` parameter is the value that you want to set for the given key in the list

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
        list.__setitem__(self, key - self.start, newValue)

    def items(self):
        """
        The `items` function returns an iterator that yields tuples containing the index and value of each
        element in the object.

        :return: The `items` method is returning an iterator that yields tuples containing the index (starting from `self.start`) and the corresponding value for each element in the object.

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
