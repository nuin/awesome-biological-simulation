# ReaDDy

> Particle-based reaction-diffusion of a reversible A + B <-> C reaction in a periodic box, returning particle counts over time.

Licence: BSD-3-Clause · [Source code](https://github.com/readdy/readdy)

## What it simulates

ReaDDy simulates particles that diffuse and react in 3D space. Each particle is a point. It moves by overdamped Brownian dynamics. A reaction happens between two particles when they come closer than a reaction radius. Reaction rates are microscopic rates with units of inverse time. The per-step probability is p = 1 - exp(-rate * dt).

You describe species, diffusion constants and reactions in Python, place particles, and run. ReaDDy can add potentials, polymer bonds and topologies. The example on this page uses none of those. It runs one reversible reaction, A + B <-> C, in a cubic box of edge 10. It returns the count of A, B and C over time.

The key assumption is the spatial resolution. Particles have no volume unless you add an interaction potential. The fusion reaction is evaluated on particle pairs that are within the radius.

## When to use it

Use ReaDDy when space matters in a reaction network:

- Does crowding or slow diffusion lower the binding rate below the well-mixed value?
- How many complexes form in a small compartment with a few hundred molecules?
- What do reactions do on polymers, membranes or other bonded structures?

[GillesPy2](gillespy2.md) on biosimhub fits better for well-mixed stochastic models, where space does not matter and runs are much cheaper. [Cytosim](cytosim.md) fits filament mechanics.

## Install it yourself

The README gives conda as the preferred route, on Mac and Linux only. The dry run `micromamba create -n t --dry-run -c conda-forge -c bioconda readdy=2.0.14` resolves readdy 2.0.14 on linux-64.

```
conda create -n readdy -c conda-forge readdy=2.0.14
conda activate readdy
```

The recipe's image uses the same package and runs the single-threaded kernel. The minimal Python script follows the ReaDDy docs for the system and the simulation:

```python
import numpy as np
import readdy

system = readdy.ReactionDiffusionSystem(box_size=[10., 10., 10.], unit_system=None)
for name in ("A", "B", "C"):
    system.add_species(name, diffusion_constant=1.)
system.reactions.add("fusion: A +(1) B -> C", rate=1.)
system.reactions.add("fission: C -> A +(1) B", rate=0.1)

sim = system.simulation(kernel="SingleCPU")
sim.output_file = "traj.h5"
sim.add_particles("A", np.random.uniform(-5, 5, size=(100, 3)))
sim.add_particles("B", np.random.uniform(-5, 5, size=(100, 3)))
sim.observe.number_of_particles(stride=25, types=["A", "B", "C"], callback=print)
sim.run(5000, 0.01)
```

With `unit_system=None` the system is unitless and `kbt` is 1. The default unit system is nanometers, nanoseconds and kJ/mol. In the recipe's image the box has `periodic_boundary_conditions` of `[True, True, True]`.

## Run the tested example

This recipe builds ReaDDy in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 1.5 s. ReaDDy has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [readdy-recipe.tar.gz](https://biosimhub.pages.dev/guides/readdy/readdy-recipe.tar.gz) (Dockerfile, run_readdy.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf readdy-recipe.tar.gz
   cd readdy
   sh run.sh
   ```

![Terminal recording of the ReaDDy example run](https://biosimhub.pages.dev/media/readdy/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/readdy:2.0.14 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/readdy:2.0.14 python /opt/run_readdy.py --box 10 --n_a 100 \
    --n_b 100 --diffusion 1 --radius 1 --fusion_rate 1 \
    --fission_rate 0.1 --steps 5000 --dt 0.01 \
    --seed 42 > out/readdy_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `particle_counts.csv` | 4.0 KB |
| `readdy_log.txt` | 3.4 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/readdy/result-dark.png"><img src="https://biosimhub.pages.dev/media/readdy/result.png" alt="Plot of the ReaDDy example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>particle_counts.csv</code></summary>

```
step,time,A,B,C
0,0.0,100,100,0
25,0.25,91,91,9
50,0.5,86,86,14
75,0.75,78,78,22
100,1.0,74,74,26
125,1.25,72,72,28
150,1.5,70,70,30
175,1.75,68,68,32
200,2.0,66,66,34
225,2.25,61,61,39
250,2.5,58,58,42
```

</details>

<details><summary>First lines of <code>readdy_log.txt</code></summary>

```
final counts A,B,C: [40, 40, 60]
[2026-10-12 06:07:32] [info] Simulation progress: 100 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 200 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 300 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 400 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 500 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 600 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 700 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 800 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 900 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 1000 / 5000 steps
[2026-10-12 06:07:32] [info] Simulation progress: 1100 / 5000 steps
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--box` | Box edge length | 10 | 2 to 100 |
| `--n_a` | Initial particles of A | 100 | 0 to 2000 |
| `--n_b` | Initial particles of B | 100 | 0 to 2000 |
| `--diffusion` | Diffusion constant | 1 | 0.01 to 100 |
| `--radius` | Reaction radius | 1 | 0.1 to 5 |
| `--fusion_rate` | Fusion rate (A + B -> C) | 1 | 0 to 100 |
| `--fission_rate` | Fission rate (C -> A + B) | 0.1 | 0 to 100 |
| `--steps` | Time steps | 5000 | 10 to 200000 |
| `--dt` | Time step | 0.01 | 0.0001 to 0.1 |
| `--seed` | Seed for initial positions (the engine's own RNG is not seedable) | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper script `run_readdy.py` wraps the script above. It builds the system from the command-line values, scatters the particles uniformly in the box, and records counts every `steps // 200` steps. With 5000 steps that is every 25 steps, which gives 201 rows in `particle_counts.csv` (4052 bytes).

The file has the columns `step,time,A,B,C`. It starts at `0,0.0,100,100,0`. At step 25 (time 0.25) it reads 91, 91 and 9. By time 2.5 the line is 58, 58, 42. A and B always match because each reaction removes one of each and starts with 100 of each.

`readdy_log.txt` begins with the helper's line `final counts A,B,C: [40, 40, 60]`. ReaDDy's own progress lines follow, one per 100 steps, in the form `Simulation progress: 100 / 5000 steps`. At time 50 the system holds 60 complexes.

The helper also writes a trajectory file to `/tmp` inside the image.

## Your own runs

Copy the docker run line from the recipe and change values. All runs used 5000 steps of 0.01.

1. **Faster fusion.** Set `--fusion_rate 10`. The final counts changed from 40, 40, 60 to 17, 17, 83. More A and B ended up bound.
2. **Faster fission.** Set `--fission_rate 1`. The final counts were 78, 78, 22. C splits apart almost as fast as it forms.
3. **Faster diffusion.** Set `--diffusion 10`. At time 1.5 the example run has 30 complexes. The default seed with `--diffusion 10` gave 43. The final counts were 45, 45, 55 against 40, 40, 60.

A different `--seed 7` gave the same final counts of 40, 40, 60 as seed 42, but a different early path. At time 0.25 it had 7 complexes, against 9 for seed 42.

## Pitfalls

- **The seed is partial.** The `--seed` value only sets the initial positions. ReaDDy's own random generator is not seedable, so repeat runs of the same seed can differ.
- **Rates are per unit time of your system.** With `unit_system=None` the numbers have no units. Keep diffusion, radius, rate and time step in one consistent set.
- **Time step against radius.** A particle should move a small fraction of the reaction radius per step. At D = 1 and dt = 0.01 the root-mean-square step is about 0.14 per axis (sqrt(2 D dt)), against a radius of 1.
- **Box and counts set the concentration.** 100 particles in a box of edge 10 is 0.1 per unit volume. Doubling the edge divides the concentration by 8.
- **Linux amd64 only.** The recipe's image runs as `linux/amd64`. On Apple silicon it runs under emulation and is slower.

## Further reading

- Documentation: https://readdy.github.io/
- System configuration: https://readdy.github.io/system.html
- Simulation and observables: https://readdy.github.io/simulation.html
- Hoffmann M, Frohner C, Noe F (2019). ReaDDy 2: Fast and flexible software framework for interacting-particle reaction dynamics. PLoS Comput Biol 15:e1006830. https://doi.org/10.1371/journal.pcbi.1006830

---

Cite: Hoffmann M, Frohner C, Noe F (2019). ReaDDy 2: Fast and flexible software framework for interacting-particle reaction dynamics. PLoS Comput Biol 15:e1006830. doi:10.1371/journal.pcbi.1006830

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/readdy).
