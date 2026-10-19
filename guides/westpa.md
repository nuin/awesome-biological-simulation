# WESTPA

> Weighted-ensemble path sampling of a rare barrier-crossing event for a 1-D Langevin particle, with walker splitting and merging by bin.

Licence: MIT · [Source code](https://github.com/westpa/westpa)

## What it simulates

WESTPA runs weighted-ensemble (WE) sampling. Many short trajectories, called walkers or segments, advance in parallel. Each walker carries a statistical weight, and the weights always sum to 1. After every iteration, WESTPA sorts the walkers into bins along a progress coordinate. It splits walkers in sparsely visited bins into copies that share the parent's weight. It merges walkers in crowded bins and keeps one, chosen in proportion to weight. No walker is biased, so the weights give true probabilities and the rates are unbiased estimates.

WESTPA does not integrate dynamics itself. A propagator (a Python class, or a shell script that calls GROMACS, AMBER, OpenMM or NAMD) advances each walker one segment. WESTPA handles the resampling, the HDF5 bookkeeping and the analysis tools.

The example here replaces MD with a one-dimensional overdamped Langevin particle on the WESTPA tutorial potential, which has shallow wells at odd x (1, 3, 5, 7, 9) separated by barriers at even x. Both the wells and the barriers deepen toward low x, and the deepest well is at x = 1. Walkers start at x = 8, at the top of a barrier. The rare event is a walker reaching low x.

## When to use it

Use WESTPA when the event of interest is too rare for plain simulation, such as a protein binding, a conformational change or a permeation step, and you can name a progress coordinate that increases along the path.

- Use [OpenMM](openmm.md) or [GROMACS](gromacs.md) when the event happens often enough to observe in one long run.
- Use [LAMMPS](lammps.md) for the dynamics engine in non-biomolecular systems. WESTPA drives any engine through its propagator.
- A bad progress coordinate does not break WE. It makes the sampling inefficient, because bins then do not separate the states.

## Install it yourself

The conda command below resolves for WESTPA 2022.16 on conda-forge, including linux-aarch64 and osx-arm64:

```
micromamba create -n west -c conda-forge westpa=2022.16
```

The WESTPA documentation also describes a pip route. A WESTPA project is a directory with `west.cfg`, a system module that defines the bins, a propagator, and basis states. `w_init` builds `west.h5`, `w_run` runs the iterations, and `w_pdist`, `w_assign` and `w_direct` analyse the result.

## Run the tested example

This recipe builds WESTPA in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.9 s.

1. Download [westpa-recipe.tar.gz](https://biosimhub.pages.dev/guides/westpa/westpa-recipe.tar.gz) (Dockerfile, run_westpa.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf westpa-recipe.tar.gz
   cd westpa
   sh run.sh
   ```

![Terminal recording of the WESTPA example run](https://biosimhub.pages.dev/media/westpa/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/westpa:2022.16 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/westpa:2022.16 python /opt/run_westpa.py --iterations 60 \
    --steps 20 --walkers 4 --bin-width 0.5 --start 8 \
    --sigma 0.0316228 --target 5 --seed 42 > out/westpa_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `bstates/bstates.txt` | 12 B |
| `bstates/start` | 1 B |
| `result.json` | 207 B |
| `summary.csv` | 3.7 KB |
| `west.cfg` | 547 B |
| `west.h5` | 594.4 KB |
| `westpa_stdout.txt` | 2.5 KB |
| `wsystem.py` | 3.2 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/westpa/result-dark.png"><img src="https://biosimhub.pages.dev/media/westpa/result.png" alt="Plot of the WESTPA example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>bstates/bstates.txt</code></summary>

```
0 1.0 start
```

</details>

<details><summary>First lines of <code>result.json</code></summary>

```
{
 "iterations": 60,
 "final_segments": 52,
 "min_x_reached": 3.497194290161133,
 "total_segments": 1872,
 "final_weight_below_target": 0.00134005514510966,
 "final_total_weight": 1.0,
 "wall_seconds": 2.1
}
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
iteration,segments,min_x,weighted_mean_x,weight_below_target,total_weight
1,4,7.708662509918213,7.855693340301514,0.0,1.0
2,8,7.6831488609313965,7.907665133476257,0.0,1.0
3,8,7.652306079864502,7.9883206486701965,0.0,1.0
4,8,7.730563640594482,7.951136469841003,0.0,1.0
5,8,7.516561508178711,7.831844985485077,0.0,1.0
6,8,7.374719142913818,7.784593343734741,0.0,1.0
7,12,7.297518730163574,7.778115630149841,0.0,1.0
8,12,7.128674030303955,7.846809417009354,0.0,1.0
9,12,7.212051868438721,7.9046889543533325,0.0,1.0
10,16,7.003252983093262,7.858072489500046,0.0,1.0
11,16,6.7860026359558105,7.810250446200371,0.0,1.0
```

</details>

<details><summary>First lines of <code>west.cfg</code></summary>

```
---
west:
  system:
    driver: wsystem.System
    module_path: $WEST_SIM_ROOT
  drivers:
    we_driver: wsystem.SeededDriver
  propagation:
    max_total_iterations: 60
    propagator: wsystem.Propagator
    gen_istates: true
    block_size: 10000
```

</details>

<details><summary>First lines of <code>westpa_stdout.txt</code></summary>

```
System is being built only off of the system driver
Creating HDF5 file '/work/out/west.h5'
0 target state(s) present
Calculating progress coordinate values for basis states.
1 basis state(s) present
Calculating progress coordinate values for start states.
0 start state(s) present
Preparing initial states

        Total bins:            20
        Initial replicas:      4 in 1 bins, total weight = 1
        Total target replicas: 80
```

</details>

<details><summary>First lines of <code>wsystem.py</code></summary>

```
import itertools

import numpy as np
from numpy.random import Generator, MT19937
from westpa.core.segment import Segment
from westpa.core.binning import RectilinearBinMapper
from westpa.core.propagators import WESTPropagator
from westpa.core.systems import WESTSystem
from westpa.core.we_driver import WEDriver

PARAMS = {'steps': 20, 'walkers': 4, 'bin_width': 0.5, 'start': 8.0, 'sigma': 0.0316228, 'seed': 42}
PCOORD_LEN = PARAMS["steps"] + 1
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--iterations` | Weighted-ensemble iterations | 60 | 1 to 500 |
| `--steps` | Langevin steps per segment | 20 | 1 to 200 |
| `--walkers` | Target walkers per bin | 4 | 1 to 20 |
| `--bin-width` | Bin width along x | 0.5 | 0.1 to 2 |
| `--start` | Start position x | 8 | 1 to 9.9 |
| `--sigma` | Noise per step (sqrt(2 D dt)) | 0.0316228 | 0.005 to 0.2 |
| `--target` | Report weight below this x | 5 | 0.5 to 9.5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_westpa.py` writes the project files, calls `w_init` and `w_run` with the serial work manager, and then reads `west.h5`. It writes `west.cfg` and `wsystem.py` (the project), `west.h5` (all walkers, weights and progress coordinates), `summary.csv` (one row per iteration) and `result.json`.

- `result.json` for the default run: 60 iterations, 1872 segments run in total, and 52 walkers alive in the last iteration. The lowest x any walker reached is 3.50.
- `summary.csv` has the columns `iteration`, `segments`, `min_x`, `weighted_mean_x`, `weight_below_target` and `total_weight`. Iteration 1 starts 4 walkers in one bin. Iteration 2 has 8, and iteration 7 has 12. The walker count grows as walkers diffuse into new bins, and each bin keeps up to 4 walkers.
- `weight_below_target` is the total weight of walkers that end an iteration below x = 5. At iteration 60 it is 0.00134, so about 0.13 % of the probability is across the first barrier. The weights still sum to 1.0, as they must.
- `total_weight` stays at 1.0 in every row. A drift in this column would mean a resampling bug.

The weighted mean x stays near 8, because almost all the weight remains in the starting well. The rare tail is where WE adds information. The weights make that tail an estimate of its true probability, not a count of walkers.

## Your own runs

Each run below changes one value from the example (seed 42, 60 iterations, 4 walkers per bin, bin width 0.5).

- **No weighted ensemble.** `--bin-width 10 --walkers 1` puts everything in one bin with one walker, so there is no splitting. It ran 60 segments and the lowest x was 6.72. Ordinary dynamics did not cross the first barrier.
- **More walkers per bin.** `--walkers 8` ran 4768 segments, finished with 128 walkers and reached x = 2.30. The weight below x = 5 was 0.0082.
- **Longer run.** `--iterations 200` ran 11,580 segments and reached x = 0.52, inside the deep well. The weight below x = 5 grew to 0.065.
- **Another seed.** `--seed 7` ran 2204 segments, reached x = 1.18 and put 0.0064 of the weight below x = 5. The tail estimate changes by a factor of about 5 between seeds 42 and 7, so rare-event weights need replicate runs.
- **Wide bins.** `--bin-width 1.0` ran 844 segments, finished with 20 walkers and reached only x = 5.67. Weight below x = 5 was 0.0, because bins that wide separate the barrier crossings poorly.

## Pitfalls

- **Runs are not repeatable out of the box.** WESTPA keeps the walkers of a bin in a Python set and breaks weight ties by memory address, so two runs with the same inputs diverged at iteration 3. The helper script fixes the walker order and seeds the resampling, which makes seed 42 give the numbers above every time. A stock project needs the same care if you want exact reruns.
- **One run is one sample.** The weights are unbiased in expectation, but a single run gave 0.0013 and another seed gave 0.0064 for the same quantity. Run replicates and report the spread.
- **Bin width trades cost for coverage.** A width of 1.0 reached x = 5.67 and a width of 0.5 reached 3.50 in the same 60 iterations.
- **Segment length matters.** The default is 20 Langevin steps per segment. A segment must be long enough for the progress coordinate to move, and short enough to resample often.
- **Serial work manager.** The recipe runs on one CPU. Production WESTPA uses the `processes`, `zmq` or MPI work managers.

## Further reading

- WESTPA documentation: https://westpa.readthedocs.io
- Source: https://github.com/westpa/westpa
- Paper: Russo JD et al. (2022) WESTPA 2.0: High-performance upgrades for weighted ensemble simulations and analysis of longer-timescale applications. J Chem Theory Comput 18:638-649. https://doi.org/10.1021/acs.jctc.1c01154

---

Cite: Russo JD, et al. (2022). WESTPA 2.0: High-performance upgrades for weighted ensemble simulations and analysis of longer-timescale applications. J Chem Theory Comput 18:638-649. doi:10.1021/acs.jctc.1c01154

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/westpa).
