# Virtual Cell (VCell)

> Desktop modelling environment for cell biology with compartmental ODE, stochastic, spatial reaction-diffusion and rule-based simulation, plus geometries from microscope images.

Licence: MIT · [Source code](https://github.com/virtualcell/vcell)

## What it simulates

Virtual Cell (VCell) is a modelling and simulation platform for cell biology, built at the Center for Cell Analysis and Modeling at UConn Health. You describe a biological system, and VCell writes the mathematics and runs it.

The vcell.org site lists these simulation types:

- **Deterministic.** Compartmental ODEs, or reaction-diffusion-advection PDEs in space, with support for 2D kinematics (moving boundaries).
- **Stochastic.** Gillespie-type (SSA) solvers for reaction networks.
- **Spatial stochastic.** Reaction-diffusion with Smoldyn.
- **Hybrid and network-free.** Mixed deterministic and stochastic runs, and agent-based network-free simulation for rule-based models.
- **Particle-based.** SpringSaLaD, added as a supported application in VCell 8.0: spheres joined by springs, with Langevin dynamics, for multivalent molecules and clusters.

Models can include membrane flux, lateral membrane diffusion and electrophysiology. Spatial models can take their geometry from 2D or 3D microscope images or from analytical expressions. There are two entry routes: a biology-based interface where you enter reactions and pathways and VCell generates the equations, or direct entry of the maths.

## When to use it

- Your question needs space: diffusion in a cell shape taken from an image, or membrane-bound and cytosolic species in different compartments.
- You want to build the model by drawing reactions, not by writing code.
- You teach or learn cell modelling, and want published models to open and change.

Alternatives:

- [COPASI](copasi.md) covers non-spatial ODE and stochastic models, with scans and fitting, in a lighter desktop tool.
- [Tellurium](tellurium.md) and [GillesPy2](gillespy2.md) fit well-mixed models that you script in Python.
- [Cytosim](cytosim.md) fits cytoskeleton mechanics, which VCell does not target.

## Install

No recipe is offered. VCell is a desktop GUI program written in Java. It also relies on remote servers, a central model database and cluster computing hosted by the project, and a sandbox without network access cannot reach them. The software licence is MIT, so redistribution is not the obstacle.

From the project's pages:

- The download page at https://vcell.org/run-vcell-software lists installers for Windows, macOS and Linux. It shows VCell 8.0 (released May 2026) as the current release edition. The GitHub repository's latest release tag is 8.2.1.01.
- The page says administrator rights are no longer needed to install (since 7.7).
- The README links prebuilt installers for Windows, macOS and Linux, and runs the client from a source build with `./vcell.sh`. A source build needs Git, Maven, Poetry, Python 3.10 and Java 17. The client "connects to the VCell servers".
- The command-line module, `vcell-cli`, needs Python 3.10 and Poetry.

## A first run

Adapted from the vcell.org [home page](https://vcell.org/) and [download page](https://vcell.org/run-vcell-software):

1. Download the installer for your system and install it.
2. Start the VCell client. It talks to the project's servers, which keep the model database and run the heavy simulations.
3. Open a model from the database, or start a new one and enter reactions and compartments.
4. Pick or create an application (a way to simulate the model, such as deterministic or stochastic) and set its geometry, initial conditions and solver.
5. Run the simulation and open the results viewer.

The site does not give a worked example with numbers, so none are quoted here. Lectures and tutorials from the annual Workshop on Computational Cell Biology are on the project's YouTube channel.

## Reading the output

- **Non-spatial runs.** Time courses of species amounts or concentrations, plotted in the viewer. Stochastic applications can run multiple trials, and VCell 8.0 adds averages, standard deviations and min/max across trials.
- **Spatial runs.** Concentration fields over time on the chosen geometry.
- **Export.** Since VCell 7.7 exported results use the N5 image format, which ImageJ and similar tools can read.
- **Models and simulations.** These stay in the VCell database, so you can reopen, share with collaborators or publish them.

## Pitfalls

- **Network needed.** The client uses remote servers. Offline work is limited.
- **Pick the right application type.** A deterministic and a stochastic application of one model give different views. Compare them when copy numbers are small.
- **Geometry sets the cost.** A fine 3D mesh makes a spatial run slow and large.
- **Cite the resource.** The site asks for the VCell Resource to be acknowledged in publications, with NIH grant R24 GM134211.
- **Version differences.** The download page and the GitHub release tag use different numbers. Check which version you installed before following a tutorial.

## Further reading

- Project site: https://vcell.org/
- Source and licence: https://github.com/virtualcell/vcell
- Resasco DC, Gao F, Morgan F, Novak IL, Schaff JC, Slepchenko BM (2012). Virtual Cell: computational tools for modeling in cell biology. WIREs Syst Biol Med 4:129-140. https://doi.org/10.1002/wsbm.165
- Moraru II, Schaff JC, Slepchenko BM, et al. (2008). Virtual Cell modelling and simulation software environment. IET Syst Biol 2:352-362. https://doi.org/10.1049/iet-syb:20080102

---

Cite: Resasco DC, Gao F, Morgan F, Novak IL, Schaff JC, Slepchenko BM (2012). Virtual Cell: computational tools for modeling in cell biology. WIREs Syst Biol Med 4:129-140. doi:10.1002/wsbm.165

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/vcell).
