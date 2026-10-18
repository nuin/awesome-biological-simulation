# BioDynaMo

> A C++ platform for 3D agent-based simulation of cells and tissues, with a command-line project tool and ParaView output.

Licence: Apache-2.0 · [Source code](https://github.com/BioDynaMo/biodynamo)

## What it simulates

BioDynaMo is a platform to create, run and visualise 3D agent-based simulations. Agents are objects such as spherical cells or neurites. Each agent carries behaviors, small pieces of code that run every time step: grow, divide, secrete a substance, move along a gradient. Substances diffuse on a grid between the agents.

The core is C++ and tuned for many cores. The project's own description lists three aims: speed, reusable modules for specific biological behaviors, and visual output. The README and demo folder cover neuroscience (a pyramidal cell), tumour growth, cell sorting (soma clustering), gene regulation, epidemiology and flocking. A simulation is a C++ project that you write against the BioDynaMo library, not a parameter file for a fixed model.

## When to use it

Use BioDynaMo when your model needs very many agents in 3D with mechanics, diffusing substances and custom behavior code, and you are comfortable writing C++.

Alternatives:

- [NetLogo](netlogo.md) fits small agent models written in a few lines, with a GUI and no compiler.
- [Artistoo](artistoo.md) fits cell shape and migration as a cellular Potts model in the browser.
- [tyssue](tyssue.md) fits epithelial tissue mechanics in Python.

## Install

This guide has no run recipe. The installer is a script that fetches and builds a large stack, and each simulation is a C++ project that is compiled before it runs. The sandbox on this site starts a read-only container with no network, so it can neither install the stack nor compile a project.

The official route, from the [installation page](https://github.com/BioDynaMo/biodynamo/blob/master/doc/user_guide/installation.md):

```
curl https://biodynamo.github.io/install | bash
```

It installs the prerequisites, including ROOT, ParaView and Qt5, into `$HOME/biodynamo-vX.Y.Z`. In every new terminal run `source <installation-directory>/bin/thisbdm.sh`. To pin a version, set `BDM_INSTALL` to a commit hash before the command, or to `master` for the development version.

Supported platforms in that page: Ubuntu 20.04, 22.04 and 24.04, Ubuntu 26.04 (x86_64, experimental), and macOS newer than 12.0 on Intel and ARM. Windows and WSL are not supported. The latest GitHub release is v1.04 (October 2022); a v1.05 tag exists. The licence is Apache-2.0.

A browser route needs no install: the README links a GitHub Codespace (`BioDynaMo/biodynamoOnline`) with a pre-configured environment and a VNC desktop for ParaView.

## A first run

Adapted from the [Hello World page](https://github.com/BioDynaMo/biodynamo/blob/master/doc/user_guide/hello_world.md). The default model is one static cell.

```
biodynamo new hello_world
cd hello_world
biodynamo build
biodynamo run
```

The output ends with "Simulation completed successfully". To make the cell divide, add one line to the simulate function in `src/hello_world.h`, after the cell is created and before it is added to the resource manager:

```cpp
cell->AddBehavior(new GrowthDivision(32, 3000));
```

Rebuild and rerun. The page says to run more steps to see the cell divide.

## Reading the output

Visualization is off by default. The [visualization page](https://github.com/BioDynaMo/biodynamo/blob/master/doc/user_guide/visualization.md) enables it in a `bdm.toml` file in the project folder:

```
[visualization]
export = true
interval = 1

	[[visualize_agent]]
	name = "Cell"
```

With this, a visualization file is exported every `interval` steps and opened in ParaView. The page suggests about 2000 steps for the hello world example so the cells have time to divide. The `bdm view` command in the Codespace quick start opens ParaView.

## Pitfalls

- **Compile step.** `biodynamo build` compiles C++ against ROOT. The first build is slow and needs a compiler on the machine.
- **Environment script.** Commands fail until `thisbdm.sh` has been sourced in that terminal.
- **Visualization costs time.** It is off for performance. Export every step only for short runs.
- **Platform.** Only the Ubuntu and macOS versions listed under Install are supported. Developers build from source with the developer guide.
- **Version in methods.** The README asks for the exact version string (`biodynamo --version`, form `vMAJOR.MINOR.PATCH-SHA`) in a paper's methods.

## Further reading

- Source and README: https://github.com/BioDynaMo/biodynamo
- User guide: https://www.biodynamo.org/user-guide/
- Demos: https://github.com/BioDynaMo/biodynamo/tree/master/demo
- Breitwieser L et al. (2022). Bioinformatics 38(2):453-460. https://doi.org/10.1093/bioinformatics/btab649
- Breitwieser L et al. (2023). High-performance and scalable agent-based simulation with BioDynaMo. PPoPP '23. https://doi.org/10.1145/3572848.3577480

---

Cite: Breitwieser L, Hesam A, de Montigny J, Vavourakis V, Iosif A, Jennings J, Kaiser M, Manca M, Di Meglio A, Al-Ars Z, Rademakers F, Mutlu O, Bauer R (2022). BioDynaMo: a modular platform for high-performance agent-based simulation. Bioinformatics 38(2):453-460. doi:10.1093/bioinformatics/btab649

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/biodynamo).
