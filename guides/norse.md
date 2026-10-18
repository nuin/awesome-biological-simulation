# Norse

> Run bio-inspired spiking neuron layers as PyTorch modules; the example feeds leaky integrate-and-fire neurons constant inputs and counts their spikes.

Licence: LGPL-3.0-only · [Source code](https://github.com/norse/norse)

## What it simulates

Norse is a library that adds spiking neuron models to PyTorch. Each model is a PyTorch module: the leaky integrate-and-fire cell (`LIFCell`), the leaky integrator (`LICell`), adaptive and recurrent variants, and the long short-term spiking networks (LSNN) of Bellec et al. Spikes are all-or-nothing events, so Norse uses surrogate gradients to let backpropagation train networks that contain them.

The simulation is discrete in time. You loop over time steps, pass the input of each step through the layers, and carry the neuron state (membrane voltage, synaptic current) from one step to the next. Because the modules are PyTorch modules, you can mix them with ordinary layers such as `Conv2d` and `Linear` and run them on a GPU.

## When to use it

Use Norse when the aim is to train or evaluate a spiking network for a machine-learning task, such as classifying MNIST digits or control tasks, and you already work in PyTorch.

- Use [Brian 2](brian2.md) or [NEST](nest.md) when you want neuroscience models with explicit units, synapse types and large-scale connectivity, without training.
- Use [BrainPy](brainpy.md) for JAX-based spiking and neural-mass models.
- Use [Nengo](nengo.md) when you want to specify what the network computes and let the framework find the weights.

## Install

Norse 1.1.0 (March 2024) is the current release. The project README lists these routes:

```
pip install norse
conda install norse
docker pull quay.io/norse/norse
```

The README assumes Python 3.8 or later and PyTorch 1.9 or later. The 1.1.0 package on PyPI requires `torch>=2.0.0`, `torchvision>=0.15.0`, `numpy`, `nir` and `nirtorch`. The conda-forge package `norse` 1.1.0 exists for linux-64, osx-64 and osx-arm64. The PyTorch install is the large part, several hundred megabytes, or more with CUDA.

The licence is LGPL-3.0.

## Run the tested example

This recipe builds Norse in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 11.8 s. Norse has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [norse-recipe.tar.gz](https://biosimhub.pages.dev/guides/norse/norse-recipe.tar.gz) (Dockerfile, run_norse.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf norse-recipe.tar.gz
   cd norse
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/norse:1.1.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/norse:1.1.0 python /opt/run_norse.py --neurons 10 --steps 500 \
    --max-input 1 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `rates.csv` | 226 B |
| `run_log.txt` | 40 B |
| `v_last_neuron.csv` | 6.2 KB |

<details><summary>First lines of <code>rates.csv</code></summary>

```
neuron,input,spikes,rate_hz
0,0.0000,0,0.00
1,0.1111,0,0.00
2,0.2222,22,44.00
3,0.3333,55,110.00
4,0.4444,82,164.00
5,0.5556,99,198.00
6,0.6667,124,248.00
7,0.7778,164,328.00
8,0.8889,165,330.00
9,1.0000,165,330.00
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 10 neurons, 500 steps, 876 spikes
```

</details>

<details><summary>First lines of <code>v_last_neuron.csv</code></summary>

```
step,v
0,0.10000
1,0.27000
2,0.48700
3,0.73350
4,0.99631
5,0.00000
6,0.39514
7,0.77174
8,0.00000
9,0.44631
10,0.85873
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--neurons` | Neurons | 10 | 1 to 1000 |
| `--steps` | Time steps (1 ms each) | 500 | 10 to 20000 |
| `--max-input` | Input to the last neuron (first gets 0) | 1 | 0 to 20 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the example in the Norse [README](https://github.com/norse/norse#23-example-spiking-convolutional-classifier): a spiking convolutional network applied to a batch of random images.

```python
import torch, torch.nn as nn
from norse.torch import LICell             # Leaky integrator
from norse.torch import LIFCell            # Leaky integrate-and-fire
from norse.torch import SequentialState    # Stateful sequential layers

model = SequentialState(
    nn.Conv2d(1, 20, 5, 1),      # Convolve from 1 -> 20 channels
    LIFCell(),                   # Spiking activation layer
    nn.MaxPool2d(2, 2),
    nn.Conv2d(20, 50, 5, 1),     # Convolve from 20 -> 50 channels
    LIFCell(),
    nn.MaxPool2d(2, 2),
    nn.Flatten(),                # Flatten to 800 units
    nn.Linear(800, 10),
    LICell(),                    # Non-spiking integrator layer
)

data = torch.randn(8, 1, 28, 28) # 8 batches, 1 channel, 28x28 pixels
output, state = model(data)      # Provides a tuple (tensor (8, 10), neuron state)
```

The README says `output` has shape (8, 10): one score per class for each of the 8 images. `state` holds the neuron state to feed into the next time step. To train a full classifier, run `python -m norse.task.mnist`, as the README describes.

## Reading the output

- **Cell calls return `(output, state)`.** For `LIFCell` the output is a tensor of 0/1 spikes with the shape of the input. Pass `state` back on the next step; pass `None` on the first.
- **State.** For a LIF cell the state has the membrane voltage `v` and synaptic current `i`.
- **Rates.** Add up the spikes over time and divide by the time to get a firing rate. A `LICell` at the end of a network gives a continuous readout instead of spikes.

The recipe takes a simpler route than the README model. It feeds one `LIFCell` a constant input that rises from 0 for the first neuron to a chosen maximum for the last one, steps it for 500 time steps, and writes `rates.csv` (input, spike count and rate per neuron) and `v_last_neuron.csv` (the voltage of the last neuron over time). Neurons with larger input fire more, and neurons with too little input stay silent. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **State handling.** Forgetting to pass the state back makes every step start from rest.
- **Time axis.** The default cell steps by 1 ms (`dt = 0.001`). Inputs are per-step values, not a continuous current.
- **Surrogate gradients.** Gradients for the spike are approximate. Training can be sensitive to learning rate and neuron parameters.
- **Dependencies.** Norse tracks recent PyTorch versions. Install into a clean environment.
- **Release age.** The last release is March 2024. Check open issues before you rely on it for new work.

## Further reading

- Documentation: https://norse.github.io/norse/
- Source: https://github.com/norse/norse
- Tutorial notebooks: https://github.com/norse/notebooks
- Software citation: Pehle C, Pedersen JE (2021). Norse: a deep learning library for spiking neural networks. Zenodo. https://doi.org/10.5281/zenodo.4422025

---

Cite: Pehle C, Pedersen JE (2021). Norse: a deep learning library for spiking neural networks. Zenodo. doi:10.5281/zenodo.4422025

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/norse).
