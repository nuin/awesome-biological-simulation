# libRoadRunner

> Simulate an SBML model as a deterministic (CVODE, RK4) or stochastic (Gillespie) time course, and find its steady state.

Licence: Apache-2.0 · [Source code](https://github.com/sys-bio/roadrunner)

## What it simulates

libRoadRunner is a C++ library that loads an SBML model and simulates it. It generates machine code for the model's rate laws through LLVM, which makes repeated simulation fast. The README describes it as a library meant to be hosted by other programs, for example for parameter optimisation on a cluster, and it ships Python bindings.

What it can do, from its documentation:

- Time-course simulation with CVODE from the SUNDIALS suite, with optional conservation-law reduction.
- Stochastic simulation with a Gillespie solver, selected with `rr.setIntegrator('gillespie')`.
- Steady-state calculation with NLEQ2.
- Metabolic control analysis, frequency-domain analysis, eigenvalues and the Jacobian.

It reads SBML Level 2 and Level 3. It does not support algebraic rules or delay differential equations.

## When to use it

Use libRoadRunner when your model is an SBML file and you want fast, scriptable ODE or Gillespie runs, or many runs inside a parameter scan or a fitting loop.

- Use [COPASI](copasi.md) when you want a graphical interface or built-in parameter estimation.
- Use [GillesPy2](gillespy2.md) when you build the model in Python and want several stochastic solvers, including tau-leaping.
- Use [BioNetGen](bionetgen.md) when your model is a set of rules that must be expanded into a network first.

## Install it yourself

The documentation and the README give one command:

```bash
python3 -m venv rr
. rr/bin/activate
pip install libroadrunner==2.10.0
```

The command resolves: libroadrunner 2.10.0 was released in August 2026 and needs numpy 2.2. PyPI lists wheels for CPython 3.11 to 3.14 on Windows, macOS (Apple silicon and Intel) and Linux x86_64 (manylinux 2.28). There is no Linux ARM wheel.

The README adds one Linux requirement: the binaries depend on the ncurses library, so install `libncurses5` with the system package manager first. The recipe below does this in a Debian 12 (bookworm) image, which still has that package. Debian 13 does not.

The recipe image is linux/amd64 because of the wheel list.

## Run the tested example

This recipe builds libRoadRunner in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.6 s. libRoadRunner has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [libroadrunner-recipe.tar.gz](https://biosimhub.pages.dev/guides/libroadrunner/libroadrunner-recipe.tar.gz) (Dockerfile, run_roadrunner.py, example model.xml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf libroadrunner-recipe.tar.gz
   cd libroadrunner
   sh run.sh
   ```

![Terminal recording of the libRoadRunner example run](https://biosimhub.pages.dev/media/libroadrunner/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/libroadrunner:2.10.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/libroadrunner:2.10.0 python /opt/run_roadrunner.py /work/in/model.xml \
    --start 0 --end 50 --points 101 --integrator cvode \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 77 B |
| `steady_state.txt` | 33 B |
| `timecourse.csv` | 2.3 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/libroadrunner/result-dark.png"><img src="https://biosimhub.pages.dev/media/libroadrunner/result.png" alt="Plot of the libRoadRunner example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
roadrunner 2.10.0: integrator cvode, 101 rows, 3 columns, species ['S', 'P']
```

</details>

<details><summary>First lines of <code>steady_state.txt</code></summary>

```
S	-1.504509863882545e-21
P	100.0
```

</details>

<details><summary>First lines of <code>timecourse.csv</code></summary>

```
time,[S],[P]
0,100,0
0.5,99.167248,0.83275202
1,98.335668,1.6643321
1.5,97.505275,2.4947253
2,96.676084,3.3239165
2.5,95.84811,4.15189
3,95.021369,4.9786306
3.5,94.195878,5.8041221
4,93.371651,6.6283487
4.5,92.548707,7.4512935
5,91.72706,8.2729398
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--start` | Start time | 0 | 0 to 1000000 |
| `--end` | End time | 50 | 0.001 to 1000000 |
| `--points` | Output points | 101 | 2 to 100000 |
| `--integrator` | Integrator | cvode | cvode, gillespie, rk4 |
| `--seed` | Seed (Gillespie only) | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the README example and the tutorial page: https://libroadrunner.readthedocs.io/en/latest/tutorial/tutorial.html

```python
import roadrunner

rr = roadrunner.RoadRunner("mymodel.xml")   # an SBML file or URL
result = rr.simulate(0, 10, 100)            # start, end, number of points
print(result)
```

`simulate(start, end, points)` returns a table whose first column is time and whose other columns are the model's floating species. By default the columns hold concentrations in square brackets, such as `[S]`.

For a stochastic run, choose the Gillespie integrator and set its seed. The documentation lists the settings of that solver: `seed`, `variable_step_size`, `initial_time_step`, `minimum_time_step`, `maximum_time_step` and `nonnegative`.

```python
rr.setIntegrator("gillespie")
rr.integrator.seed = 42
result = rr.simulate(0, 10, 100)
```

The recipe's example model is a small SBML Level 3 file written for this guide. It converts a substrate S into a product P with a Michaelis-Menten rate law (Vmax 2, Km 20, S starting at 100, compartment size 1).

## Reading the output

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

The helper script `run_roadrunner.py` writes `timecourse.csv`, a header line followed by one row per output point. The first column is `time`. The other columns are the species concentrations, named as roadrunner names them (`[S]`, `[P]`). With the default 101 points from 0 to 50 the file has 101 data rows.

For the example the mass balance is a check you can do by hand: S + P stays at 100 on every row, because the single reaction turns one S into one P. S falls monotonically and the rate slows as S drops below Km.

With the CVODE integrator the helper also tries a steady-state solve and writes the result to `steady_state.txt`. The example has no inflow, so its only steady state is S at 0 and P at 100, and a solver may or may not report it as converged. If the solve fails, the helper writes the error text instead of values. A model with inflow and outflow gives a table of steady-state concentrations.

## Pitfalls

- **Concentrations against amounts.** The default selections report concentrations. The Gillespie solver counts molecules, so give the model initial amounts in whole numbers.
- **Seed only matters for Gillespie.** CVODE is deterministic. Set the seed on the integrator object after you choose the integrator.
- **Stiff models.** The documentation says that if the integrator raises an exception, set an initial time step and tighter tolerances: `rr.integrator.absolute_tolerance`, `relative_tolerance` and `initial_time_step`.
- **Missing ncurses on Linux.** An import error that names a ncurses library means `libncurses5` is missing.
- **SBML features.** Algebraic rules and delays are not supported.

## Further reading

- Documentation: https://libroadrunner.readthedocs.io
- Stochastic simulation page: https://libroadrunner.readthedocs.io/en/latest/stochastic.html
- Source and README: https://github.com/sys-bio/roadrunner
- PyPI: https://pypi.org/project/libroadrunner/
- Paper: Welsh CM et al. (2023) libRoadRunner 2.0: a high performance SBML simulation and analysis library. Bioinformatics 39:btac770. https://doi.org/10.1093/bioinformatics/btac770

---

Cite: Welsh CM et al. (2023). libRoadRunner 2.0: a high performance SBML simulation and analysis library. Bioinformatics 39:btac770. doi:10.1093/bioinformatics/btac770

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/libroadrunner).
