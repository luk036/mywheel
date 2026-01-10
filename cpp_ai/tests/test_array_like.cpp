#define DOCTEST_CONFIG_IMPLEMENT_WITH_MAIN
#include "doctest.h"
#include "array_like.hpp"
#include <vector>

using namespace cpp_ai;

TEST_CASE("RepeatArrayTest - Constructor") {
    RepeatArray<int> ra(10, 5);
    CHECK(ra.value() == 10);
    CHECK(ra.size() == 5);
}

TEST_CASE("RepeatArrayTest - GetItem") {
    RepeatArray<int> ra(10, 5);
    CHECK(ra[0] == 10);
    CHECK(ra[4] == 10);
    CHECK(ra[100] == 10); // Index is ignored
}

TEST_CASE("RepeatArrayTest - Len") {
    RepeatArray<int> ra(10, 5);
    CHECK(ra.size() == 5);
}

TEST_CASE("RepeatArrayTest - Iter") {
    RepeatArray<int> ra(10, 3);
    std::vector<int> result;
    for (auto val : ra) {
        result.push_back(val);
    }
    CHECK(result == std::vector<int>({10, 10, 10}));
}

TEST_CASE("RepeatArrayTest - Get") {
    RepeatArray<int> ra(10, 5);
    CHECK(ra.get(0) == 10);
    CHECK(ra.get(100) == 10); // Index is ignored
}

TEST_CASE("ShiftArrayTest - Constructor") {
    ShiftArray<int> sa({1, 2, 3});
    CHECK(sa.start() == 0);
    std::vector<int> result(sa.begin(), sa.end());
    CHECK(result == std::vector<int>({1, 2, 3}));
}

TEST_CASE("ShiftArrayTest - SetStart") {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    CHECK(sa.start() == 5);
}

TEST_CASE("ShiftArrayTest - GetItem") {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    CHECK(sa[5] == 1);
    CHECK(sa[7] == 3);
    CHECK_THROWS_AS(sa[4], std::out_of_range);
    CHECK_THROWS_AS(sa[8], std::out_of_range);
}

TEST_CASE("ShiftArrayTest - SetItem") {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    sa[6] = 10;
    CHECK(sa[6] == 10);
    std::vector<int> result(sa.begin(), sa.end());
    CHECK(result == std::vector<int>({1, 10, 3}));
    CHECK_THROWS_AS(sa[8] = 5, std::out_of_range);
}

TEST_CASE("ShiftArrayTest - Len") {
    ShiftArray<int> sa({1, 2, 3});
    CHECK(sa.size() == 3);
}

TEST_CASE("ShiftArrayTest - Items") {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    auto items = sa.items();
    std::vector<std::pair<size_t, int>> expected = {{5, 1}, {6, 2}, {7, 3}};
    CHECK(items == expected);
}
