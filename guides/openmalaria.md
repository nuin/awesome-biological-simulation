# OpenMalaria

> Run a stochastic individual-based Plasmodium falciparum malaria scenario and report patent prevalence by survey.

Licence: GPL-2.0-or-later · [Source code](https://github.com/OpenMalaria-Org/openmalaria)

## What it simulates

OpenMalaria is a stochastic, individual-based simulator of Plasmodium falciparum malaria. It follows every person in a simulated population through time. Each person has a parasite-density model, immunity that builds with exposure, clinical episodes and, if a health system is defined, treatment. Mosquitoes are either simulated as a vector population or replaced by a given entomological inoculation rate (EIR), the number of infectious bites per person.

You write a scenario as one XML file: demography, entomology, health system, interventions, monitoring surveys and a random seed. The simulator reads it and writes a table of survey results with one row per survey, age group and measure. A second file holds values sampled at fixed intervals, such as the simulated EIR.

The time step is 5 days. In the example scenario, the entomology section is `nonVector`. The EIR comes from a list of daily values. Prevalence therefore responds to the EIR you give it, not to mosquito ecology.

## When to use it

- You want malaria prevalence, incidence and deaths from a model that has been used to compare interventions such as bed nets, vaccines and drug campaigns.
- You have a scenario file from a published analysis and want to rerun it.
- You want stochastic spread between seeds in an individual-based model.

Use [epydemix](epydemix.md) or [odin](odin.md) for simple compartmental epidemics. OpenMalaria is a heavy tool for one disease and one parasite. Its value is in the detail of within-host biology, so a simple outbreak question does not need it.

## Install it yourself

The project builds with CMake and needs GSL, Xerces-C, the CodeSynthesis `xsd` compiler and Boost headers. Its README gives the steps (`mkdir build && cd build && cmake .. && make`) and links to releases. The repository also ships a Docker recipe.

The recipe here builds tag `schema-49.0` (commit 2d76fff) on Ubuntu 22.04 for arm64 and checks the commit hash. Compiling takes a few minutes. The final image takes 218 MB on disk.

OpenMalaria must find `scenario_current.xsd`, `densities.csv` and `autoRegressionParameters.csv` in its working directory. Without the XSD it stops with "Parsing scenario file failed. Likely the XSD schema file is not present". The helper script `run_openmalaria.py` copies these three files into a scratch folder, runs there and removes the folder.

## Run the tested example

This recipe builds OpenMalaria in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.4 s.

1. Download [openmalaria-recipe.tar.gz](https://biosimhub.pages.dev/guides/openmalaria/openmalaria-recipe.tar.gz) (Dockerfile, run_openmalaria.py, example scenario.xml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf openmalaria-recipe.tar.gz
   cd openmalaria
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/openmalaria:49.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/openmalaria:49.0 python3 /opt/run_openmalaria.py /work/in/scenario.xml \
    --pop 1000 --eir-scale 1 --survey-days 60 \
    --seed 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `ctsout.txt` | 1.9 KB |
| `output.txt` | 11.0 KB |
| `prevalence.csv` | 236 B |
| `run_log.txt` | 33 B |
| `scenario.xml` | 51.7 KB |

<details><summary>First lines of <code>ctsout.txt</code></summary>

```
##	##
timestep	recent births	input EIR	simulated EIR	human infectiousness
0	0	3.0425	3.0425	0.0488673
1	2	2.24367	2.28337	0.0489089
2	1	2.24367	2.28268	0.048925
3	2	2.24367	2.29896	0.048986
4	1	2.24367	2.29909	0.0486621
5	2	2.24367	2.30288	0.0478979
6	1	2.24367	2.29178	0.0466292
7	2	2.4168	2.4382	0.0460947
8	1	2.27533	2.24693	0.0457883
9	2	2.27533	2.23231	0.0453062
```

</details>

<details><summary>First lines of <code>output.txt</code></summary>

```
1	1	0	45
1	2	0	35
1	3	0	25
1	4	0	25
1	5	0	27
1	6	0	31
1	7	0	21
1	8	0	26
1	9	0	32
1	10	0	20
1	11	0	23
1	12	0	21
```

</details>

<details><summary>First lines of <code>prevalence.csv</code></summary>

```
survey,date,hosts,patent_hosts,patent_prevalence,first_line_treatments
1,1235-03-01,1000,726,0.726,176
2,1235-04-30,1000,710,0.71,146
3,1235-06-29,1000,727,0.727,152
4,1235-08-28,1000,719,0.719,193
5,1235-10-27,1000,694,0.694,168
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 5 surveys, 990 output rows
```

</details>

<details><summary>First lines of <code>scenario.xml</code></summary>

```
<?xml version='1.0' encoding='UTF-8'?>
<om:scenario xmlns:om="http://openmalaria.org/schema/scenario_49" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" name="test D94" schemaVersion="49" xsi:schemaLocation="http://openmalaria.org/sc
  <demography maximumAgeYrs="80" name="test" popSize="1000">
    <ageGroup lowerbound="0.0">
      <group poppercent="3.474714994" upperbound="1" />
      <group poppercent="12.76004028" upperbound="5" />
      <group poppercent="14.52151394" upperbound="10" />
      <group poppercent="12.75565434" upperbound="15" />
      <group poppercent="10.83632374" upperbound="20" />
      <group poppercent="8.393312454" upperbound="25" />
      <group poppercent="7.001421452" upperbound="30" />
      <group poppercent="5.800587654" upperbound="35" />
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--pop` | Simulated population size | 1000 | 50 to 5000 |
| `--eir-scale` | Multiplier on the entomological inoculation rate | 1 | 0 to 2 |
| `--care-seeking` | Probability of seeking official care (optional) | not set | 0 to 1 |
| `--survey-days` | Days between surveys | 60 | 5 to 180 |
| `--seed` | Seed | 1 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is `scenario.xml`, the test scenario `scenario1.xml` from the repository (schema 49). The helper script raises the population from 100 to 1000, places a survey every 60 days and runs the 1-year scenario with seed 1. It writes five files.

- `run_log.txt` says "done: 5 surveys, 990 output rows". Each survey has 22 age groups and 9 measures: 5 x 22 x 9 = 990.
- `output.txt` has four tab-separated columns: survey, age group, measure number, value. Measure 0 is nHost, 3 is nPatent (hosts with detectable parasites), and 11 is nTreatments1 (first-line treatments).
- `prevalence.csv` sums these over age groups. All 1000 hosts are counted at each survey. Patent hosts are 726, 710, 727, 719 and 694, so prevalence runs from 0.726 to 0.694. First-line treatments per survey are 176, 146, 152, 193 and 168.
- `ctsout.txt` has one row per 5-day step with input EIR and simulated EIR. The simulated value (2.28 to 2.30 in the first steps) tracks the input (2.24).
- `scenario.xml` is the scenario as run, with the overrides applied.

A prevalence near 0.72 is high. The example is a high-transmission setting, and the scenario counts a host as patent at 2.5 parasites per microlitre or more.

## Your own runs

Each run changes one setting from the example (1000 hosts, EIR multiplier 1, surveys every 60 days, seed 1). Values are patent prevalence at the 5 surveys.

- **EIR times 0.1.** 0.705, 0.646, 0.675, 0.649, 0.632.
- **EIR times 0.01.** 0.344, 0.247, 0.226, 0.214, 0.163. Prevalence falls with the EIR.
- **EIR times 2.** 0.750, 0.732, 0.763, 0.754, 0.730. Doubling the EIR adds 0.02 to 0.04.
- **No care seeking** (`--care-seeking 0`). 0.799, 0.804, 0.817, 0.822, 0.821, with 0 treatments. Treatment lowers prevalence by 0.07 to 0.13 at this EIR.
- **Seed 2.** 0.725, 0.700, 0.717, 0.733, 0.717. Seeds differ by up to 0.023 per survey at 1000 hosts.
- **200 hosts.** 0.750, 0.700, 0.680, 0.745, 0.685. Small populations are noisy.
- **5000 hosts.** 0.7386, 0.708, 0.718, 0.7204, 0.7106, in 17 s.

## Pitfalls

- **Schema version.** A scenario names its schema in the root namespace (here `scenario_49`). The helper accepts only that namespace and exits with a clear message for any other, such as `scenario_48`.
- **EIR overrides cover `EIRDaily` entries only.** The multiplier does nothing to a vector-model scenario.
- **The file's own EIR varies through the year,** so prevalence differs between surveys even in one run. Compare runs at the same survey.
- **Warnings are normal.** The test scenario prints "Deprecation warning" lines and still finishes. The helper shows them only when a run fails.
- **Cost grows with population.** 1000 hosts took 3 s, 5000 took 17 s.

## Further reading

- OpenMalaria wiki: https://github.com/OpenMalaria-Org/openmalaria/wiki
- Schema documentation: https://swisstph.github.io/openmalaria/
- Source and releases: https://github.com/OpenMalaria-Org/openmalaria
- Paper: Smith T et al. (2008) Towards a comprehensive simulation model of malaria epidemiology and control. Parasitology 135:1507-1516. https://doi.org/10.1017/S0031182008000371

---

Cite: Smith T, Maire N, Ross A, et al. (2008). Towards a comprehensive simulation model of malaria epidemiology and control. Parasitology 135:1507-1516. doi:10.1017/S0031182008000371

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openmalaria).
