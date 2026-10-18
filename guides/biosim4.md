# biosim4

> Evolve a population of neural-network agents on a 2D grid under a chosen selection challenge and log survivors, diversity and genome length per generation.

Licence: MIT · [Source code](https://github.com/davidrmiller/biosim4)

## What it simulates

biosim4 evolves a population of small neural-network agents on a 2D grid. Each agent has a genome of 32-bit genes. Each gene wires one sensor or internal neuron to one internal neuron or action, with a signed weight. Agents live for a fixed number of steps per generation and move around the grid. At the end of a generation the selection rule (the "challenge") decides who may reproduce. Survivors pair up, recombine their genomes, mutate, and fill the next generation.

Nothing in the genome says where to go. The agents learn to reach the survival zone only because the ones that wander into it leave offspring. The example uses challenge 6: survivors are agents within a quarter of the grid side from any of the four corners, and agents closer to a corner are weighted more heavily as parents.

The model is a toy, not a calibrated population-genetic model. It shows selection, drift, recombination and mutation acting on a behaviour encoded in a genome.

## When to use it

Use biosim4 to teach or explore how selection builds behaviour from random genomes:

- How fast does a population reach a survival zone under a given challenge?
- What does genetic diversity do while selection is strong?
- How do mutation rate, sexual reproduction or barriers change that?

For allele-frequency models with explicit loci and fitness, use [SLiM](slim.md), [fwdpy11](fwdpy11.md) or [simuPOP](simupop.md). For agents on a grid with scripted rules, [NetLogo](netlogo.md) is the better fit. biosim4 is the one here where the behaviour itself evolves.

## Install it yourself

biosim4 builds with `make` and needs OpenCV and CImg. On Debian 12 or Ubuntu 22.04:

```
sudo apt-get install build-essential libopencv-dev cimg-dev
git clone https://github.com/davidrmiller/biosim4
cd biosim4 && git checkout 45e808cc86e24bae941b60ddebbedd53e874cbd5
make release
```

The recipe's image builds this commit on Debian 12 and puts the binary at `/usr/local/bin/biosim4`. The program reads one config file, `./biosim4 biosim4.ini`, and writes its logs to the directories named in that file. The recipe's helper script writes the config from the form values, sets `deterministic = true` and `numThreads = 1`, and writes everything to the output folder.

## Run the tested example

This recipe builds biosim4 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 7.1 s.

1. Download [biosim4-recipe.tar.gz](https://biosimhub.pages.dev/guides/biosim4/biosim4-recipe.tar.gz) (Dockerfile, run_biosim4.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf biosim4-recipe.tar.gz
   cd biosim4
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/biosim4:45e808c .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/biosim4:45e808c sh /opt/run_biosim4.sh 64 500 150 100 6 0 0.001 24 5 true 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `biosim4.ini` | 811 B |
| `epoch-log.txt` | 2.0 KB |
| `run_log.txt` | 30.0 KB |

<details><summary>First lines of <code>biosim4.ini</code></summary>

```
numThreads = 1
sizeX = 64
sizeY = 64
population = 500
stepsPerGeneration = 150
maxGenerations = 100
genomeInitialLengthMin = 24
genomeInitialLengthMax = 24
genomeMaxLength = 300
maxNumberNeurons = 5
killEnable = false
sexualReproduction = true
```

</details>

<details><summary>First lines of <code>epoch-log.txt</code></summary>

```
0 144 0.984786 24 0
1 151 0.973599 24 0
2 164 0.968281 24 0
3 165 0.96375 24 0
4 188 0.933682 24 0
5 189 0.93588 24 0
6 208 0.926984 24 0
7 223 0.910365 24 0
8 234 0.916344 24 0
9 222 0.886365 24 0
10 230 0.865406 24 0
11 250 0.843651 24 0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Sensors:
  loc X
  loc Y
  boundary dist X
  boundary dist
  boundary dist Y
  genetic similarity fwd
  last move dir X
  last move dir Y
  long probe population fwd
  long probe barrier fwd
  population
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `size` | Grid side (cells) | 64 | 16 to 256 |
| `population` | Population size | 500 | 50 to 5000 |
| `steps` | Steps per generation | 150 | 20 to 500 |
| `generations` | Generations | 100 | 1 to 300 |
| `challenge` | Selection challenge (6 = weighted corner | 6 | 0, 1, 2, 3, 6, 9, 11 |
| `barrier` | Barrier type (0 = none | 0 | 0, 1, 3, 5 |
| `mutation` | Point mutation rate per gene | 0.001 | 0 to 0.1 |
| `genome_length` | Initial genes per genome | 24 | 4 to 100 |
| `neurons` | Maximum internal neurons | 5 | 0 to 20 |
| `sexual` | Sexual reproduction | true | true, false |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `epoch-log.txt` has one line per generation with five columns: generation, survivors, genetic diversity, average genome length and murder count. The example ran 100 generations, so it has 100 lines.
- `run_log.txt` is the program's console output (30,687 bytes in the example). It lists the sensors and actions, then prints the survivor count each generation and, every 10th generation, a few sample genomes with their connections.
- `biosim4.ini` is the exact config the run used, so a result can be repeated.

The example uses a 64 by 64 grid, 500 agents, 150 steps per generation, 100 generations, 24 genes per genome, up to 5 internal neurons and seed 42. In generation 0, 144 of the 500 agents were inside a corner zone, which is the result of random wandering. By generation 99, 351 were (70%). Genetic diversity, which is one minus the mean similarity of 1000 sampled genome pairs, fell from 0.985 to 0.368. The population converged on a smaller set of genomes.

The average genome length stays at 24 and the murder count at 0. Gene insertion and deletion are off (`geneInsertionDeletionRate = 0`) and the kill action is disabled (`killEnable = false`).

## Your own runs

Each run below changes one setting from the example. Everything else, including seed 42, is as in the example. Values are the last generation (99).

| Change | Survivors | Diversity |
|---|---|---|
| Example (challenge 6) | 351 | 0.368 |
| Challenge 1 (right half) | 494 | 0.644 |
| Mutation rate 0.01 | 362 | 0.460 |
| Asexual reproduction | 308 | 0.529 |
| Challenge 6 with 5 vertical bars | 274 | 0.242 |
| Seed 7 | 323 | 0.376 |

- **Right half.** 253 agents were in the right half in generation 0, close to the 250 expected by chance. By generation 99, 494 of 500 (99%) were. The task is simple, so most agents solve it and diversity stays higher at 0.644.
- **Higher mutation.** A ten times higher point mutation rate gave 362 survivors and diversity 0.460, against 351 and 0.368. The extra mutation kept diversity higher without a clear change in survivors.
- **No sex.** With `sexual = false`, survivors reached 308 and diversity 0.529. Each offspring then takes its genome from one parent instead of combining two, as the comment in `genome.cpp` says.
- **Barriers.** Barrier type 3 (five staggered vertical bars) started at 119 survivors in generation 0 and ended at 274. Diversity fell to 0.242, the lowest of the six runs.
- **Another seed.** Seed 7 gave 146 survivors in generation 0 and 323 in generation 99. Replicates differ by tens of survivors, so judge an effect over several seeds.

## Pitfalls

- **Video output is off.** The upstream video writer aborts with OpenCV 4.6 on Debian 12 ("image.depth() == CV_8U"), so the recipe sets `saveVideo = false`. Only the logs are produced.
- **A gnuplot message repeats in the log.** The program tries to run `/usr/bin/gnuplot` after each generation, and `run_log.txt` gets one `/usr/bin/gnuplot: not found` line per generation (100 in the example). The epoch log is still written. Plot it yourself from the five columns.
- **Exact repeats need a fixed seed.** The recipe sets `deterministic = true` and `numThreads = 1`. Two runs with seed 42 gave an identical epoch log. In `biosim4.ini`, `deterministic = false` seeds the generator randomly.
- **Grid must be square.** Challenge 6 asserts `sizeX == sizeY`. The recipe uses one side length.

## Further reading

- Project page and README: https://github.com/davidrmiller/biosim4
- Talk, "I programmed some creatures. They evolved.": https://www.youtube.com/watch?v=N3tRFayqVtk
- Selection rules for each challenge: `src/survival-criteria.cpp` in the repository
- Config reference: the comments in `biosim4.ini`
- Citation: Miller DR. biosim4: Biological evolution simulator (software, 2021). https://github.com/davidrmiller/biosim4. The project has no journal paper.

---

Cite: Miller DR. biosim4: Biological evolution simulator (software, 2021). https://github.com/davidrmiller/biosim4

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/biosim4).
