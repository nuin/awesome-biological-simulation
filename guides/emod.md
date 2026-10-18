# EMOD

> A stochastic agent-based model of malaria and HIV transmission, run through the emodpy Python packages.

Licence: MIT · [Source code](https://github.com/EMOD-Hub/EMOD)

## What it simulates

EMOD (Epidemiological MODeling) is an agent-based model. Each agent, a person or a mosquito, has properties such as age and sex, and decision rules govern its contacts. Infection and recovery are random draws: a susceptible person who meets a pathogen is not certain to be infected. The README says this is why you must run many simulations to find the probability of an outcome.

From version 2.22 the repository supports only malaria and HIV. Earlier versions also covered tuberculosis, typhoid and other diseases. The malaria build models mosquito life cycles, vector species, drugs, nets, spraying and vaccines. The HIV build models relationships, care and prevention.

A run reads four things: `config.json` (parameters), a demographics file (the population), `campaign.json` (interventions and events) and optional climate and migration files. Reporters write the output.

## When to use it

Use EMOD for policy-style questions about malaria or HIV in a defined place: what a net campaign or drug round does to prevalence over several years, with stochastic variation across seeds.

Alternatives:

- [epydemix](epydemix.md) fits compartmental and stochastic epidemic models in a well-mixed or age-structured population, in a few lines of Python.
- [GillesPy2](gillespy2.md) fits when you want to write the reactions yourself and run exact stochastic simulation.
- [NetLogo](netlogo.md) fits teaching-size agent models with a GUI.

## Install

This guide has no run recipe. The project README says its repository is "primarily intended for users interested in understanding the internal implementation of the model". The C++ source needs a long scons build with MPI and embedded Python. The supported way to run it on a single computer is through the emodpy packages and Docker, and the emodpy installation page states that Docker is "required to run EMOD locally on your computer". The sandbox on this site has no Docker and no network.

Official route for malaria (from the [emodpy-malaria installation page](https://emod.idmod.org/emodpy-malaria/installation/)). It lists Windows or Linux (Mac loosely supported), Python 3.13 (3.11 to 3.14 supported), and Docker for local runs.

```
python -m venv env
source env/bin/activate
python -m pip install emodpy-malaria
```

Current versions on PyPI: emodpy-malaria 6.0.5, and `emod-malaria` 2.37.0, a Python wheel that carries the compiled `Eradication` binary and the schema. For HIV use `emodpy-hiv` 3.3.2 and `emod-hiv` 2.37.0. The binary inside the malaria wheel is a Linux x86-64 program that links to MPICH, so it does not run natively on a Mac or an ARM machine. Cluster users can use the SLURM platform and need no Docker.

The latest release of the source repository is v2.37 (August 2026). The repository notes that, unless otherwise noted, EMOD-Hub projects are no longer actively maintained or supported by IDM or the Gates Foundation. The licence is MIT.

## A first run

Adapted from [Tutorial 1](https://emod.idmod.org/emodpy-malaria/tutorials/tutorial-1/) and `tutorials/tutorial_1_intro.py` in the emodpy-malaria repository. It runs a three-year malaria simulation with no interventions.

- `build_config` applies `set_team_defaults`, a large set of validated defaults, adds the vector species gambiae, arabiensis and funestus, and sets `Simulation_Duration` to `sim_years * 365` days.
- `build_demographics` creates a single node of 1000 people at latitude -3.2, longitude 37.9, with a birth rate of 40 per 1000 per year and ages uniform from 0 to 60.
- A reporter adds the `InsetChart` channels.
- The script then calls `emod_malaria.bootstrap.setup()` to unpack the binary and schema, builds an `EMODTask` and an `Experiment`, and runs it on the `Container` platform (Docker). SLURM and COMPS platforms are the other two options.

```
git clone https://github.com/EMOD-Hub/emodpy-malaria
cd emodpy-malaria/tutorials
python tutorial_1_intro.py
```

The repository also offers a GitHub Codespace that needs no local install.

## Reading the output

The tutorial downloads `output/InsetChart.json` for each simulation and plots it with `plot_inset_chart`. InsetChart holds one time series per channel, such as the number of infected people and population size. The tutorial writes plots to a results folder.

Tutorial 2 covers more reports. Each run has a `Run_Number`, which is the random seed. Tutorial 5 sweeps it to get many replicates.

## Pitfalls

- **Docker is not optional on a laptop.** Without it there is no local platform, and Docker needs close to a gigabyte of download, per the install page.
- **Inputs come from Python.** Writing `config.json` by hand is not practical, since the schema holds hundreds of parameters. Build the config with `set_team_defaults`.
- **Many replicates.** One run is one random draw. Sweep the run number and summarise.
- **Binary versions.** The `emod-malaria` and `emodpy-malaria` versions must match (`emod-malaria~=2.37` is pinned by emodpy-malaria 6.0.5).
- **Few diseases.** Tuberculosis, typhoid and other models were removed from version 2.22.

## Further reading

- Source and README: https://github.com/EMOD-Hub/EMOD
- Documentation: https://emod.idmod.org/EMOD/
- emodpy-malaria: https://emod.idmod.org/emodpy-malaria/
- emodpy-hiv: https://emod.idmod.org/emodpy-hiv/
- Bershteyn A et al. (2018). Pathogens and Disease 76(5):fty059. https://doi.org/10.1093/femspd/fty059

---

Cite: Bershteyn A, Gerardin J, Bridenbecker D, et al. (2018). Implementation and applications of EMOD, an individual-based multi-disease modeling platform. Pathogens and Disease 76(5):fty059. doi:10.1093/femspd/fty059

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/emod).
