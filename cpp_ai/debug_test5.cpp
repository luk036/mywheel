#include <iostream>
#include <array>
#include "dllist.hpp"

using namespace cpp_ai;

int main() {
    // Test Dllist append
    Dllist<std::array<int, 2>> list({0, 999});
    
    Dllink<std::array<int, 2>> node({100, 200});
    
    std::cout << "Before append:" << std::endl;
    std::cout << "node.is_locked() = " << std::boolalpha << node.is_locked() << std::endl;
    std::cout << "list.is_empty() = " << list.is_empty() << std::endl;
    
    std::cout << "\nhead().next() == &head()? " << (list.head().next() == &list.head()) << std::endl;
    std::cout << "head().prev() == &head()? " << (list.head().prev() == &list.head()) << std::endl;
    
    list.append(&node);
    
    std::cout << "\nAfter append:" << std::endl;
    std::cout << "node.is_locked() = " << node.is_locked() << std::endl;
    std::cout << "list.is_empty() = " << list.is_empty() << std::endl;
    
    std::cout << "\nhead().next() == &node? " << (list.head().next() == &node) << std::endl;
    std::cout << "head().prev() == &node? " << (list.head().prev() == &node) << std::endl;
    std::cout << "node.next() == &head()? " << (node.next() == &list.head()) << std::endl;
    std::cout << "node.prev() == &head()? " << (node.prev() == &list.head()) << std::endl;
    
    std::cout << "\nIterating list:" << std::endl;
    auto it = list.cbegin();
    auto end = list.cend();
    std::cout << "it == end? " << (it == end) << std::endl;
    
    if (it != end) {
        std::cout << "Dereferencing iterator..." << std::endl;
        auto& link = *it;
        std::cout << "Node: [" << link.data()[0] << ", " << link.data()[1] << "]" << std::endl;
    }
    
    return 0;
}