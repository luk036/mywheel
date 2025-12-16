-- xmake.lua for cpp_ai project
-- Build system for C++17 implementation of Python mywheel data structures
-- Includes: array_like, dllist, bpqueue, map_adapter, robin

set_project("cpp_ai")
set_version("0.1.0")

-- Set C++ standard to C++17
set_languages("c++17")

-- Add build modes
add_rules("mode.debug", "mode.release")

-- Compiler flags
if is_mode("debug") then
    add_cxxflags("-g", "-O0")
else
    add_cxxflags("-O2")
end

-- Common warnings
add_cxxflags("-Wall", "-Wextra", "-Wpedantic")

-- Download and use googletest for testing
-- main = true: link with gtest_main which provides main()
-- gmock = false: don't link with Google Mock
add_requires("gtest", {configs = {main = true, gmock = false}})

-- Main library target: static library containing all data structures
target("cpp_ai")
    set_kind("static")
    -- Public header files
    add_headerfiles("include/(**.hpp)")
    -- Source files
    add_files("src/array_like.cpp")
    add_files("src/dllist.cpp")
    add_files("src/bpqueue.cpp")
    add_files("src/map_adapter.cpp")
    add_files("src/robin.cpp")
    -- Include directories (public for library users)
    add_includedirs("include", {public = true})

-- Test executable target
target("cpp_ai_tests")
    set_kind("binary")
    -- Test source files
    add_files("tests/test_array_like.cpp")
    add_files("tests/test_dllist.cpp")
    add_files("tests/test_bpqueue.cpp")
    add_files("tests/test_map_adapter.cpp")
    add_files("tests/test_robin.cpp")
    -- Include directories
    add_includedirs("include")
    -- Dependencies
    add_deps("cpp_ai")  -- Link with our library
    add_packages("gtest")  -- Link with gtest

-- Default targets to build
set_default("cpp_ai", "cpp_ai_tests")

-- Usage examples:
--   xmake                 # Build library and tests
--   xmake build cpp_ai    # Build only library
--   xmake build cpp_ai_tests  # Build only tests
--   xmake run cpp_ai_tests    # Run tests
--   xmake clean           # Clean build
--   xmake clean -a        # Clean all (including downloaded packages)