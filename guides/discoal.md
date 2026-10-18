# discoal

> Simulate coalescent samples with recombination and selective sweeps (hard, soft or neutral), writing ms-format haplotypes.

Licence: GPL-3.0 · [Source code](https://github.com/kr-colab/discoal)

## What it simulates

discoal simulates the ancestry of a sample of chromosomes backwards in time under the coalescent, with recombination, gene conversion, population size changes, population splits and admixture. Its main feature is selection: it can condition the genealogy on a selective sweep, so the sample carries the pattern a sweep leaves in nearby neutral variation.

You give it a sample size, a number of replicates, a number of sites and a population mutation rate. It prints each replicate in Hudson's ms format: a count of segregating sites, their positions between 0 and 1, and one 0/1 string per sampled chromosome, where 1 is the derived allele.

Sweeps come in three trajectory types. `-wd` is a deterministic trajectory, `-ws` a stochastic one and `-wn` a neutral fixation used as a control. The documentation also covers soft sweeps from standing variation (`-f`) or recurrent mutation (`-uA`), partial sweeps (`-c`), sweeps outside the simulated window (`-ls`, `-ld`, `-ln`) and recurrent hitchhiking (`-R`, `-L`).

Time is in units of 4N0 generations, as in ms. Theta (4 N0 mu) and rho (4 N0 r) are rates for the whole locus, not per base pair.

## When to use it

Use discoal to generate training or null data for sweep detection: the same locus with and without a sweep, with the selection strength, sweep age and sweep position varied. It also covers neutral demography when ms-style output is enough.

- [msprime](msprime.md) is the better choice for neutral data when you want tree sequences, VCF output and published demographic models.
- [scrm](scrm.md) writes ms-format output for neutral models with recombination.
- [SLiM](slim.md) simulates selection forward in time with arbitrary fitness effects, at much higher cost. Use it when a sweep trajectory model is too restrictive.

## Install

discoal has no conda or pip package. Neither conda-forge nor bioconda lists it (checked on anaconda.org). You build it from source with a C compiler and make. The current release is v0.1.7 (21 June 2025).

```bash
git clone --depth 1 --branch v0.1.7 https://github.com/kr-colab/discoal.git
cd discoal
make discoal
./discoal 10 1 1000 -t 10
```

The last line is the check suggested in the installation page of the discoal documentation. It should print an ms-format block with segregating sites and haplotypes. The Makefile compiles with `-march=native`, which ties the binary to the CPU that built it. The recipe below overrides this with `make discoal CFLAGS="-O3 -I."`.

## Run the tested example

This recipe builds discoal in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.3 s.

1. Download [discoal-recipe.tar.gz](https://biosimhub.pages.dev/guides/discoal/discoal-recipe.tar.gz) (Dockerfile, run_discoal.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf discoal-recipe.tar.gz
   cd discoal
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/discoal:0.1.7 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/discoal:0.1.7 sh /opt/run_discoal.sh 20 10 10000 20 20 stochastic 0.05 1000 0.5 1 2 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `discoal.ms` | 5.2 KB |
| `run_log.txt` | 38 B |
| `summary.csv` | 69 B |

<details><summary>First lines of <code>discoal.ms</code></summary>

```
discoal 20 10 10000 -t 20 -r 20 -d 1 2 -ws 0.05 -a 1000 -x 0.5 
1 2

//
segsites: 13
positions: 0.087086 0.131767 0.301161 0.311484 0.358156 0.469617 0.646738 0.675577 0.735765 0.803726 0.904648 0.943505 0.946019 
0000010000000
0000010000001
0001010000001
0000000000000
0000000000000
0000011000100
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 10 replicates, 11 summary lines
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
replicate,segsites
1,13
2,14
3,13
4,8
5,23
6,11
7,19
8,23
9,17
10,24
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `samples` | Sampled chromosomes | 20 | 2 to 500 |
| `replicates` | Independent replicates | 10 | 1 to 1000 |
| `sites` | Number of sites | 10000 | 100 to 1000000 |
| `theta` | Population mutation rate theta (4 N0 mu | 20 | 0.1 to 1000 |
| `rho` | Population recombination rate rho (4 N0 r | 20 | 0 to 1000 |
| `sweep` | Sweep type | stochastic | none, stochastic, deterministic, neutral |
| `tau` | Time since the sweep ended (units of 4N generations) | 0.05 | 0 to 2 |
| `alpha` | Selection strength alpha (2Ns) | 1000 | 1 to 100000 |
| `site` | Position of the selected site (0 to 1) | 0.5 | 0 to 1 |
| `seed1` | Seed 1 | 1 | 1 to 2147483647 |
| `seed2` | Seed 2 | 2 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Selection page of the discoal documentation, https://discoal.readthedocs.io/en/latest/selection.html. A stochastic sweep that fixed 0.05 time units ago, in 20 chromosomes, 10 replicates, 10,000 sites:

```bash
./discoal 20 10 10000 -t 20 -r 20 -ws 0.05 -a 1000 -x 0.5
```

Here `-t 20` is theta, `-r 20` is rho, `-a 1000` is the selection strength alpha (2Ns) and `-x 0.5` puts the selected site in the middle of the window. The recipe's script `run_discoal.sh` builds this command from its parameters, adds `-d seed1 seed2` and also writes a summary file.

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below. The command above comes from the discoal documentation, not from a recorded run.

## Reading the output

The output follows ms. The Basic Usage page of the documentation shows this small example for `./discoal 3 2 100 -t 2`:

```
//
segsites: 4
positions: 0.01835 0.09557 0.46556 0.72880
1000
0110
0111
```

- The first line, `//`, starts a replicate.
- `segsites:` is the number of variable sites in that replicate.
- `positions:` lists them as fractions of the sequence, from 0 to 1.
- Each remaining line is one sampled chromosome. A column is a site, and 1 marks the derived allele.

The header before the first replicate repeats the command line and the two random number seeds, so a run can be reproduced. In the recipe, `discoal.ms` holds the full output and `summary.csv` has one row per replicate with its number of segregating sites. A sweep usually lowers diversity near the selected site, so compare replicates from `-ws` runs with a run that has no sweep option.

Any tool that reads ms files can take `discoal.ms`. Convert it to VCF or compute statistics with your own scripts.

## Pitfalls

- **Rates are for the whole locus.** Theta and rho scale with the number of sites you simulate. Do not enter per-base rates.
- **Time units are 4N0 generations.** A tau of 0.05 is 0.05 x 4N0 generations ago.
- **Sweeps need `-a` and `-x`.** The documentation examples always give the selection strength and the position with `-ws`, `-wd` or `-wn`.
- **Seeds come from `/dev/urandom` by default.** Each run differs unless you pass `-d seed1 seed2`.
- **Sample size limit.** The current release allows up to 65,535 chromosomes. The default maximum is 100 million sites, set by `MAXSITES` in `discoal.h`.
- **Build flags.** A binary built with `-march=native` may not run on a machine with a different CPU.

## Further reading

- Documentation: https://discoal.readthedocs.io
- Basic usage: https://discoal.readthedocs.io/en/latest/basic_usage.html
- Installation: https://discoal.readthedocs.io/en/latest/installation.html
- Source: https://github.com/kr-colab/discoal
- Paper: Kern AD, Schrider DR (2016). discoal: flexible coalescent simulations with selection. Bioinformatics 32:3839-3841. https://doi.org/10.1093/bioinformatics/btw556

---

Cite: Kern AD, Schrider DR (2016). discoal: flexible coalescent simulations with selection. Bioinformatics 32:3839-3841. doi:10.1093/bioinformatics/btw556

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/discoal).
