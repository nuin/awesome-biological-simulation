# Catalyst.jl

> Simulate a mass-action reaction network (Michaelis-Menten enzyme kinetics) as a deterministic ODE or an exact stochastic Gillespie process.

Licence: MIT · [Source code](https://github.com/SciML/Catalyst.jl)

## What it simulates

Catalyst.jl turns a list of chemical reactions into a simulation model. You write the reactions in a Julia macro, `@reaction_network`, in a notation close to chemistry. Catalyst builds the symbolic system behind it and passes it to a solver from the Julia SciML ecosystem.

The same network can be run as:

- **ODEs**, the reaction rate equations with continuous concentrations.
- **SDEs**, the chemical Langevin equation with noise terms.
- **Jump processes**, exact stochastic simulation (Gillespie's direct method and related algorithms) with integer molecule counts.
- **Hybrid models** that mix ODE, SDE and jump reactions in one system. This is new in version 16.

Catalyst also does network analysis (linkage classes, deficiency, reversibility), steady-state and bifurcation analysis, spatial models on discrete domains, parameter fitting, and import of SBML and BioNetGen files. Rate laws follow mass action unless you give another rate expression.

## When to use it

Use Catalyst.jl when you work in Julia and want one model definition that runs deterministically and stochastically, with access to the SciML solvers and optimisation tools.

- [GillesPy2](gillespy2.md) is the Python option for stochastic and ODE simulation of reaction networks.
- [COPASI](copasi.md) has a desktop interface, parameter estimation and SBML support, with no coding.
- [XPPAUT](xppaut.md) is the choice for phase planes and bifurcation diagrams of small ODE systems.

## Install

Catalyst is in the Julia General registry. The current release is v16.5.0 (30 September 2026). It needs Julia 1.10 or later. The repository licence is MIT.

```julia
using Pkg
Pkg.activate("catalyst_environment")
Pkg.add("Catalyst")
Pkg.add(["OrdinaryDiffEq", "JumpProcesses"])
```

This follows the Installation section of the Catalyst README, which recommends a new environment. OrdinaryDiffEq and JumpProcesses supply the ODE and jump solvers used in the examples below. To fix the version, use `Pkg.add(name="Catalyst", version="16.5.0")`.

Version 16 is a breaking release. Code written for version 15 or earlier may need changes. The project's HISTORY.md has the migration guide.

## Run the tested example

This recipe builds Catalyst.jl in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 36.5 s.

1. Download [catalyst-jl-recipe.tar.gz](https://biosimhub.pages.dev/guides/catalyst-jl/catalyst-jl-recipe.tar.gz) (Dockerfile, run_catalyst.jl, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf catalyst-jl-recipe.tar.gz
   cd catalyst-jl
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/catalyst-jl:16.5.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/catalyst-jl:16.5.0 julia /opt/run_catalyst.jl ode 50 10 0.01 0.1 0.1 200 1 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 58 B |
| `timeseries.csv` | 15.5 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
method ode: 201 time points, final P = 49.857956447827775
```

</details>

<details><summary>First lines of <code>timeseries.csv</code></summary>

```
time,S,E,SE,P
0.0,50.0,10.0,0.0,0.0
1.0,46.32739176507861,6.523203661936156,3.4767963380638416,0.1958118968575483
2.0,44.23460980944567,4.8706101902682715,5.129389809731727,0.6360003808226022
3.0,42.86885016121941,4.062913487567936,5.937086512432062,1.1940633263485223
4.0,41.85767976061686,3.667576263063545,6.3324237369364536,1.8098965024466855
5.0,41.02578922446651,3.479528567929467,6.520471432070531,2.453739343462963
6.0,40.28720698182838,3.397708324216323,6.602291675783675,3.110501342387943
7.0,39.59867339025687,3.3710643768759367,6.628935623124061,3.772390986619074
8.0,38.938091989887624,3.373422856553343,6.626577143446656,4.435330866665722
9.0,38.29423253707894,3.3914234037603976,6.608576596239601,5.097190866681466
10.0,37.66102449402304,3.417797050086797,6.582202949913201,5.7567725560637655
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `method` | Simulation type | ode | ode, jump |
| `s0` | Initial substrate S | 50 | 1 to 100000 |
| `e0` | Initial enzyme E | 10 | 1 to 100000 |
| `kb` | Binding rate kB | 0.01 | 1e-06 to 100 |
| `kd` | Unbinding rate kD | 0.1 | 1e-06 to 100 |
| `kp` | Catalysis rate kP | 0.1 | 1e-06 to 100 |
| `tend` | End time | 200 | 1 to 10000 |
| `dt` | Output interval | 1 | 0.01 to 1000 |
| `seed` | Seed (jump simulations) | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Quick examples in the Catalyst README, https://github.com/SciML/Catalyst.jl. Michaelis-Menten enzyme kinetics as an ODE:

```julia
using Catalyst, OrdinaryDiffEq

model = @reaction_network begin
    kB, S + E --> SE
    kD, SE --> S + E
    kP, SE --> P + E
end

u0 = [:S => 50.0, :E => 10.0, :SE => 0.0, :P => 0.0]
tspan = (0., 200.)
ps = [:kB => 0.01, :kD => 0.1, :kP => 0.1]
sol = solve(ODEProblem(model, u0, tspan, ps))
```

The same model as an exact stochastic simulation, with integer initial counts:

```julia
using JumpProcesses
u0_integers = [:S => 50, :E => 10, :SE => 0, :P => 0]
jump_sol = solve(JumpProblem(model, u0_integers, tspan, ps))
```

The recipe's script `run_catalyst.jl` runs this model with either method and writes the time series as a CSV file. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

`timeseries.csv` has the columns `time`, `S`, `E`, `SE` and `P`, one row per output interval.

- In the ODE run the values are concentrations or amounts as real numbers. Substrate S falls, product P rises, and the free enzyme E dips while the complex SE is present. Total enzyme E + SE stays constant, and S + SE + P stays constant, because the reactions only move material between those species.
- In the jump run the values are whole numbers. Two runs with different seeds follow different paths around the ODE curve. With 50 substrate molecules the difference is visible. With thousands of molecules the paths approach the ODE.

`run_log.txt` has one line with the method, the number of time points and the final value of P. In the Julia solution object, `sol[:P]` gives the values of P over time, and `sol.t` the times.

## Pitfalls

- **Integer counts for jumps.** Jump simulations track molecule numbers. Give integer initial values, as in the README example.
- **Time to first run.** Julia compiles on first use. The first simulation in a fresh session can take much longer than later ones.
- **Parameter and species names are symbols.** Use `:kB`, not `kB`, when you set values in `ps` and `u0`.
- **Package versions float.** Catalyst depends on ModelingToolkitBase and the SciML solvers. Record the Manifest.toml of a working environment to repeat a result.
- **Solver choice.** The README calls `solve` without naming an algorithm. For stiff systems, name one, such as a Rosenbrock or BDF method from OrdinaryDiffEq.
- **Reaction order and rates.** Catalyst uses mass-action rates: the rate is the constant times the product of the reactant amounts. Write an explicit expression for other kinetics.

## Further reading

- Documentation: https://docs.sciml.ai/Catalyst/stable/
- README and quick examples: https://github.com/SciML/Catalyst.jl
- Migration notes: https://github.com/SciML/Catalyst.jl/blob/master/HISTORY.md
- Paper: Loman TE, Ma Y, Ilin V, Gowda S, Korsbo N, Yewale N, Rackauckas C, Isaacson SA (2023). Catalyst: Fast and flexible modeling of reaction networks. PLoS Computational Biology 19:e1011530. https://doi.org/10.1371/journal.pcbi.1011530

---

Cite: Loman TE, Ma Y, Ilin V, Gowda S, Korsbo N, Yewale N, Rackauckas C, Isaacson SA (2023). Catalyst: Fast and flexible modeling of reaction networks. PLoS Comput Biol 19:e1011530. doi:10.1371/journal.pcbi.1011530

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/catalyst-jl).
