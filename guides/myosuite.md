# MyoSuite

> Muscle-actuated musculoskeletal models with motor-control tasks, simulated in MuJoCo through a Gymnasium interface; the recipe rolls out an elbow-pose task on the CPU.

Licence: Apache-2.0 · [Source code](https://github.com/MyoHub/myosuite)

## What it simulates

MyoSuite is a collection of musculoskeletal environments and tasks simulated with the MuJoCo physics engine. The bodies are rigid segments joined by joints and driven by muscle actuators, so the commands are muscle excitations and the state is joint angles, velocities and muscle forces. The tasks cover joint and finger posing, reaching, and object manipulation, plus the MyoChallenge set listed in the README: Baoding, Bimanual, Chase Tag, Die Reorient, OSL Run, Relocate, Soccer and Table Tennis.

The models come from the `myo_sim` package, pinned to 0.2.3 in MyoSuite 3. The package follows the Gymnasium interface: `make_env(env_id)` returns an environment with `reset`, `step` and an action space of muscle commands. Variants add muscle conditions: sarcopenia (50 percent peak force, prefix `myoSarc`), cumulative fatigue (`myoFati`) and tendon transfer for hand tasks (`myoReaf`). Version 3 also runs the same task id on a GPU backend (mjlab) or an experimental MJX path.

## When to use it

Use MyoSuite when you want to study movement control with realistic muscles: train or test a controller on a muscle-driven arm or hand, compare healthy and impaired muscles, or pull kinematics and muscle forces out of a forward simulation.

Alternatives:

- [OpenSim](opensim.md) is the standard tool for musculoskeletal modelling and inverse dynamics from motion data.
- [Nimble Physics](nimble-physics.md) is a differentiable rigid-body engine used to fit human motion.
- [SOFA Framework](sofa-framework.md) simulates deformable tissue and soft robots by finite elements.

## Install

MyoSuite 3.0.0 is on PyPI (checked on the PyPI JSON API) as a pure Python wheel for Python 3.10 or newer. It pulls in `mujoco`, `gymnasium`, `numpy`, `scipy`, `pandas` and the `myo-sim` models. The README states support for Python 3.10 to 3.14.

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -U myosuite==3.0.0
python -c "import myosuite; print(len(myosuite.myosuite_env_suite), 'envs')"
```

The last line is the project's own check. It prints the number of registered tasks. Training extras exist: `pip install "myosuite[rl]"` adds Stable-Baselines3, and the `[mjlab]` extra is for GPU training and needs an NVIDIA GPU. The licence is Apache-2.0.

The recipe installs this package in a Python 3.12 image with no GPU. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## A first run

Adapted from the Quick start in the [README](https://github.com/MyoHub/myosuite) and the [biomechanics quick start](https://myosuite.readthedocs.io/en/latest/quickstart_biomechanics.html). The recipe rolls out a task for a fixed number of steps with a chosen muscle policy and a seed:

```python
from myosuite import make_env

env = make_env("myoElbowPose1D6MRandom-v0")
obs, info = env.reset(seed=0)
for _ in range(200):
    obs, reward, terminated, truncated, info = env.step(env.action_space.sample())
    if terminated or truncated:
        obs, info = env.reset()
env.close()
```

Each call to `step` runs several MuJoCo sub-steps: the docs give a default frame skip of 10 steps of 2 ms, a 20 ms control period. `info["obs_dict"]` and `info["rwd_dict"]` break the observation and the reward into named parts.

## Run the tested example

This recipe builds MyoSuite in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.2 s.

1. Download [myosuite-recipe.tar.gz](https://biosimhub.pages.dev/guides/myosuite/myosuite-recipe.tar.gz) (Dockerfile, run_myosuite.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf myosuite-recipe.tar.gz
   cd myosuite
   sh run.sh
   ```

![Terminal recording of the MyoSuite example run](https://biosimhub.pages.dev/media/myosuite/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/myosuite:3.0.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/myosuite:3.0.0 python /opt/run_myosuite.py --env myoElbowPose1D6MRandom-v0 \
    --steps 200 --policy random --seed 0 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `rollout.csv` | 39.7 KB |
| `run_log.txt` | 117 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/myosuite/result-dark.png"><img src="https://biosimhub.pages.dev/media/myosuite/result.png" alt="Plot of the MyoSuite example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>rollout.csv</code></summary>

```
step,time,reward,action_mean,muscle_force_total_N,terminated,truncated,qpos_0,rwd_pose,rwd_bonus,rwd_penalty,rwd_act_reg,rwd_sparse,rwd_solved,rwd_done,rwd_dense
0,0.020000000000000004,-0.9769579881694037,-0.10324157029390335,1189.257846378764,0,0,0.6281369278845035,-0.8177661023351979,0.0,-0.0,-0.1591918858342058,-0.8177661023351979,0.0,0.0,-0.976957988169403
1,0.04000000000000002,-0.9447290961922051,0.21114058792591095,1429.1569626885625,0,0,0.6934566571907196,-0.7524463730289818,0.0,-0.0,-0.1922827231632234,-0.7524463730289818,0.0,0.0,-0.9447290961922051
2,0.06000000000000004,-0.8561969726313421,0.06698035448789597,1601.3583952752751,0,0,0.7878606933775069,-0.6580423368421945,0.0,-0.0,-0.19815463578914758,-0.6580423368421945,0.0,0.0,-0.856196972631342
3,0.08000000000000006,-0.7087201434299745,-0.2690613567829132,1104.841742817095,0,0,0.8666379114852892,-0.5792651187344121,0.0,-0.0,-0.1294550246955624,-0.5792651187344121,0.0,0.0,-0.7087201434299745
4,0.10000000000000007,-0.7115893524496265,0.43770310282707214,1532.680510653332,0,0,0.9447829775018088,-0.5011200527178925,0.0,-0.0,-0.21046929973173403,-0.5011200527178925,0.0,0.0,-0.7115893524496265
5,0.12000000000000009,-0.553863665
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
env=myoElbowPose1D6MRandom-v0 policy=random seed=0 steps=200 episodes=3
action_dim=6 obs_dim=9
total_reward=835.7135
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--env` | Task | myoElbowPose1D6MRandom-v0 | myoElbowPose1D6MRandom-v0, myoFatiElbowPose1D6MRandom-v0, myoSarcElbowPose1D6MRandom-v0 |
| `--steps` | Steps | 200 | 1 to 5000 |
| `--policy` | Muscle commands | random | random, zero, full |
| `--seed` | Seed | 0 | 0 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `rollout.csv`: one row per step with the simulation time, the reward, the mean muscle command, the summed muscle force, the joint angles (`qpos_0`, `qpos_1`, and so on, in radians) and the entries of the reward breakdown that are single numbers.
- `run_log.txt`: the task, policy, seed, step and episode counts, the sizes of the action and observation vectors, and the total reward.

MuJoCo reports muscle tension as a negative force, so the recipe flips the sign. With the `zero` policy the muscles are not excited and the joint settles under passive forces. With `full` all muscles are driven at maximum.

## Pitfalls

- **Run from the wrong folder and the import fails.** A directory that contains a folder named `myosuite` is imported as a namespace package, which gives `cannot import name ... from 'myosuite' (unknown location)`.
- **Policies from version 2 may not transfer.** The README for version 3 lists changed observations (no clipping), stronger motors in the `motorFinger*` tasks, and different reset and seed behaviour.
- **Baseline policies need the pinned models.** A different `myo-sim` version can change joint ranges, and the README warns that the baseline policies only hold for the pinned version.
- **The viewer is not part of the recipe.** On macOS the viewer needs `mjpython`. Headless rollouts need no display.
- **Seeds cover the environment and the actions.** Seed the environment in `reset(seed=...)` and the action space with `env.action_space.seed(...)` to repeat a random policy.
- **Muscle conditions are wrappers.** Use the prefixed task ids or the `features` option of `EnvConfig`, and do not edit the model by hand.

## Further reading

- Project: https://github.com/MyoHub/myosuite
- Documentation: https://myosuite.readthedocs.io/en/latest/
- Task list: https://myosuite.readthedocs.io/en/latest/environments.html
- Caggiano V, Wang H, Durandau G, Sartori M, Kumar V (2022). MyoSuite: a contact-rich simulation suite for musculoskeletal motor control. L4DC 2022. https://doi.org/10.48550/arXiv.2205.13600

---

Cite: Caggiano V, Wang H, Durandau G, Sartori M, Kumar V (2022). MyoSuite: a contact-rich simulation suite for musculoskeletal motor control. Learning for Dynamics and Control Conference (L4DC), 2022. arXiv:2205.13600. doi:10.48550/arXiv.2205.13600

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/myosuite).
