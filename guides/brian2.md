# Brian 2

> Simulate spiking neurons written as differential equations (leaky integrate-and-fire with a threshold and reset) and record spike times and a voltage trace.

Licence: CECILL-2.1 · [Source code](https://github.com/brian-team/brian2)

## What it simulates

Brian 2 simulates networks of spiking neurons that you describe as differential equations. You write the model as a short text string, such as `dv/dt = (1-v)/tau : 1`. Brian parses the equations, picks a numerical integrator and generates code to run them.

The unit of work is a `NeuronGroup`: N identical neurons that share equations, a spike threshold and a reset rule. You add `Synapses` between groups, input generators such as `PoissonGroup`, and monitors that record spikes or state variables. The simulator is clock-driven: every neuron updates on each time step (0.1 ms by default).

Brian checks physical units. Adding amps to volts raises a `DimensionMismatchError` before the run starts, which catches many model typos.

## When to use it

Use Brian 2 when you want to try a neuron or synapse model that is not in a fixed library. You change the equations, not the simulator. It suits teaching, single-lab studies and networks up to a few hundred thousand neurons on one machine.

- Use [NEST](nest.md) for very large networks from a fixed set of point-neuron models, with multi-core or MPI scaling.
- Use [NEURON](neuron.md) when the model needs dendrites, ion channels and cable theory.
- Use [Nengo](nengo.md) when you want to compute with neurons: it decodes represented values from spiking activity.

## Install

Brian 2.10.1 is the current release. It needs Python 3.12 or later. Both routes below exist for that version.

```
conda install -c conda-forge brian2
```

or, in a virtual environment:

```
pip install brian2
```

The Brian installation page recommends a separate environment. By default Brian tries to compile generated code with Cython and falls back to numpy. On a machine without a compiler, or where temporary directories cannot run programs, select the plain numpy target: `prefs.codegen.target = 'numpy'`. It is slower but needs nothing else. The recipe below uses it.

## Run the tested example

This recipe builds Brian 2 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.6 s.

1. Download [brian2-recipe.tar.gz](https://biosimhub.pages.dev/guides/brian2/brian2-recipe.tar.gz) (Dockerfile, run_brian2.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf brian2-recipe.tar.gz
   cd brian2
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/brian2:2.10.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/brian2:2.10.1 python /opt/run_brian2.py --neurons 1 --tau 10 \
    --drive 1 --spread 0 --threshold 0.8 --duration 50 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 33 B |
| `spikes.csv` | 46 B |
| `v_neuron0.csv` | 8.2 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 1 neurons, 50 ms, 3 spikes
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
neuron,time_ms
0,16.000
0,32.100
0,48.200
```

</details>

<details><summary>First lines of <code>v_neuron0.csv</code></summary>

```
time_ms,v
0.000,0.000000
0.100,0.009950
0.200,0.019801
0.300,0.029554
0.400,0.039211
0.500,0.048771
0.600,0.058235
0.700,0.067606
0.800,0.076884
0.900,0.086069
1.000,0.095163
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--neurons` | Neurons | 1 | 1 to 2000 |
| `--tau` | Membrane time constant (ms) | 10 | 1 to 200 |
| `--drive` | Input drive I (v relaxes toward I) | 1 | 0 to 5 |
| `--spread` | Relative spread of the drive across neurons | 0 | 0 to 1 |
| `--threshold` | Spike threshold on v | 0.8 | 0.01 to 5 |
| `--duration` | Simulated time (ms) | 50 | 1 to 2000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Brian 2 tutorial [Introduction to Brian part 1: Neurons](https://brian2.readthedocs.io/en/stable/resources/tutorials/1-intro-to-brian-neurons.html).

```python
from brian2 import *

start_scope()
tau = 10*ms
eqs = '''
dv/dt = (1-v)/tau : 1
'''
G = NeuronGroup(1, eqs, threshold='v>0.8', reset='v = 0', method='exact')
M = StateMonitor(G, 'v', record=0)
spikemon = SpikeMonitor(G)
run(50*ms)
print('Spike times: %s' % spikemon.t[:])
plot(M.t/ms, M.v[0])
xlabel('Time (ms)'); ylabel('v')
show()
```

The neuron's `v` relaxes toward 1 with a time constant of 10 ms. When `v` passes 0.8, Brian records a spike and sets `v` back to 0. The tutorial prints spike times of 16, 32.1 and 48.2 ms for this model.

## Reading the output

- **`SpikeMonitor`** stores `i` (neuron index) and `t` (spike time) for every spike. `spikemon.t[:]` is an array with units; divide by `ms` for plain numbers. `spikemon.count` gives spikes per neuron.
- **`StateMonitor`** stores the time axis `M.t` and the recorded variable `M.v`, one row per recorded neuron. You choose the neurons with `record=`. Recording every neuron of a large group uses a lot of memory.
- A voltage trace for this model rises along `1 - exp(-t/tau)`, drops to 0 at each spike and rises again. The tutorial overlays the analytic curve on the simulated one, and the two coincide.

In the recipe, the same model writes `spikes.csv` (neuron, time in ms) and `v_neuron0.csv` (time and `v` for neuron 0). The recipe's defaults match the tutorial model, so the spike times should match the tutorial values above. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **Units.** Quantities need units (`10*ms`). A bare `10` in a place that expects a time raises an error. Dimensionless variables are declared `: 1`.
- **`start_scope()`.** In notebooks, call it at the start of each cell that builds a model. Otherwise objects from earlier cells join the new run.
- **Integrator choice.** `method='exact'` works only for linear equations. Brian picks a method itself when you leave `method` out, and prints a note if it falls back to a less accurate one.
- **Seeds.** Call `seed(n)` before building the network for reproducible random numbers. Code generation targets can give slightly different floating-point results.
- **Clock-driven cost.** Cost grows with neurons times time steps. A tiny `dt` over a long run is slow.

## Further reading

- Documentation: https://brian2.readthedocs.io/
- Installation: https://brian2.readthedocs.io/en/stable/introduction/install.html
- Source: https://github.com/brian-team/brian2
- Forum: https://brian.discourse.group
- Paper: Stimberg M, Brette R, Goodman DFM (2019). Brian 2, an intuitive and efficient neural simulator. eLife 8:e47314. https://doi.org/10.7554/eLife.47314

---

Cite: Stimberg M, Brette R, Goodman DFM (2019). Brian 2, an intuitive and efficient neural simulator. eLife 8:e47314. doi:10.7554/eLife.47314

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/brian2).
