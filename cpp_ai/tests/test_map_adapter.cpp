#include <gtest/gtest.h>
#include "map_adapter.hpp"

using namespace cpp_ai;

TEST(MapAdapterTest, Constructor) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    EXPECT_EQ(&adapter.vector(), &lst);
}

TEST(MapAdapterTest, GetItem) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    EXPECT_EQ(adapter[0], 1);
    EXPECT_EQ(adapter[2], 3);
    EXPECT_THROW(adapter[3], std::out_of_range);
}

TEST(MapAdapterTest, SetItem) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    adapter[1] = 5;
    EXPECT_EQ(adapter[1], 5);
    EXPECT_THROW(adapter[3] = 6, std::out_of_range);
}

TEST(MapAdapterTest, Contains) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    EXPECT_TRUE(adapter.contains(0));
    EXPECT_TRUE(adapter.contains(2));
    EXPECT_FALSE(adapter.contains(3));
    EXPECT_FALSE(adapter.contains(static_cast<size_t>(-1))); // Underflow
}

TEST(MapAdapterTest, Len) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    EXPECT_EQ(adapter.size(), 3);
}

TEST(MapAdapterTest, Values) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    std::vector<int> result;
    for (auto it = adapter.values_begin(); it != adapter.values_end(); ++it) {
        result.push_back(*it);
    }
    EXPECT_EQ(result, std::vector<int>({1, 2, 3}));
}

TEST(MapAdapterTest, Items) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    std::vector<std::pair<size_t, int>> result;
    for (auto it = adapter.items_begin(); it != adapter.items_end(); ++it) {
        result.push_back(*it);
    }
    std::vector<std::pair<size_t, int>> expected = {{0, 1}, {1, 2}, {2, 3}};
    EXPECT_EQ(result, expected);
}

TEST(MapAdapterTest, Keys) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    std::vector<size_t> result;
    for (auto it = adapter.begin(); it != adapter.end(); ++it) {
        result.push_back(*it);
    }
    EXPECT_EQ(result, std::vector<size_t>({0, 1, 2}));
}

TEST(MapAdapterTest, SetMethod) {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    adapter.set(1, 5);
    EXPECT_EQ(adapter[1], 5);
    EXPECT_THROW(adapter.set(3, 6), std::out_of_range);
}