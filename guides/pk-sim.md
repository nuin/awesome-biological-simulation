# PK-Sim / Open Systems Pharmacology Suite

> Whole-body physiologically based pharmacokinetic modelling for drugs in humans and lab animals, in a Windows desktop application, with MoBi for custom systems pharmacology models.

Licence: GPL-2.0-only with the OSP clarifying addendum · [Source code](https://github.com/Open-Systems-Pharmacology/PK-Sim)

## What it simulates

PK-Sim simulates where a drug goes in the body over time. It is a physiologically based pharmacokinetic (PBPK) tool. The body is a set of organs joined by blood flow, and each organ has its own volume, perfusion and composition. Given a dose and the properties of the molecule, PK-Sim computes concentration-time curves in plasma, blood cells and tissues.

The built-in database holds the anatomy and physiology of humans and of the most common lab species: mouse, rat, minipig, dog, monkey, beagle and rabbit. PK-Sim derives passive distribution from the molecule's properties, and it adds active processes such as metabolism by a named enzyme or transport. It offers different model structures for small molecules and large molecules.

You work with building blocks that you reuse: individuals, populations, expression profiles, compounds, formulations, administration protocols, events, observers and observed data. A simulation combines one of each. Swap the individual for a virtual population to go from one animal to a trial. Swap the formulation for a controlled-release one, or the protocol for a multiple-dose schedule.

PK-Sim reads and writes the same simulations as MoBi, the expert tool of the same suite, which lets you edit every equation and build custom systems pharmacology models.

## When to use it

Use PK-Sim to predict exposure before or beside a clinical study, to scale from animal to human, or to test how age, weight, organ function or a drug interaction changes a profile.

- Use [mrgsolve](mrgsolve.md) when you prefer to write the ODE model in code and simulate populations from R.
- Use [COPASI](copasi.md) when the system is a biochemical reaction network in SBML, not an organism.
- Use [GillesPy2](gillespy2.md) when molecule counts are small enough that noise matters.

## Install

There is no recipe for this tool. PK-Sim is a Windows desktop application with a graphical interface, and a simulation cannot be built from a command line. The GitHub release v12.3.173 (2026-07-07) carries an installer, `PK-Sim.12.3.173.msi`, and a portable archive, `PKSim-Portable.12.3.173.zip`. The source is C# and its license is GPL version 2 with a clarifying addendum. The addendum limits liability, restates that copyleft applies to software you distribute with GPL code, and grants no trademark rights.

The suite's R package `ospsuite` is a separate tool. It loads, edits and runs simulations that were saved from PK-Sim or MoBi, and it works on Windows, Ubuntu and Apple-silicon macOS. It is not on CRAN. It needs R 4.4 or later, the `rSharp` package and .NET 10, and it comes from the OSP R-universe:

```r
install.packages(
  "ospsuite",
  repos = c(OSP = "https://open-systems-pharmacology.r-universe.dev", getOption("repos"))
)
```

The package page at the time of writing is version 13.0.1.

## A first run

In the application you build a model in this order. The steps follow the README and the PK-Sim documentation.

1. Create an **individual** (species, population, sex, age, weight, height).
2. Create a **compound** with its properties, such as molecular weight, lipophilicity, solubility, fraction unbound and any metabolising enzyme.
3. Create a **formulation** and an **administration protocol**, for example an intravenous infusion or a tablet taken every 24 hours.
4. Create a **simulation** from those blocks, choose the model structure, and press Run.

To rerun a saved simulation from R, adapted from the [ospsuite Getting Started article](https://www.open-systems-pharmacology.org/OSPSuite-R/articles/ospsuite.html), which uses the Aciclovir example that ships in the package:

```r
library(ospsuite)
simFilePath <- system.file("extdata", "Aciclovir.pkml", package = "ospsuite")
sim <- loadSimulation(simFilePath)
results <- runSimulations(sim)
```

The article plots the concentration-time profile of Aciclovir in plasma after IV administration.

## Reading the output

A run gives time profiles for every compartment you ask for, for example venous plasma, tissue interstitial space or cells. The chart editor overlays observed data you import, so you can see how close a prediction is. A PK analysis turns a profile into numbers such as the area under the curve, the peak concentration and the time of the peak.

In `ospsuite`, `runSimulations()` returns a list of results, one per simulation. The vignette combines a result with `DataCombined` and draws it with `plotTimeProfile()`.

## Pitfalls

- **Windows only for the application.** Linux and macOS users reach the models through `ospsuite` and a `.pkml` file saved on Windows.
- **Compound inputs drive the prediction.** Poorly measured lipophilicity, unbound fraction or solubility moves the profile, so document where each value came from.
- **Pick the calculation methods on purpose.** The partition-coefficient and permeability methods are options, and different choices give different distributions.
- **A species is not a person.** Check the physiology before scaling, in particular enzyme expression and protein binding.
- **Pair versions with care.** The ospsuite documentation has a "PK-Sim Installation" article. Read it before you combine the R package with a given PK-Sim release.
- **Copyleft applies if you embed it.** The license text says that software you distribute that is linked with or combined with GPL code falls under the GPL.

## Further reading

- Source and releases: https://github.com/Open-Systems-Pharmacology/PK-Sim
- Documentation: https://docs.open-systems-pharmacology.org/
- R package: https://www.open-systems-pharmacology.org/OSPSuite-R/
- Paper: Willmann S, Lippert J, Sevestre M, Solodenko J, Fois F, Schmitt W (2003). PK-Sim: a physiologically based pharmacokinetic 'whole-body' model. BIOSILICO 1:121-124. https://doi.org/10.1016/S1478-5382(03)02342-4

---

Cite: Willmann S, Lippert J, Sevestre M, Solodenko J, Fois F, Schmitt W (2003). PK-Sim: a physiologically based pharmacokinetic 'whole-body' model. BIOSILICO 1:121-124. doi:10.1016/S1478-5382(03)02342-4

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pk-sim).
