# SELAM

> Forward-time simulation of admixture between ancestral populations with optional selection, from a demography file and a sampling file.

Licence: GPL-3.0 · [Source code](https://github.com/russcd/SELAM)

## What it simulates

SELAM simulates admixture between two or more ancestral populations, forward in time. It follows local ancestry along each chromosome: for every sampled chromosome it reports which stretches came from which ancestor. It is based on the Wright-Fisher model with non-overlapping generations. Subpopulations can change size, exchange migrants with each other and receive continuing migrants from the ancestral populations. Optional selection files add single-locus, epistatic, population-specific and mate-choice selection.

Input is a demography file and a sampling file. Output is a tab-delimited file of ancestry tracts for the individuals you ask for.

Key assumptions: recombination follows a Poisson number of crossovers per chromosome with no interference, positions are in Morgans, and in the default two-sex mode the last chromosome is an X. Males carry one X copy with no recombination.

## When to use it

Use it to ask how long ancestry tracts are, and what ancestry fraction a population has, some number of generations after one or several admixture pulses. It suits questions about tract-length distributions, admixture timing and selection against ancestry from one parent population.

Alternatives on biosimhub:

- [msprime](msprime.md) fits better for neutral demographic histories, because it works backward in time. The SELAM manual says forward simulation needs much more computation than coalescent approaches.
- [SLiM](slim.md) fits better when you need selection or genome structure beyond SELAM's file formats, because you write the model as a SLiM (Eidos) script.

## Install it yourself

SELAM 0.9 is on bioconda, with builds listed for linux-64, linux-aarch64 and osx-64.

```
conda create -n selam -c conda-forge -c bioconda selam=0.9
```

This rests on the anaconda.org package index. The manual also describes compiling with `make`; that needs GSL and, optionally, tcmalloc.

The minimal command takes a demography file and an output (sampling) file:

```
SELAM -d demography.txt -o sampling.txt -g 30 --seed 42
```

## Run the tested example

This recipe builds SELAM in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.3 s.

1. Download [selam-recipe.tar.gz](https://biosimhub.pages.dev/guides/selam/selam-recipe.tar.gz) (Dockerfile, example demography.txt, sampling.txt, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf selam-recipe.tar.gz
   cd selam
   sh run.sh
   ```

![Terminal recording of the SELAM example run](https://biosimhub.pages.dev/media/selam/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/selam:0.9 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/selam:0.9 SELAM -d /work/in/demography.txt -o /work/in/sampling.txt \
    -g 30 --seed 42 -m 1 --abl 0.05 > out/selam_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `population1_output.txt` | 45.6 KB |
| `selam_log.txt` | 32 B |

<details><summary>First lines of <code>population1_output.txt</code></summary>

```
30	0	0	1	0	0	0	0	0.291224
30	0	0	1	0	0	1	0.291224	0.431449
30	0	0	1	0	0	0	0.431449	0.554773
30	0	0	1	0	0	1	0.554773	0.638902
30	0	0	1	0	0	0	0.638902	0.640981
30	0	0	1	0	0	1	0.640981	0.64893
30	0	0	1	0	0	0	0.64893	0.673743
30	0	0	1	0	0	1	0.673743	0.787055
30	0	0	1	0	0	0	0.787055	1
##	30	0	0	1	0	0
30	0	0	1	0	1	0	0	0.451585
30	0	0	1	0	1	1	0.451585	0.63773
```

</details>

<details><summary>First lines of <code>selam_log.txt</code></summary>

```
SELAM runtime: 0.100353 seconds
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-g` | Generations to run (at least the last sampling generation) | 30 | 1 to 5000 |
| `-m` | Male recombination map scalar | 1 | 0 to 5 |
| `--abl` | Ancestry block length (Morgans) | 0.05 | 0.001 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example calls SELAM directly, with no helper script.

The demography file has one row per source of individuals and one column per generation at which something changes. In the example, the row `0 0 A 1000 1000 1000` sets subpopulation 0 to 1000 individuals per sex. Rows `0 a0 A` and `0 a1 A` set the starting makeup to half ancestry a0 and half a1 (0.5 each in generation 0, zero migration in generation 1). From generation 10 each ancestral population contributes 2% of the individuals every generation.

The sampling file has one row: `30 0 100 0 population1_output.txt`. The columns are generation, subpopulation, number of females, number of males and the file name. SELAM samples 100 females from subpopulation 0 in generation 30 and stops there.

`population1_output.txt` (46,646 bytes) has one row per tract. The columns are generation, subpopulation, sex (0 is female), individual number, chromosome, parent of origin (0 is the mother), ancestry type, start and stop in Morgans. The first row, `30 0 0 1 0 0 0 0 0.291224`, is an ancestry 0 tract covering the first 0.29 Morgans of individual 1's maternal chromosome.

Counting the file gives:

- 1297 tracts on 200 chromosome copies (100 females, two copies each).
- Mean tract length 0.154 Morgans.
- Ancestry 1 covers 50.5% of the genome (101.0 of 200 Morgans). The start was 50% and migration was symmetric.

`selam_log.txt` holds one line, `SELAM runtime: 0.100353 seconds` in the recorded example. A second run took 1.2 seconds.

## Your own runs

- `--seed 7`: 1256 tracts, mean length 0.159, ancestry 1 at 45.9%. Seed 42 gave 1297, 0.154 and 50.5%.
- Sampling file with two rows, generation 10 and generation 30, both 100 females: generation 10 has 740 tracts with mean length 0.270 Morgans, generation 30 has 1267 tracts with mean 0.158. Tracts get shorter and more numerous as recombination breaks them up.
- `-m 0` (no recombination in male gametes), seed 42: 1269 tracts, mean 0.158, ancestry 1 at 49.6%. Only paternal gametes lose recombination, so the change is small.
- `--abl 0.01` and `--abl 0.5` with seed 42 gave a file byte-identical to `--abl 0.05`. With no selected sites, the ancestry block length changed nothing in the output.

## Pitfalls

- The seed defaults to the clock (`time(NULL)` in the source). Always pass `--seed` if you want a repeatable run.
- Each demography file needs a generation 0 column, at least two ancestral populations named `a0`, `a1`, and a size row where the destination and source subpopulation match.
- Sampling rows with the same file name append to that file, as the manual says. Delete the old file before re-running in the same directory.
- `-g` did not shorten the run. With `-g 20` and a sample at generation 30, the output matched the `-g 30` run exactly. Set `-g` to the last sampling generation anyway.
- `##` lines appear only when selected sites exist. This example has none.
- The output lists ancestry tracts, plus selected-site genotypes only when a selection file is given. Neutral SNP genotypes are not in the file.

## Further reading

- Source and README: https://github.com/russcd/SELAM
- SELAM manual (PDF): https://raw.githubusercontent.com/russcd/SELAM/master/SELAM_manual.pdf
- Corbett-Detig R, Jones M (2016). Bioinformatics 32:3035-3037. https://doi.org/10.1093/bioinformatics/btw365

---

Cite: Corbett-Detig R, Jones M (2016). SELAM, a forward-time genetic simulator for population admixture. Bioinformatics 32:3035-3037. doi:10.1093/bioinformatics/btw365

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/selam).
