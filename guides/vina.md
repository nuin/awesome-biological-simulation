# AutoDock Vina

> Dock a small-molecule ligand into a rigid receptor inside a search box and return ranked binding poses with scores.

Licence: Apache-2.0 · [Source code](https://github.com/ccsb-scripps/AutoDock-Vina)

## What it simulates

AutoDock Vina docks a small molecule (the ligand) into a protein (the receptor) and ranks the poses it finds. It is a search plus a score, with no dynamics. The receptor is rigid. The ligand can twist around its rotatable bonds. You give Vina a box, and it searches for ligand positions, orientations and twists inside that box.

Each pose gets a score in kcal/mol. More negative means a better predicted fit. Vina reports up to `--num_modes` poses and lists how far each differs from the best one as RMSD lower and upper bounds.

The key assumptions are a rigid receptor, a search limited to your box, and a scoring function fitted to known binding data. The score ranks poses. It does not give a measured binding energy.

Input is a receptor and a ligand, both in PDBQT format (PDB plus partial charges and atom types), and the box centre and size in Angstrom. Output is a PDBQT file with all poses and a log with the score table.

## When to use it

- You have a protein structure and a few candidate ligands and want to rank them or see where they sit.
- You want to ask whether a known ligand's pose is reproduced (redocking).
- You want a quick screening step before more costly methods.

[OpenMM](openmm.md) and [GROMACS](gromacs.md) on biosimhub fit when you need the motion of a complex over time, with flexible protein and water. Use Vina first to place the ligand, then a molecular dynamics tool to test whether the pose holds. Vina does not do dynamics.

## Install it yourself

Pinned to 1.2.7 (conda-forge, checked with a micromamba dry run, 90 MB of downloads):

```
micromamba create -n vina -c conda-forge vina=1.2.7
micromamba activate vina
```

The Vina documentation prepares inputs with Meeko. The commands from its basic docking tutorial are:

```
mk_prepare_receptor.py -i 1iep_receptorH.pdb -o 1iep_receptor -p -v
mk_prepare_ligand.py -i 1iep_ligand.sdf -o 1iep_ligand.pdbqt
```

The tutorial prepares the ligand from an SDF file, since a PDB file has no bond information. Meeko is a separate package and is not in the recipe's image.

The `vina` command line, as printed by `vina --help` in the 1.2.7 container, has these main options: `--receptor`, `--ligand`, `--center_x/y/z`, `--size_x/y/z`, `--exhaustiveness` (default 8), `--num_modes` (default 9), `--scoring` (`ad4`, `vina` or `vinardo`, default `vina`), `--seed` (default 0), `--cpu` and `--out`.

Minimal run:

```
vina --receptor receptor.pdbqt --ligand ligand.pdbqt \
  --center_x 0 --center_y 0 --center_z 0 --size_x 14 --size_y 14 --size_z 14 \
  --out docked.pdbqt
```

## Run the tested example

This recipe builds AutoDock Vina in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 1.3 s.

1. Download [vina-recipe.tar.gz](https://biosimhub.pages.dev/guides/vina/vina-recipe.tar.gz) (Dockerfile, example receptor.pdbqt, ligand.pdbqt, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf vina-recipe.tar.gz
   cd vina
   sh run.sh
   ```

![Terminal recording of the AutoDock Vina example run](https://biosimhub.pages.dev/media/vina/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/vina:1.2.7 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/vina:1.2.7 vina --receptor /work/in/receptor.pdbqt --ligand /work/in/ligand.pdbqt \
    --center_x 0 --center_y 0 --center_z 0 --size_x 14 \
    --size_y 14 --size_z 14 --exhaustiveness 8 \
    --num_modes 9 --scoring vina --seed 42 --cpu 1 \
    --out docked.pdbqt > out/vina_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `docked.pdbqt` | 5.9 KB |
| `vina_log.txt` | 2.0 KB |

<details><summary>First lines of <code>docked.pdbqt</code></summary>

```
MODEL 1
REMARK VINA RESULT:    -1.231      0.000      0.000
REMARK INTER + INTRA:          -1.303
REMARK INTER:                  -1.303
REMARK INTRA:                   0.000
REMARK UNBOUND:                 0.000
ROOT
ATOM      1 C1   LIG A   1      -0.767  -1.017   3.607  1.00  0.00     0.050 C 
ATOM      2 C2   LIG A   1       0.708  -1.072   3.336  1.00  0.00     0.050 C 
ENDROOT
BRANCH   2   3
ATOM      3 C3   LIG A   1       1.321   0.298   3.076  1.00  0.00     0.100 C 
```

</details>

<details><summary>First lines of <code>vina_log.txt</code></summary>

```
AutoDock Vina f458505-mod
#################################################################
# If you used AutoDock Vina in your work, please cite:          #
#                                                               #
# J. Eberhardt, D. Santos-Martins, A. F. Tillack, and S. Forli  #
# AutoDock Vina 1.2.0: New Docking Methods, Expanded Force      #
# Field, and Python Bindings, J. Chem. Inf. Model. (2021)       #
# DOI 10.1021/acs.jcim.1c00203                                  #
#                                                               #
# O. Trott, A. J. Olson,                                        #
# AutoDock Vina: improving the speed and accuracy of docking    #
# with a new scoring function, efficient optimization and       #
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--center_x` | Box centre x (A) | 0 | -1000 to 1000 |
| `--center_y` | Box centre y (A) | 0 | -1000 to 1000 |
| `--center_z` | Box centre z (A) | 0 | -1000 to 1000 |
| `--size_x` | Box size x (A) | 14 | 1 to 60 |
| `--size_y` | Box size y (A) | 14 | 1 to 60 |
| `--size_z` | Box size z (A) | 14 | 1 to 60 |
| `--exhaustiveness` | Exhaustiveness of the search | 8 | 1 to 64 |
| `--num_modes` | Maximum binding modes | 9 | 1 to 20 |
| `--scoring` | Scoring function | vina | vina, vinardo |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is a toy. The receptor is 48 atoms placed around the origin. The ligand has 5 atoms (C1, C2, C3, O1 and HO) and one rotatable bond (`TORSDOF 1`). The example is a toy so that it runs in about a second. The scores are therefore weak. A real protein-ligand pair scores much lower.

The example runs `vina` directly with `--cpu 1` and seed 42, with no helper script.

- `vina_log.txt` (2,068 bytes): the Vina banner and citations, then the settings: `Scoring function : vina`, `Grid center: X 0 Y 0 Z 0`, `Grid size  : X 14 Y 14 Z 14`, `Exhaustiveness: 8`, `CPU: 1` and `Performing docking (random seed: 42)`. After the progress bar comes the table of 9 modes.
- `docked.pdbqt` (6,075 bytes): 9 `MODEL` blocks, one per pose. Each starts with `REMARK VINA RESULT:    -1.231      0.000      0.000`, which holds the score and the two RMSD bounds. The next lines split the score into `INTER + INTRA`, `INTER`, `INTRA` and `UNBOUND`.

The best pose scores -1.231 kcal/mol (`INTER` -1.303, `INTRA` 0). The other eight range from -1.228 to -1.184. The poses differ by 2.2 to 6.7 Angstrom RMSD from the best, so the scores of very different poses are within 0.05 kcal/mol. The table is flat because the toy receptor does not favour one pose.

## Your own runs

Same image and box; only the stated option changed.

**Vinardo scoring** (`--scoring vinardo`). The best pose scores -1.415 and the nine scores run from -1.415 to -1.383. The spread is 0.03 kcal/mol, against 0.05 for Vina scoring. Treat Vina and Vinardo values as separate scales.

**More search effort** (`--exhaustiveness 32`). The best score is -1.232, against -1.231 at 8, and the RMSDs of the other poses change (the 2nd pose sits 5.8 Angstrom from the best, against 2.2). The Vina tutorial says higher exhaustiveness gives a more consistent result. Here the top score barely moves because the toy surface is flat.

**Different seed** (`--seed 5`). The best score is -1.232, and the 2nd pose is -1.225 at 3.6 Angstrom, against -1.228 at 2.2 with seed 42. Seeds change which poses are reported, so compare seeds when the table is flat.

**Box away from the pocket** (`--center_x 30`). All nine poses score 0.000. The ligand has no receptor contact there.

**Smaller box** (`--size_x 4 --size_y 4 --size_z 4`). The best score is -0.936, and only eight modes come back instead of nine. A box that is too tight can exclude better poses.

## Pitfalls

- **The box decides the answer.** Vina searches only the box. Place it on the binding site and make it a few Angstrom larger than the ligand. The Vina tutorial uses 20 x 20 x 20 Angstrom for its example.
- **Seeds and exhaustiveness.** The default seed is 0. Set one for reproducibility, and rerun with exhaustiveness 32 as in the tutorial before trusting a ranking.
- **Score units.** Scores are in kcal/mol, with negative values for favourable binding. Do not compare scores across scoring functions. The Vina tutorial says AutoDock and Vina scores are not comparable.
- **PDBQT preparation.** Vina needs charges and atom types in the PDBQT files. A plain PDB file does not work. Prepare the ligand from a file with bond information, such as SDF.
- **Rigid receptor.** Side chains do not move unless you supply `--flex`. Poses for ligands that need an induced fit can be wrong.

## Further reading

- Documentation: https://autodock-vina.readthedocs.io/en/latest/
- Basic docking tutorial: https://autodock-vina.readthedocs.io/en/latest/docking_basic.html
- Source: https://github.com/ccsb-scripps/AutoDock-Vina
- Paper: Trott O, Olson AJ (2010), J Comput Chem 31:455-461, https://doi.org/10.1002/jcc.21334
- Vina 1.2 paper: Eberhardt J et al. (2021), J Chem Inf Model, https://doi.org/10.1021/acs.jcim.1c00203

---

Cite: Trott O, Olson AJ (2010). AutoDock Vina. J Comput Chem 31:455-461. doi:10.1002/jcc.21334

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/vina).
