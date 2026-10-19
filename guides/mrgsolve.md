# mrgsolve

> Simulate repeated oral dosing, plasma concentration and an indirect response for a virtual group of subjects with mrgsolve's pre-compiled house model, from R.

Licence: GPL-2.0-or-later · [Source code](https://github.com/metrumresearchgroup/mrgsolve)

## What it simulates

mrgsolve simulates ordinary-differential-equation models of drug disposition and effect, from R. You write a model in a small text format with C++ code for the equations. mrgsolve compiles it and solves it for dosing events, covariates and random effects. It is used for population pharmacokinetics and pharmacodynamics (PK/PD) and for quantitative systems pharmacology (QSP) and physiologically based PK models.

A model file has blocks for parameters (`$PARAM`), compartments (`$CMT`), the equations (`$ODE`), derived values (`$TABLE`) and the columns to return (`$CAPTURE`). Between-subject variability goes in `$OMEGA` and residual error in `$SIGMA`. A simulation takes the model, an event table of doses and an optional data set of subjects.

The recipe uses `house()`, a model that ships pre-compiled in the package. It is a generic indirect-response PK/PD model with a gut dosing compartment (GUT), a central compartment (CENT) and a response (RESP). The mrgsolve reference page lists the defaults: clearance 1 L/hr, volume 20 L, absorption rate 1.2 per hr, KIN 100, KOUT 2 and IC50 10.

## When to use it

Use mrgsolve for dose-regimen studies, virtual populations and QSP models, when you want the model, the data and the plots in one R session.

- Use [PK-Sim](pk-sim.md) when you want a whole-body PBPK model with built-in physiology and a graphical interface.
- Use [COPASI](copasi.md) when the model is a biochemical reaction network in SBML.
- Use [GillesPy2](gillespy2.md) when counts are small and you need stochastic simulation.

## Install

From CRAN, in R:

```r
install.packages("mrgsolve")
```

CRAN lists mrgsolve 2.0.1 (published 2026-05-20), licensed GPL (>= 2). The conda-forge package `r-mrgsolve` is also 2.0.1, built for Linux x86-64, macOS Intel and Windows:

```
micromamba create -n mrg -c conda-forge r-base=4.5 r-mrgsolve=2.0.1
```

You need a C++ and a Fortran compiler to compile your own models. The installation wiki says the usual toolchain for building R packages is enough: Rtools on Windows, the command line tools on macOS, and gcc with gfortran on Linux. It also warns against running R on a network or cloud-synced drive.

## A first run

Adapted from the [README](https://github.com/metrumresearchgroup/mrgsolve#readme). It reads the one-compartment model `pk1` from the model library, gives 100 mg every 24 hours for 10 doses and plots the concentration.

```r
library(mrgsolve)
mod <- mread("pk1", modlib())
mod %>%
  ev(amt = 100, ii = 24, addl = 9) %>%
  mrgsim(end = 300, delta = 0.1) %>%
  plot(CP ~ time)
```

`mread` compiles the model, so this needs the compiler. The recipe swaps in `house()` so that nothing is compiled. A virtual group gets 100 mg every 24 hours for 4 doses, over 168 hours.

## Run the tested example

This recipe builds mrgsolve in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 5.5 s. mrgsolve has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [mrgsolve-recipe.tar.gz](https://biosimhub.pages.dev/guides/mrgsolve/mrgsolve-recipe.tar.gz) (Dockerfile, run_mrgsolve.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf mrgsolve-recipe.tar.gz
   cd mrgsolve
   sh run.sh
   ```

![Terminal recording of the mrgsolve example run](https://biosimhub.pages.dev/media/mrgsolve/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/mrgsolve:2.0.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/mrgsolve:2.0.1 Rscript /opt/run_mrgsolve.R --dose 100 --interval 24 \
    --doses 4 --end 168 --delta 1 --subjects 20 \
    --omega 0.09 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 181 B |
| `simulation.csv` | 312.8 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/mrgsolve/result-dark.png"><img src="https://biosimhub.pages.dev/media/mrgsolve/result.png" alt="Plot of the mrgsolve example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
mrgsolve 2.0.1 model=house subjects=20 dose=100 every 24 h x 4, omega=0.09, seed=42
rows=3400 columns=ID,time,GUT,CENT,RESP,DV,CP
CP at t=168: mean=0.08906 min=0.0001045 max=0.5247
```

</details>

<details><summary>First lines of <code>simulation.csv</code></summary>

```
"ID","time","GUT","CENT","RESP","DV","CP"
1,0,0,0,74.3338598851186,0,0
1,0,100,0,74.3338598851186,0,0
1,1,24.6711793739724,73.2769586568107,62.5834814056561,3.88283877676362,3.88283877676362
1,2,6.08667092718241,88.1183626729226,54.3010317849808,4.66926305080134,4.66926305080134
1,3,1.50165350059702,88.6860101750282,51.5055222566597,4.69934186101822,4.69934186101822
1,4,0.370475628053316,85.8688214822683,51.0313310601494,4.55006315597617,4.55006315597617
1,5,0.0914007063557165,82.3471845994768,51.3689871246389,4.36345677251224,4.36345677251224
1,6,0.0225496343187156,78.7766124603556,51.9630601695324,4.17425738144659,4.17425738144659
1,7,0.0055632616192119,75.3133123444263,52.6281500016641,3.9907421778656,3.9907421778656
1,8,0.00137252247650274,71.9905505649686,53.305481390522,3.8146738950149,3.8146738950149
1,9,0.000338616835659079,68.8114953296622,53.976924655434,3.64622041158183,3.64622041158183
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--dose` | Dose per administration (mg) | 100 | 0.1 to 10000 |
| `--interval` | Dosing interval (hours) | 24 | 1 to 720 |
| `--doses` | Number of doses | 4 | 1 to 100 |
| `--end` | Simulation end time (hours) | 168 | 1 to 5000 |
| `--delta` | Output step (hours) | 1 | 0.1 to 24 |
| `--subjects` | Virtual subjects | 20 | 1 to 500 |
| `--omega` | Between-subject variance of CL | 0.09 | 0 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`mrgsim()` returns a table with one row per subject and time. The house model returns `ID`, `time`, the compartment amounts `GUT`, `CENT` and `RESP`, and the captured items `DV` (the dependent variable, with residual error) and `CP` (plasma concentration). The recipe writes it to `simulation.csv` and prints the mean, minimum and maximum `CP` at the last time in `run_log.txt`.

- `CP` is `CENT` divided by the individual volume. It rises after each dose and falls between doses.
- `RESP` starts at KIN/KOUT and falls while `CP` is high, because the drug inhibits the production of the response.
- Subjects differ because the recipe sets a shared variance on the random effects of CL, VC, KA and KOUT. The packaged model has all four set to zero.

## Pitfalls

- **Model compilation needs a compiler and a place to run code.** `mread()` builds a shared library in a temporary directory and loads it. A read-only or no-exec temporary directory can make it fail, which is why the recipe uses `house()`.
- **Random effects are zero by default in `house()`.** Identical subjects are the result until you set `omat()`.
- **Units are yours to keep consistent.** The house code divides amounts in mg by a volume in L, while its labels call `CP` ng/ml.
- **Dosing goes to compartment 1 unless told otherwise.** In `house()`, that is `GUT`. Set `cmt` in the event to dose elsewhere.
- **A seed fixes the random effects only.** The recipe calls `set.seed()` before simulating, so the same seed and settings give the same table.

## Further reading

- User guide: https://mrgsolve.org/user-guide/
- Reference for `house()`: https://mrgsolve.org/docs/reference/house.html
- Installation wiki: https://github.com/metrumresearchgroup/mrgsolve/wiki/mrgsolve-Installation
- Source: https://github.com/metrumresearchgroup/mrgsolve
- Paper: Elmokadem A, Riggs MM, Baron KT (2019). Quantitative systems pharmacology and physiologically-based pharmacokinetic modeling with mrgsolve: a hands-on tutorial. CPT: Pharmacometrics & Systems Pharmacology 8:883-893. https://doi.org/10.1002/psp4.12467

---

Cite: Elmokadem A, Riggs MM, Baron KT (2019). Quantitative systems pharmacology and physiologically-based pharmacokinetic modeling with mrgsolve, a hands-on tutorial. CPT Pharmacometrics Syst Pharmacol 8:883-893. doi:10.1002/psp4.12467

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/mrgsolve).
