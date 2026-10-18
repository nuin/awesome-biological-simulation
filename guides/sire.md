# Sire

> Python and C++ molecular simulation toolkit; the recipe minimises a small water box and runs short OpenMM dynamics through Sire.

Licence: GPL-3.0-only · [Source code](https://github.com/OpenBioSim/sire)

## What it simulates

Sire is a Python and C++ library for molecular modelling. It loads molecular systems from many file formats, lets you search and edit them, evaluates energies, and runs minimisation and molecular dynamics through OpenMM. It also holds the machinery for alchemical free energy calculations and Monte Carlo moves. Sire is a key component of BioSimSpace, which uses it to convert between GROMACS, NAMD, Amber and other programs.

The 2024 paper describes it as an interoperability engine: one script can load a structure, run SMARTS searches with RDKit, run GPU dynamics with OpenMM and show the trajectory in a notebook viewer. The documentation lists tutorial parts on indexing, properties, measurement, energies and movement, dynamics, free energy perturbation, perturbation set-up and QM/MM-style embedding.

Input is a topology and coordinate file set. Sire reads Amber (`.prm7`/`.rst7`, `.top`/`.crd`), GROMACS (`.top`/`.gro`), PDB and other formats. Output is whatever you save: coordinates, trajectories and energy tables.

## When to use it

Use Sire to script a simulation workflow in Python: load, select atoms, minimise, run dynamics, analyse the trajectory and the energies in one place. Use it to prepare or convert inputs for other engines, and for free energy work with its perturbation tools.

- [OpenMM](openmm.md) is the engine Sire calls for dynamics. Use it directly when you do not need Sire's search and editing tools.
- [GROMACS](gromacs.md) and [LAMMPS](lammps.md) are standalone engines with large user bases and their own input languages.
- [OpenMD](openmd.md) is another molecular dynamics code, for rigid-body and interface systems.

## Install

Sire is distributed as a conda package on the `openbiosim` channel. The install page recommends a fresh environment with Python below 3.13 (3.10, 3.11 and 3.12 are packaged):

```
conda create -n openbiosim "python<3.13"
conda install -n openbiosim -c conda-forge -c openbiosim sire
```

The channel lists 2026.2.0 as the current release, with 2026.3.0.dev as the development build. Pin a version with `sire==2026.2.0`. The channel listing shows `linux-64`, `osx-64`, `osx-arm64` and `win-64` builds for it, with no Linux ARM build. An older `michellab` channel release (2023.2.0) has `linux-aarch64`. The project also runs a free JupyterHub at https://try.openbiosim.org with 2 GB of memory and one core, meant for learning only.

## A first run

Adapted from the tutorial page "Molecular Dynamics and Minimisation" (https://sire.openbiosim.org/tutorial/part05/05_dynamics.html). The tutorial loads a molecule, minimises it and runs dynamics:

```python
import sire as sr
mols = sr.load(sr.expand(sr.tutorial_url, "ala.top", "ala.crd"))
mols = mols.minimisation().run().commit()
d = mols.dynamics()
d.run("10ps", "0.5ps")
mols = d.commit()
mols.trajectory().energy().pretty_plot()
```

`sr.tutorial_url` points to files on the project web server, so this needs network access. The tutorial's own printed values are an energy of 29.3786 kcal/mol for the first molecule before minimisation and 17.7799 kcal/mol after. For the whole system it prints -5855.24 kcal/mol before and -7971.79 kcal/mol after. It shows `Dynamics(completed=10 ps, ...)` as the result of a run. These numbers come from the tutorial and depend on the test system.

The container recipe below does the same steps on a self-contained 64-molecule SPC/E water box, with no download. The box and the helper script were written for this recipe. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds Sire in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 37.4 s. Sire has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [sire-recipe.tar.gz](https://biosimhub.pages.dev/guides/sire/sire-recipe.tar.gz) (Dockerfile, run_sire.py, example topology.top, coordinates.gro, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf sire-recipe.tar.gz
   cd sire
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/sire:2026.2.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/sire:2026.2.0 python /opt/run_sire.py /work/in/topology.top /work/in/coordinates.gro \
    --time-ps 2 --temperature 300 --timestep-fs 1 \
    --cutoff-nm 0.6 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `energies.csv` | 1.2 KB |
| `final.gro87` | 16.4 KB |
| `minimised.gro87` | 16.4 KB |
| `run_log.txt` | 946 B |

<details><summary>First lines of <code>energies.csv</code></summary>

```
time,lambda,kinetic,potential
0.10000000000000007,0.0,417.2279805432432,-369.9431390052504
0.20000000000000015,0.0,384.27625135623424,-395.2780938680556
0.3000000000000002,0.0,405.01924997784835,-451.50463758004275
0.4000000000000003,0.0,375.58887537589027,-458.4630007232902
0.5000000000000003,0.0,332.43668022607824,-450.9737927077136
0.6000000000000004,0.0,314.91940381008044,-461.6561045713542
0.7000000000000006,0.0,301.88432972798273,-488.1039417887335
0.8000000000000006,0.0,315.7500090346802,-519.316242284594
0.9000000000000008,0.0,295.43585076591665,-518.1160164907265
1.0000000000000007,0.0,259.19808624848156,-519.9829114890274
1.0999999999999897,0.0,292.27394287017086,-573.9393708408458
```

</details>

<details><summary>First lines of <code>final.gro87</code></summary>

```
64 SPC/E waters, flexible 
  192
    1SOL     OW    1   1.147433   0.108047   0.900245 -0.0476870 -0.2483255 -0.3539231
    1SOL    HW1    2   1.242201   0.101028   0.924077 -0.8710031  0.0914419 -2.0306414
    1SOL    HW2    3   1.111784   0.200937   0.922075 -0.3698134  0.3532046  0.5283625
    2SOL     OW    4   0.080671   0.084905   0.646754 -0.1962238  0.0323331 -0.4981705
    2SOL    HW1    5   0.160486   0.039442   0.608551 -0.4648064  1.1120328 -1.2026345
    2SOL    HW2    6   0.009834   0.093135   0.578815  0.5814783 -1.0078778 -0.0725154
    3SOL     OW    7   0.458207   0.138941   0.644083  0.0989981 -0.4539624 -0.6696676
    3SOL    HW1    8   0.502973   0.118064   0.739828  2.7094977  0.0035138  2.2006768
    3SOL    HW2    9   0.390944   0.065645   0.622109 -1.1703551 -1.2959774 -0.2035886
    4SOL     OW   10   1.145703   1.197942   1.193046  0.4282157 -0.2689990 -0.0294961
```

</details>

<details><summary>First lines of <code>minimised.gro87</code></summary>

```
64 SPC/E waters, flexible 
  192
    1SOL     OW    1   0.154999   0.151225   0.155000  0.0000000  0.0000000  0.0000000
    1SOL    HW1    2   0.231615   0.214887   0.155000  0.0000000  0.0000000  0.0000000
    1SOL    HW2    3   0.078384   0.214888   0.155000  0.0000000  0.0000000  0.0000000
    2SOL     OW    4   0.154999   0.151225   0.465000  0.0000000  0.0000000  0.0000000
    2SOL    HW1    5   0.231615   0.214887   0.465000  0.0000000  0.0000000  0.0000000
    2SOL    HW2    6   0.078384   0.214888   0.465000  0.0000000  0.0000000  0.0000000
    3SOL     OW    7   0.154999   0.151225   0.775000  0.0000000  0.0000000  0.0000000
    3SOL    HW1    8   0.231615   0.214887   0.775000  0.0000000  0.0000000  0.0000000
    3SOL    HW2    9   0.078384   0.214888   0.775000  0.0000000  0.0000000  0.0000000
    4SOL     OW   10   0.154999   0.151225   1.085000  0.0000000  0.0000000  0.0000000
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```

WARNINGS encountered when parsing the topology:
There is not enough data for the atomtype data ''. Skipping this line.

** Warnings for molecule type GroMolType( name() = 'SOL', nExcludedAtoms() = 2 ) **

Expecting only one line that provides the name and number of excluded atoms for this moleculetype. Instead, the number of lines is 2 : [
SOL 2

]
Cannot extract atom information from the line '' as it should contain at least six words (pieces of information)
Cannot extract bond information from the line '' as it should contain at least two words (pieces of information)
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--time-ps` | Dynamics length (ps) | 2 | 0.1 to 50 |
| `--temperature` | Temperature (K) | 300 | 100 to 500 |
| `--timestep-fs` | Time step (fs) | 1 | 0.5 to 2 |
| `--cutoff-nm` | Non-bonded cutoff (nm) | 0.6 | 0.3 to 1.2 |
| `--seed` | Seed for starting velocities | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `d.run(...)` returns a summary line with the simulated time, the energy and the speed in ns per day. The tutorial notes that the speed depends on the hardware and whether a GPU is used.
- `mols.energy()` returns the total potential energy with units. Compare before and after minimisation: the value must fall.
- `mols.trajectory()` holds the saved frames. `.energy()` on it gives per-frame energies and `pretty_plot()` draws them.
- `d.energy_trajectory()` holds the energy terms recorded during dynamics, as a table.

A healthy short run keeps total energy steady apart from thermal noise, and the temperature near the value you set.

## Pitfalls

- **Pin the version.** The channel keeps only a small number of releases, so an unpinned install changes over time.
- **Platform support differs.** There is no Linux ARM build of the current release on the `openbiosim` channel. An ARM Linux host needs emulation or the older `michellab` build.
- **The tutorial needs the network.** `sr.tutorial_url` downloads files at run time. Offline use needs local copies.
- **Minimise first.** A hand-built structure with overlaps gives huge forces and a failed dynamics run.
- **Cut-off and box.** The non-bonded cutoff must be less than half the shortest box length.
- **Dynamics runs on OpenMM platforms.** CPU speed is far below GPU speed for large systems.

## Further reading

- Documentation: https://sire.openbiosim.org/
- Installation: https://sire.openbiosim.org/install.html
- Quick start: https://sire.openbiosim.org/quickstart/index.html
- Source: https://github.com/OpenBioSim/sire
- Paper: Woods CJ et al. (2024) Sire: An interoperability engine for prototyping algorithms and exchanging information between molecular simulation programs. J Chem Phys 160(20):202503. https://doi.org/10.1063/5.0200458

---

Cite: Woods CJ, et al. (2024). Sire: An interoperability engine for prototyping algorithms and exchanging information between molecular simulation programs. J Chem Phys 160(20):202503. doi:10.1063/5.0200458

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/sire).
