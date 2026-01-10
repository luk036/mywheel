#include "doctest.h"
#include "robin.hpp"
#include <vector>

using namespace cpp_ai;

TEST_CASE("SlNodeTest - Constructor") {
    SlNode node(5);
    CHECK(node.data() == 5);
    CHECK(node.next() == &node);
}

TEST_CASE("RobinIteratorTest - Constructor") {
    SlNode node(1);
    RobinIterator iterator(&node);
    CHECK(*iterator == 1);
}

TEST_CASE("RobinIteratorTest - Next") {
    Robin r(3);
    auto iterator = r.exclude(0);

    CHECK(*iterator == 1);
    ++iterator;
    CHECK(*iterator == 2);
    ++iterator;
    CHECK(iterator.is_done());
}

TEST_CASE("RobinTest - Constructor") {
    Robin r(5);
    CHECK(r.size() == 5);
    CHECK_FALSE(r.empty());
}

TEST_CASE("RobinTest - Exclude") {
    Robin r(5);
    auto iterator = r.exclude(3);
    CHECK(*iterator == 4);
}

TEST_CASE("RobinTest - Iteration") {
    Robin r(5);

    // Test starting from 0
    auto iterator = r.exclude(0);
    std::vector<int> result;
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    CHECK(result == std::vector<int>({1, 2, 3, 4}));

    // Test starting from 3
    iterator = r.exclude(3);
    result.clear();
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    CHECK(result == std::vector<int>({4, 0, 1, 2}));

    // Test starting from the last element
    iterator = r.exclude(4);
    result.clear();
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    CHECK(result == std::vector<int>({0, 1, 2, 3}));
}

TEST_CASE("RobinTest - OnePart") {
    Robin r(1);
    auto iterator = r.exclude(0);
    CHECK(iterator.is_done());

    std::vector<int> result;
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    CHECK(result.empty());
}

TEST_CASE("RobinTest - ZeroParts") {
    Robin r(0);
    CHECK(r.empty());
    CHECK_THROWS_AS(r.exclude(0), std::out_of_range);
}

TEST_CASE("RobinTest - OutOfRange") {
    Robin r(5);
    CHECK_THROWS_AS(r.exclude(5), std::out_of_range);
    CHECK_THROWS_AS(r.exclude(10), std::out_of_range);
}
