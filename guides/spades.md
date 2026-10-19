# SpaDES

> Run a SpaDES.core discrete-event simulation of forest ageing and fire spread on a raster, and write yearly fire statistics and the final age map.

Licence: GPL-3.0 · [Source code](https://github.com/PredictiveEcology/SpaDES)

## What it simulates

SpaDES is an R framework for spatial discrete-event simulation. It does not model one system itself. You write modules, each with events (such as init, grow, fire, stats) and the objects they read and write. SpaDES.core keeps an event queue sorted by time and priority, runs the next event, and lets each event schedule later ones.

The recipe runs one module, `forestFire`, written for this page. A raster of forest stands starts with random ages. Each year every stand ages by one year. Every `return interval` years a set of fires ignites at random cells and spreads to neighbouring cells. The chance of spreading into a stand rises linearly from a minimum for a stand just burned to a maximum for a stand at the maximum age. Burned stands reset to age 0.

The run uses SpaDES.core 3.2.1 and SpaDES.tools 2.1.3, whose `spread` function does the percolation.

## When to use it

- You build a landscape model out of reusable modules (vegetation, fire, wildlife) that share a raster and need an event scheduler.
- You want to see how fire size and stand age change with the spread probability, the fire return interval and the number of ignitions.
- You want a worked, small module to copy before writing your own.

Use [NetLogo](netlogo.md) for agent-based models with a built-in viewer. SpaDES suits R users who need caching, module reuse and raster data. The recipe's module is a teaching model with no calibration to real forests.

## Install it yourself

The `SpaDES` metapackage was archived on CRAN on 2026-07-13 because it requires the archived package `reproducible`. SpaDES.core and SpaDES.tools are installed separately. The recipe installs R 4.4 from conda-forge and the packages from CRAN source (this compiles `Rcpp` code and takes a few minutes):

```r
install.packages(c("SpaDES.core", "SpaDES.tools"))
```

A module is a folder containing `<name>.R` with `defineModule()` and a `doEvent.<name>()` function. The recipe's `forestFire.R` is 74 lines and is included in the download.

## Run the tested example

This recipe builds SpaDES in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 5.4 s.

1. Download [spades-recipe.tar.gz](https://biosimhub.pages.dev/guides/spades/spades-recipe.tar.gz) (Dockerfile, forestFire.R, run_spades.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf spades-recipe.tar.gz
   cd spades
   sh run.sh
   ```

![Terminal recording of the SpaDES example run](https://biosimhub.pages.dev/media/spades/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/spades:3.2.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/spades:3.2.1 Rscript /opt/run_spades.R 100 100 5 5 0.05 0.3 100 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `final_age.csv` | 30.8 KB |
| `fire_stats.csv` | 2.3 KB |
| `run_log.txt` | 238 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/spades/result-dark.png"><img src="https://biosimhub.pages.dev/media/spades/result.png" alt="Plot of the SpaDES example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>final_age.csv</code></summary>

```
25,146,25,25,25,25,136,25,25,25,25,188,126,25,25,25,104,183,133,25,25,25,25,25,5,25,25,114,25,25,25,25,75,75,117,75,75,103,30,149,30,30,30,30,30,30,105,101,102,120,101,157,109,139,104,132,148,199,172,
137,25,25,25,25,172,25,25,25,25,25,25,25,25,25,25,162,25,25,25,25,25,142,25,5,5,25,25,25,25,25,25,75,75,75,75,75,133,30,30,159,30,30,30,30,30,30,123,197,124,191,160,161,113,133,165,194,131,126,55,55,1
25,25,25,25,25,112,25,25,25,25,25,25,136,25,25,169,115,109,25,25,124,25,25,25,25,25,25,25,25,188,75,25,25,75,75,121,75,75,30,30,30,30,30,30,30,30,30,30,133,124,164,113,148,110,127,117,154,55,55,55,55,
25,25,25,25,25,25,25,25,25,25,25,25,25,123,25,25,119,174,25,25,25,25,25,25,25,25,25,25,25,106,75,75,25,75,75,112,129,75,30,30,30,132,30,30,30,30,30,30,30,181,124,75,75,75,178,145,102,75,55,55,141,197,
164,25,25,25,175,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,194,162,117,75,75,139,75,75,75,75,30,30,30,30,30,30,30,30,30,30,30,75,126,75,179,75,75,75,75,75,75,55,55,55,100,110,5
25,142,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,25,113,25,25,25,25,25,115,25,25,25,171,75,75,75,109,75,30,75,30,30,30,30,30,30,75,30,30,30,198,75,75,75,147,107,195,75,75,75,75,55,45,104,55,55
```

</details>

<details><summary>First lines of <code>fire_stats.csv</code></summary>

```
"year","burned_cells","burned_fraction","mean_age","old_fraction"
1,0,0,50.8878,0.5125
2,0,0,51.8878,0.5236
3,0,0,52.8878,0.5339
4,0,0,53.8878,0.5432
5,69,0.0069,54.4368,0.5477
6,0,0,55.4368,0.5585
7,0,0,56.4368,0.5686
8,0,0,57.4368,0.5796
9,0,0,58.4368,0.5911
10,88,0.0088,58.8689,0.5933
11,0,0,59.8689,0.6024
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
[1] TRUE
SpaDES.core 3.2.1, forestFire module, 100 x 100 cells, 100 years, seed 42
fire events: 20, burned cells total: 9080, largest event: 1683 cells (16.8 percent)
final mean age 65.9 years, 64.8 percent of cells at least 50 years old
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `size` | Grid side (cells) | 100 | 20 to 300 |
| `years` | Simulated years | 100 | 10 to 500 |
| `n_fires` | Ignitions per fire event | 5 | 1 to 100 |
| `return_interval` | Years between fire events | 5 | 1 to 50 |
| `spread_min` | Spread probability into a young stand | 0.05 | 0.01 to 0.6 |
| `spread_max` | Spread probability into a stand at the maximum age | 0.3 | 0.01 to 0.6 |
| `max_age` | Age at which flammability stops rising (years) | 100 | 10 to 300 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `run_spades.R` copies the module to a scratch folder, calls `simInit()` with your parameters, runs `spades()` and writes three files. The run uses a seed set before `simInit`.

The example uses a 100 x 100 grid, 100 years, 5 ignitions every 5 years, spread probability 0.05 for young stands and 0.3 at age 100, and seed 42. It took 5.4 seconds.

- `run_log.txt` holds the summary: 20 fire events burned 9,080 cells in total (the grid has 10,000). The largest event burned 1,683 cells, 16.8 percent of the grid. At year 100 the mean stand age is 65.9 years and 64.8 percent of cells are at least 50 years old.
- `fire_stats.csv` has one row per year (100 rows) with `year, burned_cells, burned_fraction, mean_age, old_fraction`. The first fire is at year 5 and burned 69 cells. Later fires burned 88 cells (year 10), 665 (year 20), 1,683 (year 45), 1,235 (year 60) and 194 (year 100). Years without a fire show 0.
- `final_age.csv` is a 100 x 100 matrix of stand ages at year 100, with no header. Cells at 25 burned at year 75, and cells at 5 burned at year 95.

Initial ages are random between 0 and 100, so the mean age at year 1 is 50.9. Fire sizes grow with time as stands age and become more flammable: the events before year 20 burned 23 to 88 cells, and those after year 40 burned up to 1,683.

## Your own runs

Same image and settings as the example, with one change each.

- **Higher maximum spread** (`spread_max 0.5`). One fire burned 7,520 cells (75.2 percent), the total burned was 22,955 cells and the final mean age fell to 23.4 years.
- **Lower maximum spread** (`spread_max 0.15`). Fires stayed small: 663 cells burned in total, the largest event was 129 cells, and the mean age rose to 142.6 years.
- **Rarer fires** (`return_interval 20`). Only 5 events, but the largest burned 5,216 cells (52.2 percent).
- **More ignitions** (`n_fires 20`). 12,382 cells burned in total, and the largest event was 888 cells (8.9 percent).
- **Another seed** (`seed 43`). 10,197 cells burned and the largest event was 1,527 cells, against 9,080 and 1,683 with seed 42.
- **Larger grid and run** (200 x 200 cells, 200 years). 40 events burned 69,631 cells, and the largest was 9,447 cells (23.6 percent of 40,000).

Two runs with the example settings gave identical `fire_stats.csv` files.

## Pitfalls

- **The `SpaDES` metapackage is not installable from CRAN.** Install `SpaDES.core` and `SpaDES.tools` directly.
- **Sample module `fireSpread` in SpaDES.core 3.2.1.** In a 20-year test with `returnInterval` 10, its burn event ran once, at the start time 0, and never again. With `startTime` 1 in a 5-year test it did not run at all. For that reason the recipe ships its own module.
- **Stand ages are not capped.** `max_age` only sets where flammability stops rising. Mean ages can pass it, as in the 142.6-year run.
- **Spread probability must make sense.** If `spread_min` is larger than `spread_max`, flammability falls with age. The recipe does not block this.
- **No network.** With default options, an offline SpaDES run printed a failed CRAN download warning and a note from the `Require` package installer. The recipe sets `spades.useRequire = FALSE`, which removes both.

## Further reading

- SpaDES.core on CRAN: https://CRAN.R-project.org/package=SpaDES.core
- Project site and wiki: https://spades.predictiveecology.org
- Source: https://github.com/PredictiveEcology/SpaDES
- Paper: McIntire EJB et al. (2022) PERFICT: A re-imagined foundation for predictive ecology. Ecology Letters 25:1345-1351. https://doi.org/10.1111/ele.13994

---

Cite: McIntire EJB, Chubaty AM, Cumming SG, et al. (2022). PERFICT: A re-imagined foundation for predictive ecology. Ecology Letters 25:1345-1351. doi:10.1111/ele.13994

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/spades).
