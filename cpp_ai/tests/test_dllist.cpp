#include <gtest/gtest.h>
#include "dllist.hpp"

using namespace cpp_ai;

TEST(DllinkTest, Constructor) {
    Dllink<int> link(1);
    EXPECT_EQ(link.data(), 1);
    EXPECT_TRUE(link.is_locked());
}

TEST(DllinkTest, LockAndIsLocked) {
    Dllink<int> link(1);
    EXPECT_TRUE(link.is_locked());
    
    // Simulate attaching to a list
    Dllink<int> other(2);
    link.attach(&other);
    EXPECT_FALSE(link.is_locked());
    
    link.lock();
    EXPECT_TRUE(link.is_locked());
}

TEST(DllinkTest, AttachAndDetach) {
    Dllink<std::string> a("a");
    Dllink<std::string> b("b");
    Dllink<std::string> c("c");

    // Attach b after a
    a.attach(&b);
    EXPECT_EQ(a.next(), &b);
    EXPECT_EQ(b.prev(), &a);
    EXPECT_TRUE(b.is_locked()); // b.next points to b

    // Attach c after b
    b.attach(&c);
    EXPECT_EQ(b.next(), &c);
    EXPECT_EQ(c.prev(), &b);
    EXPECT_TRUE(c.is_locked()); // c.next points to c
    EXPECT_EQ(a.prev(), &c); // circular

    // Detach b
    b.detach();
    EXPECT_EQ(a.next(), &c);
    EXPECT_EQ(c.prev(), &a);
}

TEST(DllistTest, Constructor) {
    Dllist<int> dlist(0);
    EXPECT_TRUE(dlist.is_empty());
}

TEST(DllistTest, Clear) {
    Dllist<int> dlist(0);
    Dllink<int> link(1);
    dlist.append(&link);
    dlist.clear();
    EXPECT_TRUE(dlist.is_empty());
}

TEST(DllistTest, AppendAndPop) {
    Dllist<int> dlist(0);
    Dllink<int> link1(1);
    Dllink<int> link2(2);

    dlist.append(&link1);
    EXPECT_FALSE(dlist.is_empty());
    
    dlist.append(&link2);
    
    auto* popped = dlist.pop();
    EXPECT_EQ(popped, &link2);
    
    popped = dlist.pop();
    EXPECT_EQ(popped, &link1);
    EXPECT_TRUE(dlist.is_empty());
}

TEST(DllistTest, AppendlftAndPopleft) {
    Dllist<int> dlist(0);
    Dllink<int> link1(1);
    Dllink<int> link2(2);

    dlist.appendleft(&link1);
    EXPECT_FALSE(dlist.is_empty());
    
    dlist.appendleft(&link2);
    
    auto* popped = dlist.popleft();
    EXPECT_EQ(popped, &link2);
    
    popped = dlist.popleft();
    EXPECT_EQ(popped, &link1);
    EXPECT_TRUE(dlist.is_empty());
}

TEST(DllistTest, Iteration) {
    Dllist<int> dlist(0);
    Dllink<int> link1(1);
    Dllink<int> link2(2);
    Dllink<int> link3(3);

    dlist.append(&link1);
    dlist.append(&link2);
    dlist.append(&link3);

    std::vector<int> items;
    for (auto& link : dlist) {
        items.push_back(link.data());
    }
    EXPECT_EQ(items, std::vector<int>({1, 2, 3}));
}

TEST(DllistTest, EmptyIteration) {
    Dllist<int> dlist(0);
    std::vector<int> items;
    for (auto& link : dlist) {
        items.push_back(link.data());
    }
    EXPECT_TRUE(items.empty());
}