# biorbd

> Forward dynamics of a musculoskeletal rigid-body model described in a bioMod file, driven by constant muscle activations.

Licence: MIT · [Source code](https://github.com/pyomeca/biorbd)

## What it simulates

biorbd is a library for the dynamics of musculoskeletal models. A model is a tree of rigid segments joined by translational and rotational degrees of freedom, with optional muscles, markers, IMUs and joint actuators. The rigid-body algorithms follow Featherstone's equations as implemented in RBDL. You get the standard calls:

- **Forward kinematics.** Marker positions in the world frame for a given pose q.
- **Inverse dynamics.** The joint torques tau needed for given q, qdot and qddot.
- **Forward dynamics.** The accelerations qddot produced by given q, qdot and tau.
- **Muscle terms.** Muscle lengths, forces and the joint torque a set of muscle activations produces.

The core is C++ (Eigen or CasADi for the linear algebra), with Python and MATLAB interfaces. biorbd does not integrate a trajectory for you. It returns accelerations, and you step the state forward yourself, or hand the model to an optimiser.

Models are written in the `.bioMod` text format, version 4. Segments carry mass, inertia and centre of mass. Segment tags such as `translations` and `rotations` set the generalized coordinates and their order. `//` starts a comment.

## When to use it

Use biorbd to evaluate musculoskeletal dynamics from a script, for example the muscle-driven acceleration of an arm at one pose, or as the dynamics inside an optimal-control problem.

- Use [OpenSim](opensim.md) when you want a full workflow with scaling, inverse kinematics and static optimization, and a large library of published models.
- Use [ArtiSynth](artisynth.md) when finite-element soft tissue and contact matter as much as the skeleton.
- Use biorbd when you want a small library with a Python call per quantity and no GUI.

biorbd reads OpenSim models after conversion, and the README describes the conversion route.

## Install

The README gives one command for the conda-forge package:

```bash
conda install -c conda-forge biorbd
```

This installs the binaries, the headers and the Python binder into the active environment. The current release is 1.12.3 (GitHub tag `Release_1.12.3`, July 2026). conda-forge has builds for Linux x86-64 and aarch64, macOS and Windows, for Python 3.10 to 3.14. No MATLAB binaries are on conda-forge. MATLAB users download them from the GitHub release page.

The recipe below pins `conda-forge::biorbd=1.12.3` with Python 3.12 in a micromamba image. The other route is a source build with CMake, which needs RBDL, Eigen or CasADi, and SWIG for the Python binder.

## A first run

Adapted from the Python 3 section of the README, https://github.com/pyomeca/biorbd. The example loads a model, computes marker positions at one pose, then the joint accelerations produced by muscles at half activation:

```python
import numpy as np
import biorbd

model = biorbd.Model("arm26.bioMod")
Q = np.ones(model.nbQ()) / 10      # position
Qdot = np.ones(model.nbQ()) / 10   # velocity

for marker in model.markers(Q):
    print(marker.to_array())

states = model.stateSet()
for state in states:
    state.setActivation(0.5)
joint_torque = model.muscularJointTorque(states, Q, Qdot)
Qddot = model.ForwardDynamics(Q, Qdot, joint_torque)
print(Qddot.to_array())
```

The README uses `arm26.bioMod` from the repository's `examples/` folder. The recipe ships the same file, taken from the 1.12.3 tag.

## Run the tested example

This recipe builds biorbd in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.3 s.

1. Download [biorbd-recipe.tar.gz](https://biosimhub.pages.dev/guides/biorbd/biorbd-recipe.tar.gz) (Dockerfile, run_biorbd.py, example model.biomod, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf biorbd-recipe.tar.gz
   cd biorbd
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/biorbd:1.12.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/biorbd:1.12.3 python /opt/run_biorbd.py /work/in/model.biomod \
    --activation 0.5 --q0 0.1 --steps 200 --dt 0.005 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `markers_final.csv` | 348 B |
| `run_log.txt` | 58 B |
| `summary.json` | 253 B |
| `trajectory.csv` | 32.2 KB |

<details><summary>First lines of <code>markers_final.csv</code></summary>

```
marker,x,y,z
r_acromion,-0.01256,0.04,0.17
r_humerus_epicondyle,-0.14796608833390465,-0.26731923173346944,0.1919407681610304
COM_arm,-0.1012155124969926,-0.16685371249782666,0.16501582954216207
r_radius_styloid,-0.33022020607690805,-0.4153728730090927,0.24235570049189206
COM_hand,-0.2870383612813565,-0.38169445784697725,0.14842597701087096
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
dofs=2 muscles=6 markers=5 steps=200 dt=0.005 finite=True
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "dofs": 2,
 "muscles": 6,
 "markers": 5,
 "activation": 0.5,
 "q0": 0.1,
 "steps": 200,
 "dt_s": 0.005,
 "final_q": [
  -0.4829363468494495,
  -0.4029347470320074
 ],
```

</details>

<details><summary>First lines of <code>trajectory.csv</code></summary>

```
time_s,q_r_humerus_rotation1_RotZ,q_r_ulna_radius_hand_rotation1_RotZ,qdot_r_humerus_rotation1_RotZ,qdot_r_ulna_radius_hand_rotation1_RotZ,qddot_r_humerus_rotation1_RotZ,qddot_r_ulna_radius_hand_rotat
0.0,0.1,0.1,0.0,0.0,135.58831202796358,-458.26229358579496,-9.20589047461192,-12.096339614328823
0.005,0.1033897078006991,0.08854344266035513,0.6779415601398179,-2.291311467928975,94.15513337222025,-326.5335316152259,-7.481729237223141,-9.019690005277303
0.01,0.1091332939357037,0.0689235470303296,1.1487172270009192,-3.9239791260051047,77.26230559384042,-271.5558193585993,-6.608453434973606,-7.668533192739733
0.015,0.11680843771055431,0.04251475591633909,1.5350287549701214,-5.281758222798102,70.39590977392567,-248.49460892470807,-6.147252809315476,-7.066390905437119
0.02,0.12624347922975307,0.009893599579230875,1.8870083038397496,-6.5242312674216425,68.44902139997605,-241.9058648053906,-5.984535078993169,-6.8956027746147655
0.025,0.13738974628395123,-0.0287752033780121,2.22925341083963,-7.733760591448595,68.30454363788053,-242.94028163897818,-6.126692094596898,-7.006782123920124
0.03,0.1502436269290964,-0.07351751337622953,2.5707761290290323,-8.948461999643486,66.76763008289991,-243.28
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--activation` | Muscle activation (0 to 1 | 0.5 | 0 to 1 |
| `--q0` | Initial value of every coordinate | 0.1 | -3 to 3 |
| `--steps` | Time steps | 200 | 1 to 5000 |
| `--dt` | Time step (s) | 0.005 | 0.0001 to 0.05 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_biorbd.py` wraps the calls above in a loop. At each step it sets every muscle to the chosen activation, asks for the muscle joint torque, computes the accelerations with `ForwardDynamics`, then advances the state with a semi-implicit Euler step: velocity first, then position. It writes four files.

- `trajectory.csv` has one row per step. The columns are time, then q, qdot, qddot and tau for every degree of freedom, named from the model.
- `markers_final.csv` has the world positions (x, y, z) of each marker in the model at the last state.
- `summary.json` records the number of degrees of freedom, muscles and markers, the settings, the final q and qdot, and a `finite` flag that is false if the state went to infinity or NaN.
- `run_log.txt` has a one-line summary.

A model without muscles gets zero tau, so it moves only under gravity. The arm26 model has muscles. A large time step or a stiff pose can make the state diverge, and `finite` shows that.

## Pitfalls

- **Two Python interfaces.** The `biorbd.Model` interface used here works on every Python version. The newer `biorbd.Biorbd` wrapper (properties such as `model.nb_q`) is imported only on Python 3.12 and later. Examples written for one do not run on the other.
- **Eigen backend only for numbers.** Several upstream examples say they work only with the Eigen backend. The CasADi backend builds symbolic expressions.
- **Integration is yours.** biorbd gives qddot. A fixed-step Euler loop is crude, and muscle activation has no dynamics unless you add them.
- **Constant activation.** The recipe applies one activation to all muscles. Real motion needs per-muscle activations that vary in time.
- **Windows paths.** The README says paths in the C++ API must use `/` or `\\`.
- **Meshes.** The recipe has no mesh files. Leave `meshfile` lines out or comment them, as `arm26.bioMod` does.
- **Slow builds.** The README warns that a debug build is slow. Use at least `RelWithDebInfo` when compiling.

## Further reading

- README with the model-file reference: https://github.com/pyomeca/biorbd
- Releases: https://github.com/pyomeca/biorbd/releases
- Conda-forge package: https://anaconda.org/conda-forge/biorbd
- Paper: Michaud B, Begon M (2021). biorbd: A C++, Python and MATLAB library to analyze and simulate the human body biomechanics. Journal of Open Source Software 6:2562. https://doi.org/10.21105/joss.02562

---

Cite: Michaud B, Begon M (2021). biorbd: A C++, Python and MATLAB library to analyze and simulate the human body biomechanics. J Open Source Softw 6:2562. doi:10.21105/joss.02562

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/biorbd).
