# Avida

> Evolve a population of self-replicating digital organisms that earn CPU time by computing logic functions, and write per-100-update population, fitness and task statistics.

Licence: LGPL-3.0-or-later · [Source code](https://github.com/devosoft/avida)

## What it simulates

Avida is a digital evolution platform. Each organism is a short program written in a virtual assembly language, and it runs on its own virtual CPU. The ancestor does one thing: copy itself. Copying errors, insertions and deletions create variants. Programs that replicate faster leave more offspring, so the population evolves by natural selection in a computer.

The environment can reward logic functions. An organism that reads numbers from its input, computes a function such as NOT, NAND or OR, and writes the right answer to its output gets extra CPU time. Nobody writes these programs. Avida's best-known result is that complex functions such as EQU evolve through chains of simpler ones (Lenski et al. 2003, Nature 423:139-144).

The recipe seeds one default ancestor of 100 instructions into a toroidal world with one organism per cell, and records statistics every 100 updates. One update is on average 30 CPU cycles per organism.

## When to use it

Use Avida to study how mutation rate, population size and selection shape adaptation, with full replicates and perfect records of every genotype.

- Use [SLiM](slim.md) or [simuPOP](simupop.md) for forward simulations of real genomes with defined loci.
- Use [Nemo](nemo.md) for quantitative genetics and metapopulation questions.
- Use [AgentPy](agentpy.md) or [Agents.jl](agents-jl.md) for agent rules that you write yourself.

## Install it yourself

Avida has no conda or pip package. The recipe builds the Avida repository at commit 47f13dadb547fcf10f620ace60247f38b30b8b16 (the binary prints "Avida 2.14.0") with CMake and a C++ compiler:

```
git clone https://github.com/devosoft/avida.git
cd avida && git submodule update --init libs/apto
export AVIDA_DISABLE_BACKTRACE=1
mkdir cbuild && cd cbuild
cmake .. -DCMAKE_BUILD_TYPE=Release -DCMAKE_POLICY_VERSION_MINIMUM=3.5
make -j4 install
```

The build lands in `cbuild/work/` with the `avida` binary and the default configuration files. Three things were needed for a clean build with GCC 15:

- **x86-64 only.** On aarch64 the compile stopped at an inline assembly `lock xaddl` in the atomic counters, so the recipe runs as linux/amd64, under emulation on ARM machines.
- **Backtrace support off.** The optional backtrace library failed to link with the libbfd of the toolchain used, and Avida's own `build_avida` script falls back to the same setting.
- **CMake policy flag.** The old CMake files need `CMAKE_POLICY_VERSION_MINIMUM=3.5` with a current CMake.

The build took about 6 minutes.

## Run the tested example

This recipe builds Avida in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 13.4 s. Avida has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [avida-recipe.tar.gz](https://biosimhub.pages.dev/guides/avida/avida-recipe.tar.gz) (Dockerfile, run_avida.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf avida-recipe.tar.gz
   cd avida
   sh run.sh
   ```

![Terminal recording of the Avida example run](https://biosimhub.pages.dev/media/avida/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/avida:2.14.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/avida:2.14.0 sh /opt/run_avida.sh 30 3000 42 0.0075 0.05 0.05 all > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `average.csv` | 3.2 KB |
| `count.csv` | 2.1 KB |
| `dominant.csv` | 2.7 KB |
| `run_log.txt` | 242 B |
| `tasks.csv` | 886 B |
| `time.csv` | 850 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/avida/result-dark.png"><img src="https://biosimhub.pages.dev/media/avida/result.png" alt="Plot of the Avida example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>average.csv</code></summary>

```
Update,Merit,Gestation Time,Fitness,Repro Rate?,(deprecated) Size,Copied Size,Executed Size,(deprecated) Abundance,Proportion of organisms that gave birth in this update,Proportion of Breed True Organ
0,97,389,0,0,0,100,97,0,1,1,0,0,0,0,0
100,94.0725,391.333,0.240549,0,0,98.7681,94.0725,0,0.0289855,0,0,6.97101,-3.3089,0,0
200,95.601,401.391,0.241046,0,0,102.181,97.2202,0,0.0129534,0.00259067,0,14.7668,-3.22915,0,0
300,97.6924,411.817,0.241669,0,0,105.74,100.524,0,0.0283768,0.00908059,0,22.462,-3.15486,0,0
400,99.3593,412.154,0.244566,0,0,106.536,101.067,0,0.0622914,0.0189099,0,30.1735,-3.67765,0,0
500,99.0779,403.699,0.249537,0,0,106.492,100.694,0,0.0456062,0.0144605,0,38.0667,-3.58569,0,0.155704
600,98.9944,401.126,0.250696,0,0,106.7,99.8478,0,0.0511111,0.0266667,0,45.9622,-3.02382,0,0.153335
700,98.2056,384.658,0.258066,0,0,104.858,98.3133,0,0.0433333,0.0155556,0,54.5889,-2.85619,0,0.155659
800,99.2011,382.493,0.264576,0,0,106.224,99.4867,0,0.0455556,0.02,0,63.8489,-3.79844,0,0.158028
900,96.5933,370.03,0.267105,0,0,103.841,97.22,0,0.0611111,0.0188889,0,73.4444,-5.99445,0,0.159714
1000,99.0724,358.301,0.286987,0,0,102.843,96.5802,0,0.0489978,0.0155902,0,84.01,-7.4918,0,0.162637
```

</details>

<details><summary>First lines of <code>count.csv</code></summary>

```
update,number of insts executed this update,number of organisms,number of different genotypes,number of different threshold genotypes,(deprecated) number of different species,(deprecated) number of di
0,30,1,1,1,0,0,0,1,0,1,1,1,1,0,0
100,2010,69,46,3,0,0,0,2,0,0,28,39,69,0,0
200,11580,386,284,36,0,0,0,5,5,1,150,213,386,0,0
300,26340,881,700,102,0,0,0,25,22,8,308,495,881,0,0
400,27000,899,744,98,0,0,0,56,57,17,284,497,899,0,0
500,27000,899,710,109,0,0,0,41,42,13,324,505,899,0,0
600,27000,900,715,110,0,0,0,46,46,24,315,509,900,0,0
700,27000,900,705,103,0,0,0,39,39,14,342,504,900,0,0
800,27000,900,700,91,0,0,0,41,41,18,313,518,900,0,0
900,27000,900,718,112,0,0,0,55,55,17,328,498,900,0,0
1000,26910,898,695,101,0,0,0,44,43,14,354,494,898,0,0
```

</details>

<details><summary>First lines of <code>dominant.csv</code></summary>

```
Update,Average Merit of the Dominant Genotype,Average Gestation Time of the Dominant Genotype,Average Fitness of the Dominant Genotype,Repro Rate?,Size of Dominant Genotype,Copied Size of Dominant Gen
0,0,0,0,0,100,0,0,1,0,0,0,0,2.22507e-308,1,100-aaaaa
100,97,389,0.249357,0.00257069,100,100,0,13,0,0,0,0,0.249357,1,100-aaaaa
200,97,382,0.253927,0.0026178,100,100,0,8,0,0,4,0,0.253927,58,100-aaaan
300,97,382,0.253927,0.0026178,100,100,0,6,0,0,6,0,0.253927,860,100-aaacp
400,96,381,0.251969,0.00262467,99,99,0,5,1,0,7,0,0.251969,1878,099-aaabd
500,96,384,0.25,0.00260417,102,101.867,0,7,3,3,9,0,0.25,5870,102-aaaaz
600,97,380,0.255263,0.00263158,100,100,0,6,1,1,10,0,0.255263,7203,100-aaaig
700,96,378,0.253968,0.0026455,100,100,0,7,0,0,14,0,0.253968,10941,100-aaami
800,96,371,0.25876,0.00269542,99,99,0,8,2,1,12,0,0.25876,12743,099-aaahc
900,83,364,0.228022,0.00274725,99,99,0,5,0,0,15,0,0.228022,13334,099-aaahq
1000,78,259,0.301158,0.003861,100,100,0,8,0,0,17,0,0.301158,19995,100-aaatk
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
last update: UD: 3000    Gen: 558.0733   Fit: 33.67112   Orgs: 900     
tasks done by organisms at the last update (Not,Nand,And,OrNot,Or,AndNot,Nor,Xor,Equals): 736,852,0,769,751,0,0,0,0
done: 30 x 30 world, 3000 updates, seed 42, tasks all
```

</details>

<details><summary>First lines of <code>tasks.csv</code></summary>

```
Update,Not,Nand,And,OrNot,Or,AndNot,Nor,Xor,Equals
0,0,0,0,0,0,0,0,0,0
100,0,0,0,0,0,0,0,0,0
200,0,0,0,0,0,0,0,0,0
300,0,0,0,0,0,0,0,0,0
400,0,0,0,0,0,0,0,0,0
500,0,0,0,0,0,0,0,0,0
600,1,0,0,0,0,0,0,0,0
700,0,0,0,0,0,0,0,0,0
800,0,0,0,0,0,0,0,0,0
900,0,0,0,0,0,0,0,0,0
1000,24,0,0,0,0,0,0,0,0
```

</details>

<details><summary>First lines of <code>time.csv</code></summary>

```
update,avida time,average generation,num_executed?
0,0,0,30
100,1.03318,6.97101,2010
200,2.08828,14.7668,11580
300,3.12363,22.462,26340
400,4.13747,30.1735,27000
500,5.14345,38.0667,27000
600,6.15429,45.9622,27000
700,7.16346,54.5889,27000
800,8.17328,63.8489,27000
900,9.19779,73.4444,27000
1000,10.22,84.01,26910
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `world` | World side length (cells | 30 | 5 to 60 |
| `updates` | Updates to run | 3000 | 100 to 5000 |
| `copy_mut` | Copy mutation probability per instruction | 0.0075 | 0 to 0.05 |
| `ins` | Insertion probability per division | 0.05 | 0 to 1 |
| `del` | Deletion probability per division | 0.05 | 0 to 1 |
| `tasks` | Logic tasks that give a CPU-time reward | all | all, simple, none |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is a 30 x 30 world (900 cells), 3,000 updates, copy mutation probability 0.0075 per instruction, insertion and deletion probabilities of 0.05 per division, and all nine logic tasks rewarded. It ran in 13.4 s.

- `run_log.txt` shows the last update: generation 558.07, average fitness 33.67 and 900 organisms. It also lists how many organisms perform each task: NOT 736, NAND 852, ORNOT 769, OR 751, and none for AND, ANDNOT, NOR, XOR or EQU.
- `tasks.csv` has one row per 100 updates and one column per task. NOT first appears at update 600, NAND at 1,100, ORNOT at 1,300 and OR at 1,600. A task in this file is the number of organisms that performed it during that update.
- `average.csv` has the population averages: merit, gestation time, fitness, genome size and generation. Gestation time at the end is 282.2 cycles and the average copied size is 99.2 instructions.
- `count.csv` has the number of organisms and distinct genotypes. At update 3,000 there are 900 organisms and 697 genotypes.
- `dominant.csv` follows the most abundant genotype, and `time.csv` gives Avida time and the average generation at each update.

Fitness here is merit divided by gestation time. The ancestor starts at merit 97 and gestation 389, a fitness of about 0.25. Reward tasks raise merit, and fitter genotypes take over, so the average fitness grew to 33.67 and the generation count to 558. That is a 135-fold gain in fitness from a program that cannot compute anything at the start.

## Your own runs

Each run changes the listed settings from the example and uses seed 42 unless noted. All used a 30 x 30 world and 3,000 updates.

- **No rewards (`--tasks none`).** Fitness stayed at 0.34, with no task done at any point. Generation reached 323.5 instead of 558.1. Selection acted only on replication speed.
- **Three simple tasks (`--tasks simple`).** NOT appeared at update 600, NAND at 1,100 and AND at 3,000. At the end 764 organisms did NOT, 777 did NAND and 12 did AND. Fitness was 1.21.
- **Higher mutation (copy_mut 0.02).** Fitness was 0.39 and 842 genotypes were present, against 697 for the example. NOT reached 388 organisms and NAND only 89. Too many copy errors destroy what selection builds.
- **No copy mutation (copy_mut 0).** No task appeared, fitness stayed at 0.25 and only 279 genotypes existed. Insertions and deletions still made variants, but not enough for a task to evolve.
- **Another seed (`--seed 43`).** Seven tasks appeared, up to NOR at update 3,000. Fitness was 56.9 against 33.7 for seed 42. Evolution is a random process, so judge any effect over many seeds.

## Pitfalls

- **Slow under emulation.** A 60 x 60 world for 2,000 updates took 42 s. The recipe caps the world at 60 and the run at 5,000 updates.
- **Data columns come from the `.dat` header.** The helper turns Avida's headed text files into CSV. Fields with commas in their names get a semicolon.
- **Task counts are per update, not cumulative.** A task row counts the organisms that did the task during that update, so it can drop to 0 and return.
- **Single runs mislead.** Seed 42 evolved four tasks and seed 43 evolved seven at the same settings.
- **Rare tasks are fragile.** AND appeared in 12 organisms at update 3,000 in the simple environment and in 5 organisms under seed 43. Such a result needs more updates to confirm.

## Further reading

- Avida documentation: https://github.com/devosoft/avida/wiki
- Source: https://github.com/devosoft/avida
- Paper: Ofria C, Wilke CO (2004) Avida: A software platform for research in computational evolutionary biology. Artificial Life 10(2):191-229. https://doi.org/10.1162/106454604773563612
- Paper: Lenski RE, Ofria C, Pennock RT, Adami C (2003) The evolutionary origin of complex features. Nature 423:139-144. https://doi.org/10.1038/nature01568

---

Cite: Ofria C, Wilke CO (2004). Avida: A software platform for research in computational evolutionary biology. Artificial Life 10(2):191-229. doi:10.1162/106454604773563612

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/avida).
