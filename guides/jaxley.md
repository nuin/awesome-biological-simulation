# Jaxley

> Simulate a Hodgkin-Huxley neuron in JAX on the CPU with a step current and write the membrane-potential trace.

Licence: Apache-2.0 · [Source code](https://github.com/jaxleyverse/jaxley)

## What it simulates

Jaxley simulates biophysical neuron models: cells built from compartments with Hodgkin-Huxley-style ion channels, connected by synapses into networks. It is written in JAX, so a whole simulation is a differentiable function. You can take gradients of an output (a voltage trace, a firing rate) with respect to channel conductances, synaptic weights or morphology parameters, and train them with gradient descent.

A model is built bottom-up from `Compartment`, `Branch`, `Cell` and `Network` objects, or read from an SWC morphology file with `jx.read_swc`. Channels such as `HH`, `Na`, `K` and `Leak` are inserted on whole cells or on chosen branches. Parameters can be shared across groups of compartments. The same code runs on CPU, GPU or TPU, and `jit`-compilation makes repeated runs fast.

## When to use it

Use Jaxley to fit detailed neuron or small-network models to data by gradient, or to run many parameter variants in parallel on a GPU.

- Use NEURON when you need its large library of published mechanisms and the long-standing NMODL ecosystem.
- Use NEST or [PyNN](pynn.md) for large networks of point neurons.
- Use [neurolib](neurolib.md) for population-level whole-brain models.

Jaxley covers the kinds of models listed in its FAQ. A channel not shipped with Jaxley or the companion package `jaxley-mech` has to be written in Python.

## Install

Jaxley 0.14.0 (September 2026) is the current release. The README gives:

```
pip install jaxley
```

This installs JAX for CPU (Python 3.10 or newer), plus matplotlib, numpy, pandas, networkx and tridiax. For a GPU, the README says to install JAX with GPU support in addition, for example `pip install -U "jax[cuda13]"`. Jaxley is not on conda-forge. The licence is Apache-2.0.

## A first run

Adapted from the [Jaxley README](https://github.com/jaxleyverse/jaxley#getting-started), which runs one cell with Hodgkin-Huxley channels and a step current:

```python
import matplotlib.pyplot as plt
from jax import config

import jaxley as jx
from jaxley.channels import HH

config.update("jax_platform_name", "cpu")

cell = jx.Cell()
cell.insert(HH())

current = jx.step_current(i_delay=1.0, i_dur=1.0, i_amp=0.1, delta_t=0.025, t_max=10.0)
cell.stimulate(current)
cell.record("v")

v = jx.integrate(cell)
plt.plot(v.T)
```

The [basics tutorial](https://jaxley.readthedocs.io/en/latest/tutorials/01_morph_neurons.html) also sets `jax_enable_x64` to True, which switches JAX to 64-bit floats. It then builds a multi-branch cell from a `Compartment` and a `Branch`, and inserts `Leak`, `Na` and `K` channels.

## Run the tested example

This recipe builds Jaxley in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 5.8 s.

1. Download [jaxley-recipe.tar.gz](https://biosimhub.pages.dev/guides/jaxley/jaxley-recipe.tar.gz) (Dockerfile, run_jaxley.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf jaxley-recipe.tar.gz
   cd jaxley
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/jaxley:0.14.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/jaxley:0.14.0 python /opt/run_jaxley.py --amp 0.1 --delay 2 \
    --dur 5 --tmax 20 --dt 0.025 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 178 B |
| `voltage.csv` | 39.9 KB |
| `voltage.png` | 28.1 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Added 1 external_states. See `.externals` for details.
Added 1 recordings. See `.recordings` for details.
done: 802 samples of 0.025 ms, peak 47.1 mV, 1 upward crossings of 0 mV
```

</details>

<details><summary>First lines of <code>voltage.csv</code></summary>

```
time_ms,v_mV
0.000000000000000000e+00,-7.000000000000000000e+01
2.500000000000000139e-02,-6.948756081069512902e+01
5.000000000000000278e-02,-6.909088173979448300e+01
7.500000000000001110e-02,-6.877443768415565728e+01
1.000000000000000056e-01,-6.851477492327271079e+01
1.250000000000000000e-01,-6.829603413179125937e+01
1.500000000000000222e-01,-6.810727942222975173e+01
1.750000000000000167e-01,-6.794084395493179329e+01
2.000000000000000111e-01,-6.779127429172092434e+01
2.250000000000000056e-01,-6.765464045577638785e+01
2.500000000000000000e-01,-6.752807602854002766e+01
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--amp` | Step current amplitude (nA) | 0.1 | 0 to 1 |
| `--delay` | Step start (ms) | 2 | 0 to 50 |
| `--dur` | Step length (ms) | 5 | 0.1 to 100 |
| `--tmax` | Duration (ms) | 20 | 5 to 200 |
| `--dt` | Time step (ms) | 0.025 | 0.005 to 0.1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`jx.integrate(cell)` returns a JAX array of the recorded variable with shape (recordings, time steps). In the example, row 0 is the membrane potential of the one recorded compartment in mV, sampled every `delta_t` ms. The time axis is `delta_t` times the sample index. The step current has amplitude `i_amp` in nA, starting at `i_delay` ms and lasting `i_dur` ms.

A cell shows a rest value before the step. A step that is large and long enough produces one or more spikes, each an upstroke above 0 mV followed by a fall below rest. The README does not quote the peak voltages, so check the trace yourself.

For training, wrap `jx.integrate` in a loss function and differentiate it with `jax.grad`. The gradient tutorial in the docs walks through this.

## Pitfalls

- **JAX arrays, not lists.** Results come back as JAX arrays. Convert with `numpy.asarray` before saving.
- **First call compiles.** The first `integrate` triggers compilation. Later calls with the same shapes reuse it.
- **Precision.** The tutorials enable 64-bit floats. Gradient training with 32-bit floats may be less stable.
- **Time step.** The step current and the integration both use `delta_t`. Pass the same value to both.
- **GPU installs.** Installing the matching JAX build for your CUDA version is separate from installing Jaxley.
- **Units.** Time is in ms, voltage in mV, current in nA.

## Further reading

- Documentation: https://jaxley.readthedocs.io/en/latest/
- Tutorials: https://jaxley.readthedocs.io/en/latest/tutorials/01_morph_neurons.html
- Installation: https://jaxley.readthedocs.io/en/latest/installation.html
- Source: https://github.com/jaxleyverse/jaxley
- Paper: Deistler M, Kadhim KL, Pals M, et al. (2025). Jaxley: differentiable simulation enables large-scale training of detailed biophysical models of neural dynamics. Nature Methods 22:2649-2657. https://doi.org/10.1038/s41592-025-02895-w

---

Cite: Deistler M, Kadhim KL, Pals M, et al. (2025). Jaxley: differentiable simulation enables large-scale training of detailed biophysical models of neural dynamics. Nature Methods 22:2649-2657. doi:10.1038/s41592-025-02895-w

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/jaxley).
