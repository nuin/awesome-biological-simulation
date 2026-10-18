# sPyNNaker

> Runs PyNN-defined spiking neural network simulations on SpiNNaker neuromorphic hardware, for researchers who have access to a SpiNNaker board or the Manchester machine.

Licence: Apache-2.0 · [Source code](https://github.com/SpiNNakerManchester/sPyNNaker)

## What it simulates

sPyNNaker lets you write a spiking network in PyNN, the common Python interface for neural simulators, and run it on SpiNNaker. SpiNNaker is a neuromorphic computer built from many small ARM cores that exchange spike packets over a network. Each core simulates a group of neurons in real time. The full machine in Manchester has about a million cores.

You define populations (for example `IF_curr_exp` leaky integrate-and-fire cells), projections between them with synapse types and plasticity rules such as spike-timing-dependent plasticity (STDP), inputs such as current sources or spike trains, and the quantities to record. sPyNNaker maps the network onto cores, loads the data onto the machine, runs it, and pulls the recorded spikes and voltages back as Neo objects.

The neurons are points with simple synapses, stepped at 1 ms in the examples. It is not a detailed biophysical simulator. The documentation keeps a page of supported models and limitations.

## When to use it

Use sPyNNaker if you have a SpiNNaker board, an account on the Manchester machine, or the EBRAINS platform, and you want large spiking networks in real time or want to test neuromorphic hardware.

- Use [NGC-Learn](ngclearn.md) for spiking circuits on an ordinary CPU or GPU, with JAX.
- Use [Simbrain](simbrain.md) for a desktop tool to build and watch a small network.
- Use [NetPyNE](netpyne.md) when each neuron needs morphology and ion channels.

## Install

There is no runnable recipe here. A simulation needs a SpiNNaker machine: a local board, a spalloc server such as the Manchester one, or the EBRAINS, Jupyter or portal routes in the documentation. A virtual mode runs the mapping steps without hardware but does not run the network.

The package is on PyPI as `sPyNNaker`; the current version is 7.4.1 (PyPI shows it as `1!7.4.1`, with an epoch prefix). The install guide recommends a virtual environment, Python 3.12 and Ubuntu 22.04. It lists Python 3.13 as unsupported at the time of writing.

```
pip install matplotlib
pip install sPyNNaker
python -m spynnaker.pyNN.setup_pynn
```

The last line installs the `pyNN.spiNNaker` front end. The first import writes a `.spynnaker.cfg` file in your home directory. Edit its `[Machine]` section: set `machineName` and `version` for a local board (`version = 3` for a 4-chip board, `5` for a 48-chip board), or `spalloc_server` and `spalloc_user` for a server. For virtual mode, set `width`, `height` and `virtual_board = True`. A local board needs your network adapter set to `192.168.240.254` with mask `255.255.255.0`.

The conda-forge channel has no sPyNNaker package. The licence is Apache-2.0 (repository LICENSE file).

## A first run

The PyNNExamples repository holds ready scripts. The install guide's check is `python va_benchmark.py` from its `examples` folder; if the install worked, a plot appears at the end. A small script is `current_injection_example.py`, taken from the PyNN documentation:

```python
import pyNN.spiNNaker as sim

sim.setup(timestep=1.0)
cells = sim.Population(4, sim.IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0, tau_m=10.0))
current_sources = [
    sim.DCSource(amplitude=0.5, start=50.0, stop=400.0),
    sim.StepCurrentSource(times=[50.0, 210.0, 250.0, 410.0], amplitudes=[0.4, 0.6, -0.2, 0.2]),
    sim.ACSource(start=50.0, stop=450.0, amplitude=0.2, offset=0.1, frequency=10.0, phase=180.0),
    sim.NoisyCurrentSource(mean=0.5, stdev=0.2, start=50.0, stop=450.0, dt=1.0),
]
for cell, source in zip(cells, current_sources):
    cell.inject(source)
cells.record('v')
sim.run(500.0)
vm = cells.get_data().segments[0].filter(name="v")[0]
sim.end()
```

Adapted from <https://github.com/SpiNNakerManchester/PyNNExamples/blob/master/examples/current_injection_example.py> and the install guide at <http://spinnakermanchester.github.io/spynnaker/8.0.0/PyNNOnSpinnakerInstall.html>.

## Reading the output

During a run the software prints its stages: partitioning, placement, routing, loading and running. Afterwards `get_data()` returns a Neo block. `segments[0]` holds the recorded variable as an analog signal, with one column per neuron and a time axis in ms. Spikes recorded with `record('spikes')` come back as spike trains, one per neuron. The example above plots the four membrane potentials against time, one for each current source type.

The example uses `timestep=1.0` ms.

## Pitfalls

- **No board, no results.** Virtual mode checks the script and the mapping only. The run returns before data load.
- **Config file first.** On first use sPyNNaker creates `.spynnaker.cfg` and exits. Edit it and run again.
- **Model limits.** Not every PyNN cell, synapse or connector is supported. Read the models and limitations page.
- **Python version.** Python 3.13 is not supported, per the install guide.
- **Epoch in the version.** To pin the version, write `sPyNNaker==1!7.4.1`, with the epoch.

## Further reading

- Software for SpiNNaker (all guides): https://spinnakermanchester.github.io/
- Installation guide: http://spinnakermanchester.github.io/spynnaker/8.0.0/PyNNOnSpinnakerInstall.html
- Examples: https://github.com/SpiNNakerManchester/PyNNExamples
- Source: https://github.com/SpiNNakerManchester/sPyNNaker
- Paper: Rhodes O et al. (2018). sPyNNaker: a software package for running PyNN simulations on SpiNNaker. Frontiers in Neuroscience 12:816. https://doi.org/10.3389/fnins.2018.00816

---

Cite: Rhodes O, et al. (2018). sPyNNaker: a software package for running PyNN simulations on SpiNNaker. Frontiers in Neuroscience 12:816. doi:10.3389/fnins.2018.00816

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/spynnaker).
