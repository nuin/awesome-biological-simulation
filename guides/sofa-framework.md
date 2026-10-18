# SOFA Framework

> Real-time finite-element and rigid-body physics; the recipe runs a headless scene of a point mass on a spring under gravity and records its trajectory.

Licence: LGPL-2.1-or-later · [Source code](https://github.com/sofa-framework/sofa)

## What it simulates

SOFA (Simulation Open Framework Architecture) is an open-source framework for interactive physics simulation, with an emphasis on medical simulation and robotics. It is built around the finite element method, but it also handles rigid bodies, mass-spring systems, collisions, constraints and fluids through plugins. A simulation is a scene graph: nodes hold components such as a mechanical state, a mass, a force field, a solver, a collision model or a visual model. Mappings link a model to its collision or visual copy.

In the SOFA sense a time step has three parts. An animation loop calls an integration scheme (for example implicit Euler), which builds a linear system for the step. A linear solver (for example conjugate gradient) solves it and updates the mechanical state. Constraint-based contact adds a further solve on top.

## When to use it

Use SOFA for soft tissue and deformable bodies that must run in real time: organ deformation, soft robots, and scenes driven by haptic devices. The scene is built in C++ or in Python through the SofaPython3 plugin, and `runSofa` is the graphical application.

Alternatives:

- [OpenSim](opensim.md) models whole-body musculoskeletal dynamics with rigid segments and muscles.
- [tyssue](tyssue.md) simulates epithelial tissue mechanics with vertex models.
- [MyoSuite](myosuite.md) runs muscle-driven rigid-body models with MuJoCo.
- [Nimble Physics](nimble-physics.md) is a differentiable rigid-body engine used for human motion fitting.

## Install

The project's download page offers binaries for Linux (Python 3.10 and 3.12 builds, as `.run` and `.zip`), Windows and macOS. The current release is v26.06.00. The page also points to a conda route, and conda-forge carries the packages `libsofa` and `sofa-gl` at 26.06.00, plus `sofa-python3`, whose latest build is 25.12.00 (checked on anaconda.org). The Python bindings are available for Linux x86-64, macOS Intel and Windows, for Python 3.10 to 3.14. They are not built for Linux aarch64.

```bash
conda create -n sofa -c conda-forge sofa-python3=25.12.00 python=3.12
conda activate sofa
python -c "import Sofa; print(Sofa.__file__)"
```

Source is on GitHub (`git clone -b v26.06.00 https://github.com/sofa-framework/sofa.git`) and builds with CMake; the project has build guides for each system. SOFA is released under the LGPL (version 2.1 or later), except the `applications` folder, which is GPL.

The recipe pins `sofa-python3` 25.12.00 on `linux/amd64`. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## A first run

Adapted from the [SofaPython3 first steps](https://sofapython3.readthedocs.io/en/latest/content/FirstSteps.html). A script run from a plain Python interpreter creates the root node, calls its own `createScene`, initializes the graph and steps it:

```python
import Sofa, Sofa.Simulation

root = Sofa.Core.Node("root")
createScene(root)                 # your scene description
Sofa.Simulation.initRoot(root)
for i in range(10):
    Sofa.Simulation.animate(root, root.dt.value)
```

The docs build a falling sphere from a rigid mechanical object, a uniform mass, an implicit Euler scheme and a conjugate-gradient solver. The recipe uses the same pattern in a smaller scene with no meshes: one point mass, gravity of 9.81 m/s2, and a spring that pulls the point back to its start. It writes the position after every step.

## Run the tested example

This recipe builds SOFA Framework in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 4.9 s. SOFA Framework has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [sofa-framework-recipe.tar.gz](https://biosimhub.pages.dev/guides/sofa-framework/sofa-framework-recipe.tar.gz) (Dockerfile, run_sofa.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf sofa-framework-recipe.tar.gz
   cd sofa-framework
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/sofa-framework:25.12.00 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/sofa-framework:25.12.00 python /opt/run_sofa.py --mass 1 --stiffness 100 \
    --dt 0.001 --steps 2000 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 1.0 KB |
| `trajectory.csv` | 94.7 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
---------------------------------------
Checking SOFA_ROOT and SOFAPYTHON3_ROOT
Using environment variable SOFA_ROOT: /opt/conda
---------------------------------------
[INFO]    [PluginManager] Loaded plugin: /opt/conda/lib/libSofa.Component.StateContainer.so
[INFO]    [PluginManager] Loaded plugin: /opt/conda/lib/libSofa.Component.Mass.so
[INFO]    [PluginManager] Loaded plugin: /opt/conda/lib/libSofa.Component.SolidMechanics.Spring.so
[INFO]    [PluginManager] Loaded plugin: /opt/conda/lib/libSofa.Component.LinearSolver.Iterative.so
[INFO]    [PluginManager] Loaded plugin: /opt/conda/lib/libSofa.Component.AnimationLoop.so
[INFO]    [PluginManager] Loaded plugin: /opt/conda/lib/libSofa.Component.ODESolver.Backward.so
steps=2000 dt=0.001 mass=1.0 stiffness=100.0
static deflection (m*g/k) = -0.098100
```

</details>

<details><summary>First lines of <code>trajectory.csv</code></summary>

```
step,time,x,y,z
0,0.000000,0.00000000,0.00000000,0.00000000
1,0.001000,0.00000000,-0.00000981,0.00000000
2,0.002000,0.00000000,-0.00002943,0.00000000
3,0.003000,0.00000000,-0.00005885,0.00000000
4,0.004000,0.00000000,-0.00009807,0.00000000
5,0.005000,0.00000000,-0.00014708,0.00000000
6,0.006000,0.00000000,-0.00020589,0.00000000
7,0.007000,0.00000000,-0.00027447,0.00000000
8,0.008000,0.00000000,-0.00035284,0.00000000
9,0.009000,0.00000000,-0.00044096,0.00000000
10,0.010000,0.00000000,-0.00053885,0.00000000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--mass` | Mass (kg) | 1 | 0.01 to 1000 |
| `--stiffness` | Spring stiffness (N/m) | 100 | 0.1 to 100000 |
| `--dt` | Time step (s) | 0.001 | 0.0001 to 0.05 |
| `--steps` | Steps | 2000 | 1 to 100000 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `trajectory.csv`: step, time and the x, y and z position of the mass. The mass starts at the rest point of the spring, falls under gravity and oscillates in y about the static deflection.
- `run_log.txt`: the settings, the static deflection m g / k, and the undamped period 2 pi sqrt(m / k), which give a hand check for the trajectory.

Implicit Euler damps oscillations numerically, so the amplitude decays over time even though the model has no friction. A smaller time step reduces that damping.

## Pitfalls

- **The class names change between releases.** The docs for the newest code show an `EulerImplicitIntegrationScheme` where older releases have `EulerImplicitSolver`. The recipe tries both. Match the names to the version you install.
- **Load the plugins.** A component is only found after its module is loaded, with `RequiredPlugin` or `SofaRuntime.importPlugin`. An unknown component fails at scene creation.
- **Python versions must match.** The Linux binaries come in builds for Python 3.10 and 3.12, and the conda package follows the Python of its environment.
- **Python conda builds lag the library.** `sofa-python3` was at 25.12.00 while `libsofa` was at 26.06.00. Install them together from one solve so the versions agree.
- **A GUI is optional.** The graphical front end, ImGui since v25.06, is only needed to look at a scene. A script that calls `animate` runs without it.
- **Units are whatever you choose.** SOFA applies no unit system. Keep lengths, masses and forces in one consistent set.

## Further reading

- Project: https://github.com/sofa-framework/sofa
- Download page: https://www.sofa-framework.org/download/
- SofaPython3 documentation: https://sofapython3.readthedocs.io/
- Faure F, Duriez C, Delingette H, et al. (2012). SOFA: a multi-model framework for interactive physical simulation. In Soft Tissue Biomechanical Modeling for Computer Assisted Surgery, Studies in Mechanobiology, Tissue Engineering and Biomaterials 11:283-321. https://doi.org/10.1007/8415_2012_125

---

Cite: Faure F, Duriez C, Delingette H, Allard J, Gilles B, Marchesseau S, Talbot H, Courtecuisse H, Bousquet G, Peterlik I, Cotin S (2012). SOFA: a multi-model framework for interactive physical simulation. In Soft Tissue Biomechanical Modeling for Computer Assisted Surgery, Studies in Mechanobiology, Tissue Engineering and Biomaterials 11:283-321. doi:10.1007/8415_2012_125

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/sofa-framework).
