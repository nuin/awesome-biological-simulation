# slendr

> Define a population-split model in R, simulate it with msprime as a tree sequence, and compute diversity, divergence and F_ST.

Licence: MIT · [Source code](https://github.com/bodkan/slendr)

## What it simulates

slendr is an R package for population genetic simulation. You describe a model in R: populations, splits, size changes and gene flow, optionally on a real or abstract map. slendr compiles it and runs it with one of two engines that ship with the package, SLiM or msprime. Both write a tree sequence, which slendr reads back into R. You compute statistics from it with R functions that wrap tskit.

Models are declarative. You create populations with `population()`, change them with `resize()`, link them with `gene_flow()` and join everything with `compile_model()`. You schedule which individuals to record with `schedule_sampling()`. The spatial models use SLiM's continuous space, and the same code without a `map` gives a standard random-mating model.

Mutations are not simulated during the run. You add them to the tree sequence afterwards with `ts_mutate()`. Statistics include `ts_diversity()`, `ts_divergence()`, `ts_fst()`, `ts_tajima()` and f-statistics. slendr also lets you add custom SLiM code to a model for selection.

## When to use it

Use slendr when you work in R and want demographic models that read like a description, plus tree-sequence analysis in the same script. It is well suited to teaching and to models with spatial structure.

- [msprime](msprime.md) gives full control over the coalescent in Python, with no R layer.
- [stdpopsim](stdpopsim.md) offers published species models with rates and maps.
- [SLiM](slim.md) is the engine for forward simulations with arbitrary selection, and slendr hides its scripting.

## Install

slendr is on CRAN. The current release is 1.5.0 (26 June 2026). The licence is MIT. There is no conda-forge package (checked on anaconda.org).

```r
install.packages("slendr")
library(slendr)
setup_env()   # once, after each install or update
init_env()
```

`setup_env()` creates the Python environment that slendr needs (it includes msprime and tskit), using conda by default. The README says to run it in the console, not in your scripts. `init_env()` activates it at the start of a script. The SLiM engine needs SLiM installed separately; the CRAN page lists it as a system requirement. The msprime engine does not need SLiM.

## Run the tested example

This recipe builds slendr in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 17.9 s. slendr has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [slendr-recipe.tar.gz](https://biosimhub.pages.dev/guides/slendr/slendr-recipe.tar.gz) (Dockerfile, run_slendr.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf slendr-recipe.tar.gz
   cd slendr
   sh run.sh
   ```

![Terminal recording of the slendr example run](https://biosimhub.pages.dev/media/slendr/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/slendr:1.5.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/slendr:1.5.0 Rscript /opt/run_slendr.R 1000 1000 1000 500 1500 0 20 1000000 1e-08 1e-08 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `divergence.csv` | 50 B |
| `diversity.csv` | 67 B |
| `fst.csv` | 40 B |
| `run_log.txt` | 62 B |

<details><summary>First lines of <code>divergence.csv</code></summary>

```
"x","y","divergence"
"A","B",6.29487499999999e-05
```

</details>

<details><summary>First lines of <code>diversity.csv</code></summary>

```
"set","diversity"
"A",4.2351282051282e-05
"B",3.77551282051282e-05
```

</details>

<details><summary>First lines of <code>fst.csv</code></summary>

```
"x","y","Fst"
"A","B",0.222282624085116
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
seed 42: 40 sampled individuals in 2 populations, F_ST 0.2223
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `n_anc` | Ancestral population size | 1000 | 10 to 100000 |
| `n_a` | Population A size after the split | 1000 | 10 to 100000 |
| `n_b` | Population B size after the split | 1000 | 10 to 100000 |
| `split` | Split time (generation of the simulation) | 500 | 2 to 100000 |
| `sim_length` | Total generations simulated | 1500 | 10 to 200000 |
| `migration` | Gene flow rate A to B per generation (0 = none) | 0 | 0 to 0.5 |
| `samples` | Diploid individuals sampled per population | 20 | 2 to 500 |
| `seq_length` | Sequence length (bp) | 1000000 | 1000 to 50000000 |
| `recomb` | Recombination rate per bp per generation | 1e-08 | 0 to 0.0001 |
| `mu` | Mutation rate per bp per generation | 1e-08 | 0 to 0.0001 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the slendr README, https://github.com/bodkan/slendr, and the non-spatial models article, https://bodkan.net/slendr/articles/vignette-04-nonspatial-models.html. The README builds an out-of-Africa style model and runs it with msprime:

```r
library(slendr)
init_env()

anc_all <- population("ancestor_all", time = 700e3, N = 10000, remove = 640e3)
afr <- population("AFR", parent = anc_all, time = 650e3, N = 10000)
# ... more populations, then:
model <- compile_model(
  populations = list(anc_all, afr, anc_arch, nea, den, nonafr, eur, pap),
  gene_flow = gf,
  generation_time = 30
)
ts <- msprime(model, sequence_length = 100e6, recombination_rate = 1e-8)
```

The recipe's script `run_slendr.R` is simpler. An ancestral population splits into populations A and B, with optional gene flow from A to B. It samples diploid individuals from both at the end, adds mutations and computes diversity, divergence and F_ST. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

The recipe writes three CSV files, built from `ts_diversity()`, `ts_divergence()` and `ts_fst()` on the two sample sets.

- `diversity.csv` has one row per population with its nucleotide diversity (pi, per site).
- `divergence.csv` has one row for the pair A and B with the mean pairwise difference between them (per site).
- `fst.csv` has the pair and its F_ST. The tree sequence article describes the result as a simple data frame with the two sets and the value.
- `run_log.txt` has the seed, the number of sampled individuals and the F_ST.

Read them as you would read data from a coalescent simulator. Right after a split with no gene flow, divergence is close to diversity and F_ST is small. As time since the split grows, divergence rises above diversity and F_ST rises. Gene flow pulls F_ST down again.

For scale, the tree-sequence article gives an example with African, European and Neanderthal samples in which diversity is about 0.0004 per site for the two modern human groups, and about 0.00005 for the other sets. These values belong to that article's model, not to the recipe.

## Pitfalls

- **Run `setup_env()` once, not in every script.** The README says so. It downloads and installs Python packages.
- **Time direction.** A model with a `time` that grows runs forward and needs `simulation_length` in `compile_model()` (slendr 1.5.0 rejects the older `sim_length`). A model whose times shrink toward 0 runs backward in time, as in the README.
- **Mutations come after the run.** Without `ts_mutate()`, the tree sequence has no variants and the diversity statistics are zero.
- **Seeds.** Pass `random_seed` to `msprime()` and to `ts_mutate()`. Pass both to repeat a result.
- **Generation time.** Times are in your units. Set `generation_time` and `time_units` in `compile_model()` when your times are in years.
- **Backend choice.** The msprime engine is faster for neutral models. SLiM is needed for spatial models and for selection.

## Further reading

- Documentation: https://bodkan.net/slendr/
- Tree sequence analysis: https://bodkan.net/slendr/articles/vignette-05-tree-sequences.html
- Source: https://github.com/bodkan/slendr
- Paper: Petr M, Haller BC, Ralph PL, Racimo F (2023). slendr: a framework for spatio-temporal population genomic simulations on geographic landscapes. Peer Community Journal 3:e121. https://doi.org/10.24072/pcjournal.354

---

Cite: Petr M, Haller BC, Ralph PL, Racimo F (2023). slendr: a framework for spatio-temporal population genomic simulations on geographic landscapes. Peer Community J 3:e121. doi:10.24072/pcjournal.354

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/slendr).
