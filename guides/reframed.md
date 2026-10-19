# ReFramed

> Constraint-based analysis of a genome-scale metabolic model (SBML): FBA, parsimonious FBA or flux variability analysis, with optional uptake limits and a reaction knockout.

Licence: Apache-2.0 · [Source code](https://github.com/cdanielmachado/reframed)

## What it simulates

ReFramed is a Python package for constraint-based modelling of metabolism. A genome-scale model is a stoichiometric matrix S of metabolites by reactions, with a lower and an upper bound on each reaction flux. Constraint-based methods assume steady state (S v = 0) and search for flux distributions v inside the bounds. They do not simulate time or concentrations.

The README lists the methods, with references: flux balance analysis (FBA), flux variability analysis (FVA), parsimonious FBA (pFBA), loopless FBA, linear MOMA, ROOM, GIMME, E-Flux, thermodynamic flux analysis and variability analysis, constrained-allocation FBA, SteadyCom for communities, and others. The documentation also describes gene and reaction knockouts, essential-gene screens and `Environment` helpers that set the medium.

The README states that the package is discontinued and points to a successor, fluxbound: https://github.com/cdanielmachado/fluxbound. The last release is 1.6.0 (April 2025).

## When to use it

Use ReFramed when you need FBA, FVA or pFBA on an SBML model from a script, or when an existing workflow already depends on it.

- Use [COPASI](copasi.md) for kinetic models with time courses. Constraint-based methods give steady-state fluxes only.
- Use [CNApy](cnapy.md) when you want a graphical interface for the same family of methods, with maps and strain design.
- Use fluxbound (linked above) for new work, since ReFramed is no longer developed.

## Install it yourself

ReFramed is on PyPI and on Bioconda. The conda command below resolves for reframed 1.6.0 (a noarch package, Apache-2.0):

```bash
conda create -n reframed -c conda-forge -c bioconda reframed=1.6.0
conda activate reframed
```

The Bioconda package depends on `python-libsbml`, `scipy`, `numpy`, `sympy` and the SCIP optimiser (`scip` and `pyscipopt`). SCIP is free. The installation page of the documentation says CPLEX and Gurobi are supported directly and need a licence, and that OptLang gives access to other solvers. ReFramed picks a solver by looking for gurobi, cplex, scip and optlang in that order, so the Bioconda package, which carries only SCIP, uses SCIP.

`pip install reframed` also works. In that case install a solver yourself.

The recipe below uses the Bioconda package. The package is noarch, so the image builds natively on arm64 and on amd64.

## Run the tested example

This recipe builds ReFramed in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 0.7 s.

1. Download [reframed-recipe.tar.gz](https://biosimhub.pages.dev/guides/reframed/reframed-recipe.tar.gz) (Dockerfile, run_reframed.py, example model.xml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf reframed-recipe.tar.gz
   cd reframed
   sh run.sh
   ```

![Terminal recording of the ReFramed example run](https://biosimhub.pages.dev/media/reframed/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/reframed:1.6.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/reframed:1.6.0 python /opt/run_reframed.py /work/in/model.xml \
    --method fba --glucose 10 --oxygen 1000 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `fluxes.csv` | 1.4 KB |
| `run_log.txt` | 57 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/reframed/result-dark.png"><img src="https://biosimhub.pages.dev/media/reframed/result.png" alt="Plot of the ReFramed example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>fluxes.csv</code></summary>

```
reaction,flux
R_ACALD,8.8817842e-16
R_ACALDt,8.8817842e-16
R_ACKr,0
R_ACONTa,6.0072496
R_ACONTb,6.0072496
R_ACt2r,0
R_ADK1,0
R_AKGDH,5.0643757
R_AKGt2r,0
R_ALCD2x,0
R_ATPM,8.39
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
fba: status Status.OPTIMAL, objective 0.8739215069684304
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--method` | Method | fba | fba, pfba, fva |
| `--glucose` | Maximum glucose uptake | 10 | 0 to 1000 |
| `--oxygen` | Maximum oxygen uptake | 1000 | 0 to 1000 |
| `--knockout` | Reaction to knock out (id | not set | text |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Basic usage and Simulation pages of the documentation: https://reframed.readthedocs.io/en/latest/simulation.html

```python
from reframed import load_cbmodel, FBA, FVA

model = load_cbmodel("e_coli_core.xml", flavor="fbc2")
model.summary()

sol = FBA(model)
sol.show_values(pattern="R_EX", sort=True)

# a temporary constraint: limit oxygen uptake
sol = FBA(model, constraints={"R_EX_o2_e": (-15, 0)})
```

The model file is the E. coli core model (from the BiGG collection), which the ReFramed repository carries as a test file (`tests/data/e_coli_core.xml.gz`). The recipe's helper unpacks it and takes glucose and oxygen uptake limits as arguments.

The documentation shows the FBA call printing `Objective: 0.8739215069684306` and `Status: Optimal` for this model. That number comes from the documentation, with the glucose uptake at -10 as set in the model file.

## Reading the output

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

The helper writes `fluxes.csv` for FBA or pFBA, with one row per reaction and the flux in mmol per gram dry weight per hour. For FVA it writes `flux_ranges.csv` with the minimum and maximum flux of every reaction. The first line of `run_log.txt` gives the solver status and the objective value.

Read the results this way:

- The objective is the flux through the biomass reaction `R_BIOMASS_Ecoli_core_w_GAM`, which is the predicted growth rate in 1/h.
- Exchange reactions start with `R_EX_`. A negative flux is uptake and a positive flux is secretion. In the documentation's output oxygen and glucose are negative and CO2 is positive.
- With pFBA the total flux is also minimised, so the table has fewer unneeded loops than plain FBA.
- In FVA a wide range means the reaction is poorly determined by the objective.

## Pitfalls

- **No solver, no result.** If no solver loads, the package fails when you ask for a solution. Check that `pyscipopt` imports.
- **Sign convention.** An exchange reaction runs out of the cell when positive. Uptake limits are lower bounds, for example `(-10, 1000)`.
- **Reaction identifiers keep the `R_` prefix.** `R_PGI` is a reaction and `M_g6p_c` is a metabolite. The BiGG identifiers in `cobrapy` models drop the prefix.
- **Model flavour.** Use `flavor="fbc2"` for SBML with the FBC version 2 package, which most current models use, and `"cobra"` for the older form.
- **Unmaintained.** The author recommends fluxbound for new projects.

## Further reading

- Source and README: https://github.com/cdanielmachado/reframed
- Documentation: https://reframed.readthedocs.io
- Bioconda package: https://anaconda.org/bioconda/reframed
- Successor: https://github.com/cdanielmachado/fluxbound
- No journal paper is listed in the README. Cite the repository.

---

Cite: Machado D (2025). ReFramed: metabolic modeling package (software). https://github.com/cdanielmachado/reframed

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/reframed).
