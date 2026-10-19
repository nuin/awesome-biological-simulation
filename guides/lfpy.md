# LFPy

> Compute extracellular potentials (LFP, spikes, EEG, MEG) from multicompartment neuron models run in NEURON.

Licence: GPL-3.0-or-later · [Source code](https://github.com/LFPy/LFPy)

## What it simulates

LFPy computes the electric and magnetic signals that neurons produce outside their cell membranes. It takes a multicompartment neuron model, runs it in NEURON, and converts the transmembrane currents of every compartment into an extracellular potential. Version 2 also predicts current dipole moments, EEG scalp potentials and MEG fields from networks of such neurons.

The default method is the line-source approximation (Holt and Koch, 1999), with a simpler point-source method also available. The project README lists the assumptions: an infinite extracellular medium with homogeneous, frequency-independent conductivity, and a minimum distance between compartments and electrodes that you can set.

LFPy does not replace NEURON. It adds Python classes (`Cell`, `Synapse`, `Network`, probe classes) around it. If a model already runs in NEURON, the README says it is likely to work with LFPy.

## When to use it

Use LFPy when you need a simulated LFP, spike waveform, EEG or MEG signal from detailed neurons, for example to test spike-sorting software or to relate a population model to a recording.

- Use [HNN-core](hnn-core.md) when you want a ready-made neocortical column that outputs a MEG/EEG current dipole.
- Use [Rockpool](rockpool.md) or [Auryn](auryn.md) when point neurons are enough and there is no extracellular signal to compute.
- Use NEURON on its own when you only need membrane voltages.

## Install

LFPy 2.3.7 is on PyPI and on conda-forge, with builds for Linux (x86-64 and aarch64) and macOS (Intel and Apple silicon). The PyPI metadata asks for Python 3.10 or newer. NEURON is a dependency, and conda-forge pulls it in (NEURON 9.0 or newer).

```bash
pip install LFPy
```

```bash
conda install -c conda-forge lfpy
```

After installing, the README suggests checking NEURON with `import neuron; neuron.test()`. The licence is GPL-3.0-or-later.

The recipe below installs the conda-forge package and runs the README example without plotting. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds LFPy in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.7 s.

1. Download [lfpy-recipe.tar.gz](https://biosimhub.pages.dev/guides/lfpy/lfpy-recipe.tar.gz) (Dockerfile, run_lfpy.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf lfpy-recipe.tar.gz
   cd lfpy
   sh run.sh
   ```

![Terminal recording of the LFPy example run](https://biosimhub.pages.dev/media/lfpy/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/lfpy:2.3.7 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/lfpy:2.3.7 python /opt/run_lfpy.py --tstop 100 --weight 0.005 \
    --sigma 0.3 --contacts 11 --spacing 20 --x 10 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `lfp.csv` | 236.9 KB |
| `run_log.txt` | 52 B |
| `traces.csv` | 48.3 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/lfpy/result-dark.png"><img src="https://biosimhub.pages.dev/media/lfpy/result.png" alt="Plot of the LFPy example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>lfp.csv</code></summary>

```
z_um,0.000,0.062,0.125,0.188,0.250,0.312,0.375,0.438,0.500,0.562,0.625,0.688,0.750,0.812,0.875,0.938,1.000,1.062,1.125,1.188,1.250,1.312,1.375,1.438,1.500,1.562,1.625,1.688,1.750,1.812,1.875,1.938,2.0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
compartments=6 samples=1601 contacts=11 tstop=100.0
```

</details>

<details><summary>First lines of <code>traces.csv</code></summary>

```
t_ms,v_soma_mV,i_syn_nA
0.0000,-70.000000,-0.00000000
0.0625,-70.000000,-0.00000000
0.1250,-70.000000,-0.00000000
0.1875,-70.000000,-0.00000000
0.2500,-70.000000,-0.00000000
0.3125,-70.000000,-0.00000000
0.3750,-70.000000,-0.00000000
0.4375,-70.000000,-0.00000000
0.5000,-70.000000,-0.00000000
0.5625,-70.000000,-0.00000000
0.6250,-70.000000,-0.00000000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--tstop` | Simulated time (ms) | 100 | 10 to 1000 |
| `--weight` | Synapse max conductance (uS) | 0.005 | 0 to 0.1 |
| `--sigma` | Extracellular conductivity (S/m) | 0.3 | 0.01 to 3 |
| `--contacts` | Probe contacts | 11 | 1 to 64 |
| `--spacing` | Contact spacing (um) | 20 | 1 to 200 |
| `--x` | Probe distance from the cell axis (um) | 10 | 1 to 500 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the [LFPy README](https://github.com/LFPy/LFPy#usage). A passive ball-and-stick neuron gets a two-spike synaptic input at the soma, and a vertical probe of 11 contacts records the potential:

```python
import numpy as np
import LFPy
from LFPy import Cell, Synapse, LineSourcePotential

cell = Cell(morphology=''.join(LFPy.__path__ + ['/test/ball_and_sticks.hoc']),
            passive=True, tstop=100)          # ms
synapse = Synapse(cell=cell, idx=cell.get_idx("soma[0]"), syntype='Exp2Syn',
                  weight=0.005, e=0, tau1=0.5, tau2=5., record_current=True)
synapse.set_spike_times(np.array([20., 40]))
lsp = LineSourcePotential(cell=cell,
                          x=np.zeros(11) + 10, y=np.zeros(11),
                          z=np.arange(11) * 20, sigma=0.3)
cell.simulate(probes=[lsp])
```

The README then plots synaptic current, soma voltage and the probe data against time.

## Reading the output

- `cell.tvec` is the time axis in ms. `cell.somav` is the soma membrane potential in mV. `synapse.i` is the synaptic current in nA.
- `lsp.data` is an array with one row per electrode contact and one column per time step. `lsp.z` gives the contact depths in micrometres. Units follow LFPy defaults, so check the docs before comparing amplitudes with data.
- A synaptic input depolarises the soma and draws current across the membrane. Expect a deflection on the contacts after each input, near 20 ms and near 40 ms, the two spike times. Amplitude and sign change with contact depth and distance from the cell, so compare contacts rather than reading one trace.
- The recipe helper writes `traces.csv` (time, soma voltage, synaptic current) and `lfp.csv` (one row per contact, one column per sample).

## Pitfalls

- **NEURON must work first.** Most install trouble comes from NEURON, Python version or MPI packages.
- **Mechanisms need compiling.** Models with custom `.mod` files must be compiled with `nrnivmodl` before LFPy can load them. The passive example needs none.
- **Homogeneous medium.** The conductivity `sigma` is one number for the whole space. Boundaries such as the cortical surface need other tools or the EEG classes.
- **Contacts too close to a compartment** give singular values. Keep probes outside the set minimum distance.
- **Version 1 and version 2 papers differ.** Cite the 2018 paper for network, EEG and MEG work.

## Further reading

- Documentation: https://lfpy.readthedocs.io
- Source: https://github.com/LFPy/LFPy
- Tutorial: https://github.com/LFPy/tutorial_at_EBRAINS
- Hagen E, Naess S, Ness TV, Einevoll GT (2018). Multimodal modeling of neural network activity: computing LFP, ECoG, EEG, and MEG signals with LFPy 2.0. Front Neuroinform 12:92. https://doi.org/10.3389/fninf.2018.00092
- Linden H, et al. (2013). LFPy: a tool for biophysical simulation of extracellular potentials generated by detailed model neurons. Front Neuroinform 7:41. https://doi.org/10.3389/fninf.2013.00041

---

Cite: Hagen E, Naess S, Ness TV, Einevoll GT (2018). Multimodal modeling of neural network activity: computing LFP, ECoG, EEG, and MEG signals with LFPy 2.0. Front Neuroinform 12:92. doi:10.3389/fninf.2018.00092

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/lfpy).
