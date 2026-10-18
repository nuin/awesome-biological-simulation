# EpiModel

> Simulate an SIR epidemic as a deterministic compartmental model, a stochastic individual-contact model, or a network model with partnership dynamics.

Licence: GPL-3.0-or-later · [Source code](https://github.com/EpiModel/EpiModel)

## What it simulates

EpiModel simulates infectious-disease transmission with three model classes that share one interface.

- **dcm** is deterministic. It solves differential or difference equations for the compartments (susceptible, infected, recovered) and gives one smooth curve.
- **icm** is stochastic. It tracks individuals who mix at random and gives different curves from run to run.
- **net** is stochastic and network-based. It fits an exponential random graph model (ERGM) to a target number of partnerships. It then lets partnerships form and dissolve over time, and transmission happens along the current edges. This is the part of EpiModel built on the Statnet packages.

The recipe runs an SIR model in any of the three. You set transmission probability per act, acts per partnership per step, a recovery rate, the population size and the number of steps. For the network class you also set the mean degree and the mean partnership duration.

## When to use it

- You want to see how a partnership network, with a mean degree and a partnership length, changes an epidemic compared with random mixing.
- You want the deterministic curve and the stochastic spread side by side for the same parameters.
- You teach network epidemiology and want a package that fits an ERGM and simulates from it.

Use [epydemix](epydemix.md) for age-structured stochastic compartment models in Python. Use [NDlib](ndlib.md) for epidemics on a fixed graph that you choose by type. EpiModel's network class is the choice when partnerships must come and go over time.

## Install it yourself

EpiModel 2.7.0 is on CRAN and needs R 4.1 or newer. The recipe uses R 4.4 from conda-forge, and compiles `ergm`, `tergm`, `networkDynamic` and EpiModel from CRAN source. This works natively on arm64, and the image is 2.27 GB.

```r
install.packages("EpiModel")
```

A minimal deterministic run, using the same settings as the recipe's dcm class:

```r
library(EpiModel)
param <- param.dcm(inf.prob = 0.1, act.rate = 1, rec.rate = 0.05)
init <- init.dcm(s.num = 490, i.num = 10, r.num = 0)
control <- control.dcm(type = "SIR", nsteps = 100)
mod <- dcm(param, init, control)
df <- as.data.frame(mod)
```

In the 2.7.0 image this gave a peak of 81.8 infected at step 74.

## Run the tested example

This recipe builds EpiModel in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 7.5 s.

1. Download [epimodel-recipe.tar.gz](https://biosimhub.pages.dev/guides/epimodel/epimodel-recipe.tar.gz) (Dockerfile, run_epimodel.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf epimodel-recipe.tar.gz
   cd epimodel
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/epimodel:2.7.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/epimodel:2.7.0 Rscript /opt/run_epimodel.R net 500 10 0.1 1 0.05 100 5 2 20 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `results.csv` | 2.9 KB |
| `run_log.txt` | 113 B |

<details><summary>First lines of <code>results.csv</code></summary>

```
"time","s.num","i.num","r.num","num","si.flow","ir.flow"
1,490,10,0,500,NA,NA
2,488.2,11.6,0.2,500,1.8,0.2
3,486.6,12.6,0.8,500,1.6,0.6
4,484.6,14.4,1,500,2,0.2
5,482.4,15.8,1.8,500,2.2,0.8
6,479.8,18,2.2,500,2.6,0.4
7,476.8,19.2,4,500,3,1.8
8,474.8,20.2,5,500,2,1
9,473,20.8,6.2,500,1.8,1.2
10,470.6,21.6,7.8,500,2.4,1.6
11,467.8,23.2,9,500,2.8,1.2
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
EpiModel 2.7.0, model net, N=500, seed=42
peak i.num 100.2 at step 54
final s.num 124.0, i.num 43.0, r.num 333.0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `type` | Model class (dcm deterministic | net | dcm, icm, net |
| `population` | Population size | 500 | 50 to 2000 |
| `initial_infected` | Initially infected | 10 | 1 to 100 |
| `inf_prob` | Transmission probability per act | 0.1 | 0.001 to 1 |
| `act_rate` | Acts per partnership per step | 1 | 0.1 to 10 |
| `rec_rate` | Recovery rate per step | 0.05 | 0.001 to 1 |
| `days` | Time steps | 100 | 10 to 500 |
| `nsims` | Simulations (icm and net) | 5 | 1 to 20 |
| `mean_degree` | Mean degree (net only) | 2 | 0.1 to 10 |
| `duration` | Mean partnership duration in steps (net only) | 20 | 1 to 500 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `run_epimodel.R` builds the chosen model and writes `results.csv` plus a three-line `run_log.txt`. For the network class it creates 500 nodes, fits `netest` with the formula `~edges` and a target of nodes times mean degree divided by 2 edges, and runs `netsim` with the SIR type, 10 initial infections and 5 simulations. Your seed is set with `set.seed` before the fit and the run.

The example is the network class with 500 nodes, transmission probability 0.1, 1 act per step, recovery rate 0.05, mean degree 2, mean partnership duration 20 steps, 100 steps and seed 42. The run took 7.5 seconds.

- `run_log.txt` gives the peak and the end state. The mean over 5 simulations peaked at 100.2 infected at step 54. At step 100 there were 124.0 susceptible, 43.0 infected and 333.0 recovered.
- `results.csv` has 100 rows (steps 1 to 100) and the columns `time,s.num,i.num,r.num,num,si.flow,ir.flow`. For the network and icm classes the values are means over the simulations, so they are not whole numbers. At step 1 there are 490 susceptible and 10 infected. `si.flow` and `ir.flow` are the new infections and new recoveries per step. They are NA at step 1.

At step 54 the file shows 241 susceptible, 100.2 infected and 158.8 recovered. The population `num` stays at 500 because the model has no births or deaths.

## Your own runs

Same image and settings as the example, with one change each.

- **Another seed** (`seed 43`). The peak is 84.8 at step 66, against 100.2 at step 54, and the final recovered count is 297.4 against 333.0. Averages over 5 simulations still shift with the seed.
- **Mean degree 1**. The peak falls to 16.4 at step 23, and only 65.0 recover by step 100.
- **Partnerships of 200 steps** (`duration 200`). The peak is 73.8 at step 36 and 245.0 have recovered by the end.
- **Deterministic version** (`dcm`, same transmission, 1 act per step). The curve peaks at 81.8 infected at step 74, and 268.0 have recovered by step 100. It has no spread between runs.
- **Four acts per step in the dcm** (`act_rate 4`). The peak is 308.7 at step 18, and 493.3 have recovered at step 100.
- **Stochastic random mixing** (`icm`). The mean peak is 54.8 at step 91, and 198.6 have recovered by step 100. The icm peaks later and lower than the dcm with the same numbers (81.8 at step 74).

Two runs of the example settings gave byte-identical `results.csv` files.

## Pitfalls

- **Integer counts break icm.** In the 2.7.0 image, `icm` failed with "invalid first argument" in `sample.int` when the population, initial counts, steps and simulations were all R integers; the same call with plain numbers worked. The recipe passes numeric values. Do the same in your own scripts (`500`, not `500L`).
- **init.net needs `r.num`.** An SIR `netsim` stops with "Specify r.num in init.net" unless you set `r.num = 0`.
- **The classes are not interchangeable.** The same transmission and recovery numbers gave a peak of 81.8 at step 74 in dcm and 100.2 at step 54 in the network class. Compare classes only after you match their contact structure.
- **Averages hide the spread.** `icm` and `net` write the mean of the simulations, so one file does not show the range between runs.
- **Size limits.** The recipe caps the population at 2,000 and the steps at 500 to stay inside its time limit.

## Further reading

- Tutorials: https://www.epimodel.org/tut.html
- CRAN page: https://cran.r-project.org/package=EpiModel
- Source: https://github.com/EpiModel/EpiModel
- Paper: Jenness SM, Goodreau SM, Morris M (2018) EpiModel: An R package for mathematical modeling of infectious disease over networks. J Stat Softw 84(8):1-47. https://doi.org/10.18637/jss.v084.i08

---

Cite: Jenness SM, Goodreau SM, Morris M (2018). EpiModel: An R package for mathematical modeling of infectious disease over networks. J Stat Softw 84(8):1-47. doi:10.18637/jss.v084.i08

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/epimodel).
