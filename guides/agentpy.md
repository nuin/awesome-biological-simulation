# AgentPy

> Run an agent-based SIR epidemic on a small-world contact network and write the infection time series and a summary.

Licence: BSD-3-Clause · [Source code](https://github.com/jofmi/agentpy)

## What it simulates

AgentPy is a Python framework for agent-based models. You write an agent class and a model class. The model creates the agents, calls their `step` method once per time step, records data and stops on a condition. Agents can sit on a network, a grid or in open space.

AgentPy ships no fixed model, so the recipe adds one: a stochastic SIR epidemic on a Watts-Strogatz small-world network. Each agent is susceptible (S), infected (I) or recovered (R). In every step an infected agent infects each susceptible neighbour with probability `infect`, then recovers with probability `recover`. New infections take effect at the end of the step, so the order of agents does not matter. The helper script `run_agentpy.py` holds the model in about 70 lines.

## When to use it

Use AgentPy when individuals differ or interact locally, and a set of differential equations would hide that. Typical cases are contact networks, spatial spread, and behaviour rules.

- Use [Agents.jl](agents-jl.md) for the same kind of model when speed matters. Agents.jl is compiled Julia, aimed at large populations.
- Use [Epydemix](epydemix.md) when you want a ready-made age-structured epidemic model instead of writing agent rules.
- Use [GillesPy2](gillespy2.md) for well-mixed stochastic reaction systems, where there is no network.

## Install it yourself

AgentPy installs from PyPI. The recipe uses a Python 3.12 environment with NumPy, pandas, SciPy, NetworkX and Matplotlib from conda-forge, then:

```
pip install agentpy==0.1.5
```

This resolved and imported in the 0.1.5 image. The helper script uses four calls: `ap.AgentList` to make the agents, `ap.Network` with `add_agents` to place them on a NetworkX graph, `Model.run` to execute the steps and `Model.stop` to end the run when no agent is infected.

## Run the tested example

This recipe builds AgentPy in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.8 s.

1. Download [agentpy-recipe.tar.gz](https://biosimhub.pages.dev/guides/agentpy/agentpy-recipe.tar.gz) (Dockerfile, run_agentpy.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf agentpy-recipe.tar.gz
   cd agentpy
   sh run.sh
   ```

![Terminal recording of the AgentPy example run](https://biosimhub.pages.dev/media/agentpy/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/agentpy:0.1.5 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/agentpy:0.1.5 python /opt/run_agentpy.py --agents 500 --degree 6 \
    --rewire 0.1 --infect 0.15 --recover 0.1 --seeds 5 \
    --steps 150 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 87 B |
| `sir.csv` | 1.0 KB |
| `summary.csv` | 95 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/agentpy/result-dark.png"><img src="https://biosimhub.pages.dev/media/agentpy/result.png" alt="Plot of the AgentPy example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 75 steps, peak 205 infected at step 16, 496 of 500 ever infected (agentpy 0.1.5)
```

</details>

<details><summary>First lines of <code>sir.csv</code></summary>

```
step,susceptible,infected,recovered
0,495,5,0
1,488,11,1
2,482,16,2
3,469,28,3
4,451,38,11
5,440,44,16
6,430,50,20
7,413,60,27
8,394,73,33
9,367,94,39
10,338,113,49
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
agents,steps_run,peak_infected,peak_step,final_recovered,attack_rate
500,75,205,16,496,0.992
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--agents` | Number of agents | 500 | 10 to 5000 |
| `--degree` | Contacts per agent (even) | 6 | 2 to 20 |
| `--rewire` | Network rewiring probability | 0.1 | 0 to 1 |
| `--infect` | Infection probability per contact per step | 0.15 | 0 to 1 |
| `--recover` | Recovery probability per step | 0.1 | 0.001 to 1 |
| `--seeds` | Initially infected agents | 5 | 1 to 100 |
| `--steps` | Maximum steps | 150 | 1 to 1000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is 500 agents, 6 contacts each, rewiring 0.1, infection 0.15, recovery 0.1, 5 initial cases and seed 42. It finished in 3.8 s.

- `run_log.txt` has one line: "done: 75 steps, peak 205 infected at step 16, 496 of 500 ever infected (agentpy 0.1.5)". The run stopped at step 75 because no agent was infected any more.
- `sir.csv` has one row per step with the S, I and R counts. Step 0 is 495, 5, 0. Step 10 is 338, 113, 49.
- `summary.csv` has one row: peak infected 205 at step 16, 496 recovered and an attack rate of 0.992.

Check the result against the basic reproduction number. Each agent has 6 contacts, so a case infects about 6 x 0.15 = 0.9 neighbours per step. A case stays infectious for 1 / 0.1 = 10 steps on average, so R0 is near 9. An R0 that large infects almost everyone, which matches the 99.2% attack rate. The network clustering lowers the true value somewhat, because neighbours share contacts.

## Your own runs

Each run changes one value from the example. All used the same image.

- **Weaker infection.** `--infect 0.03` gives R0 near 1.8 by the same estimate. Only 13 of 500 agents were ever infected (attack rate 0.026), and the peak stayed at the 5 seeded cases. The outbreak died out in 39 steps. A mean-field SIR model with R0 of 1.8 predicts a large epidemic, so clustering and the random loss of the first cases matter here.
- **No rewiring.** `--rewire 0` makes a plain ring lattice. Contacts are only to near neighbours on the ring. The peak fell to 68 infected at step 22, and the run reached the 150-step limit with 444 agents ever infected (attack rate 0.888, 435 recovered). Shortcuts in the example network (rewiring 0.1) are what produce a fast, tall peak.
- **Another seed.** `--seed 43` gave a peak of 241 at step 18 and an attack rate of 0.994, close to the seed 42 result. Far above the threshold, the two replicates agree.
- **Very weak infection.** `--infect 0.01` infected 9 agents in total and ended at step 26.

## Pitfalls

- **One seed controls both the graph and the dynamics.** The helper passes the seed to NetworkX and to the model, so a changed seed gives a different network as well as different transmissions.
- **One run is one sample.** The model is stochastic, and a weak outbreak can die out after a few steps. Report the distribution over many seeds, not one run.
- **The step limit can cut a run short.** The ring-lattice run reached the 150-step limit with infections still going. Raise `--steps` when `steps_run` equals the limit.
- **Degree must be even and below the agent count.** The Watts-Strogatz graph needs it, and the helper exits with a message otherwise.
- **Agents are Python objects.** The helper loops over all agents each step, so run time grows with agents times steps. The recipe limits agents to 5000.

## Further reading

- AgentPy documentation: https://agentpy.readthedocs.io
- Source: https://github.com/jofmi/agentpy
- Paper: Foramitti J (2021) AgentPy: A package for agent-based modeling in Python. Journal of Open Source Software 6(62):3065. https://doi.org/10.21105/joss.03065

---

Cite: Foramitti J (2021). AgentPy: A package for agent-based modeling in Python. Journal of Open Source Software 6(62):3065. doi:10.21105/joss.03065

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/agentpy).
