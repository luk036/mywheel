add_rules("mode.debug", "mode.release")

set_languages("c++17")

target("mywheel")
    set_kind("static")
    add_headerfiles("include/(mywheel/**.hpp)")
    add_files("src/**.cpp")
    add_includedirs("include", {public = true})

    -- C++17 features
    add_cxxflags("-std=c++17", "-Wall", "-Wextra", "-pedantic")

    if is_mode("debug") then
        add_defines("DEBUG")
        add_cxxflags("-g", "-O0")
    else
        add_cxxflags("-O3")
    end

target("test_mywheel")
    set_kind("binary")
    add_deps("mywheel")
    add_files("tests/**.cpp")
    add_includedirs("include")

    -- Download doctest if not present
    before_build(function (target)
        local doctest_path = path.join(target:scriptdir(), "tests", "doctest.h")
        if not os.isfile(doctest_path) then
            print("Downloading doctest...")
            os.execv("curl", {"-L", "https://raw.githubusercontent.com/doctest/doctest/v2.4.11/doctest/doctest.h", "-o", doctest_path})
        end
    end)

-- Package configuration
package("mywheel")
    set_description("MyWheel C++ Library")
    set_license("MIT")

    add_urls("https://github.com/luk036/mywheel.git")
    add_versions("1.0.0", "dcda260be4010b1509c1dcb9d5f3edcddba9cc51")

    on_install(function (package)
        import("package.tools.cmake").install(package)
    end)
