# Cytosim

> 2D Brownian-dynamics simulation of flexible cytoskeletal filaments with molecular motors and crosslinkers, from a .cym config file.

Licence: GPL-3.0-or-later · [Source code](https://gitlab.com/f-nedelec/cytosim)

## What it simulates

Cytosim simulates flexible cytoskeletal filaments in 2D or 3D. It also handles the molecules that bind them, such as motors and crosslinkers. Filaments are chains of points that bend with a set rigidity. The solver moves all points together with Brownian (overdamped Langevin) dynamics, so thermal motion, viscous drag and bending forces are all in the same step.

You write a plain-text `.cym` configuration file. It defines a space, a fiber type and how many fibers to create. A `run` command then advances time and saves frames. The example on this page puts 10 microtubules of length 4 um and rigidity 20 pN.um^2 into a circular cell of radius 5 um. The microtubules bend against the wall and each other.

The key assumption is the physical unit system. Cytosim does not check units. It expects micrometers, picoNewtons and seconds, with a default viscosity of 1 pN.s/um^2 and kT of 0.0042 pN.um. Mixed units give wrong answers without any error.

## When to use it

Use Cytosim for questions about filament networks and their mechanics:

- How do microtubules buckle or align when confined to a cell?
- What does an aster of microtubules look like when motors pull on it?
- How fast does a spindle-like bundle form with crosslinkers?

On biosimhub, [GROMACS](gromacs.md) and [LAMMPS](lammps.md) fit better when you need atoms or coarse-grained beads rather than whole filaments. The biosimhub copy of Cytosim runs the 2D engine `sim2D` only, with no viewer.

## Install it yourself

The conda-forge package pins to version 1.0.5. A dry run of `micromamba create -n t --dry-run -c conda-forge -c bioconda cytosim=1.0.5` resolved cytosim 1.0.5 with Python 3.14 on linux-64.

```
conda create -n cytosim -c conda-forge cytosim=1.0.5
conda activate cytosim
```

The Cytosim README says this installs `sim2D`, `sim3D`, `play2D` and `play3D`. The recipe's image has `sim2D` and `sim3D`. The minimal command is one line:

```
sim2D config.cym
```

`sim2D --help` lists the options. A file name ending in `.cym` runs that file. A `+` argument sends messages to the terminal instead of `messages.cmo`. A `-` argument suppresses them.

The README also shows a Python module. `import cytosim2D`, then `sim = cytosim2D.start("example.cym")`, `sim.run(10)` and `sim.save()`.

## Run the tested example

This recipe builds Cytosim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.5 s. Cytosim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [cytosim-recipe.tar.gz](https://biosimhub.pages.dev/guides/cytosim/cytosim-recipe.tar.gz) (Dockerfile, example config.cym, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf cytosim-recipe.tar.gz
   cd cytosim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/cytosim:1.0.5 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/cytosim:1.0.5 sim2D /work/in/config.cym
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `messages.cmo` | 2.0 KB |
| `objects.cmo` | 12.2 KB |
| `properties.cmp` | 437 B |

<details><summary>First lines of <code>messages.cmo</code></summary>

```
% Mon Oct 12 06:06:21 2026 PID 7
   Dimension 2  Periodic 1  AttachPool 1  Precision 8
   Fiber has lattice 0 density 0 family 0 glue 0 bind_closest 1
   Built Oct 14 2025 13:25:54 with 14.3.0
   Code version unknown (no assertions)
   FiberGrid of dim 2 has 484 voxels:  [-5.5, 5.5]/22 = 0.5 [-5.5, 5.5]/22 = 0.5
% Mon Oct 12 06:06:22 2026
F1          1.00s   CPU      0.060s           0s
	size 2*90 kern 9 SMS1x 0 (96) SMSBDx +4*0 (0) count   10 residual 0.00035959 
	size 2*90 kern 9 SMS1x 0 (96) SMSBDx +4*0 (0) count   12 residual 0.000164382
F2          2.00s   CPU      0.009s           0s
	size 2*90 kern 9 SMS1x 0 (96) count   12 residual 0.000166971
```

</details>

<details><summary>First lines of <code>properties.cmp</code></summary>

```
% Mon Oct 12 06:06:21 2026
% Cytosim property file, pid 7

set simul system
{
 time_step            = 0.005;
 random_seed          = 268818617;
 binding_grid_step    = 0.5;
}

set space cell
{
```

</details>


## Reading the output

The example writes three files in the output folder.

- `messages.cmo` (2051 bytes) is the text log. It starts with the build line and the grid. The grid line reads `FiberGrid of dim 2 has 484 voxels`, which is a 22 by 22 grid of 0.5 um steps from -5.5 to 5.5 um. One line per frame follows, such as `F1 1.00s CPU 0.060s`. The lines under it show the solver: `size 2*90` means 2 dimensions times 90 points, which is 10 fibers with 9 points each. The `count` and `residual` values report each solver pass. The residual is about 0.0002 to 0.0004 in the first frames.
- `properties.cmp` (437 bytes) lists every property set after defaults. It shows `time_step = 0.005`, the `random_seed` Cytosim picked, and the `confine` setting of the fiber.
- `objects.cmo` (12541 bytes) is a binary trajectory. It holds 11 frames, from `#time 0.000000 sec` to `#time 10.000000 sec`. 2000 steps of 0.005 s make 10 s, and `nb_frames = 10` saves ten frames after the first.

The example log shows CPU times of 0.114 s for frame 8 and 0.016 s for frame 10. The whole job took 0.5 s.

The binary `objects.cmo` frames are read by Cytosim's own tools (`play2D`, `report`) or the Python module. A text parser cannot read them. The `report` tool is not in the recipe's image.

## Your own runs

Copy the docker run line from the recipe and change the config file. All three runs below used the 1.0.5 image.

1. **More fibers.** Change `new 10 microtubule` to `new 20 microtubule`. The solver line changed from `size 2*90` to `size 2*180`. `objects.cmo` grew from 12541 to 22881 bytes. The last frame took 0.052 s of CPU against 0.016 s.
2. **Softer filaments.** Change `rigidity = 20` to `rigidity = 1`. The sizes stayed at `2*90` and 12541 bytes. The first-frame solver count dropped from 12 to 4 iterations. The solver needed fewer passes for softer fibers in this run.
3. **A fixed seed.** Add `random_seed = 7` inside `set simul system`. The value appeared in `properties.cmp`. Two runs with that seed still wrote `objects.cmo` files that differed in 8040 bytes, so treat the output as one random sample and compare statistics over several runs.

## Pitfalls

- **Wrong units.** Lengths are in um, forces in pN, time in s. A rigidity of 20 means 20 pN.um^2. Convert before you write the file.
- **No seed set.** Each run drew a different `random_seed` (268818617 in the stored example, other values in repeat runs). Two runs of the same file are two samples.
- **Time step.** The example uses `time_step = 0.005` s. Check the `residual` column in `messages.cmo` after you change it or the fiber stiffness.
- **Fibers leave the space.** A fiber needs a `confine` setting or it can leave the cell. The example uses `confine = inside, 200`, which `properties.cmp` records as `confine = 1, 200, 200, first`.
- **Binary output.** `objects.cmo` is not text. Use Cytosim's tools to read it.

## Further reading

- Cytosim source and README: https://gitlab.com/f-nedelec/cytosim
- Units: https://gitlab.com/f-nedelec/cytosim/-/blob/master/doc/sim/units.md
- Nedelec F, Foethke D (2007). Collective Langevin dynamics of flexible cytoskeletal fibers. New J Phys 9:427. https://doi.org/10.1088/1367-2630/9/11/427

---

Cite: Nedelec F, Foethke D (2007). Collective Langevin dynamics of flexible cytoskeletal fibers. New J Phys 9:427. doi:10.1088/1367-2630/9/11/427

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cytosim).
