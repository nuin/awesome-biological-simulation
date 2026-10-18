# BioGears

> Whole-body human physiology engine; runs an XML scenario of patient insults and treatments and returns vital-sign time series.

Licence: Apache-2.0 · [Source code](https://github.com/BioGearsEngine/core)

## What it simulates

BioGears is a C++ engine for whole-body human physiology. The project says it is meant for medical education, research and training. A virtual patient has linked organ systems: cardiovascular, respiratory, renal, energy and metabolism, temperature, drugs and more. The engine advances them together with a lumped-parameter model, in which each system is a circuit of resistances, compliances and flows, and not a mesh.

You start a patient from a patient file or from a saved engine state. Then you apply actions at chosen times and let time advance. Actions include hemorrhage, drug and fluid administration, airway obstruction, burns, exercise and many others. Data requests choose which values the engine records, for example heart rate, blood volume, arterial pressure and oxygen saturation.

Scenarios are XML files with a name, a starting point, a list of data requests and a list of actions. `AdvanceTimeData` moves the clock. The shipped scenarios cover insults and treatments such as hemorrhage with and without fluid, asthma, burns, drug infusions and CPR.

## When to use it

Use BioGears for scenario-style questions about a whole patient: how blood pressure and heart rate respond to a bleed, how long a drug dose acts, how a treatment changes oxygen saturation.

- Use [rxode2](rxode2.md) when you need pharmacokinetic and pharmacodynamic models with your own equations and between-subject variability.
- Use [openCARP](opencarp.md) when your question is about electrical activity in cardiac cells and tissue.
- Use [GillesPy2](gillespy2.md) or another reaction-network tool when the question is cellular and stochastic.

BioGears gives you the engine's built-in model. It does not let you edit the equations from a scenario file.

## Install

The project publishes release archives on GitHub. Release 8.2.0 (published 12 December 2024) has `Biogears-8.2.0-Linux.tar.gz`, about 24 MB, and a Windows installer. The Linux archive holds `bin/bg-cli`, `bin/bg-scenario`, three shared libraries, the headers, and a `howtos` folder of example programs for the C++ API.

```bash
curl -LO https://github.com/BioGearsEngine/core/releases/download/8.2.0/Biogears-8.2.0-Linux.tar.gz
tar -xzf Biogears-8.2.0-Linux.tar.gz
cd Biogears-8.2.0-Linux/bin
```

The binaries are 64-bit x86 Linux programs that link against Xerces-C 3.2 (`libxerces-c-3.2.so`) and the standard C++ runtime. On Debian 12 and Ubuntu 22.04 that library is the `libxerces-c3.2` package. Put the `bin` folder on `LD_LIBRARY_PATH`, or run from it.

The source build uses CMake (minimum 3.20) and the dependencies listed on the project wiki, https://github.com/BioGearsEngine/core/wiki. The `docker/` folder in the repository builds on Ubuntu 18.04, which is old. The recipe below uses the release archive and checks its SHA-256.

## A first run

Adapted from the command line page of the repository, https://github.com/BioGearsEngine/core/blob/master/projects/cli/README.MD. It describes `bg-cli`:

```
bg-cli [HELP, VERIFY, VERSION, THREADED]
       [JOBS N]
       [CONFIG [FILE]...], [SCENARIO [FILE]...], [TEST cdm|bge], [VALIDATE patient|drug|system|all]
```

`SCENARIO` takes one or more scenario files and runs them. `JOBS` sets the number of parallel jobs. `VALIDATE all` runs the validation scenarios. Copies of the shipped scenarios are embedded in the libraries: the driver code falls back to an embedded copy when it cannot find a scenario file on disk.

The recipe's scenario starts from that state, and bleeds from the aorta at 100 mL/min for 2 minutes after 30 seconds. It then adds 60 seconds of recovery. It is a shortened copy of the repository's `HemorrhageClass2NoFluid.xml`.

## Run the tested example

This recipe builds BioGears in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.6 s. BioGears has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [biogears-recipe.tar.gz](https://biosimhub.pages.dev/guides/biogears/biogears-recipe.tar.gz) (Dockerfile, run.sh, example scenario.xml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf biogears-recipe.tar.gz
   cd biogears
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/biogears:8.2.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/biogears:8.2.0 /usr/local/bin/run-biogears /work/in/scenario.xml > out/bg_cli_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `bg_cli_stdout.txt` | 6.0 KB |
| `scenario.xml` | 2.1 KB |

<details><summary>First lines of <code>bg_cli_stdout.txt</code></summary>

```
Reading scenario.xml
Error while processing scenario.xml
:0:0 warning: unable to open primary document entity 'xsd/BioGearsDataModel.xsd'
:4:168 error: no declaration found for element 'Scenario'
:4:168 error: attribute 'xmlns' is not declared for element 'Scenario'
:4:168 error: attribute '{http://www.w3.org/2000/xmlns/}xsi' is not declared for element 'Scenario'
:4:168 error: attribute 'contentVersion' is not declared for element 'Scenario'
:4:168 error: attribute '{http://www.w3.org/2001/XMLSchema-instance}schemaLocation' is not declared for element 'Scenario'
:5:9 error: no declaration found for element 'Name'
:6:16 error: no declaration found for element 'Description'
:7:20 error: no declaration found for element 'EngineStateFile'
:8:38 error: no declaration found for element 'DataRequests'
```

</details>

<details><summary>First lines of <code>scenario.xml</code></summary>

```
<?xml version="1.0" encoding="UTF-8"?>
<!-- Adapted from share/Scenarios/Patient/HemorrhageClass2NoFluid.xml in BioGearsEngine/core (Apache-2.0).
     Starts from the stabilized StandardMale state, so no stabilization time is spent. -->
<Scenario xmlns="uri:/mil/tatrc/physiology/datamodel" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" contentVersion="BioGears_6.3.0-beta" xsi:schemaLocation="">
  <Name>HemorrhageShort</Name>
  <Description>Bleed from the aorta at 100 mL/min for 2 minutes, then 1 minute of recovery</Description>
  <EngineStateFile>./states/StandardMale@0s.xml</EngineStateFile>
  <DataRequests SamplesPerSecond="1">
    <DataRequest xsi:type="PhysiologyDataRequestData" Name="HeartRate"                 Unit="1/min"  Precision="2"/>
    <DataRequest xsi:type="PhysiologyDataRequestData" Name="BloodVolume"               Unit="L"      Precision="3"/>
    <DataRequest xsi:type="PhysiologyDataRequestData" Name="MeanArterialPressure"      Unit="mmHg"   Precision="1"/>
    <DataRequest xsi:type="PhysiologyDataRequestData" Name="SystolicArterialPressure"  Unit="mmHg"   Precision="0"/>
```

</details>


## Reading the output

For a scenario file named `scenario.xml`, the driver code names its files from the scenario name:

- `scenario.log` is the console log.
- `scenarioResults.log` is the engine's own log.
- `scenarioResults.csv` is the time series: one row per sample and one column per data request, with the request's name and unit in the header. The recipe asks for one sample per second, so a 3.5 minute scenario gives about 210 rows.
- `bg_cli_stdout.txt` has what `bg-cli` printed.

Read the CSV with any spreadsheet or with pandas. In the hemorrhage scenario you expect blood volume to fall during the bleed, and heart rate and arterial pressure to respond. This describes the direction the model is built to show. It is not a result from the recipe.

## Pitfalls

- **Starting from a patient file is slow.** A scenario that names a `PatientFile` makes the engine stabilize the patient first. A saved engine state skips that.
- **Engine states may need a folder.** The recipe's scenario names `./states/StandardMale@0s.xml`. If `bg-cli` cannot find that state, copy the `states` folder from the repository's `share/data` next to the scenario, or change the scenario to start from a `PatientFile`.
- **Scenario files are strict XML.** The schema expects the order name, description, start, data requests, actions. The shipped files use `contentVersion="BioGears_6.3.0-beta"`.
- **Units are strings.** A data request needs a unit the engine knows, such as `1/min`, `mmHg` or `L`.
- **Results go next to the scenario.** The driver builds its output path from the scenario path, so run it on a writable copy.
- **Not a clinical tool.** The README describes the engine as a research and training platform.

## Further reading

- Repository and README: https://github.com/BioGearsEngine/core
- Command line tool: https://github.com/BioGearsEngine/core/blob/master/projects/cli/README.MD
- Documentation site named in the README: www.BioGearsEngine.com
- Releases: https://github.com/BioGearsEngine/core/releases
- Paper: Baird A, McDaniel M, White S, et al. (2020). BioGears: A C++ library for whole body physiology simulations. Journal of Open Source Software 5:2645. https://doi.org/10.21105/joss.02645

---

Cite: Baird A, McDaniel M, White S, et al. (2020). BioGears: A C++ library for whole body physiology simulations. J Open Source Softw 5:2645. doi:10.21105/joss.02645

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/biogears).
