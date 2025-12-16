#include <gtest/gtest.h>
#include "robin.hpp"

using namespace cpp_ai;

TEST(SlNodeTest, Constructor) {
    SlNode node(5);
    EXPECT_EQ(node.data(), 5);
    EXPECT_EQ(node.next(), &node);
}

TEST(RobinIteratorTest, Constructor) {
    SlNode node(1);
    RobinIterator iterator(&node);
    EXPECT_EQ(*iterator, 1);
}

TEST(RobinIteratorTest, Next) {
    Robin r(3);
    auto iterator = r.exclude(0);
    
    EXPECT_EQ(*iterator, 1);
    ++iterator;
    EXPECT_EQ(*iterator, 2);
    ++iterator;
    EXPECT_TRUE(iterator.is_done());
}

TEST(RobinTest, Constructor) {
    Robin r(5);
    EXPECT_EQ(r.size(), 5);
    EXPECT_FALSE(r.empty());
}

TEST(RobinTest, Exclude) {
    Robin r(5);
    auto iterator = r.exclude(3);
    EXPECT_EQ(*iterator, 4);
}

TEST(RobinTest, Iteration) {
    Robin r(5);
    
    // Test starting from 0
    auto iterator = r.exclude(0);
    std::vector<int> result;
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    EXPECT_EQ(result, std::vector<int>({1, 2, 3, 4}));

    // Test starting from 3
    iterator = r.exclude(3);
    result.clear();
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    EXPECT_EQ(result, std::vector<int>({4, 0, 1, 2}));

    // Test starting from the last element
    iterator = r.exclude(4);
    result.clear();
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    EXPECT_EQ(result, std::vector<int>({0, 1, 2, 3}));
}

TEST(RobinTest, OnePart) {
    Robin r(1);
    auto iterator = r.exclude(0);
    EXPECT_TRUE(iterator.is_done());
    
    std::vector<int> result;
    while (!iterator.is_done()) {
        result.push_back(*iterator);
        ++iterator;
    }
    EXPECT_TRUE(result.empty());
}

TEST(RobinTest, ZeroParts) {
    Robin r(0);
    EXPECT_TRUE(r.empty());
    EXPECT_THROW(r.exclude(0), std::out_of_range);
}

TEST(RobinTest, OutOfRange) {
    Robin r(5);
    EXPECT_THROW(r.exclude(5), std::out_of_range);
    EXPECT_THROW(r.exclude(10), std::out_of_range);
}