from mywheel.array_like import RepeatArray, ShiftArray


def test_repeat_array():
    """
    The `test_repeat_array` function is a function that tests the `RepeatArray` class.
    """
    repeat_array = RepeatArray(1, 5)
    assert repeat_array.value == 1
    assert repeat_array.size == 5
    assert repeat_array[0] == 1
    assert repeat_array[1] == 1
    assert repeat_array[2] == 1
    assert repeat_array[3] == 1
    assert repeat_array[4] == 1
    assert len(repeat_array) == 5
    assert repeat_array.get(0) == 1
    assert repeat_array.get(1) == 1
    assert repeat_array.get(2) == 1
    assert repeat_array.get(3) == 1
    assert repeat_array.get(4) == 1
    for i in repeat_array:
        assert i == 1


def test_shift_array():
    """
    The `test_shift_array` function is a function that tests the `ShiftArray` class.
    """
    shift_array = ShiftArray([1, 2, 3, 4, 5])
    shift_array.set_start(3)
    assert shift_array[3] == 1
    assert shift_array[4] == 2
    assert shift_array[5] == 3
    assert shift_array[6] == 4
    assert shift_array[7] == 5
    shift_array[6] = 8
    assert shift_array[6] == 8

    for i, v in shift_array.items():
        assert v == shift_array[i]


if __name__ == "__main__":
    test_repeat_array()
    test_shift_array()
