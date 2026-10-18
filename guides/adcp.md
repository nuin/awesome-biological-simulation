# AutoDock CrankPep (ADCP)

> Dock a flexible peptide of up to about 20 residues, or a cyclic peptide, into a rigid receptor by folding it in the receptor's affinity-grid field with Monte Carlo search.

Licence: LGPL-2.0-only · [Source code](https://github.com/ccsb-scripps/ADCP)

## What it simulates

AutoDock CrankPep (ADCP) docks a peptide into a protein. It treats the peptide as a chain that folds. A Monte Carlo search moves the backbone and side chains while the receptor acts as a rigid field of AutoDock affinity grids. The README states that it can dock peptides from 3D structures in PDB files or from a sequence string, that it has redocked peptides of up to 20 residues, and that it handles cyclic peptides.

The method combines ideas from protein folding with the AutoDock scoring function. ADCP builds on CRANKITE (Podtelezhnikov and Wild 2008). The output is a ranked list of peptide poses with a binding score in kcal/mol, and each pose can be compared with a reference structure by RMSD.

Input is a target file (`.trg`) and a peptide sequence. The target file is a zip of affinity maps for the receptor plus pocket information. It is made with the `agfr` program from the same suite.

## When to use it

Use ADCP when the ligand is a peptide that is too flexible for rigid or few-torsion docking, and you know the approximate binding site or can let AutoSite find pockets.

- [AutoDock Vina](vina.md) handles small molecules and short, rigid ligands.
- [OpenMM](openmm.md) and [GROMACS](gromacs.md) can refine or test a docked peptide with molecular dynamics, at far higher cost.

ADCP keeps the receptor rigid. Large receptor motion on binding is outside its model.

## Install

ADCP is part of ADFRsuite, which also holds `agfr`, AutoSite, AutoGrid4, `prepare_receptor` and `prepare_ligand`. The downloads page (https://ccsb.scripps.edu/adcp/downloads/) lists ADFRsuite 1.0 for Linux (an installer, `ADFRsuite_Linux-x867_64_1.0_install.run`) and for macOS (a tarball). There is no conda or PyPI package. It installs to `~/ADFRsuite-1.0` by default and ships its own Python 2.7 interpreter, separate from the system one.

```
chmod a+x ADFRsuite_Linux-x867_64_1.0_install.run
./ADFRsuite_Linux-x867_64_1.0_install.run
export PATH=$HOME/ADFRsuite-1.0/bin:$PATH
```

The GitHub repository holds the C source of the ADCP engine and the Python wrapper `runADCP.py`. It has no releases or tags. Its README describes a second way to use the compiled binary directly, which needs unzipped map files in the working directory. The licence file is the GNU Library General Public License 2.0, and the project site says the suite is LGPL2 except the MSMS surface component, which is free for academic use only and is not used by `adcp`, `agfr`, `prepare_ligand` or `prepare_receptor`.

No container recipe is provided. The install is a binary installer from a project web server, and the example needs affinity maps made by `agfr` and AutoGrid4 from a receptor structure, which cannot be produced without running those programs.

## A first run

Adapted from the project's redocking tutorial (https://ccsb.scripps.edu/adcp/tutorial-redocking/). It redocks the pseudophosphorylated Smad1 peptide into the TPR domain of CHIP (PDB 3Q47). The tutorial data file is `ADCP_tutorial_data.zip` from the same page.

```
reduce 3Q47_rec.pdb > 3Q47_recH.pdb
reduce 3Q47_pep.pdb > 3Q47_pepH.pdb
prepare_receptor -r 3Q47_recH.pdb
prepare_ligand -l 3Q47_pepH.pdb
agfr -r 3Q47_recH.pdbqt -l 3Q47_pepH.pdbqt -asv 1.1 -o 3Q47
adcp -t 3Q47.trg -s npisdvd -N 20 -n 1000000 -o 3Q47_redocking -ref 3Q47_pepH.pdb
```

The first two commands add hydrogens. The next two convert to PDBQT. `agfr` puts the box around the known peptide with 4 angstrom of padding and writes `3Q47.trg`. `adcp` then runs 20 searches (`-N`) of up to 1,000,000 steps each (`-n`). The `-s` argument is the sequence in one-letter codes.

## Reading the output

ADCP writes three kinds of files, as listed in the tutorial:

- `3Q47_redocking_ranked_*.pdb`: the final solutions after clustering, in rank order.
- `3Q47_redocking_*.pdb`: the Monte Carlo trajectory of each search.
- `3Q47_redocking_*.out`: a detailed text output per search.

The terminal prints a table with one row per cluster. Columns are the mode number, the affinity in kcal/mol, the cluster RMSD, the RMSD to the reference (`-ref`), the cluster size, the average RMSD, the best RMSD, the average energy and the run that found the best member.

The tutorial shows an example run on 8 cores: 20 runs of 1,000,000 steps took 148.19 seconds. Mode 1 had an affinity of -17.2 kcal/mol, a reference RMSD of 0.9 angstrom and a cluster size of 245. Mode 2 had -14.7 kcal/mol and 2.5 angstrom. These numbers come from the tutorial page and will differ on other hardware and seeds.

A good redocking has the top cluster close to the reference, large in size, and clearly lower in energy than the next one.

## Pitfalls

- **The search is stochastic.** Two runs with different seeds can give different poses. The `--seed` option reproduces a run for the same version of the code.
- **Use enough searches.** The tutorial suggests 100 replicas with 1 million steps per amino acid, starting from a mix of extended and helical conformations. The default is 50 searches of 2.5 million evaluations each.
- **Scores rank poses.** They are not measured binding energies.
- **Check atom types.** A target file holds maps for chosen atom types. A peptide with a type that has no map cannot be docked with that file.
- **Know the pocket.** With an unknown site, `agfr` offers pocket modes and a GUI. The tutorial centres the box on the known peptide.
- **Python 2.7 is bundled.** ADFRsuite uses its own interpreter. Do not mix it with a system Python.

## Further reading

- ADCP home: https://ccsb.scripps.edu/adcp/
- Downloads: https://ccsb.scripps.edu/adcp/downloads/
- Redocking tutorial: https://ccsb.scripps.edu/adcp/tutorial-redocking/
- Source: https://github.com/ccsb-scripps/ADCP
- Paper: Zhang Y, Sanner MF (2019) AutoDock CrankPep: combining folding and docking to predict protein-peptide complexes. Bioinformatics 35(24):5121-5127. https://doi.org/10.1093/bioinformatics/btz459

---

Cite: Zhang Y, Sanner MF (2019). AutoDock CrankPep: combining folding and docking to predict protein-peptide complexes. Bioinformatics 35(24):5121-5127. doi:10.1093/bioinformatics/btz459

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/adcp).
