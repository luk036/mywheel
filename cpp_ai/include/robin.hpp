#ifndef ROBIN_HPP
#define ROBIN_HPP

#include <vector>
#include <iterator>
#include <stdexcept>
#include <memory>

namespace cpp_ai {

/**
 * @brief Node for a singly-linked list.
 *
 * Similar to Python's SlNode class.
 */
class SlNode {
private:
    SlNode* next_;
    int data_;

public:
    /**
     * @brief Construct a new SlNode object.
     *
     * @param data The data to store in the node.
     */
    explicit SlNode(int data) : next_(this), data_(data) {}

    // Disable copying
    SlNode(const SlNode&) = delete;
    SlNode& operator=(const SlNode&) = delete;

    // Allow moving
    SlNode(SlNode&& other) noexcept : next_(other.next_), data_(other.data_) {
        if (next_ == &other) next_ = this;
        other.next_ = &other;
    }

    SlNode& operator=(SlNode&& other) noexcept {
        if (this != &other) {
            next_ = other.next_;
            data_ = other.data_;

            if (next_ == &other) next_ = this;
            other.next_ = &other;
        }
        return *this;
    }

    /**
     * @brief Get the next node.
     *
     * @return SlNode* Pointer to the next node.
     */
    SlNode* next() { return next_; }
    const SlNode* next() const { return next_; }

    /**
     * @brief Set the next node.
     *
     * @param next Pointer to the next node.
     */
    void set_next(SlNode* next) { next_ = next; }

    /**
     * @brief Get the data stored in the node.
     *
     * @return int The data.
     */
    int data() const { return data_; }
};

/**
 * @brief Iterator for round-robin traversal.
 *
 * Similar to Python's RobinIterator class.
 */
class RobinIterator {
private:
    SlNode* cur_;
    SlNode* stop_;

public:
    using iterator_category = std::input_iterator_tag;
    using value_type = int;
    using difference_type = std::ptrdiff_t;
    using pointer = const int*;
    using reference = int;

    /**
     * @brief Construct a new RobinIterator object.
     *
     * @param node The starting node.
     */
    explicit RobinIterator(SlNode* node) : cur_(node), stop_(node) {}

    /**
     * @brief Get the current value.
     *
     * @return int The current value.
     */
    reference operator*() const { return cur_->data(); }

    /**
     * @brief Move to the next node.
     *
     * @return RobinIterator& Reference to this iterator.
     */
    RobinIterator& operator++() {
        cur_ = cur_->next();
        return *this;
    }

    /**
     * @brief Move to the next node (post-increment).
     *
     * @return RobinIterator Copy of the iterator before incrementing.
     */
    RobinIterator operator++(int) {
        RobinIterator tmp = *this;
        ++(*this);
        return tmp;
    }

    /**
     * @brief Check if iteration is complete.
     *
     * @return true if iteration is complete, false otherwise.
     */
    bool is_done() const { return cur_ == stop_; }

    /**
     * @brief Equality operator.
     *
     * @param other The other iterator to compare with.
     * @return true if equal, false otherwise.
     */
    bool operator==(const RobinIterator& other) const {
        return cur_ == other.cur_ && stop_ == other.stop_;
    }

    /**
     * @brief Inequality operator.
     *
     * @param other The other iterator to compare with.
     * @return true if not equal, false otherwise.
     */
    bool operator!=(const RobinIterator& other) const {
        return !(*this == other);
    }
};

/**
 * @brief Round-robin cycle implementation.
 *
 * Similar to Python's Robin class.
 */
class Robin {
private:
    std::vector<std::unique_ptr<SlNode>> cycle_;

public:
    /**
     * @brief Construct a new Robin object.
     *
     * @param num_parts Number of parts in the cycle.
     */
    explicit Robin(size_t num_parts) {
        if (num_parts == 0) {
            return;
        }

        // Create nodes
        cycle_.reserve(num_parts);
        for (size_t i = 0; i < num_parts; ++i) {
            cycle_.push_back(std::make_unique<SlNode>(static_cast<int>(i)));
        }

        // Link nodes in a circular list
        for (size_t i = 0; i < num_parts; ++i) {
            size_t prev = (i == 0) ? num_parts - 1 : i - 1;
            cycle_[prev]->set_next(cycle_[i].get());
        }
    }

    // Disable copying
    Robin(const Robin&) = delete;
    Robin& operator=(const Robin&) = delete;

    // Allow moving
    Robin(Robin&&) = default;
    Robin& operator=(Robin&&) = default;

    /**
     * @brief Get an iterator starting from the specified part.
     *
     * @param from_part The starting part index.
     * @return RobinIterator Iterator starting from the specified part.
     * @throws std::out_of_range if the cycle is empty.
     */
    RobinIterator exclude(size_t from_part) {
        if (cycle_.empty()) {
            throw std::out_of_range("Cannot exclude from an empty cycle.");
        }
        if (from_part >= cycle_.size()) {
            throw std::out_of_range("Part index out of range.");
        }
        return RobinIterator(cycle_[from_part].get());
    }

    /**
     * @brief Get the number of parts in the cycle.
     *
     * @return size_t Number of parts.
     */
    size_t size() const { return cycle_.size(); }

    /**
     * @brief Check if the cycle is empty.
     *
     * @return true if empty, false otherwise.
     */
    bool empty() const { return cycle_.empty(); }
};

} // namespace cpp_ai

#endif // ROBIN_HPP
