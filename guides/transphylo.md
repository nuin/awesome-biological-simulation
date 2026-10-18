# TransPhylo

> Simulate an outbreak with its phylogeny, then infer who infected whom and the reproduction number from the dated tree.

Licence: GPL-2.0-or-later · [Source code](https://github.com/xavierdidelot/TransPhylo)

## What it simulates

TransPhylo works on outbreaks where only some cases are sampled. It takes a dated phylogeny of pathogen samples and infers who infected whom, including unsampled hosts who passed the infection on. It colours each branch of the tree by host, so a colour change marks a transmission event. The README describes the same idea.

It also simulates the forward process: `simulateOutbreak` generates an outbreak with its transmission tree and the phylogeny of the sampled cases. The recipe simulates first, then infers from the simulated tree, so you can compare the answer with the truth.

The model assumes a branching process. The number of offspring per case is negative binomial with mean R, a gamma generation time, a gamma sampling delay, and a within-host coalescent with scale Ne x g. A fixed probability pi says whether an infected host is sampled. Time is in years.

## When to use it

- You have a dated tree from an outbreak, for example from a bacterial genome study, and want a transmission tree with uncertainty.
- You want R, the sampling probability and the within-host scale from the tree.
- You want to learn how much a tree of N samples can tell you, using simulated truth.

Use [treesimulator](treesimulator.md) to generate phylogenies from epidemiological models without inferring transmission. Use [odin](odin.md) when the question is the epidemic curve and no genomic data are involved.

## Install it yourself

TransPhylo is an R package under GPL-2.0 or later. The README gives `devtools::install_github('xavierdidelot/TransPhylo')`. The conda-forge index lists r-transphylo 1.4.5 for linux-64, osx-64 and win-64, and bioconda lists 1.4.0. Neither has a Linux arm64 build.

The recipe installs tag v.1.4.10 (commit 0759ed7) from source on Debian 12 with R 4.2.2. It needs a C++ compiler plus the Rcpp, ape and coda packages. The helper script `run_transphylo.R` calls `simulateOutbreak`, `extractPTree`, `inferTTree` and `computeMatWIW`.

## Run the tested example

This recipe builds TransPhylo in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 10.8 s.

1. Download [transphylo-recipe.tar.gz](https://biosimhub.pages.dev/guides/transphylo/transphylo-recipe.tar.gz) (Dockerfile, run_transphylo.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf transphylo-recipe.tar.gz
   cd transphylo
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/transphylo:1.4.10 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/transphylo:1.4.10 Rscript /opt/run_transphylo.R --r 3 --neg 0.27 \
    --obs 0.5 --years 3 --min_cases 20 --mcmc 3000 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `mcmc_trace.csv` | 76.1 KB |
| `phylogeny.nwk` | 566 B |
| `run_log.txt` | 165 B |
| `summary.csv` | 251 B |
| `who_infected_whom.csv` | 1.7 KB |

<details><summary>First lines of <code>mcmc_trace.csv</code></summary>

```
sample,log_post,off_r,off_p,pi,neg
1,-309.594128847471,0.989134926872794,0.5,0.502206707466394,0.482626642896794
2,-249.286612387806,0.943214510683902,0.5,0.547065702418331,0.905141625185497
3,-243.858643028131,0.871661792625673,0.5,0.534960872249212,0.96611135602463
4,-168.531654792503,0.9371111546061,0.5,0.563374930550344,1.41216432359535
5,-121.884562389083,1.04326367122121,0.5,0.585266984603368,1.17227739070542
6,-121.136637193816,1.20552067260724,0.5,0.58334541086806,0.946988008897752
7,-112.475578907926,1.16405560809653,0.5,0.603969542821869,0.925680948635563
8,-110.844670685753,1.30886880226899,0.5,0.630328948877286,1.12125196818262
9,-106.541419268885,1.32906365359668,0.5,0.598614468658343,1.10775034092832
10,-84.1938603165831,1.20002477837261,0.5,0.581544018303975,1.33552317703608
11,-84.8236081995072,1.13327803916764,0.5,0.572590693645179,1.23866178815253
```

</details>

<details><summary>First lines of <code>phylogeny.nwk</code></summary>

```
((((((11:1.132713909,(12:0.6831903947,20:0.8415619066):0.422522117):0.0275208159,13:0.5406557154):0.4060031412,14:1.33918623):0.2420425824,4:0.6297239409):0.1968681878,((17:1.493913957,3:0.1814671573)
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
TransPhylo 1.4.10: simulated 20 sampled cases (tree height 2.729 years)
MCMC 3000 iterations in 10.0 s; R posterior mean 3.82 (95% interval 2.01 to 5.76), true 3.00
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
parameter,true,posterior_mean,q025,q975
offspring_mean_R,3,3.82090668629322,2.01115396738169,5.75541305882507
sampling_prob_pi,0.5,0.789280657777344,0.535528284986504,0.990961432643236
neg_years,0.27,1.57501701011408,0.558098860706668,2.6992692442541
```

</details>

<details><summary>First lines of <code>who_infected_whom.csv</code></summary>

```
,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20
1,0,0.548902195608783,0.0818363273453093,0.261477045908183,0,0.0818363273453093,0.2375249500998,0,0.506986027944111,0,0,0,0.0818363273453093,0,0.471057884231536,0,0,0,0,0
2,0,0,0,0,0.944111776447117,0,0,0,0,0,0,0,0,0,0,0.882235528942125,0,0,0,0
3,0.0139720558882236,0.0179640718562874,0,0.0179640718562874,0,0.0179640718562874,0.0179640718562874,0.00199600798403194,0.00998003992015968,0,0,0,0.0179640718562874,0,0,0,0.992015968063885,0,0,0
4,0.259481037924151,0.259481037924151,0.762475049900206,0,0,0.762475049900206,0.22754491017964,0,0.259481037924151,0,0,0,0.72654690618763,0.307385229540918,0,0,0,0,0,0
5,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
6,0.059880239520958,0.059880239520958,0.0678642714570858,0.0678642714570858,0,0,0.0578842315369261,0.00798403193612774,0.0499001996007984,0,0,0,0.0678642714570858,0,0,0,0,0.904191616766477,0,0
7,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
8,0,0,0,0,0,0,0,0,0.00998003992015968,1.00000000000001,0,0,0,0,0,0,0,0,0.00998003992015968,0
9,0,0,0,0,0,0,0,0.938123752495021,0,0,0,0,0,0,0,0,0,0,0.936127744510989,0
10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
11,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--r` | Mean offspring number (reproduction number R) | 3 | 0.5 to 10 |
| `--obs` | Probability a case is sampled | 0.5 | 0.05 to 1 |
| `--neg` | Within-host coalescent scale Ne x g (years) | 0.27 | 0.01 to 5 |
| `--years` | Outbreak duration (years) | 3 | 1 to 6 |
| `--min_cases` | Minimum sampled cases (resimulates until reached) | 20 | 5 to 150 |
| `--mcmc` | MCMC iterations | 3000 | 500 to 30000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example simulates an outbreak with true R 3, sampling probability 0.5 and Ne x g 0.27 years over 3 years, keeping the first simulation with at least 20 sampled cases. It then runs 3000 MCMC iterations with seed 42.

- `run_log.txt` says "simulated 20 sampled cases (tree height 2.729 years)" and "MCMC 3000 iterations in 10.0 s; R posterior mean 3.82 (95% interval 2.01 to 5.76), true 3.00".
- `summary.csv` lists the true value and the second-half posterior mean and 95% interval for three parameters. R is 3.82 (2.01 to 5.76) against a true 3. The sampling probability is 0.789 (0.536 to 0.991) against 0.5. Ne x g is 1.575 (0.558 to 2.699) against 0.27.
- `mcmc_trace.csv` has 1000 rows (every 3rd iteration) with log posterior, R, pi and Ne x g.
- `who_infected_whom.csv` is a 20 x 20 matrix. Rows are the infector and columns the infected. Each column sums to at most 1. Six pairs have probability above 0.9 and 16 above 0.5.
- `phylogeny.nwk` is the simulated tree in Newick format.

R is recovered with the true value inside the interval. Pi and Ne x g are not: both true values sit below the lower end of their intervals. A 20-tip tree carries little information about them.

## Your own runs

Each run changes one setting from the example. All used seed 42 unless noted.

- **Every case sampled** (`--obs 1`). 45 sampled cases, R 3.94 (3.17 to 4.89). The interval is 1.72 wide against 3.75 in the example.
- **Lower R, longer outbreak** (`--r 1.5 --years 6`). 27 cases, tree height 5.354 years, R 1.49 (1.07 to 2.13), true 1.5.
- **Another seed** (`--seed 43`). 22 cases, R 3.55 (2.47 to 4.93). A different outbreak gives a different estimate.
- **Longer chain** (`--mcmc 15000`). Same 20 cases, R 3.72 (2.25 to 5.41), in 46.0 s. Five times the iterations shifted the mean by 0.1 and took 4.6 times as long.
- **A larger tree** (`--min_cases 60 --years 4`). 73 cases, R 3.44 (2.79 to 4.15).

## Pitfalls

- **Small trees give wide intervals.** The R interval narrows from 3.75 wide at 20 cases to 1.36 at 73.
- **Weakly identified parameters.** The within-host scale Ne x g had posterior means of 0.78 to 1.58 in the runs above against a true 0.27. With every case sampled, the sampling probability was 0.737 (0.644 to 0.829) against a true 1.
- **Chain length.** 3000 iterations are enough for a demonstration. Check `mcmc_trace.csv` for a flat log posterior before trusting an estimate, and raise `--mcmc` if it still climbs.
- **Resimulation.** The helper repeats the simulation until it reaches `--min_cases` sampled cases, up to 500 tries, and stops if none reaches it. Low R or a short outbreak can fail this.
- **Fixed generation time.** The inference is told the true generation and sampling distributions (gamma, shape 10, scale 0.1 years). Real data would need these from other sources.

## Further reading

- TransPhylo tutorial: https://xavierdidelot.github.io/TransPhylo/articles/TransPhylo.html
- Function reference: https://xavierdidelot.github.io/TransPhylo/reference/index.html
- Source: https://github.com/xavierdidelot/TransPhylo
- Paper: Didelot X, Fraser C, Gardy J, Colijn C (2017) Genomic infectious disease epidemiology in partially sampled and ongoing outbreaks. Molecular Biology and Evolution 34:997-1007. https://doi.org/10.1093/molbev/msw275

---

Cite: Didelot X, Fraser C, Gardy J, Colijn C (2017). Genomic infectious disease epidemiology in partially sampled and ongoing outbreaks. Mol Biol Evol 34:997-1007. doi:10.1093/molbev/msw275

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/transphylo).
