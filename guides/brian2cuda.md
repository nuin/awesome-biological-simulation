# Brian2CUDA

> GPU backend for the Brian 2 spiking network simulator that generates C++/CUDA code for NVIDIA graphics cards.

Licence: GPL-3.0-only · [Source code](https://github.com/brian-team/brian2cuda)

## What it simulates

Brian2CUDA is a code-generation device for Brian 2. You write a spiking network model in Brian 2 (equations, neuron groups, synapses, monitors), switch one device setting, and Brian2CUDA generates C++/CUDA code that runs the simulation on an NVIDIA GPU.

It does not define a new model language. Everything about the model comes from Brian 2, where neurons are given as differential equations with physical units. Brian2CUDA changes only where the code runs. It targets large networks, where the GPU's parallelism pays off against the time to compile and transfer data.

## When to use it

Use Brian2CUDA when a Brian 2 model works on the CPU but is too slow, and you have a CUDA-capable GPU.

- Use plain Brian 2 first. Its standalone C++ device needs no GPU, and small networks often run faster on the CPU.
- Use [CARLsim 6](carlsim6.md) when you prefer a C++ library with Izhikevich neurons and built-in plasticity rules.
- Use [Auryn](auryn.md) for fast CPU simulation of plastic networks in C++.
- Use [Rockpool](rockpool.md) when the goal is training networks for hardware.

## Install

There is no recipe for this tool. It needs an NVIDIA GPU, the CUDA toolkit with `nvcc`, and a C++ compiler, none of which a CPU-only sandbox provides.

The current PyPI release is 1.0b1 (2025-12-05), a beta. It requires Python 3.10 or newer and pins Brian 2 at 2.10.1. The README gives one command:

```bash
python -m pip install brian2cuda
```

Because every release so far is a pre-release, pip installs the newest one when you name the package. The licence is GPL-3.0-only.

Brian2CUDA looks for CUDA in this order: the preference `devices.cuda_standalone.cuda_backend.cuda_path`, the `CUDA_PATH` environment variable, the location of `nvcc` on `PATH`, then `/usr/local/cuda` and `/opt/cuda`. It queries GPUs with `nvidia-smi` and uses the one with the highest compute capability unless you set `gpu_id`. Drivers older than 510.39.01 may need extra setup. On a machine without a GPU you can still generate code by turning off GPU detection and giving the compute capability and runtime version as preferences.

## A first run

Adapted from the [Brian2CUDA introduction](https://brian2cuda.readthedocs.io/en/latest/introduction/index.html). Take any Brian 2 script and change its imports:

```python
# Standard Brian2 import
from brian2 import *

# Enable GPU usage via Brian2CUDA
import brian2cuda
set_device("cuda_standalone")
```

The rest of the script stays as written. For a first model, the Brian 2 tutorial on neurons defines `eqs = 'dv/dt = (1-v)/tau : 1'`, creates `NeuronGroup(1, eqs)` and calls `run(100*ms)`. See [Brian 2 standalone code generation](https://brian2.readthedocs.io/en/stable/user/computation.html) for other `set_device` options.

## Reading the output

- Monitors work as in Brian 2. After `run`, read `SpikeMonitor.t` and `.i` for spike times and neuron indices, and `StateMonitor.v` for traces.
- The first call generates and compiles code, so expect a delay before the simulation starts. The project's performance page covers when that cost is worth it.
- Output is written to a project directory that standalone mode creates. Set `directory=` in `set_device` to choose it.
- Spike and event monitor data are not sorted by neuron index. This is listed under known issues.

## Pitfalls

- **Beta software.** Version 1.0b1 is the latest, and the docs carry a known-issues page.
- **Changing delays between `run` calls loses spikes.** The same holds for changing the time step of synapses with delays.
- **Mixed time steps.** A synapse with homogeneous delays and a source group on a different `dt` triggers a documented bug.
- **Single precision** fails with variable names that mix double digits and a dot or scientific notation.
- **Brian 2 pin.** The package fixes Brian 2 at 2.10.1, which may clash with other environments.
- **Support.** Use the Brian forum for questions and the GitHub tracker for bugs.

## Further reading

- Documentation: https://brian2cuda.readthedocs.io
- Source: https://github.com/brian-team/brian2cuda
- Brian 2 documentation: https://brian2.readthedocs.io
- Alevi D, Stimberg M, Sprekeler H, Obermayer K, Augustin M (2022). Brian2CUDA: flexible and efficient simulation of spiking neural network models on GPUs. Front Neuroinform. https://doi.org/10.3389/fninf.2022.883700

---

Cite: Alevi D, Stimberg M, Sprekeler H, Obermayer K, Augustin M (2022). Brian2CUDA: flexible and efficient simulation of spiking neural network models on GPUs. Front Neuroinform 16:883700. doi:10.3389/fninf.2022.883700

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/brian2cuda).
