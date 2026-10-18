# CP2K

> Run a Gaussian and plane waves DFT calculation (single-point energy or geometry optimisation) on a small molecule in a box and report the total energy.

Licence: GPL-2.0-or-later · [Source code](https://github.com/cp2k/cp2k)

## What it simulates

CP2K is a quantum chemistry and solid-state physics package. The recipe uses its Quickstep module: density functional theory (DFT) with Gaussian orbitals for the wave function and plane waves for the electron density (the GPW method), plus GTH pseudopotentials that replace the core electrons.

You give it a molecule as an XYZ file, a box size, an exchange-correlation functional (PBE or BLYP), a basis set and a plane-wave cutoff. It solves the Kohn-Sham equations self-consistently and returns the total energy. With `GEO_OPT` it also moves the atoms downhill until the forces are small.

The helper `run_cp2k.py` writes the CP2K input for a closed-shell molecule of H, C, N, O, F, P, S or Cl, with open boundary conditions inside a cubic box. Energies are in hartree (Ha), and 1 Ha is 27.2114 eV. Energies are valence-only because the pseudopotential removes the core, so only differences between calculations with the same settings mean anything.

## When to use it

Use CP2K for energies, forces and relaxed geometries of molecules and periodic systems when classical force fields are not accurate enough.

- Use [NWChem](nwchem.md) or [DFTB+](dftbplus.md) for other quantum chemistry options (DFTB+ is semi-empirical and much faster).
- Use [DeePMD-kit](deepmd-kit.md) to train a fast potential on CP2K energies and forces.
- Use [OpenMM](openmm.md) for classical molecular dynamics of large systems.

## Install it yourself

The recipe image uses the conda-forge package `cp2k` 2026.2, the MPICH build, which ships `cp2k.psmp` and `cp2k.popt`:

```
micromamba create -n cp2k -c conda-forge "cp2k=2026.2=*mpich*"
micromamba run -n cp2k cp2k.psmp -i run.inp -o cp2k.out
```

The package needs glibc 2.38 or newer. On Debian 12 (glibc 2.36) the binary stops with "GLIBC_2.38 not found", so the recipe image is built on Ubuntu 24.04. The image is 3.0 GB. The basis and pseudopotential files are in `share/cp2k/data` inside the environment, and the input refers to them by name.

## Run the tested example

This recipe builds CP2K in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 9.2 s.

1. Download [cp2k-recipe.tar.gz](https://biosimhub.pages.dev/guides/cp2k/cp2k-recipe.tar.gz) (Dockerfile, run_cp2k.py, example structure.xyz, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf cp2k-recipe.tar.gz
   cd cp2k
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/cp2k:2026.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/cp2k:2026.2 python /opt/run_cp2k.py --xyz /work/in/structure.xyz \
    --run_type ENERGY --xc PBE --basis DZVP-MOLOPT-SR-GTH \
    --cutoff 300 --box 10 --charge 0 --eps_scf 1e-06 \
    --max_steps 50 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cp2k.out` | 71.6 KB |
| `run.inp` | 1.3 KB |
| `run_log.txt` | 113 B |
| `summary.json` | 261 B |

<details><summary>First lines of <code>cp2k.out</code></summary>

```
 DBCSR| CPU Multiplication driver                                           BLAS (U)
 DBCSR| Multrec recursion limit                                              512 (U)
 DBCSR| Multiplication stack size                                           1000 (D)
 DBCSR| Maximum elements for images                                    UNLIMITED (U)
 DBCSR| Multiplicative factor virtual images                                   1 (U)
 DBCSR| Use multiplication densification                                       T (D)
 DBCSR| Multiplication size stacks                                             3 (U)
 DBCSR| Use memory pool for CPU allocation                                     F (U)
 DBCSR| Number of 3D layers                                               SINGLE (U)
 DBCSR| Use MPI memory allocation                                              F (U)
 DBCSR| Use RMA algorithm                                                      F (U)
 DBCSR| Use Communication thread                                               T (U)
```

</details>

<details><summary>First lines of <code>run.inp</code></summary>

```
&GLOBAL
  PROJECT run
  RUN_TYPE ENERGY
  PRINT_LEVEL MEDIUM
&END GLOBAL
&FORCE_EVAL
  METHOD Quickstep
  &DFT
    BASIS_SET_FILE_NAME BASIS_MOLOPT
    POTENTIAL_FILE_NAME POTENTIAL
    CHARGE 0
    &MGRID
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 3 atoms, 8 electrons, E = -17.21977043794623 Ha, 1 energy evaluations, last SCF 16 steps, gap 10.631896 eV
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "atoms": 3,
 "electrons": 8,
 "total_energy_hartree": -17.21977043794623,
 "energy_evaluations": 1,
 "scf_steps_last": 16,
 "geo_opt_steps": null,
 "homo_lumo_gap_ev": 10.631896,
 "mulliken_charges": [
  -0.2453,
  0.12265,
  0.12265
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--run_type` | Calculation | ENERGY | ENERGY, GEO_OPT |
| `--xc` | Exchange-correlation functional | PBE | PBE, BLYP |
| `--basis` | Basis set | DZVP-MOLOPT-SR-GTH | SZV-MOLOPT-SR-GTH, DZVP-MOLOPT-SR-GTH |
| `--cutoff` | Plane-wave cutoff (Ry) | 300 | 100 to 600 |
| `--box` | Cubic box edge (A) | 10 | 6 to 20 |
| `--charge` | Net charge | 0 | -2 to 2 |
| `--eps_scf` | SCF convergence threshold | 1e-06 | 1e-08 to 0.001 |
| `--max_steps` | Maximum optimisation steps | 50 | 1 to 200 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is a water molecule (O-H 0.9572 A, H-O-H 104.52 degrees) with PBE, the DZVP-MOLOPT-SR-GTH basis, a 300 Ry cutoff and a 10 A box. It took 9.2 s.

- `run_log.txt` has one line: "done: 3 atoms, 8 electrons, E = -17.21977043794623 Ha, 1 energy evaluations, last SCF 16 steps, gap 10.631896 eV".
- `cp2k.out` (73,315 bytes) is the full CP2K log. The SCF table shows the convergence measure falling from 0.69 at iteration 1 to 4.8e-07 at iteration 16, below the 1e-6 threshold. It ends with "SCF run converged in 16 steps".
- `run.inp` is the CP2K input the helper wrote (1,301 bytes).
- `summary.json` holds the energy, the SCF step count, the gap and the Mulliken charges: O -0.2453 and H +0.12265 each.

The 8 electrons are the valence electrons: 6 from oxygen and 1 from each hydrogen. The Mulliken charges sum to zero and have the right sign, with oxygen negative. The "gap" is the Kohn-Sham band gap between the highest occupied and lowest unoccupied orbital, 10.63 eV. The gap depends strongly on the basis (13.38 eV with the smaller SZV basis, below), because a small basis has few virtual orbitals and pushes the lowest one up. Treat it as a basis-dependent number, not as a water band gap.

## Your own runs

Each run changes one value from the example (PBE, DZVP, 300 Ry, 10 A box).

- **Geometry optimisation.** `--run_type GEO_OPT` took 7 energy evaluations and 35 s. The energy went from -17.219770 to -17.219970 Ha (0.2 mHa, 0.0054 eV lower). The final O-H length is 0.9701 A and H-O-H is 104.17 degrees. PBE bonds are slightly longer than the starting 0.9572 A.
- **BLYP instead of PBE.** `--xc BLYP` gave -17.209646 Ha and 22 SCF steps. Different functionals give different absolute energies, so compare only runs that share a functional.
- **Smaller basis.** `--basis SZV-MOLOPT-SR-GTH` gave -17.135344 Ha, 84 mHa (2.3 eV) above the DZVP result, and a gap of 13.38 eV. The single-zeta basis is too small for quantitative work.
- **Cutoff.** `--cutoff 600` gave -17.219687 Ha in 29 s, 0.08 mHa from the 300 Ry value. `--cutoff 150` gave -17.225795 Ha in 4 s, 6 mHa lower than the converged value. A lower energy at a lower cutoff means the grid is too coarse. Converge the cutoff before comparing energies.
- **Box size.** `--box 6` gave -17.219815 Ha in 5 s and `--box 16` gave -17.219689 Ha in 70 s. The open boundary conditions make the answer nearly independent of the box once it holds the density, so a larger box only costs time.
- **Charge +2.** `--charge 2` gave 6 electrons, -15.675356 Ha and a gap of 0.77 eV.

## Pitfalls

- **Odd electron counts.** The helper handles closed-shell systems only. It stops with an error when the electron count is odd, so a radical or a single-charge ion needs a spin-polarised input that the recipe does not write.
- **Cutoff is in Ry.** CP2K reports the density cutoff in hartree, so 300 Ry appears as 150.0 a.u. in the log.
- **Timing grows with the box and the cutoff.** The 16 A box took 70 s and the 600 Ry cutoff 29 s, against 9.2 s for the example. The default limit is 300 s.
- **Pseudopotential and functional must match.** The helper picks `GTH-PBE` or `GTH-BLYP` from `--xc`. In your own input, use the pseudopotential generated for the functional you run.
- **Only one core.** The recipe runs `cp2k.psmp` on one process with one thread. Real systems need MPI and more cores.

## Further reading

- CP2K manual: https://manual.cp2k.org
- CP2K input reference for GPW: https://manual.cp2k.org/trunk/CP2K_INPUT/FORCE_EVAL/DFT.html
- Source: https://github.com/cp2k/cp2k
- Paper: Kuehne TD et al. (2020) CP2K: An electronic structure and molecular dynamics software package - Quickstep: Efficient and accurate electronic structure calculations. J Chem Phys 152:194103. https://doi.org/10.1063/5.0007045

---

Cite: Kuehne TD, et al. (2020). CP2K: An electronic structure and molecular dynamics software package - Quickstep: Efficient and accurate electronic structure calculations. J Chem Phys 152:194103. doi:10.1063/5.0007045

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cp2k).
