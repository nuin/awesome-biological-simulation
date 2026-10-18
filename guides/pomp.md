# pomp

> Simulate a partially observed stochastic SIR epidemic many times, with binomial case reports, and return the latent S/I/R paths and reported cases.

Licence: GPL-3.0-or-later · [Source code](https://github.com/kingaa/pomp)

## What it simulates

pomp (Partially Observed Markov Processes) is an R package for models in which a hidden state changes at random over time and you see only noisy measurements of it. You write the model as a set of pieces: how the hidden state starts (`rinit`), how it moves in time (`rprocess`) and how data are generated from it (`rmeasure`). pomp then simulates from the model, and can also fit it to data with particle filters, iterated filtering (`mif2`) and particle MCMC.

The biosimhub example uses the simulation side only. The hidden state is a stochastic SIR epidemic in a closed population. Each day a share of susceptible people become infected and a share of infectious people recover, drawn from exponential waiting times with `reulermultinom` on an Euler step. The measurement is a count of reported cases: each new infection is reported with probability rho.

The key assumptions are random mixing, constant rates, a fixed Euler step (`dt`) and independent reporting. Everything else is what you write into the model pieces.

## When to use it

- You have counts of cases over time and want a stochastic model that generates data like them, for example to test a fitting method on simulated data.
- You want the spread of epidemics from a given R0 in a small population, including the chance that an outbreak dies out.
- You plan to fit the same model to real data with `pfilter` or `mif2` later.

[epydemix](epydemix.md) fits when you want a ready-made SIR or SEIR with age groups in Python. [GillesPy2](gillespy2.md) fits when you want exact event-by-event simulation.

## Install it yourself

pomp 6.4 is on CRAN and needs R 4.1 or newer and a C compiler. The recipe's image uses R 4.2.2 from Debian bookworm, the Debian packages for mvtnorm, deSolve, coda, data.table and digest, and `R CMD INSTALL pomp_6.4.tar.gz` from the CRAN source archive. In an R session, `install.packages("pomp")` does the same.

Minimal script with a fixed seed. The model pieces are plain R functions here. pomp can also compile C snippets, which is faster for large runs but needs to load a compiled library from a writable, executable directory:

```r
library(pomp)

sir <- pomp(
  data = data.frame(day = 1:60, reports = NA_real_),
  times = "day", t0 = 0,
  rprocess = euler(function(S, I, R, C, Beta, gamma, N, delta.t, ...) {
    inf <- reulermultinom(1, S, Beta * I / N, delta.t)
    rec <- reulermultinom(1, I, gamma, delta.t)
    c(S = S - inf, I = I + inf - rec, R = R + rec, C = C + inf)
  }, delta.t = 0.1),
  rinit = function(N, I0, ...) c(S = N - I0, I = I0, R = 0, C = 0),
  rmeasure = function(C, rho, ...) c(reports = rbinom(1, round(C), rho)),
  accumvars = "C", statenames = c("S", "I", "R", "C"),
  paramnames = c("Beta", "gamma", "rho", "N", "I0"),
  params = c(Beta = 0.5, gamma = 0.25, rho = 0.3, N = 5000, I0 = 5)
)
sims <- simulate(sir, nsim = 3, seed = 7, format = "data.frame")
print(aggregate(reports ~ .id, sims, sum))
```

In the recipe's image this printed total reports of 1181, 1182 and 1142 for the three simulations, the same on a second run. `accumvars = "C"` makes C a counter that pomp resets to 0 after each reporting time.

## Run the tested example

This recipe builds pomp in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 1.8 s.

1. Download [pomp-recipe.tar.gz](https://biosimhub.pages.dev/guides/pomp/pomp-recipe.tar.gz) (Dockerfile, driver.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pomp-recipe.tar.gz
   cd pomp
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pomp:6.4 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pomp:6.4 Rscript /opt/driver.R --population 10000 --r0 2 \
    --infectious-days 4 --reporting 0.3 --initial 5 \
    --days 100 --nsim 20 --dt 0.05 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 156 B |
| `simulations.csv` | 45.5 KB |
| `summary.csv` | 455 B |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
pomp 6.4: SIR, N=10000, R0=2.00, 20 simulations over 100 days, seed=42
final size mean 7596 (min 9, max 8140); peak infectious mean 1478; reports mean 2268
```

</details>

<details><summary>First lines of <code>simulations.csv</code></summary>

```
sim,day,S,I,R,C,reports
1,1,9990,8,2,5,2
2,1,9995,2,3,0,0
3,1,9995,4,1,0,0
4,1,9989,8,3,6,2
5,1,9993,6,1,2,0
6,1,9990,8,2,5,1
7,1,9989,9,2,6,2
8,1,9994,4,2,1,0
9,1,9993,6,1,2,1
10,1,9993,6,1,2,0
11,1,9992,6,2,3,2
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
sim,peak_day,peak_infectious,final_size,total_reports
1,26,1672,8039,2393
2,33,1589,7891,2354
3,34,1451,8050,2374
4,41,1384,7864,2353
5,32,1510,8012,2362
6,29,1521,7881,2351
7,31,1525,8140,2421
8,32,1531,7990,2424
9,29,1709,8078,2501
10,1,6,9,1
11,42,1478,7922,2330
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--population` | Population size | 10000 | 100 to 200000 |
| `--r0` | Basic reproduction number R0 | 2 | 0.1 to 10 |
| `--infectious-days` | Mean infectious period (days) | 4 | 0.5 to 30 |
| `--reporting` | Reporting probability per new infection | 0.3 | 0.01 to 1 |
| `--initial` | Initially infectious people | 5 | 1 to 1000 |
| `--days` | Simulation length (days) | 100 | 10 to 365 |
| `--nsim` | Simulations | 20 | 1 to 100 |
| `--dt` | Euler step (days) | 0.05 | 0.01 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `driver.R` builds the model above from your options: beta is R0 divided by the infectious period, gamma is 1 divided by the infectious period, and the Euler step is 0.05 days. The example uses 10,000 people, R0 = 2, a 4 day infectious period, reporting probability 0.3, 5 initially infectious people, 100 days, 20 simulations and seed 42. It ran in 1.0 s.

- `run_log.txt` (156 bytes): `pomp 6.4: SIR, N=10000, R0=2.00, 20 simulations over 100 days, seed=42`, then `final size mean 7596 (min 9, max 8140); peak infectious mean 1478; reports mean 2268`.
- `simulations.csv` (46,552 bytes): one row per simulation and day, with S, I, R, the new infections since the last report (C) and the reported cases.
- `summary.csv` (455 bytes): one row per simulation with the peak day, peak number infectious, final size and total reports.

The mean of 7596 mixes two outcomes. In 19 of the 20 simulations the epidemic took off and ended with 7864 to 8140 people ever infected (mean 7996), peaking on day 24 to day 42. In one simulation (number 10) the 5 first cases recovered before spreading: the epidemic stopped at 9 people. Theory for a closed population with R0 = 2 gives a final size of 79.7 percent, or 7968 people, which agrees with the 7996 of the epidemics that took off. The chance of early extinction is about (1/R0)^5 = 3 percent per run, so seeing 1 in 20 is ordinary.

Reported cases total 2268 on average, which is 0.3 times the 7596 infections. The reports are binomial, so day-to-day counts are noisy even when S, I and R are smooth.

## Your own runs

Same image as the recipe, seed 42, 20 simulations unless noted.

- **Higher R0** (`--r0 3`). Every simulation took off. Final sizes ranged from 9369 to 9465 (mean 9418, theory 9405), and the peaks came on day 17 to day 22.
- **Lower R0** (`--r0 1.5`). 5 of 20 simulations died out early. The other 15 averaged 5813 infected (theory 5828) and peaked on day 42 to day 68.
- **Below threshold** (`--r0 0.8`). 19 of 20 simulations ended under 100 infected, mean 23, and the largest outbreak reached 150 people.
- **A coarse step** (`--dt 1`). The epidemics that took off averaged 8572 infected, against 7996 with `dt` = 0.05. The mean peak number infectious rose from 1478 to 1910.
- **Another seed** (`--seed 43`). 1 simulation died out again. The mean final size was 7595.
- **Larger and rarely reported** (`--population 50000 --reporting 0.1`). The mean final size was 37,974, and the reported cases averaged 3816.

## Pitfalls

- **Euler step.** A one-day step overshoots a fast epidemic. The run above with `dt` 1 overestimated the final size by 7 percent. Use 0.1 or smaller.
- **C snippets and read-only machines.** pomp compiles `Csnippet` code into a shared library and loads it. Where `/tmp` is mounted non-executable, as in the biosimhub job server, the load fails with "failed to map segment from shared object". The recipe therefore writes the model as R functions. On your own machine, use C snippets for speed.
- **Means hide die-outs.** Report the number of early extinctions and the size of the epidemics that took off.
- **Reports are not infections.** With rho = 0.3 the data show a third of the infections, and the peak of reports is lower than the peak of infections.
- **Seeds.** Pass `seed` to `simulate`. The same seed reproduced the same output in every run here.

## Further reading

- Package website and tutorials: https://kingaa.github.io/pomp/
- Source: https://github.com/kingaa/pomp
- Paper: King AA, Nguyen D, Ionides EL (2016) Statistical inference for partially observed Markov processes via the R package pomp. Journal of Statistical Software 69(12):1-43. https://doi.org/10.18637/jss.v069.i12

---

Cite: King AA, Nguyen D, Ionides EL (2016). Statistical inference for partially observed Markov processes via the R package pomp. Journal of Statistical Software 69(12):1-43. doi:10.18637/jss.v069.i12

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pomp).
