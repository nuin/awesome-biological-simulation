# DFTB+

> Semiempirical density-functional tight-binding and xTB calculations (energies, geometry optimisation, MD) from an HSD input file.

Licence: LGPL-3.0-or-later · [Source code](https://github.com/dftbplus/dftbplus)

## What it simulates

DFTB+ computes the electronic structure of molecules and solids with density-functional tight-binding (DFTB) and the extended tight-binding (xTB) family. It approximates density functional theory with pre-computed parameters, so a small molecule takes a fraction of a second. The DFTB+ site puts it about two orders of magnitude faster than full DFT.

Input is one text file in HSD format: a geometry, a driver (single point, geometry optimisation, molecular dynamics) and a Hamiltonian. Output is the total energy, atomic charges, orbital energies and the final geometry.

The key assumption is the tight-binding approximation: the Hamiltonian comes from fixed parameter sets. It does not solve the full density functional. The example uses GFN1-xTB, which needs no separate Slater-Koster parameter files.

## When to use it

- Geometries, charges and energies of molecules where full DFT is too slow.
- Pre-optimising structures before a higher-level calculation.
- Quick molecular dynamics on a small system with quantum-derived forces.

Alternatives on biosimhub: [NWChem](nwchem.md) gives ab initio SCF and DFT with Gaussian basis sets, at higher cost. Classical tools ([GROMACS](gromacs.md), [OpenMM](openmm.md), [LAMMPS](lammps.md)) are far faster but cannot describe electrons or bond changes.

## Install it yourself

DFTB+ 25.1 from conda-forge. The dry run resolved `dftbplus 25.1 nompi_h34242df_100` (50 MB in total):

```
conda install -c conda-forge dftbplus=25.1
```

DFTB+ always reads a file called `dftb_in.hsd` in the current directory, so name your input that and run:

```
dftb+
```

The recipe wraps these two steps in a script `run-dftbplus`, which copies the uploaded input to `dftb_in.hsd` and runs `dftb+`.

## Run the tested example

This recipe builds DFTB+ in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.3 s.

1. Download [dftbplus-recipe.tar.gz](https://biosimhub.pages.dev/guides/dftbplus/dftbplus-recipe.tar.gz) (Dockerfile, run.sh, example input.hsd, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf dftbplus-recipe.tar.gz
   cd dftbplus
   sh run.sh
   ```

![Terminal recording of the DFTB+ example run](https://biosimhub.pages.dev/media/dftbplus/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/dftbplus:25.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/dftbplus:25.1 run-dftbplus /work/in/input.hsd > out/dftb_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `band.out` | 298 B |
| `charges.bin` | 328 B |
| `detailed.out` | 2.5 KB |
| `dftb_in.hsd` | 355 B |
| `dftb_pin.hsd` | 2.0 KB |
| `dftb_stdout.txt` | 10.1 KB |
| `geo_end.gen` | 218 B |
| `geo_end.xyz` | 233 B |

<details><summary>First lines of <code>band.out</code></summary>

```
 KPT            1  SPIN            1  KWEIGHT    1.0000000000000000     
     1    -20.6264  2.00000
     2    -16.6673  2.00000
     3    -14.8611  2.00000
     4    -13.6047  2.00000
     5     -4.2569  0.00000
     6     -1.3576  0.00000
     7      9.4888  0.00000
     8     12.4018  0.00000

```

</details>

<details><summary>First lines of <code>detailed.out</code></summary>

```
 Fermi distribution function

Geometry optimization step: 6


********************************************************************************
 iSCC Total electronic   Diff electronic      SCC error    
    4   -0.58064880E+01   -0.10563754E-08    0.39396170E-08
********************************************************************************

 Total charge:    -0.00000000

```

</details>

<details><summary>First lines of <code>dftb_in.hsd</code></summary>

```
# Geometry optimisation of a water molecule with GFN1-xTB (needs no Slater-Koster files)
Geometry = xyzFormat {
3

O  0.000  0.000  0.119
H  0.000  0.757 -0.477
H  0.000 -0.757 -0.477
}
Driver = GeometryOptimisation {
  Optimiser = Rational {}
  MaxSteps = 100
}
```

</details>

<details><summary>First lines of <code>dftb_pin.hsd</code></summary>

```
Geometry = xyzFormat {
3
O  0.000  0.000  0.119
H  0.000  0.757 -0.477
H  0.000 -0.757 -0.477
}
Driver = GeometryOptimisation {
  Optimiser = Rational {
    DiagLimit = 1.0000000000000000E-002
  }
  MaxSteps = 100
  LatticeOpt = No
```

</details>

<details><summary>First lines of <code>dftb_stdout.txt</code></summary>

```
|===============================================================================
|
|  DFTB+ development version (commit: a23bfb2)
|
|  Copyright (C) 2006 - 2025  DFTB+ developers group
|
|===============================================================================
|
|  When publishing results obtained with DFTB+, please cite the following
|  reference:
|
|    Recent Developments in DFTB+, a Software Package for Efficient Atomistic
```

</details>

<details><summary>First lines of <code>geo_end.gen</code></summary>

```
 3  C
 O H
    1  1   -0.7543120124E-16    0.2794466514E-16    0.1009362947E+00
    2  2    0.1146578893E-15    0.7709109860E+00   -0.4679815755E+00
    3  2   -0.3922668805E-16   -0.7709109860E+00   -0.4679815755E+00
```

</details>

<details><summary>First lines of <code>geo_end.xyz</code></summary>

```
    3
Geometry Step: 6
    O     -0.00000000      0.00000000      0.10093629      6.67118102
    H      0.00000000      0.77091099     -0.46798158      0.66440949
    H     -0.00000000     -0.77091099     -0.46798158      0.66440949
```

</details>


## Reading the output

The example input is a water molecule in `xyzFormat` (3 atoms), `Driver = GeometryOptimisation` with the `Rational` optimiser and at most 100 steps, and `Hamiltonian = xTB { Method = "GFN1-xTB" }`.

The run converged after 7 geometry steps (0 to 6) and printed `Geometry converged`.

- Total energy: -5.7685128 H at step 0, -5.7687749 H at step 6. That is -156.9692 eV to -156.9764 eV, a drop of 7.2 meV.
- `geo_end.xyz` (233 bytes) holds the optimised geometry. The oxygen sits at z = 0.10094 and the hydrogens at y = +0.77091 and -0.77091, z = -0.46798 (angstroms). From those the O-H bond is 0.958 A and the H-O-H angle 107.1 degrees. The start was 0.963 A and 103.6 degrees.
- The fourth column of `geo_end.xyz` is the atom population from `detailed.out`: 6.671 on O and 0.664 on each H.
- `detailed.out` (2594 bytes) lists gross charges: O -0.671, each H +0.336. The total charge is 0. Energy terms are: electronic -5.8065 H, repulsive 0.0379 H, total -5.7688 H.
- `band.out` (298 bytes) lists 8 orbital energies with occupations. Four are filled (2.0 electrons), from -20.63 to -13.60 eV. The first empty level is -4.26 eV, so the HOMO-LUMO gap is 9.35 eV.
- `geo_end.gen` is the same geometry in `.gen` format. `dftb_pin.hsd` is the parsed input with every default written out. `charges.bin` is a binary restart file.

## Your own runs

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out "$@"; }
dr biosimhub/dftbplus:25.1 run-dftbplus /work/in/input.hsd > out/dftb_stdout.txt
```

Edit `in/input.hsd` between runs.

1. GFN2-xTB: change `Method` to `"GFN2-xTB"`. The optimisation took 8 steps (0 to 7) and the total energy was -5.0705 H. The geometry shifted to O-H 0.959 A and 107.2 degrees. The O charge became -0.565.
2. Single point: delete the `Driver` block. One step ran and the energy was -5.7685128 H, the same as step 0 of the optimisation. The O charge is -0.667.
3. A cation: add `Charge = 1.0` inside the `xTB` block. The run reported `Total charge: 1.00000000`. It took 9 steps and ended at -5.0156 H. The O-H bond lengthened to 1.006 A and the angle opened to 116.8 degrees. The O charge was -0.094 and each H +0.547.

Total energies from different Hamiltonians or charge states are not comparable. Compare geometries and charges.

## Pitfalls

- The input file name matters for a native run. DFTB+ reads only `dftb_in.hsd`.
- The example's own comment says GFN1-xTB needs no Slater-Koster files. Other Hamiltonians may need parameter files, so read the DFTB+ recipes (linked below) before you change `Hamiltonian`.
- Look for `Geometry converged` in `dftb_stdout.txt`. The example allows `MaxSteps = 100`, and a run that uses all 100 steps has not reached a minimum.
- The example ends with `ParserOptions { ParserVersion = 14 }`. Keep it when you copy the file.
- Energies are in hartree (H) in the logs and eV beside them. The geometry is in angstroms.
- The example is neutral because it sets no charge. Add `Charge` for ions, as in run 3.

## Further reading

- DFTB+ home page: https://dftbplus.org/
- DFTB+ recipes (tutorials): https://dftbplus-recipes.readthedocs.io/en/latest/
- Source: https://github.com/dftbplus/dftbplus
- Hourahine B et al. (2020) J Chem Phys 152:124101. https://doi.org/10.1063/1.5143190

---

Cite: Hourahine B et al. (2020). DFTB+, a software package for efficient approximate density functional theory based atomistic simulations. J Chem Phys 152:124101. doi:10.1063/1.5143190

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/dftbplus).
