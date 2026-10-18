# Tinker-HP

> A massively parallel MPI and GPU molecular dynamics package with polarizable force fields (AMOEBA, AMOEBA+, HIPPO), for large systems on clusters.

Licence: LicenseRef-Tinker-26.2 · [Source code](https://github.com/TinkerTools/tinker-hp)

## What it simulates

Tinker-HP is the high-performance branch of [Tinker](tinker.md). It keeps Tinker's file formats and simplicity, and adds domain decomposition so that polarizable molecular dynamics runs on thousands of cores or on several GPUs. The README describes it as a multi-precision, MPI package for long polarizable simulations and polarizable QM/MM, giving access to systems of up to millions of atoms.

It supports the polarizable AMOEBA, AMOEBA+ and HIPPO force fields and classical ones (Amber, CHARMM, OPLS). Electrostatics use smooth particle mesh Ewald with a distributed 3D FFT (the shipped `2decomp_fft` library). The README's news section lists later additions: PLUMED and Colvars interfaces, the Lambda-ABF method for alchemical free energies, ring-polymer and quantum thermal bath methods for nuclear quantum effects (Quantum-HP), and interfaces to neural network potentials (Deep-HP), including the FeNNix-Bio1 foundation model.

Versions in the repository: 1.3 for CPUs, 1.3 for one or several GPUs, and 1.1v, a CPU version vectorised for AVX-512.

## When to use it

Use Tinker-HP when you need polarizable force fields on a system that is too large or too slow for one node, and you have a cluster or NVIDIA GPUs.

Alternatives:

- [Tinker](tinker.md) runs the same force fields on a CPU node, with more analysis tools.
- [OpenMM](openmm.md) runs AMOEBA on GPUs from Python, under a different licence.
- [GROMACS](gromacs.md) is the usual choice for fixed-charge force fields at scale.

## Install

This guide has no run recipe, and this site does not run Tinker-HP for visitors. There are two reasons.

**Licence.** Tinker-HP is covered by the Tinker licence (version 26.2, `LICENSE.pdf` in the Tinker repository). The README says it is "available free of charge for ALL Academic Institutions, National Laboratories, and supercomputer centers through the global Tinker license", and that companies and other non-academic groups must contact the managing universities. That licence is granted to a named licensee for "internal academic purposes only". Clause 2 bars making the software "available to third parties" without written consent, clause 6 bars disclosing it to any third party in perpetuity, and clause 9 requires a commercial licence for any service performed for sale. A public image or run form would break clauses 2 and 6.

**Hardware.** It is an MPI and GPU code aimed at clusters. The GPU version needs an NVIDIA GPU with compute capability above 5.0, the NVIDIA HPC SDK (the prerequisites page names versions up to 22.7 as the stable ones) and a CUDA-aware MPI. The sandbox on this site has no GPU and one CPU.

Official route:

1. Obtain and accept the Tinker licence (https://dasher.wustl.edu/tinker/downloads/license.pdf, also in the repository as `license-Tinker.pdf`).
2. Clone https://github.com/TinkerTools/tinker-hp. There is also a GPU container from NVIDIA on its NGC catalogue (`hpc:tinkerhp`).
3. For the CPU version, follow the build guide in `v1.3/CPU/source/Build_CPU.md`. It needs the MKL library or FFTW, and an MPI library supporting MPI 3 (non-blocking collectives). The README notes it was tested most with Intel MPI. Generate the `configure` script and build:

```
autoconf ; automake
./configure ; make ; make install
```

Options include `--enable-fft-fftw3`, `--with-fftlib=...`, `--enable-plumed` and `--enable-colvars`. For GPUs, follow `Build_GPU.md`.

The README names no numbered release. The current GitHub version is 1.3.

## A first run

Adapted from `v1.3/CPU/example` in the repository. The DHFR example (`dhfr.run`) is a single command:

```
mpirun -np 8 ../bin/dynamic dhfr2 10 2.0 1.0 2 300.0
```

It runs the `dynamic` program on 8 MPI processes for the structure `dhfr2` with 10 steps, a 2.0 fs time step, 1.0 ps between frames, ensemble 2 (constant temperature, NVT) and 300 K. The key file `dhfr2.key` selects the `amoebabio09` parameters, the `respa` integrator, a 62.23 Angstrom cubic box, a 12 Angstrom van der Waals cutoff, particle mesh Ewald with a 64 x 64 x 64 grid, and a fixed `randomseed 12345`. The repository also has `dhfr.log` for comparison. Only 10 steps are run, which is a functional test, not science.

## Reading the output

- The program prints energies and temperatures to the screen as it runs, in Tinker's style. Compare with `dhfr.log`.
- Restart (`.dyn`) and trajectory (`.arc`) files carry the state and frames, with the same formats as Tinker.
- Tinker's analysis programs read them, so Tinker-HP and Tinker share a toolchain.

## Pitfalls

- **MPI choice.** Performance depends on the MPI library. The authors saw better results with Intel MPI than with Open MPI.
- **GPU toolchain.** Binaries built with compilers newer than HPC SDK 22.7 reported start-up crashes on some machines, per the prerequisites page. Use one of its listed stable setups.
- **Same licence as Tinker.** Share the repository link, not the source.
- **Citations.** The README asks for the Tinker-HP paper, the GPU paper if you use GPUs, and the Tinker 8 paper.

## Further reading

- Source and README: https://github.com/TinkerTools/tinker-hp
- Website: https://tinker-hp.org
- Build guide: https://github.com/TinkerTools/tinker-hp/blob/master/v1.3/CPU/source/Build_CPU.md
- Lagardere L et al. (2018). Chem Sci 9:956-972. https://doi.org/10.1039/C7SC04531J
- Adjoua O et al. (2021). Tinker-HP on GPUs. J Chem Theory Comput 17:2034-2053. https://doi.org/10.1021/acs.jctc.0c01164

---

Cite: Lagardere L, Jolly LH, Lipparini F, et al. (2018). Tinker-HP: a massively parallel molecular dynamics package for multiscale simulations of large complex systems with advanced polarizable force fields. Chem Sci 9:956-972. doi:10.1039/C7SC04531J

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/tinker-hp).
