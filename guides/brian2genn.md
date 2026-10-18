# Brian2GeNN

> A Brian 2 device that generates and runs GeNN code, so spiking-network models written in Python run on NVIDIA GPUs.

Licence: GPL-2.0 · [Source code](https://github.com/brian-team/brian2genn)

## What it simulates

Brian2GeNN is not a simulator of its own. It is a device for Brian 2, the Python simulator for spiking neural networks. When the device is selected, Brian 2 turns the model (neuron equations, synapses, monitors) into code for GeNN, compiles it, runs it and reads the results back into the normal Brian 2 objects.

GeNN (GPU enhanced Neuronal Networks) is a code-generation framework. It produces CUDA code for NVIDIA graphics cards, and a "CPU-only" mode that runs the same generated code on the processor. The point of Brian2GeNN is to run large Brian 2 networks on a GPU without writing CUDA.

The model is the usual Brian 2 one: groups of neurons with differential equations, a threshold and a reset, synapses with `on_pre` rules, and monitors for spikes and state variables. Integration uses a single fixed time step for the whole network, because GeNN has one clock.

## When to use it

Use it when a Brian 2 model is too slow on the CPU and an NVIDIA GPU is available. Networks with many neurons or synapses benefit most. The documentation says the device is in beta status.

The restrictions matter more than the speed for many scripts. The documentation lists unsupported features: linked variables, custom events, heterogeneous delays within one synapse group, multiple synaptic pathways, multiple clocks, multiple networks, custom schedules, and more than one `run` statement per script. `TimedArray` is limited to `run_regularly` code that runs on the CPU. Summed variables work from version 1.4 with restrictions.

Alternatives:

- Plain Brian 2 runs everything on the CPU, supports all features, and needs no GPU. Its standalone mode generates C++ code for the CPU.
- NEST scales spiking networks across CPU cores and clusters. It is a separate simulator with its own model language.
- [PyLEMS](pylems.md) runs small LEMS models and suits single cells rather than large networks.

## Install it yourself

There is no recipe on biosimhub for this tool. It needs an NVIDIA GPU with the CUDA toolkit and driver, and the hosted sandbox has no GPU. GeNN also compiles generated code at run time, which the sandbox (no network, read-only root) does not suit. The CPU-only mode would run without a GPU, but it still needs a GeNN build and a C++ compiler.

Per the documentation:

1. Install Brian 2 (the package pins `brian2` between 2.5.0.2 and below 2.6).
2. Install GeNN, following its own instructions, and put GeNN's `bin` directory on the path, or set the preference `devices.genn.path`.
3. Install the CUDA toolkit and driver. Set `CUDA_PATH`, or the preference `devices.genn.cuda_backend.cuda_path`.
4. Install the interface:

```bash
pip install brian2genn
```

The current PyPI version is 1.7.0 (July 2023). The project no longer provides conda packages; old ones remain in the `brian-team` channel under the `archive` label. Brian2GeNN is distributed under GPL-2.0.

## A first run

Adapted from the documentation, "Using Brian2GeNN" (https://brian2genn.readthedocs.io/en/stable/introduction/index.html).

Import the package, select the device after the other imports, and write the Brian 2 script as usual:

```python
from brian2 import *
import brian2genn
set_device('genn')

# ... define NeuronGroup, Synapses and monitors as in any Brian 2 script ...

run(500*ms)
```

At the first `run`, code for GeNN is generated, compiled and executed. For the CPU-only mode and debug output, the documentation gives `set_device('genn', use_GPU=False, debug=True)`. The preference `prefs.devices.genn.connectivity` takes `'DENSE'` or `'SPARSE'` and sets how GeNN stores connections.

## Reading the output

Nothing changes in how results are read. After `run`, a `SpikeMonitor` gives spike times and neuron indices, and a `StateMonitor` gives recorded variables, as with any Brian 2 device. The generated GeNN project stays in an output directory, where its generated code can be inspected.

## Pitfalls

- **One run per script.** For repeated runs, call `device.reinit()` and `device.activate()` after each `run`. Each run repeats the full code generation and compile step, which can take a noticeable time.
- **Version pin.** The package requires `brian2` older than 2.6. A recent Brian 2 install will conflict.
- **Synapse limits.** One delay per synapse group, and one pre and one post pathway.
- **Linked variables.** Rewrite the model so the shared input is computed inside the receiving group, as the documentation shows.

## Further reading

- Repository: https://github.com/brian-team/brian2genn
- Documentation: https://brian2genn.readthedocs.io/
- Unsupported features: https://brian2genn.readthedocs.io/en/stable/introduction/exclusions.html
- GeNN: https://github.com/genn-team/genn
- Stimberg M, Goodman DFM, Nowotny T (2020). Brian2GeNN: accelerating spiking neural network simulations with graphics hardware. Scientific Reports 10:410. https://doi.org/10.1038/s41598-019-54957-7

---

Cite: Stimberg M, Goodman DFM, Nowotny T (2020). Brian2GeNN: accelerating spiking neural network simulations with graphics hardware. Scientific Reports 10:410. doi:10.1038/s41598-019-54957-7

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/brian2genn).
