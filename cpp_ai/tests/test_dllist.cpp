#include "doctest.h"
#include "dllist.hpp"
#include <vector>

using namespace cpp_ai;

TEST_CASE("DllinkTest - Constructor") {
    Dllink<int> link(1);
    CHECK(link.data() == 1);
    CHECK(link.is_locked());
}

TEST_CASE("DllinkTest - LockAndIsLocked") {
    Dllink<int> link(1);
    CHECK(link.is_locked());
    
    // Simulate attaching to a list
    Dllink<int> other(2);
    link.attach(&other);
    CHECK_FALSE(link.is_locked());
    
    link.lock();
    CHECK(link.is_locked());
}

TEST_CASE("DllinkTest - AttachAndDetach") {
    Dllink<std::string> a(std::string("a"));
    Dllink<std::string> b(std::string("b"));
    Dllink<std::string> c(std::string("c"));

    // Attach b after a
    a.attach(&b);
    CHECK(a.next() == &b);
    CHECK(b.prev() == &a);
    CHECK_FALSE(b.is_locked()); // b is now part of circular list with a

    // Attach c after b
    b.attach(&c);
    CHECK(b.next() == &c);
    CHECK(c.prev() == &b);
    CHECK_FALSE(c.is_locked()); // c is now part of circular list
    CHECK(a.prev() == &c); // circular - c is before a
    CHECK(c.next() == &a); // circular - a is after c

    // Detach b
    b.detach();
    CHECK(a.next() == &c);
    CHECK(c.prev() == &a);
    CHECK(b.is_locked()); // b is now locked after detach
}

TEST_CASE("DllistTest - Constructor") {
    Dllist<int> dlist(0);
    CHECK(dlist.is_empty());
}

TEST_CASE("DllistTest - Clear") {
    Dllist<int> dlist(0);
    Dllink<int> link(1);
    dlist.append(&link);
    dlist.clear();
    CHECK(dlist.is_empty());
}

TEST_CASE("DllistTest - AppendAndPop") {
    Dllist<int> dlist(0);
    Dllink<int> link1(1);
    Dllink<int> link2(2);

    dlist.append(&link1);
    CHECK_FALSE(dlist.is_empty());
    
    dlist.append(&link2);
    
    auto* popped = dlist.pop();
    CHECK(popped == &link2);
    
    popped = dlist.pop();
    CHECK(popped == &link1);
    CHECK(dlist.is_empty());
}

TEST_CASE("DllistTest - AppendlftAndPopleft") {
    Dllist<int> dlist(0);
    Dllink<int> link1(1);
    Dllink<int> link2(2);

    dlist.appendleft(&link1);
    CHECK_FALSE(dlist.is_empty());
    
    dlist.appendleft(&link2);
    
    auto* popped = dlist.popleft();
    CHECK(popped == &link2);
    
    popped = dlist.popleft();
    CHECK(popped == &link1);
    CHECK(dlist.is_empty());
}

TEST_CASE("DllistTest - Iteration") {
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
    CHECK(items == std::vector<int>({1, 2, 3}));
}

TEST_CASE("DllistTest - EmptyIteration") {
    Dllist<int> dlist(0);
    std::vector<int> items;
    for (auto& link : dlist) {
        items.push_back(link.data());
    }
    CHECK(items.empty());
}