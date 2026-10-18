# Cardioid

> Parallel cardiac electrophysiology on a 3D grid of cells, from single-cell models up to whole-heart runs on supercomputers.

Licence: MIT · [Source code](https://github.com/llnl/cardioid)

## What it simulates

Cardioid is a cardiac multiscale simulation suite from Lawrence Livermore National Laboratory (LLNL). The repository holds separate simulators for different jobs:

- **Electrics.** The main simulator. It couples a diffusion step on a 3D grid with a cell model at each grid cell, for example the TT06 model (`BetterTT06` in the code). It writes activation and recovery times and state snapshots.
- **Fibers.** Generates fibre orientations for a heart mesh. It uses MFEM.
- **Mechanics and ECG.** Cardiac mechanics and torso ECG tools, also built on MFEM.

The electrics code divides the domain into subdomains and spreads them over MPI tasks. The README says the code was a finalist for the 2012 Gordon Bell Prize and reached nearly 12 petaflops on the Sequoia supercomputer at over 90 percent parallel efficiency on 1,572,864 cores. Those figures come from the README.

Input is a text file, `object.data`, made of blocks of the form `name CLASS { keyword = value; }`. The root block is `SIMULATE`. It names the anatomy, the domain decomposition, the diffusion method, the reaction (cell) model, the stimuli and the sensors.

## When to use it

Use Cardioid for cell-resolution tissue or whole-ventricle runs where you have a cluster with MPI, and for studies that depend on very fine grids.

- Use [openCARP](opencarp.md) for a cardiac simulator with a single-cell tool (`bench`) that runs without a mesh.
- Use [TorchCor](torchcor.md) when you have a GPU and a finite-element heart mesh.

## Install

There is no recipe for Cardioid on this site. The project targets high-performance computing systems: its README recommends building with Spack, uses a CMake build on the BLT make system with per-machine architecture files in `arch/*.cmake`, and needs MPI, OpenMP, Lapack and Perl. The fibers, mechanics and ECG parts also need MFEM installed by hand. The repository has no tagged releases, and its last commit on `master` is `2f66d9f` from 26 October 2021.

The README's Spack route:

```bash
git clone https://github.com/spack/spack.git
. spack/share/spack/setup-env.sh
mkdir myenv && cd myenv
spack env create -d .
spacktivate .
spack compiler find
spack external find cmake perl
spack external find --not-buildable openmpi mvapich2 mpich spectrum-mpi cuda
spack add cardioid          # or cardioid+cuda
spack develop cardioid@develop
spack concretize -f
spack install
```

The README then says the binary is `.spack-env/view/bin/cardioid`. Spack carries a `cardioid` package (the `package.py` is in the spack-packages repository), but this guide does not state its version.

Without Spack, run CMake with an architecture file. The builds go in `build/<arch>` and the executables are installed in `build/<arch>/bin`. CUDA support is optional and needs NVTX and NVRTC.

## A first run

Adapted from the repository's own test case, `test/tests/Niederer/`, which holds `object.data`, `tt06.fit.data` and a `definition` script.

The test's `definition` runs:

```bash
cardioid object.data tt06.fit.data
```

The `object.data` file builds its own tissue, so it needs no mesh file. Its geometry matches the slab of the Niederer et al. (2011) N-version benchmark: 20 by 7 by 3 mm with a grid spacing of 0.10 mm in every direction, one conductivity block (sigma11 of 0.0001334177 S/mm along the fibre, 0.0000176062 across), the `BetterTT06` cell model, two box stimuli (the first starts at 0 ms, the second at 565 ms, each lasting 2 ms), and an `activationAndRecovery` sensor writing to a file named `arTime`. The `definition` script is tagged `seq`, for sequential. The file sets `maxLoop = 10` steps of `dt = 0.01` ms, so the run is a smoke test that checks the code starts and agrees with saved numbers. A physiological run needs `maxLoop` raised to cover hundreds of milliseconds, and a grid of 420,000 cells is large for one workstation.

## Reading the output

The repository does not describe each output file, so this section names only what the test setup shows.

- `stdOut` is the console log of the run.
- The `arTime` file holds the activation and recovery times that the `activationAndRecovery` sensor records. `printRate` and `evalRate` in the sensor block set how often it writes and evaluates.
- Snapshot files start with `snapshot.0`. The test's `clean` step removes `stdOut`, `data` and `snapshot.0*`.
- The test compares the results to saved values with `numCompare` at a tolerance of 1e-14 for the sequential run.

## Pitfalls

- **Grid size.** At 0.10 mm spacing the benchmark slab has 200 by 70 by 30 cells, which is 420,000. Coarser spacing runs sooner and conducts differently.
- **Units.** The input uses mm, ms and S/mm, and the diffusion scale is in mm^3/mF. A wrong unit changes conduction speed.
- **Keywords are free-form.** The input format accepts any keyword. A misspelled name may be ignored, so check a run against the test's `object.data`.
- **Build effort.** A first build on a new machine usually means writing an architecture file.

## Further reading

- Source and README: https://github.com/llnl/cardioid
- Benchmark: Niederer SA et al. (2011) Verification of cardiac tissue electrophysiology simulators using an N-version benchmark. Philos Trans A 369:4331-4351. https://doi.org/10.1098/rsta.2011.0139
- Paper: Mirin AA et al. (2012) Toward real-time modeling of human heart ventricles at cellular resolution. https://doi.org/10.1109/sc.2012.108
- Companion paper: Richards DF et al. (2013) Towards real-time simulation of cardiac electrophysiology in a human heart at high resolution. https://doi.org/10.1080/10255842.2013.795556

---

Cite: Mirin AA, Richards DF, Glosli JN, et al. (2012). Toward real-time modeling of human heart ventricles at cellular resolution: Simulation of drug-induced arrhythmias. SC12: International Conference for High Performance Computing, Networking, Storage and Analysis, pp 1-11. doi:10.1109/sc.2012.108

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cardioid).
