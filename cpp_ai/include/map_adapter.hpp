#ifndef MAP_ADAPTER_HPP
#define MAP_ADAPTER_HPP

#include <vector>
#include <iterator>
#include <stdexcept>
#include <utility>
#include <type_traits>

namespace cpp_ai {

/**
 * @brief A map-like adapter for a vector.
 * 
 * Adapts a vector to behave like a map with integer keys.
 * Similar to Python's MapAdapter class.
 */
template<typename T>
class MapAdapter {
private:
    std::vector<T>* lst_;

public:
    /**
     * @brief Construct a new MapAdapter object.
     * 
     * @param lst Reference to the vector to adapt.
     */
    explicit MapAdapter(std::vector<T>& lst) : lst_(&lst) {}

    // Disable copying
    MapAdapter(const MapAdapter&) = delete;
    MapAdapter& operator=(const MapAdapter&) = delete;

    // Allow moving
    MapAdapter(MapAdapter&& other) noexcept : lst_(other.lst_) {
        other.lst_ = nullptr;
    }

    MapAdapter& operator=(MapAdapter&& other) noexcept {
        if (this != &other) {
            lst_ = other.lst_;
            other.lst_ = nullptr;
        }
        return *this;
    }

    /**
     * @brief Get the element at the specified index.
     * 
     * @param key The index.
     * @return T& Reference to the element.
     * @throws std::out_of_range if index is out of range.
     */
    T& operator[](size_t key) {
        if (key >= lst_->size()) {
            throw std::out_of_range("Index out of range");
        }
        return (*lst_)[key];
    }

    /**
     * @brief Get the element at the specified index (const version).
     * 
     * @param key The index.
     * @return const T& Const reference to the element.
     * @throws std::out_of_range if index is out of range.
     */
    const T& operator[](size_t key) const {
        if (key >= lst_->size()) {
            throw std::out_of_range("Index out of range");
        }
        return (*lst_)[key];
    }

    /**
     * @brief Set the element at the specified index.
     * 
     * @param key The index.
     * @param value The new value.
     * @throws std::out_of_range if index is out of range.
     */
    void set(size_t key, const T& value) {
        if (key >= lst_->size()) {
            throw std::out_of_range("Index out of range");
        }
        (*lst_)[key] = value;
    }

    /**
     * @brief Check if an index is within bounds.
     * 
     * @param key The index to check.
     * @return true if index is within bounds, false otherwise.
     */
    bool contains(size_t key) const {
        return key < lst_->size();
    }

    /**
     * @brief Get the size of the adapted vector.
     * 
     * @return size_t The size.
     */
    size_t size() const { return lst_->size(); }

    // Iterator over keys
    class key_iterator {
    private:
        size_t current_;
        size_t size_;

    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = size_t;
        using difference_type = std::ptrdiff_t;
        using pointer = const size_t*;
        using reference = size_t;

        key_iterator(size_t size, size_t current = 0) 
            : current_(current), size_(size) {}

        reference operator*() const { return current_; }
        
        key_iterator& operator++() {
            ++current_;
            return *this;
        }
        
        key_iterator operator++(int) {
            key_iterator tmp = *this;
            ++(*this);
            return tmp;
        }
        
        bool operator==(const key_iterator& other) const {
            return current_ == other.current_;
        }
        
        bool operator!=(const key_iterator& other) const {
            return !(*this == other);
        }
    };

    key_iterator begin() const { return key_iterator(lst_->size(), 0); }
    key_iterator end() const { return key_iterator(lst_->size(), lst_->size()); }

    // Iterator over values
    class value_iterator {
    private:
        typename std::vector<T>::iterator current_;

    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = T;
        using difference_type = std::ptrdiff_t;
        using pointer = T*;
        using reference = T&;

        value_iterator(typename std::vector<T>::iterator begin,
                      typename std::vector<T>::iterator end,
                      typename std::vector<T>::iterator current)
            : current_(current) {}
        
        value_iterator(typename std::vector<T>::iterator begin,
                      typename std::vector<T>::iterator end)
            : current_(begin) {}

        reference operator*() const { return *current_; }
        pointer operator->() const { return &(*current_); }
        
        value_iterator& operator++() {
            ++current_;
            return *this;
        }
        
        value_iterator operator++(int) {
            value_iterator tmp = *this;
            ++(*this);
            return tmp;
        }
        
        bool operator==(const value_iterator& other) const {
            return current_ == other.current_;
        }
        
        bool operator!=(const value_iterator& other) const {
            return !(*this == other);
        }
    };

    value_iterator values_begin() { return value_iterator(lst_->begin(), lst_->end()); }
    value_iterator values_end() { return value_iterator(lst_->begin(), lst_->end(), lst_->end()); }

    // Iterator over key-value pairs
    class item_iterator {
    private:
        size_t index_;
        typename std::vector<T>::iterator current_;

    public:
        using iterator_category = std::forward_iterator_tag;
        using value_type = std::pair<size_t, T>;
        using difference_type = std::ptrdiff_t;
        using pointer = std::pair<size_t, T>*;
        using reference = std::pair<size_t, T>;

        item_iterator(size_t index,
                     typename std::vector<T>::iterator begin,
                     typename std::vector<T>::iterator end,
                     typename std::vector<T>::iterator current)
            : index_(index), current_(current) {}
        
        item_iterator(size_t index,
                     typename std::vector<T>::iterator begin,
                     typename std::vector<T>::iterator end)
            : index_(index), current_(begin) {}

        reference operator*() const { return {index_, *current_}; }
        
        item_iterator& operator++() {
            ++index_;
            ++current_;
            return *this;
        }
        
        item_iterator operator++(int) {
            item_iterator tmp = *this;
            ++(*this);
            return tmp;
        }
        
        bool operator==(const item_iterator& other) const {
            return current_ == other.current_;
        }
        
        bool operator!=(const item_iterator& other) const {
            return !(*this == other);
        }
    };

    item_iterator items_begin() { return item_iterator(0, lst_->begin(), lst_->end()); }
    item_iterator items_end() { return item_iterator(lst_->size(), lst_->begin(), lst_->end(), lst_->end()); }

    /**
     * @brief Get the adapted vector.
     * 
     * @return std::vector<T>& Reference to the vector.
     */
    std::vector<T>& vector() { return *lst_; }
    const std::vector<T>& vector() const { return *lst_; }
};

} // namespace cpp_ai

#endif // MAP_ADAPTER_HPP