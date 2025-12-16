cmake_minimum_required(VERSION 3.14)
project(cpp_ai VERSION 0.1.0 LANGUAGES CXX)

set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
set(CMAKE_CXX_EXTENSIONS OFF)

# Set runtime library to match Visual Studio defaults (MD/MDd)
if(MSVC)
    set(CMAKE_MSVC_RUNTIME_LIBRARY "MultiThreaded$<$<CONFIG:Debug>:Debug>DLL")
endif()

# Enable testing
enable_testing()

# Download and setup GoogleTest
include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/refs/tags/v1.14.0.tar.gz
)

# Set GoogleTest to use the same runtime library
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Main library
add_library(cpp_ai
    src/array_like.cpp
    src/dllist.cpp
    src/bpqueue.cpp
    src/map_adapter.cpp
    src/robin.cpp
)

target_include_directories(cpp_ai PUBLIC include)

# Tests
add_executable(cpp_ai_tests
    tests/test_array_like.cpp
    tests/test_dllist.cpp
    tests/test_bpqueue.cpp
    tests/test_map_adapter.cpp
    tests/test_robin.cpp
)

target_include_directories(cpp_ai_tests PRIVATE include)
target_link_libraries(cpp_ai_tests cpp_ai gtest gtest_main)

add_test(NAME cpp_ai_tests COMMAND cpp_ai_tests)