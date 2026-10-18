# OpenSim

> Forward dynamics of an OpenSim musculoskeletal or mechanical model (.osim) from its default pose, returning coordinate trajectories as CSV.

Licence: Apache-2.0 · [Source code](https://github.com/opensim-org/opensim-core)

## What it simulates

OpenSim simulates the motion of multibody models of the musculoskeletal system. A model (`.osim` file) lists rigid bodies, the joints between them, the coordinates of each joint and, in biological models, muscles. Forward dynamics takes the model at a starting pose and integrates the equations of motion. The result is each coordinate's value and speed over time.

The example loads a one-body pendulum. A rod of 1 kg hangs from a pin joint with a single coordinate called `angle`, in radians, in a gravity of 9.81 m/s^2. The model starts at `angle = 1` rad (the default value in the file) and no speed. The run integrates 5 s and reports every 0.02 s.

The key assumption is the model. OpenSim computes what the file describes. Masses, inertias, joint locations and muscle parameters all come from the `.osim` file, so the output is only as good as those values. The recipe's helper applies no controls and no excitation. A model with muscles is equilibrated first and then moves under gravity alone.

## When to use it

Use OpenSim for questions about body mechanics:

- How does a limb or a mechanical linkage move under gravity and its own muscle forces?
- What are the joint angles and speeds after a given starting pose?
- How does a change in mass, inertia or joint position change the motion?

No other guide covers rigid-body and muscle models. [LAMMPS](lammps.md) handles particle systems, and [XPPAUT](xppaut.md) handles small sets of differential equations. The recipe's container runs only forward dynamics from the default pose.

## Install it yourself

The OpenSim install guide gives `conda install -c opensim-org opensim` inside a conda environment. The conda-forge build also exists. A dry run `micromamba create -n t --dry-run -c conda-forge -c bioconda opensim=4.5.2` resolves opensim 4.5.2 with Python 3.14.8 on linux-64. The recipe's container pins Python 3.12 with `--strict-channel-priority`.

```
conda create -n opensim -c conda-forge python=3.12 opensim=4.5.2
conda activate opensim
```

The minimal Python script is the recipe's helper without the CSV code:

```python
import opensim as osim

model = osim.Model("pendulum.osim")
state = model.initSystem()
manager = osim.Manager(model)
manager.setIntegratorAccuracy(1e-6)
state.setTime(0.0)
manager.initialize(state)
for k in range(1, 251):
    state = manager.integrate(k * 0.02)
    model.realizeVelocity(state)
    q = model.getCoordinateSet().get(0)
    print(state.getTime(), q.getValue(state), q.getSpeedValue(state))
```

## Run the tested example

This recipe builds OpenSim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 1.3 s. OpenSim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [opensim-recipe.tar.gz](https://biosimhub.pages.dev/guides/opensim/opensim-recipe.tar.gz) (Dockerfile, run_opensim.py, example model.osim, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf opensim-recipe.tar.gz
   cd opensim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/opensim:4.5.2 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/opensim:4.5.2 python /opt/run_opensim.py /work/in/model.osim \
    --duration 5 --report_dt 0.02 --accuracy 1e-06 > out/opensim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `opensim_log.txt` | 128 B |
| `states.csv` | 16.0 KB |

<details><summary>First lines of <code>opensim_log.txt</code></summary>

```
[info] Loaded model pendulum from file /work/in/model.osim
model pendulum: 1 coordinates, 250 steps of 0.02 s, final time 5.000
```

</details>

<details><summary>First lines of <code>states.csv</code></summary>

```
time,angle_value,angle_speed,kinetic_energy
0.0,1.0,0.0,0.0
0.02,0.9983656661932405,-0.16340476085261396,0.013484063513996478
0.04,0.9934661034642728,-0.3264652598443032,0.05382268077203024
0.06,0.9853116733325387,-0.4888327593510985,0.12067352064047854
0.08,0.9739197933568785,-0.6501496770345461,0.2134607742868029
0.1,0.9593151557662533,-0.8100454684223561,0.33136769876035516
0.12,0.9415300249747002,-0.9681328706652856,0.4733270339076164
0.14,0.9206046055442778,-1.1240046349354087,0.6380101417749222
0.16,0.8965874695618743,-1.2772308737331575,0.8238159459326683
0.18,0.8695360298683672,-1.4273571492137724,1.028860957862892
0.2,0.8395170430800983,-1.5739034257055244,1.2509718566910308
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--duration` | Simulated time (s) | 5 | 0.1 to 60 |
| `--report_dt` | Reporting interval (s) | 0.02 | 0.001 to 1 |
| `--accuracy` | Integrator accuracy | 1e-06 | 1e-10 to 0.01 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`run_opensim.py` wraps the script above. It loads the model, runs `equilibrateMuscles` if the model has muscles, then calls `manager.integrate` in steps of `--report_dt`. At each step it writes the time, every coordinate's value and speed, and the model's kinetic energy.

The log has two lines. `Loaded model pendulum from file /work/in/model.osim` is OpenSim's own message. `model pendulum: 1 coordinates, 250 steps of 0.02 s, final time 5.000` comes from the helper.

`states.csv` (16375 bytes) has 251 rows with the columns `time,angle_value,angle_speed,kinetic_energy`. It starts at `0.0,1.0,0.0,0.0`. At 0.02 s the angle is 0.9984 rad, the speed is -0.1634 rad/s and the kinetic energy is 0.01348. At 0.2 s the angle is 0.8395. The angle first reaches zero between 0.52 and 0.54 s, so a quarter swing takes about 0.54 s. The angle reaches -0.9999 at the other end of the swing. At 5.0 s it is -0.4665 rad, moving at -2.618 rad/s with a kinetic energy of 3.4615.

The kinetic energy and speed give the inertia about the pin. 2 * 0.013484 / 0.1634^2 is 1.01 kg.m^2. The model file has 0.01 about the center of mass and a center of mass 1.0 m from the pin (0.5 m below the rod origin, with the joint 0.5 m above it). 0.01 + 1 kg * (1.0 m)^2 is 1.01.

## Your own runs

Copy the docker run line from the recipe and change values. The `--accuracy` flag sets the integrator accuracy.

1. **Longer run.** Set `--duration 20 --report_dt 0.1`. The file has 201 rows. At 20 s the angle is -0.3344 rad, the speed is -2.8025 rad/s and the kinetic energy is 3.9663.
2. **Looser accuracy.** Add `--accuracy 0.01`. At 20 s the angle is -0.3340, the speed is -2.8028 and the kinetic energy is 3.9671. Accuracy 0.01 and 1e-06 differ by 0.0003 rad after 20 s here.
3. **Another starting pose.** Edit `<default_value>1</default_value>` to `0.2` in the model. The first sample at or below zero came at 0.52 s, against 0.54 s for 1 rad. The quarter swing is a little shorter for a smaller swing.

To run your own model, replace `pendulum.osim`. The helper reports every coordinate and starts from the file's default pose.

## Pitfalls

- **Only the default pose.** The helper does not read a motion or state file. To start elsewhere, edit the default coordinate values in the model.
- **Radians.** Angles are in radians and speeds in rad/s for rotational coordinates. Translational coordinates are in meters.
- **No controls.** The helper sets no muscle excitations or actuator controls. A task that needs controls needs your own script.
- **Report step is not integration step.** `--report_dt` sets how often rows are written. `--accuracy` sets the integrator error tolerance. Lowering the report step does not make the solution more accurate.
- **Run time.** The pendulum took 1.3 s. The recipe's image runs as `linux/amd64`.

## Further reading

- Installation: https://opensimconfluence.atlassian.net/wiki/spaces/OpenSim/pages/53085346/Installation+Guide
- Source: https://github.com/opensim-org/opensim-core
- Delp SL et al. (2007). OpenSim: open-source software to create and analyze dynamic simulations of movement. IEEE Trans Biomed Eng 54:1940-1950. https://doi.org/10.1109/TBME.2007.901024

---

Cite: Delp SL et al. (2007). OpenSim, open-source software to create and analyze dynamic simulations of movement. IEEE Trans Biomed Eng 54:1940-1950. doi:10.1109/TBME.2007.901024

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/opensim).
