# GROMACS

> Classical molecular dynamics of proteins, lipids and nucleic acids; upload a prepared run input (.tpr) and mdrun simulates it.

Licence: LGPL-2.1-or-later · [Source code](https://github.com/gromacs/gromacs)

## What it simulates

GROMACS runs classical molecular dynamics of proteins, lipids, nucleic acids and solvent. It integrates Newton's equations on a force field with bonded terms, Lennard-Jones and Coulomb interactions. Long-range electrostatics use particle-mesh Ewald (PME).

The input to `gmx mdrun` is a single binary run input file, `.tpr`. `gmx grompp` builds it from three text inputs: an `.mdp` file with the settings, a coordinate file (`.gro`) and a topology (`.top`). Output is a log (`md.log`), an energy file (`md.edr`), a compressed trajectory (`md.xtc`), a full-precision trajectory (`md.trr`) and a checkpoint (`md.cpt`).

The key assumption is a fixed-charge, pairwise force field. Bonds do not break, and protonation states are set in the topology.

## When to use it

- Solvated proteins, membranes and nucleic acids, with the AMBER, CHARMM, OPLS or GROMOS force fields.
- Free-energy and long-timescale work on CPU or GPU, where speed matters.

Alternatives on biosimhub: [OpenMM](openmm.md) takes a PDB and a Python script, so it suits a quick solvated run without writing `.mdp` and `.top` files. [LAMMPS](lammps.md) fits non-biomolecular systems and custom potentials.

The biosimhub example runs a prebuilt `.tpr`. Build one on your own machine with `gmx grompp`.

## Install it yourself

GROMACS 2026.3 from conda-forge. A dry run resolved `gromacs 2026.3 nompi_h2d14928_100`:

```
conda install -c conda-forge gromacs=2026.3
```

The program is `gmx`. A minimal workflow from coordinates and a topology:

```
gmx grompp -f md.mdp -c conf.gro -p topol.top -o md.tpr
gmx mdrun -deffnm md
```

`-deffnm md` names every output `md.*`. `-nsteps N` overrides the step count stored in the `.tpr`. The recipe also passes `-ntmpi 1 -ntomp 2 -nb cpu -pin off -noconfout`. In the GROMACS docs, `-ntmpi` sets thread-MPI ranks, `-ntomp` sets OpenMP threads per rank, `-nb cpu` runs short-range non-bonded work on the CPU, and `-pin off` stops mdrun from binding threads to cores. In the example run, `-noconfout` left out the final `confout.gro`.

## Run the tested example

This recipe builds GROMACS in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 2.4 s.

1. Download [gromacs-recipe.tar.gz](https://biosimhub.pages.dev/guides/gromacs/gromacs-recipe.tar.gz) (Dockerfile, example tpr.tpr, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf gromacs-recipe.tar.gz
   cd gromacs
   sh run.sh
   ```

![Terminal recording of the GROMACS example run](https://biosimhub.pages.dev/media/gromacs/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/gromacs:2026.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/gromacs:2026.3 gmx mdrun -s /work/in/tpr.tpr -deffnm md -nsteps 5000 \
    -ntmpi 1 -ntomp 2 -nb cpu -pin off -noconfout > out/mdrun_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `md.edr` | 10.3 KB |
| `md.log` | 27.4 KB |
| `md.xtc` | 57.7 KB |
| `mdrun_stdout.txt` | 0 B |

<details><summary>First lines of <code>md.log</code></summary>

```
                :-) GROMACS - gmx mdrun, 2026.3-conda_forge (-:

Copyright 1991-2026 The GROMACS Authors.
GROMACS is free software; you can redistribute it and/or modify it
under the terms of the GNU Lesser General Public License
as published by the Free Software Foundation; either version 2.1
of the License, or (at your option) any later version.

                         Current GROMACS contributors:
       Mark Abraham           Andrey Alekseenko           Brian Andrews       
        Paul Bauer              Cathrine Bergh              Hugh Bird         
      Eliane Briand               Ania Brown                Yiqi Chen         
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-nsteps` | MD steps (overrides the run input) | 5000 | 1 to 5000000 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example `water.tpr` holds 1530 atoms: 510 water molecules (`SOL`, OPLS atom types) in a 2.5 nm cubic box. `gmx dump -s water.tpr` shows leap-frog `md`, dt 0.002 ps, 5000 steps, PME, 0.9 nm cutoffs, a V-rescale thermostat at 300 K (tau-t 0.1 ps), and no pressure coupling. So 5000 steps is 10 ps.

- `md.log` (28078 bytes) prints an energy block every 500 steps (`nstlog`).
- `md.edr` (10512 bytes) holds energies every 100 steps. `gmx energy -f md.edr` reads it.
- `md.xtc` (59084 bytes) holds 11 frames, one every 500 steps.
- `mdrun_stdout.txt` is empty (0 bytes). mdrun writes its progress to stderr, and the log has the content.

`gmx energy` on this run reports:

- Step 0: potential energy +4571 kJ/mol, temperature 1374 K, pressure 1.1e5 bar. The starting structure is not relaxed.
- 2 ps: -20856 kJ/mol and 322.5 K. 10 ps: -20868 kJ/mol and 299.6 K.
- The whole-run average temperature is 338 K, which includes the hot start. Average only after equilibration.

## Your own runs

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out "$@"; }
```

1. A longer run: `dr biosimhub/gromacs:2026.3 gmx mdrun -s /work/in/tpr.tpr -deffnm md -nsteps 25000 -ntmpi 1 -ntomp 2 -nb cpu -pin off -noconfout`. That is 50 ps. `gmx energy -b 10` (skip the first 10 ps) gave potential energy -20993.2 kJ/mol (error estimate 25, RMSD 136.8) and temperature 299.72 K. `md.xtc` grew to 272980 bytes and `md.edr` to 48912.
2. Your own tiny system. `gmx solvate -cs spc216.gro -box 2.5 2.5 2.5 -p topol.top -o box.gro` gave 510 water molecules, 1530 atoms. The topology used `oplsaa.ff/forcefield.itp` and `oplsaa.ff/tip3p.itp`. Steepest-descent minimisation (`integrator = steep`, `emtol = 1000`) converged in 7 steps. A 5000-step MD with `gen-vel = yes`, `gen-temp = 300`, `gen-seed = 7` and `constraints = h-bonds` averaged 301.5 K over the last 5 ps (error estimate 2.4 K). Minimising first removes the 1374 K start of the example.
3. Run the resulting `md.tpr` with the commands above, or upload it to the biosimhub page.

## Pitfalls

- Averages that include equilibration are wrong. The example's 338 K average sits 38 K above its 300 K target. Use `gmx energy -b <ps>`.
- `-nsteps` only changes the length. Time step, thermostat and cutoffs live in the `.tpr`, so change them in the `.mdp` and run `grompp` again.
- Minimise before MD. An unrelaxed box starts at +4571 kJ/mol and 1374 K.
- With `-noconfout` there is no final structure file. Use `md.cpt` to continue, or drop the flag.
- On a shared machine `-pin off` and a fixed `-ntmpi`/`-ntomp` stop mdrun from grabbing cores that belong to other jobs.

## Further reading

- mdrun performance options: https://manual.gromacs.org/current/user-guide/mdrun-performance.html
- `gmx mdrun`: https://manual.gromacs.org/current/onlinehelp/gmx-mdrun.html
- mdp options: https://manual.gromacs.org/current/user-guide/mdp-options.html
- Install guide: https://manual.gromacs.org/current/install-guide/index.html
- Source: https://github.com/gromacs/gromacs
- Van Der Spoel D et al. (2005) J Comput Chem 26:1701-1718. https://doi.org/10.1002/jcc.20291

---

Cite: Van Der Spoel D et al. (2005). GROMACS: fast, flexible, and free. J Comput Chem 26:1701-1718. doi:10.1002/jcc.20291

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/gromacs).
