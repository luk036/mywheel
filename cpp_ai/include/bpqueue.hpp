#ifndef BPQUEUE_HPP
#define BPQUEUE_HPP

#include "dllist.hpp"
#include <vector>
#include <cassert>
#include <iterator>
#include <algorithm>
#include <array>

namespace cpp_ai {

/**
 * @brief Bounded Priority Queue with integer keys in [a..b].
 * 
 * Implemented by array (bucket) of doubly-linked lists.
 * Efficient if key is bounded by a small integer value.
 * 
 * Similar to Python's BPQueue class.
 */
class BPQueue {
private:
    using Item = Dllink<std::array<int, 2>>;
    
    int max_;
    int offset_;
    int high_;
    std::vector<Dllist<std::array<int, 2>>> bucket_;
    Item sentinel_;

    void update_max_key() {
        while (max_ > 0 && bucket_[max_].is_empty()) {
            --max_;
        }
    }

public:
    /**
     * @brief Construct a new BPQueue object.
     * 
     * @param a Lower bound of key range (inclusive).
     * @param b Upper bound of key range (inclusive).
     */
    BPQueue(int a, int b) : max_(0), offset_(a - 1), high_(b - offset_), sentinel_({0, 8965}) {
        assert(a <= b);
        bucket_.reserve(high_ + 1);
        for (int i = 0; i <= high_; ++i) {
            bucket_.emplace_back(std::array<int, 2>{i, 4848});
        }
        bucket_[0].appendleft(&sentinel_); // sentinel
    }

    // Disable copying
    BPQueue(const BPQueue&) = delete;
    BPQueue& operator=(const BPQueue&) = delete;

    // Allow moving
    BPQueue(BPQueue&&) = default;
    BPQueue& operator=(BPQueue&&) = default;

    /**
     * @brief Check if the queue is empty.
     * 
     * @return true if empty, false otherwise.
     */
    bool is_empty() const { return max_ == 0; }

    /**
     * @brief Get the maximum key in the queue.
     * 
     * @return int The maximum key.
     */
    int get_max() const { return max_ + offset_; }

    /**
     * @brief Clear the queue.
     */
    void clear() {
        while (max_ > 0) {
            bucket_[max_].clear();
            --max_;
        }
    }

    /**
     * @brief Set the key of an item.
     * 
     * @param it The item.
     * @param gain The new key value.
     */
    void set_key(Item* it, int gain) {
        it->data()[0] = gain - offset_;
    }

    /**
     * @brief Append an item using its internal key.
     * 
     * @param it The item to append.
     */
    void appendleft_direct(Item* it) {
        assert(it->data()[0] > offset_);
        appendleft(it, it->data()[0]);
    }

    /**
     * @brief Append an item with an external key to the front of its bucket.
     * 
     * @param it The item to append.
     * @param k The external key.
     */
    void appendleft(Item* it, int k) {
        assert(k > offset_);
        it->data()[0] = k - offset_;
        int key = it->data()[0];
        if (max_ < key) {
            max_ = key;
        }
        bucket_[key].appendleft(it);
    }

    /**
     * @brief Append an item with an external key to the end of its bucket.
     * 
     * @param it The item to append.
     * @param k The external key.
     */
    void append(Item* it, int k) {
        assert(k > offset_);
        it->data()[0] = k - offset_;
        int key = it->data()[0];
        if (max_ < key) {
            max_ = key;
        }
        bucket_[key].append(it);
    }

    /**
     * @brief Remove and return the item with the highest key.
     * 
     * @return Item* Pointer to the removed item.
     */
    Item* popleft() {
        Item* res = bucket_[max_].popleft();
        update_max_key();
        return res;
    }

    /**
     * @brief Decrease the key of an item.
     * 
     * @param it The item.
     * @param delta The amount to decrease.
     */
    void decrease_key(Item* it, int delta) {
        it->detach();
        it->data()[0] -= delta;
        assert(it->data()[0] > 0);
        assert(it->data()[0] <= high_);
        bucket_[it->data()[0]].append(it); // FIFO
        if (max_ < it->data()[0]) {
            max_ = it->data()[0];
            return;
        }
        update_max_key();
    }

    /**
     * @brief Increase the key of an item.
     * 
     * @param it The item.
     * @param delta The amount to increase.
     */
    void increase_key(Item* it, int delta) {
        it->detach();
        it->data()[0] += delta;
        assert(it->data()[0] > 0);
        assert(it->data()[0] <= high_);
        bucket_[it->data()[0]].appendleft(it); // LIFO
        if (max_ < it->data()[0]) {
            max_ = it->data()[0];
        }
        update_max_key();
    }

    /**
     * @brief Modify the key of an item (increase or decrease).
     * 
     * @param it The item.
     * @param delta The amount to modify (positive for increase, negative for decrease).
     */
    void modify_key(Item* it, int delta) {
        if (it->is_locked()) {
            return;
        }
        if (delta > 0) {
            increase_key(it, delta);
        } else if (delta < 0) {
            decrease_key(it, -delta);
        }
    }

    /**
     * @brief Detach an item from the queue.
     * 
     * @param it The item to detach.
     */
    void detach(Item* it) {
        it->detach();
        update_max_key();
    }

    // Iterator support
    class iterator {
    private:
        const BPQueue* bpq_;
        int curkey_;
        typename Dllist<std::array<int, 2>>::const_iterator curitem_;
        typename Dllist<std::array<int, 2>>::const_iterator end_;

        void advance() {
            // Move to next item, next bucket if needed
            while (curkey_ > 0) {
                if (curitem_ != end_) {
                    ++curitem_;
                }
                if (curitem_ == end_) {
                    // Current bucket exhausted, move to next lower bucket
                    --curkey_;
                    if (curkey_ > 0) {
                        curitem_ = bpq_->bucket_[curkey_].cbegin();
                        end_ = bpq_->bucket_[curkey_].cend();
                    }
                } else {
                    // Found next item
                    break;
                }
            }
            // If curkey_ <= 0, we're done
            if (curkey_ <= 0) {
                curitem_ = typename Dllist<std::array<int, 2>>::const_iterator();
                end_ = typename Dllist<std::array<int, 2>>::const_iterator();
            }
        }

    public:
        using iterator_category = std::input_iterator_tag;
        using value_type = Item*;
        using difference_type = std::ptrdiff_t;
        using pointer = Item**;
        using reference = Item*&;

        // Constructor for end iterator
        iterator() : bpq_(nullptr), curkey_(0), curitem_(), end_() {}

        // Constructor for begin iterator
        explicit iterator(const BPQueue* bpq) 
            : bpq_(bpq), curkey_(bpq->max_) {
            if (curkey_ > 0) {
                curitem_ = bpq->bucket_[curkey_].cbegin();
                end_ = bpq->bucket_[curkey_].cend();
                // If first bucket is empty, advance
                if (curitem_ == end_) {
                    advance();
                }
            }
            // If curkey_ <= 0, we're already an end iterator
        }

        value_type operator*() const { 
            // Need to cast away const since we're returning a non-const pointer
            return const_cast<Item*>(&(*curitem_));
        }
        
        iterator& operator++() {
            if (curkey_ > 0) {
                advance();
            }
            return *this;
        }
        
        iterator operator++(int) {
            iterator tmp = *this;
            ++(*this);
            return tmp;
        }
        
        bool operator==(const iterator& other) const {
            return curkey_ == other.curkey_ && curitem_ == other.curitem_;
        }
        
        bool operator!=(const iterator& other) const {
            return !(*this == other);
        }
    };

    iterator begin() const { return iterator(this); }
    iterator end() const { return iterator(); }
};

} // namespace cpp_ai

#endif // BPQUEUE_HPP