# CompuCell3D

> Run a cellular Potts (Glazier-Graner-Hogeweg) tissue model written as a CompuCell3D Python script, without the Player GUI.

Licence: MIT · [Source code](https://github.com/CompuCell3D/CompuCell3D)

## What it simulates

CompuCell3D simulates tissues of many cells with the cellular Potts model, also called the Glazier-Graner-Hogeweg (GGH) model. Space is a regular lattice. Each cell is the set of lattice sites that carry its label. The simulation proceeds in Monte Carlo steps (MCS). In a step the program tries to copy the label of one site onto a neighbouring site. It accepts or rejects each copy from the change in an energy function, with some randomness set by a temperature-like fluctuation amplitude.

The energy function is built from plugins that you switch on. Typical terms are a contact energy between cell types (adhesion), a volume constraint that pulls each cell toward a target volume, and surface, chemotaxis or elongation terms. Steppables are Python classes that run at set steps and change cells or read them out. Diffusing chemicals are solved on the same lattice with PDE solvers. Intracellular networks written in SBML can run inside each cell.

The catalog entry describes this as simulation of multicellular tissue morphogenesis with PDE fields and intracellular SBML networks. Time is in MCS and length is in lattice sites. You set how those map to seconds and micrometres.

## When to use it

Use CompuCell3D when cell shape and cell-cell contact matter: sorting by differential adhesion, branching, wound healing, somite or vascular patterning.

- Use [Tyssue](tyssue.md) when you model an epithelium as a vertex mesh, where each cell is a polygon with shared edges.
- Use [Artistoo](artistoo.md) when you want the same cellular Potts model in the browser, in two dimensions.
- Use [NetLogo](netlogo.md) when cells are points or simple agents and shape does not matter.

## Install it yourself

The README gives the conda route:

```bash
conda install -c compucell3d -c conda-forge cc3d
```

Pin the version in a fresh environment:

```bash
micromamba create -n cc3d -c compucell3d -c conda-forge cc3d=4.10.0
```

The package exists. The channel page https://anaconda.org/compucell3d/cc3d lists cc3d 4.10.0 (released 11 October 2026, MIT) for linux-64, osx-64, osx-arm64 and win-64, built for Python 3.12 on Linux. There is no Linux ARM build. The package pulls in VTK 9.2, Boost, NumPy 2.2 and a Jupyter stack, so the environment is large.

Three entry points follow from the README:

- `python -m cc3d.player5` starts the Player, the graphical interface.
- `python -m cc3d.twedit5` starts the model editor.
- `python -m cc3d.run_script -i <full path to .cc3d file>` runs a simulation without a graphical interface.

The recipe uses only the last one, on linux/amd64.

## Run the tested example

This recipe builds CompuCell3D in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 14.7 s. CompuCell3D has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [compucell3d-recipe.tar.gz](https://biosimhub.pages.dev/guides/compucell3d/compucell3d-recipe.tar.gz) (Dockerfile, run_cc3d.py, example model.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf compucell3d-recipe.tar.gz
   cd compucell3d
   sh run.sh
   ```

![Terminal recording of the CompuCell3D example run](https://biosimhub.pages.dev/media/compucell3d/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/compucell3d:4.10.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/compucell3d:4.10.0 python /opt/run_cc3d.py /work/in/model.py \
    --steps 1000 --seed 42 --report 100 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `project/Simulation/model.py` | 3.0 KB |
| `project/model.cc3d` | 115 B |
| `run_log.txt` | 32 B |

<details><summary>First lines of <code>project/Simulation/model.py</code></summary>

```
"""Cell sorting in two dimensions (cellular Potts model), written for CompuCell3D 4.x.

Adapted from CompuCell3D/core/Demos/PyCoreSpecs/SortingDemo (MIT). Steps, seed and report
interval come from the environment; a steppable writes cell_stats.csv.
"""
import os

from cc3d import CompuCellSetup
from cc3d.core.PyCoreSpecs import Metadata, PottsCore, CellTypePlugin, VolumePlugin, ContactPlugin
from cc3d.core.PyCoreSpecs import NeighborTrackerPlugin, BlobInitializer
from cc3d.core.PySteppables import SteppableBasePy

```

</details>

<details><summary>First lines of <code>project/model.cc3d</code></summary>

```
<Simulation version="4.4.0">
   <PythonScript Type="PythonScript">Simulation/model.py</PythonScript>
</Simulation>
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
vtk not found. Ignoring for now
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--steps` | Monte Carlo steps | 1000 | 1 to 100000 |
| `--report` | Statistics interval (steps) | 100 | 1 to 100000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Python-specification demo `SortingDemo`: https://github.com/CompuCell3D/CompuCell3D/tree/master/CompuCell3D/core/Demos/PyCoreSpecs/SortingDemo

A project is a `.cc3d` file that lists its scripts. A project made only from a Python script needs a manifest like this one:

```xml
<Simulation version="4.4.0">
   <PythonScript Type="PythonScript">Simulation/model.py</PythonScript>
</Simulation>
```

The script `Simulation/model.py` registers the model with the specification classes:

```python
from cc3d import CompuCellSetup
from cc3d.core.PyCoreSpecs import Metadata, PottsCore, CellTypePlugin, VolumePlugin, ContactPlugin, BlobInitializer

CompuCellSetup.register_specs(Metadata(num_processors=4))
CompuCellSetup.register_specs(PottsCore(dim_x=100, dim_y=100, steps=16000, neighbor_order=2))
CompuCellSetup.register_specs(CellTypePlugin("Condensing", "NonCondensing"))
# volume constraint, contact energies and BlobInitializer follow, then:
CompuCellSetup.run()
```

Two cell types start as a mixed blob of 40 pixel diameter. The contact energies are 2 between two Condensing cells, 11 between a Condensing and a NonCondensing cell, 16 between two NonCondensing cells and 16 for either type against the medium. Cells that stick to their own type more strongly than to the other type will sort.

Run it with the headless command. The script options are `-i` (project), `-o` (output folder), `-f` (snapshot output frequency, 0 for none) and `-c` (core name for the VTK files).

The recipe's example model is the same sorting model, shortened to 1000 steps and on one processor. It adds a seed, a neighbour-tracker plugin and a small steppable. The steppable writes `cell_stats.csv` every 100 steps.

## Reading the output

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

The steppable writes one row per report, with these columns: `mcs`, `cells`, `mean_volume`, `heterotypic_boundary` and `homotypic_boundary`. The boundary columns add up the common surface area between neighbouring cells of different types and of the same type, each shared boundary counted once.

If sorting works, `heterotypic_boundary` falls as the run goes on, because the two types separate into a core and a shell, and `homotypic_boundary` rises. `mean_volume` stays near the target volume of 25 with some scatter, because the volume constraint is a penalty and not a hard limit. The cell count does not change, since the model has no growth or division.

The helper passes `-o cc3d_output` as the output folder and leaves the snapshot frequency at its default of 0.

## Pitfalls

- **Full paths.** The README asks for the full path to the `.cc3d` file.
- **Steps are in the script.** In Python-specification models the `steps` argument of `PottsCore` sets the run length. The command line has no step option.
- **Seeds.** Without `random_seed` in `PottsCore`, two runs of the same model differ. Set it for a repeatable result.
- **Units.** One MCS is not a fixed time. Choose a time scale by comparing a measured rate with the simulated one.
- **Threads.** `Metadata(num_processors=n)` sets the thread count. The recipe's model uses 1, to match the one-CPU limit.
- **Version pinning.** The demos change between releases. Match the demo folder to your installed version.

## Further reading

- Project and README: https://github.com/CompuCell3D/CompuCell3D
- Project site and downloads: https://compucell3d.org/
- Python scripting manual: https://pythonscriptingmanual.readthedocs.io/en/latest/
- Conda package: https://anaconda.org/compucell3d/cc3d
- Paper: Swat MH et al. (2012) Multi-scale modeling of tissues using CompuCell3D. Methods in Cell Biology 110:325-366. https://doi.org/10.1016/B978-0-12-388403-9.00013-8

---

Cite: Swat MH et al. (2012). Multi-scale modeling of tissues using CompuCell3D. Methods Cell Biol 110:325-366. doi:10.1016/B978-0-12-388403-9.00013-8

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/compucell3d).
