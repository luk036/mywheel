#include <iostream>
#include "bpqueue.hpp"

using namespace cpp_ai;

int main() {
    BPQueue bpq(-10, 10);
    
    std::vector<Dllink<std::array<int, 2>>> nodes;
    for (int i = 0; i < 10; ++i) {
        nodes.emplace_back(std::array<int, 2>{2 * i - 10, i});
    }
    
    std::vector<Dllink<std::array<int, 2>>*> node_ptrs;
    for (auto& node : nodes) {
        node_ptrs.push_back(&node);
    }
    
    std::cout << "Before appendfrom:" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << "Node " << i << ": [" << nodes[i].data()[0] << ", " << nodes[i].data()[1] << "]" << std::endl;
    }
    
    bpq.appendfrom(node_ptrs);
    
    std::cout << "\nAfter appendfrom:" << std::endl;
    for (int i = 0; i < 10; ++i) {
        std::cout << "Node " << i << ": [" << nodes[i].data()[0] << ", " << nodes[i].data()[1] << "]" << std::endl;
    }
    
    std::cout << "\nmax_ = " << bpq.get_max() << std::endl;
    
    std::cout << "\nIterating:" << std::endl;
    int count = 0;
    for (auto it = bpq.begin(); it != bpq.end(); ++it) {
        std::cout << "Item " << count << ": [" << (*it)->data()[0] << ", " << (*it)->data()[1] << "]" << std::endl;
        ++count;
        if (count > 20) {
            std::cout << "Breaking to avoid infinite loop" << std::endl;
            break;
        }
    }
    std::cout << "Count: " << count << std::endl;
    
    return 0;
}