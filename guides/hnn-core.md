# HNN-core

> Simulate a biophysical neocortical column in NEURON and read out the MEG/EEG current dipole, spikes and drive-evoked responses.

Licence: BSD-3-Clause · [Source code](https://github.com/jonescompneurolab/hnn-core)

## What it simulates

HNN-core simulates a biophysically detailed model of a neocortical column in NEURON and turns the result into the signals that MEG and EEG measure. The network has layer 2/3 and layer 5 pyramidal cells plus basket interneurons. Its main output is the aggregate current dipole, in nano-ampere-metres, which is directly comparable to source-localised human data. Local field potentials, current-source density and spikes can be simulated at the same time.

You drive the column with external inputs. The tutorial uses evoked drives (spikes arriving at set times at proximal or distal dendrites) and also names Poisson and bursty drives. Each drive gets AMPA and NMDA synaptic weights per cell type.

HNN-core is the code behind the Human Neocortical Neurosolver (HNN) tool from Brown University. The same package powers the HNN graphical interface.

## When to use it

Use HNN-core to ask which cellular and circuit events could produce an ERP or a brain rhythm measured with MEG or EEG.

- Use [LFPy](lfpy.md) when you want to compute extracellular potentials from your own morphologies.
- Use [PyRates](pyrates.md) when you want a population-level model that runs far faster.
- Use [Rockpool](rockpool.md) when the goal is a trained spiking network, not a cortical column.

## Install

HNN-core 0.6.1 (released 2026-05-13) is on PyPI as a source distribution. Its licence is BSD-3-Clause. The README recommends conda for a full install:

```bash
conda create -y -q -n hnn-core-env python=3.12
conda activate hnn-core-env
conda install hnn-core-all -c jonescompneurolab -c conda-forge
```

The conda packages support Python 3.12 only. The PyPI package supports Python 3.9 to 3.13, and 0.6.1 asks for NEURON between 7.7 and 8.2.7.

```bash
pip install hnn-core
```

The package prints a survey notice and writes a file inside its own folder on first import, and NEURON compiles its mechanism files on first use. The recipe below therefore does both while building the image, pins Python 3.12 and NEURON 8.2.7, and runs on linux/amd64. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds HNN-core in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 30.5 s. HNN-core has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [hnn-core-recipe.tar.gz](https://biosimhub.pages.dev/guides/hnn-core/hnn-core-recipe.tar.gz) (Dockerfile, run_hnn.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf hnn-core-recipe.tar.gz
   cd hnn-core
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/hnn-core:0.6.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/hnn-core:0.6.1 python /opt/run_hnn.py --tstop 60 --seed 544 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `dipole.csv` | 39.1 KB |
| `run_log.txt` | 373 B |
| `spikes.csv` | 6.9 KB |

<details><summary>First lines of <code>dipole.csv</code></summary>

```
t_ms,agg_nAm
0.000,0.004901
0.025,-0.001220
0.050,-0.001243
0.075,-0.001226
0.100,-0.001209
0.125,-0.001197
0.150,-0.001190
0.175,-0.001186
0.200,-0.001182
0.225,-0.001180
0.250,-0.001177
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Joblib will run 1 trial(s) in parallel by distributing trials over 1 jobs.
Loading custom mechanism files from /usr/local/lib/python3.12/site-packages/hnn_core/mod/x86_64/libnrnmech.so
Building the NEURON model
[Done]
Trial 1: 0.03 ms...
Trial 1: 10.0 ms...
Trial 1: 20.0 ms...
Trial 1: 30.0 ms...
Trial 1: 40.0 ms...
Trial 1: 50.0 ms...
tstop=60.0 samples=2401 spikes=326
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
time_ms,gid,type
19.214,298.0,evprox1
19.771,321.0,evprox1
20.151,491.0,evprox1
20.780,432.0,evprox1
21.168,389.0,evprox1
21.402,440.0,evprox1
21.434,285.0,evprox1
21.640,391.0,evprox1
21.792,458.0,evprox1
21.989,527.0,evprox1
21.993,473.0,evprox1
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--tstop` | Simulated time (ms) | 60 | 10 to 170 |
| `--seed` | Drive seed | 544 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the [ERP tutorial](https://jonescompneurolab.github.io/hnn-core/stable/auto_examples/workflows/plot_simulate_evoked.html). The tutorial builds a network, adds one distal and two proximal evoked drives, and simulates 170 ms with 2 trials. This shortened version keeps one proximal drive:

```python
from hnn_core import simulate_dipole, jones_2009_model

net = jones_2009_model()
weights_ampa = {'L2_basket': 0.08831, 'L2_pyramidal': 0.01525,
                'L5_basket': 0.19934, 'L5_pyramidal': 0.00865}
delays = {'L2_basket': 0.1, 'L2_pyramidal': 0.1,
          'L5_basket': 1., 'L5_pyramidal': 1.}
net.add_evoked_drive('evprox1', mu=26.61, sigma=2.47, numspikes=1,
                     weights_ampa=weights_ampa, weights_nmda=None,
                     location='proximal', synaptic_delays=delays,
                     event_seed=544)
dpls = simulate_dipole(net, tstop=60., n_trials=1)
```

The tutorial smooths and scales the dipole before plotting, with a window of 30 samples and a factor of 3000, for example `dpl.smooth(30).scale(3000)`.

## Reading the output

- `simulate_dipole` returns a list of `Dipole` objects, one per trial. `dpl.times` is time in ms and `dpl.data['agg']` is the aggregate dipole. Layer traces `L2` and `L5` sit beside it.
- `net.cell_response` holds spike times, cell IDs and spike types. The tutorial plots a spike histogram split into `evprox` and `evdist` input spikes.
- A proximal drive excites the dendrites nearest the soma, a distal drive those far from it. Compare the sign and timing of the dipole after each to relate waveform features to layers.
- The recipe helper writes `dipole.csv` (time and aggregate dipole) and `spikes.csv`.

## Pitfalls

- **NEURON version limits.** The 0.6.1 package caps NEURON at 8.2.7, which limits the Python versions that install cleanly.
- **A C compiler is needed.** Mechanism files compile on first use.
- **Runtime grows with the network.** The full 170 ms run with several drives takes much longer than a short test. Shorten `tstop` first.
- **Units.** Dipoles are in nAm. The tutorial's scaling factor is a fit to match data, not a physical constant.
- **Drive seeds.** Each drive takes its own `event_seed`. Change it to draw a different spike timing for that drive.

## Further reading

- Documentation: https://jonescompneurolab.github.io/hnn-core/stable/
- Textbook and installation guide: https://jonescompneurolab.github.io/textbook/content/preface.html
- Source: https://github.com/jonescompneurolab/hnn-core
- Jas M, et al. (2023). HNN-core: a Python software for cellular and circuit-level interpretation of human MEG/EEG. J Open Source Softw 8(92):5848. https://doi.org/10.21105/joss.05848

---

Cite: Jas M, Thorpe R, Tolley N, Bailey C, Brandt S, Caldwell B, et al. (2023). HNN-core: a Python software for cellular and circuit-level interpretation of human MEG/EEG. J Open Source Softw 8(92):5848. doi:10.21105/joss.05848

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/hnn-core).
