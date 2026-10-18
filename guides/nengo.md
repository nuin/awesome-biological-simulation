# Nengo

> Build a Neural Engineering Framework model in Python; the example passes a sine wave through two spiking ensembles and decodes it back.

Licence: GPL-2.0-only · [Source code](https://github.com/nengo/nengo)

## What it simulates

Nengo builds neural models with the Neural Engineering Framework (NEF). You do not set every synapse. You say what a group of neurons should represent (a number, a vector) and what computation connections should perform. Nengo then solves for the connection weights so that the spiking activity of one ensemble approximates the function you asked for.

The parts are `Node` (an input or output signal), `Ensemble` (a population of neurons that represents a vector), `Connection` (a link that can apply a function) and `Probe` (a recorder). The same model runs on the reference simulator in Python, on GPUs with NengoDL and on neuromorphic hardware through backends such as NengoLoihi. The large Spaun brain model was built with it.

## When to use it

Use Nengo when the question is "what can this network compute", for example integrating a signal, holding a memory or running a small cognitive model, and you want spiking neurons doing the work.

- Use [Brian 2](brian2.md) when you need to define the neuron or synapse equations yourself.
- Use [NEST](nest.md) for large spiking networks built from a fixed model library.
- Use [Norse](norse.md) or [BrainPy](brainpy.md) when you want gradient-based training or JAX compilation.

## Install

Nengo 4.1.0 is the current release. It is on PyPI (Python 3.8 or later) and conda-forge (noarch).

```
pip install nengo
```

or

```
conda install -c conda-forge nengo
```

Nengo's only required dependency is NumPy. SciPy, scikit-learn and matplotlib are optional; matplotlib is needed to plot as in the examples.

The licence file in the repository is the GNU General Public License version 2, with no "or later" clause (SPDX GPL-2.0-only). The conda-forge package labels it with a custom Nengo licence reference.

## Run the tested example

This recipe builds Nengo in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.1 s.

1. Download [nengo-recipe.tar.gz](https://biosimhub.pages.dev/guides/nengo/nengo-recipe.tar.gz) (Dockerfile, run_nengo.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf nengo-recipe.tar.gz
   cd nengo
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/nengo:4.1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/nengo:4.1.0 python /opt/run_nengo.py --neurons 100 --freq 0.159 \
    --duration 2 --synapse 0.01 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `decoded.csv` | 60.6 KB |
| `run_log.txt` | 47 B |
| `summary.csv` | 61 B |

<details><summary>First lines of <code>decoded.csv</code></summary>

```
time_s,input,decoded_A,decoded_B
0.001,0.00100,0.00000,0.00000
0.002,0.00200,-0.01429,0.00624
0.003,0.00300,0.00750,0.01915
0.004,0.00400,0.00445,0.00684
0.005,0.00500,-0.00031,-0.01223
0.006,0.00599,0.01413,-0.03081
0.007,0.00699,0.01244,0.01314
0.008,0.00799,0.01028,0.01338
0.009,0.00899,0.00373,0.01902
0.010,0.00999,0.02669,-0.01692
0.011,0.01099,-0.00886,0.00251
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 2000 steps, rmse A 0.0205, rmse B 0.0256
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
steps,rmse_A_vs_input,rmse_B_vs_input
2000,0.02047,0.02561
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--neurons` | Neurons per ensemble | 100 | 10 to 2000 |
| `--freq` | Input sine frequency (Hz) | 0.159 | 0.01 to 20 |
| `--duration` | Simulated time (s) | 2 | 0.1 to 20 |
| `--synapse` | Probe filter time constant (s) | 0.01 | 0.001 to 0.5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Nengo example [Communication channel](https://www.nengo.ai/nengo/examples/basic/communication-channel.html).

```python
import matplotlib.pyplot as plt
import numpy as np
import nengo

model = nengo.Network(label="Communications Channel")
with model:
    sin = nengo.Node(np.sin)
    A = nengo.Ensemble(100, dimensions=1)
    B = nengo.Ensemble(100, dimensions=1)
    nengo.Connection(sin, A)
    nengo.Connection(A, B)

    sin_probe = nengo.Probe(sin)
    A_probe = nengo.Probe(A, synapse=0.01)
    B_probe = nengo.Probe(B, synapse=0.01)

with nengo.Simulator(model) as sim:
    sim.run(2)

plt.plot(sim.trange(), sim.data[sin_probe], label="input")
plt.plot(sim.trange(), sim.data[A_probe], label="A")
plt.plot(sim.trange(), sim.data[B_probe], label="B")
plt.legend(); plt.show()
```

An input sine wave feeds ensemble A of 100 spiking neurons, and A feeds ensemble B of 100 neurons. The connection from A to B is the "communication channel": it passes the value on unchanged. The simulation covers 2 seconds.

## Reading the output

- **`sim.trange()`** is the time axis, one value per 1 ms step by default.
- **`sim.data[probe]`** is an array of shape (steps, dimensions). For an ensemble probe it is the value decoded from the filtered spikes, not raw spikes. The `synapse=0.01` argument sets a 10 ms low-pass filter on that decoded value.
- **What to expect.** The example text says the plots show the ideal sine input and estimates of it decoded from the spiking activity of A and B. The decoded curves should follow the input with some spiking noise.
- **Spikes.** `nengo.Probe(A.neurons)` records the neuron outputs themselves.

The recipe writes `decoded.csv` (time, input, decoded A, decoded B) and `summary.csv` with the root-mean-square error of each decoded signal against the input. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **Representation range.** An ensemble represents values in a radius of 1 by default. Inputs far outside it saturate. Set `radius` to match your signal.
- **More neurons, less noise.** Decoding error falls as the neuron count rises. Use enough neurons for the precision you need.
- **Seeds.** Set `seed` on the `Network` to get the same neurons and weights each run; without it every build differs.
- **Filters add lag.** Synaptic and probe filters delay and smooth signals. Compare signals with the same filtering.
- **Probe only what you need.** Probing all neurons for long runs uses a lot of memory.

## Further reading

- Documentation: https://www.nengo.ai/nengo/
- Getting started: https://www.nengo.ai/nengo/getting-started.html
- Source: https://github.com/nengo/nengo
- Paper: Bekolay T, et al. (2014). Nengo: a Python tool for building large-scale functional brain models. Front Neuroinform 7:48. https://doi.org/10.3389/fninf.2013.00048

---

Cite: Bekolay T, Bergstra J, Hunsberger E, DeWolf T, Stewart TC, Rasmussen D, Choo X, Voelker A, Eliasmith C (2014). Nengo: a Python tool for building large-scale functional brain models. Front Neuroinform 7:48. doi:10.3389/fninf.2013.00048

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/nengo).
