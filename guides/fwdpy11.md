# fwdpy11

> Forward-time neutral Wright-Fisher simulation with recombination and an optional population size change; returns a sampled VCF, the site frequency spectrum and diversity statistics.

Licence: GPL-3.0-or-later · [Source code](https://github.com/molpopgen/fwdpy11)

## What it simulates

fwdpy11 simulates a diploid population forward in time, one generation after another, with recombination. It records the ancestry of every individual as a tree sequence. Each simulated individual is real, so the model can carry selection, quantitative traits and multiple demes. The example here uses none of that. It runs the neutral model and changes the population size once.

The example sets an initial size, a final size and the number of generations over which the size changes. It runs a burn-in of 10 times the initial size, then the change. Then msprime "recapitates" the result, which means it simulates the ancestry of the first generation back to a common ancestor, and adds neutral mutations. Finally it samples diploid individuals and reports a VCF, the site frequency spectrum and diversity statistics.

The key assumptions: Wright-Fisher reproduction with random mating, a single deme, a mutation rate and recombination rate that are uniform along the sequence, and no selection.

## When to use it

Use fwdpy11 when you need forward simulation in Python with tree-sequence recording: selection on mutations, traits under stabilizing selection, or demes with structure. Tree-sequence recording keeps the ancestry of the living population and simplifies it periodically (every 50 generations in the recipe's helper script).

- Use [msprime](msprime.md) for neutral questions. It simulates backwards in time and follows only the sampled lineages.
- Use [SLiM](slim.md) when you prefer a scripting language (Eidos) with a GUI for forward models and no Python.

## Install it yourself

The conda command below resolves for fwdpy11 0.24.5. The recipe's image also pins msprime 1.3.4, tskit below 0.6.5 and Python 3.12. A dry run of that full set resolved:

```
micromamba create -n fwd -c conda-forge -c bioconda \
  fwdpy11=0.24.5 msprime=1.3.4 "tskit<0.6.5" python=3.12
```

The fwdpy11 manual says channel order matters for bioconda. It also describes a pip route that needs the GNU Scientific Library and cmake on your system.

A minimal forward run, with no mutations added:

```python
import fwdpy11

pop = fwdpy11.DiploidPopulation(100, 10000.0)   # 100 diploids, 10 kb
rng = fwdpy11.GSLrng(1)
demog = fwdpy11.ForwardDemesGraph.tubes([100], burnin=10)
params = fwdpy11.ModelParams(
    nregions=[], sregions=[],
    recregions=[fwdpy11.PoissonInterval(0.0, 10000.0, 1e-4)],
    rates=(0.0, 0.0, None), gvalue=fwdpy11.Multiplicative(2.0),
    demography=demog, simlen=1000)
fwdpy11.evolvets(rng, pop, params, simplification_interval=100)
ts = pop.dump_tables_to_tskit()
```

After 1000 generations this run had 200 sample nodes and 3 trees. Recombination rates in fwdpy11 are per genomic segment per generation, so 1e-4 here is for the whole 10 kb.

## Run the tested example

This recipe builds fwdpy11 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.4 s.

1. Download [fwdpy11-recipe.tar.gz](https://biosimhub.pages.dev/guides/fwdpy11/fwdpy11-recipe.tar.gz) (Dockerfile, run_fwdpy11.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf fwdpy11-recipe.tar.gz
   cd fwdpy11
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/fwdpy11:0.24.5 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/fwdpy11:0.24.5 python /opt/run_fwdpy11.py --popsize 200 --final-popsize 200 \
    --change-gens 100 --burnin 10 --length 100000 \
    --mu 1e-06 --rec 1e-07 --samples 20 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 213 B |
| `sfs.csv` | 256 B |
| `sim.vcf` | 71.4 KB |
| `summary.txt` | 212 B |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
initial_population_size	200
final_population_size	200
change_generations	100
sequence_length	100000
sampled_haplotypes	40
segregating_sites	430
nucleotide_diversity_per_bp	0.000906449
tajimas_d	-0.386798
seed	42

```

</details>

<details><summary>First lines of <code>sfs.csv</code></summary>

```
derived_count,sites
1,115
2,97
3,21
4,14
5,7
6,1
7,5
8,5
9,4
10,3
11,0
```

</details>

<details><summary>First lines of <code>sim.vcf</code></summary>

```
##fileformat=VCFv4.2
##source=tskit 0.6.4
##FILTER=<ID=PASS,Description="All filters passed">
##contig=<ID=chr1,length=100001>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	tsk_0	tsk_1	tsk_2	tsk_3	tsk_4	tsk_5	tsk_6	tsk_7	tsk_8	tsk_9	tsk_10	tsk_11	tsk_12	tsk_13	tsk_14	tsk_15	tsk_16	tsk_17	tsk_18	tsk_19
chr1	71	0	G	A	.	PASS	.	GT	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1
chr1	328	1	T	G	.	PASS	.	GT	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1
chr1	337	2	T	C	.	PASS	.	GT	1|1	0|0	0|0	1|1	0|1	0|1	0|0	0|0	0|1	0|1	1|0	0|0	0|0	0|0	1|0	0|1	0|0	0|1	0|0	0|0
chr1	351	3	A	G	.	PASS	.	GT	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1
chr1	724	4	C	A	.	PASS	.	GT	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1	1|1
chr1	754	5	T	A	.	PASS	.	GT	1|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|1	0|0	0|0	0|0	0|0	0|0	0|0	0|1	0|0	0|0	0|0	0|0
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
initial_population_size	200
final_population_size	200
change_generations	100
sequence_length	100000
sampled_haplotypes	40
segregating_sites	430
nucleotide_diversity_per_bp	0.000906449
tajimas_d	-0.386798
seed	42
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--popsize` | Initial population size (diploids) | 200 | 20 to 2000 |
| `--final-popsize` | Final population size (diploids) | 200 | 20 to 5000 |
| `--change-gens` | Generations of size change | 100 | 1 to 5000 |
| `--burnin` | Burn-in (multiples of the initial size) | 10 | 1 to 20 |
| `--length` | Sequence length (bp) | 100000 | 1000 to 5000000 |
| `--mu` | Mutation rate per bp per generation | 1e-06 | 1e-10 to 0.0001 |
| `--rec` | Recombination rate per bp per generation | 1e-07 | 0 to 0.0001 |
| `--samples` | Sampled diploid individuals | 20 | 2 to 200 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper script `run_fwdpy11.py` makes a `DiploidPopulation`, describes the size history with a `demes` graph, and calls `evolvets`. It then calls msprime `sim_ancestry` on the result and `sim_mutations`, picks random diploids, simplifies the tree sequence to them and writes the files. Its per-base rates are multiplied by the sequence length for the forward step. The forward run lasts 10 x 200 + 100 = 2100 generations.

- `run_log.txt` and `summary.txt` hold the same nine lines: sizes 200 and 200, 100 change generations, 100,000 bp, 40 sampled haplotypes, 430 segregating sites, pi 0.000906 per bp, Tajima's D -0.384 and seed 42.
- `sfs.csv` has columns `derived_count,sites`. It starts at 115 sites seen in one haplotype out of 40, 97 in two and 21 in three. The spectrum has many singletons, as expected for a neutral sample.
- `sim.vcf` is written for contig `chr1` of length 100,001, with 20 diploid columns (tsk_0 to tsk_19).

Check pi against theory. With 200 diploids and a mutation rate of 1e-6, 4 N mu = 0.0008 per bp. The observed 0.000906 is close. The example keeps N at 200 all the way through.

## Your own runs

Each run changes values from the example (200 diploids, burn-in 10, seed 42).

- **Growth.** `--final-popsize 2000` gave 578 segregating sites, pi 0.000983 and Tajima's D -1.04. Singletons rose from 115 to 200. A recent expansion adds rare variants, which pushes D negative.
- **Decline.** `--popsize 2000 --final-popsize 200` gave 2055 sites, pi 0.00621 and D +1.08. Diversity is still near the old large size (4 x 2000 x 1e-6 = 0.008) and rare variants are depleted. This run took about two minutes, because the burn-in is 20,000 generations of 2000 individuals.
- **Short burn-in.** `--burnin 1` gave 420 sites, pi 0.00131 and D +1.22. With only 200 forward generations, most of the genealogy comes from msprime's recapitation, so one replicate can land far from the equilibrium 0.0008. Run several seeds before reading anything into it.
- **Larger population.** `--popsize 1000 --final-popsize 1000` gave 1758 sites and pi 0.00363, against 4 N mu = 0.004.

## Pitfalls

- **Run time grows with N and burn-in.** The forward run costs generations x individuals. Start with N below 2000 and check the burn-in.
- **Burn-in is a multiple of the initial size.** `--burnin 10` with N = 200 is 2000 generations.
- **Rates are per bp in the recipe's helper script and per segment in the library.** In your own script, multiply a per-bp rate by the length.
- **Recapitation.** The fwdpy11 manual says to pass `preserve_first_generation=True` to `evolvets` before coalescing the first generation with msprime. The recipe's helper script does this. A script of your own must too.
- **Versions are pinned.** The recipe pins tskit below 0.6.5 and msprime 1.3.4. Keep those pins unless you test a newer set.

## Further reading

- Manual: https://molpopgen.github.io/fwdpy11/intro.html
- Finishing a simulation with msprime: https://molpopgen.github.io/fwdpy11/short_vignettes/recapitation.html
- Installation: https://molpopgen.github.io/fwdpy11/pages/installation.html
- Source: https://github.com/molpopgen/fwdpy11
- Papers (listed in the manual's citation page): Thornton KR (2014) A C++ template library for efficient forward-time population genetic simulation of large populations. Genetics 198:157-166. Thornton KR (2019) Polygenic adaptation to an environmental shift. Genetics 213:1513-1530. https://molpopgen.github.io/fwdpy11/misc/bibliography.html

---

Cite: Thornton KR. fwdpy11, forward-time population genetic simulation in Python, https://github.com/molpopgen/fwdpy11

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/fwdpy11).
