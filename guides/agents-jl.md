# Agents.jl

> Run a Schelling segregation agent-based model on a grid in Julia and write the happiness and same-group share per step plus the final grid.

Licence: MIT · [Source code](https://github.com/JuliaDynamics/Agents.jl)

## What it simulates

Agents.jl is a Julia package for agent-based models. You define an agent type, a space (grid, continuous space, graph or OpenStreetMap), a step rule and a scheduler. The package runs the model, collects data and keeps the code short and fast.

The recipe runs Schelling's segregation model, the standard Agents.jl example. Two groups of residents live on a square grid with at most one resident per cell. A resident is happy when at least `min_happy` of the neighbours within `radius` cells belong to the same group. An unhappy resident moves to a random empty cell. Nobody asks for segregation, yet the groups separate. The helper script `run_agents.jl` records the share of happy residents and the mean share of same-group neighbours at every step.

## When to use it

Use Agents.jl when you want an agent-based model that runs fast enough for large populations and many replicates, or when the agents move in space.

- Use [AgentPy](agentpy.md) when you prefer Python and your populations are small.
- Use [Parcels](parcels.md) or [OpenDrift](opendrift.md) for passive particles in a flow, where agents do not decide anything.
- Use [Epydemix](epydemix.md) for ready-made epidemic models.

## Install it yourself

From a Julia 1.11 session:

```
using Pkg
Pkg.add(PackageSpec(name="Agents", version="7.1.0"))
```

This installed Agents 7.1.0 on Julia 1.11.7. The whole image build, including the Julia download, took 2 min 14 s. The script uses the `@agent struct` macro and the `StandardABM` constructor of Agents 7. Run the recipe's script with `julia /opt/run_agents.jl --size 40 --seed 42`.

## Run the tested example

This recipe builds Agents.jl in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.3 s.

1. Download [agents-jl-recipe.tar.gz](https://biosimhub.pages.dev/guides/agents-jl/agents-jl-recipe.tar.gz) (Dockerfile, run_agents.jl, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf agents-jl-recipe.tar.gz
   cd agents-jl
   sh run.sh
   ```

![Terminal recording of the Agents.jl example run](https://biosimhub.pages.dev/media/agents-jl/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/agents-jl:7.1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/agents-jl:7.1.0 julia /opt/run_agents.jl --size 40 --density 0.8 \
    --minority 0.5 --min-happy 3 --radius 1 --steps 50 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `grid.csv` | 9.5 KB |
| `run_log.txt` | 92 B |
| `steps.csv` | 242 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/agents-jl/result-dark.png"><img src="https://biosimhub.pages.dev/media/agents-jl/result.png" alt="Plot of the Agents.jl example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>grid.csv</code></summary>

```
x,y,group
1,3,1
1,4,1
1,6,1
1,7,1
1,8,1
1,9,1
1,11,1
1,12,1
1,20,1
1,21,1
1,22,1
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 1280 agents on 40x40, 12 steps, 100.0 % happy, same-group share 0.8 (Agents.jl 7.1.0)
```

</details>

<details><summary>First lines of <code>steps.csv</code></summary>

```
step,fraction_happy,mean_same_group_share
0,0.6375,0.5
1,0.8289,0.6195
2,0.8977,0.6964
3,0.9273,0.7283
4,0.9547,0.7547
5,0.9664,0.7738
6,0.9805,0.783
7,0.9867,0.7898
8,0.993,0.7971
9,0.9969,0.7958
10,0.9984,0.7979
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--size` | Grid side length | 40 | 5 to 150 |
| `--density` | Fraction of cells occupied | 0.8 | 0.1 to 0.95 |
| `--minority` | Fraction in the smaller group | 0.5 | 0.05 to 0.5 |
| `--min-happy` | Neighbours of the same group needed to be happy | 3 | 0 to 24 |
| `--radius` | Neighbourhood radius (cells) | 1 | 1 to 3 |
| `--steps` | Maximum steps | 50 | 1 to 500 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is a 40 x 40 grid with 80% of the cells occupied (1,280 residents), two equal groups, a radius of 1 and `min_happy` of 3. It ran in 3.3 s.

- `run_log.txt` has the line "done: 1280 agents on 40x40, 12 steps, 100.0 % happy, same-group share 0.8 (Agents.jl 7.1.0)". The run stopped at step 12 because everyone was happy.
- `steps.csv` has one row per step. Step 0 is 63.75% happy with a mean same-group share of 0.50, which is what a random mix gives. Step 1 is 82.89% and 0.6195. Step 5 is 96.64% and 0.7738. Step 10 is 99.84% and 0.7979.
- `grid.csv` (9,691 bytes) lists every resident with its `x`, `y` and `group`.

The rule only asks for 3 same-group neighbours out of at most 8, which is about 40%. The final neighbourhoods are 80% same-group. The preference was mild and the outcome was strong, which is the point of the model.

## Your own runs

Each run changes one setting from the example. All finished in about 3.3 s.

- **Milder preference.** `--min-happy 2` ended after 5 steps with a same-group share of 0.62. The groups barely separated.
- **Stricter preference.** `--min-happy 4` took 49 steps and ended at 0.943. Starting happiness was only 36.2%.
- **Too strict.** `--min-happy 5` did not settle. After the 50-step limit 75.3% were happy and the share was 0.857. At the start only 13.7% were happy.
- **Fuller grid.** `--density 0.95` ended after 11 steps at 0.767. With few empty cells the residents have less room to sort.
- **Smaller minority.** `--minority 0.2` was still moving at step 50, with 97.8% happy and a share of 0.852. The starting share was already 0.677, because the 80% majority fills most neighbourhoods.
- **Larger neighbourhood.** `--radius 2 --min-happy 8` ended after 25 steps at 0.825.
- **Another seed.** `--seed 43` finished in 16 steps at 0.812, against 12 steps and 0.800 for seed 42. The final share varies by about 0.01 between seeds, and the number of steps varies more.

## Pitfalls

- **`min_happy` is a count, not a fraction.** Its useful range depends on the radius. With radius 1 a cell has at most 8 neighbours, so a value of 5 is already 62%. The helper does not rescale it.
- **Runs may not converge.** A strict rule can leave residents moving forever, as with `--min-happy 5`. The step limit ends the run, and the log then shows less than 100% happy.
- **Edges count.** The grid is not periodic, so an agent at the edge has fewer neighbours and finds it harder to be happy.
- **First run is slower.** The Julia code compiles on the first call. The recipe precompiles the packages in the image, so the example still ran in 3.3 s, including the compile of the model code.
- **Pin the version.** The script was written and run against Agents 7.1.0. Check the release notes before moving to another major version.

## Further reading

- Agents.jl documentation: https://juliadynamics.github.io/Agents.jl/stable/
- Source: https://github.com/JuliaDynamics/Agents.jl
- Paper: Datseris G, Vahdati AR, DuBois TC (2024) Agents.jl: a performant and feature-full agent-based modeling software of minimal code complexity. SIMULATION 100(10):1019-1031. https://doi.org/10.1177/00375497211068820

---

Cite: Datseris G, Vahdati AR, DuBois TC (2024). Agents.jl: a performant and feature-full agent-based modeling software of minimal code complexity. SIMULATION 100(10):1019-1031. doi:10.1177/00375497211068820

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/agents-jl).
