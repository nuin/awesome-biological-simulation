# GillesPy2

> Simulate a mass-action biochemical reaction network with stochastic (SSA, tau-leaping) or deterministic (ODE) solvers.

Licence: GPL-3.0 · [Source code](https://github.com/StochSS/GillesPy2)

## What it simulates

GillesPy2 simulates a network of chemical reactions in a well-mixed volume. You list species, rate constants and reactions. It returns the count of every species over time.

It offers three solvers. The Gillespie direct method (SSA) draws every reaction event one at a time, so it is exact. Tau-leaping fires many reactions per step, so it is faster and approximate. The ODE solver integrates the average behaviour and has no noise.

The key assumption is mass action. Each reaction fires at a rate equal to its constant times the product of the reactant counts. The volume is well mixed, so there is no space. Counts are whole molecules, so small populations can hit zero and stay there.

Input is a model, either Python objects or an SBML file. Output is one trajectory per run, as an array with a time column and one column per species.

## When to use it

- You want noise at low copy numbers, for example gene expression bursts with 10 to 100 mRNAs.
- You want to know how often a population goes extinct, or how wide the spread between runs is.
- You want to compare the stochastic mean with the ODE answer for the same model.

[COPASI](copasi.md) on biosimhub covers the same model class with a desktop-style task interface, SBML import and parameter scans. Choose it when your model already exists as SBML or you need a GUI. [epydemix](epydemix.md) fits better for epidemics with age groups and contact matrices. GillesPy2 fits when you want a Python script and a choice of exact or approximate solvers.

## Install it yourself

Pinned to version 1.8.3 (conda-forge, checked with a micromamba dry run, 136 MB of downloads):

```
micromamba create -n gp -c conda-forge gillespy2=1.8.3
micromamba activate gp
```

The project also documents `python3 -m pip install gillespy2 --user --upgrade`.

The conda package has no `g++` or `scons`. GillesPy2 logs a warning that the C++ solvers are unavailable and falls back to the NumPy solvers. Results stay valid, only slower.

Minimal script with the Python API, the same model as the example below (run in the recipe's 1.8.3 image):

```python
import numpy as np
from gillespy2 import Model, Species, Parameter, Reaction, NumPySSASolver

model = Model(name="LV")
model.add_parameter([Parameter(name="k_birth", expression=1.0),
                     Parameter(name="k_eat", expression=0.01),
                     Parameter(name="k_death", expression=0.5)])
prey = Species(name="Prey", initial_value=100, mode="discrete")
pred = Species(name="Predator", initial_value=50, mode="discrete")
model.add_species([prey, pred])
p = model.listOfParameters
model.add_reaction([
    Reaction(name="birth", reactants={prey: 1}, products={prey: 2}, rate=p["k_birth"]),
    Reaction(name="eat", reactants={prey: 1, pred: 1}, products={pred: 2}, rate=p["k_eat"]),
    Reaction(name="death", reactants={pred: 1}, products={}, rate=p["k_death"])])
model.timespan(np.linspace(0, 20, 201))
res = model.run(solver=NumPySSASolver, number_of_trajectories=5, seed=42)
print(res[0]["time"][-1], res[0]["Prey"][-1])
```

`res[i]` is trajectory i. `res[i]["time"]` and `res[i]["Prey"]` are arrays. The official docs describe the same pattern (`results[index]`, then a species name).

## Run the tested example

This recipe builds GillesPy2 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 1.5 s.

1. Download [gillespy2-recipe.tar.gz](https://biosimhub.pages.dev/guides/gillespy2/gillespy2-recipe.tar.gz) (Dockerfile, run_gillespy2.py, example model.rxn, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf gillespy2-recipe.tar.gz
   cd gillespy2
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/gillespy2:1.8.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/gillespy2:1.8.3 python /opt/run_gillespy2.py /work/in/model.rxn \
    --time 20 --points 201 --trajectories 5 --solver ssa \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `mean.csv` | 6.0 KB |
| `run_log.txt` | 57 B |
| `trajectories.csv` | 13.2 KB |

<details><summary>First lines of <code>mean.csv</code></summary>

```
time,Prey_mean,Predator_mean,Prey_sd,Predator_sd
0,100,50,0,0
0.1,104,53.4,4.14729,2.41661
0.2,109.8,56.6,6.73498,3.61109
0.3,114.6,59.4,6.9455,2.57682
0.4,121.6,60.4,8.40476,3.82623
0.5,128.4,65.2,8.61626,5.03587
0.6,131.4,70.8,15.9072,8.56505
0.7,132.8,77,16.4609,5.83095
0.8,137,81,18.6226,8.09938
0.9,138.8,89,16.9635,7.53658
1,137.4,99.2,15.2525,5.34416
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 2 species, 3 reactions, 5 trajectories, solver ssa
```

</details>

<details><summary>First lines of <code>trajectories.csv</code></summary>

```
trajectory,time,Prey,Predator
0,0,100,50
0,0.1,102,52
0,0.2,103,56
0,0.3,105,59
0,0.4,114,58
0,0.5,127,59
0,0.6,139,60
0,0.7,140,71
0,0.8,143,74
0,0.9,149,82
0,1,146,96
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--time` | Simulated time | 20 | 0.001 to 100000 |
| `--points` | Output time points | 201 | 2 to 5000 |
| `--trajectories` | Trajectories (stochastic solvers) | 5 | 1 to 100 |
| `--solver` | Solver | ssa | ssa, tau_leaping, ode |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is a Lotka-Volterra predator-prey model: prey reproduce, predators eat prey and become new predators, predators die. It starts with 100 prey and 50 predators, runs to t = 20 with 201 output points and 5 SSA trajectories, seed 42.

The recipe's helper script `run_gillespy2.py` is not part of GillesPy2. It reads the text model (`species`, `parameter`, `reaction A + B -> C ; rate` lines), builds a `Model` with discrete species, runs the chosen solver and writes CSV files. It caps models at 50 species and 100 reactions. The seed goes to the SSA and tau-leaping solvers only.

- `run_log.txt`: `done: 2 species, 3 reactions, 5 trajectories, solver ssa`.
- `trajectories.csv` (13,483 bytes): columns `trajectory,time,Prey,Predator`. It has 5 x 201 = 1,005 data rows. Trajectory 0 starts `0,0,100,50`, then reaches 146 prey and 96 predators at t = 1.
- `mean.csv` (6,146 bytes): per time point, the mean and standard deviation across trajectories. At t = 0 the sd is 0. At t = 1 the mean is 137.4 prey and 99.2 predators, with sd 15.3 and 5.3.

The sd uses the population formula (`np.std`, divide by N). With 5 trajectories the means are rough.

## Your own runs

All runs below used the recipe's image, the example model and seed 42. Only the stated option changed.

**Switch to the ODE solver** (`--solver ode`). The output has one trajectory and every sd is 0. The prey peak is 133.9 at t = 1 and the predator peak 207.8 at t = 2.5. At t = 20 the ODE gives 128.8 prey and 76.9 predators. The `--trajectories` value is ignored.

**Use tau-leaping** (`--solver tau_leaping`). Five trajectories give a different path from the SSA run, since the algorithm draws random numbers differently. The mean prey peak is 175 at t = 12.2, against 138.8 at t = 0.9 for SSA. At t = 20 the mean is 17.2 prey and 12.0 predators. Five runs cannot say which solver is closer, so raise the count before comparing.

**Raise trajectories to 30** (`--trajectories 30`). The mean at t = 20 is 55.7 prey (sd 53.8) and 59.5 predators (sd 68.0). Eight of 30 runs have zero prey at t = 20. The ODE gives 128.8 prey at that time, so for this model the ODE does not describe the typical stochastic run.

For your own model, edit a copy of the `.rxn` file. Species names are word characters. A product side of `0` means nothing is made.

## Pitfalls

- **One seed, one path.** Seed 42 gives the same 5 trajectories every time. Report several seeds or 30 or more trajectories before drawing conclusions.
- **The ODE ignores trajectories.** `--solver ode` always writes 1 trajectory with sd 0. Do not read that zero as precision.
- **Rates use counts.** `Prey + Predator -> 2 Predator ; k_eat` fires at `k_eat * Prey * Predator`, with counts of molecules. Rescale `k_eat` by the volume ratio if you change the volume.
- **Extinction is absorbing.** Once prey or predators reach 0 in a run they stay there. Trajectory 0 in the example ends with 0 prey and 0 predators.
- **Slow without C++ solvers.** Large counts or long times take much longer in the NumPy solvers. Try tau-leaping, or install `g++` and `scons` to use the compiled solvers.

## Further reading

- Documentation: https://gillespy2.readthedocs.io/en/latest/
- Basic usage: https://gillespy2.readthedocs.io/en/latest/getting_started/basic_usage/basic_usage.html
- Installation: https://gillespy2.readthedocs.io/en/latest/getting_started/installation/installation.html
- Source: https://github.com/StochSS/GillesPy2
- Paper: Abel JH, Drawert B, Hellander A, Petzold LR (2016), IEEE Life Sci Lett 2:35-38, https://doi.org/10.1109/LLS.2017.2652448

---

Cite: Abel JH, Drawert B, Hellander A, Petzold LR (2016). GillesPy: A Python package for stochastic model building and simulation. IEEE Life Sci Lett 2:35-38. doi:10.1109/LLS.2017.2652448

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/gillespy2).
