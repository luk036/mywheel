#include "doctest.h"
#include "bpqueue.hpp"

using namespace cpp_ai;

TEST_CASE("BPQueueTest - Constructor") {
    BPQueue bpq(-3, 3);
    CHECK(bpq.is_empty());
    CHECK(bpq.get_max() == -4); // a - 1
}

TEST_CASE("BPQueueTest - AppendAndPop") {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    Dllink<std::array<int, 2>> b({0, 2});
    Dllink<std::array<int, 2>> c({0, 3});

    bpq.append(&a, 3);
    bpq.append(&b, -2);
    bpq.append(&c, 5);

    CHECK_FALSE(bpq.is_empty());
    CHECK(bpq.get_max() == 5);

    auto* item = bpq.popleft();
    CHECK(item->data()[1] == 3);
    CHECK(bpq.get_max() == 3);

    item = bpq.popleft();
    CHECK(item->data()[1] == 1);
    CHECK(bpq.get_max() == -2);

    item = bpq.popleft();
    CHECK(item->data()[1] == 2);
    CHECK(bpq.is_empty());
}

TEST_CASE("BPQueueTest - Appendlft") {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    Dllink<std::array<int, 2>> b({0, 2});

    bpq.appendleft(&a, 3);
    bpq.appendleft(&b, 3);

    auto* item1 = bpq.popleft();
    CHECK(item1->data()[1] == 2); // b was appended left, so it comes first

    auto* item2 = bpq.popleft();
    CHECK(item2->data()[1] == 1); // a comes second
}

TEST_CASE("BPQueueTest - Clear") {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> node({0, 1});
    bpq.append(&node, 3);
    bpq.clear();
    CHECK(bpq.is_empty());
}

TEST_CASE("BPQueueTest - KeyManipulation") {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});

    bpq.append(&a, 0);
    CHECK(bpq.get_max() == 0);

    bpq.increase_key(&a, 2);
    CHECK(bpq.get_max() == 2);

    bpq.decrease_key(&a, 3);
    CHECK(bpq.get_max() == -1);

    bpq.modify_key(&a, 4);
    CHECK(bpq.get_max() == 3);

    bpq.modify_key(&a, -5);
    CHECK(bpq.get_max() == -2);
}

TEST_CASE("BPQueueTest - Detach") {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    Dllink<std::array<int, 2>> b({0, 2});

    bpq.append(&a, 3);
    bpq.append(&b, 5);

    bpq.detach(&a);
    CHECK(bpq.get_max() == 5);

    auto* item = bpq.popleft();
    CHECK(item->data()[1] == 2);
    CHECK(bpq.is_empty());
}

TEST_CASE("BPQueueTest - LockedItem") {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    bpq.append(&a, 0);
    a.lock();
    bpq.modify_key(&a, 3); // Should have no effect
    CHECK(bpq.get_max() == 0);
}
