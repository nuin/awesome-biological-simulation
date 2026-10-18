# rxode2

> Solve an ODE-based pharmacokinetic or pharmacodynamic model from the rxode2 mini-language for a repeated-dose regimen.

Licence: GPL-3.0-or-later · [Source code](https://github.com/nlmixr2/rxode2)

## What it simulates

rxode2 is an R package for solving and simulating ordinary differential equation (ODE) models. It was written for pharmacometrics, the modelling of how drugs move through the body (pharmacokinetics, PK) and what they do (pharmacodynamics, PD). It also works for any ODE system. It is the simulation engine of nlmixr2.

You write the model in a short mini-language: one `d/dt(compartment) = ...` line per state, with ordinary assignments for derived quantities. rxode2 translates the text to C, compiles it into a shared library and loads it, so the solve is fast. A dosing and sampling schedule is an event table, built with `et()`. `rxSolve()` then solves the model for that schedule and returns a data frame.

A model can include covariates that change over time, lag times, bioavailability, rate and duration of infusions, and between-subject variability when you simulate many subjects. Single-subject runs are the simple case. Multi-subject runs can use several threads.

## When to use it

Use rxode2 for dose-regimen questions on a compartmental model: concentration after repeated oral doses, steady-state peaks and troughs, or an effect compartment driven by concentration.

- Use [BioGears](biogears.md) when you want a whole-body physiology engine with built-in organ models and scenario files, and not equations you write.
- Use [XPPAUT](xppaut.md) when you want to explore an ODE system as a dynamical system, with phase planes and bifurcations.
- Use [GillesPy2](gillespy2.md) when the system is a small reaction network and discrete molecule counts matter.

The README compares rxode2 with mrgsolve, dMod and PKPDsim, other R packages for pharmacometric ODE models. It notes that rxode2 can solve several subjects in parallel and supports symbolic manipulation of the ODE system, which mrgsolve does not.

## Install

From R, the README gives:

```r
install.packages("rxode2")
```

CRAN has version 5.1.8 (published 13 October 2026), and the GitHub release v5.1.8 carries the same date. The README says that building models needs a working C compiler, and that OpenMP support is needed for threaded solving. On Linux it asks for gcc with OpenMP and gfortran, plus system libraries such as udunits and the symengine dependencies. `pkgbuild::has_build_tools(debug = TRUE)` checks the toolchain.

conda-forge also has the package:

```bash
micromamba create -n rx -c conda-forge r-base=4.5 r-rxode2=5.0.2 gxx_linux-64=14 gfortran_linux-64=14 make
```

The conda package `r-rxode2` is at 5.0.2 for linux-64, osx-64 and win-64, and it needs R 4.4 or 4.5. There is no linux-aarch64 build, so the recipe pins `linux/amd64`. conda-forge's R package does not pull in a compiler, so the command adds the conda compilers. The licence is GPL-3.0-or-later. The recipe installs the unmodified package.

## A first run

Adapted from the README, https://github.com/nlmixr2/rxode2. It defines a two-compartment oral PK model with a turnover effect, builds a dosing schedule, and solves.

```r
library(rxode2)

mod1 <- function() {
  ini({
    # central
    KA=2.94E-01
    CL=1.86E+01
    V2=4.02E+01
    # peripheral
    Q=1.05E+01
    V3=2.97E+02
    # effects
    Kin=1
    Kout=1
    EC50=200
  })
  model({
    C2 <- centr/V2
    C3 <- peri/V3
    d/dt(depot) <- -KA*depot
    d/dt(centr) <- KA*depot - CL*C2 - Q*C2 + Q*C3
    d/dt(peri)  <- Q*C2 - Q*C3
    eff(0) <- 1
    d/dt(eff)   <- Kin - Kout*(1-C2/(EC50+C2))*eff
  })
}

ev <- et(amountUnits="mg", timeUnits="hours") |>
  et(amt=10000, addl=9, ii=12, cmt="depot") |>
  et(0:240)

x <- mod1 |> rxSolve(ev)
```

The README prints the first rows of the result. At time 0 the depot holds 10000 and C2 is 0. At hour 1, C2 is 44.4 and the depot holds 7453. At hour 2, C2 is 54.9. At hour 3, C2 is 51.9. Those numbers come from the README output, which also adds a second dosing series later in the run.

The recipe's helper writes the same model in the older text form (a string of `d/dt(...)` lines) and builds the schedule from the dose, interval, extra doses and end time you set.

## Run the tested example

This recipe builds rxode2 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 9.1 s. rxode2 has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [rxode2-recipe.tar.gz](https://biosimhub.pages.dev/guides/rxode2/rxode2-recipe.tar.gz) (Dockerfile, run.sh, run_rxode2.R, example model.txt, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf rxode2-recipe.tar.gz
   cd rxode2
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/rxode2:5.0.2 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/rxode2:5.0.2 /usr/local/bin/run-rxode2 /work/in/model.txt 10000 12 9 120 depot > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 87 B |
| `solve.csv` | 12.3 KB |
| `summary.txt` | 247 B |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
rxode2 5.0.2
rows 121 columns 7
dose 10000 mg into depot every 12 h, 10 doses in total
```

</details>

<details><summary>First lines of <code>solve.csv</code></summary>

```
"time","C2","C3","depot","centr","peri","eff"
0,0,0,10000,0,0,1
1,44.375547639462,0.919829801210995,7452.76491439837,1783.89701510637,273.189450959666,1.08466445642686
2,54.8829562013207,2.67298249826682,5554.37048662528,2206.29483929309,793.875801985246,1.18082493841928
3,51.9034259213792,4.45649274281692,4139.54174691901,2086.51772203944,1323.57834461663,1.22891364788605
4,44.497380502615,5.98070759004021,3085.1031468085,1788.79469620512,1776.27015424194,1.23460966242575
5,36.4843405394273,7.17749806448426,2299.25484630497,1466.67048968498,2131.71692515183,1.21474234371457
6,29.3073813654877,8.06677193800771,1713.58057882398,1178.1567308926,2395.83126558829,1.18397585439958
7,23.3703506167326,8.6971745618648,1277.09131603095,939.48809479265,2583.06084487385,1.15167951616674
8,18.652832935688,9.12112261321701,951.786131154339,749.843884014658,2708.97341612545,1.12256131591103
9,14.9858055069769,9.38540054036779,709.343824224717,602.429381380471,2787.46396048923,1.09829545876089
10,12.1696908595163,9.52855510165092,528.657313557134,489.221572552557,2829.98086519032,1.0789500137777
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
rxode2 5.0.2
rows 121 columns 7
dose 10000 mg into depot every 12 h, 10 doses in total
time min 0 max 120
C2 min 0 max 71.6315
C3 min 0 max 42.6524
depot min 302.519 max 10302.5
centr min 0 max 2879.59
peri min 0 max 12667.8
eff min 1 max 1.31343
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `amt` | Dose amount (mg) | 10000 | 0.001 to 1000000000 |
| `ii` | Dosing interval (hours) | 12 | 0.1 to 1000 |
| `addl` | Additional doses | 9 | 0 to 200 |
| `tend` | Last sampling time (hours) | 120 | 1 to 2000 |
| `cmt` | Compartment that receives the dose | depot | text |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_rxode2.R` compiles the model, solves it for the schedule and writes three files.

- `solve.csv` is the solved table: a `time` column, then the model's compartments and the derived values it defines. For the example, that is `C2`, `C3`, `depot`, `centr`, `peri` and `eff`, one row per hour from 0 to the last sampling time.
- `summary.txt` has the rxode2 version, the row and column counts, the dose description and the minimum and maximum of each numeric column.
- `run_log.txt` has the first three of those lines.

The units of the columns are the ones your equations imply. Plot `C2` against `time` in R or a spreadsheet. With repeated doses it rises and falls with each dose, and the README plots `C2` and `eff` against time.

## Pitfalls

- **The first run compiles.** The README output shows steps such as creating an include directory and precompiling headers. A first solve takes longer than later ones, and every new model is compiled.
- **A compiler must exist where the model runs.** In a locked-down container the temporary directory may not allow loading compiled code. The recipe points `TMPDIR` at the working directory for that reason.
- **Compartment names must match.** The dose goes to the compartment you name (`depot` here). A name the model does not define is an error.
- **Parameters written in the model are constants.** To vary them, pass `params=` to `rxSolve`. The vignettes cover between-subject variability and covariates.
- **Time units are labels.** `timeUnits="hours"` labels plots. The equations use whatever time unit your rates assume.
- **Stiff systems.** The package has a vignette on stiff models and solver choice.

## Further reading

- Repository and README: https://github.com/nlmixr2/rxode2
- Documentation: https://nlmixr2.github.io/rxode2/
- CRAN package: https://cran.r-project.org/package=rxode2
- Paper: Wang W, Hallow KM, James DA (2016). A tutorial on RxODE: simulating differential equation pharmacometric models in R. CPT: Pharmacometrics and Systems Pharmacology 5:3-10. https://doi.org/10.1002/psp4.12052

---

Cite: Wang W, Hallow KM, James DA (2016). A tutorial on RxODE: simulating differential equation pharmacometric models in R. CPT Pharmacometrics Syst Pharmacol 5:3-10. doi:10.1002/psp4.12052

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/rxode2).
