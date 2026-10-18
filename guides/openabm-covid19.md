# OpenABM-Covid19

> Age-stratified agent-based SARS-CoV-2 epidemic on household, workplace and random contact networks, with optional lockdown and app-based contact tracing.

Licence: GPL-3.0 · [Source code](https://github.com/BDI-pathogens/OpenABM-Covid19)

## What it simulates

OpenABM-Covid19 simulates a SARS-CoV-2 epidemic in a population of individual people. Each person has an age, a household and a set of daily contacts at work or school and at random. The model runs in one-day steps. Infected people pass through presymptomatic, asymptomatic or symptomatic stages, and some are hospitalised, go to intensive care, recover or die. The probability of each step depends on age.

Contacts come from three networks: household, occupation (age-specific) and random. Interventions act on those networks: lockdown scales the contacts down, and testing with digital or manual contact tracing quarantines contacts of known cases. The core is C with a Python (SWIG) interface. The biosimhub example uses the Python interface and the model's default parameters, a UK-like age structure.

The key assumptions are a closed population, no vaccination in this example, and one virus strain. Transmission between two people depends on the infectious rate and on the type of contact.

## When to use it

- You want to see how an outbreak develops in an age-structured population, with hospital and death counts by age.
- You want to compare interventions on the same population and seed: lockdown timing, testing and app-based tracing.
- You want an individual-level model whose networks you can change in Python.

[epydemix](epydemix.md) fits when age groups and a contact matrix are enough. [PyRoss](pyross.md) fits when you need an ODE or fast stochastic model of age groups and later want to fit it to data.

## Install it yourself

OpenABM-Covid19 is not on PyPI. It builds from source with a C compiler, the GNU Scientific Library (GSL) and SWIG. The recipe's image builds commit 367a0d3 on Python 3.10 (Debian bookworm, numpy 1.26.4, pandas 2.2.2). Three details from that build:

- Run SWIG with `-module covid19`, from inside `src`: `swig -python -module covid19 covid19.i`. The interface file at this commit names the module `OpenABMCovid19`, which does not match `setup.py`.
- Install `libc6-dev` next to gcc. On Debian, `gsl-config --cflags` returns `-I/usr/include`, which makes gcc fail with "stdlib.h: No such file or directory". The recipe removes that flag from `setup.py` before `pip install --no-deps .`.
- The package pins matplotlib 3.2.2, which does not build on Python 3.10. The recipe installs with `--no-deps` and adds click and tqdm itself.

Minimal script with a fixed seed:

```python
import COVID19.model as abm

model = abm.Model(params={"n_total": 10000, "end_time": 30, "rng_seed": 1})
model.run(verbose=False)
r = model.results
print(len(r), r["total_infected"].iloc[-1], r["n_symptoms"].iloc[-1])
```

In the recipe's image this printed `30 3176 922` on two runs in a row: 30 days, 3176 people ever infected and 922 symptomatic on day 30. `model.results` is a pandas table with one row per day and 70 columns.

## Run the tested example

This recipe builds OpenABM-Covid19 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 1.4 s.

1. Download [openabm-covid19-recipe.tar.gz](https://biosimhub.pages.dev/guides/openabm-covid19/openabm-covid19-recipe.tar.gz) (Dockerfile, driver.py, fix_setup.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf openabm-covid19-recipe.tar.gz
   cd openabm-covid19
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/openabm-covid19:367a0d3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/openabm-covid19:367a0d3 python /opt/driver.py --population 20000 --days 100 \
    --seed-infections 10 --infectious-rate 5.8 \
    --lockdown-start 0 --lockdown-days 30 --app-uptake 0 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `by_age.csv` | 198 B |
| `run_log.txt` | 183 B |
| `timeseries.csv` | 4.2 KB |

<details><summary>First lines of <code>by_age.csv</code></summary>

```
age_group,total_infected,total_case,total_death
0-9,1487,0,0
10-19,1962,0,0
20-29,2400,0,0
30-39,2425,5,1
40-49,2339,33,4
50-59,2438,71,6
60-69,2011,102,32
70-79,1384,101,55
80+,780,74,81
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
OpenABM-Covid19: N=20000, 100 days, seed=42, infectious_rate=5.8
infected 17226 (86.1%), cases 386, deaths 179
peak symptomatic 5699 on day 45, peak hospital 140, peak quarantined 49
```

</details>

<details><summary>First lines of <code>timeseries.csv</code></summary>

```
time,total_infected,total_case,total_death,n_presymptom,n_symptoms,n_hospital,n_critical,n_recovered,n_quarantine,R_inst
1,10,0,0,6,1,0,0,0,0,-1.000
2,10,0,0,5,2,0,0,0,0,-1.000
3,13,0,0,5,3,0,0,0,0,-1.000
4,21,0,0,10,3,0,0,0,0,4.806
5,30,0,0,13,4,0,0,0,0,4.288
6,42,0,0,19,6,0,0,0,0,5.249
7,52,0,0,28,6,0,0,0,0,3.564
8,63,0,0,30,10,0,0,1,0,2.826
9,86,0,0,46,12,0,0,1,0,4.274
10,110,0,0,59,16,0,0,1,0,3.419
11,130,0,0,70,22,0,0,1,0,2.311
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--population` | Population size | 20000 | 1000 to 100000 |
| `--days` | Simulation length (days) | 100 | 10 to 200 |
| `--seed-infections` | Initially infected people | 10 | 1 to 500 |
| `--infectious-rate` | Infectious rate (transmission per contact scale) | 5.8 | 1 to 10 |
| `--lockdown-start` | Lockdown start day (0 = no lockdown) | 0 | 0 to 200 |
| `--lockdown-days` | Lockdown length (days) | 30 | 1 to 200 |
| `--app-uptake` | Tracing app uptake in every age group (0 = no testing or tracing) | 0 | 0 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `driver.py` builds the model from your options and writes two tables. The example uses 20,000 people, 10 initial infections, infectious rate 5.8, 100 days, no lockdown, no tracing and seed 42. It ran in 4.8 s.

- `run_log.txt` (183 bytes): `infected 17226 (86.1%), cases 386, deaths 179`, then `peak symptomatic 5699 on day 45, peak hospital 140, peak quarantined 49`.
- `timeseries.csv` (4,259 bytes): one row per day with the total infected, cases, deaths, and the number presymptomatic, symptomatic, in hospital, in intensive care, recovered and quarantined. `R_inst` is the instantaneous reproduction number. It is -1 on days without a defined value, such as the first three days and the days after the epidemic has ended.
- `by_age.csv` (198 bytes): totals for nine age groups.

With no intervention the epidemic reaches 86.1 percent of the population. The number of ever-infected people was 10 on day 1, 859 on day 20, 5225 on day 30 and 13,296 on day 40. `R_inst` was 3.42 on day 10 and 0.82 on day 40, below 1 once most people are immune.

The 179 deaths are 1.04 percent of the 17,226 infected. By age they rise steeply: 0 deaths in under 30s, 4 among 2339 infected aged 40-49, 32 among 2011 aged 60-69 and 81 among 780 aged 80 and over. `total_case` counts people with a recorded case, which here is mostly hospital diagnosis because testing is off. It is 386, far below the number infected.

## Your own runs

Same image as the recipe, 20,000 people, 100 days and seed 42 unless noted.

- **Lockdown from day 20 to day 50** (`--lockdown-start 20 --lockdown-days 30`). Total infected fell from 17,226 to 16,235 (81.2 percent). The peak of symptomatic people fell from 5699 to 3352 and moved from day 45 to day 72. Lockdown delayed the epidemic and flattened it, but did not stop it.
- **Testing and tracing app with 80 percent uptake** (`--app-uptake 0.8`). Total infected was 16,617 (83.1 percent), recorded cases rose from 386 to 7359 and the peak number in quarantine rose from 49 to 3659. At 80 percent uptake with these default settings, tracing alone did not stop the epidemic.
- **Lower infectious rate** (`--infectious-rate 3.5`). 12,844 people (64.2 percent) were infected, the peak symptomatic count was 2921 on day 62, and `R_inst` on day 10 was 1.41 instead of 3.42.
- **Another seed** (`--seed 43`). 17,344 infected and 188 deaths, with a peak of 5831 on day 56 instead of day 45. Early growth differs by chance, so one seed shifts the timing by about 11 days.
- **A larger population** (`--population 50000`). 85.7 percent infected and 443 deaths. A run with 100,000 people and 200 days took about 18 s.

## Pitfalls

- **Seeds.** Pass `rng_seed`. The same seed gave identical output on every run here.
- **Small populations.** With 10 initial infections in 20,000 people, the first days are noisy. Use 50,000 or more, and several seeds, for the timing of the peak.
- **The infectious rate is not R0.** The model reports `R_inst` over time. Check it before comparing runs.
- **Interventions have many switches.** The recipe turns on testing on symptoms, tracing and quarantine of traced contacts together and sets the app uptake for every age group. Other options, such as manual tracing and household quarantine, are in the parameter list.
- **Days count from 1.** The first row of `timeseries.csv` is day 1.

## Further reading

- Model description: https://github.com/BDI-pathogens/OpenABM-Covid19/blob/master/documentation/covid19.md
- Parameter dictionary: https://github.com/BDI-pathogens/OpenABM-Covid19/blob/master/documentation/parameters/parameter_dictionary.md
- Source: https://github.com/BDI-pathogens/OpenABM-Covid19
- Paper: Hinch R et al. (2021) OpenABM-Covid19: an agent-based model for non-pharmaceutical interventions against COVID-19 including contact tracing. PLoS Comput Biol 17:e1009146. https://doi.org/10.1371/journal.pcbi.1009146

---

Cite: Hinch R, Probert WJM, Nurtay A, et al. (2021). OpenABM-Covid19: An agent-based model for non-pharmaceutical interventions against COVID-19 including contact tracing. PLoS Comput Biol 17(7):e1009146. doi:10.1371/journal.pcbi.1009146

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openabm-covid19).
