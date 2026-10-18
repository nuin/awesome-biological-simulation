# Tellurium

> Load an Antimony reaction model and run a deterministic ODE or repeated stochastic (Gillespie) timecourse with libRoadRunner.

Licence: Apache-2.0 · [Source code](https://github.com/sys-bio/tellurium)

## What it simulates

Tellurium is a Python environment for kinetic models of biochemical networks. You write a model in Antimony, a short text notation for reactions, or load SBML. Tellurium converts it to SBML and hands it to libRoadRunner, a compiled simulator.

Two kinds of run are available. The default integrator, CVODE, solves the reaction rate equations as ODEs, so the output is smooth and has no noise. The `gillespie` integrator draws each reaction event at random (Gibson direct method, as the project docs call it), so counts are whole numbers and every run differs unless you fix the seed.

Key assumptions: mass-action or user-written rate laws, a well-mixed compartment, no space. Tellurium also reads and writes SED-ML and COMBINE archives for sharing a model together with its simulation setup.

## When to use it

- You have a small or medium model and want to write, run and plot it in a few lines.
- You need both a deterministic and a stochastic answer from one model file.
- You need SBML, Antimony, SED-ML or COMBINE archive conversion.

Alternatives:

- [GillesPy2](gillespy2.md) is built for stochastic work and offers tau-leaping and several solvers.
- [COPASI](copasi.md) has a task interface for parameter scans and fitting, with no code.
- [AMICI](amici.md) compiles the ODEs and returns parameter sensitivities, which suits large models and fitting.

## Install

Tellurium 2.2.13.1 is the current release on PyPI (Apache-2.0). The README gives one command:

```bash
pip install tellurium
```

The README says there is no separate conda package, so Anaconda users install it with pip as well. The dependencies include libRoadRunner (2.10.0 on PyPI), Antimony and libSBML. libRoadRunner 2.10.0 has Linux wheels for x86-64 only (macOS arm64 and Windows wheels exist too), so pip has no libRoadRunner for ARM Linux. The recipe on this page pins `tellurium==2.2.13.1` on x86-64.

The README also lists a Spyder-based desktop front end and a notebook front end, which need no pip step.

## A first run

Adapted from the project's [introduction notebook](https://github.com/sys-bio/tellurium/blob/master/docs/_notebooks/core/introduction.rst). The deterministic example is one reaction:

```python
import tellurium as te
r = te.loada('S1 -> S2; k1*S1; k1 = 0.1; S1 = 10')
r.simulate(0, 50, 100)
r.plot()
```

The stochastic example from the same page uses a three-step chain, a Gillespie integrator and a fixed seed:

```python
import tellurium as te
r = te.loada('''
    J1: S1 -> S2;  k1*S1;
    J2: S2 -> S3; k2*S2 - k3*S3
    J3: S3 -> S4; k4*S3;
    k1 = 0.1; k2 = 0.5; k3 = 0.5; k4 = 0.5;
    S1 = 100;
''')
r.integrator = 'gillespie'
r.integrator.seed = 1234
r.integrator.variable_step_size = False
s = r.simulate(0, 50, 101)
```

The recipe uses this chain as its example model and repeats the stochastic run.

## Run the tested example

This recipe builds Tellurium in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 5.8 s. Tellurium has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [tellurium-recipe.tar.gz](https://biosimhub.pages.dev/guides/tellurium/tellurium-recipe.tar.gz) (Dockerfile, run_tellurium.py, example model.ant, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf tellurium-recipe.tar.gz
   cd tellurium
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/tellurium:2.2.13.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/tellurium:2.2.13.1 python /opt/run_tellurium.py /work/in/model.ant \
    --end 50 --points 101 --integrator gillespie \
    --runs 10 --seed 1234 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `mean.csv` | 2.2 KB |
| `run_log.txt` | 83 B |
| `trajectories.csv` | 16.6 KB |

<details><summary>First lines of <code>mean.csv</code></summary>

```
time,S1,S2,S3,S4
0,100,0,0,0
0.5,94.8,4.4,0.7,0.1
1,89.2,8.8,1.7,0.3
1.5,84.7,11.3,3.2,0.8
2,80.7,12.8,4.1,2.4
2.5,77.2,14.6,4.6,3.6
3,73.7,15,6.6,4.7
3.5,69.5,17.3,7,6.2
4,66.2,18,8.3,7.5
4.5,63,18.6,9.3,9.1
5,60.4,18.7,8.7,12.2
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
tellurium=2.2.13.1 integrator=gillespie runs=10 seed=1234 columns=time,S1,S2,S3,S4
```

</details>

<details><summary>First lines of <code>trajectories.csv</code></summary>

```
run,time,S1,S2,S3,S4
1,0,100,0,0,0
1,0.5,95,4,1,0
1,1,86,12,2,0
1,1.5,81,13,5,1
1,2,75,16,6,3
1,2.5,74,16,4,6
1,3,71,16,7,6
1,3.5,65,19,8,8
1,4,61,21,9,9
1,4.5,60,20,10,10
1,5,58,18,9,15
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--end` | End time | 50 | 0.001 to 100000 |
| `--points` | Output time points | 101 | 2 to 5000 |
| `--integrator` | Integrator | gillespie | cvode, gillespie |
| `--runs` | Stochastic runs (gillespie) | 10 | 1 to 100 |
| `--seed` | Seed (gillespie) | 1234 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- **`simulate` returns an array.** The first column is `time`. The other columns follow the `selections` list. By default they are the floating species. In the recipe the selections are species ids, so the values are amounts.
- **Deterministic run.** One smooth curve per species. With `S1 -> S2` at `k1 = 0.1` the reactant decays exponentially and the product rises to the starting amount.
- **Stochastic runs.** Each run is a step-like count trajectory. The mean over many runs approaches the ODE curve, and single runs scatter around it.
- **Recipe files.** `trajectories.csv` has a `run` column then the selections. `mean.csv` holds the mean over runs. For `cvode` there is one run, so the two files match. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **`No module named 'tesbml'` on import.** tellurium 2.2.13.1 still imports the old `tesbml` package, which has no wheels after Python 3.8. On a newer Python, add a file `tesbml.py` containing `from libsbml import *` to site-packages; `python-libsbml` is already installed as a dependency. The recipe does this.

- **Reset between runs.** After `simulate`, the model keeps its end state. Call `r.reset()` or `r.resetToOrigin()` before the next run, as the docs do in their loops.
- **Set the seed on the integrator.** `r.integrator.seed = 1234` applies to the Gillespie integrator. The docs also describe `r.setSeed(...)` for repeating identical traces.
- **Output grid.** For Gillespie, `variable_step_size = False` gives the fixed number of points you ask for. With it on, each run has its own length.
- **Antimony reaction syntax.** `S1 -> S2; k1*S1` is a reaction with its rate law. Species and parameters are set on the same text, for example `S1 = 100`.
- **Heavy install.** The package pulls in Jupyter, Plotly and several SBML libraries. A virtual environment keeps them apart.

## Further reading

- Repository and licence: https://github.com/sys-bio/tellurium
- Documentation: https://tellurium.readthedocs.io/en/latest/
- Stochastic notebook: https://github.com/sys-bio/tellurium/blob/master/docs/_notebooks/core/tellurium_stochastic.rst
- Choi K, Medley JK, König M, Stocking K, Smith L, Gu S, Sauro HM (2018). Tellurium: an extensible python-based modeling environment for systems and synthetic biology. Biosystems 171:74-79. https://doi.org/10.1016/j.biosystems.2018.07.006

---

Cite: Choi K, Medley JK, König M, Stocking K, Smith L, Gu S, Sauro HM (2018). Tellurium: an extensible python-based modeling environment for systems and synthetic biology. Biosystems 171:74-79. doi:10.1016/j.biosystems.2018.07.006

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/tellurium).
