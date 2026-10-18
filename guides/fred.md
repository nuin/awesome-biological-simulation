# FRED

> An agent-based epidemic simulator over census-based synthetic populations of households, schools and workplaces, free for non-commercial research only.

Licence: LicenseRef-UPitt-FRED-EULA · [Source code](https://github.com/PublicHealthDynamicsLab/FRED)

## What it simulates

FRED (Framework for Reconstructing Epidemiological Dynamics) is an agent-based model from the University of Pittsburgh Public Health Dynamics Laboratory, built with the Pittsburgh Supercomputing Center and Carnegie Mellon University. Each agent is a person in a synthetic population. People live in geolocated households and go to schools and workplaces, and infection spreads through those mixing groups.

The synthetic populations are statistically realistic copies of real places, built from census microdata. FRED's U.S. population is based on the U.S. Synthetic Population 2010 (Version 1) from RTI International. It includes group quarters such as dormitories, prisons, nursing homes and military barracks. Populations for U.S. counties and states are downloaded from the lab's website.

A model is a text file. In version 5 it declares locations, dates and one or more conditions (diseases or states) and the rules that move agents between them. Vaccines, antivirals, school closure and similar interventions are set up in the same file.

## When to use it

Use FRED when you need an epidemic over a real U.S. county or state, with people placed in households, schools and workplaces, and you are at a non-profit or governmental institution.

Alternatives:

- [epydemix](epydemix.md) fits age-structured stochastic models with contact matrices, under a free software licence.
- [NetLogo](netlogo.md) fits small agent-based teaching models.
- [EMOD](emod.md) fits malaria and HIV transmission, under the MIT licence.

## Install

This guide has no run recipe, and this site does not host a FRED run form. The reason is the licence. The EULA in the repository (FRED Version 5, University of Pittsburgh) says the software is for "Non-Commercial, Educational or Research Purposes only", at "a non-profit or governmental institution". Under Scope of Grant the licensee may not:

- "redistribute, post, or otherwise enable or permit other individuals who have not executed a license agreement with UNIVERSITY to access or use the SOFTWARE";
- "modify or create derivative works based on the SOFTWARE".

A public server that runs FRED for anonymous visitors would break the first rule. A public image that others pull would break it too. So the only route is to obtain FRED yourself, under the EULA, on a machine you control.

Official route, from the README:

1. Read the EULA (the `LICENSE` file). Downloading or installing means you agree to it.
2. Clone the repository: `git clone https://github.com/PublicHealthDynamicsLab/FRED`. The current version file reads `PUB.5.7.0`.
3. From the top-level directory run `make`. It compiles the source and unzips the included population files. The default flags use C++17 and `-O3` with OpenMP.
4. Set `FRED_HOME` to the folder, and add `$FRED_HOME/bin` and `$FRED_HOME/pybin/bin` to `PATH`. Set `FRED_GNUPLOT` to your gnuplot path for plots.

The README says FRED has been built on macOS and on RHEL, CentOS, OpenSUSE and Ubuntu, and will not compile on Windows without significant changes. It also says this public version is always several check-ins behind the private version, and that the commercial version is owned and maintained by Epistemix. Commercial use needs a licence from Epistemix (the EULA names sales@epistemix.com).

## A first run

Adapted from `models/minimal/minimal.fred` in the repository and the usage line of `bin/fred_job`. The minimal model is:

```
locations = Jefferson_County_PA
start_date = 2020-Jan-01
end_date = 2020-Jan-10
condition ACTIVE {}
```

It simulates ten days in a small Pennsylvania county, with one empty condition. The `fred_job` script takes `-p model.fred`, `-k key` (a name for the job), and `-s` and `-n` for the first and last run number:

```
cd models/minimal
fred_job -p minimal.fred -k first_test -n 1
```

`bin/fred_installation_test` checks that `FRED_HOME` is set and the binary exists. The command line above comes from the script's usage text. The repository does not state example output.

## Reading the output

- Each job writes a folder per run (`RUN1`, `RUN2`, and so on) under the job's output directory, with a log file for each run.
- `fred_csv`, `fred_plot` and the other scripts in `bin/` turn results into tables and figures. `fred_help` prints the parameter documentation.
- `fred_job` passes each run number to the FRED binary (`-r`), so a set of runs is one job. Run several replicates and summarise.

## Pitfalls

- **The licence limits who can use your copy.** Colleagues who have not agreed to the EULA cannot use it. Pass the repository link, not the files.
- **Model files follow the repository.** Models in `models/` match this version. Check any model from a paper against the version it was written for.
- **Population files are separate.** A location other than the included ones needs a download from the lab website.
- **Citation line.** The EULA asks that publications reference "FRED: A Framework for Reconstructing Epidemiological Dynamics (Version 5) ©2019, University of Pittsburgh".
- **No Windows build.**

## Further reading

- Source and README: https://github.com/PublicHealthDynamicsLab/FRED
- Synthetic populations: https://fred.publichealth.pitt.edu/syn_pops
- Epistemix (commercial version): https://www.epistemix.com
- Grefenstette JJ et al. (2013). BMC Public Health 13:940. https://doi.org/10.1186/1471-2458-13-940

---

Cite: Grefenstette JJ, Brown ST, Rosenfeld R, et al. (2013). FRED (A Framework for Reconstructing Epidemic Dynamics): an open-source software system for modeling infectious diseases and control strategies using census-based populations. BMC Public Health 13:940. doi:10.1186/1471-2458-13-940

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/fred).
