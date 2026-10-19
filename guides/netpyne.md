# NetPyNE

> Build and run a network of Hodgkin-Huxley neurons on NEURON from a declarative NetPyNE parameter file, and save the spike times and per-population firing rates.

Licence: MIT · [Source code](https://github.com/suny-downstate-medical-center/netpyne)

## What it simulates

NetPyNE builds and runs networks of biophysically detailed neurons on the NEURON simulator. You describe the network in Python dictionaries instead of writing NEURON code: populations of cells, cell types with sections and ion channels, synapse types, connection rules, stimulation, and what to record. NetPyNE then creates the cells, wires them, runs NEURON and gathers the results.

The description lives in two objects. `netParams` holds the network: `popParams`, `cellParams`, `synMechParams`, `connParams`, `stimSourceParams` and `stimTargetParams`. `simConfig` holds the run: duration, time step `dt`, random seeds, what to record, what to save and which plots to draw. Time is in milliseconds.

Beyond one process, NetPyNE also runs on several cores through MPI, runs batches over parameter ranges, and ships a graphical interface (the NetPyNE GUI at gui.netpyne.org) for the same models. It can import and export NeuroML and SONATA models.

## When to use it

Use NetPyNE when the cells need real morphology and channels, the network is more than a few cells, and you do not want to hand-write NEURON network code. It suits cortical column models, multi-scale models with LFP or EEG outputs, and parameter sweeps.

- Use [Arbor](arbor.md) when you need the same kind of detailed cells on many cores or a GPU.
- Use [c302](c302.md) for the C. elegans nervous system as a NeuroML model.
- Use [NGC-Learn](ngclearn.md) for point-neuron circuits where the learning rule is the question.

## Install

NetPyNE is a pure Python package on PyPI; the current release is 1.1.1. It needs the NEURON simulator, which also installs with pip on Linux and macOS (the NEURON release on PyPI is 9.0.2, with wheels for Linux x86-64 and ARM64 and for macOS).

```
pip install neuron
pip install netpyne
```

These are the commands in the NetPyNE install guide (`pip install netpyne`, and `pip install neuron` for NEURON on Linux or Mac). For parallel runs the guide says to install NEURON with MPI support. The guide recommends Anaconda for the Python environment. On Windows it recommends the Windows Subsystem for Linux.

There is no NetPyNE package on conda-forge. NEURON itself is on conda-forge (9.0.1).

## Run the tested example

This recipe builds NetPyNE in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.5 s.

1. Download [netpyne-recipe.tar.gz](https://biosimhub.pages.dev/guides/netpyne/netpyne-recipe.tar.gz) (Dockerfile, run_netpyne.py, example model.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf netpyne-recipe.tar.gz
   cd netpyne
   sh run.sh
   ```

![Terminal recording of the NetPyNE example run](https://biosimhub.pages.dev/media/netpyne/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/netpyne:1.1.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/netpyne:1.1.1 python /opt/run_netpyne.py --model /work/in/model.py \
    --cells 0 --duration 0 --seed 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `netpyne_run_data.json` | 2.1 MB |
| `run_log.txt` | 1.2 KB |
| `spikes.csv` | 49.7 KB |
| `summary.csv` | 59 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/netpyne/result-dark.png"><img src="https://biosimhub.pages.dev/media/netpyne/result.png" alt="Plot of the NetPyNE example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>netpyne_run_data.json</code></summary>

```
{
    "net": {
        "cells": [
            {
                "conns": [
                    {
                        "delay": 13.121985331296386,
                        "label": "PYR->PYR",
                        "loc": 0.5,
                        "preGid": 28,
                        "preLoc": 0.5,
                        "sec": "soma",
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```

Start time:  2026-10-18 05:11:17.627743

Validating NetParams ...
✅  Successfully validated generalParams
✅  Successfully validated cellParams
✅  Successfully validated popParams
✅  Successfully validated synMechParams
✅  Successfully validated connParams
✅  Successfully validated subConnParams
✅  Successfully validated stimSourceParams
✅  Successfully validated stimTargetParams
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
time_ms,cell_id
3.4750000001000156,18.0
5.20000000010004,62.0
5.850000000100049,71.0
6.150000000100054,114.0
6.175000000100054,27.0
6.225000000100055,78.0
6.250000000100055,52.0
7.1250000001000675,124.0
7.425000000100072,54.0
8.450000000100054,128.0
8.475000000100053,79.0
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
population,cells,spikes,mean_rate_hz
PYR,200,2067,10.335
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--cells` | Cells per population (0 keeps the file's value) | 0 | 0 to 1000 |
| `--duration` | Duration in ms (0 keeps the file's value) | 0 | 0 to 5000 |
| `--seed` | Seed | 1 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Tutorial 1 of the NetPyNE docs needs three lines of code and one parameter file, `HHTut.py`. The file defines 200 Hodgkin-Huxley cells in one population (`PYR`), each a single soma with `hh` channels. The cells receive random background input (`NetStim`, 10 Hz, noise 0.5) and connect to each other with a random convergence of 1 to 15 inputs per cell. The simulation lasts 1 second with `dt = 0.025` ms.

```python
import HHTut
from netpyne import sim
sim.createSimulateAnalyze(netParams = HHTut.netParams, simConfig = HHTut.simConfig)
```

Run it with `python tut1.py`. For several cores the tutorial gives `mpiexec -n 4 nrniv -python -mpi tut1.py`.

The recipe's driver script loads the same `HHTut.py`, turns the figures off (the container has no display), calls `sim.createSimulate`, and writes the spikes and a firing-rate table.

Adapted from <http://doc.netpyne.org/tutorial.html>, the "Quick and easy example".

## Reading the output

The tutorial shows three figures: a 2D map of the cells and connections, a raster plot (cell number against spike time) and the voltage trace of one cell. The tutorial notes that figures are saved as `HHTut_raster.png` and `HHTut_traces.png`, and that on some systems the windows show up empty, so use the saved files.

The recipe saves tables instead:

- `spikes.csv`: one row per spike, with the time in ms and the cell id.
- `summary.csv`: one row per population with its cell count, spike count and mean rate in Hz (spikes per cell per second of simulated time).
- `netpyne_run.json`: NetPyNE's full data file, with the network, spikes and recorded traces.

The `simConfig.seeds` dictionary sets separate seeds for connectivity, stimulation and cell placement.

## Pitfalls

- **NEURON first.** NetPyNE imports `neuron`. If it fails, check `python -c "import neuron"` before debugging NetPyNE.
- **Custom channels need compiling.** Models that use their own `.mod` files need `nrnivmodl` run in the model folder first. The tutorial model uses only built-in mechanisms (`hh`, `Exp2Syn`, `NetStim`).
- **Blank figures.** The tutorial advises adding `import pylab; pylab.show()` to the script if the plot windows are empty.
- **Nested dictionaries.** Misspelled keys in `netParams` are a common source of errors. Setting `simConfig.validateNetParams = True` (as `HHTut.py` does) checks them.
- **Parallel runs.** Use `mpiexec` with `nrniv -python -mpi`. Results gather on the master node.
- **Python versions.** The install guide's dependency text is older than the package. Check `python_requires` on PyPI for current limits.

## Further reading

- Documentation: http://doc.netpyne.org/
- Tutorial: http://doc.netpyne.org/tutorial.html
- Project site: https://www.netpyne.org/
- Source: https://github.com/suny-downstate-medical-center/netpyne
- Paper: Dura-Bernal S et al. (2019). NetPyNE, a tool for data-driven multiscale modeling of brain circuits. eLife 8:e44494. https://doi.org/10.7554/eLife.44494

---

Cite: Dura-Bernal S, et al. (2019). NetPyNE, a tool for data-driven multiscale modeling of brain circuits. eLife 8:e44494. doi:10.7554/eLife.44494

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/netpyne).
