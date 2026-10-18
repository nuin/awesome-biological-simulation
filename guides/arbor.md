# Arbor

> Simulate a multi-compartment Hodgkin-Huxley neuron with Arbor's single-cell model, driven by a current clamp, and save its voltage trace and spike times.

Licence: BSD-3-Clause · [Source code](https://github.com/arbor-sim/arbor)

## What it simulates

Arbor simulates networks of neurons that have a shape. Each cell is a tree of cylindrical cable segments (a morphology) with ion channels painted on regions of it and synapses, current clamps and detectors placed at points on it. The membrane equations are solved on every compartment of every cell. This is the same class of model as NEURON, but Arbor is built from the start for many cores and for GPUs.

You describe a model as a recipe: how many cells there are, what each cell is, how cells connect, and what to probe. Arbor builds the cells, distributes them over the available hardware, and runs them in time steps. Cell kinds are cable cells (the detailed ones), leaky integrate-and-fire cells, adaptive exponential cells, spike sources and benchmark cells. Quantities carry units in the Python interface: `5 * U.mm` and `5000 * U.um` are the same length, and a wrong dimension raises an error.

## When to use it

Use Arbor for networks of detailed cells that are big enough that run time matters: thousands to millions of cells, cluster or GPU runs, or custom ion channels written in NMODL.

- Use [NetPyNE](netpyne.md) when you want a declarative network description on top of NEURON and a GUI.
- Use [NGC-Learn](ngclearn.md) for point-neuron circuits with local learning rules.
- Use [c302](c302.md) for the C. elegans connectome as a NeuroML model.

## Install

The current release is 0.12.2 (PyPI, and a GitHub release with sources and wheels). The Arbor documentation recommends pip in a virtual environment:

```
python -m venv arbor_env
source arbor_env/bin/activate
pip install arbor
```

Check the install with `import arbor as A; A.print_config()`, which prints the version and the enabled features. PyPI carries binary wheels for Linux x86-64 and macOS on Apple Silicon, for Python 3.11 to 3.14. On any other platform pip builds from source, which needs git, cmake and a C++ compiler. The documentation lists `git cmake gcc python3-dev python3-pip` for Ubuntu and Debian.

There is no Arbor package on conda-forge. For the C++ library, MPI and GPU builds, see the "Build and install from source" and "Spack Installation" pages.

## Run the tested example

This recipe builds Arbor in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 20.2 s. Arbor has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [arbor-recipe.tar.gz](https://biosimhub.pages.dev/guides/arbor/arbor-recipe.tar.gz) (Dockerfile, run_arbor.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf arbor-recipe.tar.gz
   cd arbor
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/arbor:0.12.2 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/arbor:0.12.2 python /opt/run_arbor.py --amplitude 0.8 --start 10 \
    --duration 2 --tfinal 30 --vinit -40 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 20 B |
| `spikes.csv` | 35 B |
| `voltage.csv` | 8.7 KB |
| `voltage.png` | 15.5 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
1 spikes: 10.084 ms
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
spike_time_ms
10.083560309485517
```

</details>

<details><summary>First lines of <code>voltage.csv</code></summary>

```
time_ms,v_mV
0.0,-40.0
0.1,-54.021164627078704
0.2,-61.967053369443846
0.30000000000000004,-67.36853032854215
0.4,-70.99315652576946
0.5,-73.19028152473564
0.6000000000000001,-74.41462623596593
0.7000000000000001,-75.06632843087247
0.8,-75.40282495205821
0.9,-75.5681959664753
1.0,-75.6395475611173
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--amplitude` | Clamp current (nA) | 0.8 | 0 to 5 |
| `--start` | Clamp start (ms) | 10 | 0 to 500 |
| `--duration` | Clamp duration (ms) | 2 | 0.1 to 500 |
| `--tfinal` | Simulated time (ms) | 30 | 5 to 1000 |
| `--vinit` | Initial membrane potential (mV) | -40 | -90 to 0 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

The tutorial "A simple single-cell model" models a cylindrical cell of 6 um length and 3 um radius, with Hodgkin-Huxley dynamics and a current clamp, for 30 ms. The steps are:

1. Build a morphology of one segment (a `segment_tree`).
2. Name regions and points with a `label_dict`: `"soma"` is `(tag 1)` and `"midpoint"` is `(location 0 0.5)`.
3. Build a `decor`: initial voltage -40 mV, `hh` channels painted on the soma, a 0.8 nA clamp that starts at 10 ms and lasts 2 ms, and a spike detector at -10 mV.
4. Join the three into an `A.cable_cell` and wrap it in `A.single_cell_model`.
5. Add a voltage probe at 10 kHz and call `m.run(tfinal=30 * U.ms)`.
6. Read `m.spikes` and `m.traces`.

The full code is `python/examples/single_cell_model.py` in the repository, about ten lines of model code. The recipe's driver script follows these steps and writes the results to files.

Adapted from <https://docs.arbor-sim.org/en/latest/tutorial/single_cell_model.html>.

## Reading the output

`m.spikes` is a list of spike times in ms. The tutorial says a single spike should appear around the time the stimulus starts, at 10 ms. `m.traces[0]` holds the probe data: `.time` in ms and `.value` in mV. The tutorial plots them as membrane potential against time.

The recipe saves the trace as `voltage.csv` (two columns: time and voltage), the spike times as `spikes.csv` and a plot as `voltage.png`. The trace shows the resting level near the initial potential, a rise when the clamp turns on and, if the current is strong enough, the sharp rise and fall of an action potential. Lower the clamp amplitude and the spike disappears; the response then stays below threshold.

## Pitfalls

- **Units are mandatory.** Pass `0.8 * U.nA`, not `0.8`. A mismatched dimension, such as millivolts where a current belongs, is rejected at run time. The tutorial states this.
- **Quote the labels.** Region and location names are passed as quoted strings inside strings: `'"soma"'`.
- **Platform wheels.** No wheel exists for Linux on ARM or for Intel Macs, so pip builds from source there and needs a compiler and cmake.
- **API differences.** The unit-based interface in the current tutorial is newer than many examples online. Older code that passes bare numbers will fail on 0.12.
- **Detailed cells cost time.** A cable cell is discretised into compartments. Use the discretisation controls only after the model works.
- **Recipes, not scripts.** The single-cell model hides the recipe. Networks need an `A.recipe` subclass, the domain decomposition and `A.simulation`; the "A ring network" tutorial shows the pattern.

## Further reading

- Documentation: https://docs.arbor-sim.org/
- Python installation: https://docs.arbor-sim.org/en/latest/install/python.html
- Tutorials: https://docs.arbor-sim.org/en/latest/tutorial/index.html
- Source: https://github.com/arbor-sim/arbor
- Paper: Abi Akar N et al. (2019). Arbor, a morphologically-detailed neural network simulation library for contemporary high-performance computing architectures. 27th Euromicro International Conference on Parallel, Distributed and Network-Based Processing (PDP), pp 274-282. https://doi.org/10.1109/EMPDP.2019.8671560

---

Cite: Abi Akar N, et al. (2019). Arbor, a morphologically-detailed neural network simulation library for contemporary high-performance computing architectures. 27th Euromicro PDP, pp 274-282. doi:10.1109/EMPDP.2019.8671560

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/arbor).
