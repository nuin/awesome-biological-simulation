# bioptim

> Solve an optimal control problem for a musculoskeletal-style model, here a torque-driven pendulum swing-up, and return the optimal trajectory and torques.

Licence: MIT · [Source code](https://github.com/pyomeca/bioptim)

## What it simulates

bioptim solves optimal control problems for musculoskeletal models. You describe a movement as a model, a duration, bounds on positions, velocities and controls, and a cost to minimise. bioptim finds the state and control trajectories that satisfy the dynamics and bounds at the lowest cost. A typical use is predicting a motion, such as a jump or a reach, without recording one.

It uses direct multiple shooting. The movement is split into shooting intervals. The equations of motion come from biorbd (rigid-body dynamics from a `.bioMod` text model), and the problem is built in CasADi. The default solver is IPOPT. ACADOS is the other supported solver, but it has no conda or pip package.

The controls can be joint torques, muscle activations or muscle excitations, and several phases can be chained. Because the solution is a local optimum of a non-convex problem, the initial guess and the bounds shape the result.

## When to use it

Use bioptim when the question is "what movement does this model choose" and you can write the goal as a cost.

- Use [OpenSim](opensim.md) when you have recorded motion and want inverse kinematics, inverse dynamics or muscle analyses.
- Use [FEBio](febio.md) when the question is about stress and strain inside tissue rather than whole-body movement.

## Install

```
conda install -c conda-forge bioptim
```

conda-forge lists bioptim 3.4.0 (the GitHub release of 2025-11-25) for Linux x86-64, macOS Intel, macOS Apple silicon and Windows. The package has builds for Python 3.11 to 3.14. Its dependencies include biorbd 1.12, numpy, scipy and matplotlib. bioptim is not on PyPI. The README names conda as the preferred route, and it describes a source install for people who add the dependencies by hand. The license is MIT.

A pinned environment looks like this:

```
micromamba create -n bioptim -c conda-forge bioptim=3.4.0
```

## A first run

Adapted from [`basic_ocp.py`](https://github.com/pyomeca/bioptim/blob/Release_3.4.0/bioptim/examples/getting_started/basic_ocp.py), the first example of the getting-started folder in release 3.4.0. A pendulum starts hanging down and must end upright while using as little torque as possible. The solver may only drive the sideways motion. The file builds the problem in `prepare_ocp`: a torque-driven `TorqueBiorbdModel`, a `MINIMIZE_CONTROL` objective on `tau`, bounds from the model's joint ranges, start and end at rest, and a final rotation of 3.14 rad. The example uses 1 second and 400 shooting nodes.

The recipe's helper script follows the same steps with fewer nodes, no live plots and no animation, and it writes the solution to a CSV file.

## Run the tested example

This recipe builds bioptim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 28.6 s. bioptim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [bioptim-recipe.tar.gz](https://biosimhub.pages.dev/guides/bioptim/bioptim-recipe.tar.gz) (Dockerfile, run_bioptim.py, example model.biomod, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bioptim-recipe.tar.gz
   cd bioptim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/bioptim:3.4.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bioptim:3.4.0 python /opt/run_bioptim.py --model /work/in/model.biomod \
    --final-time 1 --shooting 50 --max-torque 100 \
    --target-angle 3.14 --max-iter 1000 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 10.3 KB |
| `trajectory.csv` | 8.8 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```

******************************************************************************
This program contains Ipopt, a library for large-scale nonlinear optimization.
 Ipopt is released as open source code under the Eclipse Public License (EPL).
         For more information visit https://github.com/coin-or/Ipopt
******************************************************************************

This is Ipopt version 3.14.19, running with linear solver MUMPS 5.7.3.

Number of nonzeros in equality constraint Jacobian...:     1033
Number of nonzeros in inequality constraint Jacobian.:        0
Number of nonzeros in Lagrangian Hessian.............:      491
```

</details>

<details><summary>First lines of <code>trajectory.csv</code></summary>

```
time,q0,q1,qdot0,qdot1,tau0,tau1
0.000000000000000000e+00,0.000000000000000000e+00,0.000000000000000000e+00,0.000000000000000000e+00,0.000000000000000000e+00,6.663456821347474524e+00,0.000000000000000000e+00
2.000000000000000042e-02,3.266355815879014995e-02,-3.280178967249255256e-02,3.325742952816487907e+00,-3.339606947986194729e+00,4.900232387490964570e+00,0.000000000000000000e+00
4.000000000000000083e-02,1.239067642765600830e-01,-1.244004459008727637e-01,5.568747203824158554e+00,-5.586854479532922468e+00,3.203822616952773483e+00,0.000000000000000000e+00
5.999999999999999778e-02,2.343867884340626873e-01,-2.350769588963513845e-01,5.261052481678498260e+00,-5.260384778507986248e+00,2.219296053500595889e+00,0.000000000000000000e+00
8.000000000000000167e-02,3.292300101458042749e-01,-3.296980176459458622e-01,4.261970484316885965e+00,-4.239880150275606496e+00,1.709038530770969011e+00,0.000000000000000000e+00
1.000000000000000056e-01,4.058957719190526281e-01,-4.056920013878761444e-01,3.453557994876809367e+00,-3.407061974915151392e+00,1.376822732505462943e+00,0.000000000000000000e+00
1.199999999999999956e-01,4.685204996120488907e-01,-4.670885702918824989e-01,2.841576970470371055e+00,-2.763
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--final-time` | Movement duration (s) | 1 | 0.2 to 10 |
| `--shooting` | Shooting intervals | 50 | 10 to 200 |
| `--max-torque` | Torque bound on the actuated joint | 100 | 1 to 1000 |
| `--target-angle` | Final pendulum angle (rad) | 3.14 | 0.1 to 6.28 |
| `--max-iter` | Maximum IPOPT iterations | 1000 | 10 to 5000 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The solver prints IPOPT's iteration table, then `sol.print_cost()` lists each objective with its weighted value. The helper's last lines give `status`, `iterations`, the number of nodes and the total cost. A status of 0 means IPOPT reported a solution.

`trajectory.csv` has one row per node and these columns:

- `time` in seconds, from 0 to the final time.
- `q0`, `q1`: the two generalized coordinates of the pendulum segment, a translation along y and a rotation about x.
- `qdot0`, `qdot1`: their velocities.
- `tau0`, `tau1`: the generalized forces. `tau1` is 0 because the rotation is passive, and the last row of the `tau` columns may be empty, because constant controls act over intervals and have no value at the last node.

Check that the last `q1` equals the target angle and that the end velocities are 0. Those are hard bounds, so an exact miss signals a failed solve.

## Pitfalls

- **Run headless on purpose.** The example calls `sol.animate` with bioviz and enables live plots, which need a display. The recipe leaves both out.
- **The model extension is case sensitive.** biorbd chooses its reader from the extension, so the helper copies the input to a file named `model.bioMod` first.
- **The model may point to mesh files.** The `meshfile` line in the shipped `pendulum.bioMod` names an STL mesh for visualization. The example input in the recipe drops that line.
- **More nodes cost more time.** The problem grows with the number of shooting intervals, and so does each IPOPT iteration.
- **A different guess can give a different answer.** Swing-up problems are non-convex, so the initial guess can change the solution IPOPT finds.
- **Two solvers have extra setup.** ACADOS has no conda or pip package, and the HSL linear solvers are optional downloads.
- **The API changed between releases.** The 3.4.0 examples use `DynamicsOptions` and `TorqueBiorbdModel`. Tutorials written for older releases may use other names, so check them against the release you installed.

## Further reading

- Source and README: https://github.com/pyomeca/bioptim
- Tutorial notebooks: https://github.com/pyomeca/bioptim-tutorial
- Examples from the paper: https://github.com/s2mLab/BioptimPaperExamples
- biorbd: https://github.com/pyomeca/biorbd
- Paper: Michaud B, Bailly F, Charbonneau E, et al. (2023). Bioptim, a Python framework for musculoskeletal optimal control in biomechanics. IEEE Transactions on Systems, Man, and Cybernetics: Systems 53:321-332. https://doi.org/10.1109/TSMC.2022.3183831

---

Cite: Michaud B, Bailly F, Charbonneau E, et al. (2023). Bioptim, a Python framework for musculoskeletal optimal control in biomechanics. IEEE Transactions on Systems, Man, and Cybernetics - Systems 53:321-332. doi:10.1109/TSMC.2022.3183831

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bioptim).
