# CellModeller

> Agent-based simulation of growing and dividing bacterial colonies, with rod-shaped cell mechanics, gene regulation and cell-cell signalling, run through OpenCL.

Licence: BSD-3-Clause · [Source code](https://github.com/cellmodeller/CellModeller)

## What it simulates

CellModeller is a Python framework for simulating large populations of growing and dividing cells, such as bacterial colonies and biofilms. Each cell is an agent. The framework combines three parts that you pick when you write a model:

- A biophysics module. The project page names a published biophysical model of rod-shaped bacteria (Rudge et al. 2012, 2013). Cells grow, divide and push on their neighbours in it.
- A regulation module, which holds each cell's internal state, such as gene expression, and runs ODEs coupled to growth and division.
- A signalling module, for communication between cells.

The project page lists simulations of more than 100,000 cells in 3D, constraints that model growth chambers, channels and surfaces, and PDF and video output. The heavy numerical parts run through OpenCL and PyOpenCL.

You describe the cell behaviour in a Python file with four functions: `setup(sim)` builds the modules and places the first cell, `init(cell)` sets a new cell's attributes, `update(cells)` runs every step and may flag a cell for division, and `divide(parent, d1, d2)` sets the attributes of the two daughters.

## When to use it

Use CellModeller when the physical contact of rod-shaped cells shapes the result: colony growth in a chamber, mechanical ordering of cells, or patterns that arise when signals diffuse through a growing colony.

- Use [Cytosim](cytosim.md) when you model filaments and motors inside one cell.
- Use [NetLogo](netlogo.md) for simple agent models where cell shape and mechanics do not matter.
- Use [Tyssue](tyssue.md) for epithelial sheets where cells are polygons.

## Install

CellModeller needs an OpenCL device. This site gives no ready-to-run recipe for it, because the biophysics solver is written as OpenCL kernels and the project describes it as GPU-accelerated, and the viewer needs OpenGL and Qt. Run it on a machine with a working OpenCL driver.

Since release v4.5.0 (12 October 2026) the repository holds the core simulator only. The cell models and examples moved to a second repository, `cmcomponents` (v1.1.0). To get both, clone and install it:

```bash
python3 -m venv cm
. cm/bin/activate
git clone https://github.com/cellmodeller/cmcomponents.git
pip install ./cmcomponents
```

The `cmcomponents` project file lists CellModeller v4.5.0 from GitHub as a dependency, so pip fetches it. CellModeller is not on PyPI. Its `setup.py` lists numpy, scipy, pyopengl, mako, pyqt5, pyopencl, reportlab, matplotlib and `setuptools>=70,<82`. The upper bound is there because the code uses `pkg_resources`.

The project page also names a folder for results. Create it before a run: `mkdir -p ~/cellmodeller/data`.

## A first run

Adapted from `Examples/ex1_simpleGrowth.py` in the cmcomponents repository, and from `scripts/batch.py` in the CellModeller repository: https://github.com/cellmodeller/cmcomponents/tree/main/Examples

Save the model as `ex1_simpleGrowth.py`:

```python
import random
from cellmodeller.regulation.module_regulator import ModuleRegulator
from cmcomponents.biophysics.bacterial_models import CLBacterium

def setup(sim):
    biophys = CLBacterium(sim, jitter_z=False, max_cells=100000, gamma=100.)
    regul = ModuleRegulator(sim, sim.moduleName)
    sim.init(biophys, regul, None, None)
    sim.addCell(cellType=0, pos=(0, 0, 0), dir=(1, 0, 0))
    sim.pickleSteps = 100
    sim.saveOutput = True

def init(cell):
    cell.targetVol = 3.5 + random.uniform(0.0, 0.5)
    cell.growthRate = 1.0

def update(cells):
    for (id, cell) in cells.items():
        if cell.volume > cell.targetVol:
            cell.divideFlag = True

def divide(parent, d1, d2):
    d1.targetVol = 3.5 + random.uniform(0.0, 0.5)
    d2.targetVol = 3.5 + random.uniform(0.0, 0.5)
```

The upstream example also adds a renderer for the viewer. This listing leaves it out for batch use. Run it without the GUI with the batch script. Give the OpenCL platform and device numbers, or leave them out to be asked:

```bash
python scripts/batch.py ex1_simpleGrowth.py 0 0
```

The batch script builds a `Simulator` with a time step of 0.025 and steps it until the colony reaches 50,000 cells less a buffer of 256.

## Reading the output

With `saveOutput = True`, the simulator writes a pickle of the cell states every `pickleSteps` steps (100 here) into the output folder. Each pickle holds the cells at that step, with their positions, lengths, volumes and the attributes you set. Load them with Python's `pickle` module, or use the helper scripts in the repository's `scripts` folder: `length_histogram.py`, `spatial_analyze.py`, `contact_graph.py`, `draw_2d_pdf.py`, and `video.sh`.

In the example every cell grows at rate 1.0 and divides when its volume passes a target of 3.5 to 4.0. The cell count therefore grows roughly exponentially at first, then more slowly in 3D as the colony crowds. No numbers are quoted here, because none appear in the project's documents.

## Pitfalls

- **No OpenCL device, no run.** `pyopencl` must find a platform. On a laptop, list devices with `pyopencl.get_platforms()` and pick numbers from that list.
- **Version split.** Examples written for older releases import from `CellModeller.` paths with capital letters. Since v4.5.0 names are snake case (`cellmodeller.simulator`), and models import biophysics from `cmcomponents`.
- **Licence wording differs.** The project page says MIT. The `licence.txt` in the repository is the BSD 3-clause text. This guide follows the file.
- **Memory.** `max_cells` sets the maximum number of cells the biophysics module handles. Raise it only as far as the device memory allows.
- **Random numbers.** The example uses Python's `random` module without a seed. Seed it for a repeatable colony.

## Further reading

- Project page: https://cellmodeller.github.io/CellModeller/
- Core repository: https://github.com/cellmodeller/CellModeller
- Models and examples: https://github.com/cellmodeller/cmcomponents
- Paper: Rudge TJ et al. (2012) Computational modeling of synthetic microbial biofilms. ACS Synthetic Biology 1:345-352. https://doi.org/10.1021/sb300031n

---

Cite: Rudge TJ, Steiner PJ, Phillips A, Haseloff J (2012). Computational modeling of synthetic microbial biofilms. ACS Synth Biol 1:345-352. doi:10.1021/sb300031n

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cellmodeller).
