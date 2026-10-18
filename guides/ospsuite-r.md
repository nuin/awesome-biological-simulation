# ospsuite (OSPSuite-R)

> Load a PK-Sim or MoBi physiologically based pharmacokinetic simulation (.pkml), optionally scale its doses, run it and export the output time profiles.

Licence: GPL-2.0-only · [Source code](https://github.com/Open-Systems-Pharmacology/OSPSuite-R)

## What it simulates

ospsuite is the R interface to the Open Systems Pharmacology (OSP) Suite. It loads, changes and runs simulations built in PK-Sim and MoBi. PK-Sim builds physiologically based pharmacokinetic (PBPK) models of the whole body: organs, blood flows, tissue partitioning and drug properties. MoBi builds general quantitative systems pharmacology (QSP) models. Both save a simulation as a `.pkml` file. ospsuite runs that file from R.

You can:

- load a simulation and browse its parameter tree (`loadSimulation()`, `getSimulationTree()`);
- find parameters by path with wildcards and set or scale their values (`getAllParametersMatching()`, `setParameterValues()`, `scaleParameterValues()`);
- run it (`runSimulations()`) and get time profiles of the outputs;
- create individuals and run population simulations, calculate PK parameters, and run sensitivity analyses;
- compare simulated and observed data with `DataCombined` and plot them.

A parameter path matches what PK-Sim and MoBi display, for example `Organism|Weight`. The models themselves, including the physiology and the drug data, are made in the PK-Sim and MoBi desktop applications, which run on Windows. The R package is for scripting on top of them.

## When to use it

Use ospsuite to script runs of an existing PBPK or QSP model: dose scans, virtual populations, sensitivity analysis and automated reports.

- [PKPDsim](pkpdsim.md) simulates compartment PK-PD models that you write yourself in R, and needs no desktop application.
- [COPASI](copasi.md) handles general kinetic models with parameter estimation.
- mrgsolve, an R package, simulates ODE-based PK-PD models written as model code.

## Install

ospsuite is not on CRAN or conda. Both it and its dependencies come from the OSP R-universe. It needs R 4.4 or later, and it supports Windows, Linux (Ubuntu) and macOS on Apple Silicon. The current GitHub release is 13.0.1 (24 September 2026). The R-universe build available at the time of writing is 12.4.5. The licence is GPL-2.0 with a clarifying addendum, in the repository's LICENSE file.

```r
install.packages(
  "ospsuite",
  repos = c(OSP = "https://open-systems-pharmacology.r-universe.dev", getOption("repos"))
)
```

The package needs rSharp, which needs the .NET runtime. The current README names .NET 10, but the 12.4.5 build on R-universe still looks for .NET 8 ("No .NET 8 runtime was found"), so match the runtime to the version you install. On Ubuntu the rSharp README gives (use `dotnet-runtime-8.0` for 12.4.5):

```
sudo apt-get install dotnet-runtime-10.0 libcurl4-openssl-dev libssl-dev libxml2-dev
sudo apt-get install libfontconfig1-dev libharfbuzz-dev libfribidi-dev
sudo apt-get install libfreetype6-dev libpng-dev libtiff5-dev libjpeg-dev
```

The README also lists two known issues. Loading may fail unless the system locale is English, so set `LC_ALL=en_US.UTF-8` on Linux. On Linux, add the package's `lib` folder to `LD_LIBRARY_PATH`, for example `/usr/local/lib/R/site-library/ospsuite/lib/`.

## Run the tested example

This recipe builds ospsuite (OSPSuite-R) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 6.4 s. ospsuite (OSPSuite-R) has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [ospsuite-r-recipe.tar.gz](https://biosimhub.pages.dev/guides/ospsuite-r/ospsuite-r-recipe.tar.gz) (Dockerfile, run_ospsuite.R, example simulation.pkml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf ospsuite-r-recipe.tar.gz
   cd ospsuite-r
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/ospsuite-r:12.4.5 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/ospsuite-r:12.4.5 Rscript /opt/run_ospsuite.R /work/in/simulation.pkml 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `results.csv` | 1.5 KB |
| `run_log.txt` | 81 B |

<details><summary>First lines of <code>results.csv</code></summary>

```
"IndividualId","Time","Organism|Liver|A","Organism|Liver|B","Organism|A","Organism|B"
0,0,30,5,40,10
0,15,25.8203010559082,9.1796989440918,34.4270668029785,15.5729322433472
0,30,22.2231636047363,12.7768354415894,29.6308860778809,20.3691139221191
0,45,19.12912940979,15.8708715438843,25.5055046081543,24.4944953918457
0,60,16.4672946929932,18.5327053070068,21.9563941955566,28.0436058044434
0,75,14.176212310791,20.823787689209,18.9016170501709,31.0983829498291
0,90,12.2038259506226,22.7961750030518,16.2717685699463,33.7282333374023
0,105,10.5057516098022,24.4942474365234,14.0076684951782,35.9923324584961
0,120,9.0438871383667,25.956111907959,12.0585165023804,37.9414825439453
0,135,7.78541803359985,27.2145824432373,10.380558013916,39.619441986084
0,150,6.70206451416016,28.2979354858398,8.93608570098877,41.0639152526855
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
simulation Simple: 4 output paths, 21 time points, 0 dose parameters scaled by 1
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `dose_factor` | Factor applied to every dose parameter (1 = unchanged) | 1 | 0.01 to 100 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Getting Started article, https://www.open-systems-pharmacology.org/OSPSuite-R/articles/ospsuite.html. The article uses an Aciclovir example model that ships with the package:

```r
library(ospsuite)
simFilePath <- system.file("extdata", "Aciclovir.pkml", package = "ospsuite")
sim <- loadSimulation(simFilePath)
results <- runSimulations(sim)

myDataCombined <- DataCombined$new()
myDataCombined$addSimulationResults(results[[1]])
plotTimeProfile(myDataCombined)
```

The article says the plot shows the concentration-time profile of Aciclovir in plasma after an intravenous dose. It also shows how to change the dose: a parameter at a path ending in `ProtocolSchemaItem|Dose`, set with `setParameterValues()` or doubled with `scaleParameterValues(dose, factor = 2)`.

The recipe's script `run_ospsuite.R` loads any `.pkml` file, optionally scales every parameter at a `ProtocolSchemaItem|Dose` path, runs the simulation and writes all outputs to a CSV file. It uses the small `simple.pkml` file from the package's `inst/extdata` folder. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

`results.csv` is the table of simulation results from `getOutputValues()`. Each row is one time point. The columns are the individual's ID, the time, and one value column per output path. A PBPK model has many outputs: concentrations in plasma, tissues and cells, and amounts in compartments. Pick the column for one path to plot one profile.

`run_log.txt` has the simulation name, the number of output paths, the number of time points and how many dose parameters were scaled. If the number scaled is 0, the model has no parameter at that path, and the dose factor had no effect.

## Pitfalls

- **Objects cannot be saved.** The README warns that simulation objects are .NET objects. Saving and restoring an R workspace turns them into `NULL`. Reload the `.pkml` file in each session.
- **Locale.** Loading may fail unless the system locale is English.
- **Binary packages.** ospsuite and rSharp ship precompiled libraries, so they cannot go to CRAN. The architecture must match what the package provides.
- **Models need the desktop tools.** To create or change the model structure you need PK-Sim or MoBi. The R package edits parameters and initial values.
- **Version mismatch.** A `.pkml` file saved by a newer PK-Sim may not load in an older ospsuite.
- **Dose paths differ by model.** The recipe's wildcard only finds doses stored at a `ProtocolSchemaItem|Dose` path.

## Further reading

- Documentation: https://www.open-systems-pharmacology.org/OSPSuite-R/
- Installation prerequisites (rSharp): https://github.com/Open-Systems-Pharmacology/rSharp
- Source: https://github.com/Open-Systems-Pharmacology/OSPSuite-R
- Paper: Lippert J, Burghaus R, Edginton A, et al. (2019). Open Systems Pharmacology Community: An Open Access, Open Source, Open Science Approach to Modeling and Simulation in Pharmaceutical Sciences. CPT: Pharmacometrics & Systems Pharmacology 8:878-882. https://doi.org/10.1002/psp4.12473

---

Cite: Lippert J, Burghaus R, Edginton A, et al. (2019). Open Systems Pharmacology Community: An Open Access, Open Source, Open Science Approach to Modeling and Simulation in Pharmaceutical Sciences. CPT Pharmacometrics Syst Pharmacol 8:878-882. doi:10.1002/psp4.12473

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/ospsuite-r).
