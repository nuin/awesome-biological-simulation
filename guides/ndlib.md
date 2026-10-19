# NDlib

> Run an SI, SIS, SIR or SEIR epidemic on a random network (Erdos-Renyi, Barabasi-Albert or Watts-Strogatz) and write the compartment counts per iteration.

Licence: BSD-2-Clause · [Source code](https://github.com/GiulioRossetti/ndlib)

## What it simulates

NDlib simulates a spreading process on a network. Nodes are people, and edges are contacts. Each iteration, every infected node passes the infection to each susceptible neighbour with probability `beta`. Infected nodes recover with probability `gamma`.

NDlib ships many models. The biosimhub recipe runs four epidemic models: SI (infected nodes stay infected), SIS (they recover to susceptible and can be infected again), SIR (they recover and become removed) and SEIR (susceptible nodes first pass through a non-infectious exposed state). The library also has opinion-dynamics and threshold models that the recipe does not use.

The key assumption is that time is discrete and that the network does not change during the run. Each node is in one state and all contacts transmit with the same probability.

## When to use it

- You want to see how network shape changes an epidemic with the same transmission and recovery settings.
- You want a quick SIR, SIS or SEIR curve on a graph of 50 to 20,000 nodes, with counts per iteration in a CSV.
- You teach epidemics on networks and want the contact structure to be visible in the results.

Use [epydemix](epydemix.md) for a well-mixed population with age groups and contact matrices. Use [Covasim](covasim.md) when you need a COVID-19 model with households, schools and workplaces already built in.

## Install it yourself

NDlib 6.0.1 is on PyPI. Its package metadata omits `six`, which it imports, so the recipe installs both:

```
python3.11 -m venv nd && . nd/bin/activate
pip install ndlib==6.0.1 six
```

A minimal run with the Python API, tried in the recipe's image:

```python
import networkx as nx
import ndlib.models.ModelConfig as mc
import ndlib.models.epidemics as ep

g = nx.erdos_renyi_graph(1000, 0.01, seed=1)
model = ep.SIRModel(g, seed=1)
cfg = mc.Configuration()
cfg.add_model_parameter("beta", 0.05)
cfg.add_model_parameter("gamma", 0.1)
cfg.add_model_parameter("fraction_infected", 0.01)
model.set_initial_status(cfg)
trends = model.build_trends(model.iteration_bunch(100))
counts = trends[0]["trends"]["node_count"]
```

After 100 iterations the final counts were 30 susceptible, 1 infected and 969 removed. The peak number infected was 489.

## Run the tested example

This recipe builds NDlib in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.8 s.

1. Download [ndlib-recipe.tar.gz](https://biosimhub.pages.dev/guides/ndlib/ndlib-recipe.tar.gz) (Dockerfile, run_ndlib.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf ndlib-recipe.tar.gz
   cd ndlib
   sh run.sh
   ```

![Terminal recording of the NDlib example run](https://biosimhub.pages.dev/media/ndlib/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/ndlib:6.0.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/ndlib:6.0.1 python /opt/run_ndlib.py --model SIR --graph erdos_renyi \
    --nodes 1000 --degree 10 --beta 0.05 --gamma 0.1 \
    --alpha 0.2 --infected 0.01 --iterations 100 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 256 B |
| `summary.json` | 277 B |
| `trends.csv` | 1.4 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/ndlib/result-dark.png"><img src="https://biosimhub.pages.dev/media/ndlib/result.png" alt="Plot of the NDlib example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
{"ndlib": "6.0.1", "model": "SIR", "graph": "erdos_renyi", "nodes": 1000, "edges": 4988, "mean_degree": 9.976, "max_degree": 20, "clustering": 0.0111, "peak_infected": 451, "peak_iteration": 19, "fina
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "ndlib": "6.0.1",
 "model": "SIR",
 "graph": "erdos_renyi",
 "nodes": 1000,
 "edges": 4988,
 "mean_degree": 9.976,
 "max_degree": 20,
 "clustering": 0.0111,
 "peak_infected": 451,
 "peak_iteration": 19,
 "final": {
```

</details>

<details><summary>First lines of <code>trends.csv</code></summary>

```
iteration,Susceptible,Infected,Removed
0,990,10,0
1,988,12,0
2,979,18,3
3,969,27,4
4,956,36,8
5,941,48,11
6,921,63,16
7,889,90,21
8,860,106,34
9,819,138,43
10,776,169,55
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--model` | Epidemic model | SIR | SI, SIS, SIR, SEIR |
| `--graph` | Network | erdos_renyi | erdos_renyi, barabasi_albert, watts_strogatz |
| `--nodes` | Nodes | 1000 | 50 to 20000 |
| `--degree` | Target mean degree | 10 | 2 to 50 |
| `--beta` | Infection probability per contact per iteration | 0.05 | 0.001 to 1 |
| `--gamma` | Recovery probability per iteration (SIS | 0.1 | 0.001 to 1 |
| `--alpha` | Incubation rate (SEIR) | 0.2 | 0.001 to 1 |
| `--infected` | Initially infected fraction | 0.01 | 0.001 to 0.5 |
| `--iterations` | Iterations | 100 | 5 to 1000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's script `run_ndlib.py` builds the graph with NetworkX, creates the model with your seed, sets `beta`, `gamma` (called `lambda` in SIS) and the starting infected fraction, runs the iterations and writes three files.

The example is SIR on an Erdos-Renyi graph of 1,000 nodes with mean degree 10, `beta` 0.05, `gamma` 0.1, 1 percent infected at the start, 100 iterations and seed 42. It ran in 1.8 seconds.

- `run_log.txt` and `summary.json` hold the same summary. The graph has 4,988 edges, a mean degree of 9.976, a maximum degree of 20 and a clustering coefficient of 0.0111. The infected count peaked at 451 at iteration 19. At the end, 45 nodes were susceptible, none infected and 955 removed.
- `trends.csv` has one row per iteration (100 rows) and the columns `iteration,Susceptible,Infected,Removed`. SEIR adds an `Exposed` column. Iteration 0 shows 990 susceptible and 10 infected. Iteration 10 shows 776, 169 and 55.

The infection died out at iteration 79, the first row with zero infected. The 955 removed nodes are 95.5 percent of the network. With a transmission chance per contact of beta/(beta+gamma) = 0.33 and about 10 contacts, a large outbreak is expected, and one occurred.

## Your own runs

Same image and seed 42, one option changed from the example.

- **Scale-free network** (`--graph barabasi_albert`). Mean degree 9.95 but a maximum degree of 148. The peak rose to 495 infected at iteration 14, five iterations earlier than the random graph. The final removed count was 944.
- **Clustered network** (`--graph watts_strogatz`). Mean degree 10 and clustering 0.499. The peak fell to 327 at iteration 25, and 980 nodes were removed at the end. High clustering means neighbours share contacts, and the peak is lower than on the random graph.
- **Lower infection chance** (`--beta 0.02`). The peak fell to 107 at iteration 52, and the epidemic had not ended after 100 iterations: 371 susceptible, 33 infected, 596 removed.
- **SIS** (`--model SIS --iterations 200`). The infection does not die out. The peak was 794 at iteration 72, and the end state was 223 susceptible and 777 infected.
- **SEIR** (`--model SEIR`, incubation rate 0.2). The peak of infectious nodes was 276 at iteration 39, 20 iterations later than SIR. The final state was 29 susceptible, 2 infected and 969 removed.
- **SI** (`--model SI`). All 1,000 nodes were infected by iteration 40.
- **Another seed** (`--seed 43`). The random graph changes (4,950 edges), with a peak of 448 at iteration 17 and 948 removed.

Two runs with seed 42 gave identical `trends.csv` files.

## Pitfalls

- **Seed the graph and the model.** The recipe passes the seed to NetworkX and to NDlib, and also sets the global Python and NumPy seeds.
- **Probabilities are per iteration and per contact.** `beta` 0.05 means each infected neighbour infects with a 5 percent chance each step.
- **SIS has no end.** The infection can persist for the whole run, so pick the iteration count to cover the plateau.
- **Status codes differ by model.** The recipe writes names in the CSV header. In the Python API the codes are numbers, for example 0 susceptible, 1 infected, 2 removed in SIR.

## Further reading

- Documentation: https://ndlib.readthedocs.io/en/latest/
- Source: https://github.com/GiulioRossetti/ndlib
- Paper: Rossetti G et al. (2018) NDlib: a python library to model and analyze diffusion processes over complex networks. Int J Data Sci Anal 5:61-77. https://doi.org/10.1007/s41060-017-0086-6

---

Cite: Rossetti G, Milli L, Rinzivillo S, Sirbu A, Pedreschi D, Giannotti F (2018). NDlib: a python library to model and analyze diffusion processes over complex networks. Int J Data Sci Anal 5:61-77. doi:10.1007/s41060-017-0086-6

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/ndlib).
