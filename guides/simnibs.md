# SimNIBS

> Finite-element simulation of the electric fields that TMS, tDCS and other non-invasive brain stimulation induce in individualised head models.

Licence: GPL-3.0-or-later · [Source code](https://github.com/simnibs/simnibs)

## What it simulates

SimNIBS calculates the electric field that non-invasive brain stimulation produces inside the head. It covers transcranial magnetic stimulation (TMS), where a coil induces currents in the brain, and transcranial electric stimulation such as tDCS and tACS, where electrodes on the scalp inject current. It also supports EEG forward modelling and optimisation of coil position or electrode montage.

The model is a head mesh built from a person's MRI. The segmentation pipeline `charm` labels the tissues (skin, skull, cerebrospinal fluid, grey matter, white matter and others). It then builds a tetrahedral mesh. SimNIBS assigns a conductivity to each tissue and solves the electromagnetic problem with the finite element method. The result is a mesh file with the electric field in every element, which you can view in the GUI or Gmsh, or process in Python or MATLAB.

Simulations are quasi-static: the field follows the stimulator current instantly, with no wave propagation. SimNIBS predicts the field, not the neural response.

## When to use it

Use SimNIBS to plan or analyse a stimulation study: where a coil or electrode pair puts the field in one person's cortex, how a different montage changes it, which position best hits a target.

- Use [The Virtual Brain](tvb.md) to model what a network of brain regions does with a perturbation, once the field is known.
- Use [Simbrain](simbrain.md) for teaching-scale neural networks rather than head physics.
- Use [NetPyNE](netpyne.md) when the question is how single neurons respond to an applied field.

## Install

SimNIBS is not a pip or conda-forge package. The documentation (version 4.6.0) gives an installer for each system and says an installation takes about 3 GB of disk space.

- **Windows:** run `simnibs_installer_windows.exe`.
- **Linux:** run `tar -xzf simnibs_installer_linux.tar.gz` and then `simnibs_installer/install`. A silent mode with no GUI exists (`install -h`).
- **macOS:** run `simnibs_installer_macos.pkg`. Only Apple Silicon is supported since version 4.5.

The installer takes 5 to 10 minutes. An advanced route builds a conda environment from the project's environment file and installs a SimNIBS wheel from the GitHub release page.

No runnable recipe is provided here. The input is an individual head model that `charm` builds from MRI, and the installation alone takes about 3 GB, far beyond a small example. Download the installer and the example dataset from the SimNIBS site.

## A first run

The scripting tutorial uses the example dataset, which contains the head model of the subject "ernie". The Python interface builds a nested structure and hands it to `run_simnibs`:

```python
from simnibs import sim_struct, run_simnibs

s = sim_struct.SESSION()
s.subpath = 'm2m_ernie'      # head mesh folder
s.pathfem = 'tutorial/'      # output folder

tdcslist = s.add_tdcslist()
tdcslist.currents = [-1e-3, 1e-3]       # 1 mA, cathode and anode
cathode = tdcslist.add_electrode()
cathode.channelnr = 1
cathode.dimensions = [50, 70]           # mm
cathode.shape = 'rect'
cathode.thickness = 5
cathode.centre = 'C3'
cathode.pos_ydir = 'Cz'
anode = tdcslist.add_electrode()
anode.channelnr = 2
anode.dimensions = [30, 30]
anode.shape = 'ellipse'
anode.thickness = 5
anode.centre = 'C4'
# ... then: run_simnibs(s)
```

To build the head model from MRI instead, run `charm ernie org/ernie_T1.nii.gz org/ernie_T2.nii.gz`. It makes a folder `m2m_ernie` with the segmentation and mesh. Run scripts with `simnibs_python`.

Adapted from <https://simnibs.github.io/simnibs/build/html/tutorial/scripting.html> and <https://simnibs.github.io/simnibs/build/html/tutorial/head_meshing.html>.

## Reading the output

Each simulation writes mesh files (`.msh`) to the output folder. They hold the field values per element or node, such as the electric field vector and its magnitude, with the tissue labels. Open them in the SimNIBS GUI or in Gmsh. The Python and MATLAB interfaces can read them for further analysis.

For a tDCS run with a cathode and an anode, expect the field to be strongest in the cortex under and between the electrodes and weaker elsewhere. For a TMS run, it peaks in the cortex beneath the coil centre. The head model decides much of this, because skull and cerebrospinal fluid shape current paths.

## Pitfalls

- **Dataset version.** The documentation says earlier versions of the example dataset are incompatible with SimNIBS 4.
- **Segmentation quality.** `charm` needs a T1-weighted image. A T2-weighted image is optional but recommended, because with T1 alone the skull is less accurate. Poor affine registration produces wrong segmentations; the documentation has a tutorial on fixing it.
- **Licence of datasets.** Some example datasets (Ernie Extended, the non-human primate models) are CC BY-NC 4.0.
- **Linux GUI.** The documentation notes the GUI fails on some distributions, in particular on Wayland, and suggests preloading `libstdc++.so.6`.
- **Intel Macs.** Support for Intel-based Macs ended with version 4.5.
- **Conductivities are assumptions.** Tissue conductivities are literature values; the field scales with them. Treat the numbers as estimates, not measurements.

## Further reading

- Documentation: https://simnibs.github.io/simnibs/build/html/index.html
- Installation: https://simnibs.github.io/simnibs/build/html/installation/simnibs_installer.html
- Head modelling with charm: https://simnibs.github.io/simnibs/build/html/tutorial/head_meshing.html
- Source: https://github.com/simnibs/simnibs
- Paper: Saturnino GB, Madsen KH, Thielscher A (2019). Electric field simulations for transcranial brain stimulation using FEM: an efficient implementation and error analysis. Journal of Neural Engineering 16:066032. https://doi.org/10.1088/1741-2552/ab41ba

---

Cite: Saturnino GB, Madsen KH, Thielscher A (2019). Electric field simulations for transcranial brain stimulation using FEM: an efficient implementation and error analysis. Journal of Neural Engineering 16:066032. doi:10.1088/1741-2552/ab41ba

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simnibs).
