# COPASI

> Deterministic (LSODA, RADAU5) and stochastic (Gillespie, Gibson-Bruck, tau-leap) time courses of SBML biochemical models.

Licence: Artistic-2.0 (COPASI); BSD-2-Clause (COPASI.js) · [Source code](https://github.com/copasi/COPASI.js)

**[Run COPASI in your browser](https://biosimhub.pages.dev/run/copasi/index.html)**: Deterministic (LSODA, RADAU5) and stochastic (Gillespie, Gibson-Bruck, tau-leap) time courses of SBML biochemical models. Nothing to install; the first visit downloads about 7 MB.

## What it simulates

COPASI simulates biochemical reaction networks: species that react through rate laws, in compartments of fixed volume. You give it a model in SBML. It returns the amount or concentration of each species over time.

It offers deterministic and stochastic methods. The deterministic methods, LSODA and RADAU5, integrate ordinary differential equations. LSODA switches between a non-stiff and a stiff solver as needed and is COPASI's default time-course method. RADAU5 is an implicit Runge-Kutta method suited to stiff systems. The stochastic methods are Gillespie's direct method, the Gibson-Bruck next-reaction method and tau-leaping. They count discrete particles and draw random reaction events.

The key assumption is a well-mixed compartment. Deterministic runs treat concentrations as continuous and noise-free. Stochastic runs need amounts in particle numbers, so the model must be in item units or scaled to them.

## When to use it

- You have an SBML model from BioModels and want its time course in a few seconds.
- You want to change an initial concentration or a global parameter and see the effect.
- You want to compare a deterministic run with a stochastic one, for example for a gene circuit with 10 to 1000 molecules.

[GillesPy2](gillespy2.md) on biosimhub fits when you write the reactions in Python or need the choice of exact or tau-leaping solvers with many trajectories. [XPPAUT](xppaut.md) fits when you want phase planes and bifurcations for a small ODE system. COPASI fits when the model already exists as SBML and you want a point-and-run tool.

## Run it in your browser

The page runs COPASI 4.47 (Build 306) compiled to WebAssembly through COPASI.js release v0.0.7. Nothing leaves your computer. The first load downloads about 7.2 MB, and a run on the bundled models takes 6 to 14 ms after that, per the page's test notes.

Controls:

- **Model.** Three BioModels examples (Repressilator, MAPK cascade, Mitotic oscillator) or Your SBML. For your own model, upload an SBML or COPASI `.cps` file, or paste SBML into the source box and press Use pasted text. Malformed SBML shows a message in the status line, and the previous model stays loaded.
- **End time** and **Points.** The run starts at t = 0. Points go from 2 to 100,001. Defaults are 1000 minutes for the repressilator, 9000 s for the MAPK cascade and 100 minutes for the mitotic oscillator.
- **Method.** Deterministic (LSODA), Deterministic (RADAU5), Stochastic (Gillespie direct), Stochastic (Gibson-Bruck) and Stochastic (tau-leap).
- **Seed.** Used by the stochastic methods. The same seed gives the same trajectory.
- **Initial values and parameters.** A table of species initial concentrations and fixed global parameters. Edited cells are outlined. Reset to model values restores the originals. Reaction-local parameters are not listed.
- **Run, Stop, Download CSV.** Stop ends the worker and restarts it. The CSV holds every variable COPASI reports, including assignment-rule quantities.

Readouts:

- **Species against time.** The chart draws at most five species. By default it picks the five with the largest peaks. Tick boxes change the choice.
- **Values at the end time.** Every output variable at the last time point.

Limits of the browser build: one model at a time, no parameter scans, no parameter estimation, and the default 5-species chart. Stochastic methods work on the repressilator, which is in item units. The other two examples use moles or nanomoles, so COPASI refuses a stochastic run, and the page suggests a deterministic method.

## Install it yourself

The desktop application, with a graphical interface and the command-line `CopasiSE`, is at https://copasi.org/Download/. Installation notes are at https://copasi.org/Support/Installation/.

For Python, the COPASI project's interface is BasiCO. The PyPI name is `copasi-basico`. The name `basico` on PyPI is a different package. A pip dry run of `pip install copasi-basico` resolved to copasi_basico 0.88 with python-copasi 4.48.309.

```
pip install copasi-basico
```

The BasiCO README lists the modules: `model_io` (load, create, save), `model_info`, `task_timecourse` (time courses), `task_parameter_estimation`, `task_scan`, `task_steadystate` and others. The documentation at https://basico.readthedocs.io/ has a notebook on simulating a model with the `run_time_course` command.

The page uses COPASI 4.47 build 306. A pip install brings a newer COPASI, so small differences in the last digits are possible.

## Reading the output

Use the Repressilator example, which models three genes that repress each other in a ring (Elowitz and Leibler, 2000). It has 6 species and 12 reactions, in item units, with a 1000 minute default end time.

The page's tests give reference values for LSODA at t = 100 with 1001 points: LacI protein (PX) 288.9113, TetR protein (PY) 1038.9228 and cI protein (PZ) 113.8297. The page gives 288.9112624, 1038.9228482 and 113.8297333. RADAU5 gives 288.9118, 1038.9210 and 113.8296, close to LSODA but not identical, since it uses looser default tolerances (1e-4 relative, against 1e-6 for LSODA).

In the stochastic methods the end values are whole molecule counts. A run with seed 42 repeats exactly, and seed 7 gives a different trajectory, according to the page's tests.

The status line after a run reads `Done:` followed by the number of points, the end time, the run time in ms and the COPASI version. Check the number of points against what you asked for.

## Your own runs

Try these in the page, one change at a time.

- **Compare LSODA and RADAU5** on the repressilator at the same end time. They should agree to about four digits, as above.
- **Switch to Gillespie direct with seed 42,** then seed 7. The molecule counts are integers and the two paths differ. Run 10 seeds before you judge a mean.
- **Edit TetR mRNA (Y) from 20 to 40,** run, then press Reset to model values. The page's tests confirm the edit changes the run and that Reset restores the original values.
- **Load the MAPK cascade and choose a stochastic method.** The refusal is the expected result: its amounts are in nanomoles and COPASI needs particle numbers.

## Pitfalls

- **Stochastic methods need particle numbers.** A model in moles or nanomoles gives a "particle number" error. Use a deterministic method or rescale the model to items.
- **Seed only matters for stochastic methods.** Deterministic runs ignore it.
- **Time units come from the model.** The chart axis says minutes or seconds for the examples and "model units" for your SBML. Check the SBML time unit before you read the axis.
- **Local parameters cannot be edited here.** The table lists species and global quantities only. Edit the SBML for reaction-local constants.
- **Large particle numbers slow stochastic runs.** The page's Stop message advises a shorter end time or tau-leap.

## Further reading

- COPASI home: https://copasi.org/
- User manual: https://copasi.org/Support/User_Manual/
- Stochastic methods: https://copasi.org/Support/User_Manual/Methods/Time_Course_Calculation/Stochastic_Simulation/
- Deterministic methods: https://copasi.org/Support/User_Manual/Methods/Time_Course_Calculation/Deterministic_Simulation/
- COPASI.js: https://github.com/copasi/COPASI.js
- BasiCO: https://basico.readthedocs.io/en/latest/
- Example models: https://www.ebi.ac.uk/biomodels/BIOMD0000000012

---

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/copasi).
