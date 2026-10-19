# BindsNET

> A small spiking network in PyTorch, with Poisson inputs driving leaky integrate-and-fire neurons, and recorded spikes and voltage.

Licence: AGPL-3.0 · [Source code](https://github.com/BindsNET/bindsnet)

## What it simulates

BindsNET simulates spiking neural networks with PyTorch tensors, on CPU or GPU. The network is a `Network` object with layers of nodes (`Input`, `LIFNodes`, `AdaptiveLIFNodes`, and others) joined by `Connection` objects that hold weights. The state is updated at a fixed small time step, on the order of 1 ms. It does this by turning the differential equations of the neuron models into difference equations.

The library is built for machine learning. It has local learning rules (spike-timing-dependent plasticity and variants, reward-modulated rules), spike encoders for images, dataset loaders and pipelines for unsupervised, supervised and reinforcement learning, including an Atari Breakout demo. It comes from the BINDS lab at the University of Massachusetts Amherst.

## When to use it

Use BindsNET when you want to try a biologically inspired learning rule on a task such as digit recognition, in code that behaves like normal PyTorch.

- Use [Norse](norse.md) when you want spiking layers trained by gradient descent inside a PyTorch model.
- Use [Brian 2](brian2.md) when you want to write the neuron equations yourself and care about physical units.
- Use [NEST](nest.md) when you need large, anatomically structured networks and validated neuron models.

## Install

BindsNET 0.3.4 (June 2026) is the current release. It requires Python 3.11 to 3.13.

```
pip install bindsnet
```

The project documents `pip install bindsnet`, an install from GitHub, a `poetry install` from the committed lock file and a Dockerfile that builds the pinned stack. A conda-forge package `bindsnet` 0.3.4 (noarch) also exists. The 0.3.4 package depends on `torch`, `torchvision`, `numpy`, `scipy`, `pandas`, `matplotlib`, `scikit-learn`, `scikit-image`, `opencv-python`, `tensorboardX`, `gymnasium[atari]` and `ale-py`. That stack is large.

The recipe on this page installs CPU-only PyTorch (torch 2.14.1 and torchvision 0.29.1 from the PyTorch CPU wheel index, which has x86-64 and aarch64 builds) on `python:3.12.15-slim-bookworm`, and then `bindsnet==0.3.4` from PyPI, unmodified. It adds two system libraries (`libgl1`, `libglib2.0-0`) that the OpenCV dependency loads. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below. The full dependency stack, with Gymnasium and the Arcade Learning Environment, is large, so the image is too.

The licence is AGPL-3.0. Section 13 asks anyone who modifies BindsNET and lets others use it over a network to offer them the modified source. The recipe changes nothing in BindsNET and only calls it from a short script, but check the licence before you put a modified copy behind a service.

## A first run

Adapted from the reproduction table [REPRODUCING.md](https://github.com/BindsNET/bindsnet/blob/master/REPRODUCING.md) and the [README](https://github.com/BindsNET/bindsnet#getting-started). It replicates the spiking network of Diehl and Cook (2015) on MNIST.

```
git clone https://github.com/BindsNET/bindsnet
cd bindsnet
python examples/mnist/eth_mnist.py --n_neurons 100 --n_epochs 1 --time 250 --seed 0
```

The script downloads MNIST on first use. `--n_neurons` sets the number of excitatory (and inhibitory) neurons, `--time` the simulated milliseconds per image, `--n_epochs` the passes over the training set, and `--seed` the random seed. `--plot` opens monitoring figures. The REPRODUCING.md file states that its expected-output cells describe what the script reports, and that it has not measured a final accuracy for these commands.

The recipe below does not train on MNIST. Its script builds the smallest network from the BindsNET benchmark example, `examples/benchmark/benchmark.py`: an `Input` layer `X` and a `LIFNodes` layer `Y` joined by a `Connection`, driven by `poisson` spike trains and run with `network.run`. The script adds `Monitor` objects that record spikes and voltage, and sets the weights to a random uniform draw scaled by a parameter. The default is 100 inputs, 50 LIF neurons and 500 steps of 1 ms, so it should run for seconds on one CPU. This is a check that the library works, not a learning experiment.

## Run the tested example

This recipe builds BindsNET in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.4 s.

1. Download [bindsnet-recipe.tar.gz](https://biosimhub.pages.dev/guides/bindsnet/bindsnet-recipe.tar.gz) (Dockerfile, run_bindsnet.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bindsnet-recipe.tar.gz
   cd bindsnet
   sh run.sh
   ```

![Terminal recording of the BindsNET example run](https://biosimhub.pages.dev/media/bindsnet/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/bindsnet:0.3.4 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bindsnet:0.3.4 python /opt/run_bindsnet.py --n-input 100 \
    --n-output 50 --time 500 --max-rate 50 --weight-scale 0.2 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `output_spikes.csv` | 2.3 KB |
| `raster.png` | 32.0 KB |
| `run_log.txt` | 0 B |
| `summary.txt` | 107 B |
| `voltage_neuron0.csv` | 11.1 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/bindsnet/result-dark.png"><img src="https://biosimhub.pages.dev/media/bindsnet/result.png" alt="Plot of the BindsNET example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>output_spikes.csv</code></summary>

```
step,neuron
72,30
73,44
76,18
76,19
76,21
76,23
76,28
76,33
76,36
76,41
77,35
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
seed	42
steps	500
input_spikes	1303
output_spikes	310
mean_input_rate_hz	26.060
mean_output_rate_hz	12.400
```

</details>

<details><summary>First lines of <code>voltage_neuron0.csv</code></summary>

```
step,voltage
0,-65.0
1,-65.0
2,-65.0
3,-65.0
4,-65.0
5,-65.0
6,-65.0
7,-65.0
8,-65.0
9,-65.0
10,-65.0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--n-input` | Input neurons | 100 | 1 to 1000 |
| `--n-output` | LIF neurons | 50 | 1 to 500 |
| `--time` | Simulation steps (1 step = 1 ms) | 500 | 10 to 5000 |
| `--max-rate` | Highest input rate (Hz) | 50 | 0.1 to 200 |
| `--weight-scale` | Weight scale (weights uniform in 0 to scale) | 0.2 | 0 to 5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- **Console output.** The script prints its training progress and accuracy figures while it runs. REPRODUCING.md lists what each script reports.
- **Plots** with `--plot`: input spikes, the learned weight maps (each excitatory neuron's receptive field), voltages and spike rasters.
- **Spike tensors.** Monitors (`Monitor` objects) record node variables such as spikes `s` and voltages `v`. `monitor.get('s')` returns a tensor of shape time by batch by neurons.
- **Recipe output.** The script writes the output spikes as a two-column CSV (step, neuron), the voltage of the first output neuron, a raster plot of input and output spikes and a summary with spike counts and mean rates. The input rates are drawn per neuron from a uniform range, so the summary mean input rate is about half the highest rate you set.
- **Learned weights.** In the MNIST example each excitatory neuron has a 28 by 28 weight map over the input pixels, which the `--plot` figures display.

## Pitfalls

- **Seeds and determinism.** The scripts call `torch.manual_seed`. REPRODUCING.md notes that GPU atomics and the first-run dataset download can still cause variation.
- **Time cost.** The time dimension multiplies the cost. A run with `--time 250` is 250 steps per image.
- **Downloads.** Datasets come from upstream sources at run time. Offline machines need them in place first.
- **Version drift.** The 0.3.4 requirements are recent (`torch<3,>=2.14`). Older tutorials may use older APIs.
- **Licence.** Check AGPL-3.0 before putting a modified copy behind a service.

## Further reading

- Source and README: https://github.com/BindsNET/bindsnet
- Documentation: https://bindsnet-docs.readthedocs.io/
- Examples: https://github.com/BindsNET/bindsnet/tree/master/examples
- Paper: Hazan H, et al. (2018). BindsNET: a machine learning-oriented spiking neural networks library in Python. Front Neuroinform 12:89. https://doi.org/10.3389/fninf.2018.00089

---

Cite: Hazan H, Saunders DJ, Khan H, Patel D, Sanghavi DT, Siegelmann HT, Kozma R (2018). BindsNET: a machine learning-oriented spiking neural networks library in Python. Front Neuroinform 12:89. doi:10.3389/fninf.2018.00089

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bindsnet).
