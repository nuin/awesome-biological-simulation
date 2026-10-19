# JumpProcesses.jl

> Gillespie-type stochastic simulation of a mass-action SIR epidemic with JumpProcesses.jl, repeated over seeded runs.

Licence: MIT · [Source code](https://github.com/SciML/JumpProcesses.jl)

## What it simulates

JumpProcesses.jl simulates systems where the state changes by discrete jumps at random times. The standard example is a chemical reaction network with whole-molecule counts: each reaction is a jump, and its rate (propensity) depends on the current counts. The same machinery covers epidemics, queues and any point process.

The package is part of the SciML ecosystem. It offers:

- **Exact methods.** Gillespie's direct method and its relatives, called aggregators. `Direct()` is the default. Others include next-reaction and rejection-based methods.
- **Jump types.** `MassActionJump` for standard mass-action reactions (the fastest), `ConstantRateJump` for any rate function that stays constant between jumps, and `VariableRateJump` for rates that change in time or with continuous dynamics.
- **Approximate methods.** Tau-leaping, which fires many jumps per step, through `RegularJump`.
- **Hybrids.** Jumps coupled to ODEs or SDEs, such as piecewise deterministic Markov processes and jump-diffusions.

Key assumption for the exact path: between jumps the rates are constant, so waiting times are exponential. `SSAStepper` handles pure jump problems.

## When to use it

- You work in Julia and want fast exact stochastic simulation with many reactions or species.
- Your model mixes jumps with ODEs or SDEs.
- You simulate point processes with time-varying intensity, not only chemistry.

Alternatives:

- [GillesPy2](gillespy2.md) is the Python route to exact and tau-leaping solvers.
- [Tellurium](tellurium.md) runs a Gillespie integrator from an Antimony or SBML model.
- [epydemix](epydemix.md) fits epidemics with age groups and contact matrices.

## Install

JumpProcesses.jl 10.0.0 is the current release in the Julia General registry (MIT, Julia 1.10 or newer). The README installs it with the package manager:

```julia
using Pkg
Pkg.add("JumpProcesses")
```

The README warns that 10.0 is a transitional release. StochasticDiffEq, ModelingToolkit and Catalyst cannot yet be installed beside it, so an environment that includes them keeps version 9.x. Its advice is to wait for 10.0.1 unless you use JumpProcesses on its own. Jumps coupled to delay differential equations are not supported in 10.0. Coupling jumps to ODEs needs an extra solver package such as `OrdinaryDiffEqTsit5`.

The recipe on this page uses the official `julia:1.12.7-bookworm` image, adds JumpProcesses 10.0.0 to a project folder and precompiles it.

## A first run

Adapted from the [README example](https://github.com/SciML/JumpProcesses.jl#stochastic-chemical-kinetics-sir-model). It is a stochastic SIR epidemic with two reactions, S + I to 2I and I to R:

```julia
using JumpProcesses

# order S = 1, I = 2, R = 3
substoich = [[1 => 1, 2 => 1],    # S + I
             [2 => 1]]            # I
netstoich = [[1 => -1, 2 => 1],   # S -> S-1, I -> I+1
             [2 => -1, 3 => 1]]   # I -> I-1, R -> R+1
p = (0.1 / 1000, 0.01)            # rate constants
maj = MassActionJump(substoich, netstoich; param_idxs = [1, 2])

u0 = [999, 1, 0]
dprob = DiscreteProblem(u0, (0.0, 250.0), p)
jprob = JumpProblem(dprob, Direct(), maj)
sol = solve(jprob, SSAStepper(); seed = 1234)
```

In version 10 the random number generator is set in `solve`, with `seed` or `rng`. In version 9 it was a keyword of `JumpProblem`.

## Run the tested example

This recipe builds JumpProcesses.jl in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.4 s.

1. Download [jumpprocesses-recipe.tar.gz](https://biosimhub.pages.dev/guides/jumpprocesses/jumpprocesses-recipe.tar.gz) (Dockerfile, run_jumpprocesses.jl, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf jumpprocesses-recipe.tar.gz
   cd jumpprocesses
   sh run.sh
   ```

![Terminal recording of the JumpProcesses.jl example run](https://biosimhub.pages.dev/media/jumpprocesses/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/jumpprocesses:10.0.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/jumpprocesses:10.0.0 julia --project=/opt/jp /opt/run_jumpprocesses.jl \
    --population 1000 --infected 1 --beta 0.1 \
    --gamma 0.01 --tend 250 --points 126 --runs 5 \
    --seed 1234 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `final_sizes.csv` | 86 B |
| `run_log.txt` | 96 B |
| `trajectories.csv` | 9.4 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/jumpprocesses/result-dark.png"><img src="https://biosimhub.pages.dev/media/jumpprocesses/result.png" alt="Plot of the JumpProcesses.jl example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>final_sizes.csv</code></summary>

```
run,final_S,final_I,final_R
1,0,183,817
2,0,208,792
3,1,271,728
4,999,0,1
5,0,167,833
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
JumpProcesses 10.0.0 population=1000 infected=1 beta=0.1 gamma=0.01 tend=250.0 runs=5 seed=1234
```

</details>

<details><summary>First lines of <code>trajectories.csv</code></summary>

```
run,time,S,I,R
1,0,999,1,0
1,2,999,1,0
1,4,999,1,0
1,6,998,2,0
1,8,997,3,0
1,10,996,4,0
1,12,996,4,0
1,14,994,6,0
1,16,994,6,0
1,18,992,8,0
1,20,989,11,0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--population` | Population size | 1000 | 10 to 1000000 |
| `--infected` | Initially infected | 1 | 1 to 1000 |
| `--beta` | Infection rate constant (divided by population) | 0.1 | 0.0001 to 100 |
| `--gamma` | Recovery rate | 0.01 | 0.0001 to 100 |
| `--tend` | End time | 250 | 0.1 to 100000 |
| `--points` | Output time points | 126 | 2 to 2000 |
| `--runs` | Runs | 5 | 1 to 100 |
| `--seed` | Seed | 1234 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- **`sol.t` and `sol.u`.** The jump times and the state after each one. The state vector holds S, I and R counts.
- **Piecewise constant.** `sol(t)` returns the state at time `t` without interpolation. Between two jumps the state does not change, and the docs say evaluation at a time between saved points is not interpolated.
- **Epidemic shape.** With `S + I -> 2I` at 0.1/1000 and `I -> R` at 0.01, one infected person in 1000 starts a wave. Infected counts rise, peak and fall as susceptibles run out. A run can also die out early by chance, which is why several seeds matter.
- **Recipe files.** `trajectories.csv` holds S, I and R on a fixed time grid for each run. `final_sizes.csv` holds the final counts per run.

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **One active solve per `JumpProblem`.** Version 10 reuses the problem's internal state, so concurrent solves need `deepcopy(jprob)` or an `EnsembleProblem`.
- **Only one `MassActionJump` per problem.** It must hold all mass-action reactions. Put other reactions in `ConstantRateJump`s.
- **First call is slow.** Julia compiles on first use. Precompiling in the image avoids most of it. Time the second call, not the first.
- **Reproducibility.** Pass `seed` to `solve`. The RNG moved from `JumpProblem` to `solve` in 10.0.
- **Time-varying rates are not constant-rate jumps.** If a rate depends on time or an ODE state, use `VariableRateJump`. A `ConstantRateJump` would give wrong waiting times.

## Further reading

- Repository: https://github.com/SciML/JumpProcesses.jl
- Documentation: https://docs.sciml.ai/JumpProcesses/stable/
- SSA tutorial: https://docs.sciml.ai/JumpProcesses/stable/tutorials/discrete_stochastic_example/
- Breaking changes in 10.0: https://github.com/SciML/JumpProcesses.jl/blob/master/HISTORY.md
- Zagatti GA, Isaacson SA, Rackauckas C, Ilin V, Ng SK, Bressan S (2024). Extending JumpProcesses.jl for fast point process simulation with time-varying intensities. Proc JuliaCon 6(58):133. https://doi.org/10.21105/jcon.00133

---

Cite: Zagatti GA, Isaacson SA, Rackauckas C, Ilin V, Ng SK, Bressan S (2024). Extending JumpProcesses.jl for fast point process simulation with time-varying intensities. Proc JuliaCon 6(58):133. doi:10.21105/jcon.00133

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/jumpprocesses).
