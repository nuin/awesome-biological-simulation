# TorchCor

> Finite-element cardiac electrophysiology on heart meshes in PyTorch, from monodomain tissue models to reaction-eikonal activation maps and 12-lead ECGs.

Licence: MIT · [Source code](https://github.com/sagebei/torchcor)

## What it simulates

TorchCor simulates the spread of electrical activation through heart tissue. It solves the monodomain model, a reaction-diffusion equation, on a finite-element mesh. Each node carries a cell model that produces the ionic current. The diffusion step uses a conjugate-gradient solve, and everything runs as PyTorch tensor operations.

Three workflows are documented:

- **Monodomain.** Implicit diffusion plus an explicit ionic update at each time step. The result is the transmembrane voltage Vm at every node, sampled at an interval you choose.
- **Reaction-eikonal.** An eikonal solver computes the arrival time of the wavefront from conduction velocities. A reaction step then fires each cell's action potential at that time. This costs much less than the monodomain model.
- **ECG.** A lead-field (reciprocity) solver on a heart-torso mesh turns Vm into body-surface signals, including the 12-lead ECG.

The cell models in `torchcor.ionic` are AlievPanfilov, BuenoOrovio, CourtemancheRamirezNattel, MitchellSchaeffer, ModifiedMS2v, OHaraRudy, TenTusscherPanfilov, Tomek19, Tomek20 and TWorld. You assign conductivities per mesh region, and stimuli are lists of nodes with a start time, duration and intensity.

## When to use it

Use TorchCor when you have a whole-heart or atrial mesh with millions of nodes and a CUDA GPU. The documented workflow is built around that case.

- Use [openCARP](opencarp.md) when you want an established CPU and cluster cardiac simulator, with a single-cell tool (`bench`) that runs without a mesh.
- Use a reaction-eikonal run inside TorchCor when you need activation times and a rough Vm, not the full diffusion solve.
- Use [BioGears](biogears.md) when you need whole-body organ systems and not tissue-level conduction.

TorchCor is a poor fit when you have no mesh. The repository does not ship one. The README sends you to a Google Drive folder for the bi-ventricle mesh, and the docs show paths to atrium meshes that are not in the repository either.

## Install

There is no recipe for TorchCor on this site. The workflow in the project documentation targets a GPU: the README and the examples set the device to `cuda:0`, the README timing was taken on an NVIDIA RTX 5090, and the `docker/` folder in the repository is a GPU-enabled setup. The cell models also call `torch.compile`. The server sandbox has no GPU, and the meshes are large downloads from outside GitHub.

Install on your own machine with pip. The current release on PyPI is 1.0.6 and it needs Python 3.10 or newer:

```bash
pip install torchcor
```

The docs say to install the PyTorch build that matches your CUDA toolkit first (from pytorch.org), then run `pip install torchcor`. They state that on a CPU-only machine the default wheel is fine and that the code falls back to the CPU. A development install is `git clone https://github.com/sagebei/torchcor.git`, then `pip install -e .` inside the folder.

Check the install:

```python
import torchcor as tc
print(tc.get_device())   # cuda:0, or cpu
```

## A first run

Adapted from the project README, https://github.com/sagebei/torchcor, and the Quickstart in its documentation, https://torchcor.readthedocs.io/en/latest/quickstart.html.

The README example runs a bi-ventricle with the ten Tusscher-Panfilov cell model. It needs a mesh folder with four kinds of file: `.pts` (node coordinates), `.elem` (connectivity), `.lon` (fibre directions) and one or more `.vtx` files (pacing nodes).

```python
import torchcor as tc
from torchcor.simulator import Monodomain
from torchcor.ionic import TenTusscherPanfilov

tc.set_device("cuda:0")
dtype = tc.float32
im = TenTusscherPanfilov(cell_type="ENDO", dt=0.01, dtype=dtype)

simulator = Monodomain(ionic_models=[im], T=500, dt=0.01, dtype=dtype)
simulator.load_mesh(path="path/to/ventricle/Case_1")
simulator.add_conductivity([34, 35], il=0.5272, it=0.2076, el=1.0732, et=0.4227)
simulator.add_stimulus("path/to/ventricle/Case_1/LV_sf.vtx",
                       start=0.0, duration=1.0, intensity=100)

Vm = simulator.solve(a_tol=1e-5, r_tol=1e-5, max_iter=100,
                     snapshot_interval=1, result_path="./biventricle")
ATs = simulator.compute_activation_map(Vm=Vm, snapshot_interval=1, threshold=0)
RTs = simulator.compute_repolarization_map(Vm=Vm, snapshot_interval=1, threshold=-70)
```

The README example sets more conductivity regions and stimuli than shown here. The example takes `T=500` ms with `dt=0.01` ms, so 50,000 time steps. The README says the full example took 47.6 seconds on an RTX 5090. That number comes from the README, not from this site.

## Reading the output

- `Vm` is a tensor of shape (T, N_nodes): the transmembrane voltage in mV at each saved snapshot. With `snapshot_interval=1`, one row per millisecond.
- `compute_activation_map` returns the local activation time per node: the first up-crossing of the threshold. A node that never crosses gets NaN. The README example uses a threshold of 0 mV.
- `compute_repolarization_map` returns the repolarisation time per node. It searches after the activation time, so it finds the down-crossing and not the upstroke.
- `save_vm` writes `Vm.pt` into `result_path`, and the maps can be saved as `.pt` files. All are readable with `torch.load`.
- `vm_to_vtk` writes VTK frames with the maps for ParaView.
- `sim.eikonal_activation_times()` in a reaction-eikonal run returns the wavefront arrival time at every node.
- `LeadField.compute_12lead(Vm)` returns a dictionary of the 12 standard leads.

## Pitfalls

- **Units.** `load_mesh` divides coordinates by `unit_conversion`. CARP files store micrometres, so 1000 gives millimetres. The wrong value changes conduction speed.
- **Mass lumping.** The docs say `mass_lumping=True` matches openCARP's default and gives the correct conduction velocity. They say the consistent mass matrix conducts about 35 percent too fast.
- **Conductivity and velocity must agree.** For the reaction-eikonal model with diffusion, the conductivities must imply the same conduction velocity as `add_velocity`, or the two fronts diverge.
- **Precision.** The lead-field solve runs in float64. The docs say accuracy degrades badly in float32.
- **Convergence.** `solve` raises an exception if a conjugate-gradient step reaches `max_iter`.
- **ECG meshes.** The heart mesh must be the same sub-domain of the torso mesh, with shared node ordering.

## Further reading

- Documentation: https://torchcor.readthedocs.io/en/latest/
- Source: https://github.com/sagebei/torchcor
- Paper: Zhou B et al. (2026) TorchCor. SoftwareX 33:102521. https://doi.org/10.1016/j.softx.2026.102521

---

Cite: Zhou B, Balmus M, Corrado C, Cicci L, Qian S, Niederer SA (2026). TorchCor: High-performance cardiac electrophysiology simulations with the finite element method on GPUs. SoftwareX 33:102521. doi:10.1016/j.softx.2026.102521

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/torchcor).
