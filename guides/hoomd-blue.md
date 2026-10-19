# HOOMD-blue

> Molecular dynamics of a Lennard-Jones fluid in reduced units, returning a GSD trajectory, a thermodynamic log and the radial distribution function.

Licence: BSD-3-Clause · [Source code](https://github.com/glotzerlab/hoomd-blue)

## What it simulates

HOOMD-blue is a molecular dynamics engine for particles. It integrates Newton's equations for a set of particles that interact through pair forces, and it also runs hard-particle Monte Carlo. It is built for coarse-grained and soft-matter models: colloids, polymers, liquids and self-assembling shapes. You script it in Python.

The recipe runs the simplest useful case. A fluid of identical Lennard-Jones particles starts on a cubic lattice in a periodic box, is given random velocities at your temperature, and is integrated for a fixed number of steps. All quantities are in reduced units: the particle diameter sigma, the well depth epsilon and the mass are all 1.

The key assumptions are a single particle type, a pair potential shifted to zero at the cutoff, and a constant-volume box. The model is not a specific substance. Reduced results map to argon-like fluids only after you pick a sigma and an epsilon.

## When to use it

- You want to see how density and temperature set the structure of a simple fluid.
- You need a small, scriptable MD example to check a HOOMD installation or to adapt.
- You work on coarse-grained models where particles are beads, not atoms.

For all-atom proteins with a force field, use [OpenMM](openmm.md) or [GROMACS](gromacs.md). For general input-script MD with many potentials, use [LAMMPS](lammps.md). HOOMD-blue fits when you prefer Python scripts and the GPU build matters. This recipe uses the CPU build only.

## Install it yourself

Pinned to 7.2.0 (conda-forge, CPU build; conda-forge publishes it for linux-64, osx and win only, so the recipe runs it as linux/amd64):

```
micromamba create -n hoomd -c conda-forge hoomd=7.2.0
micromamba activate hoomd
python -c "import hoomd; print(hoomd.version.version)"
```

The helper `run_hoomd.py` builds the lattice itself with `hoomd.Snapshot`, so no input file is needed.

## Run the tested example

This recipe builds HOOMD-blue in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 4.9 s. HOOMD-blue has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [hoomd-blue-recipe.tar.gz](https://biosimhub.pages.dev/guides/hoomd-blue/hoomd-blue-recipe.tar.gz) (Dockerfile, run_hoomd.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf hoomd-blue-recipe.tar.gz
   cd hoomd-blue
   sh run.sh
   ```

![Terminal recording of the HOOMD-blue example run](https://biosimhub.pages.dev/media/hoomd-blue/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/hoomd-blue:7.2.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/hoomd-blue:7.2.0 python /opt/run_hoomd.py --n-side 6 --density 0.8 \
    --kt 1.2 --steps 20000 --dt 0.005 --r-cut 2.5 \
    --thermostat bussi --seed 42 > out/hoomd_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `hoomd_log.txt` | 239 B |
| `log.csv` | 6.3 KB |
| `rdf.csv` | 1.6 KB |
| `trajectory.gsd` | 146.6 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/hoomd-blue/result-dark.png"><img src="https://biosimhub.pages.dev/media/hoomd-blue/result.png" alt="Plot of the HOOMD-blue example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>hoomd_log.txt</code></summary>

```
hoomd 7.2.0 cpu, 216 particles, box 6.4633, 20000 steps (5000 equilibration), thermostat bussi
mean potential energy per particle -4.5402
mean kinetic temperature 1.2003 (target 1.2)
mean pressure 2.5307
g(r) first peak 2.545 at r = 1.083
```

</details>

<details><summary>First lines of <code>log.csv</code></summary>

```
step,time,potential_energy_per_particle,kinetic_temperature,pressure
5100,25.5000,-4.542946,1.140145,2.416868
5200,26.0000,-4.487416,1.178208,2.601715
5300,26.5000,-4.503306,1.247431,2.760652
5400,27.0000,-4.651428,1.204118,2.021948
5500,27.5000,-4.408695,1.257271,3.160748
5600,28.0000,-4.598386,1.127149,2.157035
5700,28.5000,-4.424015,1.289076,3.181101
5800,29.0000,-4.555346,1.113177,2.358626
5900,29.5000,-4.552390,1.239498,2.447688
6000,30.0000,-4.432167,1.179751,3.096375
6100,30.5000,-4.630551,1.169929,1.866095
```

</details>

<details><summary>First lines of <code>rdf.csv</code></summary>

```
r,g_r
0.0162,0.00000
0.0485,0.00000
0.0808,0.00000
0.1131,0.00000
0.1454,0.00000
0.1777,0.00000
0.2101,0.00000
0.2424,0.00000
0.2747,0.00000
0.3070,0.00000
0.3393,0.00000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--n-side` | Lattice cells per side (particles = cells cubed) | 6 | 3 to 10 |
| `--density` | Number density (reduced units) | 0.8 | 0.05 to 1.2 |
| `--kt` | Temperature kT (epsilon) | 1.2 | 0.2 to 5 |
| `--steps` | Total MD steps (a quarter is equilibration) | 20000 | 1000 to 200000 |
| `--dt` | Time step (reduced time) | 0.005 | 0.0005 to 0.01 |
| `--r-cut` | Pair cutoff (sigma) | 2.5 | 1.5 to 4 |
| `--thermostat` | Thermostat | bussi | bussi, langevin, nve |
| `--seed` | Seed (0 to 65535) | 42 | 0 to 65535 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper builds a 6 x 6 x 6 lattice (216 particles) at density 0.8 and kT 1.2, then runs 20,000 steps of dt 0.005 with a Bussi thermostat. The first 5,000 steps are equilibration. The run took 4.9 s on one CPU under amd64 emulation.

- `hoomd_log.txt` holds the summary. Box edge 6.4633. Mean potential energy per particle -4.5402. Mean kinetic temperature 1.2003 against a target of 1.2. Mean pressure 2.5307. The first g(r) peak is 2.545 at r = 1.083.
- `log.csv` has 150 rows, one per 100 steps after equilibration, with step, time, potential energy per particle, kinetic temperature and pressure. Pressure ranges from 1.83 to 3.27 across rows, a wide spread around the 2.53 mean in a box this small.
- `rdf.csv` has 100 bins from r = 0.016 to 3.2 (the half box). g(r) is near 0 below r = 0.9 (0.005 at r = 0.889), because particles repel strongly at short range, and peaks near 1.08. At r = 3.2 it is 1.03, near the ideal-gas value of 1.
- `trajectory.gsd` is 150,155 bytes with a frame every 400 steps. Open it with the `gsd` Python module, OVITO or VMD.

The temperature check is the first sanity test. The kinetic temperature 1.2003 sits within 0.3 percent of the 1.2 target. The second test is the structure: a first peak of about 2.5 at about one sigma is what a dense LJ liquid looks like.

## Your own runs

Each run below changes values from the example (seed 42, 216 particles). Each ran in the recipe's image.

- **Dilute gas.** `--density 0.3 --kt 1.5` gave potential energy -1.70 per particle, pressure 0.33 and a first g(r) peak of 1.75 at r = 1.14. Lower density means weaker packing, so the peak drops from 2.5 to 1.75.
- **Cold liquid.** `--kt 0.7 --density 0.85 --n-side 8 --steps 40000` gave 512 particles, potential energy -5.25, pressure 0.85 and a first peak of 3.03 at r = 1.10. A colder liquid has sharper shells.
- **Another seed.** `--seed 43` gave potential energy -4.52, pressure 2.59 and a peak of 2.51. Seeds change velocities, so report averages over several seeds.
- **No thermostat.** `--thermostat nve` gave a mean kinetic temperature of 1.09, below the 1.2 start. Total energy is conserved and nothing holds the temperature, so it ends at 1.09 and the potential energy at -4.62. Use NVE only after an NVT equilibration.
- **Langevin.** `--thermostat langevin` gave temperature 1.19 and pressure 2.65.

## Pitfalls

- **Pressure needs a writer.** HOOMD computes the virial only on steps where a writer requests it. Reading `thermo.pressure` with no such writer returns `nan`. The helper attaches a table writer on the sampling interval for this reason.
- **The cutoff must fit the box.** The cutoff has to be at most half the box edge. The helper stops with an error otherwise. At density 0.8, the 3-cell lattice gives a box of 3.2 and fails for the default cutoff 2.5, so raise `--n-side`.
- **Seeds are 16-bit.** HOOMD accepts seeds from 0 to 65535.
- **Small boxes are noisy.** 216 particles give pressure samples from 1.83 to 3.27 in one run. Use 512 or more particles and several seeds for quantitative work.
- **No GPU here.** The recipe is the CPU build. The same script uses `hoomd.device.GPU()` on a machine with the GPU build.

## Further reading

- Documentation: https://hoomd-blue.readthedocs.io
- Tutorial: https://hoomd-blue.readthedocs.io/en/latest/tutorial/00-Introduction/00-index.html
- Source: https://github.com/glotzerlab/hoomd-blue
- Paper: Anderson JA, Glaser J, Glotzer SC (2020) HOOMD-blue: A Python package for high-performance molecular dynamics and hard particle Monte Carlo simulations. Comput Mater Sci 173:109363. https://doi.org/10.1016/j.commatsci.2019.109363

---

Cite: Anderson JA, Glaser J, Glotzer SC (2020). HOOMD-blue: A Python package for high-performance molecular dynamics and hard particle Monte Carlo simulations. Comput Mater Sci 173:109363. doi:10.1016/j.commatsci.2019.109363

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/hoomd-blue).
