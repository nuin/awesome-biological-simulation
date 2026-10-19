# Nemo

> Individual-based forward-time simulation of population genetics and life-history evolution in structured populations, driven by an ini-style configuration file.

Licence: GPL-3.0-or-later · [Source code](https://nemo2.sourceforge.io)

## What it simulates

Nemo is a forward-time, individual-based simulator for population genetics and life-history evolution. Its own description calls it genetically explicit: every individual carries its alleles, and patches of individuals can exchange migrants. You compose a simulation from a configuration file that lists a population, a life cycle (the ordered events each generation) and the traits to track.

The example is a quantitative-genetics run. One patch holds 200 hermaphrodites with Wright-Fisher mating. Two traits are controlled by 100 loci, and every locus affects both traits (full pleiotropy). Mutations add normally distributed effects to existing allele values, with rate 0.005 per locus and a mutation matrix of 0.10 variance and 0.02 covariance. Gaussian stabilizing selection pulls both traits toward an optimum of 0 with selection variance 10. A smaller selection variance makes a narrower fitness peak.

Input is one `.ini` file. Output is a table of statistics at the generations you choose.

## When to use it

Use it for questions about how genetic variance and trait covariance build up under mutation, selection and drift, how G-matrices evolve, or how dispersal among patches shapes differentiation. Nemo also covers neutral markers, deleterious mutations and incompatibilities.

Alternatives:

- [simuPOP](simupop.md) fits better when you want to script the model in Python and control each step.
- [SLiM](slim.md) fits better when you want to write the model yourself as a SLiM (Eidos) script and upload it.

## Install it yourself

The Nemo site gives `conda create -n nemo -c conda-forge -c ecoevo nemo`. The recipe uses the bioconda build pinned to 2.4.2, which the anaconda.org index lists for linux-64, linux-aarch64 and osx-arm64.

```
conda create -n nemo -c conda-forge -c bioconda nemo=2.4.2
```

A micromamba dry run did not finish (downloads from conda.anaconda.org timed out), so the version rests on the package index listing.

The executable name carries the version. Run a configuration with:

```
nemo2.4.2 my_simulation.ini
```

With no argument, Nemo looks for `Nemo2.ini` in the current directory. The site notes that 2.4.0 and 2.4.1 had a random-number bug affecting free recombination for some bitstring trait architectures, and recommends 2.4.2.

## Run the tested example

This recipe builds Nemo in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s.

1. Download [nemo-recipe.tar.gz](https://biosimhub.pages.dev/guides/nemo/nemo-recipe.tar.gz) (Dockerfile, run.sh, example config.ini, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf nemo-recipe.tar.gz
   cd nemo
   sh run.sh
   ```

![Terminal recording of the Nemo example run](https://biosimhub.pages.dev/media/nemo/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/nemo:2.4.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/nemo:2.4.2 run-nemo /work/in/config.ini > out/nemo_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `nemo.log` | 427 B |
| `nemo_log.txt` | 4.4 KB |
| `quanti.log` | 736 B |
| `quanti.txt` | 455 B |

<details><summary>First lines of <code>nemo.log</code></summary>

```
--- N E M O ---
    LOGFILE


| basename                                |      start time     |      stop time      | e-time CPU | repl done | rpl e-time | mean gen | version               | hostname             | output files 
| quanti                                  | 12-10-2026 06:07:11 | 12-10-2026 06:07:11 |   00:00:00 |         1 |   00:00:00 |      300 |  2.4.2 [03 Aug 2026] | 5d7fb355fa7a         | ".log": ".txt":
```

</details>

<details><summary>First lines of <code>nemo_log.txt</code></summary>

```

  N E M O 2.4.2 [03 Aug 2026]

  Copyright (C) 2006-2026 The Authors
  This is free software; see the source for copying
  conditions. There is NO warranty; not even for 
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
  https://nemo2.sourceforge.io; nemo-simul@googlegroups.com
-----------------------------------------------------------
reading parameters from "/work/in/config.ini"
setting random seed from input value: 13215

```

</details>

<details><summary>First lines of <code>quanti.log</code></summary>

```
# Nemo    v2.4.2  [03 Aug 2026]
#
# simulation started on 12-10-2026 06:07:11


filename quanti
generations 300
random_seed 13215
replicates 1
run_mode overwrite

patch_nbfem 200
```

</details>

<details><summary>First lines of <code>quanti.txt</code></summary>

```
replicate   	generation  	adlt.q1     	adlt.q2     	adlt.q1.Va  	adlt.q2.Va  	adlt.q12.cov
1           	1           	0.00959557  	-0.0282552  	0.0854271   	0.103036    	0.0166001   
1           	100         	-0.0718561  	0.253406    	4.30294     	5.1922      	0.981596    
1           	200         	-0.0439237  	-0.269244   	5.90944     	5.22319     	0.176737    
1           	300         	0.0371594   	0.00668908  	8.63008     	7.0021      	0.735529    
```

</details>


## Reading the output

The recipe's `run-nemo` is a short shell script. It refuses configuration files that set `preexec*`, `postexec*` or `root_dir` (those keys can run shell commands or move the output), then calls `nemo2.4.2` on the file.

The run wrote four files:

- `quanti.txt` (455 bytes) holds the statistics. Columns are replicate, generation, `adlt.q1` and `adlt.q2` (mean phenotype of each trait among adults), `adlt.q1.Va` and `adlt.q2.Va` (within-patch additive genetic variance) and `adlt.q12.cov` (genetic covariance between the traits).
- `quanti.log` echoes every parameter, with a start and finish time.
- `nemo.log` has one summary line per simulation: 300 generations, 1 replicate, Nemo 2.4.2.
- `nemo_log.txt` is the terminal output, mostly the progress counter.

`stat_log_time 100` gives rows at generations 1, 100, 200 and 300. Additive variance of trait 1 grows from 0.085 to 4.30, 5.91 and 8.63. For trait 2 it is 0.103, 5.19, 5.22 and 7.00. The mean phenotypes stay near 0 (between -0.07 and 0.04 for trait 1), which is where the optimum sits. The covariance is 0.017, 0.98, 0.18 and 0.74. Variance is still rising at generation 300, so 300 generations is too short to read an equilibrium.

The file sets `random_seed 13215`, so the run repeats exactly. A second run gave the same `quanti.txt` values.

## Your own runs

Each run changes one line of the example file.

- `selection_variance {{1}}` (narrower fitness peak): trait 1 variance at generation 300 is 5.08 instead of 8.63, and trait 2 is 4.39 instead of 7.00.
- `quanti_mutation_rate 0.0005` (ten times lower): trait 1 variance at generation 300 is 0.776 instead of 8.63, and trait 2 is 1.15 instead of 7.00.
- `replicates 5`: replicate 1 matches the single run. At generation 300 the trait 1 variance is 8.63, 7.08, 7.44, 8.33 and 8.21. The file has 20 data rows.
- `patch_nbfem 1000` (five times more individuals): trait 1 variance at generation 300 is 9.97 and trait 2 is 10.05.

## Pitfalls

- Matrix values need double braces, as in `selection_variance {{10}}`. The manual says a single decimal applies to all traits and patches, and a matrix gives per-patch and per-trait values.
- The example needs `mating_system 6` with `patch_nbmal 0`. The manual's example for hermaphrodites uses the same pair.
- Rows appear only at `stat_log_time` multiples. For a curve of Va over time, lower it to 10 or 1.
- One replicate is one draw. In the five-replicate run the trait 1 variance at generation 300 ranged from 7.08 to 8.63.
- The recipe rejects `root_dir`. In a native run, `root_dir` sets the directory the results go to.

## Further reading

- Nemo home page: https://nemo2.sourceforge.io
- Nemo 2.4.2 manual (PDF): https://sourceforge.net/projects/nemo2/files/Nemo/2.4.2/Nemo2-manual.pdf/download
- Guillaume F, Rougemont J (2006). Bioinformatics 22:2556-2557. https://doi.org/10.1093/bioinformatics/btl415

---

Cite: Guillaume F, Rougemont J (2006). Nemo - an evolutionary and population genetics programming framework. Bioinformatics 22:2556-2557. doi:10.1093/bioinformatics/btl415

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/nemo).
