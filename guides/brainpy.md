# BrainPy

> Simulate spiking brain-dynamics models compiled with JAX; the example is a small excitatory-inhibitory network of leaky integrate-and-fire neurons.

Licence: GPL-3.0 · [Source code](https://github.com/brainpy/BrainPy)

## What it simulates

BrainPy is a Python framework for brain dynamics models. It covers spiking neuron networks, firing-rate models and neural-mass models, plus tools for training and for analysing low-dimensional dynamics. Models are written as Python classes whose update step is compiled with JAX (just-in-time), so the same code runs on CPU, GPU or TPU.

The built-in library, `brainpy.dyn`, has neuron models such as leaky integrate-and-fire (`LifRef`), synapse models (exponential, alpha), projections that wire populations together, and a runner (`DSRunner`) that steps the model and records monitors. A model is a `DynamicalSystem`: you define its parts in `__init__` and one time step in `update`.

BrainPy 2.8 sits inside a newer family of packages ("BrainX"); the classic `brainpy.dyn` API used here is still part of the 2.8.2 package.

## When to use it

Use BrainPy when you want to write your own network model in Python and have the loop compiled for speed, or when you need to fit or train a dynamical model with gradients.

- Use [Brian 2](brian2.md) for equation-string models and wide documentation.
- Use [NEST](nest.md) for the largest spiking networks from a validated model library.
- Use [Norse](norse.md) for PyTorch-based spiking networks.

## Install

BrainPy 2.8.2 (July 2026) is the current release on PyPI. It requires Python 3.11 or later. There is no conda-forge package.

```
pip install brainpy -U
pip install brainpy[cpu] -U     # CPU only
```

Other extras: `[cuda12]`, `[cuda13]` and `[tpu]` for accelerators. The package pulls in `jax`, `brainstate`, `brainunit`, `braintools`, `brainevent` and `brainpy_state`. The README also describes a Binder environment and `pip install BrainX` for the whole ecosystem. The licence is GPL-3.0.

## Run the tested example

This recipe builds BrainPy in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 21 s. BrainPy has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [brainpy-recipe.tar.gz](https://biosimhub.pages.dev/guides/brainpy/brainpy-recipe.tar.gz) (Dockerfile, run_brainpy.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf brainpy-recipe.tar.gz
   cd brainpy
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/brainpy:2.8.2 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/brainpy:2.8.2 python /opt/run_brainpy.py --excitatory 800 \
    --inhibitory 200 --duration 100 --current 20 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `rates.csv` | 75 B |
| `run_log.txt` | 46 B |
| `spikes.csv` | 47.3 KB |

<details><summary>First lines of <code>rates.csv</code></summary>

```
population,neurons,spikes,mean_rate_hz
E,800,3261,40.76
I,200,897,44.85
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 1000 steps, 3261 E spikes, 897 I spikes
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
population,neuron,time_ms
E,413,0.0
E,636,0.0
E,746,0.0
E,756,0.0
E,399,0.4
E,348,0.7
E,742,0.8
E,434,1.0
E,74,1.2
E,95,1.2
E,282,1.3
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--excitatory` | Excitatory neurons | 800 | 10 to 4000 |
| `--inhibitory` | Inhibitory neurons | 200 | 5 to 1000 |
| `--duration` | Simulated time (ms) | 100 | 1 to 1000 |
| `--current` | Constant input to every neuron | 20 | 0 to 100 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the repository notebook [Simulating a Brain Dynamics Model](https://github.com/brainpy/BrainPy/blob/main/docs/quickstart/simulation.ipynb): an excitatory-inhibitory (E-I) balanced network of leaky integrate-and-fire neurons.

```python
import brainpy as bp
import brainpy.math as bm

bm.set_platform('cpu')

class Exponential(bp.Projection):
    def __init__(self, pre, post, delay, prob, g_max, tau, E):
        super().__init__()
        self.pron = bp.dyn.FullProjAlignPost(
            pre=pre, delay=delay,
            comm=bp.dnn.EventCSRLinear(bp.conn.FixedProb(prob, pre=pre.num, post=post.num), g_max),
            syn=bp.dyn.Expon(size=post.num, tau=tau),
            out=bp.dyn.COBA(E=E), post=post)

class EINet(bp.DynamicalSystem):
    def __init__(self, ne=3200, ni=800):
        super().__init__()
        self.E = bp.dyn.LifRef(ne, V_rest=-60., V_th=-50., V_reset=-60., tau=20., tau_ref=5.,
                               V_initializer=bp.init.Normal(-55., 2.))
        self.I = bp.dyn.LifRef(ni, V_rest=-60., V_th=-50., V_reset=-60., tau=20., tau_ref=5.,
                               V_initializer=bp.init.Normal(-55., 2.))
        self.E2E = Exponential(self.E, self.E, 0., 0.02, 0.6, 5., 0.)
        self.E2I = Exponential(self.E, self.I, 0., 0.02, 0.6, 5., 0.)
        self.I2E = Exponential(self.I, self.E, 0., 0.02, 6.7, 10., -80.)
        self.I2I = Exponential(self.I, self.I, 0., 0.02, 6.7, 10., -80.)

    def update(self, inp=0.):
        self.E2E(); self.E2I(); self.I2E(); self.I2I()
        self.E(inp); self.I(inp)
        return self.E.spike.value, self.I.spike.value

net = EINet()
runner = bp.DSRunner(net, monitors=['E.spike', 'I.spike'])
runner.run(inputs=bm.ones(1000) * 20.)   # 100 ms
E_sps = runner.mon['E.spike']
I_sps = runner.mon['I.spike']
```

The network has 3200 excitatory and 800 inhibitory neurons, 2 percent random connectivity, and a constant input of 20 to every neuron. The notebook marks 1000 steps as 100 ms, which means a 0.1 ms time step.

## Reading the output

- **`runner.mon['E.spike']`** is a 0/1 array of shape (time steps, neurons). A one at (t, k) means neuron k fired at step t. Multiply the step index by `bm.get_dt()` to get milliseconds.
- **Raster.** Plot the positions of the ones as dots, time on the x axis and neuron on the y axis, to get a spike raster. An E-I balanced network is meant to fire irregularly and asynchronously.
- **Rate.** Total spikes divided by neurons and by the duration in seconds gives the mean firing rate per population.

The recipe uses the same model with 800 excitatory and 200 inhibitory neurons by default and writes `spikes.csv` (population, neuron, time in ms) and `rates.csv` (spikes and mean rate per population). The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **Two API generations.** The README links a newer state-based API in the BrainX packages (`brainpy.state`) and migration notes. Tutorials for the classic `brainpy.dyn` API and for the new one do not mix. Match the tutorial to the package.
- **First call is slow.** JAX compiles the model on the first run. Later runs of the same shape are fast.
- **Array shape and dtype.** JAX arrays are immutable and use 32-bit floats by default. Use `bm` functions rather than NumPy in model code.
- **Seeds.** Set `bm.random.seed(n)` for repeatable runs.
- **Time unit.** The default `dt` is 0.1 ms. Check `bm.get_dt()` before converting steps to time.

## Further reading

- Source and README: https://github.com/brainpy/BrainPy
- Documentation: https://brainpy.readthedocs.io/
- Ecosystem: https://brainx.chaobrain.com
- Paper: Wang C, Zhang T, Chen X, He S, Li S, Wu S (2023). BrainPy, a flexible, integrative, efficient, and extensible framework for general-purpose brain dynamics programming. eLife 12:e86365. https://doi.org/10.7554/eLife.86365

---

Cite: Wang C, Zhang T, Chen X, He S, Li S, Wu S (2023). BrainPy, a flexible, integrative, efficient, and extensible framework for general-purpose brain dynamics programming. eLife 12:e86365. doi:10.7554/eLife.86365

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/brainpy).
