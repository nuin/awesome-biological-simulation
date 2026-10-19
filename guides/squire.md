# squire

> Age-structured COVID-19 SEIR model with hospital and ICU demand, run as an ODE or as one stochastic replicate, with a change in R0 on a chosen day.

Licence: MIT · [Source code](https://github.com/mrc-ide/squire)

## What it simulates

squire simulates a SARS-CoV-2 epidemic in an age-structured population. People move from susceptible to exposed, then through infectious stages that follow disease severity: mild cases, and severe cases that need hospital or ICU care. Severe cases pass through oxygen or mechanical-ventilation pathways, and a case that cannot get a bed has a higher chance of dying. The model has 17 five-year age groups, a country-specific contact matrix and country-specific population and healthcare capacity data that ship inside the package.

Two versions exist. `run_deterministic_SEIR_model` solves the equations as ODEs. `run_explicit_SEEIR_model` is stochastic: each run draws random transitions, so repeated runs differ. The README warns that squire is released without support and that parameter names and output formats can change without notice.

## When to use it

Use squire to ask how a change in transmission (R0) at a chosen day shifts hospital and ICU demand, and deaths, for a given country.

- Use [epydemix](epydemix.md) for a generic SIR or SEIR model with your own contact matrices and quantile bands.
- Use [MEmilio](memilio.md) for a general ODE or agent-based model library, in particular when you want regions or vaccination.
- Use [GillesPy2](gillespy2.md) when the system is a reaction network, not a population.

The model is COVID-specific. Its severity and duration parameters are set for SARS-CoV-2 in 2020. The authors ask users to contact them before publishing results from it.

## Install

squire is an R package (current tag v0.7.1, MIT licence), installed from GitHub:

```r
install.packages("remotes")
remotes::install_github("mrc-ide/squire")
```

It needs a C compiler because it ships a generated odin model in `src/odin.c`. Its imports include odin, dde and drjacoby, which are not on conda-forge. odin (1.2.7) and dde (1.0.7) are on CRAN. drjacoby is GitHub-only (mrc-ide/drjacoby, latest tag v1.5.4).

## Run the tested example

This recipe builds squire in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.8 s.

1. Download [squire-recipe.tar.gz](https://biosimhub.pages.dev/guides/squire/squire-recipe.tar.gz) (Dockerfile, run_squire.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf squire-recipe.tar.gz
   cd squire
   sh run.sh
   ```

![Terminal recording of the squire example run](https://biosimhub.pages.dev/media/squire/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/squire:0.7.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/squire:0.7.1 Rscript /opt/run_squire.R --country 'United Kingdom' \
    --model deterministic --r0 3 --r0-after 1.5 \
    --change-day 60 --days 250 --hosp-beds 100000 \
    --icu-beds 5000 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `by_age_final.csv` | 191 B |
| `run_log.txt` | 117 B |
| `summary.csv` | 273 B |
| `timeseries.csv` | 16.1 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/squire/result-dark.png"><img src="https://biosimhub.pages.dev/media/squire/result.png" alt="Plot of the squire example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>by_age_final.csv</code></summary>

```
"age_group","deaths_cumulative"
1,207.2
2,502.6
3,699.9
4,775.7
5,875.9
6,1381.2
7,2202
8,3844.8
9,6093.6
10,9544.4
11,13934.1
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: United Kingdom, deterministic model, population 67886004, peak hospital demand 97060 on day 107, deaths 233590
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
"country","model","population","r0","r0_after","change_day","peak_hospital_demand","peak_hospital_day","peak_icu_demand","peak_icu_day","deaths_end","hospital_capacity","icu_capacity"
"United Kingdom","deterministic",67886004,3,1.5,60,97060,107,8268,103,233590,100000,5000
```

</details>

<details><summary>First lines of <code>timeseries.csv</code></summary>

```
"day","susceptible","exposed","recovered","deaths_cumulative","infections","hospital_demand","icu_demand"
1,67885984,20,0,0,0,0,0
2,67885983.36,19.21,0.21,0,0.24,0,0
3,67885980.26,19.28,1.25,0,0.34,0,0
4,67885974.48,21.33,3.17,0,0.4,0.01,0
5,67885966.39,25.11,5.87,0,0.46,0.02,0.01
6,67885956.21,30.27,9.29,0,0.54,0.05,0.01
7,67885943.82,36.66,13.47,0,0.65,0.08,0.02
8,67885928.88,44.37,18.53,0,0.78,0.12,0.03
9,67885910.89,53.65,24.65,0,0.95,0.17,0.05
10,67885889.17,64.83,32.04,0.01,1.15,0.24,0.07
11,67885862.9,78.35,40.97,0.01,1.39,0.32,0.09
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--country` | Country | United Kingdom | United Kingdom, Kenya, India, Brazil, Japan, Nigeria |
| `--model` | Model | deterministic | deterministic, stochastic |
| `--r0` | R0 at the start | 3 | 0.5 to 8 |
| `--r0-after` | R0 after the change day | 1.5 | 0.1 to 8 |
| `--change-day` | Day R0 changes (0 = never) | 60 | 0 to 700 |
| `--days` | Simulated days | 250 | 30 to 700 |
| `--hosp-beds` | Hospital beds | 100000 | 100 to 5000000 |
| `--icu-beds` | ICU beds | 5000 | 10 to 500000 |
| `--seed` | Seed (stochastic model) | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the README at https://github.com/mrc-ide/squire and the package site at https://mrc-ide.github.io/squire/. The helper script `run_squire.R` follows the same calls:

```r
library(squire)
pop <- get_population("United Kingdom")
cm  <- get_mixing_matrix("United Kingdom")
out <- run_deterministic_SEIR_model(
  population = pop$n, country = "United Kingdom", contact_matrix_set = cm,
  tt_R0 = c(0, 60), R0 = c(3, 1.5), time_period = 250,
  hosp_bed_capacity = 100000, ICU_bed_capacity = 5000)
format_output(out, var_select = c("hospital_demand", "ICU_demand", "D"), reduce_age = TRUE)
```

`tt_R0` gives the days on which R0 changes and `R0` gives the new values, so R0 falls from 3 to 1.5 on day 60. `format_output` returns a long table with columns replicate, compartment, t and y.

The recipe has since been built and run on biosimhub as an image. The helper script ran in a conda-forge R 4.3 test container with the package versions above. With the settings shown, one run printed a peak hospital demand of 96,175 on day 108, a peak ICU demand of 8,232 on day 104 and 232,814 cumulative deaths on day 250 for a population of 67,886,004. A stochastic run with seed 42 gave a peak of 105,826 on day 102 and 254,540 deaths. Treat these as one trial, not as a reference.

## Reading the output

The recipe writes `timeseries.csv` with one row per day: susceptible, exposed, recovered, cumulative deaths, daily infections, hospital demand and ICU demand. `by_age_final.csv` has cumulative deaths in the 17 age groups on the last day, and `summary.csv` has the peaks and capacities.

Compare `hospital_demand` and `icu_demand` with the bed counts in `summary.csv`. When demand passes capacity, squire raises the death probability for people who cannot be treated, so deaths rise faster than infections.

## Pitfalls

- **Stochastic runs differ.** Use a seed for repeatability and run many seeds before you read an average.
- **Time step.** The deterministic model returns values every 0.1 day. The helper keeps whole days.
- **Population argument.** A population that does not match the country's age structure changes the age mix the model uses. The helper rescales the age counts and keeps the proportions.
- **Capacity numbers are inputs.** Defaults for beds come from package data and are rough. Set them yourself.
- **Install order.** `install_github("mrc-ide/squire")` fails if drjacoby is missing, because it is a declared import.

## Further reading

- Source: https://github.com/mrc-ide/squire
- Package site and vignettes: https://mrc-ide.github.io/squire/
- Paper: Walker PGT et al. (2020) The impact of COVID-19 and strategies for mitigation and suppression in low- and middle-income countries. Science 369(6502):413-422. https://doi.org/10.1126/science.abc0035

---

Cite: Walker PGT, et al. (2020). The impact of COVID-19 and strategies for mitigation and suppression in low- and middle-income countries. Science 369(6502):413-422. doi:10.1126/science.abc0035

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/squire).
