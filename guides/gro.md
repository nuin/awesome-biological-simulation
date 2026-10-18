# gro

> Simulator for growing bacterial micro-colonies in two dimensions, with a language for programming gene circuits, cell signalling and cell-cell communication.

Licence: LicenseRef-UW-Open-Source-NonCommercial · [Source code](https://github.com/klavinslab/gro)

## What it simulates

gro simulates a micro-colony of bacteria (or yeast) growing on a flat surface, one cell at a time. Each cell has a position, an orientation and a volume. Cells grow, divide, push on each other and carry a small program that you write. The program decides what the cell does: make or lose a protein, send or sense a signal, divide, die, move.

The language is the Cell Control Language (CCL), in `.gro` files. A program is a set of rules of the form `condition : { actions }`. Since v1.1.0 you can write the same programs in Python instead, as a class that subclasses `Program` with `State` fields and decorated rule methods. Both frontends share one C++ simulator.

From the CCL reference:

- A cell is 1 micrometre across and starts 2 micrometres long, so its volume is 1.57 fL. By default 10 pixels equal 1 micrometre.
- Volume grows exponentially and doubles in about 20 minutes. A cell divides at about 3.14 fL, with some random variation, and the daughter takes about half the volume.
- On division the program is copied and numeric local variables are halved. That is why a protein count dilutes as the cells grow.
- Signals diffuse on a 160 by 160 finite-element grid with 0.5 micrometres per element, and decay at a rate you set.
- `rate(k)` is true with probability k times dt per tick, which is how stochastic reactions are written.

## When to use it

Use gro to prototype a synthetic gene circuit in a growing colony and to watch it work: a quorum-sensing pattern, a band-pass filter on a signal, a toggle or oscillator passed down through divisions.

- Use [CellModeller](cellmodeller.md) when 3D rod mechanics and very large colonies matter and you have an OpenCL device.
- Use [NetLogo](netlogo.md) for general agent-based models without cell physics.
- Use [GillesPy2](gillespy2.md) for a stochastic circuit in one well-mixed compartment.

## Install

gro is a desktop program with a Qt window, and its licence limits use to non-commercial work. This site gives no ready-to-run recipe for it, for those two reasons. Build and run it on your own computer.

The README says v1.1.0 and later are source-only, and binary releases are deferred. The newest tag on GitHub is v1.1.0-rc.1 (18 May 2026). The README lists these requirements: Qt 6 and CMake 3.24 or newer. The libraries CCL, Chipmunk2D and pybind11 are fetched during the build.

On macOS:

```bash
brew install qt cmake bison flex m4 python@3.13
git clone https://github.com/klavinslab/gro.git
cd gro
cmake -S . -B build
cmake --build build -j
open gro.app
```

On Linux:

```bash
sudo apt install qt6-base-dev cmake bison flex python3-dev
git clone https://github.com/klavinslab/gro.git
cd gro
cmake -S . -B build
cmake --build build -j
./build/gro
```

Keep the program next to the `examples/`, `include/` and `python/` folders. At launch the binary walks up from its own folder to find them.

**Licence.** gro uses the UW Open Source License. It grants a worldwide, royalty-free, non-commercial licence to use, change and distribute the software. Copies and derivative works must carry a licence that prohibits commercial use, keep the University of Washington copyright notice and attribute the source. For commercial use the licence file says to write to license@uw.edu. The identifier in the page header is a label chosen here, not an SPDX identifier.

## A first run

Adapted from the CCL reference, Getting Started section: https://github.com/klavinslab/gro/blob/master/docs/gro.md

The simplest program, `examples/growth.gro`:

```
include gro

set ( "dt", 0.1 );   // fast and inaccurate

program p() := {

  skip();

};

ecoli ( [ x := 0, y := 0 ], program p() );
```

Start gro, choose File, Open and pick the file (or pick it from the Examples menu). The window shows one E. coli cell at the origin that grows and divides into a colony. The `dt` setting is the time step in minutes. A larger value is faster and less accurate. Edit the file in a text editor and choose Reload.

The reference then adds, step by step:

- A `dilute(m)` program in which a cell starts with `m` copies of GFP, with no production, so that the GFP count halves at each division.
- A production and decay program with `rate ( k1 ) : { gfp := gfp + 1 }` and `rate ( k2 * gfp ) : { gfp := gfp - 1 }`.
- A signal, `ahl := signal ( 1, 0.01 )`, with a diffusion rate and a degradation rate, and a sensor program that reads it with `get_signal`.

## Reading the output

Most of the output is visual: cell shapes, with fluorescence shown as colour. The `gfp_saturation_max` and `gfp_saturation_min` parameters set how bright a given GFP count looks, like the gamma setting on a microscope.

For numbers, write them out yourself. A program can call `message` to show text for a selected cell. The reference shows an `output(delta)` program that uses `print` to give a cell's id, its age and `gfp / volume` every `delta` minutes, and says that `fopen` and `fprint` write to a file instead. Keep the age counter in a record, because gro halves numeric locals but not record fields when a cell divides.

The reference states two rough sizes for a check: the average cell volume is about 2.36 fL, so 100 copies of a protein per cell is about 42 per fL. These numbers come from the reference, not from a run on this site.

## Pitfalls

- **Time step.** With `dt = 0.1`, a `rate()` guard fires at most 10 times per minute. A reaction that needs more than that falls behind. The reference uses `dt = 0.01` for its mRNA and protein example.
- **Simulation time is not real time.** The colony grows exponentially, so the work per simulated minute grows too.
- **Locals halve at division.** A counter that must survive a division goes in a record.
- **Non-commercial licence.** Check it before using gro in a company or a paid service.

## Further reading

- Source and README: https://github.com/klavinslab/gro
- CCL reference: https://github.com/klavinslab/gro/blob/master/docs/gro.md
- Python reference: https://github.com/klavinslab/gro/blob/master/docs/python.md
- Original site: http://depts.washington.edu/soslab/gro/
- Paper: Jang SS et al. (2012) Specification and simulation of synthetic multicelled behaviors. ACS Synthetic Biology 1:365-374. https://doi.org/10.1021/sb300034m

---

Cite: Jang SS, Oishi KT, Egbert RG, Klavins E (2012). Specification and simulation of synthetic multicelled behaviors. ACS Synth Biol 1:365-374. doi:10.1021/sb300034m

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/gro).
