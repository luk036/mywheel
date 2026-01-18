"""
Round-Robin Implementation

This code implements a round-robin algorithm, which is a method for fairly distributing tasks
or resources among a group of participants. The main purpose of this code is to create a
circular list of elements and provide a way to iterate through them, starting from any given
point.

The code defines three main classes: SlNode, RobinIterator, and Robin. SlNode represents a node
in a singly-linked list, containing a data value and a reference to the next node. RobinIterator
is responsible for iterating over the linked list, while Robin sets up the circular structure
and provides a method to start iterating from a specific point.

The primary input for this code is the number of parts or elements in the round-robin cycle,
which is provided when creating a Robin object. The main output is an iterator that allows you
to cycle through the elements in the list, starting from a specified position.

To achieve its purpose, the code first creates a circular linked list using the SlNode class.
Each node contains an integer value and a reference to the next node. The Robin class sets up
this circular structure by creating a list of nodes and connecting them in a loop.

The key functionality is provided by the exclude method in the Robin class. This method takes an
integer parameter representing the starting position and returns a RobinIterator object. The
iterator allows you to cycle through the elements of the list, starting from the specified
position and continuing until you've gone through all elements except the starting one.

An important aspect of the logic is how the iteration works. The RobinIterator keeps track of
two pointers: curr (current) and stop. As you iterate, curr moves to the next node in the list.
The iteration stops when curr reaches the stop node, which is set to the starting position. This
ensures that you go through all elements exactly once before stopping.

In summary, this code provides a flexible way to implement a round-robin system, allowing users
to start from any point in the cycle and iterate through all other elements before returning to
the starting point. This can be useful in various scenarios, such as task scheduling or resource
allocation, where you need to fairly distribute something among a group of participants in a
circular manner.
"""

from typing import List

__all__ = ["SlNode", "RobinIterator", "Robin"]


class SlNode:
    """Node for a Singly-linked list

    The `SlNode` class represents a node in a singly-linked list, with a `next` pointer and a `data`
    value.

    .. svgbob::
       :align: center

            SlNode
             +---------+
             | next  *-|----->
             +---------+
             |  data   |
             +---------+
    """

    next: "SlNode"
    data: int

    def __init__(self, data: int):
        """
        The function initializes an object with a data attribute and a next attribute that points to itself.

        :param data: The `data` parameter is an integer that represents the value to be stored in the node
        :type data: int
        """
        self.next = self
        self.data = data


class RobinIterator:
    """The `RobinIterator` class is an iterator that iterates over a singly linked list starting from a
    given node.
    """

    __slots__ = ("curr", "stop")
    curr: SlNode
    stop: SlNode

    def __init__(self, node: SlNode) -> None:
        """
        The function initializes the current and stop pointers to the given node.

        :param node: The `node` parameter is an instance of the `SlNode` class. It represents a node in a singly linked list
        :type node: SlNode

        Examples:
            >>> node = SlNode(1)
            >>> iter = RobinIterator(node)
            >>> iter.curr == node
            True
            >>> iter.stop == node
            True
            >>> iter.curr.next == node
            True
            >>> iter.stop.next == node
            True
            >>> iter.curr.data == 1
            True
            >>> iter.stop.data == 1
            True
            >>> iter.curr.next.data == 1
            True
            >>> iter.stop.next.data == 1
            True
            >>> iter.curr.next.next == node
            True
            >>> iter.stop.next.next == node
            True
            >>> iter.curr.next.next.data == 1
            True
            >>> iter.stop.next.next.data == 1
            True
            >>> iter.curr.next.next.next == node
            True
            >>> iter.stop.next.next.next == node
            True
            >>> iter.curr.next.next.next.data == 1
            True
            >>> iter.stop.next.next.next.data == 1
            True
            >>> iter.curr.next.next.next.next == node
            True
        """
        self.curr = self.stop = node

    def __iter__(self) -> "RobinIterator":
        """
        The function returns an instance of the RobinIterator class.

        :return: The `__iter__` method is returning an instance of the `RobinIterator` class.
        """
        return self

    def __next__(self) -> int:
        """
        The __next__ function returns the next item in the iterator.

        :return: The `next()` method is being called and its return value is being returned.
        """
        self.curr = self.curr.next
        if self.curr != self.stop:
            return self.curr.data
        else:
            raise StopIteration()


class Robin:
    """Round Robin

    The `Robin` class implements a round-robin algorithm for cycling through a list of parts, and
    the `exclude` method returns an iterator starting from a specified part.
    The `Robin` class implements a round-robin algorithm for cycling through a list of parts, and
    the `exclude` method returns an iterator starting from a specified part.

    .. svgbob::
       :align: center

      .----------------------------------------------- - - ------------------------------.
      |  +--------+      +--------+      +--------+           +--------+      +--------+  )
      `->|   0  *-|----->|   1  *-|----->|   2  *-|--- - - -->| n-2  *-|----->| n-1  *-|-'
         +--------+      +--------+      +--------+           +--------+      +--------+

    """

    __slots__ = "cycle"
    cycle: List[SlNode]

    def __init__(self, num_parts: int):
        """
        The function initializes a cycle of linked nodes with a given number of parts.

        :param num_parts: The `num_parts` parameter is an integer that represents the number of parts in the cycle
        :type num_parts: int
        """
        if num_parts == 0:
            self.cycle = []
            return
        self.cycle = list(SlNode(k) for k in range(num_parts))
        prev_node = self.cycle[-1]
        for curr_node in self.cycle:
            prev_node.next = curr_node
            prev_node = curr_node

    def exclude(self, from_part: int) -> RobinIterator:
        """
        The `exclude` function returns a `RobinIterator` object that excludes a specified part of a cycle.

        :param from_part: The `from_part` parameter is an integer that represents the starting index of the
                          cycle that should be excluded

        :type from_part: int

        :return: The `exclude` method is returning a `RobinIterator` object.

        Examples:
            >>> r = Robin(5)
            >>> iter = r.exclude(3)
            >>> iter.curr.data == 3
            True
            >>> iter.stop.data == 3
            True
        """
        if not self.cycle:
            raise IndexError("Cannot exclude from an empty cycle.")
        return RobinIterator(self.cycle[from_part])


if __name__ == "__main__":
    robin = Robin(5)
    for k in robin.exclude(3):
        print(k)
