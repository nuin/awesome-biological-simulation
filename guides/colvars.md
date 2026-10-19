# Colvars

> Collective-variable biasing inside LAMMPS; the example runs well-tempered metadynamics on an argon pair distance and writes the free-energy profile.

Licence: LGPL-3.0-or-later · [Source code](https://github.com/Colvars/colvars)

## What it simulates

Colvars is a C++ library that adds collective variables (CVs) and biasing methods to a molecular dynamics engine. A CV is a function of atom positions, such as a distance, an angle, an RMSD or a coordination number. Colvars can restrain a CV, steer it, or flatten its free-energy landscape with adaptive biasing force (ABF), metadynamics, umbrella sampling or replica-exchange variants.

Colvars has no executable of its own. It runs inside LAMMPS, NAMD, GROMACS, VMD and other engines, and the engine hands it positions and takes back forces. The example here uses the Colvars build in LAMMPS 22 Jul 2025 (Colvars version 2025-04-30, patch 1). It runs well-tempered metadynamics on the distance between two argon atoms in a 216-atom Lennard-Jones liquid, and writes the free-energy profile along that distance.

## When to use it

Use Colvars when the process you care about is slow along a coordinate you can write down, and you already run LAMMPS, NAMD or GROMACS.

- Use [LAMMPS](lammps.md) alone for plain MD with no biasing.
- Use [GROMACS](gromacs.md) with PLUMED, or [OpenMM](openmm.md), when your workflow is built around those engines. Colvars and PLUMED cover similar ground.
- Use [WESTPA](westpa.md) when you want unbiased rates for a rare event, not a free-energy profile along a CV.

## Install it yourself

The conda-forge LAMMPS build includes the COLVARS package. `lmp -h` lists COLVARS among the installed packages. The command below resolves for LAMMPS 2025.07.22:

```
micromamba create -n lmp-colvars -c conda-forge lammps=2025.07.22
```

On Linux aarch64 this build needs glibc 2.38 or newer, so the container recipe uses Ubuntu 24.04. A run needs two inputs. The LAMMPS script has a line `fix cv all colvars <config> output cv`, and the Colvars configuration file defines the CVs and the bias. The script must also contain `atom_modify map yes`, otherwise LAMMPS stops with "Fix colvars requires an atom map".

## Run the tested example

This recipe builds Colvars in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 6.8 s.

1. Download [colvars-recipe.tar.gz](https://biosimhub.pages.dev/guides/colvars/colvars-recipe.tar.gz) (Dockerfile, example script.in, config.colvars, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf colvars-recipe.tar.gz
   cd colvars
   sh run.sh
   ```

![Terminal recording of the Colvars example run](https://biosimhub.pages.dev/media/colvars/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/colvars:lammps-2025.07.22 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/colvars:lammps-2025.07.22 lmp -in /work/in/script.in -var cfg /work/in/config.colvars \
    -var seed 12345 -var temp 120 -var steps 200000 \
    -log lammps_log.txt > out/lammps_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cv.colvars.state` | 63.3 KB |
| `cv.colvars.state.old` | 60.5 KB |
| `cv.colvars.traj` | 76.3 KB |
| `cv.pmf` | 1.4 KB |
| `cv.pmf.BAK` | 1.4 KB |
| `final.data` | 29.6 KB |
| `lammps_log.txt` | 26.3 KB |
| `lammps_stdout.txt` | 24.3 KB |

<details><summary>First lines of <code>cv.colvars.state</code></summary>

```
configuration {
  step       204000
  dt 5.000000e+00
  version 2025-04-30
}

colvar {
  name d
  x       11.616476536686
}

metadynamics {
```

</details>

<details><summary>First lines of <code>cv.colvars.state.old</code></summary>

```
configuration {
  step       200000
  dt 5.000000e+00
  version 2025-04-30
}

colvar {
  name d
  x       11.264296182687
}

metadynamics {
```

</details>

<details><summary>First lines of <code>cv.colvars.traj</code></summary>

```
# step         d                      
        4000    1.96973284115545e+01  
        4100    1.21904980037452e+01  
        4200    9.61875784328257e+00  
        4300    7.36846720628380e+00  
        4400    5.52229119059713e+00  
        4500    6.97057021097194e+00  
        4600    9.27847956333843e+00  
        4700    1.10470022831104e+01  
        4800    1.15057288674522e+01  
        4900    1.07171710472598e+01  
        5000    1.04336411993598e+01  
```

</details>

<details><summary>First lines of <code>cv.pmf</code></summary>

```
# 1
#  3.00000000000000e+00  3.00000000000000e-01         30  0

  3.15000000000000e+00   1.30019181774547e+00
  3.45000000000000e+00   3.84446612075105e-01
  3.75000000000000e+00   1.54924868716826e-01
  4.05000000000000e+00   2.01396378033321e-01
  4.35000000000000e+00   2.47833034796623e-01
  4.65000000000000e+00   2.74207790338895e-01
  4.95000000000000e+00   2.57937939527109e-01
  5.25000000000000e+00   2.08569260220967e-01
  5.55000000000000e+00   2.15849693771314e-01
```

</details>

<details><summary>First lines of <code>cv.pmf.BAK</code></summary>

```
# 1
#  3.00000000000000e+00  3.00000000000000e-01         30  0

  3.15000000000000e+00   1.21410241665197e+00
  3.45000000000000e+00   3.04675341597818e-01
  3.75000000000000e+00   1.04977278484098e-01
  4.05000000000000e+00   1.76484512787892e-01
  4.35000000000000e+00   2.18868858598400e-01
  4.65000000000000e+00   2.29892918582565e-01
  4.95000000000000e+00   1.93592317940043e-01
  5.25000000000000e+00   1.43428383563739e-01
  5.55000000000000e+00   1.63671121480108e-01
```

</details>

<details><summary>First lines of <code>final.data</code></summary>

```
LAMMPS data file via write_data, version 22 Jul 2025, timestep = 204000, units = real

216 atoms
1 atom types

0 30.522 xlo xhi
0 30.522 ylo yhi
0 30.522 zlo zhi

Masses

1 39.948
```

</details>

<details><summary>First lines of <code>lammps_log.txt</code></summary>

```
LAMMPS (22 Jul 2025 - Update 6)
  using 2 OpenMP thread(s) per MPI task
# Liquid-like argon (216 LJ atoms, real units) with a well-tempered
# metadynamics bias on the distance between atoms 1 and 2 through Colvars.
# Variables set from the command line: seed, temp, steps; cfg is the Colvars config file.
units real
atom_style atomic
atom_modify map yes
boundary p p p
lattice sc 5.087
Lattice spacing in x,y,z = 5.087 5.087 5.087
region box block 0 6 0 6 0 6
```

</details>

<details><summary>First lines of <code>lammps_stdout.txt</code></summary>

```
LAMMPS (22 Jul 2025 - Update 6)
  using 2 OpenMP thread(s) per MPI task
Lattice spacing in x,y,z = 5.087 5.087 5.087
Created orthogonal box = (0 0 0) to (30.522 30.522 30.522)
  1 by 1 by 1 MPI processor grid
Created 216 atoms
  using lattice units in orthogonal box = (0 0 0) to (30.522 30.522 30.522)
  create_atoms CPU = 0.000 seconds
Generated 0 of 0 mixed pair_coeff terms from geometric mixing rule
Neighbor list info ...
  update: every = 1 steps, delay = 0 steps, check = yes
  max neighbors/atom: 2000, page size: 100000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `temp` | Temperature (K) | 120 | 50 to 300 |
| `steps` | Biased MD steps (5 fs each) | 200000 | 1000 to 400000 |
| `seed` | Seed (available to the script as ${seed}) | 12345 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The script (`argon.in`) builds 216 argon atoms on a simple cubic lattice at 5.087 Angstrom spacing (reduced density 0.3), runs 4000 steps of NVT at 120 K to melt the lattice, then attaches Colvars and runs 200,000 steps of 5 fs (1 ns). The configuration (`metad_distance.colvars`) defines one CV, `d`, the distance between atoms 1 and 2, with walls at 3.2 and 11.5 Angstrom. It adds a well-tempered metadynamics bias with 0.02 kcal/mol hills every 100 steps and a bias temperature of 1200 K.

- `cv.colvars.traj` has 2001 rows, one every 100 steps from step 4000 to 204000, with the value of `d` in Angstrom. The first rows are 19.70, 12.19, 9.62 and 7.37 Angstrom, so the atoms start far apart and diffuse together. Over the run `d` spans 3.16 to 12.50 Angstrom with a mean of 7.74.
- `cv.pmf` is the free-energy profile F(d) in kcal/mol, 30 points from 3.15 to 11.85 Angstrom at 0.3 Angstrom spacing. Its lowest values sit near zero (0.00 at 11.55 Angstrom). F rises to 1.30 kcal/mol at 3.15 Angstrom, which is about 5.5 kT (kT = 0.238 kcal/mol at 120 K). F is 0.15 at 3.75 Angstrom, 0.21 at 6.15 and 0.19 at 9.15. The steep rise at short range is the repulsive core of the Lennard-Jones potential.
- `cv.colvars.state` is the restart file. It holds the accumulated hills, so a later run can continue the bias. `cv.pmf.BAK` and `cv.colvars.state.old` are the previous copies that Colvars keeps.
- `lammps_log.txt`, `lammps_stdout.txt` and `final.data` are the usual LAMMPS log and final configuration. The whole example takes 6.8 s on one machine.

The profile is a free energy along the distance. It includes the 4 pi r squared volume factor, so it is not the pair potential. Expect F to run about 2 kT ln(r) below the pair potential of mean force at large r.

## Your own runs

Each run below changes one value from the example (seed 12345, 120 K, 200,000 biased steps).

- **Another seed.** `seed 7` gave F(3.15) = 1.26 and F(3.75) = 0.04 kcal/mol. The distance spanned 3.08 to 12.63 Angstrom. The short-range wall of the profile is reproducible and the shallow structure near 3.75 Angstrom is not.
- **Warmer.** `temp 150` gave F(3.15) = 1.64, F(3.75) = 0.56 and F(9.15) = 0.27 kcal/mol. The mean distance rose from 7.74 to 8.05 Angstrom.
- **Shorter.** `steps 20000` (100 ps) gave F(3.15) = 0.40 kcal/mol, far below the 1.30 of the longer run, because only 200 trajectory rows and 200 hills had been laid. The run took under 1 s.
- **Longer.** `steps 400000` gave F(3.15) = 1.80 and F(3.75) = 0.53 kcal/mol, with the distance spanning 3.02 to 12.53 Angstrom. The run took 9 s against 4 s for the 200,000-step run.

The 120 K profiles agree that the short-range wall is steep (F(3.15) of 1.26 to 1.80 kcal/mol for the three runs of 200,000 steps or more). They disagree at 3.75 Angstrom, where F ranges from 0.04 to 0.53 kcal/mol, a spread of 2.1 kT. One 1 ns run of one pair does not converge this profile.

## Pitfalls

- **An atom map is required.** Put `atom_modify map yes` before `create_box`.
- **Metadynamics needs a hill width.** Without `hillWidth` or `gaussianSigmas`, Colvars stops with "positive values are required for either hillWidth or gaussianSigmas". `hillWidth` is in units of the CV width.
- **Walls keep the CV in range.** Distances above half the box length (15.2 Angstrom here) are ambiguous under periodic boundaries, so the example caps `d` with an upper wall at 11.5 Angstrom. Between the wall and the 12.0 Angstrom grid edge the profile is not reliable. The last point at 11.85 Angstrom came out at 0.43 kcal/mol against 0.00 at 11.55.
- **Profiles need convergence checks.** Compare profiles from several seeds, or from the first and second half of one run, before trusting a feature smaller than about 0.5 kcal/mol.
- **Units.** The example uses real units (kcal/mol, Angstrom, fs). Colvars config values use the same units as the engine.

## Further reading

- Colvars documentation: https://colvars.github.io/
- LAMMPS fix colvars: https://docs.lammps.org/fix_colvars.html
- Source: https://github.com/Colvars/colvars
- Paper: Fiorin G, Klein ML, Henin J (2013) Using collective variables to drive molecular dynamics simulations. Mol Phys 111:3345-3362. https://doi.org/10.1080/00268976.2013.813594
- Well-tempered metadynamics: Barducci A, Bussi G, Parrinello M (2008) Phys Rev Lett 100:020603. https://doi.org/10.1103/PhysRevLett.100.020603

---

Cite: Fiorin G, Klein ML, Henin J (2013). Using collective variables to drive molecular dynamics simulations. Mol Phys 111:3345-3362. doi:10.1080/00268976.2013.813594

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/colvars).
