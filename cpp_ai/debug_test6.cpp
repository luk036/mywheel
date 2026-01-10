#include <iostream>
#include <vector>
#include <array>
#include "bpqueue.hpp"

using namespace cpp_ai;

int main() {
    BPQueue bpq(-10, 10);

    std::cout << "offset_ = " << -11 << std::endl;
    std::cout << "high_ = " << 21 << std::endl;

    // Create just 2 nodes
    Dllink<std::array<int, 2>> node1({-10, 0});
    Dllink<std::array<int, 2>> node2({-8, 1});

    std::vector<Dllink<std::array<int, 2>>*> nodes = {&node1, &node2};

    std::cout << "\nBefore appendfrom:" << std::endl;
    std::cout << "node1.data() = [" << node1.data()[0] << ", " << node1.data()[1] << "]" << std::endl;
    std::cout << "node2.data() = [" << node2.data()[0] << ", " << node2.data()[1] << "]" << std::endl;

    bpq.appendfrom(nodes);

    std::cout << "\nAfter appendfrom:" << std::endl;
    std::cout << "node1.data() = [" << node1.data()[0] << ", " << node1.data()[1] << "]" << std::endl;
    std::cout << "node2.data() = [" << node2.data()[0] << ", " << node2.data()[1] << "]" << std::endl;
    std::cout << "max_ = " << bpq.get_max() << std::endl;

    std::cout << "\nTrying to iterate (max 5 iterations):" << std::endl;
    int count = 0;
    for (auto it = bpq.begin(); it != bpq.end(); ++it) {
        std::cout << "Item " << count << ": [" << (*it)->data()[0] << ", " << (*it)->data()[1] << "]" << std::endl;
        ++count;
        if (count >= 5) {
            std::cout << "Breaking after 5 iterations" << std::endl;
            break;
        }
    }
    std::cout << "Total iterations: " << count << std::endl;

    return 0;
}
