#include <gtest/gtest.h>
#include "array_like.hpp"

using namespace cpp_ai;

TEST(RepeatArrayTest, Constructor) {
    RepeatArray<int> ra(10, 5);
    EXPECT_EQ(ra.value(), 10);
    EXPECT_EQ(ra.size(), 5);
}

TEST(RepeatArrayTest, GetItem) {
    RepeatArray<int> ra(10, 5);
    EXPECT_EQ(ra[0], 10);
    EXPECT_EQ(ra[4], 10);
    EXPECT_EQ(ra[100], 10); // Index is ignored
}

TEST(RepeatArrayTest, Len) {
    RepeatArray<int> ra(10, 5);
    EXPECT_EQ(ra.size(), 5);
}

TEST(RepeatArrayTest, Iter) {
    RepeatArray<int> ra(10, 3);
    std::vector<int> result;
    for (auto val : ra) {
        result.push_back(val);
    }
    EXPECT_EQ(result, std::vector<int>({10, 10, 10}));
}

TEST(RepeatArrayTest, Get) {
    RepeatArray<int> ra(10, 5);
    EXPECT_EQ(ra.get(0), 10);
    EXPECT_EQ(ra.get(100), 10); // Index is ignored
}

TEST(ShiftArrayTest, Constructor) {
    ShiftArray<int> sa({1, 2, 3});
    EXPECT_EQ(sa.start(), 0);
    std::vector<int> result(sa.begin(), sa.end());
    EXPECT_EQ(result, std::vector<int>({1, 2, 3}));
}

TEST(ShiftArrayTest, SetStart) {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    EXPECT_EQ(sa.start(), 5);
}

TEST(ShiftArrayTest, GetItem) {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    EXPECT_EQ(sa[5], 1);
    EXPECT_EQ(sa[7], 3);
    EXPECT_THROW(sa[4], std::out_of_range);
    EXPECT_THROW(sa[8], std::out_of_range);
}

TEST(ShiftArrayTest, SetItem) {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    sa[6] = 10;
    EXPECT_EQ(sa[6], 10);
    std::vector<int> result(sa.begin(), sa.end());
    EXPECT_EQ(result, std::vector<int>({1, 10, 3}));
    EXPECT_THROW(sa[8] = 5, std::out_of_range);
}

TEST(ShiftArrayTest, Len) {
    ShiftArray<int> sa({1, 2, 3});
    EXPECT_EQ(sa.size(), 3);
}

TEST(ShiftArrayTest, Items) {
    ShiftArray<int> sa({1, 2, 3});
    sa.set_start(5);
    auto items = sa.items();
    std::vector<std::pair<size_t, int>> expected = {{5, 1}, {6, 2}, {7, 3}};
    EXPECT_EQ(items, expected);
}