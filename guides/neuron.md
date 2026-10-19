# NEURON

> Simulate a biophysically detailed neuron; the example is a Hodgkin-Huxley soma with a current-clamp pulse and a recorded membrane potential.

Licence: BSD-3-Clause · [Source code](https://github.com/neuronsimulator/nrn)

## What it simulates

NEURON simulates neurons and networks of neurons with biophysical detail. A cell is built from sections: unbranched cables, each divided into segments. NEURON solves the cable equation along them, with voltage-dependent ion channels, synapses and ion concentrations on each section. Channel behaviour is written in NMODL, a small language that NEURON compiles. The Hodgkin-Huxley channels (`hh`) and the passive membrane are built in.

It also handles networks of such cells, including parallel runs over MPI, and reaction-diffusion inside cells through its RxD module. Models run from Python or from the older HOC scripting language.

## When to use it

Use NEURON when the shape of the neuron matters: dendritic integration, back-propagating spikes, channel distributions along a cell, extracellular stimulation.

- Use [NEST](nest.md) for large networks of simple point neurons.
- Use [Brian 2](brian2.md) for equation-defined point-neuron models and quick prototypes.
- Use [Nengo](nengo.md) when the goal is a functional model, such as a network that represents and transforms a signal.

## Install

NEURON 9.0.2 is the current release on PyPI (the GitHub release is also 9.0.2). The conda-forge package `neuron` is at 9.0.1.

```
pip3 install neuron
```

or

```
conda install -c conda-forge neuron
```

The README gives `pip3 install neuron` for the official Linux and Mac wheels, and installers for Mac and Windows on the GitHub releases page. The PyPI package needs Python 3.10 or later. conda-forge builds exist for linux-64, linux-aarch64, osx-64 and osx-arm64. Custom channels written in NMODL need `nrnivmodl`, which compiles them against a C++ compiler. NEURON 9 and later is stricter about C++ in MOD files: see "Adapting MOD files for C++ with NEURON >= 9.0" in the NEURON docs if an older mechanism fails to compile.

The licence is BSD-3-Clause for the distribution (the repository Copyright file says files without their own notice use a compatible licence).

## Run the tested example

This recipe builds NEURON in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.8 s.

1. Download [neuron-recipe.tar.gz](https://biosimhub.pages.dev/guides/neuron/neuron-recipe.tar.gz) (Dockerfile, run_neuron.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf neuron-recipe.tar.gz
   cd neuron
   sh run.sh
   ```

![Terminal recording of the NEURON example run](https://biosimhub.pages.dev/media/neuron/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/neuron:9.0.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/neuron:9.0.1 python /opt/run_neuron.py --amp 0.9 --delay 2 \
    --dur 0.1 --tstop 40 --length 20 --diam 20 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 54 B |
| `summary.csv` | 64 B |
| `trace.csv` | 27.7 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/neuron/result-dark.png"><img src="https://biosimhub.pages.dev/media/neuron/result.png" alt="Plot of the NEURON example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 1601 samples, peak 37.0 mV, 1 crossings of 0 mV
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
peak_v_mV,peak_time_ms,upward_crossings_of_0mV
36.956,5.250,1
```

</details>

<details><summary>First lines of <code>trace.csv</code></summary>

```
time_ms,v_mV
0.0000,-65.0000
0.0250,-64.9993
0.0500,-64.9985
0.0750,-64.9978
0.1000,-64.9971
0.1250,-64.9964
0.1500,-64.9957
0.1750,-64.9950
0.2000,-64.9943
0.2250,-64.9936
0.2500,-64.9930
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--amp` | Clamp amplitude (nA) | 0.9 | 0 to 20 |
| `--delay` | Clamp onset (ms) | 2 | 0 to 1000 |
| `--dur` | Clamp duration (ms) | 0.1 | 0.01 to 1000 |
| `--tstop` | Simulated time (ms) | 40 | 1 to 1000 |
| `--length` | Soma length (um) | 20 | 1 to 500 |
| `--diam` | Soma diameter (um) | 20 | 1 to 500 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the NEURON tutorial [Scripting NEURON basics](https://nrn.readthedocs.io/en/latest/tutorials/scripting-neuron-basics.html): a single-compartment cell with Hodgkin-Huxley channels and a brief current pulse.

```python
from neuron import n
from neuron.units import mV, ms

soma = n.Section("soma")
soma.L = 20
soma.diam = 20
soma.insert(n.hh)

iclamp = n.IClamp(soma(0.5))
iclamp.delay = 2
iclamp.dur = 0.1
iclamp.amp = 0.9

v = n.Vector().record(soma(0.5)._ref_v)
t = n.Vector().record(n._ref_t)

n.load_file("stdrun.hoc")
n.finitialize(-65 * mV)
n.continuerun(40 * ms)
```

The tutorial notes that `n` is the current name of the module that older code calls `h`; both work in NEURON 9. The cell is a 20 by 20 micrometre soma. The clamp injects 0.9 nA from 2 ms for 0.1 ms. The run starts at -65 mV and stops at 40 ms. The tutorial then plots `v` against `t` with bokeh or matplotlib.

## Reading the output

- **`v` and `t`** are NEURON `Vector` objects: the membrane potential at the middle of the soma and the matching times, one value per time step. `v.to_python()` or `list(v)` converts them.
- **The trace.** At rest the membrane sits near the starting potential. The pulse depolarises it. If it crosses threshold, the Hodgkin-Huxley channels produce an action potential of the shape known from the squid giant axon, then the potential returns to rest.
- **`soma.psection()`** prints the section's properties: geometry, `Ra`, `cm`, the `hh` conductances, and the attached point processes. The tutorial shows `gnabar` 0.12 and `gkbar` 0.036 S/cm2 as the `hh` defaults.

The recipe writes `trace.csv` (time and potential) and `summary.csv` with the peak potential, the time of the peak and the number of upward crossings of 0 mV. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **Units.** Time is ms, potential mV, length micrometres, current nA for `IClamp`. Concentrations are mM.
- **Initialise before running.** Call `finitialize` before `continuerun`; otherwise the state is undefined.
- **`nseg`.** Each section defaults to one segment. For long cables, raise `nseg` (an odd number) or the spatial resolution is poor.
- **Hodgkin-Huxley kinetics are for squid axon.** For other cells, use channel models from ModelDB or write your own NMODL.
- **Compile step for custom mechanisms.** Run `nrnivmodl` in the folder with your `.mod` files, and run Python from that folder.

## Further reading

- Documentation: https://nrn.readthedocs.io/
- Source: https://github.com/neuronsimulator/nrn
- Ball-and-stick tutorials (morphology and networks): https://nrn.readthedocs.io/en/latest/tutorials/ball-and-stick-1.html
- Paper: Hines ML, Carnevale NT (1997). The NEURON simulation environment. Neural Comput 9:1179-1209. https://doi.org/10.1162/neco.1997.9.6.1179

---

Cite: Hines ML, Carnevale NT (1997). The NEURON simulation environment. Neural Comput 9:1179-1209. doi:10.1162/neco.1997.9.6.1179

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/neuron).
