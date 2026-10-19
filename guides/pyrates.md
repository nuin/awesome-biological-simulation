# PyRates

> Generate and run code for neural mass, rate-based and other dynamical systems models defined as graphs of differential equations.

Licence: GPL-3.0 · [Source code](https://github.com/pyrates-neuroscience/PyRates)

## What it simulates

PyRates generates and runs code for dynamical systems models. You describe a model as a graph: nodes hold differential and algebraic equations, edges carry coupling between nodes, and networks can nest. PyRates turns the graph into a vector field function for a chosen backend and integrates it.

It was built for neural mass and rate-based models of brain populations, and it ships pre-implemented models such as the Jansen-Rit neural mass model. Any system of ordinary differential equations can be written in the same form.

Backends listed in the project README:

- NumPy for CPU runs in Python (the default).
- TensorFlow and PyTorch for GPU runs and gradient-based parameter fitting.
- Julia, with tools such as DifferentialEquations.jl.
- Fortran, with an interface to the continuation software Auto-07p.
- MATLAB for differential equation solving.

Edges can carry scalar delays or delay distributions. Delay distributions are translated into gamma-kernel convolutions.

## When to use it

Use PyRates for population-level models, parameter sweeps and bifurcation analysis, where spikes are not simulated individually.

- Use [Auryn](auryn.md) or [Rockpool](rockpool.md) when you want individual spiking neurons.
- Use [HNN-core](hnn-core.md) when you want a detailed column model whose output is a MEG/EEG dipole.
- Use [DynaSim](dynasim.md) when you work in MATLAB and want to define small neural ODE models from text equations.

## Install

PyRates 1.2.3 (released 2026-06-12) is on PyPI as a pure Python wheel. It is not on conda-forge.

```bash
pip install pyrates
```

Optional packages come in groups: `pip install pyrates[backends]` adds Torch, JAX and Diffrax, and `pip install pyrates[all]` adds everything. The licence is GPL-3.0.

The recipe below installs the PyPI wheel into a Python 3.12 image and runs the Jansen-Rit example. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds PyRates in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.6 s.

1. Download [pyrates-recipe.tar.gz](https://biosimhub.pages.dev/guides/pyrates/pyrates-recipe.tar.gz) (Dockerfile, run_pyrates.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pyrates-recipe.tar.gz
   cd pyrates
   sh run.sh
   ```

![Terminal recording of the PyRates example run](https://biosimhub.pages.dev/media/pyrates/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pyrates:1.2.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pyrates:1.2.3 python /opt/run_pyrates.py --time 2 --step 0.0001 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `jansen_rit.csv` | 695.4 KB |
| `run_log.txt` | 575 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/pyrates/result-dark.png"><img src="https://biosimhub.pages.dev/media/pyrates/result.png" alt="Plot of the PyRates example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>jansen_rit.csv</code></summary>

```
,psp_e,psp_i
0.0,0.0,0.0
0.0001,0.0,0.0
0.0002,7.73914e-07,-6.231286e-08
0.00030000000000000003,2.3062637e-06,-1.8631545e-07
0.0004,4.581805e-06,-3.7138994e-07
0.0005,7.5855264e-06,-6.169238e-07
0.0006000000000000001,1.1302643e-05,-9.2230954e-07
0.0007,1.5718595e-05,-1.286945e-06
0.0008,2.0819047e-05,-1.7102329e-06
0.0009000000000000001,2.658988e-05,-2.1915814e-06
0.001,3.301719e-05,-2.7304031e-06
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Compilation Progress
--------------------
	(1) Translating the circuit template into a networkx graph representation...
		...finished.
	(2) Preprocessing edge transmission operations...
		...finished.
	(3) Parsing the model equations into a compute graph...
		...finished.
	Model compilation was finished.
Simulation Progress
-------------------
	 (1) Generating the network run function...
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--time` | Simulated time (s) | 2 | 0.1 to 20 |
| `--step` | Integration step (s) | 0.0001 | 1e-05 to 0.001 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the [PyRates documentation example](https://pyrates.readthedocs.io/en/latest/simple_example.html). It integrates the Jansen-Rit model over 2 s:

```python
from pyrates import integrate

model_def = "model_templates.neural_mass_models.jansenrit.JRC"
results = integrate(model_def, simulation_time=2.0, step_size=1e-4,
                    outputs={'psp_e': 'pc/rpo_e_in/v',
                             'psp_i': 'pc/rpo_i/v'},
                    clear=True)
```

The documentation says `integrate` returns a `pandas.DataFrame` with the resulting time series. `clear=True` deletes the generated run files afterwards.

## Reading the output

- The DataFrame has one row per time point and one column per name in `outputs`, here `psp_e` and `psp_i`. They record the membrane potential at the model nodes named in the `outputs` paths (`pc/rpo_e_in/v` and `pc/rpo_i/v`; the variable name is a lower-case `v`, and an upper-case `V` returns an empty table), which stand for the excitatory and inhibitory post-synaptic potentials.
- The row count depends on the step size and the sampling settings. Check `len(results)` instead of assuming it.
- For the Jansen-Rit model, look for a settling period and then either a steady state or oscillations. The model is known for alpha-like rhythms, and the parameter set decides which you see.
- The recipe helper writes the DataFrame to `jansen_rit.csv`.

## Pitfalls

- **networkx is capped.** PyPI metadata requires `networkx<=3.5`. Pin it if another package pulls in a newer version.
- **Old docs mention Python 3.6.** The package page requires Python 3.8 or newer.
- **Generated code lands in the working directory.** Use `clear=True` or run in a scratch folder.
- **Step size sets stability.** Fixed-step solvers need a step small enough for the fastest time constant in the model.
- **Backend packages are optional.** Torch, JAX and Julia are not installed by default.

## Further reading

- Documentation: https://pyrates.readthedocs.io
- Source: https://github.com/pyrates-neuroscience/PyRates
- Gast R, Knosche TR, Kennedy A (2023). PyRates: a code-generation tool for modeling dynamical systems in biology and beyond. PLoS Comput Biol 19:e1011761. https://doi.org/10.1371/journal.pcbi.1011761
- Gast R, Rose D, Salomon C, Moller HE, Weiskopf N, Knosche TR (2019). PyRates: a Python framework for rate-based neural simulations. PLoS ONE 14:e0225900. https://doi.org/10.1371/journal.pone.0225900

---

Cite: Gast R, Knosche TR, Kennedy A (2023). PyRates: a code-generation tool for modeling dynamical systems in biology and beyond. PLoS Comput Biol 19:e1011761. doi:10.1371/journal.pcbi.1011761

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pyrates).
