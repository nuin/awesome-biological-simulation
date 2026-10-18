# treesimulator

> Simulate a rooted phylogenetic tree under an epidemiological birth-death model with sampling.

Licence: GPL-3.0-only · [Source code](https://github.com/evolbioinfo/treesimulator)

## What it simulates

treesimulator generates a rooted phylogenetic tree from an epidemiological birth-death model. Infected hosts transmit at rate la (the birth rate) and are removed (recover or isolate) at rate psi. A removed host is sampled with probability p. Sampled hosts become the tips of the tree. The README defines the reproduction number as R = la/psi.

The recipe uses the basic BD model: one infectious state, constant rates. Input is the three rates, a target number of tips and a seed. Output is a Newick tree, `tree.nwk`, and a CSV of the true and observed parameters.

Key assumptions: rates are constant over the run, hosts are exchangeable, and the process stops at the requested number of sampled tips, a time limit `--T`, or extinction, whichever comes first.

## When to use it

Use it to make test trees for phylodynamic methods, to check how an estimator recovers R and the infectious period, or to see what tree shape a given R and sampling probability produce.

The README lists richer models that this recipe does not use: BD with contact tracing, BDEI (an exposed state), BDSS (superspreaders), BDEISS and user-defined multi-type models.

Alternatives on biosimhub:

- [epydemix](epydemix.md) fits better when you want SIR or SEIR compartment counts over time, with 5/50/95 percent bands over many runs.
- [msprime](msprime.md) fits better for coalescent genealogies of a fixed population.

## Install it yourself

treesimulator 0.2.30 is on PyPI and on bioconda (a noarch package).

```
pip install treesimulator==0.2.30
# or
conda create -n treesim -c conda-forge -c bioconda treesimulator=0.2.30
```

PyPI lists these dependencies: six, ete3, numpy, scipy, sympy and lifelines. The versions come from the anaconda.org and PyPI indexes.

The README also offers a Docker image (`evolbioinfo/treesimulator`) and Apptainer. The command is:

```
generate_bd --max_tips 200 --la 0.5 --psi 0.25 --p 0.5 --nwk tree.nwk --log params.csv -s 1
```

`generate_bd --help` lists all options, including `--T`, skyline intervals (`--skyline_times`, `--skyline_sampled`) and contact tracing (`--upsilon`, `--X_C`, `--X_p`).

## Run the tested example

This recipe builds treesimulator in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 3.7 s.

1. Download [treesimulator-recipe.tar.gz](https://biosimhub.pages.dev/guides/treesimulator/treesimulator-recipe.tar.gz) (Dockerfile, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf treesimulator-recipe.tar.gz
   cd treesimulator
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/treesimulator:0.2.30 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/treesimulator:0.2.30 generate_bd --max_tips 200 --la 0.5 --psi 0.25 \
    --p 0.5 --nwk tree.nwk --log params.csv -s 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `params.csv` | 146 B |
| `run_log.txt` | 0 B |
| `tree.nwk` | 10.2 KB |

<details><summary>First lines of <code>params.csv</code></summary>

```
R,R_I,d,d_I,la_II,p_I,psi_I,t_I,R,d,tips,end_time,R_observed,d_observed,p_observed
2,2,4,4,0.5,0.5,0.25,4,2,4,200,22.391,2.03226,3.86615,0.496278
```

</details>

<details><summary>First lines of <code>tree.nwk</code></summary>

```
(((((12:0.363828[&&NHX:state=I],8:1.08105[&&NHX:state=I]):0.867897[&&NHX:state=I],((30:2.72874[&&NHX:state=I],(48:1.82738[&&NHX:state=I],(5:2.66337[&&NHX:state=I],(53:2.13442[&&NHX:state=I],(334:2.418
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-s` | Seed (The epidemic can die out before reaching the requested tips; try another seed.) | 1 | 1 to 2147483647 |
| `--max_tips` | Number of sampled tips | 200 | 3 to 20000 |
| `--la` | Transmission (birth) rate | 0.5 | 0.001 to 100 |
| `--psi` | Sampling (removal) rate | 0.25 | 0.001 to 100 |
| `--p` | Probability of becoming removed after sampling | 0.5 | 0 to 1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example calls `generate_bd` directly. It took 3.7 seconds.

`params.csv` has one data row: `2,2,4,4,0.5,0.5,0.25,4,2,4,200,22.391,2.03226,3.86615,0.496278`. The first columns echo the input model: R = 2 (0.5/0.25), la 0.5, p 0.5, psi 0.25 and a value d = 4, which equals 1/psi. The last columns report the tree: 200 tips, an end time of 22.391 and the observed values R 2.03, d 3.87 and p 0.496. Observed values come from the simulated tree, so they scatter around the inputs.

`tree.nwk` (10,461 bytes) has 200 tips. The deepest root-to-tip path is 22.391, which equals the end time. Each branch carries an NHX annotation, `[&&NHX:state=I]`, giving the infectious state. Tip names are host numbers and do not run from 1 to 200 (the file starts with tips 12 and 8, and a tip named 334 appears).

`run_log.txt` is empty. `generate_bd` writes its log to standard error, which prints the model parameters and the final `Generated a tree with 200 sampled tips over time T=...` line.

## Your own runs

- `--la 1.0` (R = 4): 200 tips in 9.26 time units instead of 22.39. Observed R is 4.19.
- `--p 1.0` (every removed host sampled): 200 tips in 19.42 time units, and observed p is 1.
- `-s 2` with the example settings: 200 tips in 14.20 time units, observed R 2.14. Seed alone moves the end time from 22.4 to 14.2.
- `--la 0.2` (R = 0.8): the epidemic died out. The run exits with status 0 and writes a tree of 10 tips over 14.99 time units instead of 200 tips.

## Pitfalls

- With R below 1 the epidemic dies out and you get fewer tips than `--max_tips` without an error. Check the `tips` column in `params.csv`.
- With R near 1 many seeds die early. A run can end before the requested tips. Try another seed.
- Rates and tree branch lengths share one time unit. Whether it is days or years depends on how you read la and psi.
- `--la`, `--psi` and `--p` accept lists, one value per skyline interval. A single value is a constant model.
- The log goes to stderr, so a redirect of standard output alone leaves an empty file.

## Further reading

- Source and README: https://github.com/evolbioinfo/treesimulator
- Voznica J, Zhukova A, et al. Accounting for contact tracing in epidemiological birth-death models. PLoS Comput Biol. https://doi.org/10.1371/journal.pcbi.1012461

---

Cite: Zhukova A, Gascuel O (2025). Accounting for contact tracing in epidemiological birth-death models. PLoS Comput Biol. doi:10.1371/journal.pcbi.1012461

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/treesimulator).
