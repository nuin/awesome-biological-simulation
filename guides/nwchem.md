# NWChem

> Computational chemistry package for quantum chemistry, QM/MM and molecular dynamics, driven by an NWChem input deck.

Licence: ECL-2.0 · [Source code](https://github.com/nwchemgit/nwchem)

## What it simulates

NWChem is a computational chemistry package. It solves the electronic structure of molecules with Hartree-Fock (SCF), density functional theory and correlated methods, and it also covers QM/MM and molecular dynamics. You describe the job in an input deck: `start`, `title`, a `geometry` block, a `basis` block, and a `task` line that names the method and the operation.

Input is one text deck. Output is a long text file with the energy, orbital information and, for an optimisation, every geometry step. The run also leaves a database (`.db`), orbital vectors (`.movecs`) and scratch files in the working directory.

The key assumption is the Born-Oppenheimer approximation: nuclei sit at fixed points while the electrons are solved quantum mechanically in a finite Gaussian basis. Results depend on the method and basis you choose.

## When to use it

- Geometries, energies and charges of small molecules from first principles.
- Comparing methods and basis sets on the same molecule.

Alternatives: [DFTB+](dftbplus.md) answers the same kind of question much faster with a tight-binding model, at lower accuracy. [GROMACS](gromacs.md), [OpenMM](openmm.md) and [LAMMPS](lammps.md) run classical dynamics of large systems that NWChem would take too long to treat quantum mechanically.

## Install it yourself

NWChem 7.3.1 from conda-forge. A dry run resolved `nwchem 7.3.1` (an MPI build, 229 MB in total):

```
conda install -c conda-forge nwchem=7.3.1
nwchem water.nw
```

The conda activation script sets `NWCHEM_BASIS_LIBRARY` and `NWCHEM_NWPW_LIBRARY`. The recipe's image has no activation step, so it sets them directly.

Security: an NWChem deck can run operating system commands. A deck containing `task shell "echo ran-a-shell-command"` printed `ran-a-shell-command` in the recipe's container. Run only input decks you trust.

## Run the tested example

This recipe builds NWChem in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 2 s.

1. Download [nwchem-recipe.tar.gz](https://biosimhub.pages.dev/guides/nwchem/nwchem-recipe.tar.gz) (Dockerfile, example deck.nw, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf nwchem-recipe.tar.gz
   cd nwchem
   sh run.sh
   ```

![Terminal recording of the NWChem example run](https://biosimhub.pages.dev/media/nwchem/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/nwchem:7.3.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/nwchem:7.3.1 nwchem /work/in/deck.nw > out/nwchem_output.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `nwchem_output.txt` | 75.1 KB |
| `water.b` | 240 B |
| `water.b^-1` | 240 B |
| `water.c` | 96 B |
| `water.cfock` | 427 B |
| `water.db` | 831.2 KB |
| `water.drv.hess` | 96 B |
| `water.movecs` | 913 B |
| `water.p` | 96 B |
| `water.zmat` | 48 B |

<details><summary>First lines of <code>nwchem_output.txt</code></summary>

```
 argument  1 = /work/in/deck.nw
                                         
                                         


             Northwest Computational Chemistry Package (NWChem) 7.3.0
             --------------------------------------------------------


                    Environmental Molecular Sciences Laboratory
                       Pacific Northwest National Laboratory
                                Richland, WA 99352
```

</details>


## Reading the output

The example deck: water at the starting geometry O (0, 0, 0.117), H (0, +-0.757, -0.469) angstroms, the `sto-3g` basis for every atom, and `task scf optimize`, which means a Hartree-Fock (SCF) geometry optimisation.

`nwchem_output.txt` is 76870 bytes. In it:

- The optimisation table (lines starting with `@`) has four rows, steps 0 to 3. Energy goes from -74.96294665 to -74.96590119 hartree. Gmax, the largest gradient component, falls from 0.03812 to 0.00002. The log then prints `Optimization converged`.
- The final geometry has O-H 0.98943 A and H-O-H 100.03 degrees. The symmetry group is C2v.
- The Mulliken table gives oxygen 8.33 electrons and each hydrogen 0.83.
- The job took 0.4 s of CPU time.

The other files:

- `water.db` (851197 bytes) is the run database, named after `start water`. The `restart` directive reuses it.
- `water.movecs` (913 bytes) holds the molecular orbital vectors.
- `water.b`, `water.b^-1`, `water.c`, `water.p`, `water.cfock`, `water.zmat` and `water.drv.hess` are optimiser and Fock scratch files, 48 to 427 bytes.

The package banner in the output reads `NWChem 7.3.0`, although the conda package is 7.3.1.

## Your own runs

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out "$@"; }
dr biosimhub/nwchem:7.3.1 nwchem /work/in/deck.nw > out/nwchem_output.txt
```

1. A bigger basis: change `sto-3g` to `6-31g*`. It converged in four steps (0 to 3) to -76.01074651 hartree, with O-H 0.94732 A and H-O-H 105.50 degrees. The wall time was 0.6 s.
2. B3LYP: use the `6-31g*` basis, add a `dft` block with `xc b3lyp`, and set `task dft optimize`. It converged in four steps to -76.40895454 hartree, with O-H 0.96874 A and 103.65 degrees (0.7 s).
The angle moved from 100.03 to 105.50 degrees between STO-3G and 6-31G* at the same SCF level, so the basis set changes the answer by more than 5 degrees here. Energies from different methods are not comparable.

## Pitfalls

- The recipe runs NWChem as one process (`nproc = 1`).
- The recipe's image sets `NWCHEM_BASIS_LIBRARY` by hand because it has no conda activation. In your own environment, activate it so the variable points at the basis library.
- `start water` names every output file, and `restart water` reuses that job's data. Use a fresh folder per job to keep outputs apart.
- Energies are in hartree. Geometry coordinates are in angstroms because the deck says `units angstrom`.
- Decks can run shell commands with `task shell`. Never run a deck from an unknown source.
- Check for `Optimization converged` in the output before you trust a geometry.

## Further reading

- NWChem sample inputs: https://nwchemgit.github.io/Sample.html
- Top-level directives: https://nwchemgit.github.io/Top-level.html
- Basis sets: https://nwchemgit.github.io/Basis.html
- Source: https://github.com/nwchemgit/nwchem
- Apra E et al. (2020) J Chem Phys 152:184102. https://doi.org/10.1063/5.0004997

---

Cite: Apra E et al. (2020). NWChem: Past, present, and future. J Chem Phys 152:184102. doi:10.1063/5.0004997

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/nwchem).
