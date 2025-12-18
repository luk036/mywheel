#ifndef DLLIST_HPP
#define DLLIST_HPP

#include <cstddef>
#include <iterator>
#include <utility>
#include <string>

namespace cpp_ai {

/**
 * @brief A node in a doubly linked list.
 * 
 * Similar to Python's Dllink class.
 */
template<typename T>
class Dllink {
private:
    Dllink* next_;
    Dllink* prev_;
    T data_;

public:
    /**
     * @brief Construct a new Dllink object.
     * 
     * @param data The data to store in the node.
     */
    explicit Dllink(T data) : next_(this), prev_(this), data_(std::move(data)) {}

    // Disable copying
    Dllink(const Dllink&) = delete;
    Dllink& operator=(const Dllink&) = delete;

    // Allow moving
    Dllink(Dllink&& other) noexcept 
        : next_(other.next_), prev_(other.prev_), data_(std::move(other.data_)) {
        if (next_ == &other) next_ = this;
        if (prev_ == &other) prev_ = this;
        other.next_ = &other;
        other.prev_ = &other;
    }

    Dllink& operator=(Dllink&& other) noexcept {
        if (this != &other) {
            next_ = other.next_;
            prev_ = other.prev_;
            data_ = std::move(other.data_);
            
            if (next_ == &other) next_ = this;
            if (prev_ == &other) prev_ = this;
            other.next_ = &other;
            other.prev_ = &other;
        }
        return *this;
    }

    /**
     * @brief Check if the node is locked (points to itself).
     * 
     * @return true if locked, false otherwise.
     */
    bool is_locked() const { return next_ == this; }

    /**
     * @brief Lock the node (make it point to itself).
     */
    void lock() {
        next_ = this;
        prev_ = this;
    }

    /**
     * @brief Attach another node after this node.
     * 
     * @param node The node to attach.
     */
    void attach(Dllink* node) {
        node->next_ = next_;
        node->prev_ = this;
        next_->prev_ = node;
        next_ = node;
    }

    /**
     * @brief Detach this node from the list.
     */
    void detach() {
        prev_->next_ = next_;
        next_->prev_ = prev_;
        lock();
    }

    /**
     * @brief Get the next node.
     * 
     * @return Dllink* Pointer to the next node.
     */
    Dllink* next() { return next_; }
    const Dllink* next() const { return next_; }

    /**
     * @brief Get the previous node.
     * 
     * @return Dllink* Pointer to the previous node.
     */
    Dllink* prev() { return prev_; }
    const Dllink* prev() const { return prev_; }

    /**
     * @brief Get the data stored in the node.
     * 
     * @return T& Reference to the data.
     */
    T& data() { return data_; }
    const T& data() const { return data_; }
};

/**
 * @brief A doubly linked list with a sentinel head node.
 * 
 * Similar to Python's Dllist class.
 */
template<typename T>
class Dllist {
private:
    Dllink<T> head_;

public:
    /**
     * @brief Construct a new Dllist object.
     * 
     * @param data Data for the sentinel head node.
     */
    explicit Dllist(T data = T{}) : head_(std::move(data)) {}

    // Disable copying
    Dllist(const Dllist&) = delete;
    Dllist& operator=(const Dllist&) = delete;

    // Allow moving
    Dllist(Dllist&& other) noexcept : head_(std::move(other.head_)) {}
    Dllist& operator=(Dllist&& other) noexcept {
        if (this != &other) {
            head_ = std::move(other.head_);
        }
        return *this;
    }

    /**
     * @brief Check if the list is empty.
     * 
     * @return true if empty, false otherwise.
     */
    bool is_empty() const { return head_.next() == &head_; }

    /**
     * @brief Clear the list.
     */
    void clear() { head_.lock(); }

    /**
     * @brief Append a node to the front of the list.
     * 
     * @param node The node to append.
     */
    void appendleft(Dllink<T>* node) { head_.attach(node); }

    /**
     * @brief Append a node to the end of the list.
     * 
     * @param node The node to append.
     */
    void append(Dllink<T>* node) { head_.prev()->attach(node); }

    /**
     * @brief Remove and return the first node in the list.
     * 
     * @return Dllink<T>* Pointer to the removed node.
     */
    Dllink<T>* popleft() {
        Dllink<T>* res = head_.next();
        res->detach();
        return res;
    }

    /**
     * @brief Remove and return the last node in the list.
     * 
     * @return Dllink<T>* Pointer to the removed node.
     */
    Dllink<T>* pop() {
        Dllink<T>* res = head_.prev();
        res->detach();
        return res;
    }

    // Iterator support
    class iterator {
    private:
        Dllink<T>* current_;
        Dllink<T>* head_;

    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = Dllink<T>;
        using difference_type = std::ptrdiff_t;
        using pointer = Dllink<T>*;
        using reference = Dllink<T>&;

        iterator() : current_(nullptr), head_(nullptr) {}
        
        // Constructor for begin iterator
        explicit iterator(Dllink<T>* head) 
            : current_(head->next() == head ? nullptr : head->next()), head_(head) {}
        
        // Constructor for end iterator
        iterator(Dllink<T>* head, std::nullptr_t) 
            : current_(nullptr), head_(head) {}

        reference operator*() const { return *current_; }
        pointer operator->() const { return current_; }
        
        iterator& operator++() {
            current_ = current_->next();
            if (current_ == head_) {
                current_ = nullptr;
            }
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

    iterator begin() { return iterator(&head_); }
    iterator end() { return iterator(&head_, nullptr); }
    
    // Const iterator support
    class const_iterator {
    private:
        const Dllink<T>* current_;
        const Dllink<T>* head_;

    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = const Dllink<T>;
        using difference_type = std::ptrdiff_t;
        using pointer = const Dllink<T>*;
        using reference = const Dllink<T>&;

        const_iterator() : current_(nullptr), head_(nullptr) {}
        
        // Constructor for begin iterator
        explicit const_iterator(const Dllink<T>* head) 
            : current_(head->next() == head ? nullptr : head->next()), head_(head) {}
        
        // Constructor for end iterator
        const_iterator(const Dllink<T>* head, std::nullptr_t) 
            : current_(nullptr), head_(head) {}

        reference operator*() const { return *current_; }
        pointer operator->() const { return current_; }
        
        const_iterator& operator++() {
            current_ = current_->next();
            if (current_ == head_) {
                current_ = nullptr;
            }
            return *this;
        }
        
        const_iterator operator++(int) {
            const_iterator tmp = *this;
            ++(*this);
            return tmp;
        }
        
        bool operator==(const const_iterator& other) const {
            return current_ == other.current_;
        }
        
        bool operator!=(const const_iterator& other) const {
            return !(*this == other);
        }
    };

    const_iterator begin() const { return const_iterator(&head_); }
    const_iterator end() const { return const_iterator(&head_, nullptr); }
    const_iterator cbegin() const { return const_iterator(&head_); }
    const_iterator cend() const { return const_iterator(&head_, nullptr); }

    const Dllink<T>& head() const { return head_; }
};

} // namespace cpp_ai

#endif // DLLIST_HPP