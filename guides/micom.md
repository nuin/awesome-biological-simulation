# MICOM

> Community flux balance with the cooperative trade-off, on a bundled community of E. coli core models.

Licence: Apache-2.0 · [Source code](https://github.com/micom-dev/micom)

## What it simulates

MICOM models a microbial community as one metabolic network. Each member is a genome-scale (or smaller) metabolic model in the cobrapy format. MICOM joins them through a shared medium and adds a community biomass reaction. Abundances weight each member's biomass.

Plain flux balance analysis (FBA) maximises growth of the whole community. It tends to let a few members grow fast and starves the rest. MICOM adds the cooperative trade-off, a two-step optimisation. Step one finds the maximum community growth rate. Step two requires community growth of at least a chosen fraction of that maximum, then minimises the sum of squared individual growth rates, which spreads growth over the members. The fraction is the one free setting.

Key assumptions: steady state, a well-mixed medium, fixed relative abundances, and growth as the shared goal. There is no time dimension and no spatial structure.

## When to use it

- You have species abundances (for example from 16S or metagenomes) and want growth rates and exchange fluxes per taxon.
- You want to see which metabolites a community imports and exports, and who feeds whom.
- You want to test taxa knock-outs or a change of medium on community growth.

Alternatives:

- [COPASI](copasi.md) and [Tellurium](tellurium.md) simulate kinetic models over time. They need rate laws, which genome-scale models lack.
- The COBRA Toolbox and cobrapy (MICOM's base) cover single-organism FBA. See [COBRA Toolbox](cobra-toolbox.md) for the MATLAB route.
- [RAVEN](raven-toolbox.md) builds the genome-scale models that MICOM can then combine.

## Install

The current release is MICOM 0.39.1 on PyPI (Apache-2.0, Python 3.10 or newer). Bioconda holds an older build, 0.37.1.

```bash
python3 -m venv micom-env && . micom-env/bin/activate
pip install micom==0.39.1
```

The project's install notebook says the default solver is a hybrid of HiGHS and OSQP. Both are installed with MICOM, so no licence is needed for the cooperative trade-off. CPLEX and Gurobi are optional and faster. The recipe on this page installs `micom==0.39.1` from PyPI into a Python 3.12 image.

## A first run

Adapted from the project's [growth rates and fluxes notebook](https://github.com/micom-dev/micom/blob/main/docs/source/growth_fluxes.ipynb). The package ships a test community of four copies of the E. coli core model (95 reactions, 72 metabolites each).

```python
import numpy as np
from micom import Community, data

tax = data.test_taxonomy()            # 4 E. coli core models
com = Community(tax)

fba = com.optimize()                  # plain FBA
print(fba.members)                    # growth rate per member

sol = com.cooperative_tradeoff(fraction=0.5)
print(sol.members.growth_rate)

sweep = com.cooperative_tradeoff(fraction=np.arange(0.1, 1.01, 0.1))
```

Add `fluxes=True, pfba=True` to get parsimonious fluxes per member.

## Run the tested example

This recipe builds MICOM in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.2 s.

1. Download [micom-recipe.tar.gz](https://biosimhub.pages.dev/guides/micom/micom-recipe.tar.gz) (Dockerfile, run_micom.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf micom-recipe.tar.gz
   cd micom
   sh run.sh
   ```

![Terminal recording of the MICOM example run](https://biosimhub.pages.dev/media/micom/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/micom:0.39.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/micom:0.39.1 python /opt/run_micom.py --taxa 4 --fraction 0.5 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `members.csv` | 165 B |
| `run_log.txt` | 85 B |
| `tradeoff_sweep.csv` | 171 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/micom/result-dark.png"><img src="https://biosimhub.pages.dev/media/micom/result.png" alt="Plot of the MICOM example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>members.csv</code></summary>

```
taxon,abundance,growth_rate
Escherichia_coli_1,0.25,0.436961
Escherichia_coli_2,0.25,0.436961
Escherichia_coli_3,0.25,0.436961
Escherichia_coli_4,0.25,0.436961
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
taxa=4 fraction=0.5 fba_community_growth=0.873922 tradeoff_community_growth=0.436961
```

</details>

<details><summary>First lines of <code>tradeoff_sweep.csv</code></summary>

```
fraction,community_growth_rate
1.0,0.873921
0.9,0.78653
0.8,0.699137
0.7,0.611746
0.6,0.524353
0.5,0.43696
0.4,0.349569
0.3,0.262177
0.2,0.174785
0.1,0.0873934
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--taxa` | Number of E. coli core models in the community | 4 | 1 to 12 |
| `--fraction` | Cooperative trade-off fraction | 0.5 | 0.05 to 1 |
| `--fluxes` | Also write parsimonious fluxes | False | bool |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- **`members`.** One row per member plus a `medium` row. Columns are abundance, growth rate, reactions and metabolites.
- **Community growth rate.** The value printed with the solution object. It equals the weighted sum of member growth rates.
- **`fluxes`.** One row per compartment (each member and the medium), one column per reaction.
- **Sweep.** A table with one row per fraction and one solution per row.

Numbers from the upstream notebook, for the four-member E. coli test community: plain FBA gave unequal member growth rates of 1.53, 0.65, 0.24 and 1.07 per hour. The cooperative trade-off at fraction 1.0 gave all four members the same rate, with community growth 0.874. Fractions 0.9, 0.8 and 0.5 gave 0.787, 0.699 and 0.437. These are the notebook's values. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

The recipe writes `members.csv` (taxon, abundance, growth rate), `tradeoff_sweep.csv` (fraction against community growth) and, if requested, `fluxes.csv`.

## Pitfalls

- **The trade-off needs a quadratic solver.** Without OSQP/HiGHS, cplex or gurobi, MICOM falls back to GLPK and warns that much functionality is unavailable.
- **Plain FBA gives lopsided growth.** The notebook shows four identical models growing at four rates. Use the trade-off for per-taxon rates.
- **Pick the fraction on purpose.** The docs report that a fraction at or below 0.5 gave realistic growth rates on a set of 189 gut microbiomes. For your data, sweep it.
- **Build once, then pickle.** Building a large community is slow. `com.to_pickle(...)` and `load_pickle(...)` reload it quickly.
- **A model file is needed per taxon.** The `file` column of the taxonomy table must point at a model. The AGORA table inside the package lists names only; the model files are a separate download.

## Further reading

- Repository: https://github.com/micom-dev/micom
- Documentation notebooks: https://github.com/micom-dev/micom/tree/main/docs/source
- Diener C, Gibbons SM, Resendis-Antonio O (2020). MICOM: metagenome-scale modeling to infer metabolic interactions in the gut microbiota. mSystems 5:e00606-19. https://doi.org/10.1128/mSystems.00606-19

---

Cite: Diener C, Gibbons SM, Resendis-Antonio O (2020). MICOM: metagenome-scale modeling to infer metabolic interactions in the gut microbiota. mSystems 5:e00606-19. doi:10.1128/mSystems.00606-19

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/micom).
