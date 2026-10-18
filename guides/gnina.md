# gnina

> Molecular docking with AutoDock Vina-style search and convolutional neural network scoring of ligand poses, built for NVIDIA GPUs.

Licence: Apache-2.0 and GPL-2.0 (dual) · [Source code](https://github.com/gnina/gnina)

## What it simulates

gnina (pronounced NEE-na) is a molecular docking program. Given a receptor structure and a small-molecule ligand, it searches for binding poses and scores them. It is a fork of smina, which is a fork of AutoDock Vina. The search is Monte Carlo sampling with minimisation inside a box around the binding site. The poses are scored with an empirical function (Vina and others) and, in the main extension over Vina, with convolutional neural networks that look at the 3D grid of atoms around the ligand.

The `--cnn_scoring` option sets where the networks act: `none`, `rescore` (default, final re-ranking of poses), `refinement` (also during minimisation, about ten times slower with a GPU), and `all` (every step, extremely expensive). The default model is an ensemble of three networks. gnina also does flexible side chains, covalent docking, whole-protein docking, and scoring or minimising ligands that are already placed.

## When to use it

Use gnina when plain Vina scoring ranks poses poorly for your target and you have a GPU, or you want to re-score docked libraries with a learned model.

Alternatives:

- [AutoDock Vina](vina.md) is the CPU-only starting point and the engine gnina was forked from.
- [OpenMM](openmm.md) fits when you want molecular dynamics to relax or test a pose.
- Rosetta fits docking with full protein flexibility, under its own licence.

## Install

This guide has no run recipe. The only prebuilt release, v1.3.3 (June 2026), is a CUDA 12.8 binary of about 2 GB. The README requires CUDA 12.0 or newer to build, and the binary loads the CUDA, cuDNN and related libraries at start-up, so it fails with "cannot open shared object file" on a machine without them even when `--no_gpu` is given. The binary plus those libraries are larger than an image the site can run, and the sandbox has no GPU. Neither conda-forge nor bioconda packages gnina, and there is no supported CPU-only source build.

Official routes, from the README:

- **Prebuilt binary.** Download from https://github.com/gnina/gnina/releases/latest. The README recommends it over building from source and says it works in WSL.
- **Docker.** Pre-built images are at https://hub.docker.com/u/gnina and the Dockerfiles are in the `docker` folder. Run them with the NVIDIA container toolkit.
- **From source (Ubuntu 22.04).** Install the apt packages listed in the README, CUDA 12.0 or newer with `nvcc` on the PATH, and OpenBabel 3 built from the dkoes fork (versions 3.1.1 and older have bond-order errors). Then:

```
git clone https://github.com/gnina/gnina.git
cd gnina && mkdir build && cd build
cmake ..
make && make install
```

The build downloads libmolgrid and torch if they are missing. For a cluster with mixed GPUs, add `-DCMAKE_CUDA_ARCHITECTURES=all`.

The licence is dual: Apache-2.0 and GPL-2.0. The README says the GPL comes from the use of OpenBabel.

## A first run

Adapted from the Usage section of the [README](https://github.com/gnina/gnina#usage). To dock `lig.sdf` to the site of `rec.pdb` defined by a reference ligand `orig.sdf`:

```
gnina -r rec.pdb -l lig.sdf --autobox_ligand orig.sdf -o docked.sdf.gz
```

`--autobox_ligand` takes the box from a ligand, with 4 Angstroms of padding on all six sides by default (`--autobox_add`). You can give the box by hand with `--center_x/y/z` and `--size_x/y/z`. Other documented forms:

```
gnina -r rec.pdb -l ligs.sdf --minimize -o minimized.sdf.gz
gnina -r rec.pdb -l lig.sdf --autobox_ligand rec.pdb -o whole_docked.sdf.gz --exhaustiveness 64
```

The first re-scores ligands already in place by minimising them. The second docks over the whole protein. The default exhaustiveness is 8. `--seed` fixes the random seed.

## Reading the output

- The output file (`-o`) holds up to `--num_modes` poses (9 by default), as SDF here, with scores stored on each pose. Poses closer than `--min_rmsd_filter` (1 Angstrom by default) to a better one are dropped.
- Each pose carries an empirical affinity in kcal/mol and the CNN scores. The CNN pose score estimates how likely the pose is to be a good one, and the CNN affinity is a predicted binding strength. The scores are stored as properties in the SDF, and the console prints a table of modes.
- The README does not list example numbers. Look at the scores in the SDF properties for ranking.

## Pitfalls

- **GPU required in practice.** CNN scoring and the binary itself depend on CUDA. `--no_gpu` exists, but the binary still expects the CUDA libraries.
- **CNN modes cost.** `refinement` is about 10 times slower than `rescore` on a GPU, and `all` about 1000 times, per the README.
- **Define the box.** A search space is required. Whole-protein docking needs a higher exhaustiveness.
- **OpenBabel bond orders.** Use OpenBabel newer than 3.1.1 when you build from source.
- **Model choice.** Choose with `--cnn`. The default ensemble changed between 1.0 and 1.3, and `default1.0` keeps the old one. Name the version in the methods.
- **Training data.** The README advises against training virtual-screening models on DUD-E.

## Further reading

- Source and README: https://github.com/gnina/gnina
- Docker images: https://hub.docker.com/u/gnina
- Colab notebook linked from the README: https://colab.research.google.com/drive/1QYo5QLUE80N_G28PlpYs6OKGddhhd931
- McNutt AT et al. (2025). J Cheminformatics 17:28. https://doi.org/10.1186/s13321-025-00973-x
- McNutt AT et al. (2021). GNINA 1.0. J Cheminformatics 13:43. https://doi.org/10.1186/s13321-021-00522-2

---

Cite: McNutt AT, Li Y, Meli R, Aggarwal R, Koes DR (2025). GNINA 1.3: the next increment in molecular docking with deep learning. J Cheminformatics 17:28. doi:10.1186/s13321-025-00973-x

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/gnina).
