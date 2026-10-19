# Brain Modeling Toolkit (BMTK)

> Run the 120-neuron point-neuron cortex model from the BMTK examples on NEST, with a thalamic spike-train input and an optional current clamp.

Licence: BSD-3-Clause · [Source code](https://github.com/AllenInstitute/bmtk)

## What it simulates

BMTK, from the Allen Institute, builds and runs models of brain circuits at several levels of detail. It does not have one solver of its own for everything. It has a network builder and a set of simulation engines, and several engines call other simulators.

- **BioNet** runs multi-compartment, biophysically detailed cells with NEURON.
- **PointNet** runs point-neuron networks with NEST.
- **PopNet** runs population-level firing-rate models with DiPDE.
- **FilterNet** turns visual or auditory stimuli into spike trains, using filters that are built into BMTK.

All engines read the same network files in the SONATA format. You build a network once, save it, and then run it at a different level of detail by changing the configuration. The project documentation says models range from single cells to networks with millions of cells and billions of synapses, with automatic parallelisation. Its showcase is the Allen Institute model of mouse primary visual cortex.

## When to use it

Use BMTK when you want a layered, file-based workflow for a circuit model: build, simulate, analyse, share as SONATA.

- Use NEST or NEURON directly when you write one model for one simulator and do not need the SONATA files.
- Use [PyNN](pynn.md) when you want one script that runs on several back ends, and are happy to describe the network in Python rather than files.
- Use Brian 2 when you want to write your own neuron equations.

BMTK is a toolkit around other simulators. You still install and run NEURON or NEST for BioNet and PointNet.

## Install

BMTK 1.2.0 (June 2026) is the current release on PyPI and GitHub. The installation guide gives:

```
pip install bmtk
```

It also lists installing from source (`git clone`, then `python setup.py install`), a conda route (`conda install -c kaeldai bmtk`) and a Docker image (`alleninstitute/bmtk`). The base install needs numpy, h5py, pandas, matplotlib and jsonschema. PyPI declares extras: `bmtk[bionet]` pulls in NEURON, `bmtk[pointnet]` pulls in NEST and `bmtk[popnet]` pulls in DiPDE.

Each engine needs its simulator. BioNet needs NEURON with its Python bindings, and the example mechanisms must be compiled with `nrnivmodl`, which needs a C compiler. PointNet needs NEST. PopNet needs DiPDE.

The recipe on this page uses PointNet, because the `point_120cells` example needs no compiled mechanisms. It installs NEST 3.6 and Python 3.11 from conda-forge, then `bmtk==1.2.0` from PyPI, and it ships the example's network and model files from the v1.2.0 tag. NEST on conda-forge has Linux x86-64 and macOS builds only, so the image is built for `linux/amd64` and runs under emulation on ARM machines. The NEST version was chosen from the available conda-forge builds. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below. The project's own Docker environment pins NEST 3.3 with Python 3.9, so fall back to those if the newer pair fails. BioNet is left out because it needs `nrnivmodl` compiled mechanisms.

The licence is BSD-3-Clause.

## A first run

The `point_120cells` example is a 120-neuron network with a thalamic spike-train input, run on NEST. Adapted from the [point_120cells README](https://github.com/AllenInstitute/bmtk/tree/develop/examples/point_120cells): clone the repository, install `bmtk` and NEST, then from the example folder run

```
python run_pointnet.py config.simulation.json
```

The script is short:

```python
from bmtk.simulator import pointnet

configure = pointnet.Config.from_json("config.simulation.json")
configure.build_env()
network = pointnet.PointNetwork.from_config(configure)
sim = pointnet.PointSimulator.from_config(configure, network)
sim.run()
```

The network files already exist in the `network/` folder as SONATA files. `build_network.py` rebuilds them with the BMTK builder. The README warns that a rebuild is partly random, so the results differ a little each time. `plot_output.py` plots the results.

Settings live in the SONATA configuration JSON. In `config.simulation.json`, `run.tstop` is 3000.0 ms, a spike-train input `thalamus_spikes` drives the `thalamus` population, and a membrane-potential report records `V_m` for cells 0, 20, 60, 80 and 100 of the `cortex` population (values from the repository file). A second config adds current-clamp inputs that excite cells 20 to 39 and inhibit cells 40 to 49.

The recipe below wraps that script. Its helper copies the example, sets the run length and an optional current clamp on cells 20 to 39 (the same `current_clamp` input the example README uses for its perturbation run), runs PointNet, and copies the output files to the working folder. The default run is 1000 ms, a third of the example's 3000 ms, to keep it short.

## Run the tested example

This recipe builds Brain Modeling Toolkit (BMTK) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 17.1 s. Brain Modeling Toolkit (BMTK) has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [bmtk-recipe.tar.gz](https://biosimhub.pages.dev/guides/bmtk/bmtk-recipe.tar.gz) (Dockerfile, LICENSE-bmtk.txt, example, run_bmtk.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bmtk-recipe.tar.gz
   cd bmtk
   sh run.sh
   ```

![Terminal recording of the Brain Modeling Toolkit (BMTK) example run](https://biosimhub.pages.dev/media/bmtk/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/bmtk:1.2.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bmtk:1.2.0 python /opt/run_bmtk.py --tstop 1000 --iclamp 0 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `config.simulation.json` | 1.8 KB |
| `log.txt` | 644 B |
| `membrane_potential.h5` | 38.2 MB |
| `run_log.txt` | 1.0 KB |
| `run_summary.txt` | 30 B |
| `spikes.csv` | 6.6 KB |
| `spikes.h5` | 14.0 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/bmtk/result-dark.png"><img src="https://biosimhub.pages.dev/media/bmtk/result.png" alt="Plot of the Brain Modeling Toolkit (BMTK) example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>config.simulation.json</code></summary>

```
{
  "run": {
    "tstop": 1000.0,
    "dt": 0.001,
    "block_run": false,
    "block_size": 1000.0
  },
  "inputs": {
    "thalamus_spikes": {
      "input_type": "spikes",
      "module": "sonata",
      "input_file": "/tmp/example/point_120cells/inputs/thalamus_spikes.h5",
```

</details>

<details><summary>First lines of <code>log.txt</code></summary>

```
2026-10-18 04:52:13,099 [INFO] Created log file
2026-10-18 04:52:13,183 [INFO] Batch processing nodes for cortex/0.
2026-10-18 04:52:13,189 [INFO] Batch processing nodes for thalamus/0.
2026-10-18 04:52:13,217 [INFO] Setting up output directory
2026-10-18 04:52:13,217 [INFO] Building cells.
2026-10-18 04:52:13,232 [INFO] Building recurrent connections
2026-10-18 04:52:13,246 [INFO] Network created.
2026-10-18 04:52:13,246 [INFO] Build virtual cell stimulations for thalamus_spikes
2026-10-18 04:52:13,311 [INFO] Simulation Started
2026-10-18 04:52:22,230 [INFO] Simulation finished, finalizing results.
2026-10-18 04:52:23,194 [INFO] Done.
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```

              -- N E S T --
  Copyright (C) 2004 The NEST Initiative

 Version: 3.6.0
 Built: Apr  5 2024 08:03:04

 This program is provided AS IS and comes with
 NO WARRANTY. See the file LICENSE for details.

 Problems or suggestions?
   Visit https://www.nest-simulator.org
```

</details>

<details><summary>First lines of <code>run_summary.txt</code></summary>

```
tstop_ms	1000.0
iclamp_pA	0.0
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
timestamps population node_ids
51.278 cortex 0
987.618 cortex 78
59.594 cortex 78
47.251 cortex 78
810.073 cortex 77
760.824 cortex 77
595.656 cortex 77
467.362 cortex 77
319.438 cortex 77
56.087 cortex 77
961.269 cortex 76
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--tstop` | Simulated time (ms) | 1000 | 100 to 3000 |
| `--iclamp` | Current clamp on cortex cells 20 to 39 (pA | 0 | -500 to 500 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

A successful run creates an `output` directory. It holds a log file, the spike trains (`spikes.h5`, and `spikes.csv` when the config asks for it) and any recorded cell variables, as the example README states. In the recipe the helper copies these files to the job's output list. The membrane potential report is written as a file beside them.

- Spike files list, for each spike, the node id and the time in ms.
- The membrane-potential report holds `V_m` over time for the listed cells.
- The `bmtk.analyzer` module reads these files back and draws raster plots, firing-rate plots and traces. The user guide has a page on analysing results.

Compare the control run and the perturbation run to see the effect of the injected current on the firing of the affected cells.

## Pitfalls

- **Simulators are separate installs.** `pip install bmtk` does not give you a working BioNet or PointNet. Install NEURON or NEST first. The recipe takes NEST from conda-forge (`nest-simulator`), not from the `NEST` name in the PyPI extra.
- **Compile the mechanisms.** BioNet fails with "NEURON mechanisms not found" until `nrnivmodl` has run on the modfiles folder.
- **Paths in the config.** Configs use a manifest of `$BASE_DIR`-style variables. Moving only part of an example folder breaks the paths.
- **Python 2 notes.** The docs still say the toolkit supports Python 2.7 and 3.6 or newer. Use a current Python 3.
- **Docker volumes.** The Docker image needs the working folder mounted, and every file the config references must be inside it.
- **Rebuilt networks differ.** The builder uses random numbers, so each rebuild gives a slightly different network.

## Further reading

- User guide: https://alleninstitute.github.io/bmtk/
- Installation guide: https://alleninstitute.github.io/bmtk/installation.html
- PointNet: https://alleninstitute.github.io/bmtk/pointnet.html
- Tutorials: https://alleninstitute.github.io/bmtk/tutorials.html
- Source and examples: https://github.com/AllenInstitute/bmtk
- Paper: Dai K, Gratiy SL, Billeh YN, et al. (2020). PLoS Computational Biology 16(11):e1008386. https://doi.org/10.1371/journal.pcbi.1008386

---

Cite: Dai K, Gratiy SL, Billeh YN, et al. (2020). Brain Modeling ToolKit: An open source software suite for multiscale modeling of brain circuits. PLoS Comput Biol 16(11):e1008386. doi:10.1371/journal.pcbi.1008386

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bmtk).
