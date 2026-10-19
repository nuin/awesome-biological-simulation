# OpenPathSampling

> Sample transition paths between two states of a 2D double-well toy system with one-way shooting, and report acceptance, path length and the last accepted path.

Licence: MIT · [Source code](https://github.com/openpathsampling/openpathsampling)

## What it simulates

OpenPathSampling (OPS) samples trajectories instead of configurations. A rare event, such as a protein folding or a molecule crossing a barrier, is too infrequent to catch with plain dynamics. Path sampling takes one trajectory that already made the transition and proposes new ones by perturbing it, then accepts or rejects each proposal with a Monte Carlo rule. Every accepted path is a full transition from state A to state B.

OPS is a Python framework. It does not integrate forces itself in the usual case. It drives an MD engine such as OpenMM or GROMACS and also ships a small toy engine for model potentials.

The recipe runs transition path sampling (TPS) with one-way shooting on the toy engine. A particle moves on a 2D double-well surface under Langevin BAOAB dynamics. The two wells sit at x = -0.5 and x = +0.5. State A is x < -0.3 and state B is x > 0.3. You choose the temperature, the friction, the time step, the stored-frame interval, the number of shooting moves, the maximum path length and the seed.

The key assumption is that the dynamics are Markovian and that A and B are well separated. Shooting points are drawn uniformly along the current path.

## When to use it

Use OPS to study the mechanism and rate of an event that plain MD seldom shows: nucleation, conformational switching, ligand unbinding.

- Use [OpenMM](openmm.md) or [GROMACS](gromacs.md) for ordinary MD with no path ensemble.
- Use [LAMMPS](lammps.md) for materials force fields. The recipe here uses only OPS's toy engine.
- Use a collective-variable method such as metadynamics when you want a free-energy surface and not the transition paths.

## Install it yourself

OpenPathSampling 1.7.0 comes from conda-forge. The recipe's image resolved it with Python 3.12.15 and NumPy 1.26.4:

```
micromamba create -n ops -c conda-forge openpathsampling=1.7.0
```

The project also publishes it on PyPI (`pip install openpathsampling`). MD engines are separate installs; the toy engine needs nothing extra.

A minimal script with the same calls as the helper. It seeds both random sources: NumPy for the integrator, and OPS's own generator for shooting points and accept/reject draws.

```python
import numpy as np
import openpathsampling as paths
import openpathsampling.engines.toy as toys
from openpathsampling.rng import default_rng

np.random.seed(42)
default_rng().bit_generator.state = np.random.PCG64(42).state

pes = (toys.OuterWalls([1.0, 1.0], [0.0, 0.0])
       + toys.Gaussian(-0.7, [12.0, 0.5], [-0.5, 0.0])
       + toys.Gaussian(-0.7, [12.0, 0.5], [0.5, 0.0]))
topology = toys.Topology(n_spatial=2, masses=[1.0, 1.0], pes=pes)
integ = toys.LangevinBAOABIntegrator(dt=0.02, temperature=0.1, gamma=2.5)
engine = toys.Engine(options={"integ": integ, "n_frames_max": 5000,
                              "n_steps_per_frame": 10}, topology=topology)
start = toys.Snapshot(coordinates=np.array([[-0.5, 0.0]]),
                      velocities=np.array([[0.0, 0.0]]), engine=engine)
engine.current_snapshot = start

x = paths.FunctionCV("x", lambda s: s.xyz[0][0])
A = paths.CVDefinedVolume(x, float("-inf"), -0.3).named("A")
B = paths.CVDefinedVolume(x, 0.3, float("inf")).named("B")
network = paths.TPSNetwork(A, B)

traj = engine.generate(start, [lambda tr, trusted=None: not B(tr[-1])])
first_b = next(i for i, s in enumerate(traj) if B(s))
last_a = max(i for i in range(first_b) if A(traj[i]))
path = paths.Trajectory(traj[last_a:first_b + 1])

scheme = paths.OneWayShootingMoveScheme(network, selector=paths.UniformSelector(), engine=engine)
sset = scheme.initial_conditions_from_trajectories(path)
sampler = paths.PathSampling(storage=None, move_scheme=scheme, sample_set=sset)
sampler.run(50)
```

Plain dynamics from the bottom of A needed 2004 stored frames (20,040 integrator steps) to reach B once. The reactive part of that run, from the last frame in A to the first frame in B, is 11 frames (110 steps). With 50 shooting moves, 34 were accepted and the last path had 12 frames. Without seeding, one plain-dynamics run hit the 5000-frame limit and raised `EngineMaxLengthError`, so seed the run.

## Run the tested example

This recipe builds OpenPathSampling in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.4 s.

1. Download [openpathsampling-recipe.tar.gz](https://biosimhub.pages.dev/guides/openpathsampling/openpathsampling-recipe.tar.gz) (Dockerfile, run_tps.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf openpathsampling-recipe.tar.gz
   cd openpathsampling
   sh run.sh
   ```

![Terminal recording of the OpenPathSampling example run](https://biosimhub.pages.dev/media/openpathsampling/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/openpathsampling:1.7.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/openpathsampling:1.7.0 python -W ignore /opt/run_tps.py --temperature 0.1 \
    --gamma 2.5 --dt 0.02 --frame-steps 10 --moves 200 \
    --max-frames 5000 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `final_path.csv` | 215 B |
| `moves.csv` | 4.7 KB |
| `run_log.txt` | 309 B |
| `summary.json` | 269 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/openpathsampling/result-dark.png"><img src="https://biosimhub.pages.dev/media/openpathsampling/result.png" alt="Plot of the OpenPathSampling example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>final_path.csv</code></summary>

```
frame,x,y
0,-0.31805,-0.44347
1,-0.19374,-0.41853
2,-0.08655,-0.41119
3,-0.00967,-0.44078
4,0.01934,-0.43427
5,0.04044,-0.41533
6,0.04465,-0.39949
7,0.12267,-0.34542
8,0.21799,-0.30033
9,0.33643,-0.24512
```

</details>

<details><summary>First lines of <code>moves.csv</code></summary>

```
step,accepted,frames,x_min,x_max
1,1,11,-0.4489,0.4364
2,1,8,-0.3052,0.4364
3,0,8,-0.3052,0.4364
4,0,8,-0.3052,0.4364
5,0,8,-0.3052,0.4364
6,1,7,-0.3052,0.3068
7,0,7,-0.3052,0.3068
8,1,9,-0.3052,0.389
9,1,9,-0.3052,0.3598
10,1,8,-0.3052,0.3703
11,0,8,-0.3052,0.3703
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
initial path: 11 frames, found after 1 dynamics run(s)
{"temperature": 0.1, "gamma": 2.5, "dt": 0.02, "frame_steps": 10, "moves": 200, "seed": 42, "accepted": 115, "acceptance": 0.575, "initial_frames": 11, "final_frames": 10, "mean_frames": 11.1, "min_fr
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "temperature": 0.1,
 "gamma": 2.5,
 "dt": 0.02,
 "frame_steps": 10,
 "moves": 200,
 "seed": 42,
 "accepted": 115,
 "acceptance": 0.575,
 "initial_frames": 11,
 "final_frames": 10,
 "mean_frames": 11.1,
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--temperature` | Temperature kT (reduced units) | 0.1 | 0.07 to 0.3 |
| `--gamma` | Langevin friction (1/time) | 2.5 | 0.1 to 20 |
| `--dt` | Integrator time step | 0.02 | 0.005 to 0.05 |
| `--frame-steps` | Integrator steps per stored frame | 10 | 1 to 50 |
| `--moves` | One-way shooting moves | 200 | 10 to 2000 |
| `--max-frames` | Maximum frames per path | 5000 | 100 to 20000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example runs at kT = 0.1, friction 2.5, dt 0.02, 10 integrator steps per frame, 200 shooting moves and seed 42. It took 3.6 s. The helper first runs plain dynamics until the particle reaches B (11 frames after trimming, found on the first try), then shoots.

- `summary.json` (269 bytes): 115 of 200 moves accepted (acceptance 0.575). Path length averaged 11.1 frames, with a minimum of 7 and a maximum of 21. The final path has 10 frames and satisfies the A-to-B ensemble.
- `moves.csv` (4814 bytes) has one row per move: whether it was accepted, the path length, and the lowest and highest x on the path. In the first 100 moves 62 were accepted, in the last 100, 53. The highest x seen on any path is 0.53 and the lowest is -0.452.
- `final_path.csv` (215 bytes) lists the last accepted path. It starts at x = -0.318 in A, crosses the barrier near x = 0 at frames 3 to 4 and ends at x = 0.336 in B. The y coordinate stays between -0.44 and -0.25.
- `run_log.txt` has the initial-path line and the summary line.

An acceptance of 0.575 means more than half of the shooting moves produce a new path. A rejected move leaves the previous path in place, so `moves.csv` repeats the same path on those rows.

## Your own runs

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/out:/work/out" -w /work/out "$@"; }
dr biosimhub/openpathsampling:1.7.0 python -W ignore /opt/run_tps.py --temperature 0.07 --gamma 2.5 --dt 0.02 --frame-steps 10 --moves 200 --max-frames 5000 --seed 42
```

1. Colder, `--temperature 0.07`: 120 of 200 moves accepted (0.6), mean length 11.9 frames, range 5 to 17. The initial plain-dynamics path was longer, 16 frames against 11.
2. Heavy friction, `--gamma 10`: 96 of 200 accepted (0.48), mean length 18.7 frames, range 9 to 49. Stronger friction slows the crossing, so paths get longer, and the acceptance falls.
3. The same seed twice reproduced a 100-move run exactly (62 accepted, mean 10.8 frames, in both runs).

## Pitfalls

- Seed OPS's own generator as well as NumPy. Seeding only NumPy and Python's `random` gave 66, 69, 57 and 67 accepted moves in four runs of the same 100-move setup.
- Plain dynamics is the bottleneck at low temperature. At kT = 0.05 the helper searched for an A-to-B path and gave up with "no A to B path found". The recipe sets the minimum temperature to 0.07.
- Lengths are in stored frames. One frame is `frame_steps` integrator steps of `dt`.
- The toy potential is fixed. For other systems, build the engine and the states yourself, with OpenMM or GROMACS as the engine.
- The recipe runs TPS only. TIS or replica-exchange path sampling need extra ensembles and interface definitions.

## Further reading

- Toy engine examples in the source tree: https://github.com/openpathsampling/openpathsampling/tree/master/examples
- Source: https://github.com/openpathsampling/openpathsampling
- Swenson DWH, Prinz JH, Noe F, Chodera JD, Bolhuis PG (2019) J Chem Theory Comput 15:813-836. https://doi.org/10.1021/acs.jctc.8b00626

---

Cite: Swenson DWH, Prinz JH, Noe F, Chodera JD, Bolhuis PG (2019). OpenPathSampling: A Python framework for path sampling simulations. 1. Basics. J Chem Theory Comput 15:813-836. doi:10.1021/acs.jctc.8b00626

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openpathsampling).
