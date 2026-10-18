# Tinker

> Molecular mechanics and dynamics in Fortran, with polarizable AMOEBA and HIPPO force fields, for CPUs, under a licence that is free for named academic users.

Licence: LicenseRef-Tinker-26.2 · [Source code](https://github.com/TinkerTools/tinker)

## What it simulates

Tinker is a package for molecular mechanics and molecular dynamics, with extra tools for biopolymers. It is written in Fortran 95, runs on CPUs with OpenMP, and builds on almost any machine that has a Fortran compiler. The README lists many parameter sets: Amber, CHARMM, Allinger MM2 and MM3, OPLS, MMFF94, and the polarizable AMOEBA, AMOEBA+ and HIPPO models, which use atomic multipoles with explicit induced dipoles.

It is a collection of programs, each doing one job on a structure file: `minimize` for energy minimisation, `dynamic` for molecular dynamics, `analyze` for energies, `scan` for potential-surface searches, `bar` for free-energy estimates from simulations, and many more. A job reads a Cartesian coordinate file (`.xyz`) and a keyword file (`.key`) that points to the force-field parameter file. Other features in the README include continuum solvation (GB/SA and generalized Kirkwood), truncated Newton minimisation, free-energy perturbation and distance geometry.

## When to use it

Use Tinker when you need polarizable force fields (AMOEBA, HIPPO) with a full set of analysis tools, or you want to study or modify a force-field implementation in readable Fortran.

Alternatives:

- [OpenMM](openmm.md) runs AMOEBA on GPUs and is scriptable from Python. It has a separate licence.
- [GROMACS](gromacs.md) is fast for fixed-charge force fields and open source.
- [LAMMPS](lammps.md) fits materials and coarse-grained systems.

## Install

This guide has no run recipe, and this site does not run Tinker for visitors. The reason is the licence, which is a signed agreement between a named licensee and the Tinker Core Development Consortium. The 26.2 text (April 2026, `LICENSE.pdf` in the repository) grants a non-commercial licence "for internal academic purposes only" and says:

- Clause 2: "The Licensee may not sublicense the use of the Software, or make it available to third parties, without the prior written consent of at least one TCDC-Member."
- Clause 6: "The Licensee agrees, in perpetuity, not to disclose the Software to any third party and to use it only for the purposes of this Agreement, unless the TCDC gives prior written consent."
- Clause 9: "Commercial use of the Software ... REQUIRES A COMMERCIAL LICENSE", and the commercial uses listed include any service performed for sale.

A public recipe, image or run form hands the software to third parties, which clauses 2 and 6 forbid without consent. Offering it as a service falls under clause 9. The same licence covers Tinker-HP and Tinker-OpenMM.

Official route:

1. Read `LICENSE.pdf` and have your institution complete the licence. The document asks the licensee to sign it and return a research description.
2. Get the source from the repository, https://github.com/TinkerTools/tinker. The latest release is v26.1.2 (January 2026).
3. Build. The README says to copy `make/Makefile` into `source/` and run it. A cmake script and standalone compile scripts are also provided. FFTW libraries must be present, and prebuilt ones for some systems are in `lib/`.
4. The release is not compatible with parameter files from earlier versions. Use the files in `params/` from the same release.

Commercial licences go through Qubit Pharmaceuticals, named in clause 9 of the licence.

## A first run

Adapted from the `tutorial` folder of the repository (`0README`, `argon.run`, `argon.key`, `argon.log`). The argon tutorial minimises a periodic box of 150 argon atoms and then runs 25 picoseconds of dynamics. The key file reads:

```
parameters       ../../params/mm3
lights
randomseed       123456789
a-axis           26.0206
vdw-cutoff       12.0
tau-pressure     1.0e+20
```

and the run script is:

```
cp argon.1st argon.xyz
../bin/minimize argon 1.0
../bin/dynamic argon 5000 5.0 1.0 4 150.87 49.0
```

`minimize` takes a structure name and an RMS gradient limit (1.0). `dynamic` takes the number of steps (5000), the time step in fs (5.0), the interval between saved frames in ps (1.0), the ensemble (4 is constant pressure and temperature), the temperature in K and the pressure in atm. The fixed `randomseed` makes the trajectory repeat, so that you can compare it to the provided `argon.log`.

## Reading the output

- The program prints a log to the screen: `minimize` shows each quasi-Newton iteration with the function value, the RMS gradient and the line-search comment, as in `argon.log`.
- `dynamic` writes a restart file (`.dyn`) and a trajectory archive (`.arc`) with the frames.
- Each tutorial ships its log, and `tutorial/clean.make` removes generated files before you check your build against them.
- `analyze` breaks an energy down by term and reads trajectories.

## Pitfalls

- **Licence scope.** The licence is personal to the licensee and bars sharing the code. Do not copy the source to colleagues. Each needs their own agreement.
- **Version coupling.** Executables and parameter files must come from the same release.
- **FFTW.** The build fails without the FFTW libraries.
- **CPU only.** The GPU path is Tinker-OpenMM or Tinker-HP, both under the same licence.
- **Citation.** The licence asks that published work cite Tinker 8 (the paper above).

## Further reading

- Source and README: https://github.com/TinkerTools/tinker
- Documentation (guides in `doc/`): https://github.com/TinkerTools/tinker/tree/main/doc
- Tinker-HP: https://github.com/TinkerTools/tinker-hp
- Rackers JA et al. (2018). J Chem Theory Comput 14:5273-5289. https://doi.org/10.1021/acs.jctc.8b00529

---

Cite: Rackers JA, Wang Z, Lu C, Laury ML, Lagardere L, Schnieders MJ, Piquemal JP, Ren P, Ponder JW (2018). Tinker 8: Software tools for molecular design. J Chem Theory Comput 14:5273-5289. doi:10.1021/acs.jctc.8b00529

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/tinker).
