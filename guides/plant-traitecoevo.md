# plant

> Simulate a size-structured stand of plants competing for light under a disturbance regime, using the FF16 trait-based growth model.

Licence: AGPL-3.0-or-later · [Source code](https://github.com/traitecoevo/plant)

## What it simulates

plant is an R package for size-structured and trait-structured models of forest stands. Plants of one or more species grow, reproduce and die, and they compete for light. Growth, fecundity and mortality depend on a plant's size and on its traits, such as leaf mass per area (LMA) or wood density. The core routines are C++ behind R6 classes.

The default physiology is the FF16 strategy (Falster et al. 2011). Individuals have state variables for height, mortality, fecundity, heartwood area and heartwood mass. Light is shared: taller plants shade shorter ones, and leaf area index drives the canopy openness that each height experiences.

The package works at three levels:

- **Individuals** grown in a fixed environment, for example `grow_plant_to_time()`.
- **Patches** of competing plants, solved by the "characteristic" method (`run_scm_collect()`) that steps cohorts through time. Patches are disturbed at random, controlled by the mean disturbance interval.
- **Metapopulations**, where many patches of different ages are averaged to give seed rain, demographic equilibrium and invasion fitness for a trait value.

The model is deterministic in the characteristic method. A stochastic, finite-sized population method also exists in the package.

## When to use it

Use plant to study how traits shape forest structure and competition, to find the trait values that survive in a given disturbance regime, or to model evolution of traits with adaptive dynamics.

- [NetLogo](netlogo.md) suits agent-based ecology models that you build yourself.
- [SLiM](slim.md) simulates genetic evolution of individuals, not their growth and competition.
- [AlphaSimR](alphasimr.md) simulates quantitative-trait change in breeding programs.

## Install

plant is not on CRAN or conda. The latest tagged release is v2.0.0 (25 February 2021). The develop branch is version 2.0.0.9002 and requires R 4.5.0 or later. The repository is AGPL-3.0.

```r
install.packages("remotes")
remotes::install_github("traitecoevo/plant")
```

This follows the README, with the develop branch. The package's DESCRIPTION lists two GitHub dependencies, `odelia` and `phylloptim`, under `Remotes`, and `install_github` fetches them. A C++ compiler is required. To pin a version, add the commit after an `@`, as in `traitecoevo/plant@bd09645dec0f6d1850ffa96298dda1af6b295e07`, the commit also published on traitecoevo.r-universe.dev. For the old release use `ref = "v2.0.0"`.

## Run the tested example

This recipe builds plant in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.9 s.

1. Download [plant-traitecoevo-recipe.tar.gz](https://biosimhub.pages.dev/guides/plant-traitecoevo/plant-traitecoevo-recipe.tar.gz) (Dockerfile, run_plant.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf plant-traitecoevo-recipe.tar.gz
   cd plant-traitecoevo
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/plant-traitecoevo:2.0.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/plant-traitecoevo:2.0.0 Rscript /opt/run_plant.R 0.0825 30 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `patch_summary.csv` | 7.7 KB |
| `run_log.txt` | 97 B |

<details><summary>First lines of <code>patch_summary.csv</code></summary>

```
"time","max_height","n_cohorts","canopy_openness_ground"
0,0.392045781307038,1,1
1e-05,0.392050991523277,2,0.999999999084972
2e-05,0.392056201785904,3,0.999999998169905
3e-05,0.39206141209492,4,0.999999997254798
4e-05,0.392066622450325,5,0.999999996339651
5e-05,0.392071832852119,6,0.999999995424465
6e-05,0.392077043300302,7,0.999999994509239
7e-05,0.392082253794873,8,0.999999993593973
8e-05,0.392087464335834,9,0.999999992678668
9.52587890625e-05,0.392095415079771,10,0.999999991281946
0.000110517578125,0.392103365931716,11,0.999999989885132
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
lma 0.0825, disturbance interval 30.0 years: 142 solver steps, final time 105.3, seed rain 19.82
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `lma` | Leaf mass per area (kg/m2) | 0.0825 | 0.03 to 0.5 |
| `interval` | Mean disturbance interval (years) | 30 | 5 to 200 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Patch-level dynamics article: https://traitecoevo.github.io/plant/articles/patch.html. One species in one patch, with a mean disturbance interval of 30 years:

```r
library(plant)
params <- scm_base_parameters("FF16")
params$disturbance_mean_interval <- 30.0
patch <- expand_parameters(trait_matrix(0.0825, "lma"), params, mutant = FALSE)
result <- run_scm_collect(patch)
```

`trait_matrix(0.0825, "lma")` sets the LMA of the species. The recipe pins the v2.0.0 release, because the develop branch changed `expand_parameters()` and `run_scm_collect()` since this article; it also installs the `loggr` package from GitHub, which v2.0.0 needs. The recipe's script `run_plant.R` runs this, then writes a summary of height, number of cohorts and ground-level canopy openness over time. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

`result` is a list with the entries `time`, `species`, `env`, `seed_rain`, `patch_density` and `p`.

- `time` is the solver's time points. The article shows 142 steps for this example, unevenly spaced: half of them fall in the first year, because early development needs fine resolution.
- `species[[1]]` is a three-dimensional array of variable, time step and cohort. The article gets heights with `result$species[[1]]["height", , ]`, a matrix of 142 time steps by 141 cohorts. A cohort has `NA` before it is introduced.
- `env` holds the light environment at each step as a spline of canopy openness against height.
- `seed_rain` is the seed output of the patch over its development.

In the recipe, `patch_summary.csv` has the columns `time`, `max_height`, `n_cohorts` and `canopy_openness_ground`. Height of the tallest cohort rises with time. The ground canopy openness falls as the canopy closes. The article describes waves in it from rounds of recruitment and self-thinning. `run_log.txt` gives the number of solver steps and the seed rain.

## Pitfalls

- **Time points are not even.** Do not average over steps. Interpolate onto your own grid first.
- **Cohorts appear over time.** Arrays are padded with `NA` for cohorts that do not exist yet or have no data. Use `na.rm = TRUE`.
- **Individuals are reference objects.** Assigning `indv2 <- indv` does not copy it, and changes to one show in the other. Use `clone()` to copy.
- **Disturbance interval matters.** The mean disturbance interval sets how long a patch develops before it is cleared, so it changes the whole summary table.
- **The develop branch moves.** Documentation at traitecoevo.github.io/plant describes version 2.0.0.9002. Pin a commit for repeatable runs.
- **Solver tolerances.** Control settings such as `ode_tol_rel` are in the strategy object, and changing them changes the result slightly.

## Further reading

- Documentation: https://traitecoevo.github.io/plant/
- Individuals article: https://traitecoevo.github.io/plant/articles/individuals.html
- Source: https://github.com/traitecoevo/plant
- Paper: Falster DS, FitzJohn RG, Brännström Å, Dieckmann U, Westoby M (2016). plant: A package for modelling forest trait ecology and evolution. Methods in Ecology and Evolution 7:136-146. https://doi.org/10.1111/2041-210X.12525

---

Cite: Falster DS, FitzJohn RG, Brannstrom A, Dieckmann U, Westoby M (2016). plant: A package for modelling forest trait ecology and evolution. Methods Ecol Evol 7:136-146. doi:10.1111/2041-210X.12525

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/plant-traitecoevo).
