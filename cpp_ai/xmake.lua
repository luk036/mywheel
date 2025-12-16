-- xmake.lua for cpp_ai project
-- Supports building the cpp_ai library and test executables

set_project("cpp_ai")
set_version("0.1.0")

-- Set C++ standard
set_languages("c++17")

-- Configuration options
option("tests")
    set_default(false)
    set_description("Enable building tests (requires GoogleTest)")
    add_defines("ENABLE_TESTS")

option("gtest_local")
    set_default(false)
    set_description("Use local GoogleTest instead of downloading")

-- Main library
target("cpp_ai")
    set_kind("static")
    add_files("src/array_like.cpp")
    add_files("src/dllist.cpp")
    add_files("src/bpqueue.cpp")
    add_files("src/map_adapter.cpp")
    add_files("src/robin.cpp")
    add_includedirs("include", {public = true})
    add_headerfiles("include/(*.hpp)")
    
    -- MSVC runtime library settings
    if is_plat("windows") then
        add_cxflags("/MD", "/MDd", {force = true})
    end

-- Test executable (only built if tests option is enabled)
if has_config("tests") then
    if has_config("gtest_local") then
        -- Assume GoogleTest is available locally
        target("cpp_ai_tests")
            set_kind("binary")
            add_files("tests/test_array_like.cpp")
            add_files("tests/test_dllist.cpp")
            add_files("tests/test_bpqueue.cpp")
            add_files("tests/test_map_adapter.cpp")
            add_files("tests/test_robin.cpp")
            add_includedirs("include")
            add_deps("cpp_ai")
            add_links("gtest", "gtest_main")
    else
        -- Download GoogleTest
        add_requires("gtest")
        target("cpp_ai_tests")
            set_kind("binary")
            add_files("tests/test_array_like.cpp")
            add_files("tests/test_dllist.cpp")
            add_files("tests/test_bpqueue.cpp")
            add_files("tests/test_map_adapter.cpp")
            add_files("tests/test_robin.cpp")
            add_includedirs("include")
            add_deps("cpp_ai")
            add_packages("gtest")
    end
end

-- Debug test executables
local debug_files = {
    "debug_test.cpp",
    "debug_test2.cpp", 
    "debug_test3.cpp",
    "debug_test4.cpp",
    "debug_test5.cpp",
    "debug_test6.cpp"
}

for _, file in ipairs(debug_files) do
    if os.isfile(file) then
        local name = path.basename(file):match("(.+)%..+$")
        target(name)
            set_kind("binary")
            add_files(file)
            add_includedirs("include")
            add_deps("cpp_ai")
    end
end

-- Default build task
task("default")
    on_run(function ()
        -- Build the library by default
        os.exec("xmake build cpp_ai")
    end)

-- Clean task
task("clean-all")
    on_run(function ()
        os.exec("xmake clean")
        os.rm("build")
        os.rm(".xmake")
    end)