# NGC-Learn

> Simulate a spiking leaky integrate-and-fire neuron in the JAX-based ngc-learn library and record its membrane potential and spikes under a step current.

Licence: BSD-3-Clause · [Source code](https://github.com/NACLab/ngc-learn)

## What it simulates

NGC-Learn is a Python library for building neural circuits out of components and stepping them through time. The components cover spiking neurons (leaky integrate-and-fire, Izhikevich, adaptive exponential, Hodgkin-Huxley), rate cells, error cells, and synapses with local learning rules such as Hebbian updates and spike-timing-dependent plasticity (STDP). It also covers predictive-coding circuits, where layers pass predictions down and prediction errors up.

The library runs on JAX. A model is a `Context` that holds components, wired together, plus `MethodProcess` objects that name the order in which their methods run each step. You write the loop that feeds inputs and reads states. Time advances in steps of a size `dt` that you choose, in milliseconds.

The learning rules are local: a synapse updates from the activity of the two cells it joins, with no backpropagation through the whole network. That is the point of the library. It is built to test biologically motivated learning, not to train the largest possible network.

## When to use it

Use NGC-Learn for small to medium circuits where the learning rule is the subject: STDP variants, reward-modulated plasticity, predictive coding, spiking classifiers built from a few populations.

- Use [Arbor](arbor.md) or [NetPyNE](netpyne.md) when the cells need morphology and ion-channel detail.
- Use [The Virtual Brain](tvb.md) when the nodes are whole brain regions linked by a connectome.
- Use [Simbrain](simbrain.md) to build and watch a small network by hand in a desktop window.

## Install

The package is on PyPI. The current version is 3.2.3 (the PyPI JSON API lists it).

```
pip install ngclearn
```

The project README says versions 3.2.3 and later need Python 3.12 or newer and ngcsimlib 3.1.1 or newer (pip pulls it in). PyPI metadata still says Python 3.10 or newer, so use 3.12 to match the README. Without a CUDA build of JAX, pip installs the CPU version. Plotting needs Matplotlib and imageio. Some tutorials also need scikit-learn.

Conda-forge has no `ngclearn` package, so there is no conda route. Use a virtual environment.

## Run the tested example

This recipe builds NGC-Learn in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.7 s.

1. Download [ngclearn-recipe.tar.gz](https://biosimhub.pages.dev/guides/ngclearn/ngclearn-recipe.tar.gz) (Dockerfile, run_lif.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf ngclearn-recipe.tar.gz
   cd ngclearn
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/ngclearn:3.2.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/ngclearn:3.2.3 python /opt/run_lif.py --amplitude 0.3 --steps 200 \
    --dt 0.1 --tau-m 100 --seed 1234 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `lif_plot.jpg` | 35.9 KB |
| `lif_trace.csv` | 9.5 KB |
| `run_log.txt` | 43 B |

<details><summary>First lines of <code>lif_trace.csv</code></summary>

```
step,time_ms,current,v_mV,spike
0,0.0,0.0,-65.0,0
1,0.1,0.0,-65.0,0
2,0.2,0.0,-65.0,0
3,0.3,0.0,-65.0,0
4,0.4,0.0,-65.0,0
5,0.5,0.0,-65.0,0
6,0.6,0.0,-65.0,0
7,0.7,0.0,-65.0,0
8,0.8,0.0,-65.0,0
9,0.9,0.0,-65.0,0
10,1.0,0.30000001192092896,-64.69999694824219,0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
steps=200 amplitude=0.3 spikes=3 seed=1234
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--amplitude` | Step current after 10 steps | 0.3 | 0 to 5 |
| `--steps` | Simulation steps | 200 | 20 to 5000 |
| `--dt` | Integration step (ms) | 0.1 | 0.01 to 1 |
| `--tau-m` | Membrane time constant tau_m | 100 | 1 to 1000 |
| `--seed` | Seed | 1234 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

The example is the leaky integrate-and-fire (LIF) lesson from the ngc-learn tutorials. One LIF cell gets no current for 10 steps, then a constant current. The code builds the cell in a `Context`, defines `advance` and `reset` processes, loops over the time steps while clamping the input current, and records the membrane potential `v` and the spike `s`.

The cell uses `thr=-52` mV, `v_rest=-65` mV, `v_reset=-60` mV, `tau_m=100` and `dt=0.1` ms. The tutorial's default input after step 10 is 0.3, run for 200 steps in total.

Adapted from <https://ngc-learn.readthedocs.io/en/latest/tutorials/neurocog/lif.html>.

## Reading the output

The tutorial ends with `plot_spiking_neuron`, which saves one figure with three stacked panels: the input current, the membrane potential `v` with the threshold line, and the spike raster. The recipe's driver script also writes the same arrays as a CSV (step, time in ms, current, voltage, spike flag).

What to expect from the model, not from a recorded run:

- Before step 10, the current is zero and `v` sits at the resting potential.
- After the step, `v` climbs toward threshold. When it crosses `thr`, the cell emits a spike (`s` = 1 for that step) and `v` goes to `v_reset`.
- After a spike, the cell is silent for `refract_time` (2 ms in the example).
- The cell has an adaptive threshold. `theta_plus` raises the effective threshold after each spike and `tau_theta` sets how fast it relaxes, so the interval between spikes can lengthen.

Raise the current and the spike rate rises. Lower it below the level needed to reach threshold and the cell never fires.

## Pitfalls

- **Version and Python.** Python 3.12 is the documented floor for 3.2.3. Older Python may install but is not what the README states.
- **JAX on GPU.** The default pip install gives the CPU build. The README warns that CUDA 12 with JAX newer than 0.4.28 on Pascal-generation GPUs and driver 580 or newer needs `nvidia-cudnn-cu12==9.10.2.21` pinned.
- **Keys, not seeds.** JAX random numbers come from explicit keys (`random.PRNGKey(1234)`), split for each component. Reuse the same key and you get the same draws. Pass a distinct subkey to each component.
- **The simplified LIF is a different cell.** `SLIFCell` normalises voltage to non-negative values and has built-in lateral inhibition. `LIFCell` uses millivolt values and has neither. Parameters do not transfer between them.
- **Compile on first call.** JAX compiles on the first step, so the first loop iteration is slow and later ones are fast.
- **Legacy code.** The older TensorFlow version is a separate repository, ngc-learn-legacy. Its API differs.

## Further reading

- Documentation and tutorials: https://ngc-learn.readthedocs.io/
- Source: https://github.com/NACLab/ngc-learn
- Model museum (historical models): https://github.com/NACLab/ngc-museum
- Paper: Ororbia A, Kifer D (2022). The neural coding framework for learning generative models. Nature Communications 13:2064. https://doi.org/10.1038/s41467-022-29632-7

---

Cite: Ororbia A, Kifer D (2022). The neural coding framework for learning generative models. Nature Communications 13:2064. doi:10.1038/s41467-022-29632-7

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/ngclearn).
