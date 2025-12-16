# XMake Build System for cpp_ai

This directory contains xmake configuration for building the cpp_ai project alongside the existing CMake build system.

## Prerequisites

1. Install xmake: https://xmake.io/#/guide/installation
2. For Windows, you can use:
   ```powershell
   powershell -Command "iwr https://xmake.io/psget.ps1 -UseBasicParsing | iex"
   ```

## Building with xmake

### Basic build (library only)
```bash
xmake
# or
xmake build cpp_ai
```

### Build with tests (requires GoogleTest)
```bash
# Option 1: Download GoogleTest automatically
xmake config --tests=y
xmake build cpp_ai_tests

# Option 2: Use locally installed GoogleTest
xmake config --tests=y --gtest_local=y
xmake build cpp_ai_tests
```

### Build debug test executables
```bash
xmake build debug_test
xmake build debug_test2
# ... etc for debug_test3 through debug_test6
```

### List all targets
```bash
xmake show -l targets
```

### Clean build
```bash
xmake clean
```

## Configuration Options

- `--tests=y/n`: Enable/disable test building (default: n)
- `--gtest_local=y/n`: Use local GoogleTest instead of downloading (default: n)
- `--mode=debug/release`: Build mode (default: debug)

## Examples

1. **Build everything (library + all debug tests):**
   ```bash
   xmake
   xmake build debug_test debug_test2 debug_test3 debug_test4 debug_test5 debug_test6
   ```

2. **Build and run tests:**
   ```bash
   xmake config --tests=y
   xmake build cpp_ai_tests
   ./build/windows/x64/debug/cpp_ai_tests.exe
   ```

3. **Clean everything:**
   ```bash
   xmake clean
   ```

## Project Structure

- `xmake.lua`: Main build configuration
- `src/`: Library source files
- `include/`: Library header files
- `tests/`: Test files (require GoogleTest)
- `debug_test*.cpp`: Debug/example programs

## Compared to CMake

xmake provides:
- Simpler configuration syntax (Lua-based)
- Built-in package management
- Cross-platform support
- Faster configuration times

The xmake build produces outputs in `build/` directory, separate from CMake's `build/` directory.