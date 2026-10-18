# GeNN

> Generate GPU (CUDA or HIP) code for large spiking neural network simulations, from C++ or the PyGeNN Python interface.

Licence: LGPL-2.1 · [Source code](https://github.com/genn-team/genn)

## What it simulates

GeNN (GPU-enhanced Neuronal Networks) simulates spiking neural networks. It is a code generator. You describe populations of neurons, synapses and inputs, and GeNN writes and compiles C++ for a CUDA or HIP GPU (or for the CPU). The compiled model then runs the time steps.

The model is described in C++ or, more often now, in Python with PyGeNN. Built-in neuron models include Izhikevich and leaky integrate-and-fire, and you can write your own models as snippets of code. The project ships example projects: the Potjans and Diesmann cortical microcircuit, the SuperSpike learning model and an insect-inspired mushroom-body MNIST classifier.

## When to use it

Use GeNN when a spiking model is too large or too slow on a CPU simulator and you have an NVIDIA or AMD GPU.

- Use NEST for large point-neuron models on CPU clusters.
- Use Brian 2 when you want to write equations in strings, with optional GPU code generation through add-ons.
- Use [PyNN](pynn.md) for a portable network description. Its list of back ends is NEURON, NEST, Brian 2, Arbor and neuromorphic hardware.

GeNN gives speed at the price of a compile step for each model, and it needs a compiler toolchain on the machine.

## Install

GeNN 5.5.0 is the current release (GitHub tag 5.5.0, October 2026). The project's own installation page says binary builds are planned but that for now GeNN is installed from source. PyGeNN is not on PyPI: the PyPI simple index has no `pygenn` project.

Before installing, set up a C++ compiler (GCC 7.5 or newer on Linux, Visual Studio 2019 or newer with the C++ workload on Windows), `libffi-dev` on Linux, and CUDA or HIP if you have a GPU. Set `CUDA_PATH` (for example `/usr/local/cuda`) or `HIP_PATH`. Then, per the README:

```
pip install -U pip
pip install https://github.com/genn-team/genn/archive/refs/tags/5.5.0.zip
```

The README also gives `pip install https://github.com/genn-team/genn/archive/refs/heads/master.zip` for the development version, an editable install (`git clone`, then `pip install -e .`) and a CUDA-enabled Docker image, `gennteam/genn`.

GeNN is documented as a guide only on this site. A model must be generated and compiled on the machine that runs it, and GPU use needs the driver and CUDA toolkit there. The licence is LGPL-2.1.

## A first run

The `comp_neuro_101` tutorial defines four Izhikevich neurons that fire in different regimes. Adapted from [tutorial 1, Defining populations of neurons](https://genn-team.github.io/genn/documentation/5/tutorials/comp_neuro_101/1_neurons.html):

```python
import numpy as np
import matplotlib.pyplot as plt
from pygenn import GeNNModel

model = GeNNModel("float", "tutorial1")
model.dt = 0.1

izk_init = {"V": -65.0, "U": -20.0,
            "a": [0.02, 0.1, 0.02, 0.02],
            "b": [0.2, 0.2, 0.2, 0.2],
            "c": [-65.0, -65.0, -50.0, -55.0],
            "d": [8.0, 2.0, 2.0, 4.0]}
pop = model.add_neuron_population("Neurons", 4, "IzhikevichVariable", {}, izk_init)
model.add_current_source("CurrentSource", "DC", pop, {"amp": 10.0}, {})

model.build()
model.load()

voltage = pop.vars["V"]
voltages = []
while model.t < 200.0:
    model.step_time()
    voltage.pull_from_device()
    voltages.append(voltage.values)
```

`model.build()` generates and compiles the code, and `model.load()` loads it. The tutorial then stacks the list into a matrix and plots one panel per neuron, titled RS, FS, CH and IB.

## Reading the output

State lives in the model, not in files. `pop.vars["V"]` is a view of the membrane potential, and `pull_from_device()` copies it from the GPU before you read `.values`. Copy the values each step, because the view points at the live state.

With a 0.1 ms step and 200 ms of simulation the list has 2000 rows of 4 values (the tutorial's own comment says a 2000 by 4 matrix). Each column is one neuron. The four parameter sets give four spiking patterns: regular spiking, fast spiking, chattering and intrinsically bursting. Spikes appear as sharp upstrokes followed by a reset to the neuron's `c` value.

For bigger models, record spikes with spike recording buffers and pull them once at the end of the run. The "Simulating networks" page of the documentation covers this.

## Pitfalls

- **Build time.** Every new model structure is generated and compiled. Keep structure fixed and change parameters through variables.
- **Compiler and CUDA versions must agree.** The README warns that the latest C++ compiler is not always compatible with the latest CUDA toolkit.
- **Windows.** Run installs from a Visual Studio native tools prompt.
- **Precision.** The model constructor takes the precision (`"float"` above). Set it deliberately.
- **Memory views alias state.** Appending the `values` array without a copy gives a list of the same array. The tutorial copies the values for this reason.
- **Copy cost.** Pulling every variable every step makes the GPU wait. Pull only what you plot.

## Further reading

- Documentation: https://genn-team.github.io/genn/
- Installation: https://genn-team.github.io/genn/documentation/5/installation.html
- Tutorials: https://genn-team.github.io/genn/documentation/5/tutorials/comp_neuro_101/1_neurons.html
- Source: https://github.com/genn-team/genn
- Papers: Knight JC, Komissarov A, Nowotny T (2021). PyGeNN. Frontiers in Neuroinformatics 15:659005. https://doi.org/10.3389/fninf.2021.659005. Yavuz E, Turner J, Nowotny T (2016). GeNN: a code generation framework for accelerated brain simulations. Scientific Reports 6:18854. https://doi.org/10.1038/srep18854

---

Cite: Knight JC, Komissarov A, Nowotny T (2021). PyGeNN: A Python Library for GPU-Enhanced Neural Networks. Front Neuroinform 15:659005. doi:10.3389/fninf.2021.659005

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/genn).
