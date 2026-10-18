# NEST

> Simulate point-neuron spiking networks; the example drives integrate-and-fire neurons with a constant current and records a voltage trace and spike times.

Licence: GPL-2.0-or-later · [Source code](https://github.com/nest/nest-simulator)

## What it simulates

NEST simulates the dynamics, size and structure of spiking neural networks. Its neurons are mostly point neurons (one compartment) or have a few compartments, and it ships a large library of neuron and synapse models, including plasticity rules. The project has been developed since 1994 and runs from a laptop to the largest supercomputers.

A NEST script follows the logic of an electrophysiology experiment. You create nodes (neurons and devices such as voltmeters, spike recorders and current generators), connect them, call `Simulate` for a number of milliseconds, then read the recorders. Networks of thousands to millions of neurons are the target use. Typical models are cortical microcircuits, balanced random networks and learning rules.

## When to use it

Use NEST when network size, speed or a validated model from a paper matters more than writing new equations. It uses OpenMP threads and MPI to spread a network over cores and nodes.

- Use [Brian 2](brian2.md) when you want to write a new neuron model as equations and run a modest network.
- Use [NEURON](neuron.md) when single-cell morphology and ion channels are the question.
- Use [BrainPy](brainpy.md) when you want JAX compilation or neural-mass models next to spiking ones.

## Install

The current release is NEST 3.10 (June 2026). The NEST installation page lists pip, Docker, conda-forge, an Ubuntu PPA and Homebrew.

```
python3 -m venv nest-env
source nest-env/bin/activate
pip install --upgrade pip
pip install nest-simulator
```

The pip page states the requirements: Python 3.9 to 3.13, Linux or macOS, and lists the x86_64 architecture. PyPI also carries macOS arm64 wheels for 3.10.0. On macOS, multithreading needs `brew install libomp`. If no wheel exists for your Python, pip tries to build NEST and then needs a C++ compiler and the Boost headers. The conda-forge package `nest-simulator` 3.10 exists for linux-64, osx-64 and osx-arm64. Extras such as `nest-simulator[sonata]`, `[server]` and `[examples]` add HDF5 network files, a REST server and example dependencies.

NEST is licensed GPL-2.0-or-later.

## Run the tested example

This recipe builds NEST in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 6.8 s. NEST has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [nest-recipe.tar.gz](https://biosimhub.pages.dev/guides/nest/nest-recipe.tar.gz) (Dockerfile, run_nest.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf nest-recipe.tar.gz
   cd nest
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/nest:3.10 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/nest:3.10 python /opt/run_nest.py --neurons 1 --current 376 \
    --duration 1000 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 368 B |
| `spikes.csv` | 195 B |
| `voltage.csv` | 17.5 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```

             -- N E S T --

 Copyright (C) 2004 The NEST Initiative

 Version: 3.10.0
 Built  : Jun 12 2026 10:07:52

 This program is provided AS IS and comes with NO WARRANTY.
 See the file LICENSE for details.

 Problems or suggestions?
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
sender_gid,time_ms
1,59.300
1,120.600
1,181.900
1,243.200
1,304.500
1,365.800
1,427.100
1,488.400
1,549.700
1,611.000
1,672.300
```

</details>

<details><summary>First lines of <code>voltage.csv</code></summary>

```
time_ms,V_m_mV
1.000,-68.5688
2.000,-67.2737
3.000,-66.1019
4.000,-65.0416
5.000,-64.0822
6.000,-63.2141
7.000,-62.4286
8.000,-61.7179
9.000,-61.0748
10.000,-60.4929
11.000,-59.9664
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--neurons` | Neurons | 1 | 1 to 1000 |
| `--current` | Constant input current I_e (pA) | 376 | 0 to 2000 |
| `--duration` | Simulated time (ms) | 1000 | 10 to 10000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the NEST example [one_neuron.py](https://github.com/nest/nest-simulator/blob/main/pynest/examples/one_neuron.py) (also in the [NEST examples gallery](https://nest-simulator.readthedocs.io/en/stable/auto_examples/one_neuron.html)): one neuron driven by a constant current, with its membrane potential recorded.

```python
import matplotlib.pyplot as plt
import nest
import nest.voltage_trace

nest.verbosity = nest.VerbosityLevel.WARNING
nest.ResetKernel()

neuron = nest.Create("iaf_psc_alpha")
voltmeter = nest.Create("voltmeter")
neuron.I_e = 376.0
nest.Connect(voltmeter, neuron)
nest.Simulate(1000.0)

nest.voltage_trace.from_device(voltmeter)
plt.show()
```

`Create` makes the nodes. Setting `I_e` gives the neuron a constant input current of 376 pA. `Connect(voltmeter, neuron)` runs from the voltmeter to the neuron because NEST connections follow the direction of the signal in the kernel, and the voltmeter observes the neuron. `Simulate(1000.0)` runs 1000 ms.

## Reading the output

- **Voltage trace.** `voltage_trace.from_device` plots membrane potential against time. With enough current the potential climbs to threshold, resets, and repeats.
- **Raw data.** `voltmeter.get("events")` returns arrays including `times` and `V_m`. A `spike_recorder` returns `times` and `senders` (the ids of the neurons that fired).
- **Recipe output.** The recipe writes `voltage.csv` (time and membrane potential of the first neuron) and `spikes.csv` (neuron id and spike time). Raising `--current` raises the spike count; setting it low enough gives none.

The example page shows no numeric output, so no figures are quoted here. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **Call `ResetKernel()` first** in scripts and notebooks. Without it, nodes and connections from the previous run stay in the kernel.
- **Time is in milliseconds, currents in pA, potentials in mV.** Mixing in SI units gives wrong results with no error.
- **Connection direction.** Recorders such as voltmeters connect from the device to the neuron, spike recorders from the neuron to the device.
- **Threads and seeds.** Results are reproducible for a given seed and thread count. Changing `local_num_threads` changes the random streams.
- **Check model names.** NEST has many similar models (`iaf_psc_alpha`, `iaf_psc_exp`, `iaf_cond_alpha`). Each has its own parameters and units.

## Further reading

- Documentation: https://nest-simulator.readthedocs.io/en/stable/
- Install with pip: https://nest-simulator.readthedocs.io/en/stable/installation/pip_install.html
- Source: https://github.com/nest/nest-simulator
- Citing NEST: https://nest-simulator.readthedocs.io/en/stable/citing-nest.html (for 2.8 and later, cite the version on Zenodo; otherwise the paper below)
- Paper: Gewaltig M-O, Diesmann M (2007). NEST (NEural Simulation Tool). Scholarpedia 2(4):1430. https://doi.org/10.4249/scholarpedia.1430

---

Cite: Gewaltig M-O, Diesmann M (2007). NEST (NEural Simulation Tool). Scholarpedia 2(4):1430. doi:10.4249/scholarpedia.1430

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/nest).
