import pytest
import random
from src.mywheel.dllist import Dllink, Dllist
from src.mywheel.bpqueue import BPQueue, Dllink as BPQDllink  # Alias to avoid conflict


# Stress tests for Dllist
def test_dllist_stress_large_add_remove():
    dll = Dllist(0)
    num_elements = 10000
    nodes = [Dllink(i) for i in range(num_elements)]

    for node in nodes:
        dll.append(node)

    assert not dll.is_empty()

    for _ in range(num_elements):
        dll.popleft()

    assert dll.is_empty()


def test_dllist_stress_random_operations():
    dll = Dllist(0)
    num_operations = 5000
    max_value = 1000

    # Keep track of elements added to verify later
    added_elements = set()

    for _ in range(num_operations):
        op = random.choice(["add", "remove"])

        if op == "add":
            value = random.randint(0, max_value)
            node = Dllink(value)
            dll.append(node)
            added_elements.add(id(node))
        elif op == "remove" and not dll.is_empty():
            # Try to remove from left or right randomly
            if random.random() < 0.5:
                removed_node = dll.popleft()
            else:
                removed_node = dll.pop()

            if id(removed_node) in added_elements:
                added_elements.remove(id(removed_node))
            else:
                # This case should ideally not happen if logic is correct
                # but can occur if a node was removed twice (e.g. by random op)
                pass

    # After random operations, clear the list and ensure it's empty
    while not dll.is_empty():
        removed_node = dll.popleft()
        if id(removed_node) in added_elements:
            added_elements.remove(id(removed_node))

    assert dll.is_empty()
    assert len(added_elements) == 0


# Stress tests for BPQueue
def test_bpqueue_stress_large_add_pop():
    bpq = BPQueue(0, 100)  # Priority range from 0 to 100
    num_elements = 10000

    # Add elements with random priorities
    nodes_with_priorities = []
    for i in range(num_elements):
        priority = random.randint(0, 100)
        node = BPQDllink([0, i])  # data[0] is internal key, data[1] is original index
        bpq.append(node, priority)
        nodes_with_priorities.append((node, priority))

    assert not bpq.is_empty()

    # Pop all elements and check if they are generally in decreasing order of priority
    # (within the limits of BPQueue's behavior for same-priority items)
    last_priority = (
        bpq.get_max() + 1
    )  # Initialize with a value higher than max possible
    popped_count = 0
    while not bpq.is_empty():
        popped_node = bpq.popleft()
        current_priority = popped_node.data[0] + bpq._offset
        assert current_priority <= last_priority
        last_priority = current_priority
        popped_count += 1

    assert popped_count == num_elements
    assert bpq.is_empty()


# def test_bpqueue_stress_random_key_modifications():
#     bpq = BPQueue(0, 100)
#     num_elements = 1000
#     num_operations = 5000
#
#     # Add initial elements
#     nodes = []
#     for i in range(num_elements):
#         priority = random.randint(0, 100)
#         node = BPQDllink([0, i])
#         bpq.append(node, priority)
#         nodes.append(node)
#
#     for _ in range(num_operations):
#         op = random.choice(['increase', 'decrease', 'modify', 'pop'])
#         target_node = random.choice(nodes)
#         delta = random.randint(1, 10)
#
#         if op == 'increase':
#             # Ensure key doesn't exceed max bound
#             current_priority = target_node.data[0] + bpq._offset
#             if current_priority + delta <= 100:
#                 bpq.increase_key(target_node, delta)
#         elif op == 'decrease':
#             # Ensure key doesn't go below min bound
#             current_priority = target_node.data[0] + bpq._offset
#             if current_priority - delta >= 0:
#                 bpq.decrease_key(target_node, delta)
#         elif op == 'modify':
#             # Randomly increase or decrease
#             modify_delta = random.randint(-10, 10)
#             current_priority = target_node.data[0] + bpq._offset
#             if 0 <= current_priority + modify_delta <= 100:
#                 bpq.modify_key(target_node, modify_delta)
#         elif op == 'pop' and not bpq.is_empty():
#             bpq.popleft()
#             # Re-add the node to keep the pool of nodes for modification
#             # This might change its priority, but that's part of the stress
#             new_priority = random.randint(0, 100)
#             bpq.append(target_node, new_priority)
#
#     # Ensure no errors during operations and the queue can still be cleared
#     while not bpq.is_empty():
#         bpq.popleft()
#
#     assert bpq.is_empty()
