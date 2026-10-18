# RAVEN Toolbox

> MATLAB toolbox that reconstructs genome-scale metabolic models from genomes and databases, then curates and simulates them with flux balance analysis.

Licence: GPL-3.0 · [Source code](https://github.com/SysBioChalmers/RAVEN)

## What it simulates

RAVEN (Reconstruction, Analysis and Visualization of Metabolic Networks) builds and runs genome-scale metabolic models (GEMs). A GEM lists the reactions of an organism, which genes encode them, and bounds on each reaction flux. RAVEN covers the steps before simulation as well as the simulation.

Reconstruction uses published models as templates (transfer by protein homology), the KEGG and MetaCyc databases, or HMMs trained on KEGG orthologs. Curation and gap-filling tools find and fix missing reactions. For simulation, RAVEN solves flux balance analysis (FBA), which finds the steady-state flux vector that maximises an objective such as growth. It also does gene deletions, flux sampling and the ftINIT method for building context-specific models from transcriptomics.

Key assumptions: steady state, linear constraints, a stated objective, and no kinetics or time axis.

## When to use it

- You have a genome and want a draft metabolic model of the organism.
- You want to check, curate and gap-fill a model, and test whether it can grow.
- You build tissue or cell-type models from expression data (ftINIT).

Alternatives:

- [COBRA Toolbox](cobra-toolbox.md) is the other major MATLAB toolbox, with a larger set of analysis methods.
- [MICOM](micom.md) combines several finished models into a community.
- The RAVEN project also publishes a Python package, `raven-toolbox`, built on cobrapy. On PyPI it is at version 0.4.0, and 3.0.0b1 is a pre-release (`pip install --pre raven-toolbox`, MIT). The project documentation calls 3.0.0b1 pre-release software whose API may change.

## Install

No recipe is offered. RAVEN runs inside MATLAB, which needs a paid licence. The README and the install wiki do not mention GNU Octave.

From the project's wiki: MATLAB 2016b or later is required. The latest GitHub release of the MATLAB toolbox is v2.11.4, and the licence is GPL-3.0. The "advanced" route is recommended and needs git:

```bash
git clone --depth=1 https://github.com/SysBioChalmers/RAVEN.git
```

Then in MATLAB:

```matlab
cd('[location]/RAVEN/installation')
checkInstallation
```

`checkInstallation` installs RAVEN, tests it, and picks the default solver. That is Gurobi if present, otherwise GLPK. You can change it later with `setRavenSolver('solverName')`, where the name is `gurobi`, `glpk`, `soplex` or `cobra`. The check also tests the bundled BLAST+, DIAMOND and HMMER programs, which are needed for reconstruction from homology or KEGG. The other routes are the MATLAB Add-Ons Explorer (search "RAVEN Toolbox") and a ZIP download from the releases page.

## A first run

Adapted from `tutorial/tutorial3.m` in the repository, which runs FBA on a small yeast model. The model file `smallYeast.xlsx` is in the same folder.

```matlab
% Import the Excel model
model = importExcelModel('smallYeast.xlsx', true);

% Glucose uptake limited to 1, O2 uptake unlimited
model = setParam(model, 'ub', {'glcIN' 'o2IN'}, [1 1000]);

% Objective: ethanol production
model = setParam(model, 'obj', {'ethOUT'}, 1);

% Solve and print the exchange fluxes
sol = solveLP(model);
printFluxes(model, sol.x, true);
```

The tutorial script goes on to compare aerobic and anaerobic flux maps with `drawMap`, delete single genes with `findGeneDeletions`, and delete the `ZWF` gene to see which fluxes change.

## Reading the output

- **`sol.f`.** The optimal objective value, here ethanol production under the set bounds.
- **`sol.stat`.** The exit flag: 1 means the optimisation ended successfully, 0 a feasible but not necessarily optimal solution, -1 no feasible solution.
- **`sol.x`.** The flux for every reaction in the model, in the order of `model.rxns`.
- **`printFluxes`.** Prints the exchange fluxes: what the model takes up and secretes at the optimum. The `true` argument limits it to exchange reactions.
- **Model structure.** `model.rxns`, `model.mets`, `model.genes`, `model.S`, `model.lb`, `model.ub` and `model.c` hold the network, bounds and objective.
- **Gene deletions.** `findGeneDeletions` returns the flux vector for each knock-out, so you can see which genes stop growth.

This guide has no run of its own on biosimhub, so no output numbers are quoted.

## Pitfalls

- **Two generations of documentation.** The wiki describes RAVEN 2.x. The site raven-docs.readthedocs.io documents RAVEN 3.0.0b1, a pre-release for MATLAB and Python. Check which version you installed before copying code from either.
- **Reconstruction needs outside data.** KEGG-based work needs the KEGG-derived HMMs or database files described in the wiki's External Databases page.
- **Solver choice matters.** GLPK is the free default. The wiki recommends Gurobi as the alternative for larger problems.
- **Add RAVEN to the path for good.** If `checkInstallation` fails at "Save MATLAB path", run `addRavenToUserPath` to write a `startup.m`.
- **Model structure differs from COBRA.** RAVEN has its own model structure. The wiki's page on it lists the fields, and conversion functions exist for COBRA models.

## Further reading

- Repository: https://github.com/SysBioChalmers/RAVEN
- Wiki (RAVEN 2.x): https://github.com/SysBioChalmers/RAVEN/wiki
- Tutorials: https://github.com/SysBioChalmers/RAVEN/wiki/Tutorials
- RAVEN 3 documentation: https://raven-docs.readthedocs.io
- Wang H, Marcišauskas S, Sánchez BJ, Domenzain I, Hermansson D, Agren R, Nielsen J, Kerkhoven EJ (2018). RAVEN 2.0: a versatile toolbox for metabolic network reconstruction and a case study on Streptomyces coelicolor. PLoS Comput Biol 14(10):e1006541. https://doi.org/10.1371/journal.pcbi.1006541

---

Cite: Wang H, Marcišauskas S, Sánchez BJ, Domenzain I, Hermansson D, Agren R, Nielsen J, Kerkhoven EJ (2018). RAVEN 2.0: a versatile toolbox for metabolic network reconstruction and a case study on Streptomyces coelicolor. PLoS Comput Biol 14(10):e1006541. doi:10.1371/journal.pcbi.1006541

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/raven-toolbox).
