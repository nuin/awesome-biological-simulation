# AMICI

> Compile an SBML ODE model to C++ with CVODES and simulate it, optionally with forward parameter sensitivities.

Licence: BSD-3-Clause · [Source code](https://github.com/AMICI-dev/AMICI)

## What it simulates

AMICI simulates systems of ordinary differential equations (ODEs) from biochemical models, and it computes how the result changes with each parameter. You give it a model in SBML (or PySB). It derives all equations symbolically, writes C++ code, compiles that code into a Python module, and runs it with the SUNDIALS solvers CVODES (ODEs) and IDAS (differential-algebraic equations).

The point of the compile step is speed and sensitivities. Besides the trajectory, AMICI can return forward sensitivities (how each species at each time responds to each parameter), steady-state sensitivities and adjoint sensitivities for likelihood-based outputs. These feed gradient-based parameter estimation for large models.

Key assumptions: the model is deterministic and continuous, so there are no discrete molecule counts and no noise. Species are in well-mixed compartments. The former MATLAB interface was removed in AMICI 1.0, so Python is the interface.

## When to use it

- You fit parameters to data and need fast, exact gradients of the fit.
- Your ODE model has hundreds of states, so an interpreted simulator is too slow.
- You want SBML models imported and compiled without writing the right-hand side by hand.

Alternatives:

- [Tellurium](tellurium.md) loads and runs a model in one line and needs no compiler. Pick it for exploration and small models.
- [COPASI](copasi.md) has a task interface with parameter scans and estimation, and no code.
- [GillesPy2](gillespy2.md) fits when copy numbers are low and noise matters.

## Install

AMICI 1.1.0 is the current release on PyPI (BSD-3-Clause). It ships only as a source archive, so pip compiles it. The install guide asks for Python 3.12 or newer and a C++20 compiler (for example g++ 10.1 or newer, clang 13 or newer).

```bash
# Ubuntu 22.04 / 24.04
sudo apt install python3-dev g++ cmake
pip3 install amici==1.1.0
python3 -c "import amici"
```

The project also documents optional HDF5 (`libhdf5-serial-dev`) and Boost packages, and a conda route that first runs `conda install -c conda-forge compilers cmake`. Its repository holds a container recipe under `container/`. The recipe on this page uses a Python 3.12 image with g++, make and cmake added, and installs `amici==1.1.0` from PyPI.

## A first run

Adapted from the project's [Getting Started notebook](https://github.com/AMICI-dev/AMICI/blob/main/doc/examples/getting_started/GettingStarted.ipynb). It uses the model file `model_steadystate_scaled.xml` from the same folder: three species (`x1`, `x2`, `x3`), six reactions and parameters `p1` to `p5` and `k0`.

```python
import amici
import numpy as np
from amici.sim.sundials import SensitivityMethod, SensitivityOrder, run_simulation

sbml_importer = amici.SbmlImporter("model_steadystate_scaled.xml")
sbml_importer.sbml2amici("model_steadystate", "model_dir")      # generates and compiles C++

model_module = amici.import_model_module("model_steadystate", "model_dir")
model = model_module.get_model()
model.set_timepoints(np.linspace(0, 10, 101))
solver = model.create_solver()

# optional: forward sensitivities for all parameters
model.require_sensitivities_for_all_parameters()
solver.set_sensitivity_method(SensitivityMethod.forward)
solver.set_sensitivity_order(SensitivityOrder.first)

rdata = run_simulation(model, solver)
print(rdata.x.shape)        # (timepoints, species)
```

The notebook says compilation takes a couple of seconds for this model.

## Run the tested example

This recipe builds AMICI in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 9.1 s.

1. Download [amici-recipe.tar.gz](https://biosimhub.pages.dev/guides/amici/amici-recipe.tar.gz) (Dockerfile, run_amici.py, example model.xml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf amici-recipe.tar.gz
   cd amici
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/amici:1.1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/amici:1.1.0 python /opt/run_amici.py /work/in/model.xml \
    --tend 10 --points 101 --sensitivities forward > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `model_dir/.gitignore` | 2 B |
| `model_dir/CMakeLists.txt` | 4.1 KB |
| `model_dir/Jy.cpp` | 2.3 KB |
| `model_dir/Jy.h` | 180 B |
| `model_dir/MANIFEST.in` | 67 B |
| `model_dir/biosim_model.cpp` | 3.1 KB |
| `model_dir/biosim_model.h` | 21.0 KB |
| `model_dir/biosim_model/__init__.py` | 1.4 KB |
| `model_dir/biosim_model/__pycache__/__init__.cpython-312.pyc` | 1.7 KB |
| `model_dir/biosim_model/__pycache__/biosim_model.cpython-312.pyc` | 5.4 KB |
| `model_dir/biosim_model/_biosim_model.cpython-312-aarch64-linux-gnu.so` | 1.5 MB |
| `model_dir/biosim_model/biosim_model.py` | 3.9 KB |
| `model_dir/biosim_model/lib/libbiosim_model.a` | 166.6 KB |
| `model_dir/build_model_ext/.ninja_deps` | 43.9 KB |
| `model_dir/build_model_ext/.ninja_log` | 2.3 KB |
| `model_dir/build_model_ext/CMakeCache.txt` | 23.4 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeCCompiler.cmake` | 3.0 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeCXXCompiler.cmake` | 6.3 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeDetermineCompilerABI_C.bin` | 69.0 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeDetermineCompilerABI_CXX.bin` | 69.0 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeSystem.cmake` | 396 B |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CompilerIdC/CMakeCCompilerId.c` | 28.3 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CompilerIdC/a.out` | 69.1 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CompilerIdCXX/CMakeCXXCompilerId.cpp` | 29.0 KB |
| `model_dir/build_model_ext/CMakeFiles/4.4.4/CompilerIdCXX/a.out` | 69.1 KB |
| `model_dir/build_model_ext/CMakeFiles/CMakeConfigureLog.yaml` | 210.5 KB |
| `model_dir/build_model_ext/CMakeFiles/FindOpenMP/ompver_CXX.bin` | 68.8 KB |
| `model_dir/build_model_ext/CMakeFiles/InstallScripts.json` | 178 B |
| `model_dir/build_model_ext/CMakeFiles/TargetDirectories.txt` | 1017 B |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/Jy.cpp.o` | 2.8 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/biosim_model.cpp.o` | 5.8 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/create_splines.cpp.o` | 1.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/dJydsigma.cpp.o` | 2.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/dJydy.cpp.o` | 3.9 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/dwdp.cpp.o` | 2.7 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/dwdx.cpp.o` | 2.8 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/dxdotdw.cpp.o` | 3.2 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/dydp.cpp.o` | 1.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/dydx.cpp.o` | 1.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/sigmay.cpp.o` | 1.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/w.cpp.o` | 1.4 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/wrapfunctions.cpp.o` | 116.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/x0.cpp.o` | 1.5 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/x_rdata.cpp.o` | 1.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/x_solver.cpp.o` | 1.3 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/xdot.cpp.o` | 1.4 KB |
| `model_dir/build_model_ext/CMakeFiles/biosim_model.dir/y.cpp.o` | 1.4 KB |
| `model_dir/build_model_ext/CMakeFiles/clean_additional.cmake` | 250 B |
| `model_dir/build_model_ext/CMakeFiles/cmake.check_cache` | 85 B |
| `model_dir/build_model_ext/CMakeFiles/rules.ninja` | 3.0 KB |
| `model_dir/build_model_ext/biosim_modelConfig.cmake` | 2.7 KB |
| `model_dir/build_model_ext/build.ninja` | 66.8 KB |
| `model_dir/build_model_ext/cmake_install.cmake` | 2.5 KB |
| `model_dir/build_model_ext/install_manifest.txt` | 183 B |
| `model_dir/build_model_ext/libbiosim_model.a` | 166.6 KB |
| `model_dir/build_model_ext/swig/CMakeFiles/_biosim_model.dir/CMakeFiles/_biosim_model.dir/biosim_modelPYTHON_wrap.cxx.o` | 41.2 KB |
| `model_dir/build_model_ext/swig/CMakeFiles/_biosim_model.dir/biosim_modelPYTHON_wrap.cxx` | 129.0 KB |
| `model_dir/build_model_ext/swig/_biosim_model.cpython-312-aarch64-linux-gnu.so` | 1.5 MB |
| `model_dir/build_model_ext/swig/biosim_model.py` | 3.9 KB |
| `model_dir/build_model_ext/swig/cmake_install.cmake` | 1.8 KB |
| `model_dir/create_splines.cpp` | 373 B |
| `model_dir/dJydsigma.cpp` | 2.1 KB |
| `model_dir/dJydy.cpp` | 3.2 KB |
| `model_dir/dJydy.h` | 380 B |
| `model_dir/dwdp.cpp` | 1.9 KB |
| `model_dir/dwdp.h` | 276 B |
| `model_dir/dwdx.cpp` | 2.0 KB |
| `model_dir/dwdx.h` | 412 B |
| `model_dir/dxdotdw.cpp` | 1.9 KB |
| `model_dir/dxdotdw.h` | 422 B |
| `model_dir/dydp.cpp` | 640 B |
| `model_dir/dydx.cpp` | 561 B |
| `model_dir/main.cpp` | 3.3 KB |
| `model_dir/my.h` | 282 B |
| `model_dir/p.h` | 185 B |
| `model_dir/setup.py` | 3.1 KB |
| `model_dir/sigmay.cpp` | 807 B |
| `model_dir/sigmay.h` | 372 B |
| `model_dir/swig/CMakeLists.txt` | 1.9 KB |
| `model_dir/swig/biosim_model.i` | 3.4 KB |
| `model_dir/w.cpp` | 964 B |
| `model_dir/w.h` | 316 B |
| `model_dir/wrapfunctions.cpp` | 331 B |
| `model_dir/wrapfunctions.h` | 404 B |
| `model_dir/x.h` | 48 B |
| `model_dir/x0.cpp` | 402 B |
| `model_dir/x_rdata.cpp` | 413 B |
| `model_dir/x_rdata.h` | 66 B |
| `model_dir/x_solver.cpp` | 356 B |
| `model_dir/x_solver.h` | 90 B |
| `model_dir/xdot.cpp` | 606 B |
| `model_dir/xdot.h` | 66 B |
| `model_dir/y.cpp` | 562 B |
| `model_dir/y.h` | 262 B |
| `run_log.txt` | 80 B |
| `sensitivities.csv` | 63.6 KB |
| `species.csv` | 3.8 KB |

<details><summary>First lines of <code>model_dir/.gitignore</code></summary>

```
**
```

</details>

<details><summary>First lines of <code>model_dir/CMakeLists.txt</code></summary>

```
# Build AMICI model
cmake_minimum_required(VERSION 3.22)
cmake_policy(VERSION 3.22...3.31)

# We aren't using C++20 modules, so disable scanning for them to avoid
# clang-scan-deps-notfound errors.
# See also https://discourse.cmake.org/t/cmake-3-28-cmake-cxx-compiler-clang-scan-deps-notfound-not-found/9244/3
set(CMAKE_CXX_SCAN_FOR_MODULES OFF)

project(biosim_model)

message(STATUS "CMAKE_CURRENT_SOURCE_DIR: ${CMAKE_CURRENT_SOURCE_DIR}")
```

</details>

<details><summary>First lines of <code>model_dir/Jy.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "p.h"
#include "y.h"
#include "sigmay.h"
#include "my.h"

namespace amici {
namespace model_biosim_model {

```

</details>

<details><summary>First lines of <code>model_dir/Jy.h</code></summary>

```
#define Jy0 Jy[0]
#define Jy1 Jy[1]
#define Jy2 Jy[2]
#define Jy3 Jy[3]
#define Jy4 Jy[4]
#define Jy5 Jy[5]
#define Jy6 Jy[6]
#define Jy7 Jy[7]
#define Jy8 Jy[8]
#define Jy9 Jy[9]
```

</details>

<details><summary>First lines of <code>model_dir/MANIFEST.in</code></summary>

```
include *.cpp *.h
include CMakeLists.txt
recursive-include swig/ *
```

</details>

<details><summary>First lines of <code>model_dir/biosim_model.cpp</code></summary>

```
#include <amici/defines.h>
#include <array>
#include <string_view>

namespace amici::model_biosim_model {

// clang-format off

extern const std::array<std::string_view const, 9> free_parameter_names = {
    "p1", // p[0]
"p2", // p[1]
"p3", // p[2]
```

</details>

<details><summary>First lines of <code>model_dir/biosim_model.h</code></summary>

```
#ifndef _amici_TPL_MODELNAME_h
#define _amici_TPL_MODELNAME_h
#include <cmath>
#include <memory>
#include <gsl/gsl-lite.hpp>

#include "amici/model_ode.h"
#include "amici/splinefunctions.h"
#include "amici/event.h"

namespace amici {

```

</details>

<details><summary>First lines of <code>model_dir/biosim_model/__init__.py</code></summary>

```
"""AMICI-generated module for model biosim_model"""

import sys
import warnings
from pathlib import Path

import amici

# Ensure we are binary-compatible, see #556
if "1.1.0" != amici.__version__:
    raise amici.AmiciVersionError(
        f"Cannot use model `biosim_model` in {Path(__file__).parent}, "
```

</details>

<details><summary>First lines of <code>model_dir/biosim_model/biosim_model.py</code></summary>

```
# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.5.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

import typing

import amici
import amici.sim.sundials
import datetime
import importlib.util
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/.ninja_log</code></summary>

```
# ninja log v7
2	146	1792296619031027970	CMakeFiles/biosim_model.dir/Jy.cpp.o	64f8484d00edfb5d
148	267	1792296619176634276	CMakeFiles/biosim_model.dir/biosim_model.cpp.o	2e0bc359dc4ecc5c
268	604	1792296619296551052	CMakeFiles/biosim_model.dir/create_splines.cpp.o	1fde8e31e20f9e3c
607	741	1792296619635873082	CMakeFiles/biosim_model.dir/dJydsigma.cpp.o	9da388e7219a9b7e
741	1123	1792296619769638502	CMakeFiles/biosim_model.dir/dJydy.cpp.o	acfe9b92773174b6
1124	1471	1792296620152423766	CMakeFiles/biosim_model.dir/dwdp.cpp.o	97a387a09e103498
1472	1824	1792296620500260458	CMakeFiles/biosim_model.dir/dwdx.cpp.o	59cdfc0210f582b6
1824	2173	1792296620852556212	CMakeFiles/biosim_model.dir/dxdotdw.cpp.o	8132e0b02e132dff
2174	2304	1792296621202252122	CMakeFiles/biosim_model.dir/dydp.cpp.o	9d480cb25d3339a6
2304	2431	1792296621332628278	CMakeFiles/biosim_model.dir/dydx.cpp.o	c6d7342c3f46fb01
2431	2562	1792296621459560251	CMakeFiles/biosim_model.dir/sigmay.cpp.o	57d8438bf66877c3
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeCache.txt</code></summary>

```
# This is the CMakeCache file.
# For build in directory: /work/out/model_dir/build_model_ext
# It was generated by CMake: /usr/local/lib/python3.12/site-packages/cmake/data/bin/cmake
# You can edit this file to change values found and used by cmake.
# If you do not want to change any of the values, simply exit the editor.
# If you do want to change a value, simply edit, save, and exit the editor.
# The syntax for the file is as follows:
# KEY:TYPE=VALUE
# KEY is the name of a variable in the cache.
# TYPE is a hint to GUIs for the type of VALUE, DO NOT EDIT TYPE!.
# VALUE is the current value for the KEY.

```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeCCompiler.cmake</code></summary>

```
set(CMAKE_C_COMPILER "/usr/bin/cc")
set(CMAKE_C_COMPILER_ARG1 "")
set(CMAKE_C_COMPILER_ID "GNU")
set(CMAKE_C_COMPILER_VERSION "12.2.0")
set(CMAKE_C_COMPILER_VERSION_INTERNAL "")
set(CMAKE_C_COMPILER_WRAPPER "")
set(CMAKE_C_STANDARD_COMPUTED_DEFAULT "17")
set(CMAKE_C_EXTENSIONS_COMPUTED_DEFAULT "ON")
set(CMAKE_C_STANDARD_LATEST "23")
set(CMAKE_C_COMPILE_FEATURES "c_std_90;c_function_prototypes;c_std_99;c_restrict;c_variadic_macros;c_std_11;c_static_assert;c_std_17;c_std_23")
set(CMAKE_C90_COMPILE_FEATURES "c_std_90;c_function_prototypes")
set(CMAKE_C99_COMPILE_FEATURES "c_std_99;c_restrict;c_variadic_macros")
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeCXXCompiler.cmake</code></summary>

```
set(CMAKE_CXX_COMPILER "/usr/bin/c++")
set(CMAKE_CXX_COMPILER_ARG1 "")
set(CMAKE_CXX_COMPILER_ID "GNU")
set(CMAKE_CXX_COMPILER_VERSION "12.2.0")
set(CMAKE_CXX_COMPILER_VERSION_INTERNAL "")
set(CMAKE_CXX_COMPILER_WRAPPER "")
set(CMAKE_CXX_STANDARD_COMPUTED_DEFAULT "17")
set(CMAKE_CXX_EXTENSIONS_COMPUTED_DEFAULT "ON")
set(CMAKE_CXX_STANDARD_LATEST "23")
set(CMAKE_CXX_COMPILE_FEATURES "cxx_std_98;cxx_template_template_parameters;cxx_std_11;cxx_alias_templates;cxx_alignas;cxx_alignof;cxx_attributes;cxx_auto_type;cxx_constexpr;cxx_decltype;cxx_decltype_
set(CMAKE_CXX98_COMPILE_FEATURES "cxx_std_98;cxx_template_template_parameters")
set(CMAKE_CXX11_COMPILE_FEATURES "cxx_std_11;cxx_alias_templates;cxx_alignas;cxx_alignof;cxx_attributes;cxx_auto_type;cxx_constexpr;cxx_decltype;cxx_decltype_incomplete_return_types;cxx_default_functi
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/4.4.4/CMakeSystem.cmake</code></summary>

```
set(CMAKE_HOST_SYSTEM "Linux-7.0.12-linuxkit")
set(CMAKE_HOST_SYSTEM_NAME "Linux")
set(CMAKE_HOST_SYSTEM_VERSION "7.0.12-linuxkit")
set(CMAKE_HOST_SYSTEM_PROCESSOR "aarch64")



set(CMAKE_SYSTEM "Linux-7.0.12-linuxkit")
set(CMAKE_SYSTEM_NAME "Linux")
set(CMAKE_SYSTEM_VERSION "7.0.12-linuxkit")
set(CMAKE_SYSTEM_PROCESSOR "aarch64")

```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/4.4.4/CompilerIdC/CMakeCCompilerId.c</code></summary>

```
#ifdef __cplusplus
# error "A C++ compiler has been selected for C."
#endif

#if defined(__18CXX)
# define ID_VOID_MAIN
#endif
#if defined(__CLASSIC_C__)
/* cv-qualifiers did not exist in K&R C */
# define const
# define volatile
#endif
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/4.4.4/CompilerIdCXX/CMakeCXXCompilerId.cpp</code></summary>

```
/* This source file must have a .cpp extension so that all C++ compilers
   recognize the extension without flags.  Borland does not know .cxx for
   example.  */
#ifndef __cplusplus
# error "A C compiler has been selected for C++."
#endif

#if !defined(__has_include)
/* If the compiler does not have __has_include, pretend the answer is
   always no.  */
#  define __has_include(x) 0
#endif
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/CMakeConfigureLog.yaml</code></summary>

```

---
events:
  -
    kind: "find-v1"
    backtrace:
      - "/usr/local/lib/python3.12/site-packages/cmake/data/share/cmake-4.4/Modules/CMakeDetermineSystem.cmake:12 (find_program)"
      - "CMakeLists.txt:10 (project)"
    mode: "program"
    variable: "CMAKE_UNAME"
    description: "Path to a program."
    settings:
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/InstallScripts.json</code></summary>

```
{
	"InstallScripts" : 
	[
		"/work/out/model_dir/build_model_ext/cmake_install.cmake",
		"/work/out/model_dir/build_model_ext/swig/cmake_install.cmake"
	],
	"Parallel" : false
}
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/TargetDirectories.txt</code></summary>

```
/work/out/model_dir/build_model_ext/CMakeFiles/biosim_model.dir
/work/out/model_dir/build_model_ext/CMakeFiles/edit_cache.dir
/work/out/model_dir/build_model_ext/CMakeFiles/rebuild_cache.dir
/work/out/model_dir/build_model_ext/CMakeFiles/list_install_components.dir
/work/out/model_dir/build_model_ext/CMakeFiles/install.dir
/work/out/model_dir/build_model_ext/CMakeFiles/install/local.dir
/work/out/model_dir/build_model_ext/CMakeFiles/install/strip.dir
/work/out/model_dir/build_model_ext/swig/CMakeFiles/_biosim_model.dir
/work/out/model_dir/build_model_ext/swig/CMakeFiles/install-python.dir
/work/out/model_dir/build_model_ext/swig/CMakeFiles/edit_cache.dir
/work/out/model_dir/build_model_ext/swig/CMakeFiles/rebuild_cache.dir
/work/out/model_dir/build_model_ext/swig/CMakeFiles/list_install_components.dir
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/clean_additional.cmake</code></summary>

```
# Additional clean files
cmake_minimum_required(VERSION 3.16)

if("${CONFIG}" STREQUAL "" OR "${CONFIG}" STREQUAL "Release")
  file(REMOVE_RECURSE
  "swig/CMakeFiles/_biosim_model.dir/biosim_modelPYTHON_wrap.cxx"
  "swig/biosim_model.py"
  )
endif()
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/cmake.check_cache</code></summary>

```
# This file is generated by cmake for dependency checking of the CMakeCache.txt file
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/CMakeFiles/rules.ninja</code></summary>

```
# CMAKE generated file: DO NOT EDIT!
# Generated by "Ninja" Generator, CMake Version 4.4

# This file contains all the rules used to get the outputs files
# built from the input files.
# It is included in the main 'build.ninja'.

# =============================================================================
# Project: biosim_model
# Configurations: Release
# =============================================================================
# =============================================================================
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/biosim_modelConfig.cmake</code></summary>

```
# Generated by CMake

if("${CMAKE_MAJOR_VERSION}.${CMAKE_MINOR_VERSION}" LESS 2.8)
   message(FATAL_ERROR "CMake >= 2.8.3 required")
endif()
if(CMAKE_VERSION VERSION_LESS "2.8.3")
   message(FATAL_ERROR "CMake >= 2.8.3 required")
endif()
cmake_policy(PUSH)
cmake_policy(VERSION 2.8.3...4.2)
#----------------------------------------------------------------
# Generated CMake target import file.
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/build.ninja</code></summary>

```
# CMAKE generated file: DO NOT EDIT!
# Generated by "Ninja" Generator, CMake Version 4.4

# This file contains all the build statements describing the
# compilation DAG.

# =============================================================================
# Write statements declared in CMakeLists.txt:
# 
# Which is the root file.
# =============================================================================

```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/cmake_install.cmake</code></summary>

```
# Install script for directory: /work/out/model_dir

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/work/out/model_dir/biosim_model")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/install_manifest.txt</code></summary>

```
/work/out/model_dir/biosim_model/biosim_model.py
/work/out/model_dir/biosim_model/_biosim_model.cpython-312-aarch64-linux-gnu.so
/work/out/model_dir/biosim_model/lib/libbiosim_model.a
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/swig/CMakeFiles/_biosim_model.dir/biosim_modelPYTHON_wrap.cxx</code></summary>

```
/* ----------------------------------------------------------------------------
 * This file was automatically generated by SWIG (https://www.swig.org).
 * Version 4.5.1
 *
 * Do not make changes to this file unless you know what you are doing - modify
 * the SWIG interface file instead.
 * ----------------------------------------------------------------------------- */


#define SWIG_VERSION 0x040501
#define SWIGPYTHON
#define SWIG_PYTHON_DIRECTOR_NO_VTABLE
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/swig/biosim_model.py</code></summary>

```
# This file was automatically generated by SWIG (https://www.swig.org).
# Version 4.5.1
#
# Do not make changes to this file unless you know what you are doing - modify
# the SWIG interface file instead.

import typing

import amici
import amici.sim.sundials
import datetime
import importlib.util
```

</details>

<details><summary>First lines of <code>model_dir/build_model_ext/swig/cmake_install.cmake</code></summary>

```
# Install script for directory: /work/out/model_dir/swig

# Set the install prefix
if(NOT DEFINED CMAKE_INSTALL_PREFIX)
  set(CMAKE_INSTALL_PREFIX "/work/out/model_dir/biosim_model")
endif()
string(REGEX REPLACE "/$" "" CMAKE_INSTALL_PREFIX "${CMAKE_INSTALL_PREFIX}")

# Set the install configuration name.
if(NOT DEFINED CMAKE_INSTALL_CONFIG_NAME)
  if(BUILD_TYPE)
    string(REGEX REPLACE "^[^A-Za-z0-9_]+" ""
```

</details>

<details><summary>First lines of <code>model_dir/create_splines.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "amici/splinefunctions.h"
#include <vector>
#include "p.h"

namespace amici {
namespace model_biosim_model {

std::vector<HermiteSpline> create_splines_biosim_model(const realtype *p, const realtype *k){
```

</details>

<details><summary>First lines of <code>model_dir/dJydsigma.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "p.h"
#include "y.h"
#include "sigmay.h"
#include "my.h"

namespace amici {
namespace model_biosim_model {

```

</details>

<details><summary>First lines of <code>model_dir/dJydy.cpp</code></summary>

```
#include "amici/sundials_matrix_wrapper.h"
#include "sundials/sundials_types.h"

#include <array>
#include <algorithm>

namespace amici {
namespace model_biosim_model {

static constexpr std::array<std::array<sunindextype, 11>, 10> dJydy_colptrs_biosim_model_ = {{
    {0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1}, 
    {0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1}, 
```

</details>

<details><summary>First lines of <code>model_dir/dJydy.h</code></summary>

```
#define dJy0_dyx1 dJydy[0]
#define dJy0_dyx2_1 dJydy[1]
#define dJy0_dyx3_2 dJydy[2]
#define dJy0_dyobservable_x1_3 dJydy[3]
#define dJy0_dyobservable_x2_4 dJydy[4]
#define dJy0_dyobservable_x3_5 dJydy[5]
#define dJy0_dyobservable_x1_scaled_6 dJydy[6]
#define dJy0_dyobservable_x2_offsetted_7 dJydy[7]
#define dJy0_dyobservable_x1withsigma_8 dJydy[8]
#define dJy0_dyc1_9 dJydy[9]
```

</details>

<details><summary>First lines of <code>model_dir/dwdp.cpp</code></summary>

```
#include "amici/sundials_matrix_wrapper.h"
#include "sundials/sundials_types.h"

#include <array>
#include <algorithm>

namespace amici {
namespace model_biosim_model {

static constexpr std::array<sunindextype, 10> dwdp_colptrs_biosim_model_ = {
    0, 1, 2, 3, 4, 5, 6, 7, 8, 8
};
```

</details>

<details><summary>First lines of <code>model_dir/dwdp.h</code></summary>

```
#define dflux_r1_dp1 dwdp[0]
#define dflux_r2_dp2 dwdp[1]
#define dflux_r3_dp3 dwdp[2]
#define dflux_r4_dp4 dwdp[3]
#define dflux_r6_dp5 dwdp[4]
#define dflux_r5_dk0 dwdp[5]
#define dobservable_x1_scaled_dscaling_x1 dwdp[6]
#define dobservable_x2_offsetted_doffset_x2 dwdp[7]
```

</details>

<details><summary>First lines of <code>model_dir/dwdx.cpp</code></summary>

```
#include "amici/sundials_matrix_wrapper.h"
#include "sundials/sundials_types.h"

#include <array>
#include <algorithm>

namespace amici {
namespace model_biosim_model {

static constexpr std::array<sunindextype, 4> dwdx_colptrs_biosim_model_ = {
    0, 5, 9, 12
};
```

</details>

<details><summary>First lines of <code>model_dir/dwdx.h</code></summary>

```
#define dobservable_x1_dx1 dwdx[0]
#define dobservable_x1_scaled_dx1 dwdx[1]
#define dobservable_x1withsigma_dx1 dwdx[2]
#define dflux_r1_dx1 dwdx[3]
#define dflux_r2_dx1 dwdx[4]
#define dobservable_x2_dx2 dwdx[5]
#define dobservable_x2_offsetted_dx2 dwdx[6]
#define dflux_r2_dx2 dwdx[7]
#define dflux_r3_dx2 dwdx[8]
#define dobservable_x3_dx3 dwdx[9]
#define dflux_r4_dx3 dwdx[10]
#define dflux_r5_dx3 dwdx[11]
```

</details>

<details><summary>First lines of <code>model_dir/dxdotdw.cpp</code></summary>

```
#include "amici/sundials_matrix_wrapper.h"
#include "sundials/sundials_types.h"

#include <array>
#include <algorithm>

namespace amici {
namespace model_biosim_model {

static constexpr std::array<sunindextype, 13> dxdotdw_colptrs_biosim_model_ = {
    0, 0, 0, 0, 0, 0, 0, 2, 5, 7, 10, 11, 12
};
```

</details>

<details><summary>First lines of <code>model_dir/dxdotdw.h</code></summary>

```
#define ddx1dt_dflux_r1 dxdotdw[0]
#define ddx2dt_dflux_r1 dxdotdw[1]
#define ddx1dt_dflux_r2 dxdotdw[2]
#define ddx2dt_dflux_r2 dxdotdw[3]
#define ddx3dt_dflux_r2 dxdotdw[4]
#define ddx1dt_dflux_r3 dxdotdw[5]
#define ddx2dt_dflux_r3 dxdotdw[6]
#define ddx1dt_dflux_r4 dxdotdw[7]
#define ddx2dt_dflux_r4 dxdotdw[8]
#define ddx3dt_dflux_r4 dxdotdw[9]
#define ddx3dt_dflux_r5 dxdotdw[10]
#define ddx1dt_dflux_r6 dxdotdw[11]
```

</details>

<details><summary>First lines of <code>model_dir/dydp.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "x.h"
#include "p.h"
#include "w.h"

namespace amici {
namespace model_biosim_model {

void dydp_biosim_model(realtype *dydp, const realtype t, const realtype *x, const realtype *p, const realtype *k, const realtype *h, const int ip, const realtype *w, const realtype *tcl, const realtyp
```

</details>

<details><summary>First lines of <code>model_dir/dydx.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "x.h"
#include "p.h"
#include "w.h"

namespace amici {
namespace model_biosim_model {

void dydx_biosim_model(realtype *dydx, const realtype t, const realtype *x, const realtype *p, const realtype *k, const realtype *h, const realtype *w){
```

</details>

<details><summary>First lines of <code>model_dir/main.cpp</code></summary>

```
#include <iostream>

#include "wrapfunctions.h" /* model-provided functions */
#include <amici/amici.h>   /* AMICI base functions */

template <class T>
std::ostream& operator<<(std::ostream& os, std::vector<T> const& v) {
    os << "[";
    for (typename std::vector<T>::const_iterator ii = v.begin(); ii != v.end();
         ++ii) {
        os << " " << *ii;
    }
```

</details>

<details><summary>First lines of <code>model_dir/my.h</code></summary>

```
#define myx1 my[0]
#define myx2 my[1]
#define myx3 my[2]
#define myobservable_x1 my[3]
#define myobservable_x2 my[4]
#define myobservable_x3 my[5]
#define myobservable_x1_scaled my[6]
#define myobservable_x2_offsetted my[7]
#define myobservable_x1withsigma my[8]
#define myc1 my[9]
```

</details>

<details><summary>First lines of <code>model_dir/p.h</code></summary>

```
#define p1 p[0]
#define p2 p[1]
#define p3 p[2]
#define p4 p[3]
#define p5 p[4]
#define k0 p[5]
#define scaling_x1 p[6]
#define offset_x2 p[7]
#define observable_x1withsigma_sigma p[8]
```

</details>

<details><summary>First lines of <code>model_dir/setup.py</code></summary>

```
"""AMICI model package setup"""

import importlib.metadata
import os
import sys
from pathlib import Path

from amici import _get_amici_path
from amici._installation.custom_commands import AmiciBuildCMakeExtension
from cmake_build_extension import CMakeExtension
from setuptools import find_namespace_packages, setup

```

</details>

<details><summary>First lines of <code>model_dir/sigmay.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "p.h"
#include "y.h"
#include "sigmay.h"

namespace amici {
namespace model_biosim_model {

void sigmay_biosim_model(realtype *sigmay, const realtype t, const realtype *p, const realtype *k, const realtype *y){
```

</details>

<details><summary>First lines of <code>model_dir/sigmay.h</code></summary>

```
#define sigma_yx1 sigmay[0]
#define sigma_yx2 sigmay[1]
#define sigma_yx3 sigmay[2]
#define sigma_yobservable_x1 sigmay[3]
#define sigma_yobservable_x2 sigmay[4]
#define sigma_yobservable_x3 sigmay[5]
#define sigma_yobservable_x1_scaled sigmay[6]
#define sigma_yobservable_x2_offsetted sigmay[7]
#define sigma_yobservable_x1withsigma sigmay[8]
#define sigma_yc1 sigmay[9]
```

</details>

<details><summary>First lines of <code>model_dir/swig/CMakeLists.txt</code></summary>

```
if(DEFINED ENV{SWIG})
  set(SWIG_EXECUTABLE $ENV{SWIG})
endif()

find_package(SWIG REQUIRED)
include(${SWIG_USE_FILE})

if(DEFINED ENV{PYTHON_EXECUTABLE})
    set(Python3_EXECUTABLE $ENV{PYTHON_EXECUTABLE})
endif()
# We don't need "Interpreter" here, but without that, FindPython3 will
# ignore the Python version selected via $Python3_EXECUTABLE
```

</details>

<details><summary>First lines of <code>model_dir/swig/biosim_model.i</code></summary>

```
%define MODULEIMPORT
"
import amici
import amici.sim.sundials
import datetime
import importlib.util
import os
import sysconfig
import warnings
from pathlib import Path

ext_suffix = sysconfig.get_config_var('EXT_SUFFIX')
```

</details>

<details><summary>First lines of <code>model_dir/w.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "x.h"
#include "p.h"
#include "w.h"

namespace amici {
namespace model_biosim_model {

void w_biosim_model(realtype *w, const realtype t, const realtype *x, const realtype *p, const realtype *k, const realtype *h, const realtype *tcl, const realtype *spl, bool include_static){
```

</details>

<details><summary>First lines of <code>model_dir/w.h</code></summary>

```
#define observable_x1 w[0]
#define observable_x1_scaled w[1]
#define observable_x1withsigma w[2]
#define observable_x2 w[3]
#define observable_x2_offsetted w[4]
#define observable_x3 w[5]
#define flux_r1 w[6]
#define flux_r2 w[7]
#define flux_r3 w[8]
#define flux_r4 w[9]
#define flux_r5 w[10]
#define flux_r6 w[11]
```

</details>

<details><summary>First lines of <code>model_dir/wrapfunctions.cpp</code></summary>

```
#include "wrapfunctions.h"
#include "biosim_model.h"
#include "amici/model.h"

namespace amici {
namespace generic_model {

std::unique_ptr<amici::Model> get_model() {
    return std::unique_ptr<amici::Model>(
        new amici::model_biosim_model::Model_biosim_model()
    );
}
```

</details>

<details><summary>First lines of <code>model_dir/wrapfunctions.h</code></summary>

```
#ifndef _amici_wrapfunctions_h
#define _amici_wrapfunctions_h

#include <memory>

#include "amici/model.h"

namespace amici::generic_model {

/**
 * @brief Wrapper function to instantiate the linked Amici model without knowing
 * the name at compile time.
```

</details>

<details><summary>First lines of <code>model_dir/x.h</code></summary>

```
#define x1 x[0]
#define x2 x[1]
#define x3 x[2]
```

</details>

<details><summary>First lines of <code>model_dir/x0.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "p.h"

namespace amici {
namespace model_biosim_model {

void x0_biosim_model(realtype *x0, const realtype t, const realtype *p, const realtype *k){
    x0[0] = 0.10000000000000001;
    x0[1] = 0.40000000000000002;
```

</details>

<details><summary>First lines of <code>model_dir/x_rdata.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "x.h"
#include "p.h"

namespace amici {
namespace model_biosim_model {

void x_rdata_biosim_model(realtype *x_rdata, const realtype *x, const realtype *tcl, const realtype *p, const realtype *k){
    x_rdata[0] = x1;
```

</details>

<details><summary>First lines of <code>model_dir/x_rdata.h</code></summary>

```
#define x1 x_rdata[0]
#define x2 x_rdata[1]
#define x3 x_rdata[2]
```

</details>

<details><summary>First lines of <code>model_dir/x_solver.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "x_rdata.h"

namespace amici {
namespace model_biosim_model {

void x_solver_biosim_model(realtype *x_solver, const realtype *x_rdata){
    x_solver[0] = x1;
    x_solver[1] = x2;
```

</details>

<details><summary>First lines of <code>model_dir/x_solver.h</code></summary>

```
#define x_solver0 x_solver[0]
#define x_solver1 x_solver[1]
#define x_solver2 x_solver[2]
```

</details>

<details><summary>First lines of <code>model_dir/xdot.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "x.h"
#include "p.h"
#include "w.h"
#include "xdot.h"

namespace amici {
namespace model_biosim_model {

```

</details>

<details><summary>First lines of <code>model_dir/xdot.h</code></summary>

```
#define dx1dt xdot[0]
#define dx2dt xdot[1]
#define dx3dt xdot[2]
```

</details>

<details><summary>First lines of <code>model_dir/y.cpp</code></summary>

```
#include "amici/symbolic_functions.h"
#include "amici/defines.h"

#include <algorithm>
#include "x.h"
#include "p.h"
#include "w.h"

namespace amici {
namespace model_biosim_model {

void y_biosim_model(realtype *y, const realtype t, const realtype *x, const realtype *p, const realtype *k, const realtype *h, const realtype *w){
```

</details>

<details><summary>First lines of <code>model_dir/y.h</code></summary>

```
#define yx1 y[0]
#define yx2 y[1]
#define yx3 y[2]
#define yobservable_x1 y[3]
#define yobservable_x2 y[4]
#define yobservable_x3 y[5]
#define yobservable_x1_scaled y[6]
#define yobservable_x2_offsetted y[7]
#define yobservable_x1withsigma y[8]
#define yc1 y[9]
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
amici=1.1.0 states=3 parameters=9 timepoints=101 sensitivities=forward status=0
```

</details>

<details><summary>First lines of <code>sensitivities.csv</code></summary>

```
time,parameter,species,dx_dp
0,p1,x1,0
0,p1,x2,0
0,p1,x3,0
0,p2,x1,0
0,p2,x2,0
0,p2,x3,0
0,p3,x1,0
0,p3,x2,0
0,p3,x3,0
0,p4,x1,0
0,p4,x2,0
```

</details>

<details><summary>First lines of <code>species.csv</code></summary>

```
time,x1,x2,x3
0,0.1,0.4,0.7
0.1,0.25640545,0.50240381,0.52229498
0.2,0.37162206,0.57334533,0.39444564
0.3,0.45194902,0.62336944,0.30303653
0.4,0.50537379,0.65908472,0.23788907
0.5,0.53936722,0.68467853,0.19149058
0.6,0.55996776,0.70291097,0.15840024
0.7,0.57165981,0.71568852,0.13472701
0.8,0.57760011,0.72438017,0.11771026
0.9,0.57993194,0.72999482,0.10540045
1,0.58007244,0.73328717,0.096424058
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--tend` | End time | 10 | 0.001 to 100000 |
| `--points` | Output time points | 101 | 2 to 5000 |
| `--sensitivities` | Parameter sensitivities | forward | none, forward |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- **`rdata.x`.** One row per output time point, one column per species, in the order of `model.get_state_ids()`.
- **`rdata.sx`.** Present when sensitivities are on. Index it as `[time, parameter, species]`. A value is the derivative of that species at that time with respect to that parameter, in the order of `model.get_free_parameter_ids()`.
- **`rdata.status`.** The solver status. A non-success value means the integration failed.
- **Model directory.** The generated C++ sources and the compiled extension. Reuse it to skip recompiling, as long as the SBML file is unchanged.

The recipe on this page writes `species.csv` (a time column and one column per species) and, with sensitivities on, `sensitivities.csv` in long form: time, parameter, species and the derivative. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **A compiler is required at run time.** Each new model is compiled. Without g++ the import step fails, even though `import amici` works.
- **Compile in a directory that allows execution.** The compiled module is loaded from the model directory. On systems that mount `/tmp` without execute permission, point the model directory and `TMPDIR` somewhere else.
- **Changing the SBML means recompiling.** Parameters, tolerances and time points can change without recompiling. Equations cannot.
- **Parameters fixed at import cannot get sensitivities.** Mark a parameter as fixed in `sbml2amici` and AMICI treats it as a constant. Leave it free if you need its sensitivity.
- **Old tutorials use camelCase names.** Version 1.0 renamed methods to snake_case, for example `set_timepoints` and `get_state_ids`. Check the documentation for your installed version.

## Further reading

- Repository and licence: https://github.com/AMICI-dev/AMICI
- Documentation: https://amici.readthedocs.io/en/latest/
- Python installation: https://github.com/AMICI-dev/AMICI/blob/main/doc/python_installation.rst
- Extended notebook with sensitivities: https://github.com/AMICI-dev/AMICI/blob/main/doc/examples/getting_started_extended/GettingStartedExtended.ipynb
- Fröhlich F, Weindl D, Schälte Y, Pathirana D, Paszkowski Ł, Lines GT, Stapor P, Hasenauer J (2021). AMICI: high-performance sensitivity analysis for large ordinary differential equation models. Bioinformatics 37:3676-3677. https://doi.org/10.1093/bioinformatics/btab227

---

Cite: Fröhlich F, Weindl D, Schälte Y, Pathirana D, Paszkowski Ł, Lines GT, Stapor P, Hasenauer J (2021). AMICI: high-performance sensitivity analysis for large ordinary differential equation models. Bioinformatics 37:3676-3677. doi:10.1093/bioinformatics/btab227

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/amici).
