# COBRA Toolbox

> MATLAB suite for constraint-based modelling of genome-scale metabolic networks, with flux balance analysis, variability analysis and sampling.

Licence: GPL-3.0 · [Source code](https://github.com/opencobra/cobratoolbox)

## What it simulates

The COBRA Toolbox (COnstraint-Based Reconstruction and Analysis) models the steady-state metabolism of a cell. A model is a stoichiometric matrix S with one row per metabolite and one column per reaction, plus lower and upper bounds on each reaction flux. At steady state, production equals consumption for every internal metabolite: S v = 0.

Flux balance analysis (FBA) picks the flux vector v that maximises or minimises a linear objective, usually biomass production, within the bounds. The toolbox adds many variants: parsimonious FBA, flux variability analysis, gene and reaction knock-outs, flux sampling, and context-specific model building from omics data. The optimal objective value is unique, but the flux vector that gives it usually is not.

Key assumptions: steady state, no kinetics or concentrations, linear constraints, and a stated objective. There is no time axis.

## When to use it

- You have a genome-scale reconstruction (for example the E. coli core model or a human model) and want growth predictions, knock-out effects or flux ranges.
- You work in MATLAB and want the many published COBRA methods in one package.
- You follow a published protocol that uses `optimizeCbModel` and related functions.

Alternatives:

- [RAVEN Toolbox](raven-toolbox.md) is another MATLAB toolbox, strong at building draft models from genomes.
- [MICOM](micom.md) is a Python tool that joins several metabolic models into a community.
- COBRApy is the Python package for the same style of analysis. It is a separate project and has no page here.

## Install

No recipe is offered. The toolbox runs inside MATLAB, which needs a paid licence. The README and the docs mention no GNU Octave support.

From the project's README and installation page. Clone the repository from a terminal, not from MATLAB, with a shallow clone:

```bash
git clone --depth=1 https://github.com/opencobra/cobratoolbox.git cobratoolbox
```

Then, in MATLAB, change to the `cobratoolbox` folder and run:

```matlab
>> initCobraToolbox
```

Requirements from the installation page: a working MATLAB (no support for versions older than R2014b), git and curl. The latest GitHub release is v3.7.1. A compatible linear programming solver is needed. The docs list Gurobi, TOMLAB/CPLEX, IBM ILOG CPLEX and MOSEK, and give a compatibility table by operating system and MATLAB release. The licence is GPL-3.0.

## A first run

Adapted from the repository's [FBA tutorial script](https://github.com/opencobra/cobratoolbox/blob/master/test/tutorialDerived/analysis/FBA/tutorial_FBA_part1.m), which uses the E. coli core model:

```matlab
fileName = 'ecoli_core_model.mat';
model = readCbModel(fileName);

% glucose uptake 18.5 mmol/gDW/h, unlimited oxygen
model = changeRxnBounds(model, 'EX_glc(e)', -18.5, 'l');
model = changeRxnBounds(model, 'EX_o2(e)', -1000, 'l');

% biomass as the objective
model = changeObjective(model, 'Biomass_Ecoli_core_N(w/GAM)-Nmet2');

FBAsolution = optimizeCbModel(model, 'max')
FBAsolution.f
```

The tutorial states that `FBAsolution.f` "should be 1.6531 mmol gDW-1 hr-1". That figure comes from the tutorial, not from a run on biosimhub.

## Reading the output

- **`FBAsolution.f`.** The optimal objective value. With a biomass objective it is the predicted growth rate in 1/h.
- **`FBAsolution.v`.** The flux through every reaction, in mmol/gDW/h. Negative values on exchange reactions mean uptake, by the toolbox convention that exchanges are written as export.
- **`FBAsolution.stat`.** The solver status in standard form. Check it before trusting `f`.
- **Model fields.** `S`, `mets`, `rxns`, `lb`, `ub`, `c`, `genes` and `rules` hold the stoichiometry, bounds, objective and gene-protein rules.

## Pitfalls

- **Solver set-up.** Most failures come from a missing or incompatible solver. The tutorials start with `tutorial_initialize` and `tutorial_verify`, which check that the solvers work.
- **New MATLAB releases.** The docs warn that a new release can break solver interfaces for a few months.
- **Do not clone from inside MATLAB.** The README says to run the clone in a terminal and to keep `--depth=1`.
- **Exchange sign convention.** Setting `lb = -18.5` allows 18.5 units of uptake, not export.
- **Non-unique fluxes.** Two solvers can return different flux vectors with the same objective. Use flux variability analysis or parsimonious FBA to compare.

## Further reading

- Repository: https://github.com/opencobra/cobratoolbox
- Installation: https://opencobra.github.io/cobratoolbox/stable/installation.html
- Tutorials: https://opencobra.github.io/cobratoolbox/stable/tutorials/index.html
- Heirendt L, Arreckx S, Pfau T, et al. (2019). Creation and analysis of biochemical constraint-based models using the COBRA Toolbox v.3.0. Nat Protoc 14:639-702. https://doi.org/10.1038/s41596-018-0098-2

---

Cite: Heirendt L, Arreckx S, Pfau T, et al. (2019). Creation and analysis of biochemical constraint-based models using the COBRA Toolbox v.3.0. Nat Protoc 14:639-702. doi:10.1038/s41596-018-0098-2

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cobra-toolbox).
