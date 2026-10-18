# iBioSim

> Desktop CAD tool for modelling, simulating and designing genetic circuits, with ODE, stochastic and hybrid analysis of SBML models and SBOL support.

Licence: Apache-2.0 · [Source code](https://github.com/MyersResearchGroup/iBioSim)

## What it simulates

iBioSim is a computer-aided design (CAD) tool for genetic circuits. A circuit is a set of genes, promoters, regulators and reactions. You build it as an SBML model, analyse how it behaves, and use the result to choose between designs. The README says it targets genetic circuits first, and that metabolic networks, cell-signalling pathways and other chemical systems can be analysed too.

The tool supports several kinds of analysis on the same model. The catalog lists ODE simulation, stochastic simulation (SSA) and hybrid simulation, which mixes deterministic and stochastic parts. The numerical engine is a separate program, reb2sac, which iBioSim starts. A second program, GeneNet, learns a network from time-series data.

On the model side, the README states:

- It imports all SBML levels and versions and exports Level 3 Version 1.
- It supports all core SBML constructs except some types of fast reactions.
- It supports the SBML packages for hierarchical model composition, layout, flux balance constraints and arrays.
- It supports the Synthetic Biology Open Language (SBOL) for exchanging designs.
- It has modelling and visualisation support for multicellular and spatial models.
- It was tested on the SBML stochastic benchmark suite and on the curated models of BioModels.

## When to use it

Use iBioSim when you design a synthetic circuit and want to move between a schematic, an SBML model and an SBOL record in one program. Use it also when you need hierarchical composition of SBML models from parts.

- Use [COPASI](copasi.md) for general SBML analysis, parameter estimation and steady states.
- Use [libRoadRunner](libroadrunner.md) when you want to script fast SBML simulation from Python.
- Use [GillesPy2](gillespy2.md) when the stochastic model is built and run in Python.

## Install

iBioSim is a Java desktop program with a graphical interface. This site gives no ready-to-run recipe for it, because the work is done through the GUI and the program needs a display. Install it on your own computer.

1. Download the archive for your system from https://github.com/MyersResearchGroup/iBioSim/releases. The current release is 3.2.0 (27 November 2024), with assets `iBioSim-linux64.zip`, `iBioSim-mac64.zip` and `iBioSim-win64.zip`.
2. Unzip it where the application should live.
3. Run the start-up script named in the README: `iBioSim.bat` on Windows, `iBioSim.mac64` on macOS, `iBioSim.linux64` on Linux.

The project site asks for Java 1.7 or higher, and Graphviz as an option. The 3.2.0 release notes say that on Linux the dependencies are resolved at the first start, and that compiling them needs `bison`, `flex`, `swig`, `python2` and `libxml2-dev`. On Windows, if the fonts look very small, the notes give a high-DPI compatibility setting for `java.exe`.

If you build from source, the README uses Maven (`mvn clean install`), with the main class `edu.utah.ece.async.ibiosim.gui.Gui`. It also tells you to download the reb2sac and GeneNet binaries and copy them into the `bin` folder.

## A first run

The project documentation has a section "Getting Started" and one on "Creating a Project": https://myersresearchgroup.github.io/ibiosim.github.io/

The README names the video demo of the tool workflow: https://www.youtube.com/watch?v=g4xayzlyC2Q

In outline, the workflow is:

1. Start iBioSim and create a project, which is a folder that holds your models and analyses.
2. Make an SBML model, either by drawing the genes, promoters and species in the schematic editor or by importing an existing SBML file.
3. Create an analysis view for the model and choose the simulation type: ODE, stochastic or hybrid.
4. Set the end time, the output interval and, for stochastic runs, the number of runs and the seed.
5. Run it and plot the species you pick.

The documentation says it is still under development, and points to older manuals and tutorials for version 2.8. The repository also has `docs/iBioSim.pdf` and tutorial folders: https://github.com/MyersResearchGroup/iBioSim/tree/master/docs

## Reading the output

The result is a set of time courses for the species, parameters and reactions of the model. The program shows them in its graph panel. The README does not describe the files an analysis writes, so check the manual for the data formats of your version.

A stochastic result is one sample path per run, so compare several runs. A deterministic ODE result is one curve per species. Hybrid analysis treats some species deterministically and others stochastically, and the curves of the two kinds look different for that reason.

No numbers are quoted here, because the project documents give none that apply to a specific model.

## Pitfalls

- **Heavy first start on Linux.** The dependencies compile at first launch, and the build tools above must be present.
- **Fast reactions.** The README lists some types of fast reactions as unsupported.
- **Library versions.** The development notes in the README call for a particular libSBML version (an experimental 5.18.0 build) for validation and flattening. A source build with another version may fail.
- **Stochastic output varies.** Run enough replicates, and record the seed.
- **Documentation is mixed.** Parts of the user documentation are for version 2.8. Menu names can differ in 3.x.

## Further reading

- Source and README: https://github.com/MyersResearchGroup/iBioSim
- Documentation: https://myersresearchgroup.github.io/ibiosim.github.io/
- Project site: https://async.ece.utah.edu/tools/ibiosim/
- Releases: https://github.com/MyersResearchGroup/iBioSim/releases
- Paper: Watanabe L et al. (2019) iBioSim 3: a tool for model-based genetic circuit design. ACS Synthetic Biology 8:1560-1563. https://doi.org/10.1021/acssynbio.8b00078
- Earlier paper: Myers CJ et al. (2009) iBioSim: a tool for the analysis and design of genetic circuits. Bioinformatics 25:2848-2849. https://doi.org/10.1093/bioinformatics/btp457

---

Cite: Watanabe L, Nguyen T, Zhang M, Zundel Z, Zhang Z, Madsen C, Roehner N, Myers C (2019). iBioSim 3: a tool for model-based genetic circuit design. ACS Synth Biol 8:1560-1563. doi:10.1021/acssynbio.8b00078

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/ibiosim).
