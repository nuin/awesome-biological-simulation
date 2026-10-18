# CARLsim 6

> C++ library for large-scale spiking neural networks of Izhikevich neurons with synaptic plasticity, running on CPUs or NVIDIA GPUs.

Licence: MIT · [Source code](https://github.com/UCI-CARL/CARLsim6)

## What it simulates

CARLsim is a C++ library for large spiking neural networks. Neurons follow the Izhikevich model, and the README describes realistic synaptic dynamics. The interface is PyNN-like: you set parameters at the neuron, synapse and network level in C++.

The same network code runs in a CPU mode on ordinary x86 machines and in a GPU mode on NVIDIA cards. Release 6.1 (2023-07-13) adds an axonal plasticity learning rule. CARLsim 6 also adds CUDA 11 support, a CMake build, neuromodulatory features and an integration with the Python library LEAP for parameter tuning.

## When to use it

Use CARLsim when you want to run networks of thousands to millions of Izhikevich neurons with plasticity, for example for robotics or neuromorphic research, and you are comfortable writing C++.

- Use [Auryn](auryn.md) for fast event-driven CPU simulation of integrate-and-fire networks.
- Use [Brian2CUDA](brian2cuda.md) when you prefer Python and equation-based models on a GPU.
- Use [Rockpool](rockpool.md) when you want to train a network by gradient descent.

## Install

There is no recipe for this tool. The project is built and tested against CUDA, and a GPU is its main target. The README lists CMake 3.20 or newer, and the CUDA Toolkit 11.0 or newer only for GPU mode, with the CUDA samples installed because CARLsim uses `helper_cuda.h`. A GPU with compute capability 6.0 or higher is optional, again only for GPU mode. MATLAB or Octave is optional, for the Offline Analysis Toolbox.

The release was tested on Ubuntu 20.04, Windows 10 and 11, CUDA 11.2 to 11.7, and Titan Xp, 1080ti, RTX 3090 and A100 cards. The latest release is v6.1 (2023-07-13). The licence is MIT.

Steps from the README:

```bash
cd ~/git
git clone https://github.com/UCI-CARL/CARLsim6.git CARLsim6
cd CARLsim6
mkdir .build
cd .build
cmake -DCMAKE_INSTALL_PREFIX=/home/user1/carlsim6 -DCMAKE_BUILD_TYPE=Release ../.
make install
```

The user guide documents the CMake option `-DCARLSIM_NO_CUDA=OFF` to switch CUDA support. It also describes the googletest dependency used by the test suite. See the [Getting started chapter](http://uci-carl.github.io/CARLsim6/ch1_getting_started.html) for the full setup.

## A first run

Adapted from the README quickstart. After `make install`, open a new terminal, check the environment with `env`, and start the sample installed under the prefix:

```bash
~/carlsim6/samples/hello_world
```

The user guide also describes a `projects/hello_world` template that you copy and compile for your own network.

## Reading the output

The sample prints its progress to the terminal and writes spike data through CARLsim's monitors. CARLsim has spike, group, connection and neuron monitors, listed in the source tree under `carlsim/monitor`. Their files can be loaded with the Offline Analysis Toolbox in MATLAB or Octave. Read the sample's source to see which monitors it enables, since the output depends on that code.

CARLsim runs in CPU mode or GPU mode, chosen when the simulation object is created. The run mode changes speed, not the model.

## Pitfalls

- **CUDA versions matter.** The tested range is CUDA 11.2 to 11.7. Other versions are untested by the project.
- **Samples need the CUDA samples headers.** `helper_cuda.h` must be on the include path.
- **Environment variables.** Set `PATH` and `LD_LIBRARY_PATH` to include the CMake, googletest and CARLsim install folders, as the user guide shows.
- **Older versions exist.** The README points to CARLsim 5 or 4 when the prerequisites cannot be met.
- **The sample sets the output.** Which files appear depends on the monitors the program creates.

## Further reading

- User guide: http://uci-carl.github.io/CARLsim6/
- Source: https://github.com/UCI-CARL/CARLsim6
- Niedermeier L, et al. (2022). CARLsim 6: an open source library for large-scale, biologically detailed spiking neural network simulation. IJCNN 2022. https://doi.org/10.1109/IJCNN55064.2022.9892644

---

Cite: Niedermeier L, Chen K, Xing J, Das A, Kopsick J, Scott E, Sutton N, Weber K, Dutt N, Krichmar JL (2022). CARLsim 6: an open source library for large-scale, biologically detailed spiking neural network simulation. Proc IJCNN 2022. doi:10.1109/IJCNN55064.2022.9892644

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/carlsim6).
