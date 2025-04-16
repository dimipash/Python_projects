# Python Fibonacci Speedup with C++

This project demonstrates how to accelerate a computationally intensive Python function (calculating Fibonacci numbers recursively) by implementing the core logic in C++ and calling it from Python using `pybind11`.

## Goal

The primary goal is to compare the execution time of a pure Python Fibonacci implementation against one that utilizes a C++ backend, showcasing the potential performance gains achievable with C++ for CPU-bound tasks.

## Files

*   `fibonacci.py`: A pure Python implementation of the recursive Fibonacci algorithm. Used as a baseline for performance comparison.
*   `fibonacci.cpp`: A standalone C++ implementation of the recursive Fibonacci algorithm. Includes a `main` function for testing directly in C++.
*   `fibonacci_lib.cpp`: The C++ implementation of the Fibonacci function, specifically prepared with `pybind11` bindings to be exposed as a Python module.
*   `fibonacci_from_cpp.py`: A Python script that imports the C++ module created from `fibonacci_lib.cpp` and calls the C++ Fibonacci function. Used to measure the performance of the C++ version when called from Python.
*   `requirements.txt`: Lists the necessary Python packages (primarily `pybind11`).
*   `.gitignore`: Standard Git ignore file.

## Dependencies

*   Python 3.x
*   A C++ compiler that supports C++11 (e.g., GCC, Clang, MSVC)
*   `pybind11`: Install using pip:
    ```bash
    pip install pybind11
    ```
    *(Note: The `requirements.txt` file in the repository lists this dependency.)*

## Building the C++ Extension

Before running `fibonacci_from_cpp.py`, you need to compile `fibonacci_lib.cpp` into a Python extension module (a `.pyd` file on Windows, `.so` on Linux/macOS).

The exact command depends on your compiler and system setup. Here are examples:

**Using GCC/G++ (like MinGW on Windows):**

```bash
# Replace <python-include-path>, <pybind11-include-path>, <python-lib-path>, and python3x with your actual paths/versions
g++ -O3 -Wall -shared -std=c++11 -fPIC -I<python-include-path> -I<pybind11-include-path> fibonacci_lib.cpp -L<python-lib-path> -lpython3x -o fibonacci_lib.pyd 
```

*   You can often find include paths using:
    *   Python includes: `python -c "import sysconfig; print(sysconfig.get_path('include'))"`
    *   pybind11 includes: `python -m pybind11 --includes` (this might print multiple flags)
*   The output file name (`fibonacci_lib.pyd`) must match the module name defined in `PYBIND11_MODULE` in `fibonacci_lib.cpp`. The extension `.pyd` is specific to Windows.

**Using MSVC (Visual Studio Compiler):**

```bash
# Ensure you are in a Developer Command Prompt for VS
# Replace <python-include-path>, <pybind11-include-path>, <python-lib-path>, and python3x.lib with your actual paths/versions
cl /EHsc /O2 /shared /I<python-include-path> /I<pybind11-include-path> fibonacci_lib.cpp /link /LIBPATH:<python-lib-path> python3x.lib /OUT:fibonacci_lib.pyd
```

*   Place the resulting `fibonacci_lib.pyd` (or `.so`) file in the same directory as the Python scripts.

## Running the Comparison

1.  **Build the C++ extension** as described above.
2.  **Run the pure Python version:**
    ```bash
    python fibonacci.py
    ```
3.  **Run the Python script using the C++ backend:**
    ```bash
    python fibonacci_from_cpp.py
    ```

## Expected Outcome

Observe the execution times printed by both scripts. You should see a significant reduction in execution time when using the C++ implementation (`fibonacci_from_cpp.py`) compared to the pure Python version (`fibonacci.py`), especially for larger values of `n`. This highlights the benefit of using C++ for performance-critical code sections within a Python application.
