# pyafv

> Active finite Voronoi model of confluent epithelial tissue; simulates self-propelled cells and returns trajectories, tissue statistics and a final snapshot.

Licence: MIT · [Source code](https://github.com/wwang721/pyafv)

## What it simulates

pyafv simulates a 2D tissue with the active finite Voronoi (AFV) model. Each cell is a point. The cell shape comes from a Voronoi tessellation of the points, with a finite range. A cell has a maximal radius `r`, so a cell can have free boundaries against the medium. Standard vertex and Voronoi models cannot do this. Cells can detach, and the tissue can open or fragment.

Each cell has an area and a perimeter. Elastic terms pull the area toward a preferred area `A0` and the perimeter toward `P0`. The parameter `Lambda` is the tension difference between non-contacting edges and contacting edges. Each cell also self-propels with speed `v0` along a direction that diffuses at rate `dr`.

The example places 40 cells at random in a square of side 12.3 (that is sqrt(40 pi) * 1.1) and moves them for 300 steps of 0.05, so 15 time units. The key assumption is overdamped motion. Position changes by (force + v0 * direction) * dt, with no inertia.

## When to use it

Use pyafv to ask how activity, adhesion and preferred shape set the state of a cell collective:

- Does a tissue stay confluent, or do cells detach at a given speed?
- How do the mean area and the number of contacts change with the preferred perimeter?
- How big are the forces that hold neighbors together?

[tyssue](tyssue.md) models a fixed polygon network, where cells keep their neighbors. [Artistoo](artistoo.md) models deformable cells on a pixel grid. pyafv fits when cells move past each other and the tissue edge matters.

## Install it yourself

The package needs Python 3.10 up to 3.14. A dry run `micromamba create -n t --dry-run -c conda-forge -c bioconda pyafv=0.4.16` resolves pyafv 0.4.16 with Python 3.14.8 on linux-aarch64.

```
pip install pyafv==0.4.16
# or
conda create -n pyafv -c conda-forge pyafv=0.4.16
```

The minimal script from the package page builds the tessellation and the forces for 100 random cells:

```python
import numpy as np
import pyafv as afv

pts = np.random.rand(100, 2) * 10
params = afv.PhysicalParams(r=1.0)
sim = afv.FiniteVoronoiSimulator(pts, params)
diag = sim.build()
```

`build()` returns a dict with `forces`, `areas`, `perimeters`, `arclens`, `coord_nums`, `vertices`, `edges_type`, `regions` and `connections`. To move the cells, compute new positions and call `sim.update_positions(pts)`. `PhysicalParams` has these fields and defaults: `r=1.0`, `A0=pi`, `P0=4.8`, `KA=1.0`, `KP=1.0`, `Lambda=0.2`, `delta=None` (0.45 * r) and `seed=None`.

## Run the tested example

This recipe builds pyafv in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 1.3 s.

1. Download [pyafv-recipe.tar.gz](https://biosimhub.pages.dev/guides/pyafv/pyafv-recipe.tar.gz) (Dockerfile, run_afv.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pyafv-recipe.tar.gz
   cd pyafv
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pyafv:0.4.16 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pyafv:0.4.16 python /opt/run_afv.py --cells 40 --steps 300 \
    --dt 0.05 --v0 0.1 --dr 0.1 --p0 4.8 --lam 0.2 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 42 B |
| `summary.csv` | 20.8 KB |
| `tissue.png` | 52.4 KB |
| `trajectory.csv` | 18.9 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 40 cells, 300 steps, backend cython
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
step,time,mean_area,mean_perimeter,mean_contacts,mean_force
0,0.0,2.2917752279092625,5.667063461784797,2.35,2.409453748671232
1,0.05,2.3759863721410284,5.747999116990504,2.55,1.2369036444833479
2,0.1,2.3828824364297647,5.755142433092841,2.55,0.8028909859018784
3,0.15,2.3783907633031838,5.752573379547279,2.6,0.68868967978213
4,0.2,2.3692640252754655,5.747192117262174,2.6,0.5445358484878808
5,0.25,2.3604576169118685,5.738866603508552,2.6,0.44910429608380004
6,0.3,2.354248999702701,5.732821453000037,2.6,0.3809996285822037
7,0.35,2.3499325184369426,5.728413653363506,2.6,0.3317184735794566
8,0.4,2.3467786597866027,5.7245798828510175,2.65,0.38365882455938005
9,0.45,2.3438018015514106,5.718364621570094,2.65,0.3061719366390867
10,0.5,2.342224670619758,5.715165062003194,2.65,0.26677972693695395
```

</details>

<details><summary>First lines of <code>trajectory.csv</code></summary>

```
step,cell,x,y
0,0,9.543637078875292,5.411801559728699
0,1,10.587354358945829,8.599231690443835
0,2,1.161299056926641,12.03038036518012
0,3,9.385598957036866,9.692943758522787
0,4,1.5797667288639838,5.553700296966354
0,5,4.572303271538914,11.427921168755384
0,6,7.939488353713671,10.145457554259263
0,7,5.467731917237296,2.802076287184168
0,8,6.838574291937675,0.7869293518207436
0,9,10.205503988758203,7.789041499338989
0,10,9.34796527376245,4.3716528621763455
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--cells` | Number of cells | 40 | 4 to 200 |
| `--steps` | Time steps | 300 | 1 to 5000 |
| `--dt` | Time step | 0.05 | 0.001 to 0.2 |
| `--v0` | Self-propulsion speed | 0.1 | 0 to 2 |
| `--dr` | Rotational diffusion rate | 0.1 | 0 to 5 |
| `--p0` | Preferred perimeter | 4.8 | 2 to 8 |
| `--lam` | Edge tension difference (Lambda) | 0.2 | 0 to 2 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`run_afv.py` wraps the script above. At each step it calls `sim.build()`, records the means, moves the cells with `(F + v0 * n) * dt`, and turns each direction angle by a random amount of size `sqrt(2 * dr * dt)`. It ends with `sim.plot_2d()`.

The log has one line, `done: 40 cells, 300 steps, backend cython`. The Cython backend is the fast one. The package falls back to pure Python with a warning if it cannot load it.

`summary.csv` (21267 bytes) has 301 rows, one per step, with the means over cells. Step 0 shows a mean area of 2.292, a mean perimeter of 5.667, 2.35 contacts per cell and a mean force of 2.409. The force drops within 10 steps to 0.267 as the random start relaxes. Preferred area `A0` is pi, 3.14, so the cells stay compressed below it.

`trajectory.csv` (19344 bytes) holds the cell positions at 11 snapshots, every 30 steps, for 440 rows. `tissue.png` is the final tessellation.

## Your own runs

Copy the docker run line from the recipe and change values. The reference run is the default. At step 300 it has a mean area of 2.309, a mean perimeter of 5.652, 3.00 contacts and a mean force of 0.0834.

1. **Faster cells.** Set `--v0 0.5`. Contacts rose to 3.75 and the mean force to 0.442. The mean area was 2.264.
2. **Smaller preferred perimeter.** Set `--p0 3.6`. The mean area fell to 1.795 and the mean perimeter to 5.035. Contacts were 2.75.
3. **Higher tension difference.** Set `--lam 1.0`. The mean area fell to 2.128 and the perimeter to 5.483. Contacts rose to 3.35.

All runs used seed 42, so the start positions were the same.

## Pitfalls

- **Short runs.** The default covers 15 time units. The first rows of `summary.csv` show the start still relaxing, with the force at 2.409 at step 0. Read the last rows, and check that the means have stopped changing.
- **Step size.** Cells move (force + v0 * direction) * dt per step. With `--v0 0.5` the mean force rose from 0.083 to 0.442, so check the force column after raising speed or `dt`.
- **Seeds.** One seed sets the start positions, the directions and the noise. Use several seeds for a statement about a parameter.
- **Only means are saved.** `summary.csv` holds means over cells. Use `trajectory.csv` and `tissue.png` to look at single cells.
- **Parameter names.** The recipe's helper `--lam` is the package's `Lambda`, and `--p0` is `P0`. The helper fixes `r=1`, `A0=pi`, `KA=1` and `KP=1`.

## Further reading

- Package page: https://pypi.org/project/pyafv/
- Documentation: https://pyafv.readthedocs.io
- Source: https://github.com/wwang721/pyafv
- Wang W, Camley BA. Divergence of detachment forces in the finite Voronoi model. arXiv:2604.15481. https://doi.org/10.48550/arXiv.2604.15481

---

Cite: Wang W. pyafv, https://github.com/wwang721/pyafv

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pyafv).
