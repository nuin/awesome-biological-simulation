# APSIM Next Generation

> Farming-systems simulator for crops, soils, pastures and livestock, run from a desktop editor or the command line, under a free-for-research licence that does not allow redistribution.

Licence: LicenseRef-APSIM-General-Use · [Source code](https://github.com/APSIMInitiative/ApsimX)

## What it simulates

APSIM Next Generation (APSIM NG, repository name ApsimX) is a farming-systems simulator. It runs crop, soil, water, nitrogen, carbon and pasture models together in daily steps, on weather read from a `.met` file. The models are building blocks arranged in a tree, so one simulation can hold a field with a crop, a soil, a manager script that sows and fertilises, and a report that records chosen variables.

A model file has the extension `.apsimx`. You edit it in the desktop application, which shows the tree and a form for each model, or you run it from a command line. A run writes its results to a SQLite database (`.db`) beside the file, and a report table inside it holds the variables you asked for. The `Examples` folder in the repository has ready files, among them Wheat, Maize, Barley, Sorghum, Canola, Chickpea, AgPasture, Agroforestry and CLEM.

APSIM NG is a rewrite of the earlier APSIM 7.x line, which receives no more major releases. The authors describe it as the platform meant to run on Windows, Linux and macOS.

## When to use it

Use APSIM NG for crop sequences, soil water and nitrogen over many years, grazing systems and trees, when you want a maintained framework with a graphical editor.

- Use [DSSAT-CSM](dssat-csm.md) when a crop-specific model with cultivar coefficients is the standard in your field.
- Use [PCSE](pcse.md) when you want to script the models from Python and change process modules in code.
- Use [AquaCrop-OSPy](aquacrop-ospy.md) when a water-driven model with few parameters is enough.

## Install

There is no recipe for this tool because the licence blocks one. The General Use Licence Agreement in `LICENSE.md` grants a licence that is non-sublicensable and non-transferable. It bars you from distributing the software to any person without the licensors' written consent, and each user must accept it on download. The licence is free for public-good research and education, and for work whose results are published. Work that stays unpublished needs a Special Use licence, as the licensing page at https://www.apsim.info/download-apsim/ explains. A shared server or a prebuilt container image would redistribute the software, so use your own copy.

You download an installer after you accept the licence on the APSIM registration page (https://registration.apsim.info/). The repository has installer scripts for Windows, macOS and Debian. The Debian package puts the software under `/usr/local/lib/apsim/<version>` and adds two commands to `/usr/local/bin`: `apsim` opens the graphical editor, and `Models` runs files without it. The source tree stamps the version at build time, and the download page shows the current release number. The latest source commit is dated 2026-10-16. The software runs on .NET 8, as the repository's build scripts show.

## A first run

Adapted from the comments in the repository's [release Dockerfile](https://github.com/APSIMInitiative/ApsimX/blob/master/Dockerfiles/release-dockerfile), which run `Models path/to/my/file.apsimx`, and from the command-line options in `Models/Options.cs`.

```
cp /usr/local/lib/apsim/<version>/Examples/Wheat.apsimx .
Models Wheat.apsimx
```

Useful options from the source include `--csv` (export all reports to CSV files), `--list-simulations` (list names without running), `--simulation-names` (run only names matching a regular expression), `--single-threaded`, `--cpu-count`, `--in-memory-db` (keep results in memory instead of a database file) and `--apply` (change or create simulations from a config file). The graphical editor runs the same files with a Run button.

## Reading the output

- The `.db` file next to your `.apsimx` file holds one table per report, plus tables of units and simulation names. Open it with any SQLite tool, or let the editor show the tables in its Data store view.
- A report table has one row per reported event, such as each day, each harvest or each month, depending on the report's event list.
- `--csv` writes the same tables as CSV files. A harvest report usually carries yield, biomass and the sowing and harvest dates.
- The Summary node in the editor lists the messages and warnings a run produced. Read it before you trust a number.

## Pitfalls

- **The licence is personal.** Do not copy the installer to colleagues or host it for others. Each person registers and accepts.
- **Improvements go back to the project.** The agreement says changes you make to the software belong to the APSIM Initiative.
- **Weather must cover the run.** Give the Weather model a `.met` file that spans the simulation dates.
- **Manager scripts are code.** They are C# inside the model, so an error in one fails at load or run time.
- **Old APSIM 7.x files need conversion.** The repository has a separate command-line program with an `import` command for the older file format.
- **The 7.x and Next Generation downloads sit on the same site.** Pick Next Generation.

## Further reading

- Source and examples: https://github.com/APSIMInitiative/ApsimX
- Licensing and downloads: https://www.apsim.info/download-apsim/
- Documentation: https://docs.apsim.info/
- Paper: Holzworth D, Huth NI, Fainges J, et al. (2018). APSIM Next Generation: overcoming challenges in modernising a farming systems model. Environmental Modelling & Software 103:43-51. https://doi.org/10.1016/j.envsoft.2018.02.002

---

Cite: Holzworth D, Huth NI, Fainges J, et al. (2018). APSIM Next Generation: overcoming challenges in modernising a farming systems model. Environmental Modelling & Software 103:43-51. doi:10.1016/j.envsoft.2018.02.002

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/apsim-next-generation).
