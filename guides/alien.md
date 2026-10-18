# ALIEN

> A GPU particle engine for artificial life, where cells with small neural networks form creatures that mutate, compete and evolve.

Licence: BSD-3-Clause · [Source code](https://github.com/chrxh/alien)

## What it simulates

ALIEN (Artificial LIfe ENvironment) simulates a 2D world made of particles. Particles bond into elastic solids, flow as fluids, or act as cells with a function. The README lists 15 cell types, among them sensors, muscles, attackers, injectors, digestors, memory cells and communicators.

Each cell runs its own small neural network. A network of connected cells is a creature. A creature carries a genome, a blueprint of genes that its constructor cells read to build offspring cell by cell.

Evolution has no fitness function. Mutations change neural networks, cell properties and genome structure, and the mutation rates can themselves mutate. Selection comes from limited energy, predation and competition for space. Energy circulates between cells, free energy particles and an optional external pool, and it never appears from nothing.

The engine runs entirely on the graphics card (CUDA, with an AMD HIP build) and draws through Vulkan. The README states that it handles worlds of millions of particles in real time. A running world can be edited at any moment: draw matter, push creatures, change the physics parameters.

## When to use it

Use ALIEN to watch ecosystems form from a seeded population, to design creatures in the genome editor, or to run long evolution experiments with the dashboard of lineages and population statistics.

Alternatives:

- [NetLogo](netlogo.md) fits rule-based agents on a grid, with models you can read in a few lines and no GPU.
- [Artistoo](artistoo.md) runs cellular Potts models of cell shape and movement in the browser.
- [Cytosim](cytosim.md) fits when the question is about filaments and motors, not whole organisms.

## Install

This guide has no run recipe. ALIEN needs an NVIDIA GPU with compute capability 7.5 or higher (GeForce RTX 20 series or newer) or an AMD GPU of the RDNA2 generation or newer, and a driver with Vulkan 1.3. The README states "There is no GUI in the image" for its Docker build, and the desktop program is a Vulkan window. The sandbox on this site has no GPU and no display, so ALIEN cannot run there.

Routes from the README (latest tagged release v4.12.3, December 2024; the README points to a nightly build as the main download):

- **Windows, prebuilt.** Download and unpack https://alien-project.org/files/alien-develop.zip. It holds `alien.exe` for NVIDIA and `alien-amd.exe` for AMD. Start it from the unpacked folder, or it will not find its resource folder.
- **Linux, from source.** There is no Linux binary. Install the CUDA Toolkit 11.2 or newer (ROCm 7.2 or newer for AMD), GCC, ninja-build, pkg-config and the X11 development libraries, then:

```
git clone --recursive https://github.com/chrxh/alien.git
cd alien
cmake --preset ninja
cmake --build --preset ninja-release
```

The executable `build-ninja/Release/alien` has to be started from that folder.

- **Headless, on a GPU host.** The image `chrxh/alien:nightly` holds the command-line program `alien-cli`. With an NVIDIA GPU and the NVIDIA container toolkit:

```
docker run --rm --gpus all -v "$PWD":/data --entrypoint alien-cli chrxh/alien:nightly -i /data/example.sim -o /data/output.sim -t 1000
```

The licence is BSD-3-Clause.

## A first run

Adapted from the built-in [Getting started](https://github.com/chrxh/alien/blob/master/resources/docs/getting-started.md) chapter. ALIEN starts with a simulation already loaded.

1. Press Space to start the simulation and Space again to pause it.
2. Zoom with the mouse wheel and drag with the middle mouse button to move. Zoom in until single cells show.
3. Press Alt+O for the cell info overlay, which labels each cell with its type.
4. Press Alt+B to open the Browser. The Simulations tab lists featured simulations and community uploads. Double-click one to download and open it.
5. Press Alt+E for edit mode, choose the Apply forces tool and drag across the world to push things around.

The window Temporal control (Alt+1) shows time steps per second. The documentation is built into the program (F1).

## Reading the output

- The main view is the output: creatures and particles drawn live. The info overlay names the cell types.
- The evolution dashboard shows lineages, population statistics and long-term plots.
- Simulation files (`.sim`) hold the full world state. `alien-cli -i in.sim -o out.sim -t 1000` runs 1000 time steps and writes the end state. Without `-t` it runs until Q or Ctrl+C.
- Autosave keeps save points, so you can go back to an earlier moment.

## Pitfalls

- **GPU class.** Older cards or integrated graphics do not work. On a machine with two GPUs, the display must be on the card ALIEN picks, the one with the highest compute capability.
- **Working folder.** Start the executable from its own folder. Keep the install path free of non-English characters, and give ALIEN write access to it.
- **Large worlds are slow** on modest cards. Pick a smaller world from the Browser first.
- **No fitness function.** Populations can die out or stall. Mutation settings and energy inflow decide the outcome, so read the evolution chapter before a long run.
- **The paper is early.** The cited 2008 article describes the beginnings of ALIEN, and the README says the current simulator differs substantially. It also welcomes citing the repository.

## Further reading

- Source and README: https://github.com/chrxh/alien
- Built-in documentation: https://github.com/chrxh/alien/tree/master/resources/docs
- Project site: https://alien-project.org
- Heinemann C (2008). Artificial Life Environment. Informatik-Spektrum 31:55-61. https://doi.org/10.1007/s00287-007-0205-1

---

Cite: Heinemann C (2008). Artificial Life Environment. Informatik-Spektrum 31:55-61. doi:10.1007/s00287-007-0205-1

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/alien).
