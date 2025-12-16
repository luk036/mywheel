#include <gtest/gtest.h>
#include "bpqueue.hpp"

using namespace cpp_ai;

TEST(BPQueueTest, Constructor) {
    BPQueue bpq(-3, 3);
    EXPECT_TRUE(bpq.is_empty());
    EXPECT_EQ(bpq.get_max(), -4); // a - 1
}

TEST(BPQueueTest, AppendAndPop) {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    Dllink<std::array<int, 2>> b({0, 2});
    Dllink<std::array<int, 2>> c({0, 3});

    bpq.append(&a, 3);
    bpq.append(&b, -2);
    bpq.append(&c, 5);

    EXPECT_FALSE(bpq.is_empty());
    EXPECT_EQ(bpq.get_max(), 5);

    auto* item = bpq.popleft();
    EXPECT_EQ(item->data()[1], 3);
    EXPECT_EQ(bpq.get_max(), 3);

    item = bpq.popleft();
    EXPECT_EQ(item->data()[1], 1);
    EXPECT_EQ(bpq.get_max(), -2);

    item = bpq.popleft();
    EXPECT_EQ(item->data()[1], 2);
    EXPECT_TRUE(bpq.is_empty());
}

TEST(BPQueueTest, Appendlft) {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    Dllink<std::array<int, 2>> b({0, 2});

    bpq.appendleft(&a, 3);
    bpq.appendleft(&b, 3);

    auto* item1 = bpq.popleft();
    EXPECT_EQ(item1->data()[1], 2); // b was appended left, so it comes first
    
    auto* item2 = bpq.popleft();
    EXPECT_EQ(item2->data()[1], 1); // a comes second
}

TEST(BPQueueTest, Appendfrom) {
    BPQueue bpq(-10, 10);
    std::vector<Dllink<std::array<int, 2>>> nodes;
    for (int i = 0; i < 10; ++i) {
        nodes.emplace_back(std::array<int, 2>{2 * i - 10, i});
    }
    
    std::vector<Dllink<std::array<int, 2>>*> node_ptrs;
    for (auto& node : nodes) {
        node_ptrs.push_back(&node);
    }
    
    bpq.appendfrom(node_ptrs);
    EXPECT_EQ(bpq.get_max(), 8);
    
    int count = 0;
    for (auto it = bpq.begin(); it != bpq.end(); ++it) {
        ++count;
    }
    EXPECT_EQ(count, 10);
}

TEST(BPQueueTest, Clear) {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> node({0, 1});
    bpq.append(&node, 3);
    bpq.clear();
    EXPECT_TRUE(bpq.is_empty());
}

TEST(BPQueueTest, KeyManipulation) {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});

    bpq.append(&a, 0);
    EXPECT_EQ(bpq.get_max(), 0);

    bpq.increase_key(&a, 2);
    EXPECT_EQ(bpq.get_max(), 2);

    bpq.decrease_key(&a, 3);
    EXPECT_EQ(bpq.get_max(), -1);

    bpq.modify_key(&a, 4);
    EXPECT_EQ(bpq.get_max(), 3);

    bpq.modify_key(&a, -5);
    EXPECT_EQ(bpq.get_max(), -2);
}

TEST(BPQueueTest, Detach) {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    Dllink<std::array<int, 2>> b({0, 2});

    bpq.append(&a, 3);
    bpq.append(&b, 5);

    bpq.detach(&a);
    EXPECT_EQ(bpq.get_max(), 5);
    
    auto* item = bpq.popleft();
    EXPECT_EQ(item->data()[1], 2);
    EXPECT_TRUE(bpq.is_empty());
}

TEST(BPQueueTest, LockedItem) {
    BPQueue bpq(-5, 5);
    Dllink<std::array<int, 2>> a({0, 1});
    bpq.append(&a, 0);
    a.lock();
    bpq.modify_key(&a, 3); // Should have no effect
    EXPECT_EQ(bpq.get_max(), 0);
}