# epydemix

> Stochastic SIR or SEIR epidemic simulation in a well-mixed population, repeated over many runs with 5/50/95 percent bands per compartment.

Licence: GPL-3.0-or-later · [Source code](https://github.com/epistorm/epydemix)

## What it simulates

epydemix simulates an epidemic as a chain of random transitions between compartments such as S (susceptible), I (infectious) and R (recovered). Each simulated day, every compartment sends a random number of people to the next one. Repeating the run many times gives a spread of outcomes instead of a single curve.

The package also handles age groups, contact matrices, interventions and fitting to data (approximate Bayesian computation). The biosimhub example uses the simplest case: one well-mixed population and an SIR or SEIR model.

The key assumptions are random mixing and a fixed time step. In the 1.3.2 source, `run_simulations` takes `dt` in days with a default of 1. Transition probabilities are the rate times `dt`, and the people who move are drawn from a multinomial distribution. Rates stay constant over the run.

Input is a model, a start and end date and the number of runs. Output is a table of compartment sizes per day and per quantile.

## When to use it

- You want the range of outcomes of an outbreak, for example the 5th and 95th percentile of the peak size, in a population of 100,000.
- You want to compare R0, infectious period or latent period and see how the peak date moves.
- You plan to add age structure, interventions or calibration to data later.

[GillesPy2](gillespy2.md) on biosimhub fits when you need an exact event-by-event simulation of any reaction network, or when you want to choose the solver. [NetLogo](netlogo.md) Web (the Virus model) fits when you want individuals that move in space. Use the [webR](webr.md) page when you want SimInf or adaptivetau and an R workflow.

## Install it yourself

Pinned to 1.3.2 (conda-forge, checked with a micromamba dry run, 162 MB of downloads):

```
micromamba create -n epx -c conda-forge epydemix=1.3.2
micromamba activate epx
```

The project documents `pip install epydemix`, and `pip install epydemix[numba]` for a faster stochastic loop.

Minimal script with the Python API, an SIR model with a fixed seed (run in the recipe's 1.3.2 image):

```python
from epydemix import EpiModel

model = EpiModel(name="SIR", compartments=["S", "I", "R"], default_population_size=100000)
model.add_parameter("beta", 0.4)
model.add_parameter("gamma", 0.2)
model.add_transition("S", "I", params=("beta", "I"), kind="mediated")
model.add_transition("I", "R", params="gamma", kind="spontaneous")
res = model.run_simulations(start_date="2024-01-01", end_date="2024-04-10",
                            Nsim=20, percentage_in_agents=0.0005, rng=42)
q = res.get_quantiles_compartments(quantiles=[0.05, 0.5, 0.95])
```

This run gave a median of 13,143.5 infectious people on 2024-01-31 and 17.5 on 2024-04-10. The table `q` has 303 rows: 101 dates times 3 quantiles.

## Run the tested example

This recipe builds epydemix in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.8 s.

1. Download [epydemix-recipe.tar.gz](https://biosimhub.pages.dev/guides/epydemix/epydemix-recipe.tar.gz) (Dockerfile, driver.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf epydemix-recipe.tar.gz
   cd epydemix
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/epydemix:1.3.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/epydemix:1.3.2 python /opt/driver.py --model SIR --population 100000 \
    --r0 2 --infectious-days 5 --latent-days 3 \
    --days 120 --nsim 20 --initial-fraction 0.0005 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `compartments_quantiles.csv` | 23.8 KB |
| `run_log.txt` | 351 B |

<details><summary>First lines of <code>compartments_quantiles.csv</code></summary>

```
date,quantile,S_0,S_total,I_0,I_total,R_0,R_total
2020-01-01,0.05,99921.95,99921.95,53.95,53.95,5.0,5.0
2020-01-02,0.05,99894.75,99894.75,61.85,61.85,15.75,15.75
2020-01-03,0.05,99861.85,99861.85,68.85,68.85,26.75,26.75
2020-01-04,0.05,99812.75,99812.75,82.6,82.6,40.9,40.9
2020-01-05,0.05,99759.7,99759.7,98.95,98.95,57.95,57.95
2020-01-06,0.05,99687.95,99687.95,130.6,130.6,72.9,72.9
2020-01-07,0.05,99625.05,99625.05,154.0,154.0,96.85,96.85
2020-01-08,0.05,99532.7,99532.7,195.75,195.75,121.9,121.9
2020-01-09,0.05,99430.1,99430.1,239.0,239.0,161.9,161.9
2020-01-10,0.05,99272.4,99272.4,292.95,292.95,208.7,208.7
2020-01-11,0.05,99092.6,99092.6,367.55,367.55,258.55,258.55
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
SIR: 20 stochastic runs, N=100000, R0=2.0, seed=42
        date  quantile       S_0   S_total    I_0  I_total    R_0  R_total
0 2020-01-01      0.05  99921.95  99921.95  53.95    53.95   5.00     5.00
1 2020-01-02      0.05  99894.75  99894.75  61.85    61.85  15.75    15.75
2 2020-01-03      0.05  99861.85  99861.85  68.85    68.85  26.75    26.75
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--model` | Model | SIR | SIR, SEIR |
| `--population` | Population size | 100000 | 1000 to 5000000 |
| `--r0` | Basic reproduction number R0 | 2 | 0.1 to 20 |
| `--infectious-days` | Mean infectious period (days) | 5 | 0.5 to 60 |
| `--latent-days` | Mean latent period (days | 3 | 0.5 to 60 |
| `--days` | Simulation length (days) | 120 | 10 to 730 |
| `--nsim` | Stochastic runs | 20 | 1 to 200 |
| `--initial-fraction` | Initially infected fraction | 0.0005 | 1e-05 to 0.1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `driver.py` wraps the calls above. It sets `gamma = 1 / infectious_days` and `beta = R0 * gamma`. For SEIR it adds `sigma = 1 / latent_days` and an E compartment. It starts the run on 2020-01-01, runs `run_simulations` with `Nsim` runs and `percentage_in_agents` as the initial infected fraction, and passes your seed as `rng`. Then it calls `get_quantiles_compartments` for the 5th, 50th and 95th percentiles.

The example uses SIR, 100,000 people, R0 = 2, a 5 day infectious period, 120 days, 20 runs, 0.05 percent initially infected and seed 42.

- `run_log.txt`: `SIR: 20 stochastic runs, N=100000, R0=2.0, seed=42`, then the first three rows of the table.
- `compartments_quantiles.csv` (24,381 bytes): columns `date,quantile,S_0,S_total,I_0,I_total,R_0,R_total`. It has 363 rows: 121 dates times 3 quantiles. The `_0` columns are population group 0. With one group they equal the `_total` columns.

On 2020-01-01 the 5th percentile row reads S 99,921.95, I 53.95, R 5.0. The infectious count starts near 50 (0.05 percent of 100,000) and the first day's draws move it.

From the file, the median run peaks at 18,798 infectious on 2020-02-07, and the 5th to 95th percentile of the peak is 18,258 to 19,202. At day 120 the median has 84,514 recovered and 15,484 susceptible.

## Your own runs

Same image as the recipe and seed 42. Only the stated option changed.

**Raise R0 to 3** (`--r0 3`). The median peak rises to 33,481 infectious on 2020-01-23, 15 days earlier. At day 120 the median has 95,785 recovered.

**Switch to SEIR** (`--model SEIR`, latent period 3 days). The median peak falls to 11,349.5 on 2020-03-11, about 33 days later than SIR. The median at day 120 is 83,703 recovered. The table gains `E_0` and `E_total`.

**Go below the threshold** (`--r0 0.8`). There is no epidemic. The median infectious count is highest at the start, 48.5 on 2020-01-01, and the median ends with 353.5 recovered.

## Pitfalls

- **Daily time step.** The recipe's driver uses the default of 1 day, so a fast epidemic overshoots. At R0 = 2 the classical final-size equation gives 79.7 percent infected. The example run gives 84.5 percent. A script with `dt=0.1` gave 80,182 recovered (80.2 percent). Use a smaller `dt` in your own script.
- **Percentiles per day.** The 5th, 50th and 95th percentiles are taken separately for each day and compartment. The 95th percentile curve mixes days from different runs.
- **Seed placement.** Pass `rng=seed` to `run_simulations`. A rerun with seed 42 reproduced the first row above exactly (S 99,921.95 at the 5th percentile).
- **One population.** The recipe's driver uses one group. Age structure and contact matrices need your own script and population data.
- **Date columns.** Dates start at 2020-01-01 in the recipe's driver. Set `start_date` yourself to match real data.

## Further reading

- Documentation: https://epydemix.readthedocs.io/en/latest/
- Tutorial 1, model definition and simulation: https://github.com/epistorm/epydemix/blob/main/tutorials/01_Model_Definition_and_Simulation.ipynb
- Source: https://github.com/epistorm/epydemix
- Paper: Gozzi N et al. (2025), PLoS Comput Biol 21:e1013735, https://doi.org/10.1371/journal.pcbi.1013735

---

Cite: Gozzi N, Chinazzi M, Davis N, Gioannini C, Rossi L, Ajelli M, Perra N, Vespignani A (2025). Epydemix. PLoS Comput Biol 21:e1013735. doi:10.1371/journal.pcbi.1013735

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/epydemix).
