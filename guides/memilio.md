# MEmilio

> Deterministic SEIR epidemic in one population with an optional contact reduction, solved by MEmilio's C++ ODE model; writes the daily compartments and a summary.

Licence: Apache-2.0 · [Source code](https://github.com/SciCompMod/memilio)

## What it simulates

MEmilio is a C++ library for infectious-disease models, with Python bindings. The 2.4.1 Python wheel holds 10 model modules: ODE models (SIR, SEIR, SECIR with age groups and vaccination, a metapopulation SEIR), SDE (stochastic differential equation) SIR and SIRS models, and an agent-based model.

The biosimhub recipe uses the simplest one, the ODE SEIR model with a single group. People move from susceptible (S) to exposed (E), infectious (I) and recovered (R). The model integrates the equations with an adaptive-step solver. Rates are per day.

Three things drive the epidemic: the mean latent period, the mean infectious period, and the contact rate. The recipe fixes the transmission probability per contact at 1 and sets the contact rate to R0 divided by the infectious period. An optional damping removes a share of all contacts from a chosen day on, which stands in for a lockdown.

## When to use it

Use the SEIR module to see how R0, delays and a contact reduction shape the size and timing of a single wave.

- Use [epydemix](epydemix.md) when you need random variation between runs and quantile bands.
- Use MEmilio's age-resolved SECIR or metapopulation modules, which the recipe does not expose, when ages or regions matter.
- Use [GillesPy2](gillespy2.md) when the model is a chemical reaction network.

## Install it yourself

```
pip install memilio-simulation==2.4.1
```

The wheel needs Python 3.8 to 3.13. PyPI has Linux wheels for x86-64 only, plus macOS arm64 and Windows, so the biosimhub image runs as linux/amd64 (emulated on ARM hosts). A minimal run without the recipe's helper script:

```python
import numpy as np
from memilio.simulation import AgeGroup
from memilio.simulation.oseir import InfectionState as S
from memilio.simulation.oseir import Model, interpolate_simulation_result, simulate

g = AgeGroup(0)
m = Model(1)
m.parameters.TimeExposed[g] = 5.2
m.parameters.TimeInfected[g] = 6.0
m.parameters.TransmissionProbabilityOnContact[g] = 1.0
m.populations[g, S.Infected] = 50
m.populations.set_difference_from_total((g, S.Susceptible), 83000)
m.parameters.ContactPatterns.cont_freq_mat[0].baseline = np.full((1, 1), 2.5 / 6.0)
m.parameters.ContactPatterns.cont_freq_mat[0].minimum = np.zeros((1, 1))
r = interpolate_simulation_result(simulate(0, 100, 0.1, m))
print(r.get_last_value())
```

In the 2.4.1 image this printed S 10902, E 1571, I 3154 and R 67373 at day 100.

## Run the tested example

This recipe builds MEmilio in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.5 s. MEmilio has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [memilio-recipe.tar.gz](https://biosimhub.pages.dev/guides/memilio/memilio-recipe.tar.gz) (Dockerfile, run_memilio.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf memilio-recipe.tar.gz
   cd memilio
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/memilio:2.4.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/memilio:2.4.1 python /opt/run_memilio.py --population 83000 \
    --r0 2.5 --time-exposed 5.2 --time-infected 6 \
    --initial-exposed 100 --initial-infected 50 \
    --days 150 --reduction 0 --reduction-day 30 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 135 B |
| `seir.csv` | 5.6 KB |
| `summary.csv` | 132 B |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
[2026-10-18 01:32:46.990] [info] Adaptive step sizing successful to tolerances.
done: peak infected 10218 on day 65, attack rate 0.892
```

</details>

<details><summary>First lines of <code>seir.csv</code></summary>

```
day,susceptible,exposed,infected,recovered
0.0,82850.0,100.0,50.0,0.0
1.0,82826.45,103.9,60.21,9.44
2.0,82799.22,110.49,69.93,20.36
3.0,82768.9,119.1,79.48,32.51
4.0,82732.43,130.86,89.56,47.15
5.0,82693.38,143.69,100.11,62.82
6.0,82648.85,158.81,111.64,80.71
7.0,82600.07,175.5,124.12,100.31
8.0,82544.25,194.8,138.19,122.76
9.0,82487.86,214.3,152.4,145.44
10.0,82414.61,239.74,170.7,174.96
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
population,r0,peak_day,peak_infected,final_recovered,attack_rate,final_susceptible
83000.0,2.5,65.0,10217.8,74061.3,0.8923,8902.0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--population` | Population size | 83000 | 1000 to 100000000 |
| `--r0` | Basic reproduction number R0 | 2.5 | 0.1 to 12 |
| `--time-exposed` | Mean latent period (days) | 5.2 | 0.5 to 30 |
| `--time-infected` | Mean infectious period (days) | 6 | 0.5 to 60 |
| `--initial-exposed` | Initially exposed | 100 | 0 to 100000 |
| `--initial-infected` | Initially infectious | 50 | 1 to 100000 |
| `--days` | Simulated days | 150 | 10 to 730 |
| `--reduction` | Share of contacts removed (0 = none) | 0 | 0 to 0.99 |
| `--reduction-day` | Day the contact reduction starts | 30 | 0 to 730 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_memilio.py` builds the model, runs `simulate` for 150 days with a 0.1-day step, and writes three files.

- `seir.csv` has one row per day (151 rows). Columns are susceptible, exposed, infected and recovered. Day 0 is 82,850 susceptible, 100 exposed, 50 infected and 0 recovered. The four columns sum to 83,000 on every row.
- `summary.csv` has one row. The infectious count peaks at 10,218 on day 65. By day 150 the recovered count is 74,061, an attack rate of 0.892, with 8,902 people still susceptible.
- `run_log.txt` has the solver message and a line: "done: peak infected 10218 on day 65, attack rate 0.892".

Check the attack rate against theory. For R0 = 2.5, the final-size equation z = 1 - exp(-R0 z) gives z = 0.8926. The run gives 0.8923. For R0 = 4, the equation gives 0.9802, and the run (with a 2-day latent period) gave 0.9802.

## Your own runs

Each run changes values from the example (83,000 people, R0 2.5, 150 days).

- **Halve contacts on day 30.** `--reduction 0.5 --reduction-day 30` lowers the effective R0 to 1.25. The peak fell to 2,038 infectious on day 69, and the recovered count on day 150 was 32,829 (attack rate 0.396), with the epidemic still running.
- **Halve contacts on day 60.** The same reduction on day 60 came after the peak: the peak was 9,786 on day 60 and the attack rate on day 150 was 0.731. Timing matters as much as strength.
- **Strong reduction.** `--reduction 0.7 --reduction-day 30 --days 400` brings the effective R0 to 0.75. The peak was 1,390 on day 34, and the attack rate on day 400 was 0.131.
- **R0 below the threshold.** `--r0 1.0 --days 365` gave a peak of 80 infectious on day 17 and an attack rate of 0.044. The initial 150 exposed and infectious people produce a small wave that fades.
- **R0 4, 2-day latent period.** `--r0 4 --time-exposed 2` gave a peak of 24,433 on day 28 and an attack rate of 0.980.

## Pitfalls

- **The model is deterministic.** The same inputs give the same curves, so there is no seed and no spread. Small outbreaks and extinction need a stochastic model.
- **R0 here is the recipe's definition.** The contact rate is R0 / infectious period with transmission probability 1.
- **Attack rate is recovered over population at the end of the run.** A run that stops while infections continue, such as the day-150 runs with a contact reduction, understates the final size.
- **x86-64 only.** The Linux wheel does not exist for ARM, so ARM hosts run the image under emulation. The example took 2.5 s.

## Further reading

- Source and documentation: https://github.com/SciCompMod/memilio
- Python examples used here: https://github.com/SciCompMod/memilio/tree/main/pycode/examples/simulation
- Paper: Kuehn MJ et al. (2021) Assessment of effective mitigation and prediction of the spread of SARS-CoV-2 in Germany using demographic information and spatial resolution. Math Biosci 108648. https://doi.org/10.1016/j.mbs.2021.108648

---

Cite: Kuehn MJ, et al. (2021). Assessment of effective mitigation and prediction of the spread of SARS-CoV-2 in Germany using demographic information and spatial resolution. Math Biosci 108648. doi:10.1016/j.mbs.2021.108648

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/memilio).
