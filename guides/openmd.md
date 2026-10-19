# OpenMD

> Molecular dynamics of liquids, interfaces, nanoparticles and proteins, including rigid water models and point dipoles.

Licence: BSD-3-Clause · [Source code](https://github.com/OpenMD/OpenMD)

## What it simulates

OpenMD is a classical molecular dynamics engine written in C++. It integrates Newton's equations for atoms and for rigid bodies that also carry orientation. That makes it suited to water models, point dipoles, "sticky" atoms and coarse-grained assemblies, next to ordinary atoms.

Its README lists liquids, proteins, nanoparticles and interfaces as target systems. Zeolites, lipids and transition metals (bulk, flat interfaces and nanoparticles) have been simulated with the force fields shipped with the code.

A simulation is one `.omd` file. It starts with an `<OpenMD>` tag and has two sections: `<MetaData>` (components, ensemble, force field, cutoffs, time step, run length) and a `<Snapshot>` block with initial positions and velocities. Time is in femtoseconds, as in the `dt = 2.0` of the water sample.

## When to use it

Use OpenMD for systems where rigid-body orientation matters: SPC/E and other water models, ions in water, metal nanoparticles, liquid-vapour or solid-liquid interfaces. It ships analysis tools that work on its own trajectory format.

- [LAMMPS](lammps.md) covers a wider range of pair styles and has a larger user base.
- [GROMACS](gromacs.md) is faster for large biomolecular systems in explicit water.
- [OpenMM](openmm.md) runs on GPUs and is scriptable from Python.

OpenMD runs on CPUs. The MPI build runs in parallel. The README does not describe a GPU build.

## Install

OpenMD is built from source with CMake. The current release is v3.1 (tag `v3.1` on GitHub). The project's INSTALL.md lists a C++17 compiler and CMake 3.20 or newer as the required tools. Optional libraries add features: MPI for the parallel binary, Python with NumPy and SciPy for some utilities, qhull for the `LangevinHull` integrator, Open Babel for the `atom2md` setup program, and FFTW for surface undulation spectra.

```
git clone --branch v3.1 https://github.com/OpenMD/OpenMD.git
mkdir build && cd build
cmake ../OpenMD
make -j4
```

The INSTALL.md basic procedure uses a separate build directory and runs `cmake` on the source directory. If you run from the build directory without installing, set two variables first (from QUICK_START.md):

```
export FORCE_PARAM_PATH="$HOME/OpenMD/forceFields"
export PATH="$PATH:$HOME/OpenMD/build/bin"
```

## A first run

Adapted from QUICK_START.md in the repository (https://github.com/OpenMD/OpenMD/blob/v3.1/QUICK_START.md). The `samples` directory holds ready-made systems. Run liquid water with the SPC/E model:

```
cd OpenMD/samples/water/liquid
openmd spce.omd
```

The `spce.omd` sample has 256 SPC/E molecules in a cubic box 19.713 angstrom on a side. Its MetaData sets the `Water` force field, a shifted-force cutoff of 9.0 angstrom, damped electrostatics with `dampingAlpha = 0.18`, `dt = 2.0`, `runTime = 1e5`, `sampleTime = 100` and `statusTime = 10`. The ensemble in the file is NVE. A progress bar shows the time remaining. With an MPI build, the QUICK_START.md command is `mpirun -np 4 openmd_MPI spce.omd`.

The container recipe below runs the same sample with the SPC/E molecule written into the file in place of the `#include`, and `runTime = 2000` (2 ps). The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds OpenMD in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 15.1 s. OpenMD has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [openmd-recipe.tar.gz](https://biosimhub.pages.dev/guides/openmd/openmd-recipe.tar.gz) (Dockerfile, run_openmd.sh, example omd.omd, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf openmd-recipe.tar.gz
   cd openmd
   sh run.sh
   ```

![Terminal recording of the OpenMD example run](https://biosimhub.pages.dev/media/openmd/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/openmd:3.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/openmd:3.1 sh /opt/run_openmd.sh /work/in/omd.omd 2000 100 9 > out/openmd_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `openmd_log.txt` | 3.0 KB |
| `sim.dump` | 1.1 MB |
| `sim.eor` | 55.0 KB |
| `sim.omd` | 54.9 KB |
| `sim.report` | 967 B |
| `sim.stat` | 15.5 KB |

<details><summary>First lines of <code>openmd_log.txt</code></summary>

```
  +--------------------------------------------------------------------------+
  |    ____                    __  ___ ____                                  |
  |   / __ \____  ___  ____   /  |/  // __ \    The Open Molecular Dynamics  |
  |  / / / / __ \/ _ \/ __ \ / /|_/ // / / /    Engine:  openmd.org          |
  | / /_/ / /_/ /  __/ / / // /  / // /_/ /                                  |
  | \____/ /___/\___/_/ /_//_/  /_//_____/      Copyright 2004-2024 by the   |
  |     /_/                                     University of Notre Dame     |
  |                                                                          |
  |  Version: 3.1  Revision: ad34be2   Build date: Sun Oct 18 05:17:15 2026  |
  |                                                                          |
  | All source code is available under a BSD 3-Clause License. If you use    |
  | OpenMD or its source code in your research, please cite the following    |
```

</details>

<details><summary>First lines of <code>sim.dump</code></summary>

```
<OpenMD version=2>
  <MetaData>

molecule{
  name = "SPCE";
  atom[0]{ type = "O_SPCE"; position( 0.0, 0.0, -0.06461 ); }
  atom[1]{ type = "H_SPCE"; position( 0.0, 0.81649, 0.51275 ); }
  atom[2]{ type = "H_SPCE"; position( 0.0, -0.81649, 0.51275 ); }
  rigidBody[0]{ members(0, 1, 2); }
}


```

</details>

<details><summary>First lines of <code>sim.eor</code></summary>

```
<OpenMD version=2>
  <MetaData>

molecule{
  name = "SPCE";
  atom[0]{ type = "O_SPCE"; position( 0.0, 0.0, -0.06461 ); }
  atom[1]{ type = "H_SPCE"; position( 0.0, 0.81649, 0.51275 ); }
  atom[2]{ type = "H_SPCE"; position( 0.0, -0.81649, 0.51275 ); }
  rigidBody[0]{ members(0, 1, 2); }
}


```

</details>

<details><summary>First lines of <code>sim.omd</code></summary>

```
<OpenMD version=1>
  <MetaData>

molecule{
  name = "SPCE";
  atom[0]{ type = "O_SPCE"; position( 0.0, 0.0, -0.06461 ); }
  atom[1]{ type = "H_SPCE"; position( 0.0, 0.81649, 0.51275 ); }
  atom[2]{ type = "H_SPCE"; position( 0.0, -0.81649, 0.51275 ); }
  rigidBody[0]{ members(0, 1, 2); }
}


```

</details>

<details><summary>First lines of <code>sim.report</code></summary>

```
###############################################################################
# Status Report:                                                              #
#              Total Time:        2000 fs                                     #
#       Number of Samples:         201                                        #
#            Total Energy:     -2284.8  ±  0.0170157    kcal/mol              #
#        Potential Energy:    -2741.08  ±  1.69201      kcal/mol              #
#          Kinetic Energy:     456.282  ±  1.68132      kcal/mol              #
#             Temperature:     299.555  ±  1.10381      K                     #
#                Pressure:     374.168  ±  88.2931      atm                   #
#                  Volume:     7660.52  ±  0            A^3                   #
#      Conserved Quantity:     -2284.8  ±  0.0170157    kcal/mol              #
###############################################################################
```

</details>

<details><summary>First lines of <code>sim.stat</code></summary>

```
## Last run using OpenMD version: 3.1, revision: ad34be2c808aae08fbbe007862359cfa2f7afc74
#	Time(fs)	Total Energy(kcal/mol)	Potential Energy(kcal/mol)	Kinetic Energy(kcal/mol)	Temperature(K)	Pressure(atm)	Volume(A^3)	Conserved Quantity(kcal/mol)
	0	-2285.006	-2758.9301	473.92407	311.13697	114.09082	7660.5185	-2285.006
	10	-2284.7198	-2747.3394	462.6196	303.71545	511.72021	7660.5185	-2284.7198
	20	-2284.9201	-2751.969	467.04894	306.62336	410.4693	7660.5185	-2284.9201
	30	-2284.661	-2723.4365	438.7755	288.06151	847.72572	7660.5185	-2284.661
	40	-2284.8389	-2737.9462	453.10728	297.47049	366.52189	7660.5185	-2284.8389
	50	-2284.7789	-2738.5294	453.75055	297.89281	0.77824357	7660.5185	-2284.7789
	60	-2284.7561	-2733.6258	448.86972	294.68848	115.93624	7660.5185	-2284.7561
	70	-2284.7731	-2731.5744	446.80127	293.33052	378.08815	7660.5185	-2284.7731
	80	-2284.6336	-2726.472	441.83835	290.0723	592.74435	7660.5185	-2284.6336
	90	-2284.7771	-2737.2007	452.42358	297.02163	335.12908	7660.5185	-2284.7771
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `run_time` | Run time (fs) | 2000 | 100 to 50000 |
| `sample_time` | Time between trajectory frames (fs) | 100 | 10 to 10000 |
| `cutoff` | Cutoff radius (A) | 9 | 4 to 9.8 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The run writes four files next to the input, as listed in QUICK_START.md:

- `spce.dump`: the trajectory, with many snapshots of positions and velocities.
- `spce.eor`: the end-of-run snapshot. It is a valid starting point for a continuation run.
- `spce.stat`: a tab-separated table of time, energies, temperature, pressure and volume. The first lines name the code version and the quantities and their units.
- `spce.report`: means and confidence intervals for the same quantities.

At the end of the run the terminal prints a summary of the thermodynamic quantities. The guide's own checks are simple. In an NVE run, total energy in `spce.stat` should stay flat apart from small noise. A drift means the time step is too large for the cutoff scheme. Temperature should stay near the target set by the initial velocities.

To view the trajectory, convert it to XYZ and open it in a viewer:

```
Dump2XYZ -i spce.dump -m -b
jmol spce.xyz
```

QUICK_START.md plots `spce.stat` with `xmgrace -nxy spce.stat`. Any tool that reads tab-separated text works.

## Pitfalls

- **Force field files must be found.** An unset `FORCE_PARAM_PATH` is the usual cause of an immediate error when you run from a build directory.
- **MPI is a separate binary.** The serial `openmd` and the parallel `openmd_MPI` are different programs. The parallel one exists only if CMake found MPI.
- **Optional libraries fail quietly.** If qhull, Open Babel or FFTW are missing at configure time, the matching tools or integrators are not built. Check the CMake output.
- **Units are not SI.** Time is in fs and lengths in angstrom. Check the header of the `.stat` file before comparing numbers with other codes.
- **Samples are demonstrations.** Their run lengths are short. For production averages, increase `runTime` and check the confidence intervals in the `.report` file.

## Further reading

- Repository and README: https://github.com/OpenMD/OpenMD
- Quick start: https://github.com/OpenMD/OpenMD/blob/v3.1/QUICK_START.md
- Install notes: https://github.com/OpenMD/OpenMD/blob/v3.1/docs/INSTALL.md
- Project site: https://openmd.org/
- Paper: Drisko M et al. (2024) OpenMD: A parallel molecular dynamics engine for complex systems and interfaces. J Open Source Softw 9(103):7004. https://doi.org/10.21105/joss.07004

---

Cite: Drisko M, et al. (2024). OpenMD: A parallel molecular dynamics engine for complex systems and interfaces. J Open Source Softw 9(103):7004. doi:10.21105/joss.07004

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openmd).
