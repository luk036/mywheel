#ifndef ARRAY_LIKE_HPP
#define ARRAY_LIKE_HPP

#include <vector>
#include <iterator>
#include <stdexcept>
#include <utility>

namespace cpp_ai {

/**
 * @brief A list-like object that repeats a given value for a specified number of times.
 *
 * Similar to Python's RepeatArray class.
 */
template<typename T>
class RepeatArray {
private:
    T value_;
    size_t size_;

public:
    /**
     * @brief Construct a new RepeatArray object.
     *
     * @param value The value to repeat.
     * @param size The number of times to repeat the value.
     */
    RepeatArray(T value, size_t size) : value_(value), size_(size) {}

    /**
     * @brief Get the value at any index (always returns the same value).
     *
     * @param key The index (ignored).
     * @return T The repeated value.
     */
    T operator[](size_t key) const {
        (void)key; // Ignore the key
        return value_;
    }

    /**
     * @brief Get the value at any index (always returns the same value).
     *
     * @param key The index (ignored).
     * @return T The repeated value.
     */
    T get(size_t key) const {
        (void)key; // Ignore the key
        return value_;
    }

    /**
     * @brief Get the size of the array.
     *
     * @return size_t The size.
     */
    size_t size() const { return size_; }

    /**
     * @brief Get the value stored in the array.
     *
     * @return T The value.
     */
    T value() const { return value_; }

    // Iterator support
    class iterator {
    private:
        T value_;
        size_t count_;
        size_t current_;

    public:
        using iterator_category = std::input_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T;

        iterator(T value, size_t count, size_t current = 0)
            : value_(value), count_(count), current_(current) {}

        T operator*() const { return value_; }

        iterator& operator++() {
            ++current_;
            return *this;
        }

        iterator operator++(int) {
            iterator tmp = *this;
            ++(*this);
            return tmp;
        }

        bool operator==(const iterator& other) const {
            return current_ == other.current_;
        }

        bool operator!=(const iterator& other) const {
            return !(*this == other);
        }
    };

    iterator begin() const { return iterator(value_, size_, 0); }
    iterator end() const { return iterator(value_, size_, size_); }
};

/**
 * @brief A list with arbitrary starting index.
 *
 * Similar to Python's ShiftArray class.
 */
template<typename T>
class ShiftArray {
private:
    std::vector<T> data_;
    size_t start_;

public:
    /**
     * @brief Construct a new ShiftArray object.
     *
     * @param data Initial data.
     * @param start Starting index (default: 0).
     */
    ShiftArray(std::vector<T> data = {}, size_t start = 0)
        : data_(std::move(data)), start_(start) {}

    /**
     * @brief Set the starting index.
     *
     * @param start New starting index.
     */
    void set_start(size_t start) { start_ = start; }

    /**
     * @brief Get the starting index.
     *
     * @return size_t The starting index.
     */
    size_t start() const { return start_; }

    /**
     * @brief Get the element at the specified index.
     *
     * @param key The index.
     * @return T& Reference to the element.
     * @throws std::out_of_range if index is out of range.
     */
    T& operator[](size_t key) {
        if (key < start_ || key >= start_ + data_.size()) {
            throw std::out_of_range("Index out of range");
        }
        return data_[key - start_];
    }

    /**
     * @brief Get the element at the specified index (const version).
     *
     * @param key The index.
     * @return const T& Const reference to the element.
     * @throws std::out_of_range if index is out of range.
     */
    const T& operator[](size_t key) const {
        if (key < start_ || key >= start_ + data_.size()) {
            throw std::out_of_range("Index out of range");
        }
        return data_[key - start_];
    }

    /**
     * @brief Get the size of the array.
     *
     * @return size_t The size.
     */
    size_t size() const { return data_.size(); }

    /**
     * @brief Get iterator to the beginning.
     *
     * @return auto Iterator.
     */
    auto begin() { return data_.begin(); }
    auto begin() const { return data_.begin(); }

    /**
     * @brief Get iterator to the end.
     *
     * @return auto Iterator.
     */
    auto end() { return data_.end(); }
    auto end() const { return data_.end(); }

    /**
     * @brief Get iterator over index-value pairs.
     *
     * @return auto Iterator over pairs.
     */
    auto items() const {
        std::vector<std::pair<size_t, T>> result;
        result.reserve(data_.size());
        for (size_t i = 0; i < data_.size(); ++i) {
            result.emplace_back(start_ + i, data_[i]);
        }
        return result;
    }
};

} // namespace cpp_ai

#endif // ARRAY_LIKE_HPP
