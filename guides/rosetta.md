# Rosetta

> Monte Carlo modelling of protein and macromolecular structure for prediction, design, docking and refinement, with a Python interface called PyRosetta.

Licence: LicenseRef-Rosetta-Non-Commercial · [Source code](https://github.com/RosettaCommons/rosetta)

## What it simulates

Rosetta is a suite of algorithms for modelling the structure of proteins and other macromolecules. The README lists de novo protein design, enzyme design, ligand docking, and structure prediction of single molecules and complexes. Most protocols sample conformations by Monte Carlo moves and rank them with the Rosetta energy function, a mix of physics-based and statistical terms. A protocol produces many decoys (candidate structures), and the answer is read from the best-scoring ones.

Rosetta is maintained by RosettaCommons, a collaboration of more than 100 academic groups. It is a set of applications (such as `relax`, docking and design protocols) plus RosettaScripts, an XML language to combine moves. PyRosetta exposes the same library as Python bindings.

## When to use it

Use Rosetta when you need to refine, redesign or dock a protein structure and your lab has access to compute time. The Getting Started page warns that most applications assume access to tens of thousands of hours of computer time.

Alternatives:

- [OpenMM](openmm.md) and [GROMACS](gromacs.md) run molecular dynamics, which follows motion in time and is not a search for low-energy structures.
- [AutoDock Vina](vina.md) docks small molecules, and does nothing for protein design.
- Public servers run common Rosetta protocols for you (see below).

## Install

This guide has no run recipe, and this site does not run Rosetta for visitors. The reason is the licence. `LICENSE.md` allows only Non-Commercial Users to "run, display, copy, use and modify Software free of charge solely for internal Non-Commercial purposes", and its first condition reads: "You agree to refer other Non-Commercial Users interested in the Software to Github to download the Software to ensure quality control, and so that they agree to these license terms." Condition 3 says commercial use, "including fee-based service projects", needs a separate commercial licence from the University of Washington. A public recipe or run form would hand Rosetta to people who never accepted these terms. The README itself says the code is "not Open Source" under the OSI definition. PyRosetta has its own licence (`LICENSE.PyRosetta.md`), which also says use of PyRosetta "requires a valid concurrent non-commercial license of Rosetta".

Official routes, from the README (there are weekly builds, tagged like `v2026.39-dev62290`, and no numbered release):

- **Source.** `git clone https://github.com/RosettaCommons/rosetta`, then `cd source` and `./scons.py -j<N> mode=release bin`. It needs g++ or clang and Python.
- **Conda.** Add the RosettaCommons channel (`https://conda.rosettacommons.org`, with an East coast mirror at `https://conda.graylab.jhu.edu`) to `~/.condarc`, then install the `rosetta` package.
- **Docker.** Official images with Rosetta and PyRosetta are at https://hub.docker.com/r/rosettacommons/rosetta.
- **PyRosetta.** Build from the source tree (`python3 build.py --create-package ...` in `source/src/python/PyRosetta`) or use the Docker image. See https://www.pyrosetta.org.

Commercial users contact license@uw.edu. The Getting Started page also lists public servers for non-commercial use only.

## A first run

Adapted from the [relax application page](https://github.com/RosettaCommons/documentation/blob/main/application_documentation/structure_prediction/relax.md). `relax` is the main protocol for simple all-atom refinement. The page gives this sample command:

```
relax.linuxgccrelease -database /path/to/rosetta/main/database -in:file:s input.pdb -in:file:fullatom -native 1a19.pdb -out:file:silent default.out -relax:quick
```

`-in:file:s` is the input PDB, `-native` is a reference for RMSD, `-out:file:silent` writes decoys to one silent file, and `-relax:quick` does a short relax with 5 cycles (`-relax:thorough` uses 15). `-nstruct` sets the number of output structures per input. The page advises applying relax to idealised structures, because bond-geometry differences otherwise show up as score differences.

## Reading the output

- A silent file or PDB files, one per decoy. Each carries a score table, with total score in Rosetta energy units and the individual terms.
- With `-native`, scores sit next to the RMSD to the reference.
- Compare many decoys. One relaxed structure says little, since each decoy is a random sample. Pick the lowest-scoring decoys and look at how much they agree.
- At the end of a run Rosetta may print citations for the protocols used. The citation guide says the list is not exhaustive, so check the documentation page of the protocol for its papers.

## Pitfalls

- **Weekly builds.** There is no single version. State the build tag in your methods.
- **Database path.** Applications fail without the Rosetta `database` folder. Use `-database`.
- **Scale.** A realistic design or prediction run needs hundreds to thousands of decoys, on a cluster.
- **No one citation.** Cite the papers of the protocols you ran, as CITING_ROSETTA.md asks.
- **Licence and forks.** Forks must keep the licence restrictions, and fee-based services need a commercial licence.

## Further reading

- Source and README: https://github.com/RosettaCommons/rosetta
- Getting Started: https://www.rosettacommons.org/docs/latest/getting_started/Getting-Started
- Citing Rosetta: https://github.com/RosettaCommons/rosetta/blob/main/CITING_ROSETTA.md
- PyRosetta: https://www.pyrosetta.org
- Leaver-Fay A et al. (2011). Methods Enzymol 487:545-574. https://doi.org/10.1016/B978-0-12-381270-4.00019-6

---

Cite: Leaver-Fay A, Tyka M, Lewis SM, et al. (2011). ROSETTA3: an object-oriented software suite for the simulation and design of macromolecules. Methods Enzymol 487:545-574. doi:10.1016/B978-0-12-381270-4.00019-6

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/rosetta).
