# COBRApy

> Flux balance analysis and flux variability analysis of a genome-scale metabolic model given as SBML.

Licence: GPL-2.0-or-later OR LGPL-2.0-or-later · [Source code](https://github.com/opencobra/cobrapy)

## What it simulates

COBRApy runs constraint-based analysis of genome-scale metabolic models. A model is a table of reactions, metabolites and genes. Each reaction has a flux, bounded above and below. At steady state the fluxes must balance every internal metabolite. The model describes a space of feasible flux states, and COBRApy searches that space.

The two core methods are:

- **Flux balance analysis (FBA).** Maximise one flux, usually biomass production, subject to the bounds. `model.optimize()` returns a solution with the objective value, the solver status and one flux per reaction.
- **Flux variability analysis (FVA).** FBA often has many equally good solutions. FVA reports the minimum and maximum of every flux while the objective stays at or above a chosen fraction of its optimum.

COBRApy also covers parsimonious FBA, geometric FBA, single and double deletions, production envelopes, flux sampling, gap filling and growth media. There is no time dimension and no kinetics: fluxes are rates at steady state.

## When to use it

Use COBRApy to ask what a metabolic network can do. Typical questions are the growth rate on a given medium, which genes are essential, and how oxygen or glucose limits growth.

- [COPASI](copasi.md) fits when you have kinetic rate laws and want time courses or parameter estimation.
- [GillesPy2](gillespy2.md) fits stochastic simulation of small reaction networks with few molecules.
- Catalyst.jl, in Julia, handles reaction networks as ODE, SDE or jump systems when you need dynamics.

## Install

The package is on PyPI and on conda-forge. The current release is 0.32.1. The conda-forge package is noarch, and the PyPI page lists the licence as `LGPL-2.0-or-later OR GPL-2.0-or-later`.

```bash
micromamba create -n cobra -c conda-forge cobra=0.32.1
# or
pip install cobra==0.32.1
```

The COBRApy README recommends pip inside a virtual environment. The GLPK solver is installed as swiglpk. CPLEX and Gurobi are optional and need their own licences.

## Run the tested example

This recipe builds COBRApy in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.6 s.

1. Download [cobrapy-recipe.tar.gz](https://biosimhub.pages.dev/guides/cobrapy/cobrapy-recipe.tar.gz) (Dockerfile, run_cobrapy.py, example model.xml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf cobrapy-recipe.tar.gz
   cd cobrapy
   sh run.sh
   ```

![Terminal recording of the COBRApy example run](https://biosimhub.pages.dev/media/cobrapy/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/cobrapy:0.32.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/cobrapy:0.32.1 python /opt/run_cobrapy.py /work/in/model.xml \
    --glucose 10 --oxygen 1000 --fraction 0.9 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `fba_fluxes.csv` | 1.7 KB |
| `fva.csv` | 3.2 KB |
| `run_log.txt` | 103 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/cobrapy/result-dark.png"><img src="https://biosimhub.pages.dev/media/cobrapy/result.png" alt="Plot of the COBRApy example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>fba_fluxes.csv</code></summary>

```
reaction,flux
ACALD,0.0
ACALDt,0.0
ACKr,1.8850036560801405e-15
ACONTa,6.007249575350339
ACONTb,6.00724957535034
ACt2r,1.8850036560801405e-15
ADK1,0.0
AKGDH,5.064375661482102
AKGt2r,0.0
ALCD2x,0.0
ATPM,8.39
```

</details>

<details><summary>First lines of <code>fva.csv</code></summary>

```
reaction,minimum,maximum
ACALD,-2.5423703703703615,0.0
ACALDt,-2.542370370370359,0.0
ACKr,-3.813555555555534,0.0
ACONTa,0.8485865224814145,8.894520101187696
ACONTb,0.8485865224814148,8.8945201011877
ACt2r,-3.8135555555555483,0.0
ADK1,0.0,17.161000000000023
AKGDH,0.0,8.045933578706284
AKGt2r,-1.4300833333333312,0.0
ALCD2x,-2.214322580645154,0.0
ATPM,8.39,25.550999999999984
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
model e_coli_core: 95 reactions, 72 metabolites, 137 genes
status optimal, growth rate 0.8739 per hour
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--glucose` | Maximum glucose uptake (mmol/gDW/h) | 10 | 0 to 1000 |
| `--oxygen` | Maximum oxygen uptake (mmol/gDW/h; 0 = anaerobic) | 1000 | 0 to 1000 |
| `--fraction` | FVA fraction of the optimum | 0.9 | 0 to 1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Getting Started and Simulating with FBA pages of the COBRApy documentation: https://cobrapy.readthedocs.io/en/latest/getting_started.html and https://cobrapy.readthedocs.io/en/latest/simulating.html.

```python
from cobra.io import load_model
from cobra.flux_analysis import flux_variability_analysis

model = load_model("textbook")
solution = model.optimize()
print(solution.objective_value)
fva = flux_variability_analysis(model, fraction_of_optimum=0.9)
```

`load_model("textbook")` loads the bundled E. coli core model. The documentation shows 95 reactions, 72 metabolites and 137 genes for it, and an FBA objective value of 0.8739215069684307. The recipe's script `run_cobrapy.py` reads an SBML file instead, sets the glucose and oxygen uptake bounds, and writes the FBA fluxes and the FVA ranges as CSV files. The example input is the same textbook model as SBML.

The numbers above come from the COBRApy documentation. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

- `run_log.txt` has the model size and the solver status, then the growth rate in 1/h. The growth rate is the optimal value of the biomass reaction.
- `fba_fluxes.csv` has one row per reaction with its flux in mmol per gram dry weight per hour. A negative flux runs against the reaction's written direction. For exchange reactions, a negative flux is uptake.
- `fva.csv` has the columns `reaction`, `minimum` and `maximum`. A reaction with equal minimum and maximum is fixed by the optimum. A wide range means the network has alternative routes.

In the documentation's glucose setup, the lower bound of `EX_glc__D_e` is -10.0, meaning at most 10 mmol/gDW/h of glucose can be taken up. The recipe's `--glucose` option sets that bound. Setting `--oxygen 0` removes oxygen and gives anaerobic growth.

The FVA table in the documentation lists values such as -2.6e-14. These are numerically zero.

## Pitfalls

- **FBA fluxes are not unique.** Two solvers can return different flux vectors with the same growth rate. Use FVA or parsimonious FBA before reading a single flux as a prediction.
- **Reaction IDs must match.** The recipe script needs `EX_glc__D_e` and `EX_o2_e`. Models from other sources may name exchange reactions differently, so edit the script.
- **Bounds define the medium.** The bounds of the exchange reactions are the medium. A model with unlimited uptake of everything will grow at an unrealistic rate.
- **Infeasible models raise an error.** If no flux state satisfies the bounds, `optimize()` raises an error. Check the bounds first.
- **Status matters.** Read `solution.status`. Only "optimal" means the fluxes are an optimum.
- **Units are per gram dry weight.** The growth rate is in 1/h only if the biomass reaction is scaled to 1 gDW.

## Further reading

- Documentation: https://cobrapy.readthedocs.io/en/latest/
- Solvers: https://cobrapy.readthedocs.io/en/latest/solvers.html
- Source: https://github.com/opencobra/cobrapy
- Paper: Ebrahim A, Lerman JA, Palsson BO, Hyduke DR (2013). COBRApy: COnstraints-Based Reconstruction and Analysis for Python. BMC Systems Biology 7:74. https://doi.org/10.1186/1752-0509-7-74

---

Cite: Ebrahim A, Lerman JA, Palsson BO, Hyduke DR (2013). COBRApy: COnstraints-Based Reconstruction and Analysis for Python. BMC Syst Biol 7:74. doi:10.1186/1752-0509-7-74

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cobrapy).
