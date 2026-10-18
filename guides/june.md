# JUNE

> An individual-based COVID-19 simulation of England on a census-derived virtual population, with households, schools, workplaces and care homes.

Licence: GPL-3.0-only · [Source code](https://github.com/IDAS-Durham/JUNE)

## What it simulates

JUNE is an individual-based epidemic model from Durham University and partners. It builds a virtual copy of a place, mainly England, from Office for National Statistics data. People are placed in households and care homes, go to schools, universities and companies, and take part in leisure (pubs, cinemas, gyms, groceries) and commuting. Hospitals and care homes get their own rules. Infection spreads inside these groups as the day moves through its time steps.

The published model is for COVID-19. People move through infection stages with a symptom trajectory that depends on age and sex, and may be admitted to hospital or die. The run script has options for policies such as mask wearing, isolation, testing and vaccination. It is split by area, so large runs can be spread across processors with MPI.

The project is named after June Almeida, the virologist who first identified the coronavirus group.

## When to use it

Use JUNE to study how a policy changes the spread of a respiratory infection among people in a realistic English geography.

Alternatives:

- [epydemix](epydemix.md) fits age-structured stochastic models without a synthetic population, and installs from conda-forge.
- [FRED](fred.md) builds US synthetic populations, under a non-commercial licence.
- [NetLogo](netlogo.md) fits small teaching models.

## Install

This guide has no run recipe. A JUNE run needs a world built from census data, and that data is not in the repository or the PyPI package. The README tells you to download it with `get_june_data.sh`. The script fetches `data_private.zip` from a Durham University server using a shared login that is written inside the script, and the data licence is not stated. The README disclaimer says the data mixes datasets from the Office for National Statistics and may contain modifications. The sandbox on this site has no network, and putting the data in a public image is not clearly allowed.

The package also pins old libraries, so it needs a matching Python and an MPI build.

Official route, from the README:

```
pip install june
get_june_data.sh
```

If the script is not found, clone the repository and run `scripts/get_june_data.sh`. The package is JUNE 1.2.0 on PyPI (the latest GitHub release is v1.2.0, October 2022). Building `mpi4py` needs a working Open MPI or Intel MPI. The README gives a conda route, which it calls required for M1 Macs, and FAQs for `mpi4py`, `h5py` and `tables` build errors. To work from the latest code, `git clone` the repository and run `pip install -e .`. The licence is GPL-3.0.

## A first run

Adapted from [example_scripts/README.md](https://github.com/IDAS-Durham/JUNE/blob/master/example_scripts/README.md). The README also points to `Notebooks/quickstart.ipynb` for a gentler introduction.

1. Run `create_world.py`. It reads `london_areas.txt`, takes 20 of the super areas and adds the King's Cross area, three areas around Cambridge and five around Bath. It builds hospitals, companies, schools, universities, care homes and households, plus pubs, cinemas and groceries, and saves the world as `tests.hdf5`.
2. Run `python run_simulation.py` for a serial run, or `mpirun -np X python run_simulation.py` for X cores. The script reads `config_simulation.yaml` and `config_interaction.yaml`.

In the example configuration, `time.total_days` is 100 days starting on 2020-02-28. The script takes many options, among them `--world_path`, `--config`, `--household_beta`, indoor and outdoor beta ratios, mask wearing, vaccines and isolation settings. The repository does not state example output numbers.

## Reading the output

- JUNE writes records of the run, such as infections, hospital admissions and deaths, through its `Record` class to HDF5 files. With MPI, each process writes its own file, and the script combines them (`combine_records`).
- The `june.tracker` module can also track contacts and plot them.
- The paper plots repository, [june_paper_plots](https://github.com/IDAS-Durham/june_paper_plots), shows how the published figures were made from the records.

## Pitfalls

- **The data download.** The script depends on a Durham server. If it is down, the install is stuck at the world-building step.
- **MPI build.** Most install problems come from `mpi4py`, `h5py` and `tables`. Follow the README FAQs.
- **Python version.** The 1.2.0 requirements were written for older Python and library versions. Use a fresh environment, and use the README conda recipe if pip fails.
- **Region choice.** Even the small example builds about 30 super areas. A full-England world needs a cluster.
- **Reproducibility.** `run_simulation.py` sets the numpy, numba and random seeds to 0 at the top. Change this for replicates.

## Further reading

- Source and README: https://github.com/IDAS-Durham/JUNE
- Documentation: https://github.com/IDAS-Durham/JUNE/blob/master/docs/index.md
- Paper: Aylett-Bullock J et al. (2021). Royal Society Open Science 8(7):210506. https://doi.org/10.1098/rsos.210506
- Paper plots: https://github.com/IDAS-Durham/june_paper_plots

---

Cite: Aylett-Bullock J, Cuesta-Lazaro C, Quera-Bofarull A, et al. (2021). June: open-source individual-based epidemiology simulation. Royal Society Open Science 8(7):210506. doi:10.1098/rsos.210506

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/june).
