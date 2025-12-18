#include "doctest.h"
#include "map_adapter.hpp"
#include <vector>

using namespace cpp_ai;

TEST_CASE("MapAdapterTest - Constructor") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    CHECK(&adapter.vector() == &lst);
}

TEST_CASE("MapAdapterTest - GetItem") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    CHECK(adapter[0] == 1);
    CHECK(adapter[2] == 3);
    CHECK_THROWS_AS(adapter[3], std::out_of_range);
}

TEST_CASE("MapAdapterTest - SetItem") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    adapter[1] = 5;
    CHECK(adapter[1] == 5);
    CHECK_THROWS_AS(adapter[3] = 6, std::out_of_range);
}

TEST_CASE("MapAdapterTest - Contains") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    CHECK(adapter.contains(0));
    CHECK(adapter.contains(2));
    CHECK_FALSE(adapter.contains(3));
    CHECK_FALSE(adapter.contains(static_cast<size_t>(-1))); // Underflow
}

TEST_CASE("MapAdapterTest - Len") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    CHECK(adapter.size() == 3);
}

TEST_CASE("MapAdapterTest - Values") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    std::vector<int> result;
    for (auto it = adapter.values_begin(); it != adapter.values_end(); ++it) {
        result.push_back(*it);
    }
    CHECK(result == std::vector<int>({1, 2, 3}));
}

TEST_CASE("MapAdapterTest - Items") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    std::vector<std::pair<size_t, int>> result;
    for (auto it = adapter.items_begin(); it != adapter.items_end(); ++it) {
        result.push_back(*it);
    }
    std::vector<std::pair<size_t, int>> expected = {{0, 1}, {1, 2}, {2, 3}};
    CHECK(result == expected);
}

TEST_CASE("MapAdapterTest - Keys") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    std::vector<size_t> result;
    for (auto it = adapter.begin(); it != adapter.end(); ++it) {
        result.push_back(*it);
    }
    CHECK(result == std::vector<size_t>({0, 1, 2}));
}

TEST_CASE("MapAdapterTest - SetMethod") {
    std::vector<int> lst = {1, 2, 3};
    MapAdapter<int> adapter(lst);
    adapter.set(1, 5);
    CHECK(adapter[1] == 5);
    CHECK_THROWS_AS(adapter.set(3, 6), std::out_of_range);
}