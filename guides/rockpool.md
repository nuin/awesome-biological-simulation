# Rockpool

> Build, simulate and train spiking and rate neural networks in Python, with layers that map onto neuromorphic hardware.

Licence: AGPL-3.0 · [Source code](https://github.com/synsense/rockpool)

## What it simulates

Rockpool is a Python package for building, simulating and training small spiking and rate-based neural networks. It targets signal-processing tasks, and it can deploy trained networks on event-driven neuromorphic hardware from SynSense. The project states that it is not designed for detailed simulation of biological networks.

A network is a tree of `Module` objects, in the style of PyTorch. Each module holds parameters (weights, time constants), state (membrane voltage, synaptic current) and simulation parameters (time step). You call a module on an array of shape (time steps, channels) and get back the output, the new state and optionally recorded state.

Layers exist for several backends: plain NumPy, Torch, JAX, Brian2 and Numba. The NumPy layers need nothing beyond NumPy and SciPy.

## When to use it

Use Rockpool to design a spiking network for a signal task, train it with gradients through Torch or JAX, and export it to hardware.

- Use [Auryn](auryn.md) when you want a fast C++ simulator for plastic recurrent networks.
- Use [Brian2CUDA](brian2cuda.md) or Brian 2 when you want to write neuron models as differential equations.
- Use [LFPy](lfpy.md) when you need detailed multicompartment neurons and extracellular potentials.

## Install

Rockpool 3.1.0 is the current release on PyPI and conda-forge. Python 3.10 or newer is required.

```bash
pip install rockpool
```

Or, from conda-forge:

```bash
conda install -c conda-forge rockpool
```

Extras for Torch, JAX and Brian2 layers come with `pip install rockpool[all]`. Without them the rest of the package still works. The licence is AGPL-3.0, and the README says commercial licences are available on request.

The recipe below installs the conda-forge package plus SciPy and runs a layer of NumPy LIF neurons. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds Rockpool in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.6 s.

1. Download [rockpool-recipe.tar.gz](https://biosimhub.pages.dev/guides/rockpool/rockpool-recipe.tar.gz) (Dockerfile, run_rockpool.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf rockpool-recipe.tar.gz
   cd rockpool
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/rockpool:3.1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/rockpool:3.1.0 python /opt/run_rockpool.py --neurons 8 --steps 1000 \
    --dt 0.001 --input-scale 0.3 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 51 B |
| `spikes.csv` | 242.2 KB |
| `summary.csv` | 150 B |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
neurons=8 steps=1000 dt=0.001 spikes=22547 seed=42
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
time_s,neuron
0.002000,2
0.002000,3
0.002000,5
0.002000,6
0.003000,0
0.003000,4
0.003000,5
0.003000,7
0.004000,0
0.004000,1
0.004000,2
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
neuron,spikes,rate_hz
0,2779,2779.000
1,2851,2851.000
2,2797,2797.000
3,2842,2842.000
4,2851,2851.000
5,2804,2804.000
6,2876,2876.000
7,2747,2747.000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--neurons` | Neurons in the LIF layer | 8 | 1 to 500 |
| `--steps` | Time steps | 1000 | 10 to 20000 |
| `--dt` | Time step (s) | 0.001 | 1e-05 to 0.01 |
| `--input-scale` | Input current scale (uniform random 0 to this value) | 0.3 | 0 to 10 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the [Introduction to Rockpool](https://rockpool.ai/basics/getting_started.html) tutorial. It builds four rate neurons and pushes noise through them:

```python
import numpy as np
from rockpool.nn.modules import Rate

N = 4
mod = Rate(N)
print(mod.state())
print(mod.parameters())

T = 100
input_clocked = np.random.randn(T, N) * 3
output_clocked, new_state, recorded_state = mod(input_clocked)
mod = mod.set_attributes(new_state)
```

The tutorial then composes a network with `Sequential`:

```python
from rockpool.nn.modules import Linear, Rate
from rockpool.nn.combinators import Sequential

seqmod = Sequential(Linear((1, 10)), Rate(10), Linear((10, 1)))
output, state, _ = seqmod(np.random.rand(1000, 1))
```

## Reading the output

- The output array has shape (1, T, N): one batch, T time steps, N neurons. Plot `output[0]` to see one trace per neuron.
- The tutorial shows the initial state of the four-neuron module as `{'x': array([0., 0., 0., 0.])}` and a membrane time constant `tau` of 0.02 s with a time step `dt` of 0.001 s. Those values come from the tutorial.
- `new_state` must be written back with `set_attributes`, or the next call starts from the old state.
- For a spiking layer such as `LIF`, the output counts spikes per time step. Neurons share a resting potential of 0, have individual thresholds and use subtractive reset.
- The recipe's helper writes `spikes.csv` (one row per spike with time and neuron) and `summary.csv` (spike count and rate per neuron).

## Pitfalls

- **State does not persist unless you keep it.** Reassign `mod` from `set_attributes(new_state)` between calls.
- **Input shape matters.** Clocked data is (T, N), or (batches, T, N).
- **Training needs an extra backend.** Install Torch or JAX and use the matching module classes, for example `LIFTorch` or `LIFJax`.
- **Time steps are in seconds.** Default `dt` is 1 ms, and time constants share that unit.
- **AGPL-3.0 applies to code that links to it.** Check the terms before shipping a product.

## Further reading

- Documentation: https://rockpool.ai
- Installation page: https://rockpool.ai/basics/installation.html
- Source: https://github.com/synsense/rockpool
- Citation: Muir DR, Bauer FC, Weidel P, et al. Rockpool Documentation. Zenodo. https://doi.org/10.5281/zenodo.3773845

---

Cite: Muir DR, Bauer FC, Weidel P, et al. Rockpool Documentation. Zenodo. doi:10.5281/zenodo.3773845

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/rockpool).
