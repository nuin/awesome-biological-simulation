# Nimble Physics

> Differentiable rigid-body dynamics for articulated bodies, used for biomechanics; the recipe steps a cart-and-pole system forward in time.

Licence: BSD-2-Clause · [Source code](https://github.com/keenon/nimblephysics)

## What it simulates

Nimble Physics is a rigid-body physics engine for articulated bodies. It started as a fork of the DART engine and adds analytical gradients, so one time step, `nimble.timestep(world, state, controls)`, works as a PyTorch function that you can differentiate. The engine is written in C++ with Python bindings.

For biomechanics it adds joint types that fit the body (custom joints for knees, ellipsoid joints for shoulders, constant-curvature joints for spines), loading and saving of OpenSim skeleton models, handling of motion-capture markers, and differentiable bone scales. The project's documentation is aimed at studying real human bodies with AI, and it states that it does not cover general robotics simulation in depth.

The state of a world is a vector of joint positions followed by joint velocities. Contacts use a linear complementarity formulation.

## When to use it

Use Nimble to fit a skeleton model to marker data, compute joint torques from a measured motion, or optimize a trajectory by gradient descent through the physics.

Alternatives:

- [OpenSim](opensim.md) is the established tool for musculoskeletal models and inverse dynamics, and Nimble reads its model files.
- [MyoSuite](myosuite.md) simulates muscle-driven models in MuJoCo for motor-control and learning tasks.
- [SOFA Framework](sofa-framework.md) simulates deformable tissue by finite elements.

## Install

The package is `nimblephysics` on PyPI. The README says the project is beta software and that its API may change before 1.0. Release 0.10.52.1 has wheels for Linux x86-64 (Python 3.8 to 3.12), Linux aarch64 (Python 3.8 to 3.11) and macOS (checked on the PyPI JSON API). Release 0.10.52.2 is a macOS wheel for Python 3.9 only, so pin the earlier one on Linux. Windows is not supported; the install page recommends WSL.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install "numpy==1.26.4" torch
pip install nimblephysics==0.10.52.1
python -c "import nimblephysics as nimble; print(nimble.simulation.World())"
```

PyTorch is needed for `nimble.timestep`. Apple-silicon Macs have prebuilt wheels for Python 3.9 only, according to the README. The licence is BSD-2-Clause, with the bundled Rajagopal body model under the MIT licence.

The recipe installs the CPU build of torch 2.5.1 in a Python 3.11 image. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## A first run

Adapted from `python/new_examples/cartpole.py` in the [repository](https://github.com/keenon/nimblephysics), with the GUI and the gradient loop left out. The script builds a world with gravity, a cart on a prismatic joint and a pole on a revolute joint, then steps the state with `nimble.timestep`:

```python
import nimblephysics as nimble, torch

world = nimble.simulation.World()
world.setGravity([0, -9.81, 0])
# ... skeleton with a prismatic cart joint and a revolute pole joint ...
world.addSkeleton(cartpole)
world.setTimeStep(world.getTimeStep() * 10)

state = torch.tensor([0.0, 0.5, 0.0, 0.0])
action = torch.zeros(world.getActionSize())
for _ in range(500):
    state = nimble.timestep(world, state, action)
```

The state has four numbers: cart position, pole angle, cart velocity and pole angular velocity. The recipe lets you set the initial angle, a constant push on the cart and the time-step multiplier.

## Run the tested example

This recipe builds Nimble Physics in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.2 s.

1. Download [nimble-physics-recipe.tar.gz](https://biosimhub.pages.dev/guides/nimble-physics/nimble-physics-recipe.tar.gz) (Dockerfile, run_nimble.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf nimble-physics-recipe.tar.gz
   cd nimble-physics
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/nimble-physics:0.10.52.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/nimble-physics:0.10.52.1 python /opt/run_nimble.py --steps 500 --angle 0.5 \
    --push 0 --dt-scale 10 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 139 B |
| `states.csv` | 29.0 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
steps=500 dt=0.010000 angle0=0.5 push=0.0
final state [cart x, pole angle, cart v, pole angular v] = 0.119676 1.328889 -0.138750 -2.438477
```

</details>

<details><summary>First lines of <code>states.csv</code></summary>

```
step,time,cart_x,pole_angle,cart_v,pole_angular_v
0,0.0,0.00000000,0.50000000,0.00000000,0.00000000
1,0.010000,0.00000000,0.50000000,0.00447181,0.02038241
2,0.020000,0.00004472,0.50020382,0.00894309,0.04076463
3,0.030000,0.00013415,0.50061147,0.01341383,0.06115351
4,0.040000,0.00026829,0.50122301,0.01788404,0.08155589
5,0.050000,0.00044713,0.50203856,0.02235370,0.10197860
6,0.060000,0.00067066,0.50305835,0.02682280,0.12242847
7,0.070000,0.00093889,0.50428264,0.03129127,0.14291231
8,0.080000,0.00125181,0.50571176,0.03575903,0.16343693
9,0.090000,0.00160940,0.50734613,0.04022597,0.18400909
10,0.100000,0.00201166,0.50918622,0.04469192,0.20463558
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--steps` | Steps | 500 | 1 to 20000 |
| `--angle` | Initial pole angle (rad) | 0.5 | -3.1 to 3.1 |
| `--push` | Constant force on the cart (N) | 0 | -10 to 10 |
| `--dt-scale` | Time step multiplier | 10 | 0.1 to 20 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `states.csv`: step, time, cart position, pole angle, cart velocity and pole angular velocity after each step, starting from the initial state in row 0.
- `run_log.txt`: the settings and the final state.

With no push and a nonzero starting angle the pole joint is free, so the angle oscillates under gravity while the cart moves in reaction. Check energy and amplitude over time to see the effect of the time-step multiplier.

## Pitfalls

- **Pin the package version.** Old and new releases differ in the wheels they ship, and the project reserves the right to break its API before version 1.0.
- **Use a supported Python.** Wheels exist for specific Python versions only. A mismatch fails with `No matching distribution found`; the install page also says pip older than 19.3 gives that error.
- **Torch is a separate install.** Pick the CPU or CUDA build yourself; the wheel declares only `torch` and `numpy`.
- **Actions are forces on every degree of freedom.** The action vector has one entry per degree of freedom. In the example the pole joint's control-force limits are set to 0, so only the cart is driven.
- **The time step is a trade.** Larger steps run faster and backpropagate faster, but they are less accurate.
- **The documentation targets v0.10.31.** It says some examples may not work on other releases.

## Further reading

- Project: https://github.com/keenon/nimblephysics
- Documentation: https://nimblephysics.org/docs/
- Werling K, Omens D, Lee J, Exarchos I, Liu CK (2021). Fast and feature-complete differentiable physics for articulated rigid bodies with contact. https://doi.org/10.48550/arXiv.2103.16021

---

Cite: Werling K, Omens D, Lee J, Exarchos I, Liu CK (2021). Fast and feature-complete differentiable physics for articulated rigid bodies with contact. arXiv:2103.16021. doi:10.48550/arXiv.2103.16021

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/nimble-physics).
