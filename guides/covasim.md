# Covasim

> Agent-based SARS-CoV-2 epidemic in a synthetic population of households, schools, workplaces and community, with optional testing and contact tracing.

Licence: MIT · [Source code](https://github.com/starsimhub/covasim)

## What it simulates

Covasim simulates SARS-CoV-2 spread through a population of individual agents. Each agent has an age, a set of contacts and a disease state. Every day, infectious agents expose their contacts with a probability set by `beta`. Infected agents then move through exposed, infectious, symptomatic, severe, critical, recovered or dead, with age-dependent probabilities.

Contacts sit in layers: households, schools, workplaces and the community. The default population type in the recipe, `hybrid`, builds these layers. The `random` type draws contacts from one layer with no structure.

Testing, contact tracing, quarantine, vaccination and variants are interventions you add to the run. The recipe exposes testing and tracing.

## When to use it

- You want the shape of a COVID-19 wave in a population of 1,000 to 100,000 agents and how much it changes with transmissibility or with testing.
- You want to compare a network with household and workplace structure against random mixing.
- You want to try testing and tracing at different strengths and read the infections, tests and quarantined counts.

Use [epydemix](epydemix.md) for compartment models without individual agents, or [NetLogo](netlogo.md) when the agents should move in space. The recipe uses Covasim's default disease parameters and no vaccination or variants. Other pathogens or variants need parameters you supply yourself.

## Install it yourself

PyPI carries covasim 3.1.6 and the newer 4.0.1, which depends on the Starsim package. The recipe pins 3.1.6 on Python 3.11:

```
python3.11 -m venv cv && . cv/bin/activate
pip install covasim==3.1.6
```

A minimal run with the Python API, tried in the 3.1.6 image:

```python
import covasim as cv

sim = cv.Sim(pop_size=5000, pop_infected=10, n_days=30, rand_seed=1, verbose=0)
sim.run()
print(sim.summary["cum_infections"], sim.summary["cum_deaths"])
```

It printed 22 cumulative infections and 0 deaths.

## Run the tested example

This recipe builds Covasim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 8 s.

1. Download [covasim-recipe.tar.gz](https://biosimhub.pages.dev/guides/covasim/covasim-recipe.tar.gz) (Dockerfile, run_covasim.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf covasim-recipe.tar.gz
   cd covasim
   sh run.sh
   ```

![Terminal recording of the Covasim example run](https://biosimhub.pages.dev/media/covasim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/covasim:3.1.6 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/covasim:3.1.6 python /opt/run_covasim.py --pop-size 20000 \
    --pop-infected 20 --days 60 --beta 0.016 --pop-type hybrid \
    --test-prob 0 --trace-prob 0 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 306 B |
| `summary.json` | 289 B |
| `timeseries.csv` | 23.4 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/covasim/result-dark.png"><img src="https://biosimhub.pages.dev/media/covasim/result.png" alt="Plot of the Covasim example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Covasim 3.1.6 (2024-01-28) — © 2020-2024 by IDM
covasim 3.1.6: 20000 agents, 60 days, seed 42
cum_infections: 12822
cum_symptomatic: 6537
cum_severe: 333
cum_critical: 71
cum_deaths: 13
cum_tests: 0
cum_diagnoses: 0
cum_quarantined: 0
n_naive: 7846
r_eff: 0.987413
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "cum_infections": 12822.0,
 "cum_symptomatic": 6537.0,
 "cum_severe": 333.0,
 "cum_critical": 71.0,
 "cum_deaths": 13.0,
 "cum_tests": 0.0,
 "cum_diagnoses": 0.0,
 "cum_quarantined": 0.0,
 "n_naive": 7846.0,
 "r_eff": 0.9874130786176513,
 "peak_new_infections": 624.0,
```

</details>

<details><summary>First lines of <code>timeseries.csv</code></summary>

```
t,date,cum_infections,cum_reinfections,cum_infectious,cum_symptomatic,cum_severe,cum_critical,cum_recoveries,cum_deaths,cum_tests,cum_diagnoses,cum_known_deaths,cum_quarantined,cum_isolated,cum_doses,
0,2020-03-01,20.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,19980.0,20.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,20000
1,2020-03-02,20.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,19980.0,20.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,20000
2,2020-03-03,22.0,0.0,2.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.0,0.0,2.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,19978.0,22.0,2.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,20000
3,2020-03-04,26.0,0.0,5.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,4.0,0.0,3.0,1.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,19974.0,26.0,5.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,20000
4,2020-03-05,32.0,0.0,10.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,6.0,0.0,5.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,19968.0,32.0,10.0,2.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--pop-size` | Agents | 20000 | 1000 to 100000 |
| `--pop-infected` | Initially infected | 20 | 1 to 1000 |
| `--days` | Simulation length (days) | 60 | 10 to 365 |
| `--beta` | Transmission probability per contact per day | 0.016 | 0.001 to 0.1 |
| `--pop-type` | Contact network | hybrid | hybrid, random |
| `--test-prob` | Daily test probability for symptomatic people (0 = no testing) | 0 | 0 to 1 |
| `--trace-prob` | Contact tracing probability (needs testing) | 0 | 0 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `run_covasim.py` builds `cv.Sim` with your values, adds `cv.test_prob` (symptomatic testing, one day delay) when the test probability is above 0, and adds `cv.contact_tracing` when tracing is also above 0. It runs the simulation and writes three files.

The example uses 20,000 agents, 20 initially infected, 60 days, `beta` 0.016, the hybrid network, no testing, seed 42. The run took 8.0 seconds.

- `run_log.txt` has the version banner and the summary lines. Over 60 days: 12,822 cumulative infections, 6,537 symptomatic, 333 severe, 71 critical and 13 deaths.
- `summary.json` has the same figures plus `n_naive` (7,846 agents never infected), the effective reproduction number at the end (0.987), the peak of new infections (624 per day) and the peak day (day 55).
- `timeseries.csv` has 61 rows (day 0 to 60) and 60 columns, including `new_infections`, `cum_infections`, `n_infectious`, `n_symptomatic`, `n_severe`, `cum_tests` and `r_eff`.

The epidemic is close to its peak at day 60. Cumulative infections were 77 on day 10, 246 on day 20, 830 on day 30, 2,747 on day 40 and 7,128 on day 50. Growth runs at a factor of 3.2 to 3.4 per 10 days up to day 40, then slows to 2.6.

## Your own runs

Same image and seed 42, one option changed from the example. Each run took 7 to 9 seconds.

- **Random network** (`--pop-type random`). 9,879 infections instead of 12,822, peak of 544 new infections on day 59 instead of 624 on day 55. The structured layers speed up the early weeks: 830 cumulative infections by day 30 against 608.
- **Half the transmissibility** (`--beta 0.008`). 230 infections and a peak of 12 new infections a day. The epidemic stays small within 60 days.
- **Testing alone** (`--test-prob 0.5`). 2,201 infections instead of 12,822, with 1,544 tests and 1,056 diagnoses.
- **Testing and tracing** (`--test-prob 0.5 --trace-prob 0.8`). 398 infections, 345 tests, 236 diagnoses and 5,873 quarantined people. Peak new infections fell to 14 on day 20.
- **Another seed** (`--seed 43`). 11,956 infections and a peak of 602 on day 57, 6.8 percent below seed 42. Report many seeds.
- **Larger population** (100,000 agents, 100 initially infected). 67,928 infections, 55 deaths and a peak of 2,989 per day on day 55.

Two runs of the default settings gave byte-identical `timeseries.csv` files, so a seed reproduces a run.

## Pitfalls

- **`n_susceptible` is not "never infected".** In 3.1.6 recovered agents keep the susceptible flag, because immunity is tracked separately. The recipe reports `n_naive` for agents never infected. The example's `n_naive` is 7,846 while 20,000 minus infections is 7,178. The difference of 668 is `cum_reinfections`.
- **Short runs end mid-wave.** At 60 days the default epidemic has not finished. Raise `days` before you read final sizes.
- **Testing probability applies to symptomatic people only.** The recipe sets the asymptomatic test probability to 0, so asymptomatic spread is only caught through tracing.
- **Tracing needs testing.** The recipe adds tracing only when the test probability is above 0, because tracing starts from diagnosed cases.
- **Version banner.** Version 3.1.6 prints a copyright line on import. The recipe keeps it in `run_log.txt`.
- **Not a forecast.** The recipe uses Covasim's default parameters and adds no vaccination or variants.

## Further reading

- Documentation: https://docs.idmod.org/projects/covasim/en/latest/
- Tutorials: https://docs.idmod.org/projects/covasim/en/latest/tutorials.html
- Source: https://github.com/starsimhub/covasim
- Paper: Kerr CC et al. (2021) Covasim: an agent-based model of COVID-19 dynamics and interventions. PLoS Comput Biol 17:e1009149. https://doi.org/10.1371/journal.pcbi.1009149

---

Cite: Kerr CC, et al. (2021). Covasim: an agent-based model of COVID-19 dynamics and interventions. PLoS Comput Biol 17:e1009149. doi:10.1371/journal.pcbi.1009149

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/covasim).
