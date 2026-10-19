# ESPResSo

> Molecular dynamics of Kremer-Grest bead-spring polymers in a periodic box, with a Langevin thermostat, reporting chain size and temperature.

Licence: GPL-3.0-or-later · [Source code](https://github.com/espressomd/espresso)

## What it simulates

ESPResSo is a molecular dynamics package for coarse-grained soft matter: polymers, colloids, charged systems and lattice-Boltzmann fluids. Particles carry types, and you choose the interactions between types: Lennard-Jones and WCA potentials, bonded springs, angles, electrostatics and more. A Langevin or dissipative-particle-dynamics thermostat holds the temperature. The core is C++ with MPI, and you drive it from Python.

The example runs the Kremer-Grest bead-spring model, a standard polymer in simulation. Each bead repels others through the purely repulsive WCA form of the Lennard-Jones potential (epsilon = 1, sigma = 1). Neighbouring beads in a chain are joined by a FENE spring (k = 30, maximum extension 1.5). A Langevin thermostat at kT = 1 and friction 1 holds the temperature, and the time step is 0.01. All quantities are in reduced units.

## When to use it

Use ESPResSo for generic polymer, colloid, gel or electrolyte models where you want to define the interactions yourself in a short Python script.

- Use [LAMMPS](lammps.md) for the same kind of coarse-grained model, or for all-atom materials, when your workflow uses LAMMPS input scripts.
- Use [GROMACS](gromacs.md) or [OpenMM](openmm.md) for atomistic biomolecules in explicit water with a standard force field.
- This build has no GPU support, no waLBerla (lattice Boltzmann) and no ScaFaCoS. Those need a build with CUDA, waLBerla or ScaFaCoS enabled.

## Install it yourself

The recipe builds the tagged ESPResSo 5.0.1 release from source against conda-forge Python 3.12, Open MPI, Boost 1.86 and FFTW with CMake. The build passes `-DESPRESSO_BUILD_WITH_WALBERLA=OFF`, `-DESPRESSO_BUILD_WITH_SHARED_MEMORY_PARALLELISM=OFF` and `-DESPRESSO_BUILD_TESTS=OFF`, and installs the Python package `espressomd` to `/opt/espresso`. The runtime image is 966 MB. The ESPResSo documentation describes the other routes, including distribution packages and a CUDA build.

## Run the tested example

This recipe builds ESPResSo in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 18 s.

1. Download [espresso-recipe.tar.gz](https://biosimhub.pages.dev/guides/espresso/espresso-recipe.tar.gz) (Dockerfile, run_espresso.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf espresso-recipe.tar.gz
   cd espresso
   sh run.sh
   ```

![Terminal recording of the ESPResSo example run](https://biosimhub.pages.dev/media/espresso/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/espresso:5.0.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/espresso:5.0.1 python /opt/run_espresso.py --chains 20 --length 30 \
    --density 0.3 --temperature 1 --gamma 1 --equil-steps 20000 \
    --steps 100000 --seed 42 > out/espresso_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `espresso_stdout.txt` | 214 B |
| `final.xyz` | 14.9 KB |
| `observables.csv` | 1.7 KB |
| `result.json` | 218 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/espresso/result-dark.png"><img src="https://biosimhub.pages.dev/media/espresso/result.png" alt="Plot of the ESPResSo example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>espresso_stdout.txt</code></summary>

```
done: {"beads": 600, "box_length": 12.5992, "mean_re2": 61.339, "mean_rg2": 9.791, "ratio_re2_rg2": 6.265, "mean_temperature": 0.9889, "bond_length_mean": 0.9709, "espresso_version": "5.0.1", "wall_se
```

</details>

<details><summary>First lines of <code>final.xyz</code></summary>

```
600
Kremer-Grest chains, box 12.5992
C0 11.4335 2.0714 11.2080
C0 11.3422 2.5565 12.0162
C0 10.5907 2.8100 11.5031
C0 10.3608 2.0689 11.0908
C0 10.6548 1.6780 10.1738
C0 10.8724 2.3935 9.6510
C0 10.7367 2.6811 8.7701
C0 9.8860 3.2751 8.7015
C0 9.1019 3.7459 8.3393
C0 8.4287 3.2085 8.8118
```

</details>

<details><summary>First lines of <code>observables.csv</code></summary>

```
step,time,temperature,re2,rg2,potential
2500,245.0,0.9963,57.334,9.1522,20.0261
5000,270.0,0.9759,61.7636,9.8823,20.0807
7500,295.0,1.0339,70.5724,10.0138,20.0672
10000,320.0,0.9786,73.2353,10.4558,20.0507
12500,345.0,1.0069,66.0059,10.1762,20.1022
15000,370.0,0.9923,68.3065,10.6729,20.0964
17500,395.0,0.9477,75.2946,11.339,20.0982
20000,420.0,1.0254,69.474,10.7204,20.1018
22500,445.0,1.0478,60.484,9.9459,20.0717
25000,470.0,0.9535,58.7339,9.8688,20.1218
27500,495.0,0.9551,55.9567,9.7976,20.1655
```

</details>

<details><summary>First lines of <code>result.json</code></summary>

```
{
 "beads": 600,
 "box_length": 12.5992,
 "mean_re2": 61.339,
 "mean_rg2": 9.791,
 "ratio_re2_rg2": 6.265,
 "mean_temperature": 0.9889,
 "bond_length_mean": 0.9709,
 "espresso_version": "5.0.1",
 "wall_seconds": 17.3
}
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--chains` | Number of chains | 20 | 1 to 50 |
| `--length` | Beads per chain | 30 | 2 to 60 |
| `--density` | Bead number density (sigma^-3) | 0.3 | 0.01 to 0.85 |
| `--temperature` | Temperature kT (LJ units) | 1 | 0.1 to 5 |
| `--gamma` | Langevin friction | 1 | 0.1 to 10 |
| `--equil-steps` | Equilibration steps | 20000 | 0 to 50000 |
| `--steps` | Production steps | 100000 | 40 to 200000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_espresso.py` places 20 chains of 30 beads in a cubic box of side 12.60 (bead density 0.3). It removes overlaps with 2000 steepest-descent steps, equilibrates for 20,000 Langevin steps, and then samples 40 times over 100,000 production steps. It writes `observables.csv`, `final.xyz`, `result.json` and `espresso_stdout.txt`.

- `result.json` reports the average over the second half of the samples. The mean-square end-to-end distance is 61.3 and the mean-square radius of gyration is 9.79, so their ratio is 6.27. An ideal random-walk chain gives a ratio of 6, and a swollen chain in good solvent gives slightly more. The mean bond length is 0.971 and the kinetic temperature is 0.989, against the thermostat target of 1.0.
- `observables.csv` has 40 rows with the columns `step`, `time`, `temperature`, `re2`, `rg2` and `potential`. The first row (step 2500) has temperature 0.996 and a mean-square end-to-end distance of 57.3. The value rises to 73.2 by step 10,000 and falls to 56.0 by step 27,500. Average over many samples before reading a number.
- `potential` is the potential energy per bead, near 20. It is dominated by the FENE spring energy, which the FENE formula puts near 18 per bond at the bond length 0.97, so the high value does not mean the system is strained.
- `final.xyz` is the last configuration as 600 beads in XYZ format, with each chain made contiguous across the periodic boundary.

The run took 18.0 s on one CPU. The output repeats exactly for a given seed.

## Your own runs

Each run below changes one value from the example (20 chains of 30 beads, density 0.3, kT = 1, seed 42).

- **Chain length scaling.** 50 chains of 10 beads gave a mean-square end-to-end distance of 16.3. Ten chains of 60 beads gave 140.7. Together with the 61.3 for 30 beads, the exponent in R^2 proportional to N^(2 nu) is nu = 0.60 from 10 to 30 beads and nu = 0.60 from 30 to 60 beads. The Flory value for a good solvent is 0.588 and the ideal-chain value is 0.5.
- **Denser.** `--density 0.6` shrank the end-to-end distance from 61.3 to 46.2 and the ratio to 5.77. Neighbouring chains screen the self-avoidance, so chains move toward ideal behaviour.
- **Hotter.** `--temperature 2.0` gave a kinetic temperature of 1.98 and an end-to-end distance of 63.7. The change is within the seed-to-seed spread below, which is expected for purely repulsive beads.
- **Another seed.** `--seed 7` gave 56.1 and a ratio of 5.99, against 61.3 and 6.27 for seed 42. The 5-unit difference is the noise to expect from 20 chains.
- **Shorter sampling.** 2000 equilibration steps and 10,000 production steps took 2.1 s and gave 50.7, which is 17 % below the longer run. The chains had not yet relaxed.

## Pitfalls

- **Overlaps at the start break bonds.** A first version that placed beads at random stopped with "bond broken between particles 47, 46". The helper rejects any new bead within 0.85 sigma of a placed bead before it relaxes the system.
- **Statistics need many chains.** Twenty chains give an uncertainty near 10 % on the end-to-end distance. Increase `--chains` or the production steps to tighten it.
- **Finite-size effects.** Chains of 60 beads span about 12 in a box of 12.6, so a chain nearly spans the box. Use a larger box for long chains.
- **Reduced units.** Lengths are in sigma and energies in epsilon. Map them to physical units only at the end.
- **Interface changes.** ESPResSo 5.0 changed parts of the Python API from 4.x, so older scripts may need edits.

## Further reading

- ESPResSo documentation: https://espressomd.github.io/doc/
- Source: https://github.com/espressomd/espresso
- Paper: Weik F et al. (2019) ESPResSo 4.0 - an extensible software package for simulating soft matter systems. Eur Phys J Spec Top 227:1789-1816. https://doi.org/10.1140/epjst/e2019-800186-9
- Kremer-Grest model: Kremer K, Grest GS (1990) J Chem Phys 92:5057. https://doi.org/10.1063/1.458541

---

Cite: Weik F, et al. (2019). ESPResSo 4.0 - an extensible software package for simulating soft matter systems. Eur Phys J Spec Top 227:1789-1816. doi:10.1140/epjst/e2019-800186-9

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/espresso).
