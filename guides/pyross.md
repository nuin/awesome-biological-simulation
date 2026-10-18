# PyRoss

> Age-structured SIR epidemic, solved as an ODE and as stochastic runs (tau-leaping or Gillespie), with the daily curves and final size per age group.

Licence: MIT · [Source code](https://github.com/SoftMatterGroupCambridge/pyross)

## What it simulates

PyRoss simulates an epidemic as people moving between compartments, split by age group. This recipe uses the SIR model with two infectious classes: asymptomatic (Ia) and symptomatic (Is). People in each age group meet people in every group at rates set by a contact matrix. The force of infection on group i is beta times the contacts with infectious people in each group j, weighted by the share of group j that is infectious.

PyRoss runs the same model three ways: a deterministic ODE (`pyross.deterministic`), an exact event-by-event stochastic simulation (`pyross.stochastic`, Gillespie) and a faster stochastic approximation (tau-leaping). The library also does Bayesian inference, forecasting and optimal control of interventions. The biosimhub example uses only the three simulations.

The key assumptions are constant rates, a contact matrix that does not change over time (unless you pass a function of time) and no births, deaths or waning immunity.

## When to use it

- You want an epidemic with age structure, for example to see which age group has the highest attack rate.
- You want the ODE curve next to stochastic runs of the same model, to see how much a finite population scatters around it.
- You plan to fit the model to data or test interventions later, which are the features PyRoss was built for.

[epydemix](epydemix.md) covers a single well-mixed population with SIR or SEIR. [EoN](eon.md) fits when the contact structure is a network of individuals instead of a matrix of groups.

## Install it yourself

PyPI holds PyRoss 2.2.1 as a source package for Linux, so it compiles Cython code on install. The recipe's image builds it on Python 3.10 with gcc, g++, cmake and swig (cmake and swig are needed because nlopt 2.6.2 builds from source on arm64). It uses numpy 1.26.4, scipy 1.13.1, Cython 0.29.37 and setuptools below 70:

```
pip install numpy==1.26.4 scipy==1.13.1 cython==0.29.37 "setuptools<70" wheel matplotlib sympy nlopt cma dill
pip install --no-build-isolation --no-deps pyross==2.2.1
```

Minimal script with a fixed seed. The initial arrays must be floats, or PyRoss stops with "Buffer dtype mismatch, expected 'double' but got 'long'":

```python
import numpy as np, pyross

N = 10000
params = {"alpha": 0.0, "beta": 0.4, "gIa": 0.2, "gIs": 0.2, "fsa": 1.0, "seed": 1}
model = pyross.stochastic.SIR(params, 1, np.array([float(N)]))
S0, Ia0, Is0 = np.array([N - 10.0]), np.array([0.0]), np.array([10.0])
data = model.simulate(S0, Ia0, Is0, lambda t: np.array([[1.0]]), 100, 101, method="tau_leaping")
X = data["X"]
print(X.shape, int(X[:, 2].max()), int(N - X[-1, 0]))
```

In the recipe's image this printed `(101, 3) 1483 7879` on two runs in a row: 101 time points, a peak of 1483 symptomatic people and 7879 people ever infected. The columns of `X` are S, Ia and Is.

## Run the tested example

This recipe builds PyRoss in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.9 s.

1. Download [pyross-recipe.tar.gz](https://biosimhub.pages.dev/guides/pyross/pyross-recipe.tar.gz) (Dockerfile, driver.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pyross-recipe.tar.gz
   cd pyross
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pyross:2.2.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pyross:2.2.1 python /opt/driver.py --population 100000 \
    --groups 3 --r0 2.5 --infectious-days 5 --asymptomatic-fraction 0.3 \
    --initial 20 --days 150 --method tau_leaping \
    --runs 5 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 200 B |
| `summary.csv` | 366 B |
| `trajectories.csv` | 6.9 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
PyRoss SIR, 3 age group(s), N=100000, R0=2.5, gamma=0.200, beta=0.500
deterministic: peak day 30, peak infectious 20940, final size 84709
5 tau_leaping runs: final size mean 84801 min 84667 max 85136
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
run,kind,peak_day,peak_infectious,final_size,attack_rate_0-19_20-64_65plus
0,deterministic,30,20940,84709,0.942 0.838 0.753
1,tau_leaping,30,21058,84667,0.942 0.838 0.753
2,tau_leaping,29,20695,84770,0.940 0.838 0.759
3,tau_leaping,31,21233,85136,0.945 0.842 0.760
4,tau_leaping,32,20965,84694,0.941 0.840 0.750
5,tau_leaping,31,21022,84739,0.940 0.840 0.751
```

</details>

<details><summary>First lines of <code>trajectories.csv</code></summary>

```
day,det_S,det_I,det_R,sto_mean_S,sto_mean_I,sto_mean_R
0,99980.0,20.0,0.0,99980.0,20.0,0.0
1,99969.3,26.1,4.6,99969.2,27.4,3.4
2,99955.0,34.4,10.6,99956.0,32.8,11.2
3,99935.7,45.7,18.6,99935.2,47.2,17.6
4,99909.9,60.9,29.1,99913.0,59.4,27.6
5,99875.2,81.5,43.3,99880.2,80.2,39.6
6,99828.6,109.2,62.2,99836.0,104.0,60.0
7,99765.8,146.6,87.6,99785.4,134.8,79.8
8,99681.4,196.9,121.7,99710.2,174.6,115.2
9,99567.8,264.7,167.5,99612.4,234.0,153.6
10,99415.2,355.7,229.1,99482.2,314.4,203.4
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--population` | Population size | 100000 | 1000 to 2000000 |
| `--groups` | Age groups (1 = well mixed | 3 | 1, 3 |
| `--r0` | Basic reproduction number R0 | 2.5 | 0.1 to 10 |
| `--infectious-days` | Mean infectious period (days) | 5 | 1 to 30 |
| `--asymptomatic-fraction` | Fraction of infections that are asymptomatic | 0.3 | 0 to 1 |
| `--initial` | Initially infectious people | 20 | 3 to 1000 |
| `--days` | Simulation length (days) | 150 | 10 to 365 |
| `--method` | Stochastic algorithm | tau_leaping | tau_leaping, gillespie |
| `--runs` | Stochastic runs | 5 | 1 to 30 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `driver.py` builds three age groups (0-19, 20-64 and 65+, with 25, 55 and 20 percent of the population) and a symmetric contact matrix scaled so its largest eigenvalue is 1. With that scaling, R0 equals beta divided by gamma, so the script sets beta from your R0. It seeds 20 symptomatic infections across the groups, then runs the ODE once and the stochastic model 5 times.

The example uses 100,000 people, R0 = 2.5, a 5 day infectious period, 30 percent asymptomatic, 150 days, tau-leaping and seed 42.

- `run_log.txt` (200 bytes): `deterministic: peak day 30, peak infectious 20940, final size 84709`, then `5 tau_leaping runs: final size mean 84801 min 84667 max 85136`.
- `summary.csv` (366 bytes): the ODE row and one row per run, with the peak day, the peak number infectious, the final size and the attack rate of each age group.
- `trajectories.csv` (7,097 bytes): for each day 0 to 150, S, I and R from the ODE and the mean of the stochastic runs.

The ODE attack rates are 0.942 for ages 0-19, 0.838 for 20-64 and 0.753 for 65+. The youngest group has the most contacts, so it is infected most. A well-mixed population with R0 = 2.5 would end with 89.3 percent infected (solving z = 1 - exp(-2.5 z) gives 0.8926). The age-structured run ends at 84.7 percent, because the contact structure makes spread less even.

The five stochastic runs peak between day 29 and day 32, close to the ODE peak on day 30. Their final sizes spread by under 0.5 percent of the population.

## Your own runs

Same image as the recipe, seed 42. Only the stated options changed.

- **One age group** (`--groups 1`). The ODE gave a peak of 23,339 infectious on day 30 and a final size of 89,267, which is the 89.3 percent from the final-size equation. The stochastic mean was 89,437.
- **R0 = 1.5** (`--r0 1.5`). The ODE peak moved to day 73 at 5,400 infectious, with a final size of 51,274. The attack rates were 0.670, 0.487 and 0.387 by age group.
- **R0 = 0.8** (`--r0 0.8`). There is no epidemic. The ODE peak is day 0 with 20 infectious, and the stochastic runs ended with 50 to 147 people ever infected, from the 20 who started.
- **Exact Gillespie in a small town** (`--method gillespie --population 5000 --runs 3`). The ODE final size was 4,240 and the three runs gave a mean of 4,236 (range 4,232 to 4,244).

## Pitfalls

- **Seeds.** PyRoss draws from its own C++ generator, so `numpy.random.seed` does not reproduce a run. Pass `"seed"` inside the parameter dictionary. The recipe uses seed, seed+1 and so on for the runs, so seeds 42 and 43 share four of their five runs.
- **Float arrays.** Integer arrays for S0, Ia0 and Is0 raise the dtype error above.
- **Gillespie cost grows with events.** One 60-day Gillespie run with 100,000 people took about 3 s in total here. Cost scales with the number of infections, so use tau-leaping when you need many runs of a large population.
- **Final size includes the first infections.** At R0 = 0.8 the final size counts the 20 initial cases.
- **Compiling from source.** The Linux install needs a C compiler and, on arm64, cmake and swig for nlopt.

## Further reading

- Documentation: https://pyross.readthedocs.io
- Source: https://github.com/SoftMatterGroupCambridge/pyross
- Paper: Li YI et al. (2021) Efficient Bayesian inference of fully stochastic epidemiological models with applications to COVID-19. Royal Society Open Science 8:211065. https://doi.org/10.1098/rsos.211065

---

Cite: Li YI, Turk G, Rohrbach PB, Pietzonka P, Kappler J, Singh R, Dolezal J, Ekeh T, Kikuchi L, Peterson JD, Kobayashi H, Cates ME, Adhikari R, Jack RL (2021). Efficient Bayesian inference of fully stochastic epidemiological models with applications to COVID-19. Royal Society Open Science 8:211065. doi:10.1098/rsos.211065

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pyross).
