# perses

> Relative alchemical free-energy and expanded-ensemble simulations on OpenMM, for small-molecule transformations and protein mutations.

Licence: MIT · [Source code](https://github.com/choderalab/perses)

## What it simulates

perses, from the Chodera lab, runs expanded-ensemble and alchemical free-energy simulations on top of OpenMM. An alchemical simulation changes one molecule into another along a coupling parameter (lambda) that switches interactions off and on. The free-energy difference of the change, taken in the protein-bound state and in solvent, gives a relative binding free energy.

perses builds the hybrid system for you. Given two ligands, it finds an atom mapping, keeps the shared core, and switches the unique atoms off or on across lambda. Given a protein, it can do the same for a point mutation. The README lists the module as "experiments with expanded ensemble simulation to explore chemical and mutational space". Sampling is by replica exchange or by non-equilibrium switching, in which many short trajectories drive lambda from 0 to 1 and the work done is recorded.

The README carries a warning that the code is pre-alpha, that "it is not guaranteed to be completely tested or provide the correct results", and that the API can change without notice.

## When to use it

Use perses to estimate relative binding free energies for a congeneric ligand series, or the effect of a protein mutation, when you can run OpenMM on GPUs.

Alternatives:

- [OpenMM](openmm.md) is the engine underneath. Use it directly when you want to script your own free-energy protocol.
- [GROMACS](gromacs.md) has its own free-energy methods and a command-line workflow.
- [AutoDock Vina](vina.md) docks ligands quickly, and gives scores, not free energies.

## Install

This guide has no run recipe. The conda-forge package `perses` 0.10.3 (noarch) pulls in OpenMM, openmmtools, openff-toolkit, JAX, PyTorch, RDKit and AmberTools. A build of that stack for this site came to 437 packages and 5.6 GB, above the 4 GB image limit. A pruned rebuild did not finish, so there is no tested smaller set of packages. perses 0.10.3 also imports `pkg_resources`, so it fails to import on a Python 3.14 environment unless `setuptools` is installed. Real runs also need a GPU and hours of sampling, which the 1 CPU, 300 s sandbox cannot give.

The README gives the install in a fresh conda environment:

```
conda config --add channels conda-forge openeye
conda install perses openeye-toolkits
```

The [installation page](https://perses.readthedocs.io/en/latest/installation.html) says the same, and recommends this release build for everyone who is not developing new algorithms. The OpenEye toolkits need their own licence. The current release is 0.10.3 (September 2023). Let the conda solver pick a Python version, and keep `setuptools` in the environment. The licence is MIT.

## A first run

Adapted from `examples/dipeptide-neq-switching` in the repository (a README and `run_example.py`). It mutates a capped alanine into a capped aspartic acid and records non-equilibrium work.

```
python run_example.py
```

The script is short. It sets `nsteps_eq = 2` and `nsteps_neq = 32` with a 4 fs timestep at 300 K, builds the hybrid topology with `PointMutationExecutor` from `perses/data/ala_vacuum.pdb` (residue 2 to ASP, ionic strength 0.15 M), and uses a `PeriodicNonequilibriumIntegrator`. It then minimises, equilibrates at lambda 0, runs the forward switch from 0 to 1, equilibrates at lambda 1, and runs the reverse switch. Those step counts are a demonstration size, far below a real calculation.

Larger examples in the same folder include the Tyk2 benchmark with replica exchange (`protein-ligand-repex`, run through the perses command-line tool and a `setup.yaml`) and a kinase protein-ligand switching run.

## Reading the output

- The dipeptide script stores NumPy arrays in `output/`: the dimensionless protocol work of each forward and reverse switch, and the old and new positions saved during equilibration and switching.
- For a free-energy estimate you need many forward and reverse works. The Bennett acceptance ratio, or the Crooks fluctuation theorem, combines them into a free-energy difference. A handful of switches gives a number that means nothing.
- Replica-exchange runs write to storage files that the perses analysis tools read (the documentation has pages on storage and analysis).

## Pitfalls

- **Pre-alpha status.** Check results against a known benchmark such as the Tyk2 set before trusting new ones.
- **Atom mapping decides the result.** The documentation shows how the `core` and `geometry` strategies map atoms differently, and says what is best for a given pair is an open research question.
- **GPU needed.** CPU runs of production length are impractical.
- **Environment weight.** The stack is several gigabytes. Use a dedicated conda environment.
- **Old imports.** The example imports from `simtk` and `pkg_resources`, which can fail on current OpenMM and Python releases, so the examples may need small edits.

## Further reading

- Source and README: https://github.com/choderalab/perses
- Documentation: https://perses.readthedocs.io/
- Examples: https://github.com/choderalab/perses/tree/main/examples
- Zhang I et al. (2023). Identifying and overcoming the sampling challenges in relative binding free energy calculations of a model protein:protein complex. J Chem Theory Comput 19:4863-4882. https://doi.org/10.1021/acs.jctc.3c00333
- Rufa DA et al. (2023). Perses (0.10.3). https://doi.org/10.5281/zenodo.8350218

---

Cite: Rufa DA, Zhang I, Bruce Macdonald HE, Grinaway PB, Pulido I, Henry MM, Rodriguez-Guerra J, Wittmann M, Albanese SK, Glass WG, Silveira A, Schaller D, Naden LN, Chodera JD (2023). Perses (0.10.3). Zenodo. doi:10.5281/zenodo.8350218

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/perses).
