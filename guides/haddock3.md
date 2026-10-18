# HADDOCK3

> Information-driven docking of biomolecular complexes as a configurable workflow of rigid-body, flexible and refinement modules.

Licence: Apache-2.0 · [Source code](https://github.com/haddocking/haddock3)

## What it simulates

HADDOCK (High Ambiguity Driven protein-protein DOCKing) builds models of biomolecular complexes from the structures of the parts plus experimental or predicted information about the interface. That information enters as ambiguous interaction restraints (AIRs): a list of residues that probably touch, from NMR, mutagenesis, cross-linking or sequence prediction. HADDOCK3 is the modular Python rewrite of the original program.

A HADDOCK3 run is a workflow written in a TOML-style configuration file. Each step is a module, run in order. The repository's modules fall into groups:

- sampling: `rigidbody`, `gdock`, `lightdock`;
- refinement: `flexref`, `emref`, `mdref`, `cgtoaa`, `openmm`;
- analysis: `caprieval`, `clustfcc`, `clustrmsd`, `seletop`, `seletopclusts`, `alascan`, `contactmap`, and others;
- topology preparation (`topoaa`) before sampling.

Most modules call CNS (Crystallography and NMR System), which does the energy calculations and molecular dynamics. Typical protocols sample many rigid-body poses, select the best, refine them with flexible interfaces, cluster the results and score them against a reference.

## When to use it

- You know or can predict which residues form the interface and want models that satisfy that information.
- You dock proteins with proteins, peptides, DNA, glycans or small ligands, or antibodies with antigens. The repository has an example folder for each.
- You need a documented, repeatable multi-stage workflow that runs locally, on a cluster, or with MPI.

Alternatives:

- [LightDock](lightdock.md) docks without any restraints, on CPU, with a pip install.
- [AutoDock Vina](vina.md) docks small molecules into a rigid receptor.
- [OpenMM](openmm.md) refines or tests a complex with ordinary molecular dynamics.

## Install

The current release is 2026.10.1 on PyPI (Apache-2.0, Python 3.10 up to 3.14). The installation guide gives:

```
python -m venv .venv
source .venv/bin/activate
pip install haddock3
```

Optional extras are `haddock3[mpi]` and `haddock3[notebooks]`. The installer places a precompiled CNS executable under `haddock/cns/bin/` and checks that it runs. If it does not, the project documents compiling CNS yourself (docs/pages/CNS.md in the repository).

This site has no recipe for HADDOCK3. CNS is not covered by HADDOCK3's Apache licence. The project's DISCLAIMER states that CNS is free for non-profit use, that commercial use needs a licence from Biovia, and that each user is responsible for holding one. The CNS site hands out the source to academic users after registration. A shared public job server cannot confirm who runs it or for what purpose, so the recipe is left out. Install it on your own machine under your own licence.

## A first run

Adapted from the project's usage guide (https://github.com/haddocking/haddock3/blob/main/docs/pages/USAGE.md). Clone the repository for the example data, then run a test configuration:

```
cd examples/docking-protein-protein
haddock3 docking-protein-protein-cltsel-test.cfg
```

The usage guide recommends the files ending in `-test.cfg`, which are reduced runs. The configuration in that example names:

- two molecules, `data/e2aP_1F3G.pdb` and `data/hpr_ensemble.pdb`;
- a run directory (`run1-clt-test`) and `mode = "local"`;
- a stage list: `[topoaa]`, `[rigidbody]` with the restraint file `data/e2a-hpr_air.tbl`, `[caprieval]` against the reference `data/e2a-hpr_1GGR.pdb`, `[clustfcc]`, `[seletopclusts]`, `[flexref]`, `[emref]` and more `[caprieval]` stages.

List the options of any module with `haddock3-cfg -m rigidbody`, and all command-line options with `haddock3 -h`.

## Reading the output

The run directory holds one numbered folder per module, such as `0_topoaa` and `1_rigidbody`, in the order of the workflow. Each holds the models that module produced and its parameters. The `caprieval` modules write tables that rank models and clusters and, when a reference is given, report i-RMSD, l-RMSD and the CAPRI quality class. Clustering modules group similar models, and the selection modules pass the best ones to the next stage.

Read the cluster-level results first: a cluster of several consistent models beats a single high-scoring model. This page quotes no numbers, because none was run here.

## Pitfalls

- **CNS is required, and its licence is separate.** Check it before using results in a commercial setting.
- **The shipped CNS binary may not run** on a system with missing libraries. Compile it as the CNS.md guide describes.
- **Restraints drive the answer.** Wrong AIRs give confident wrong models. Use reference-free checks, such as the agreement between clusters.
- **Test configurations are not production runs.** The full configurations sample far more models.
- **Histidine protonation is set by hand.** The example configuration sets histidine states per molecule; wrong states change the models.

## Further reading

- User manual: https://www.bonvinlab.org/haddock3-user-manual
- Source: https://github.com/haddocking/haddock3
- Citing page: https://github.com/haddocking/haddock3/blob/main/CITING.md
- Paper: Dominguez C, Boelens R, Bonvin AMJJ (2003). J Am Chem Soc 125:1731-1737. https://doi.org/10.1021/ja026939x

---

Cite: Dominguez C, Boelens R, Bonvin AMJJ (2003). HADDOCK: a protein-protein docking approach based on biochemical or biophysical information. J Am Chem Soc 125:1731-1737. doi:10.1021/ja026939x

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/haddock3).
