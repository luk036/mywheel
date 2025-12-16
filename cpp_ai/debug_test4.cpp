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
    
    list.append(&node);
    
    std::cout << "\nAfter append:" << std::endl;
    std::cout << "node.is_locked() = " << node.is_locked() << std::endl;
    std::cout << "list.is_empty() = " << list.is_empty() << std::endl;
    
    std::cout << "\nIterating list:" << std::endl;
    int count = 0;
    for (auto it = list.cbegin(); it != list.cend(); ++it) {
        std::cout << "Node: [" << (*it).data()[0] << ", " << (*it).data()[1] << "]" << std::endl;
        ++count;
    }
    std::cout << "Count: " << count << std::endl;
    
    // Check node connections
    std::cout << "\nNode connections:" << std::endl;
    std::cout << "node.next() == &list.head()? " << (node.next() == &list.head()) << std::endl;
    std::cout << "node.prev() == &list.head()? " << (node.prev() == &list.head()) << std::endl;
    
    return 0;
}