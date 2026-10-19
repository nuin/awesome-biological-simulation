# AlphaSimR

> Simulate a breeding program as repeated selection and crossing of a founder population with a quantitative trait, and record genetic gain per generation.

Licence: MIT · [Source code](https://github.com/gaynorr/AlphaSimR)

## What it simulates

AlphaSimR simulates plant and animal breeding programs in R, down to the DNA sequence of every individual. You create founder haplotypes, define one or more traits controlled by QTL, then script selection and crossing with R functions. Each step returns a population object that you pass to the next.

The package follows four steps:

1. **Founder haplotypes.** `quickHaplo()` samples 0/1 alleles at random, which is fast but not realistic. `runMacs()` runs the MaCS coalescent simulator, bundled with the package, under a named or custom population history. `newMapPop()` imports your own haplotypes.
2. **Simulation parameters.** `SimParam$new(founderPop)` holds the genome map and the traits. `SP$addTraitA()` adds a trait with additive effects. Other trait types add dominance, epistasis or genotype-by-environment effects.
3. **The breeding program.** `newPop()`, `selectInd()`, `randCross()` and `selectCross()` model the selection and mating of each cycle.
4. **Results.** Functions such as `meanG()` and `varG()` return genetic means and variances. You must ask for the data you want to keep.

Selection can use true genetic values, as in the example below, or other criteria that the `use` argument offers.

## When to use it

Use AlphaSimR to compare breeding strategies, test genomic selection schemes or estimate expected genetic gain before a real program starts.

- [SLiM](slim.md) models selection on specific mutations in natural populations. AlphaSimR models quantitative traits under artificial selection.
- [simuPOP](simupop.md) is a Python framework for forward simulation with user-defined mating schemes.
- [msprime](msprime.md) generates realistic founder sequences. AlphaSimR can import haplotypes through `newMapPop()`.

## Install

AlphaSimR is on CRAN. The current release is 2.1.0 (8 November 2025). There is no conda-forge or bioconda package (checked on anaconda.org). The licence is MIT.

```r
install.packages("AlphaSimR")
```

The development version is on the `devel` branch:

```r
devtools::install_github(repo = "gaynorr/AlphaSimR@devel")
```

The package contains compiled code, so a C++ compiler is needed unless your platform provides a binary package. The R dependencies are Rcpp, Rdpack, methods and R6.

## Run the tested example

This recipe builds AlphaSimR in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.4 s.

1. Download [alphasimr-recipe.tar.gz](https://biosimhub.pages.dev/guides/alphasimr/alphasimr-recipe.tar.gz) (Dockerfile, run_alphasimr.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf alphasimr-recipe.tar.gz
   cd alphasimr
   sh run.sh
   ```

![Terminal recording of the AlphaSimR example run](https://biosimhub.pages.dev/media/alphasimr/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/alphasimr:2.1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/alphasimr:2.1.0 Rscript /opt/run_alphasimr.R 1000 10 1000 1000 20 25 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `genetic_gain.csv` | 804 B |
| `run_log.txt` | 65 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/alphasimr/result-dark.png"><img src="https://biosimhub.pages.dev/media/alphasimr/result.png" alt="Plot of the AlphaSimR example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>genetic_gain.csv</code></summary>

```
"generation","mean_gv","Trait1"
0,-9.62667445758569e-17,1
1,0.97818217978672,0.835237746957572
2,1.90338424736535,0.743812709946253
3,2.83179518434466,0.776832749865599
4,3.72460699598159,0.75641428941013
5,4.73610050005007,0.765383123403302
6,5.66327162230051,0.732541205199203
7,6.48496107137164,0.72166069757397
8,7.44167916504207,0.710853261311989
9,8.38519384875796,0.649880867534466
10,9.21502284153217,0.629675045266835
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
seed 42: mean genetic value -0.000 to 17.075 over 20 generations
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `n_ind` | Individuals per generation | 1000 | 20 to 5000 |
| `n_chr` | Chromosomes | 10 | 1 to 30 |
| `seg_sites` | Segregating sites per chromosome | 1000 | 100 to 5000 |
| `qtl` | QTL per chromosome | 1000 | 10 to 2000 |
| `generations` | Generations of selection | 20 | 1 to 50 |
| `n_male` | Males selected as parents | 25 | 2 to 500 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Introduction to AlphaSimR vignette: https://cran.r-project.org/web/packages/AlphaSimR/vignettes/AlphaSimR.html. The example is a simple animal breeding program with 20 generations of selection on one polygenic trait. Each generation has 1000 animals, 500 of each sex. The best 25 males are chosen by genetic value and mated to the females.

```r
library(AlphaSimR)
founderPop = quickHaplo(nInd=1000, nChr=10, segSites=1000)
SP = SimParam$new(founderPop)
SP$addTraitA(nQtlPerChr=1000)
SP$setSexes("yes_sys")
pop = newPop(founderPop)
genMean = meanG(pop)
for(generation in 1:20){
  pop = selectCross(pop=pop, nFemale=500, nMale=25, use="gv", nCrosses=1000)
  genMean = c(genMean, meanG(pop))
}
plot(0:20, genMean, xlab="Generation", ylab="Mean Genetic Value", type="l")
```

The trait has 10,000 QTL, 1,000 on each of 10 chromosome groups. The recipe's script `run_alphasimr.R` runs this program with parameters for the population size, number of QTL, number of generations and number of selected males, and writes a CSV file. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

`genetic_gain.csv` has one row per generation, starting at generation 0:

- `generation` is the cycle number. Generation 0 is the founder population.
- `mean_gv` is the mean genetic value of the population, from `meanG()`.
- `var_gv` is the genetic variance, from `varG()`.

The mean genetic value is the vignette's result. It is plotted against generation as a line, which is the genetic gain per generation. With selection on genetic value, the mean should rise with generation. The variance usually falls as selection removes variation and the number of parents is small. The slope of the mean and the fall of the variance both depend on the number of parents, the number of QTL and the founder diversity.

`run_log.txt` has one line with the seed and the first and last mean genetic value.

## Pitfalls

- **`quickHaplo()` is for prototyping.** It gives linkage and Hardy-Weinberg equilibrium with allele frequency 0.5 at every site. The vignette recommends `runMacs()` for realistic haplotypes.
- **Name the parameter object `SP`.** Many functions take a `simParam` argument that defaults to `NULL`, and then they look for an object called `SP` in your global environment.
- **Data is not kept unless you save it.** Populations are overwritten in the loop. Store the values you need, as the vignette does with `genMean`.
- **Sex setting matters.** `SP$setSexes("yes_sys")` assigns sexes in strict alternation, which gives equal numbers of males and females.
- **Seeds.** The recipe calls `set.seed()` before the founder step. The vignette does not discuss seeding, so run twice and compare before you rely on exact repeats.
- **Threads.** The vignette sets `SP$nThreads = 1L`. The recipe does the same, to stay within one CPU.

## Further reading

- Introduction vignette: https://cran.r-project.org/web/packages/AlphaSimR/vignettes/AlphaSimR.html
- Package site: https://gaynorr.github.io/AlphaSimR/
- Source: https://github.com/gaynorr/AlphaSimR
- Paper: Gaynor RC, Gorjanc G, Hickey JM (2021). AlphaSimR: an R package for breeding program simulations. G3 11:jkaa017. https://doi.org/10.1093/g3journal/jkaa017

---

Cite: Gaynor RC, Gorjanc G, Hickey JM (2021). AlphaSimR: an R package for breeding program simulations. G3 11:jkaa017. doi:10.1093/g3journal/jkaa017

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/alphasimr).
