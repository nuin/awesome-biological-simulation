# EoN (Epidemics on Networks)

> Stochastic SIR or SIS epidemic on a random contact network, repeated over several runs, with the mean S/I/R curves and final sizes.

Licence: MIT · [Source code](https://github.com/springer-math/Mathematics-of-Epidemics-on-Networks)

## What it simulates

EoN (Epidemics on Networks) simulates an epidemic that spreads along the edges of a contact network. Each node is a person. An infected node passes the disease to each susceptible neighbour at rate tau and recovers at rate gamma. In an SIR model a recovered node is immune. In an SIS model it becomes susceptible again.

The package simulates in continuous time with exact event-driven algorithms (`fast_SIR`, `fast_SIS`, `Gillespie_SIR`) and also holds ODE approximations for the same models, such as pairwise and edge-based compartmental models. The biosimhub example uses `fast_SIR` and `fast_SIS` only.

The key assumptions are constant rates, a fixed network that does not rewire, and the same tau for every edge unless you give edge weights. The network, not random mixing, decides who meets whom.

## When to use it

- You want to see how contact structure changes an outbreak. A network with a few high-degree hubs spreads a disease faster than a random network with the same mean degree.
- You want the spread of outcomes over many runs, including the chance that an outbreak dies out early.
- You want to check a network formula, such as the epidemic threshold, against a simulation.

[epydemix](epydemix.md) fits when the population is well mixed, or when you want age groups and contact matrices. [GillesPy2](gillespy2.md) fits for exact simulation of any reaction network without a graph.

## Install it yourself

Pinned to EoN 2.0 from PyPI, with networkx 3.4.2, numpy 2.1.3 and scipy 1.14.1 (the versions in the recipe image):

```
pip install EoN==2.0 networkx==3.4.2 numpy==2.1.3 scipy==1.14.1 matplotlib
```

Minimal script with a fixed seed. EoN 2.0 takes a numpy generator through `rng`, so pass one in or the run changes every time:

```python
import numpy as np, networkx as nx, EoN

rng = np.random.default_rng(1)
G = nx.fast_gnp_random_graph(1000, 8 / 999, seed=1)
t, S, I, R = EoN.fast_SIR(G, 0.1, 0.5, initial_infecteds=[0, 1, 2, 3, 4], tmax=40, rng=rng)
print(len(t), max(I), R[-1])
```

In the recipe's image this printed 1004 events, a peak of 90 infectious nodes and 504 recovered, and gave the same line on a second run.

## Run the tested example

This recipe builds EoN (Epidemics on Networks) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.2 s.

1. Download [eon-recipe.tar.gz](https://biosimhub.pages.dev/guides/eon/eon-recipe.tar.gz) (Dockerfile, driver.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf eon-recipe.tar.gz
   cd eon
   sh run.sh
   ```

![Terminal recording of the EoN (Epidemics on Networks) example run](https://biosimhub.pages.dev/media/eon/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/eon:2.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/eon:2.0 python /opt/driver.py --network erdos_renyi \
    --nodes 2000 --mean-degree 8 --model SIR --tau 0.1 \
    --gamma 0.5 --initial 5 --tmax 40 --runs 10 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `epidemic_mean.csv` | 1.0 KB |
| `run_log.txt` | 135 B |
| `summary.csv` | 612 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/eon/result-dark.png"><img src="https://biosimhub.pages.dev/media/eon/result.png" alt="Plot of the EoN (Epidemics on Networks) example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>epidemic_mean.csv</code></summary>

```
time,mean_S,mean_I,mean_R
0,1995.00,5.00,0.00
1,1990.80,5.90,3.30
2,1985.90,8.10,6.00
3,1976.60,12.00,11.40
4,1965.80,15.90,18.30
5,1953.10,20.80,26.10
6,1940.00,24.10,35.90
7,1922.40,27.30,50.30
8,1903.60,29.90,66.50
9,1884.50,32.80,82.70
10,1866.00,36.30,97.70
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
SIR on erdos_renyi: N=2000, edges=8025, <k>=8.03, <k^2>=71.9, R0~1.33
10 runs, final_size mean=738.7 min=15 max=1059; peak I mean=85.2
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
network,nodes,edges,mean_degree,second_moment_degree,r0_estimate,run,peak_infected,final_size
erdos_renyi,2000,8025,8.025,71.942,1.327,1,108,932
erdos_renyi,2000,8025,8.025,71.942,1.327,2,65,670
erdos_renyi,2000,8025,8.025,71.942,1.327,3,124,1008
erdos_renyi,2000,8025,8.025,71.942,1.327,4,5,15
erdos_renyi,2000,8025,8.025,71.942,1.327,5,108,1019
erdos_renyi,2000,8025,8.025,71.942,1.327,6,118,1059
erdos_renyi,2000,8025,8.025,71.942,1.327,7,102,939
erdos_renyi,2000,8025,8.025,71.942,1.327,8,108,768
erdos_renyi,2000,8025,8.025,71.942,1.327,9,105,931
erdos_renyi,2000,8025,8.025,71.942,1.327,10,9,46
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--network` | Network | erdos_renyi | erdos_renyi, barabasi_albert, watts_strogatz |
| `--nodes` | Nodes | 2000 | 100 to 20000 |
| `--mean-degree` | Mean degree | 8 | 2 to 40 |
| `--model` | Model | SIR | SIR, SIS |
| `--tau` | Transmission rate per infected edge | 0.1 | 0.001 to 5 |
| `--gamma` | Recovery rate per infected node | 0.5 | 0.01 to 5 |
| `--initial` | Initially infected nodes | 5 | 1 to 100 |
| `--tmax` | End time | 40 | 5 to 200 |
| `--runs` | Stochastic runs | 10 | 1 to 50 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `driver.py` builds one network, runs `fast_SIR` or `fast_SIS` the chosen number of times, and writes three files. The example uses an Erdos-Renyi network of 2000 nodes with mean degree 8, SIR, tau 0.1, gamma 0.5, 5 initial infecteds, 10 runs, end time 40 and seed 42.

- `run_log.txt` (135 bytes): `SIR on erdos_renyi: N=2000, edges=8025, <k>=8.03, <k^2>=71.9, R0~1.33`, then `10 runs, final_size mean=738.7 min=15 max=1059; peak I mean=85.2`.
- `summary.csv` (612 bytes): one row per run with the peak number infected and the final size. The network columns repeat on every row.
- `epidemic_mean.csv` (1,024 bytes): the mean S, I and R at each whole time unit from 0 to 40.

The R0 estimate is `T (<k^2> - <k>) / <k>` with `T = tau / (tau + gamma)`. Here T is 0.167 and R0 is 1.33, above 1, so large outbreaks are possible. The run sizes show two outcomes. Eight runs reached 670 to 1059 nodes. Two runs stopped at 15 and 46, because the first few infected nodes recovered before passing the disease on. The mean of 738.7 mixes both groups, so read the per-run column. The mean infectious count peaks at 62.7 around time 19 and falls to 8.3 by time 40.

## Your own runs

Same image as the recipe, seed 42, one option changed each time.

- **Hub-heavy network** (`--network barabasi_albert`). The mean degree stays near 8 (7.98), but `<k^2>` rises from 71.9 to 152.4 and R0 to 3.02. All 10 runs took off (937 to 1116 final size, mean 1033.1). The mean infectious count peaked at 191.2 around time 8, against 62.7 around time 19 on the random network.
- **SIS** (`--model SIS --tau 0.2`). R0 is 2.28. The disease persists instead of burning out. The mean number infected was 1285.4 at time 10 and 1308.0 at time 40, near a steady level of about 65 percent of the nodes. The 10 runs ended between 1259 and 1356.
- **Below threshold** (`--tau 0.05`). R0 is 0.72. Final sizes were 10 to 32 nodes, mean 16.2, and the mean infectious count was 0.7 at time 10.
- **Another seed** (`--seed 43`). The seed also builds a new network (8109 edges). Final sizes ranged from 8 to 1056, with two runs under 25.

## Pitfalls

- **The seed.** The recipe passes one numpy generator to every run, so the whole batch is reproducible. A script that only calls `random.seed` is not: an EoN 2.0 script seeded that way gave different results on each run.
- **Die-out.** With R0 near 1 some runs stop early. Report the whole distribution of final sizes, not only the mean.
- **Peak values are on a grid.** The recipe samples each run at whole time units, so a reported peak can be lower than the true peak between samples.
- **Mean degree alone is not enough.** The Erdos-Renyi and Barabasi-Albert networks above have the same mean degree and R0 of 1.33 against 3.02.
- **Time unit.** Rates are per unit time. If gamma is 0.5 per day, the mean infectious period is 2 days.
- **SIS runs end at tmax.** Check that the curve has levelled off (the mean changed by under 2 percent from time 10 to 40 in the run above).

## Further reading

- Documentation: https://epidemicsonnetworks.readthedocs.io/en/latest/
- Source: https://github.com/springer-math/Mathematics-of-Epidemics-on-Networks
- Book: Kiss IZ, Miller JC, Simon PL (2017) Mathematics of Epidemics on Networks. Springer. https://doi.org/10.1007/978-3-319-50806-1
- Paper: Miller JC, Ting T (2019) EoN. Journal of Open Source Software 4(44):1731. https://doi.org/10.21105/joss.01731

---

Cite: Miller JC, Ting T (2019). EoN (Epidemics on Networks): a fast, flexible Python package for simulation, analytic approximation, and analysis of epidemics on networks. Journal of Open Source Software 4(44):1731. doi:10.21105/joss.01731

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/eon).
