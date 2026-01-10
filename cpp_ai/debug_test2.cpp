#include <iostream>
#include "bpqueue.hpp"

using namespace cpp_ai;

int main() {
    // Simple test: add one node and iterate
    BPQueue bpq(-10, 10);

    Dllink<std::array<int, 2>> node({0, 100});

    std::cout << "Appending node with key 5" << std::endl;
    bpq.append(&node, 5);

    std::cout << "max_ = " << bpq.get_max() << std::endl;
    std::cout << "offset_ = " << -11 << std::endl;
    std::cout << "Internal key = " << node.data()[0] << std::endl;

    std::cout << "\nIterating:" << std::endl;
    int count = 0;
    for (auto it = bpq.begin(); it != bpq.end(); ++it) {
        std::cout << "Item " << count << ": [" << (*it)->data()[0] << ", " << (*it)->data()[1] << "]" << std::endl;
        ++count;
        if (count > 5) {
            std::cout << "Breaking to avoid infinite loop" << std::endl;
            break;
        }
    }
    std::cout << "Count: " << count << std::endl;

    return 0;
}
