# AutoDock4

> Dock a ligand into a rigid receptor with AutoGrid 4 energy maps and the AutoDock 4 Lamarckian genetic algorithm, returning clustered poses with estimated binding energies.

Licence: GPL-2.0-or-later · [Source code](https://github.com/ccsb-scripps/AutoDock-GPU)

## What it simulates

AutoDock 4 docks a small molecule (the ligand) into a protein (the receptor) and ranks the poses it finds. It is a search plus a score, with no dynamics. The receptor is rigid in this recipe. The ligand can move, rotate and twist around its rotatable bonds.

Docking runs in two steps. AutoGrid 4 pre-computes an energy map on a 3D grid for each ligand atom type, plus an electrostatic map and a desolvation map. AutoDock 4 then searches ligand positions with a Lamarckian genetic algorithm and scores each one by reading the maps. The score is an estimated free energy of binding in kcal/mol, where more negative means a better predicted fit. The score is a ranking tool. It is not a measured binding energy.

The key assumptions are a rigid receptor, a search limited to the grid box, and a force field with empirical weights for van der Waals, hydrogen bonding, electrostatics, desolvation and torsional entropy.

## When to use it

- You have a protein structure and a ligand and want its binding site, pose and a rough score.
- You want to check whether a known pose is reproduced (redocking).
- You want to compare with [AutoDock Vina](vina.md), which uses a different scoring function and a different search.

AutoDock-GPU is the OpenCL and CUDA port of the same method and reads the same AutoGrid maps. This recipe runs the CPU program from AutoDock 4.2.6, not AutoDock-GPU. For the motion of a complex over time, use [OpenMM](openmm.md) or [GROMACS](gromacs.md) after docking.

## Install it yourself

On Debian 12 the recipe installs the packaged programs:

```
apt-get install autodock=4.2.6-9 autogrid=4.2.6-9
autodock4 -v
```

`autodock4 -v` printed "AutoDock 4.2.6" with double-precision calculations on and OpenMP off. The conda-forge and bioconda channels have no AutoDock 4 package. The AutoDock-GPU repository is at https://github.com/ccsb-scripps/AutoDock-GPU.

The example inputs came from PDB entry 181L, T4 lysozyme L99A with benzene in its buried cavity. Open Babel made the PDBQT files with Gasteiger charges and polar hydrogens:

```
obabel -ipdb prot.pdb -opdbqt -O receptor.pdbqt -xr -h --partialcharge gasteiger
obabel -ipdb bnz.pdb -opdbqt -O ligand.pdbqt -h --partialcharge gasteiger
```

`prot.pdb` holds the ATOM records of the chain (1601 PDBQT atoms) and `bnz.pdb` holds the 6 benzene atoms. Waters, chloride and the other ligands were removed. The ligand file keeps the crystal coordinates, which is what makes the reference RMSD below meaningful.

## Run the tested example

This recipe builds AutoDock4 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 5.3 s.

1. Download [autodock4-recipe.tar.gz](https://biosimhub.pages.dev/guides/autodock4/autodock4-recipe.tar.gz) (Dockerfile, run_autodock.py, example receptor.pdbqt, ligand.pdbqt, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf autodock4-recipe.tar.gz
   cd autodock4
   sh run.sh
   ```

![Terminal recording of the AutoDock4 example run](https://biosimhub.pages.dev/media/autodock4/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/autodock4:4.2.6 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/autodock4:4.2.6 python3 /opt/run_autodock.py /work/in/receptor.pdbqt /work/in/ligand.pdbqt \
    --center 26.9 6.1 4.2 --size 18 --spacing 0.375 \
    --runs 10 --pop 150 --evals 250000 --rmstol 2 \
    --seed 42 > out/autodock4_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `autodock4_log.txt` | 190 B |
| `autodock_stdout.txt` | 0 B |
| `autogrid_stdout.txt` | 0 B |
| `best_pose.pdbqt` | 1.9 KB |
| `dock.dlg` | 40.0 KB |
| `dock.dpf` | 576 B |
| `grid.glg` | 188.3 KB |
| `grid.gpf` | 234 B |
| `ranking.csv` | 285 B |
| `rec.A.map` | 939.6 KB |
| `rec.d.map` | 689.5 KB |
| `rec.e.map` | 740.3 KB |
| `rec.maps.fld` | 1.1 KB |
| `rec.maps.xyz` | 42 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/autodock4/result-dark.png"><img src="https://biosimhub.pages.dev/media/autodock4/result.png" alt="Plot of the AutoDock4 example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>autodock4_log.txt</code></summary>

```
autogrid: 49^3 points, spacing 0.375, receptor types A C HD N NA OA S, ligand types A
autodock: 10 runs, 1 clusters at rmstol 2.0
best: run 3, binding energy -4.30 kcal/mol, cluster size 10
```

</details>

<details><summary>First lines of <code>best_pose.pdbqt</code></summary>

```
MODEL        3
USER    Run = 3
USER    DPF = dock.dpf
USER  
USER    Estimated Free Energy of Binding    =   -4.30 kcal/mol  [=(1)+(2)+(3)-(4)]
USER    Estimated Inhibition Constant, Ki   =  707.24 uM (micromolar)  [Temperature = 298.15 K]
USER    
USER    (1) Final Intermolecular Energy     =   -4.30 kcal/mol
USER        vdW + Hbond + desolv Energy     =   -4.30 kcal/mol
USER        Electrostatic Energy            =   +0.00 kcal/mol
USER    (2) Final Total Internal Energy     =   +0.00 kcal/mol
USER    (3) Torsional Free Energy           =   +0.00 kcal/mol
```

</details>

<details><summary>First lines of <code>dock.dlg</code></summary>

```
          AutoDock 4.2 Release 4.2.6   
         (C) 1989-2012 The Scripps Research Institute
        AutoDock comes with ABSOLUTELY NO WARRANTY.
        AutoDock is free software, and you are welcome
        to redistribute it under certain conditions;
        for details type 'autodock4 -C'

                     main.cc  $Revision: 1.213 $

                   Compiled on Feb 20 2022 at 09:48:33


```

</details>

<details><summary>First lines of <code>dock.dpf</code></summary>

```
autodock_parameter_version 4.2
outlev 1
intelec
seed 42
ligand_types A
fld rec.maps.fld
map rec.A.map
elecmap rec.e.map
desolvmap rec.d.map
move /work/in/ligand.pdbqt
tran0 random
quat0 random
```

</details>

<details><summary>First lines of <code>grid.glg</code></summary>

```

       _______________________________________________________

__________//____________________________/////_________________/________
_________/__/____________/_____________/______________/_______/________
________/____/___________/_____________/______________________/________
________/____/__/_____/_/////___/////__/__////_/_///__/__////_/________
_______/______/_/_____/__/_____/_____/_/_____/_//___/_/_/____//________
_______////////_/_____/__/_____/_____/_/_____/_/______/_/_____/________
_______/______/_/____//__/___/_/_____/_/_____/_/______/_/____//________
_______/______/__////_/___///___/////___/////__/______/__////_/________

```

</details>

<details><summary>First lines of <code>grid.gpf</code></summary>

```
npts 48 48 48
gridfld rec.maps.fld
spacing 0.375
receptor_types A C HD N NA OA S
ligand_types A
receptor /work/in/receptor.pdbqt
gridcenter 26.9 6.1 4.2
smooth 0.5
map rec.A.map
elecmap rec.e.map
dsolvmap rec.d.map
dielectric -0.1465
```

</details>

<details><summary>First lines of <code>ranking.csv</code></summary>

```
rank,sub_rank,run,binding_energy_kcal_mol,cluster_rmsd,reference_rmsd
1,1,3,-4.3,0.0,0.85
1,2,4,-4.3,0.04,0.85
1,3,6,-4.3,0.02,0.85
1,4,2,-4.3,0.03,0.85
1,5,1,-4.3,0.03,0.85
1,6,5,-4.3,0.03,0.85
1,7,8,-4.29,0.07,0.87
1,8,9,-4.29,0.07,0.86
1,9,10,-4.29,0.05,0.86
1,10,7,-4.29,0.11,0.89
```

</details>

<details><summary>First lines of <code>rec.A.map</code></summary>

```
GRID_PARAMETER_FILE grid.gpf
GRID_DATA_FILE rec.maps.fld
MACROMOLECULE /work/in/receptor.pdbqt
SPACING 0.375
NELEMENTS 48 48 48
CENTER 26.900 6.100 4.200
-0.088
-0.113
-0.142
-0.185
-0.228
-0.265
```

</details>

<details><summary>First lines of <code>rec.d.map</code></summary>

```
GRID_PARAMETER_FILE grid.gpf
GRID_DATA_FILE rec.maps.fld
MACROMOLECULE /work/in/receptor.pdbqt
SPACING 0.375
NELEMENTS 48 48 48
CENTER 26.900 6.100 4.200
0.176
0.207
0.230
0.281
0.316
0.349
```

</details>

<details><summary>First lines of <code>rec.e.map</code></summary>

```
GRID_PARAMETER_FILE grid.gpf
GRID_DATA_FILE rec.maps.fld
MACROMOLECULE /work/in/receptor.pdbqt
SPACING 0.375
NELEMENTS 48 48 48
CENTER 26.900 6.100 4.200
0.027
0.030
0.033
0.034
0.034
0.030
```

</details>

<details><summary>First lines of <code>rec.maps.fld</code></summary>

```
# AVS field file
#
# AutoDock Atomic Affinity and Electrostatic Grids
#
# Created by autogrid4.
#
#SPACING 0.375
#NELEMENTS 48 48 48
#CENTER 26.900 6.100 4.200
#MACROMOLECULE /work/in/receptor.pdbqt
#GRID_PARAMETER_FILE grid.gpf
#
```

</details>

<details><summary>First lines of <code>rec.maps.xyz</code></summary>

```
17.900 35.900
-2.900 15.100
-4.800 13.200
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--center` | Grid centre x (A) | 26.9 | -1000 to 1000 |
| `center_y` | Grid centre y (A) | 6.1 | -1000 to 1000 |
| `center_z` | Grid centre z (A) | 4.2 | -1000 to 1000 |
| `--size` | Grid box edge (A) | 18 | 6 to 40 |
| `--spacing` | Grid spacing (A) | 0.375 | 0.2 to 0.6 |
| `--runs` | Genetic algorithm runs | 10 | 1 to 50 |
| `--pop` | Population size | 150 | 50 to 500 |
| `--evals` | Maximum energy evaluations per run | 250000 | 10000 to 2500000 |
| `--rmstol` | Cluster RMSD tolerance (A) | 2 | 0.5 to 5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper `run_autodock.py` reads the atom types from the two PDBQT files, writes `grid.gpf` and `dock.dpf`, runs `autogrid4` and `autodock4`, and extracts a ranking and the best pose. The default grid is centred on the benzene at (26.9, 6.1, 4.2), 18 A wide at 0.375 A spacing, which is 49 points per side. The search is 10 genetic algorithm runs with a population of 150 and 250,000 energy evaluations per run. The capture took 5.3 s on one CPU.

- `autodock4_log.txt` has the summary: receptor types A, C, HD, N, NA, OA and S, ligand type A, 10 runs in 1 cluster, and a best energy of -4.30 kcal/mol from run 3.
- `ranking.csv` has one row per run: cluster rank, rank in the cluster, run number, binding energy, cluster RMSD and reference RMSD. All 10 runs fall in cluster 1 with energies of -4.30 to -4.29 kcal/mol.
- `best_pose.pdbqt` is the best run as one MODEL block. Its header lists the estimated free energy (-4.30 kcal/mol), the inhibition constant (707 uM) and the terms. Intermolecular energy is -4.30, electrostatics 0.00, internal energy 0.00 and torsional energy 0.00, since benzene has no rotatable bonds and zero partial charge.
- `dock.dlg` (about 41 KB) is the full AutoDock log, and `grid.glg` is the AutoGrid log. The maps are `rec.A.map`, `rec.e.map` and `rec.d.map`.

The reference RMSD is the distance from the input ligand coordinates, here the crystal pose. The best run is 0.85 A from the crystal benzene, and the other runs are 0.84 to 0.89 A. The method found the buried cavity from random starting positions. Benzene is a symmetric ring and the RMSD compares atoms by index, so the value can overstate the difference.

## Your own runs

Each run below changes values from the example (seed 42, 10 runs, 250,000 evaluations).

- **Another seed.** `--seed 43` gave -4.30 kcal/mol, 1 cluster of 10 and a reference RMSD of 0.85 A. The result does not depend on the seed here, because the cavity is small and the ligand has no torsions.
- **Fewer runs and evaluations.** `--runs 3 --evals 20000` took about 1 s and gave -4.28 kcal/mol in 1 cluster of 3, 0.96 A from the crystal pose.
- **Coarser, smaller grid.** `--size 12 --spacing 0.5` gave a 25-point grid and -4.28 kcal/mol, 0.92 A from the crystal pose.
- **More evaluations.** `--evals 2500000` took 25 s and gave -4.30 kcal/mol, 0.84 A. Ten times the evaluations changed the energy by less than 0.01 kcal/mol.
- **Wrong box.** A grid centred at (26.9, 6.1, 20) and 10 A wide missed the cavity. The best energy was -2.06 kcal/mol, 18.62 A from the crystal pose, with all 10 runs in one cluster. Agreement between runs does not show that the site is right.

## Pitfalls

- **A rigid, tiny test case.** Benzene has no torsions and no charge. A drug-like ligand with 5 to 15 torsions needs more runs and evaluations, and its clusters will not all agree.
- **Charges come from your preparation.** The receptor in the example has a net Gasteiger charge of 0.09, and its protonation states were not checked. Prepare real work with a tool that sets them deliberately.
- **One map per ligand atom type.** AutoGrid builds a map for each ligand atom type, and the helper reads the types from the PDBQT. A ligand with other atom types needs no change to the command.
- **The box limits the search.** The search stays inside the grid. Centre the box on the site and make it 6 to 10 A larger than the ligand.
- **Scores are for ranking.** The estimated free energy of -4.30 kcal/mol is a model output. Compare poses and ligands with the same setup, not against a measured affinity.

## Further reading

- AutoDock documentation and downloads: https://autodock.scripps.edu
- AutoDock-GPU: https://github.com/ccsb-scripps/AutoDock-GPU
- Open Babel: https://openbabel.org
- Paper: Morris GM et al. (2009) AutoDock4 and AutoDockTools4: Automated docking with selective receptor flexibility. J Comput Chem 30:2785-2791. https://doi.org/10.1002/jcc.21256

---

Cite: Morris GM, Huey R, Lindstrom W, Sanner MF, Belew RK, Goodsell DS, Olson AJ (2009). AutoDock4 and AutoDockTools4: Automated docking with selective receptor flexibility. J Comput Chem 30:2785-2791. doi:10.1002/jcc.21256

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/autodock4).
