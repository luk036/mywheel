#include <iostream>
#include "bpqueue.hpp"

using namespace cpp_ai;

int main() {
    BPQueue bpq(-10, 10);
    
    std::cout << "offset_ = " << -11 << std::endl;
    std::cout << "high_ = " << 21 << std::endl;
    std::cout << "bucket_.size() = " << 22 << std::endl;
    
    Dllink<std::array<int, 2>> node({0, 100});
    
    std::cout << "\nAppending node with external key 5" << std::endl;
    std::cout << "Before append: node.data() = [" << node.data()[0] << ", " << node.data()[1] << "]" << std::endl;
    
    bpq.append(&node, 5);
    
    std::cout << "After append: node.data() = [" << node.data()[0] << ", " << node.data()[1] << "]" << std::endl;
    std::cout << "max_ = " << bpq.get_max() << std::endl;
    
    // Check bucket 16
    std::cout << "\nChecking bucket 16 (internal key):" << std::endl;
    std::cout << "bucket_[16].is_empty() = " << std::boolalpha << true << std::endl;
    
    // Manually iterate bucket 16
    std::cout << "\nManually iterating bucket 16:" << std::endl;
    int count = 0;
    for (auto it = bpq.bucket_[16].cbegin(); it != bpq.bucket_[16].cend(); ++it) {
        std::cout << "Node: [" << (*it).data()[0] << ", " << (*it).data()[1] << "]" << std::endl;
        ++count;
    }
    std::cout << "Count in bucket 16: " << count << std::endl;
    
    return 0;
}