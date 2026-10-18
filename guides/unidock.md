# Uni-Dock

> GPU-accelerated docking of many small-molecule ligands into one protein target, using the Vina, Vinardo or AD4 scoring functions.

Licence: Apache-2.0 · [Source code](https://github.com/dptech-corp/Uni-Dock)

## What it simulates

Uni-Dock docks small molecules (ligands) into a rigid protein receptor and scores the poses. It is a GPU port of the AutoDock Vina search with batching, built for virtual screening of very large ligand libraries. It supports the Vina, Vinardo and AD4 scoring functions. The project reports a speed-up of more than 2000 times on a V100 GPU compared with AutoDock Vina on one CPU core.

As in Vina, you give a box in the receptor frame (centre and size in Angstrom). The program searches ligand positions, orientations and twists inside the box and returns the best poses with scores. More negative scores predict a better fit. Scores rank candidates; they are not binding free energies.

## When to use it

- You screen thousands to millions of ligands against one target and have an NVIDIA GPU.
- You want Vina-style scores and a Vina-like command line, with batch input.
- You need preparation helpers: the companion package Uni-Dock Tools handles SDF input and output for the vina and vinardo scoring functions.

Alternatives:

- [AutoDock Vina](vina.md) runs on CPU and fits a few ligands. It is the reference method Uni-Dock accelerates.
- [LightDock](lightdock.md) docks protein with protein or peptide on CPU.
- [OpenMM](openmm.md) tests whether a docked pose holds in molecular dynamics.

## Install

Uni-Dock officially supports NVIDIA GPUs with compute capability 7.0 or higher on Linux. The README gives the conda install:

```
conda create -n unidock_env unidock -c conda-forge
conda activate unidock_env
unidock --help
```

The current conda-forge release is 1.2.0. Its files are linux-64 builds for CUDA 12.9, with Python 3.11 and 3.12 variants. There is no arm64 build and no CPU build. The source build needs the CUDA toolkit 11.8 or newer, CMake 3.16 or newer, a C++ compiler and Boost 1.72 or newer.

This site has no recipe for Uni-Dock. The job server has no GPU, and the program has no CPU path, so a recipe would not run. Run it on your own GPU machine.

## A first run

Adapted from the project README (https://github.com/dptech-corp/Uni-Dock/blob/main/unidock/README.md):

```
unidock --receptor receptor.pdbqt \
     --gpu_batch lig1.pdbqt lig2.pdbqt lig3.pdbqt \
     --search_mode balance \
     --scoring vina \
     --center_x 0 --center_y 0 --center_z 0 \
     --size_x 20 --size_y 20 --size_z 20 \
     --num_modes 1 \
     --dir out
```

- `--receptor`: the rigid receptor, in PDBQT or PDB format.
- `--gpu_batch`: ligands to dock on the GPU, separated by spaces. PDBQT and SDF are accepted.
- `--search_mode`: `fast`, `balance` or `detail`. The README maps them to settings: fast is `--exhaustiveness 128` with `--max_step 20`, balance is 384 with 40, and detail is 512 with 40. Higher values cost more and improve accuracy.
- `--scoring`: `vina` (default), `vinardo` or `ad4`. The `ad4` option needs affinity maps through `--maps`.
- `--dir`: the folder for output poses.

The box values above are placeholders. Use the coordinates of your binding site.

## Reading the output

Each ligand gets a PDBQT file in the output folder with its best poses. Each pose carries a score in kcal/mol in a `REMARK VINA RESULT` line, as in Vina output, and lower is better. The log reports the docking time. With `--num_modes 1` only the best pose per ligand is kept, which suits ranking a large library.

Check a few top-scoring ligands by eye, and re-dock a known ligand first to confirm the box and settings reproduce its pose. This page quotes no result numbers, because it was not run here.

## Pitfalls

- **No GPU, no run.** The program requires CUDA. The conda package depends on `cuda-version >=12.9`.
- **Rigid receptor.** Flexible side chains are optional through `--flex`, but the backbone stays fixed.
- **Scores are approximate.** Vina-family scoring ranks poorly across different chemotypes. Confirm hits with a more careful method.
- **Search mode changes results.** `fast` suits a first pass over a library, and `detail` suits a short list.
- **Input preparation.** PDBQT files need charges and atom types. Prepare them with the tools in the Vina documentation, such as Meeko.

## Further reading

- Source and README: https://github.com/dptech-corp/Uni-Dock
- Usage and parameters: https://github.com/dptech-corp/Uni-Dock/blob/main/unidock/README.md
- Benchmarks: https://github.com/dptech-corp/Uni-Dock-Benchmarks
- Paper: Yu Y et al. (2023) Uni-Dock: GPU-Accelerated Docking Enables Ultralarge Virtual Screening. J Chem Theory Comput. https://doi.org/10.1021/acs.jctc.2c01145

---

Cite: Yu Y, Cai C, Wang J, Bo Z, Zhu Z, Zheng H (2023). Uni-Dock: GPU-Accelerated Docking Enables Ultralarge Virtual Screening. J Chem Theory Comput 19:3336-3345. doi:10.1021/acs.jctc.2c01145

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/unidock).
