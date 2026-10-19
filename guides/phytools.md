# phytools

> Simulate a birth-death phylogeny with a fixed number of living tips and a continuous trait evolving on it by Brownian motion.

Licence: GPL-2.0-or-later · [Source code](https://github.com/liamrevell/phytools)

## What it simulates

phytools is an R package for phylogenetic comparative biology. Its simulation side builds trees and evolves characters on them. The main functions are:

- **`pbtree`:** stochastic birth-death trees, with pure-birth (Yule) trees as the case with no extinction. You stop the process at a number of species `n`, a time `t`, or both.
- **`fastBM`:** continuous traits by Brownian motion, with options for a trend (`mu`), bounds, and an Ornstein-Uhlenbeck process.
- **`sim.history`:** discrete characters on a tree under a rate matrix Q, with the full history on the branches if you want it.
- **`sim.rates`, `sim.corrs`, `sim.ratebystate`:** traits with several rate regimes, several correlated traits, or a rate that depends on the state of another character.
- **`genSeq`:** DNA alignments on a tree under a model.

Characters evolve independently on the branches of a fixed tree. phytools does not model selection acting on the tree itself.

## When to use it

Use phytools when the question is about trees and traits: how much a method loses to tree shape, whether a test keeps its error rate under a known evolutionary model, or what a trait distribution looks like at the tips after a given history.

Alternatives:

- [Pyvolve](pyvolve.md) simulates sequences along a tree you supply, including codon models.
- [TreeSimulator](treesimulator.md) simulates trees from epidemic birth-death models.
- [PAML evolver](paml-evolver.md) simulates nucleotide, codon and protein alignments on a given tree.

## Install

phytools is a CRAN package. The current CRAN release is 2.5-2 (checked on the CRAN package database). It is also on conda-forge as `r-phytools` 2.5_2, as a noarch package that needs R 4.3 or newer:

```bash
conda create -n phytools -c conda-forge r-phytools=2.5_2
conda activate phytools
```

From inside R:

```r
install.packages("phytools")
```

The DESCRIPTION file gives the licence as GPL (version 2 or later). The development version on GitHub is newer than CRAN, so take CRAN or conda-forge for a fixed result. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## A first run

Adapted from the `pbtree` and `fastBM` entries of the [phytools reference manual](https://cran.r-project.org/web/packages/phytools/refman/phytools.html). The recipe wraps them in one script, `run_phytools.R`:

```r
library(phytools)
set.seed(42)
tree <- pbtree(b = 1, d = 0.3, n = 30, extant.only = TRUE)
x <- fastBM(tree, sig2 = 1)
write.tree(tree, file = "tree.nwk")
write.csv(data.frame(taxon = names(x), trait = as.numeric(x)),
          file = "traits.csv", row.names = FALSE)
```

`b` is the birth rate, `d` the death rate and `n` the number of species at which to stop. With `extant.only = TRUE` the extinct lineages are dropped from the returned tree. `fastBM` returns a named vector of tip values.

## Run the tested example

This recipe builds phytools in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.1 s.

1. Download [phytools-recipe.tar.gz](https://biosimhub.pages.dev/guides/phytools/phytools-recipe.tar.gz) (Dockerfile, run_phytools.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf phytools-recipe.tar.gz
   cd phytools
   sh run.sh
   ```

![Terminal recording of the phytools example run](https://biosimhub.pages.dev/media/phytools/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/phytools:2.5-2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/phytools:2.5-2 Rscript /opt/run_phytools.R --ntaxa 30 --birth 1 \
    --death 0.3 --sig2 1 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 88 B |
| `traits.csv` | 726 B |
| `tree.nwk` | 925 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/phytools/result-dark.png"><img src="https://biosimhub.pages.dev/media/phytools/result.png" alt="Plot of the phytools example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
tips=30 height=1.9094 total_length=25.6043 seed=42
trait mean=-0.3095 var=1.8787 sig2=1
```

</details>

<details><summary>First lines of <code>traits.csv</code></summary>

```
"taxon","trait"
"t22",-1.20560867229358
"t23",-0.878465995676816
"t10",-0.510464202601183
"t11",0.468450631616157
"t4",1.27236083950095
"t5",0.386870332119323
"t2",-0.626342433542579
"t19",-0.291941707780238
"t6",0.676568969651144
"t7",-2.37557026372005
"t8",0.582470663883797
```

</details>

<details><summary>First lines of <code>tree.nwk</code></summary>

```
((((t22:0.2119434984,t23:0.2119434984):0.9210539291,((t10:0.4534046287,t11:0.4534046287):0.6687129968,(t4:1.066311563,t5:1.066311563):0.05580606282):0.01087980198):0.3980182205,t2:1.531015648):0.37841
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--ntaxa` | Living tips | 30 | 3 to 500 |
| `--birth` | Birth (speciation) rate | 1 | 0.1 to 10 |
| `--death` | Death (extinction) rate (Must be below the birth rate) | 0.3 | 0 to 9.9 |
| `--sig2` | Brownian rate (sigma squared) | 1 | 0.001 to 100 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `tree.nwk`: the tree in Newick format, with branch lengths in time units. Tips are named `t1`, `t2` and so on.
- `traits.csv`: one row per tip, with the taxon name and its simulated trait value.
- `run_log.txt`: the number of tips, the tree height, the total branch length, and the mean and variance of the trait.

The expected variance of the tip values under Brownian motion grows with sigma squared times the time from the root. Closely related tips have similar values, because they share most of their path from the root.

## Pitfalls

- **Death must stay below birth.** The recipe stops with an error otherwise.
- **A tree can go extinct.** The manual notes that with a death rate above 0 and `n` as the stopping rule, a run sometimes returns fewer than `n` living tips. The recipe draws again until it has `n`.
- **`scale` changes the time unit.** The manual says `scale` rescales the tree to have total length `scale`, so the birth and death rates then only set the shape.
- **Without `extant.only` extinct tips stay in the tree.** The default is `FALSE`.
- **Set the seed before the tree.** Both `pbtree` and `fastBM` draw from R's random numbers, so one `set.seed` call before the first fixes both.
- **`fastBM` takes `sig2`, not a standard deviation.** The variance of the change along a branch is `sig2` times the branch length.
- **Package versions move.** Output for a seed can change between phytools releases, so record the version.

## Further reading

- Project: https://github.com/liamrevell/phytools
- CRAN page: https://cran.r-project.org/package=phytools
- Reference manual: https://cran.r-project.org/web/packages/phytools/refman/phytools.html
- phytools blog: https://blog.phytools.org
- Revell LJ (2024). phytools 2.0: an updated R ecosystem for phylogenetic comparative methods (and other things). PeerJ 12:e16505. https://doi.org/10.7717/peerj.16505

---

Cite: Revell LJ (2024). phytools 2.0: an updated R ecosystem for phylogenetic comparative methods (and other things). PeerJ 12:e16505. doi:10.7717/peerj.16505

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/phytools).
