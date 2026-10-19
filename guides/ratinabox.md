# RatInABox

> Simulate a rat exploring a square arena and the synthetic firing of place cells and grid cells along its path.

Licence: MIT · [Source code](https://github.com/RatInABox-Lab/RatInABox)

## What it simulates

RatInABox generates synthetic behaviour and synthetic neural data for spatial cell types. An `Agent` (the "rat") moves through a continuous 1D or 2D `Environment`, and populations of `Neurons` fire according to where the agent is and how it moves. Nothing is learned from recordings: the firing rate is a function of position and velocity.

The agent follows a smooth random policy. Speed and rotation are Ornstein-Uhlenbeck processes whose default parameters, per the README, are fit to real rat locomotion data from Sargolini et al. (2006). You can also give it your own trajectory or steer it with a policy. Environments can have walls, holes, objects and polygon boundaries, with solid or periodic edges.

Premade cell types include `PlaceCells`, `GridCells`, `BoundaryVectorCells`, `ObjectVectorCells`, `HeadDirectionCells`, `VelocityCells`, `SpeedCells` and `FieldOfViewNeurons`. Generic `FeedForwardLayer` and `NeuralNetworkNeurons` let you stack cells into small networks. Cells can be rate-based or spiking.

## When to use it

Use RatInABox for test data on spatial coding: decoding position from firing, training a network on grid-cell input, or a reinforcement-learning task with a moving agent.

- Use NEST, Brian 2 or [PyNN](pynn.md) when the neurons themselves must be simulated with membrane dynamics.
- Use [neurolib](neurolib.md) for whole-brain population models.
- Use a gridworld or gymnasium environment for discrete-state reinforcement learning tasks. The README notes that RatInABox is fully continuous in space.

RatInABox does not simulate ion channels or synapses.

## Install

The README gives:

```
pip install ratinabox
```

PyPI lists 1.15.3 (released February 2025) as current. It needs numpy, scipy, matplotlib and shapely, all installed automatically. It is not on conda-forge. For the development version, clone the repository and run `pip install -e .`. An optional `gymnasium` extra adds a wrapper for the PettingZoo and gymnasium API.

The licence is MIT.

## A first run

Adapted from the README's [simple example](https://github.com/RatInABox-Lab/RatInABox/blob/main/demos/simple_example.ipynb), copied there as code:

```python
import ratinabox
from ratinabox.Environment import Environment
from ratinabox.Agent import Agent
from ratinabox.Neurons import *

Env = Environment()
Ag = Agent(Env)
PCs = PlaceCells(Ag)

for i in range(int(20 / Ag.dt)):
    Ag.update()
    PCs.update()

print(Ag.history['pos'][:10])
print(PCs.history['firingrate'][:10])
fig, ax = Ag.plot_trajectory()
fig, ax = PCs.plot_rate_timeseries()
```

The default time step `Ag.dt` is 10 ms, so the loop above runs 2000 steps for 20 s of exploration. The README says one minute of exploration of 100 place cells at dt = 10 ms takes about 2 seconds on a laptop without a GPU.

## Run the tested example

This recipe builds RatInABox in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.8 s.

1. Download [ratinabox-recipe.tar.gz](https://biosimhub.pages.dev/guides/ratinabox/ratinabox-recipe.tar.gz) (Dockerfile, run_riab.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf ratinabox-recipe.tar.gz
   cd ratinabox
   sh run.sh
   ```

![Terminal recording of the RatInABox example run](https://biosimhub.pages.dev/media/ratinabox/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/ratinabox:1.15.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/ratinabox:1.15.3 python /opt/run_riab.py --duration 60 --place-cells 20 \
    --grid-cells 10 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `activity.csv` | 967.1 KB |
| `place_rate_maps.png` | 105.2 KB |
| `run_log.txt` | 555 B |
| `trajectory.png` | 27.8 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/ratinabox/result-dark.png"><img src="https://biosimhub.pages.dev/media/ratinabox/result.png" alt="Plot of the RatInABox example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>activity.csv</code></summary>

```
time_s,x_m,y_m,place0_hz,place1_hz,place2_hz,place3_hz,place4_hz,place5_hz,place6_hz,place7_hz,place8_hz,place9_hz,place10_hz,place11_hz,place12_hz,place13_hz,place14_hz,place15_hz,place16_hz,place17_
5.000000000000000278e-02,3.735243198485004856e-01,9.457703682336541240e-01,1.794523474040141142e-05,2.227819589236547558e-05,6.557277912318410244e-05,4.156382187472144845e-07,2.791927642458841285e-02,
1.000000000000000056e-01,3.727144424275285473e-01,9.403158912430034100e-01,2.038914293208735328e-05,2.529325527274022220e-05,7.275185295871680873e-05,4.664003482237179574e-07,3.001297552882028694e-02,
1.500000000000000222e-01,3.720936788593546263e-01,9.365709265322824661e-01,2.225603643088040206e-05,2.758742182516888249e-05,7.805476606664861516e-05,5.041209665254820887e-07,3.153526697432482845e-02,
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
WARNING: This figure has not been saved.
    • To AUTOMATICALLY save all plots (recommended), set  `ratinabox.autosave_plots = True`
    • To MANUALLY save plots, call                        `ratinabox.utils.save_figure(figure_object, save_title).
      This warning will not be shown again
HINT: You can stylize plots to make them look like repo/paper by calling `ratinabox.stylize_plots()`
      This hint will not be shown again
done: 1200 steps of 0.05 s, 20 place cells, 10 grid cells, mean place-cell rate 0.181 Hz, mean grid-cell rate 0.171 Hz
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--duration` | Exploration time (s) | 60 | 5 to 600 |
| `--place-cells` | Place cells | 20 | 1 to 200 |
| `--grid-cells` | Grid cells | 10 | 1 to 200 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

Everything is stored in each object's `history` dictionary, one entry per step:

- `Ag.history['t']` is time in seconds, and `Ag.history['pos']` is a list of (x, y) positions in metres. The default arena is 1 m by 1 m.
- `PCs.history['firingrate']` is a list of vectors, one value per cell, in Hz.
- `Ag.plot_trajectory()` draws the path. `PCs.plot_rate_timeseries()` plots firing rate against time. `PCs.plot_rate_map()` draws each cell's receptive field.

Place cells show a single bump of activity where the agent crosses the field. Grid cells show a hexagonal lattice of fields. These shapes are the check that the cell type does what it should.

## Pitfalls

- **You write the loop.** Nothing runs until you call `Ag.update()` and then `update()` on each Neurons object, in that order.
- **Two time units.** `dt` is in seconds. Speeds are in m/s and lengths in metres.
- **Seeding.** The random trajectory draws from numpy. Call `np.random.seed(...)` before creating objects when you need the same path twice.
- **Walls slow things down.** The README advises building curved boundaries from many small walls sparingly, since wall-responsive cells such as boundary vector cells get slower.
- **History grows.** The history lists keep every step. A 10-minute run with many cells holds many thousands of vectors in memory.
- **Plot windows.** On a server set `MPLBACKEND=Agg` and save figures to files.

## Further reading

- README and feature list: https://github.com/RatInABox-Lab/RatInABox
- Demos: https://github.com/RatInABox-Lab/RatInABox/tree/main/demos
- Paper (open access): https://elifesciences.org/articles/85274
- Citation: George TM, Rastogi M, de Cothi W, Clopath C, Stachenfeld K, Barry C (2024). RatInABox, a toolkit for modelling locomotion and neuronal activity in continuous environments. eLife 13:e85274. https://doi.org/10.7554/eLife.85274

---

Cite: George TM, Rastogi M, de Cothi W, Clopath C, Stachenfeld K, Barry C (2024). RatInABox, a toolkit for modelling locomotion and neuronal activity in continuous environments. eLife 13:e85274. doi:10.7554/eLife.85274

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/ratinabox).
