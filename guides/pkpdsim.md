# PKPDsim

> Simulate drug concentration over time from a one-compartment PK model under a dosing regimen, with optional between-subject variability.

Licence: MIT · [Source code](https://github.com/InsightRX/PKPDsim)

## What it simulates

PKPDsim integrates ODE systems for pharmacokinetic-pharmacodynamic (PK-PD) models, including mixed-effects models with variability between patients. You choose a model, give parameter values, define a dosing regimen and call `sim()`. The result is a data frame of compartment amounts or observed concentrations over time.

A simulation has three parts:

- **A model**, made with `new_ode_model()`. The library has `pk_1cmt_iv`, `pk_2cmt_iv`, `pk_3cmt_iv`, `pk_1cmt_oral`, `pk_2cmt_oral`, `pk_3cmt_oral` and a few more. You can also write your own ODEs as pseudo-R code, which PKPDsim translates to C++.
- **A regimen**, made with `new_regimen()`. You set dose, number of doses and interval, or give explicit times. Doses can be bolus, infusion or oral, and a regimen can start at steady state.
- **Parameters**, as a named list such as `list(CL = 5, V = 50)`.

For a population, `sim()` takes the number of patients `n` and an omega matrix for between-subject variability. PKPDsim also supports covariates, residual error, inter-occasion variability and export of a model to other tools. PKPDsim does not track units: the dose, volume and time units you choose define the concentration units.

## When to use it

Use PKPDsim to explore how dose, interval and patient variability shape drug exposure, or to simulate virtual patients from a published PK model.

- The Open Systems Pharmacology suite ([ospsuite](ospsuite-r.md)) simulates whole-body physiologically based models instead of compartment models.
- [COPASI](copasi.md) fits general kinetic models and estimates parameters from data.
- nlmixr2 in R is a tool for fitting population PK models. PKPDsim has an article on estimation with nlmixr2.

## Install

PKPDsim is on CRAN. The CRAN release is 1.4.1 (17 April 2025). The GitHub development version is 1.5.0. The licence is MIT. There is no conda package (checked on anaconda.org).

```r
install.packages("PKPDsim")
# development version
install.packages("PKPDsim", repos = "https://insightrx.r-universe.dev")
```

The package contains C++ code, so a compiler is needed unless your platform provides a binary. Custom ODE models are compiled when you create them, so they also need a compiler at run time. The library models are precompiled.

## Run the tested example

This recipe builds PKPDsim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 4.6 s.

1. Download [pkpdsim-recipe.tar.gz](https://biosimhub.pages.dev/guides/pkpdsim/pkpdsim-recipe.tar.gz) (Dockerfile, run_pkpdsim.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pkpdsim-recipe.tar.gz
   cd pkpdsim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pkpdsim:1.4.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pkpdsim:1.4.1 Rscript /opt/run_pkpdsim.R pk_1cmt_iv 100 3 12 2 5 50 0.5 20 0.2 48 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `concentrations.csv` | 59.8 KB |
| `run_log.txt` | 47 B |
| `summary.csv` | 810 B |

<details><summary>First lines of <code>concentrations.csv</code></summary>

```
"id","t","comp","y","obs_type"
1,0,"obs",0,1
1,0.5,"obs",0.372515187048505,1
1,1,"obs",0.730275950215075,1
1,1.5,"obs",1.07386667647682,1
1,2,"obs",1.40384860665878,1
1,2.5,"obs",1.34824556514839,1
1,3,"obs",1.2948448253752,1
1,3.5,"obs",1.243559159504,1
1,4,"obs",1.19430479458277,1
1,4.5,"obs",1.14700127570313,1
1,5,"obs",1.10157133458064,1
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
pk_1cmt_iv: 20 individuals, 1940 rows, seed 42
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
"id","cmax","tmax","auc"
1,2.13783790903343,26,51.9617633334804
2,2.2391592184254,26,41.6013980294013
3,2.39282287698187,26,54.9797667714417
4,2.67743324392783,26,68.0278192916694
5,2.92613838214914,26,76.0960134407255
6,2.43954697956356,26,53.1576055544682
7,2.11853954868525,26,52.0753960029504
8,2.13434789448343,26,41.563822968565
9,2.15447224914506,26,56.5222773200861
10,2.3779422116349,26,51.148163102902
11,2.3209820677823,26,58.6960032636845
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `model` | PK model | pk_1cmt_iv | pk_1cmt_iv, pk_1cmt_oral |
| `amt` | Dose per administration | 100 | 0.001 to 100000 |
| `n_doses` | Number of doses | 3 | 1 to 50 |
| `interval` | Dosing interval (h) | 12 | 0.5 to 168 |
| `t_inf` | Infusion time (h; 0 = bolus; IV model only) | 2 | 0 to 24 |
| `cl` | Clearance CL (L/h) | 5 | 0.001 to 1000 |
| `v` | Volume V (L) | 50 | 0.01 to 10000 |
| `ka` | Absorption rate KA (1/h; oral model only) | 0.5 | 0.001 to 100 |
| `n_ind` | Individuals | 20 | 1 to 500 |
| `cv` | Between-subject CV on CL and V (0 = none) | 0.2 | 0 to 2 |
| `t_end` | End of observation (h) | 48 | 1 to 1000 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Simulation and Variability articles: https://insightrx.github.io/PKPDsim/articles/simulation.html and https://insightrx.github.io/PKPDsim/articles/variability.html.

```r
library(PKPDsim)
model <- new_ode_model("pk_1cmt_iv")
parameters <- list(CL = 5, V = 50)
regimen <- new_regimen(amt = 100, n = 3, interval = 12,
                       type = "infusion", t_inf = 2)
dat <- sim(ode = model, parameters = parameters, regimen = regimen,
           t_obs = c(0.5, 2, 4, 8, 12, 16, 24))
```

This gives a 1-compartment model with clearance 5 and volume 50, and three 100-unit doses as 2-hour infusions every 12 hours. For 50 patients with variability, add `n = 50` and an omega, for example `omega = c(0.2, 0.05, 0.2)` for the lower triangle of the matrix on CL and V.

The recipe's script `run_pkpdsim.R` uses library models only, sets the seed with `set.seed()` and writes two CSV files. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

`sim()` returns a long data frame with the columns `id`, `t`, `comp`, `y` and `obs_type`: one row per patient, time and compartment. With `only_obs = TRUE`, the recipe's choice, the rows are the observations only, which are the concentrations.

The documentation shows the first rows of a run with infusions: `y` is 0 at t = 0, rises during the infusion to 90.63462 at t = 2, and falls after it ends (74.20535 at t = 4). Those numbers come from the PKPDsim Simulation article.

In the recipe:

- `concentrations.csv` holds that table for all patients at 0.5-hour steps.
- `summary.csv` has one row per patient with `cmax` (the highest concentration seen), `tmax` (the time of it) and `auc` (area under the curve to the end time, by the trapezoid rule on the 0.5-hour grid).
- `run_log.txt` gives the model name, the number of individuals and the seed.

With a coefficient of variation above 0, the patients differ in CL and V, so `cmax` and `auc` vary between rows. Higher CL gives a lower AUC for the same dose.

## Pitfalls

- **Units are yours.** PKPDsim treats the numbers as given. Dose in mg and volume in L gives mg/L.
- **Power functions.** In custom model code write `pow(base, exp)`, not `^`. Write real numbers as `3.0`, to avoid integer arithmetic. The Model article lists these rules.
- **Custom models compile code.** `new_ode_model(code = ...)` builds a C++ function. A sandbox with a read-only or non-executable temporary directory cannot do this, which is why the recipe offers library models only.
- **Omega is a variance matrix.** `omega = c(0.2, 0.05, 0.2)` fills the lower triangle: variances 0.2 and a covariance 0.05. `cv_to_omega()` takes a CV on the standard-deviation scale and assumes no correlation.
- **Steady state is assumed, not checked.** With `ss = TRUE` PKPDsim assumes steady state after 5 days by default and does not test it.
- **Vector lengths.** If `amt` and `times` differ in length, the first `amt` is repeated.

## Further reading

- Documentation: https://insightrx.github.io/PKPDsim/
- Variability article: https://insightrx.github.io/PKPDsim/articles/variability.html
- Source: https://github.com/InsightRX/PKPDsim
- Citation: Keizer R, Hughes J, Tong D, Woo K, Brooks J. PKPDsim: Tools for Performing Pharmacokinetic-Pharmacodynamic Simulations. R package. https://doi.org/10.32614/CRAN.package.PKPDsim

---

Cite: Keizer R, Hughes J, Tong D, Woo K, Brooks J. PKPDsim: Tools for Performing Pharmacokinetic-Pharmacodynamic Simulations. R package. doi:10.32614/CRAN.package.PKPDsim

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pkpdsim).
