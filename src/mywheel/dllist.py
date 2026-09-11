"""
Doubly Linked List Implementation

This code implements a doubly linked list data structure in Python. A doubly linked list is a
type of data structure where each element (node) contains data and links to both the next and
previous elements in the list.

.. svgbob::
   :align: center

      ┌──────┐    ┌──────┐    ┌──────┐
      │ Data │    │ Data │    │ Data │
      └──┬───┘    └──┬───┘    └──┬───┘
         │           │           │
      ───┼───►  ────┼───►  ────┼───►  next
      ◄──┼───  ◄────┼───  ◄────┼───  prev
         │           │           │
      Head         Node         Tail

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

__all__ = ["Dllink", "DllIterator", "Dllist"]


class Dllink(Generic[T]):
    """A Doubly-linked List class. This class simply contains a link of
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
        Examples:
            >>> a = Dllink(3)
            >>> a.data
            3
        """
        self.next = self.prev = self
        self.data = data

    def is_locked(self) -> bool:
        """
        Examples:
            >>> a = Dllink(3)
            >>> a.is_locked()
            True
        """
        return self.next is self

    def lock(self) -> None:
        """
        Lock the node so it is not attached to any list.

        Examples:
            >>> a = Dllink(3)
            >>> a.lock()
            >>> a.is_locked()
            True
        """
        self.next = self

    def attach(self, node: "Dllink[T]") -> None:
        """
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
    """Iterator over a doubly linked list, starting from the first item.

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
        Examples:
            >>> a = Dllist(3)
            >>> it = iter(a)
        """
        self.link = link
        self.curr = link.next

    def __iter__(self) -> "DllIterator[T]":
        """Return the iterator object itself."""
        return self

    def __next__(self) -> Dllink[T]:
        """
        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.append(b)
            >>> current = iter(a)
            >>> c = next(current)
            >>> id(b) == id(c)
            True
        """
        if self.curr is not self.link:
            res = self.curr
            self.curr = self.curr.next
            return res
        else:
            raise StopIteration()


class Dllist(Generic[T]):
    """Doubly linked list with a sentinel "head" node for fast deletion.

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
        Examples:
            >>> a = Dllist(3)
            >>> a.head.data
            3
        """
        self.head = Dllink(data)

    def is_empty(self) -> bool:
        """
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
        return self.head.next is self.head

    def clear(self) -> None:
        """
        Examples:
            >>> a = Dllist(3)
            >>> a.clear()
            >>> a.is_empty()
            True
        """
        self.head.next = self.head.prev = self.head

    def appendleft(self, node: Dllink[T]) -> None:
        """
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
        Examples:
            >>> a = Dllist(3)
            >>> b = Dllink(4)
            >>> a.append(b)
            >>> a.is_empty()
            False
        """
        self.head.prev.attach(node)

    def popleft(self) -> Dllink[T]:
        """
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

    def pop(self) -> Dllink[T]:
        """
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
