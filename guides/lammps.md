# LAMMPS

> Classical molecular dynamics of atoms, polymers and coarse-grained or biomolecular systems, driven by a LAMMPS input script.

Licence: GPL-2.0-only · [Source code](https://github.com/lammps/lammps)

**[Run LAMMPS in your browser](https://biosimhub.pages.dev/run/lammps/index.html)**: Lennard-Jones molecular dynamics (fcc melt, NVE) with the LAMMPS engine compiled to WebAssembly. Nothing to install; the first visit downloads about 10 MB.

## What it simulates

LAMMPS integrates Newton's equations for particles that interact through a force field you choose in a text script. It handles atoms, polymers, coarse-grained beads and full biomolecules. The script sets units, builds a box, picks pair styles, chooses a time integrator (a "fix"), and calls `run`.

Input is one script. Output is a log with thermodynamic rows (temperature, energy, pressure), plus any dump or data files the script writes. Both setups here use `units lj`: mass, length and energy are 1, and every number is a multiple of those. Temperature is T* = T kB / epsilon, density is rho* = rho sigma^dim / m, and thermo output divides extensive quantities by the atom count.

The key assumption is classical mechanics on a fixed pair potential. Here that is the 12-6 Lennard-Jones potential cut at 2.5 sigma. There are no electrons, no bond breaking, and no quantum effects.

## When to use it

- Phase behaviour and transport of simple fluids and solids: melting, diffusion, pressure against density.
- Polymers and coarse-grained models, where you write the potential yourself.
- Any system that needs a force field GROMACS or OpenMM do not ship.

Alternatives: [GROMACS](gromacs.md) fits solvated proteins and lipids, because it reads a ready topology and is tuned for them. [OpenMM](openmm.md) fits when you want a Python API and AMBER or CHARMM water boxes. [JAX MD](jax-md.md) fits when you need gradients through the simulation.

## Run it in your browser

The LAMMPS page runs the classic Lennard-Jones melt in WebAssembly. The first run downloads about 10 MB. The page uses the `lammps.js` 1.5.1 build, whose default build enables the MOLECULE package.

Controls:

- Lattice density (rho*): default 0.8442.
- Box size in fcc cells per side: default 6. Atoms = 4 x cells^3, so 6 gives 864.
- Initial temperature (T*): default 3.0.
- Steps (2000), timestep in tau (0.005), thermo output interval (20), velocity seed (87287).

Readouts:

- The chart plots temperature, potential energy per atom and total energy per atom against step.
- The canvas shows the final positions of atoms within 1 sigma of the box mid-plane, seen along z.
- The table lists atoms, steps, first and final temperature, energy drift, pressure and run time. The log is under the "LAMMPS log" toggle.

The same setup run in the recipe's container (22 Jul 2025 build) gave a temperature of 3.0 at step 0 and 1.649 at step 2000. Total energy went from -2.2786 to -2.2972 per atom, a change of 0.019. The page uses `neigh_modify every 20 delay 0 check no`, which rebuilds neighbour lists only every 20 steps, so total energy drifts a little. The browser build is a different LAMMPS release, so expect the same shape and slightly different digits.

Limits: one thread, a 200000-step cap, one fixed system. Install LAMMPS yourself for anything else.

## Install it yourself

LAMMPS 2025.07.22 from conda-forge. A dry run resolved `lammps 2025.07.22` (an OpenMPI build) in 121 packages, 389 MB:

```
conda install -c conda-forge lammps=2025.07.22
```

The executable is `lmp`. Minimal run:

```
lmp -in lj.in -var seed 12345 -log lammps_log.txt
```

`-var seed 12345` defines `${seed}` inside the script. `-log` sets the log file name; `-log none` writes no log. Set `OMP_NUM_THREADS` to choose threads per MPI task.

Security: a LAMMPS input script can run shell commands through the `shell` command, which passes anything it does not know to the operating system. Run only input files you trust. Run unknown scripts in a container with no network.

## Run the tested example

This recipe builds LAMMPS in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 2.3 s.

1. Download [lammps-recipe.tar.gz](https://biosimhub.pages.dev/guides/lammps/lammps-recipe.tar.gz) (Dockerfile, example script.in, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf lammps-recipe.tar.gz
   cd lammps
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/lammps:2025.07.22 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/lammps:2025.07.22 lmp -in /work/in/script.in -var seed 12345 \
    -log lammps_log.txt > out/lammps_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `final.data` | 109.8 KB |
| `lammps_log.txt` | 4.4 KB |
| `lammps_stdout.txt` | 4.1 KB |
| `traj.lammpstrj` | 125.9 KB |

<details><summary>First lines of <code>final.data</code></summary>

```
LAMMPS data file via write_data, version 22 Jul 2025, timestep = 2000, units = lj

864 atoms
1 atom types

0 10.077577148295044 xlo xhi
0 10.077577148295044 ylo yhi
0 10.077577148295044 zlo zhi

Masses

1 1
```

</details>

<details><summary>First lines of <code>lammps_log.txt</code></summary>

```
LAMMPS (22 Jul 2025 - Update 6)
  using 2 OpenMP thread(s) per MPI task
# Lennard-Jones fluid, NVE, 864 atoms
units lj
atom_style atomic
lattice fcc 0.8442
Lattice spacing in x,y,z = 1.6795962 1.6795962 1.6795962
region box block 0 6 0 6 0 6
create_box 1 box
Created orthogonal box = (0 0 0) to (10.077577 10.077577 10.077577)
  1 by 1 by 1 MPI processor grid
create_atoms 1 box
```

</details>

<details><summary>First lines of <code>lammps_stdout.txt</code></summary>

```
LAMMPS (22 Jul 2025 - Update 6)
  using 2 OpenMP thread(s) per MPI task
Lattice spacing in x,y,z = 1.6795962 1.6795962 1.6795962
Created orthogonal box = (0 0 0) to (10.077577 10.077577 10.077577)
  1 by 1 by 1 MPI processor grid
Created 864 atoms
  using lattice units in orthogonal box = (0 0 0) to (10.077577 10.077577 10.077577)
  create_atoms CPU = 0.000 seconds
Generated 0 of 0 mixed pair_coeff terms from geometric mixing rule
Neighbor list info ...
  update: every = 1 steps, delay = 0 steps, check = yes
  max neighbors/atom: 2000, page size: 100000
```

</details>

<details><summary>First lines of <code>traj.lammpstrj</code></summary>

```
ITEM: TIMESTEP
0
ITEM: NUMBER OF ATOMS
864
ITEM: BOX BOUNDS pp pp pp
0.0000000000000000e+00 1.0077577148295044e+01
0.0000000000000000e+00 1.0077577148295044e+01
0.0000000000000000e+00 1.0077577148295044e+01
ITEM: ATOMS id type x y z
1 1 0 0 0
2 1 0.839798 0.839798 0
3 1 0.839798 0 0.839798
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `seed` | Seed (available to the script as ${seed}) | 12345 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is `lj.in`: 864 atoms (6 x 6 x 6 fcc cells), rho* = 0.8442, a 10.0776 sigma box, velocities drawn at T* = 1.44 with seed 12345, NVE for 2000 steps.

- `lammps_log.txt` (4490 bytes) holds the echoed script and thermo rows every 100 steps.
- The first row reads T* 1.44, pair energy -6.7734, total energy -4.6159, pressure -5.02. The last (step 2000) reads T* 0.681, pair energy -5.6416, total energy -4.6207, pressure 0.92.
- Temperature fell to about half of 1.44 because the lattice melts and kinetic energy moves into potential energy. Total energy changed by 0.005 in 2000 steps, so NVE conserved it.
- The timing block shows 0.52 s for 2000 steps, 3870 steps/s, and 214 neighbour-list builds.
- `traj.lammpstrj` (128947 bytes) has five frames, one every 500 steps, as `id type x y z`.
- `final.data` (112447 bytes) is a restartable data file at timestep 2000: 864 atoms, one atom type.
- `lammps_stdout.txt` repeats the screen output.

## Your own runs

Define a helper that mounts `in/script.in`-style inputs as the recipe does:

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out "$@"; }
```

1. Another seed: `dr biosimhub/lammps:2025.07.22 lmp -in /work/in/script.in -var seed 999 -log l.txt`. The final temperature became 0.694 against 0.681, total energy -4.6227. Seeds change the starting velocities, so single runs differ by about 0.01 in T*.
2. A thermostat: replace `fix 1 all nve` with `fix 1 all nvt temp 0.7 0.7 0.5`. The final temperature was 0.699 and total energy moved to -4.625, with -4.811 at step 500, because a thermostat does not conserve it. The last number, 0.5, is the damping time. The docs suggest about 100 timesteps, which is 100 x 0.005 = 0.5.
3. A denser solid: change `lattice fcc 0.8442` to `lattice fcc 1.2`. The box shrank to 8.963 sigma, pair energy went from -7.609 to -6.553, and pressure rose from 13.65 to 19.01.

## Pitfalls

- Reduced units carry no physical scale. Map T* and rho* to argon (or anything else) with your own epsilon and sigma.
- `${seed}` in the script needs `-var seed N` on the command line. The recipe passes it for you.
- Thermo energies are per atom in lj units. Multiply by 864 for totals.
- A thermostat run shows no conserved total energy. Check energy drift only in NVE runs.
- Output goes to the current directory. Mount a writable folder or the files vanish with the container.
- Untrusted scripts can run commands on your machine through `shell`. Read the script first.

## Further reading

- LAMMPS manual, running LAMMPS: https://docs.lammps.org/Run_basics.html
- Command-line options (`-var`, `-log`): https://docs.lammps.org/Run_options.html
- Units (lj): https://docs.lammps.org/units.html
- fix nvt: https://docs.lammps.org/fix_nh.html
- The `shell` command: https://docs.lammps.org/shell.html
- Install with conda: https://docs.lammps.org/Install_conda.html
- Source: https://github.com/lammps/lammps
- Thompson AP et al. (2022) Comput Phys Commun 271:108171. https://doi.org/10.1016/j.cpc.2021.108171

---

Cite: Thompson AP et al. (2022). LAMMPS - a flexible simulation tool for particle-based materials modeling at the atomic, meso, and continuum scales. Comput Phys Commun 271:108171. doi:10.1016/j.cpc.2021.108171

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/lammps).
