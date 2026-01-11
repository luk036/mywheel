"""
Doubly Linked List Implementation

This code implements a doubly linked list data structure in Python. A doubly linked list is a
type of data structure where each element (node) contains data and links to both the next and
previous elements in the list. This implementation provides two main classes: Dllink for
individual nodes and Dllist for the entire list.

The purpose of this code is to provide a flexible and efficient way to store and manipulate
collections of data. It's particularly useful when you need to frequently insert or remove
elements from the middle of a list, as these operations can be performed quickly in a doubly
linked list.

The code doesn't take any specific inputs or produce outputs on its own. Instead, it provides a
set of tools (classes and methods) that programmers can use to create and manipulate doubly
linked lists in their own programs. Users of this code can create lists, add elements to them,
remove elements, and iterate through the lists.

The Dllink class represents individual nodes in the list. Each node contains three pieces of
information: the data it holds, a reference to the next node, and a reference to the previous
node. The Dllist class represents the entire list, using a special "head" node as a reference
point for the start of the list.

The code achieves its purpose through a series of methods that manipulate these nodes and their
connections. For example, the attach method in Dllink adds a new node after the current one by
adjusting the next and previous references of the affected nodes. The appendleft and append
methods in Dllist add new nodes to the beginning or end of the list, respectively.

An important aspect of this implementation is that it doesn't keep track of the list's length.
This design choice saves memory and processing time, as the length doesn't need to be updated
with each operation. However, it means that if a user needs to know the length of the list, they
would need to count the elements manually.

The code also includes an iterator (DllIterator) that allows users to easily traverse the list
from beginning to end. This is particularly useful for processing all elements in the list in
order.

Overall, this doubly linked list implementation provides a powerful and flexible tool for
managing collections of data, especially in situations where frequent insertions and deletions
are needed throughout the list.
"""

from typing import Generic, TypeVar

T = TypeVar("T")


class Dllink(Generic[T]):
    """The `Dllink` class is a doubly linked list implementation that
    does not keep track of the length of the list.

    A Doubly-linked List class. This class simply contains a link of
    node's. By adding a "head" node (sentinel), deleting a node is
    extremely fast (see "Introduction to Algorithm"). This class does
    not keep the length information as it is not necessary for the FM
    algorithm. This saves memory and run-time to update the length
    information. Note that this class does not own the list node. They
    are supplied by the caller in order to better reuse the nodes.

    .. svgbob::
       :align: center

            Dllink
             +---------+
             | next  *-|----->
             +---------+
        <----|-* prev  |
             +---------+
             |  data   |
             +---------+

    Examples:
        >>> a = Dllink(3)
    """

    __slots__ = ("next", "prev", "data")

    next: "Dllink[T]"
    prev: "Dllink[T]"
    data: T

    def __init__(self, data: T) -> None:
        """
            The `__init__` function initializes a `Dllink` object with a given data value and sets the
        `next` and `prev` attributes to point to itself.

        :param data: The `data` parameter is of type `T` and represents the data that will be stored
                     in the `Dllink` object. The `T` type is a generic type, meaning it can be replaced
                     with any specific type when creating an instance of the `Dllink` class
            :type data: T

            Examples:
                >>> a = Dllink(3)
                >>> a.data
                3
        """
        self.next = self.prev = self
        self.data = data

    def is_locked(self) -> bool:
        """
        The `is_locked` function returns `True` if the node is locked, and `False` otherwise.

        :return: The method is returning a boolean value indicating whether the node is locked or not.

        Examples:
            >>> a = Dllink(3)
            >>> a.is_locked()
            True
        """
        return id(self.next) == id(self)

    def lock(self) -> None:
        """
        The `lock` function locks a node by setting its `next` attribute to itself.
        (and don't append it to any list)

        Examples:
            >>> a = Dllink(3)
            >>> a.lock()
            >>> a.is_locked()
            True
        """
        self.next = self

    def attach(self, node: "Dllink[T]") -> None:
        """
        The `attach` function appends a node to the front of a doubly linked list.

        :param node: The `node` parameter is an instance of the `Dllink` class
        :type node: "Dllink[T]"

        Examples:
            >>> a = Dllink(3)
            >>> b = Dllink(4)
            >>> a.attach(b)
        """
        node.next = self.next
        self.next.prev = node
        self.next = node
        node.prev = self

    def detach(self) -> None:
        """
        The `detach` function removes a node from a doubly linked list by updating the previous and next
        pointers of the surrounding nodes.

        .. svgbob::
           :align: center

                         .---------------.
             +--------+  |   +--------+  |   +--------+
           ->| {c}  *-|--'   | {c}  *-|- `-->| {c}  *-|-
            -|-*      |<-.  -|-*      |  .---|-*      |<-
             +--------+  |   +--------+  |   +--------+
                         `---------------'

        Examples:
            >>> a = Dllink(3)
            >>> b = Dllink(4)
            >>> a.attach(b)
            >>> b.detach()
        """
        assert self.next
        next_node = self.next
        prev_node = self.prev
        prev_node.next = next_node
        next_node.prev = prev_node


class DllIterator(Generic[T]):
    """The `DllIterator` class is a list iterator that allows traversal of a doubly
    linked list from the first item.

    .. svgbob::
       :align: center

        +---+     +---+     +---+
        | A | <-> | B | <-> | C |
        +---+     +---+     +---+
          ^         ^
          |         |
         curr      next

    """

    def __init__(self, link: Dllink[T]) -> None:
        """
        The `__init__` function initializes a Dllist object with a given link.

        :param link: The `link` parameter is of type `Dllink[T]`, which means it is a reference to a
                     `Dllink` object. The `Dllink` class is likely a custom class that represents a
                     node in a doubly linked list. The `T` in `Dllink[T]`
        :type link: Dllink[T]

        Examples:
            >>> a = Dllist(3)
            >>> it = iter(a)
        """
        self.link = link
        self.curr = link.next

    def __iter__(self):
        return self

    def __next__(self):
        """
        The `__next__` function returns the next item in a doubly linked list and raises a `StopIteration`
        exception if there are no more items.

        :return: The next item in the Dllist.

        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.append(b)
            >>> current = iter(a)
            >>> c = next(current)
            >>> id(b) == id(c)
            True
        """
        if id(self.curr) != id(self.link):
            res = self.curr
            self.curr = self.curr.next
            return res
        else:
            raise StopIteration()


class Dllist(Generic[T]):
    """The `Dllist` class is a doubly linked list implementation that uses a "head" node for
    efficient deletion operations.

    By adding a "head" node (sentinel), deleting a node is extremely fast (see "Introduction
    to Algorithm"). This class does not keep the length information as it is not necessary for
    the FM algorithm. This saves memory and run-time to update the length information. Note
    that this class does not own the list node. They are supplied by the caller in order to
    better reuse the nodes.

    .. svgbob::
       :align: center

      .----------------------------------------------- ... ------------------------------.
      |  +--------+      +--------+      +--------+           +--------+      +--------+  )
      `->| head *-|----->| {c}  *-|----->| {c}  *-|--- ... -->| {c}  *-|----->| {c}  *-|-'
       .-|-* {a}  |<-----|-*      |<-----|-*      |<-- ... ---|-*      |<-----|-*      |<-.
      (  +--------+      +--------+      +--------+           +--------+      +--------+  |
       `---------------------------------------------- ... -------------------------------'

    """

    __slots__ = "head"

    head: Dllink[T]

    def __init__(self, data: T) -> None:
        """
        The function initializes a doubly linked list with a given data value.

        :param data: The "data" parameter is the value that will be stored in the Dllink object. It can be of any type
        :type data: T

        Examples:
            >>> a = Dllist(3)
            >>> a.head.data
            3
        """
        self.head = Dllink(data)

    def is_empty(self) -> bool:
        """
        The `is_empty` function checks if a doubly linked list is empty.

        :return: a boolean value indicating whether the list is empty or not.

        .. svgbob::
           :align: center

          .-------------.
          |  +--------+  )
          `->| head *-|-'
           .-|-* {a}  |<-.
          (  +--------+  |
           `-------------'

        Examples:
            >>> a = Dllist(3)
            >>> a.is_empty()
            True
        """
        return id(self.head.next) == id(self.head)

    def clear(self) -> None:
        """
        The `clear` function clears all elements from a doubly linked list.

        Examples:
            >>> a = Dllist(3)
            >>> a.clear()
            >>> a.is_empty()
            True
        """
        self.head.next = self.head.prev = self.head

    def appendleft(self, node: Dllink[T]) -> None:
        """
        The `appendleft` function appends a node to the front of a doubly linked list.

        :param node: The `node` parameter is an instance of the `Dllink` class. It represents a node
                     that you want to append to the front of the doubly linked list
        :type node: Dllink[T]

        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.appendleft(b)
            >>> a.is_empty()
            False
        """
        self.head.attach(node)

    def append(self, node: Dllink[T]) -> None:
        """
        The `append` function adds a node to the end of a doubly linked list.

        :param node: The `node` parameter is of type `Dllink[T]`, which represents a node in a doubly
                     linked list
        :type node: Dllink[T]

        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.append(b)
            >>> a.is_empty()
            False
        """
        self.head.prev.attach(node)

    def popleft(self):
        """
        The `popleft` function removes and returns the first node in a doubly linked list.

        :return: The `popleft` method is returning a `Dllink` object.

        .. svgbob::
           :align: center

                         .---------------.
             +--------+  |   +--------+  |   +--------+           +--------+      +--------+
           ->| head *-|--'   | {c}  *-|- `-->| {c}  *-|--- ... -->| {c}  *-|----->| {c}  *-|-
            -|-* {a}  |<-.  -|-*      |  .---|-*      |<-- ... ---|-*      |<-----|-*      |<-
             +--------+  |   +--------+  |   +--------+           +--------+      +--------+
                         `---------------'

        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.appendleft(b)
            >>> c = a.popleft()
            >>> id(b) == id(c)
            True
        """
        res = self.head.next
        res.detach()
        return res

    def pop(self):
        """
        The `pop` function removes and returns the last node in a doubly linked list.

        :return: The `pop` method is returning a `Dllink` object.

        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.append(b)
            >>> c = a.pop()
            >>> id(b) == id(c)
            True
        """
        res = self.head.prev
        res.detach()
        return res

    def __iter__(self) -> DllIterator[T]:
        """
        The `__iter__` function returns an iterator object for a doubly linked list.

        :return: The `__iter__` method is returning an instance of the `DllIterator` class, passing
        `self.head` as an argument.

        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.append(b)
            >>> it = iter(a)
            >>> c = next(it)
            >>> id(b) == id(c)
            True

        """
        return DllIterator(self.head)


if __name__ == "__main__":
    import doctest

    doctest.testmod()
