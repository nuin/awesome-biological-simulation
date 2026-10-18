# FATES

> A cohort-based vegetation demography model (trees by size and plant functional type) that runs as a component inside the CTSM, CESM or E3SM land models.

Licence: BSD-3-Clause-LBNL · [Source code](https://github.com/NGEET/fates)

## What it simulates

FATES, the Functionally Assembled Terrestrial Ecosystem Simulator, is a numerical model of terrestrial ecosystems. It represents a patch of vegetation as cohorts of trees that differ in size and plant functional type. Cohorts compete for light, grow, reproduce, die and burn. Patches age after disturbance, so one grid cell holds a mosaic of forest stands at different stages of recovery.

FATES is not a program that you start by itself. It is a library that a host land model calls each time step. The host supplies weather, soil, hydrology and the surface energy balance. FATES supplies the vegetation. Its development is funded by the US Department of Energy through the NGEE-Tropics project.

## When to use it

Use FATES when the question is about forest demography inside an Earth system model: how size structure, mortality and disturbance change carbon storage and canopy fluxes under a climate scenario.

Alternatives:

- Run the host model's default big-leaf vegetation when you need carbon and water fluxes and not tree-size structure.
- Stand-alone individual-based forest models fit when you want a small model that runs on a laptop without a host land model.

## Install

This guide has no run recipe. The README says: "Most users should not need to directly clone this repository. FATES needs to be run through a host model." A run needs a host land model, a CIME build with a Fortran compiler and MPI, site forcing data, surface and domain files, and a parameter file. That is far above the 1 CPU, 300 s sandbox on this site, and FATES has no stand-alone driver.

The official route, from the [installation tutorial](https://fates-users-guide.readthedocs.io/en/latest/tutorial/HPC/installation.html):

```
git clone git@github.com:ESCOMP/CTSM.git
cd CTSM
./manage_externals/checkout_externals
cd src/fates
```

For E3SM, clone `E3SM-Project/E3SM`, run `git submodule update --init --recursive`, and find FATES in `components/elm/src/external_models/fates`. The host model pulls in the version of FATES it is tested with.

The [API compatibility table](https://fates-users-guide.readthedocs.io/en/latest/user/release-tags-compat-table.html) lists which FATES tag matches which host version. The latest tag is `sci.1.93.2_api.46.0.0`. The users guide advises that, for the most stable code, you check out the most recent tag that is not a pre-release. The licence file is the modified BSD licence of Lawrence Berkeley National Laboratory (SPDX `BSD-3-Clause-LBNL`).

## A first run

Adapted from the [tutorial, case 1](https://fates-users-guide.readthedocs.io/en/latest/tutorial/HPC/running-fates-walkthrough-case1.html), which uses CTSM on a high-performance computer. It builds a single-site run for the pre-made `1x1_brazil` resolution, a point in the southern Amazon.

The script calls `create_newcase` with the compset `I2000Clm50FatesRs` and the resolution `1x1_brazil`. It then sets the run length and forcing with `xmlchange`: `STOP_N` 5 with `STOP_OPTION` nyears, `RUN_STARTDATE` 2001-01-01, atmospheric forcing years 1996 to 2001, and `CLM_FORCE_COLDSTART` on. Then:

```
./case.setup
./case.build
cd run1_1x1brazil
./case.submit
```

The tutorial data package (an OSF download) holds the scripts and sample output. Machine and project names in the script must be changed to match your system.

## Reading the output

- The run writes NetCDF history files to the scratch folder, not the case folder. While the run is going they sit in the `run/` directory, and they may be archived when it ends.
- History files hold the standard model output, including FATES variables such as size-class and patch-age-class diagnostics.
- The tutorial concatenates the files into one `run1.nc` and opens it with `ncview`, a viewer for NetCDF files. Python (xarray) or R work the same way.
- Output is large. It takes more space than the code and scripts.

## Pitfalls

- **Host and FATES must match.** A FATES tag works only with a host version that has the same API number. Use the compatibility table.
- **Cold start.** The case-1 run starts with bare ground. Long spin-up is needed before vegetation is near equilibrium, and the run length above is a teaching length.
- **Unsupported features.** The users guide keeps a list of unsupported or broken features. Check it before using a switch.
- **The tutorial is dated.** Its package was last updated for tag `sci.1.43.3_api.14.2.0` (March 2021), and the machine names are from older systems. Expect to adapt the scripts.
- **Parameters live in a file.** Plant functional type traits are set in the FATES parameter file, which the host namelist points to.

## Further reading

- Source and README: https://github.com/NGEET/fates
- Users guide and tutorials: https://fates-users-guide.readthedocs.io/en/latest/
- Technical documentation: https://fates-docs.readthedocs.io/en/latest/index.html
- Software DOI: https://doi.org/10.5281/zenodo.3825473
- Koven CD et al. (2020). Biogeosciences 17:3017-3044. https://doi.org/10.5194/bg-17-3017-2020

---

Cite: Koven CD, Knox RG, Fisher RA, et al. (2020). Benchmarking and parameter sensitivity of physiological and vegetation dynamics using the Functionally Assembled Terrestrial Ecosystem Simulator (FATES) at Barro Colorado Island, Panama. Biogeosciences 17:3017-3044. doi:10.5194/bg-17-3017-2020

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/fates).
