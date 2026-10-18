# msprime

> Simulate a coalescent genealogy with recombination and mutation, and write a VCF, a tree sequence and summary statistics.

Licence: GPL-3.0-or-later · [Source code](https://github.com/tskit-dev/msprime)

**[Run msprime in your browser](https://biosimhub.pages.dev/run/msprime/index.html)**: Coalescent simulation with recombination, mutation and simple demography; reports diversity, Tajima's D, the site frequency spectrum and the first marginal tree. Nothing to install; the first visit downloads about 17 MB.

[![The msprime plugin after its default run](https://biosimhub.pages.dev/media/msprime/plugin-light.png)](https://biosimhub.pages.dev/run/msprime/index.html)

## What it simulates

msprime simulates the ancestry of a sample of genomes backwards in time under the coalescent with recombination. It then drops mutations on the resulting genealogy. The output is a tree sequence: one genealogical tree per stretch of genome between recombination breakpoints.

You give it a sample size, a sequence length, a population size (Ne), a recombination rate and a mutation rate. You get back the genealogies, the variant sites, and any statistic you compute from them, such as nucleotide diversity (pi) or Tajima's D.

The key assumptions are a randomly mating population of constant size unless you add a demography, neutral mutations, and no selection. Time runs in generations. In the default Hudson model, a sample of 20 diploid individuals has 40 sampled genomes.

## When to use it

Use msprime to generate neutral null data: expected diversity under a demographic model, the spread of Tajima's D, or test data for a pipeline that reads VCF.

- Use [stdpopsim](stdpopsim.md) when you want a published human, fly or Arabidopsis demographic model with realistic rates and no hand-written demography.
- Use [scrm](scrm.md) when you need ms-style output for software that reads it.
- Use [SLiM](slim.md) or [fwdpy11](fwdpy11.md) when selection matters, since msprime has no general selection model.

## Run it in your browser

The msprime plugin runs msprime in Python inside your browser, through Pyodide. The first load downloads about 17.7 MB (the Python runtime, msprime, tskit and demes) from the jsDelivr CDN. The status line shows "Ready" with the msprime, tskit and Pyodide versions when it finishes.

Set these controls, then press Run:

- **Sample size**: diploid individuals, 1 to 500. The page simulates two genomes per individual.
- **Sequence length**: 1 to 100,000,000 bp. Default 1,000,000.
- **Population size Ne**: default 10,000.
- **Recombination rate** and **Mutation rate**: per bp per generation, default 1e-8 each.
- **Seed**: a whole number from 1 to 4,294,967,295. The same seed and settings give the same result.
- **Demography**: constant size, bottleneck or exponential expansion. The bottleneck and expansion options add three fields: event start (generations ago, default 2000), bottleneck duration (default 500 generations) and a size factor (default 0.1 of Ne).

The page reports three things:

1. A statistics table with the simulated value next to the constant-size expectation: haploid samples, marginal trees, sites, segregating sites S, pi, Watterson's theta and Tajima's D. The expectations use theta = 4 Ne mu. Under a bottleneck or expansion the expectation column no longer applies, and the gap between the columns is the signal.
2. The unfolded site frequency spectrum as bars, with the neutral expectation (theta / i) as a line.
3. The first marginal tree, drawn as text, with the base-pair interval it covers. Branch lengths in the drawing are approximate. If the tree has more than one root, the page says it has not fully coalesced.

Limits of the browser build: no ploidy, growth-rate or ancestry-model choice, only the three demographies above, and no VCF or tree-sequence download. For those, install msprime yourself as below.

## Install it yourself

The conda command below resolves for msprime 1.4.4 on conda-forge:

```
micromamba create -n msp -c conda-forge msprime=1.4.4
```

The msprime documentation lists `pip install msprime` as the other route. A minimal run with the Python API, without the recipe's helper script:

```python
import msprime

ts = msprime.sim_ancestry(
    samples=10, population_size=10_000,
    recombination_rate=1e-8, sequence_length=100_000, random_seed=1)
ts = msprime.sim_mutations(ts, rate=1e-8, random_seed=1)
print(ts.num_samples, ts.num_trees, ts.num_sites, ts.diversity(), ts.Tajimas_D())
```

In the 1.4.4 image this printed 20 samples, 117 trees, 149 sites, pi 0.000397 and Tajima's D -0.254.

## Run the tested example

This recipe builds msprime in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.8 s.

![Terminal recording of the msprime example](https://biosimhub.pages.dev/media/msprime/run.gif)

1. Download [msprime-recipe.tar.gz](https://biosimhub.pages.dev/guides/msprime/msprime-recipe.tar.gz) (Dockerfile, run_msprime.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf msprime-recipe.tar.gz
   cd msprime
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/msprime:1.4.4 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/msprime:1.4.4 python /opt/run_msprime.py --samples 20 --ploidy 2 \
    --ne 10000 --length 1000000 --recomb 1e-08 \
    --mu 1e-08 --growth 0 --model hudson --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 44 B |
| `sim.trees` | 280.1 KB |
| `sim.vcf` | 172.2 KB |
| `summary.csv` | 155 B |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 40 haplotypes, 1435 trees, 1611 sites
```

</details>

<details><summary>First lines of <code>sim.vcf</code></summary>

```
##fileformat=VCFv4.2
##source=tskit 1.0.3
##FILTER=<ID=PASS,Description="All filters passed">
##contig=<ID=1,length=1000001>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	tsk_0	tsk_1	tsk_2	tsk_3	tsk_4	tsk_5	tsk_6	tsk_7	tsk_8	tsk_9	tsk_10	tsk_11	tsk_12	tsk_13	tsk_14	tsk_15	tsk_16	tsk_17	tsk_18	tsk_19
1	19	0	G	T	.	PASS	.	GT	0|0	0|0	0|0	0|0	1|1	0|0	0|0	0|1	0|0	0|0	0|0	0|0	0|0	0|0	0|0	1|0	0|0	0|0	0|0	1|0
1	215	1	A	T	.	PASS	.	GT	0|0	1|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0
1	246	2	A	C	.	PASS	.	GT	1|1	0|1	0|1	0|1	1|1	0|0	1|1	1|1	1|1	1|0	0|1	0|1	1|1	1|0	1|0	1|0	1|1	0|0	1|1	1|0
1	1695	3	T	C	.	PASS	.	GT	1|0	0|0	0|0	0|1	0|0	0|0	1|0	0|0	0|0	1|0	0|0	0|0	0|1	0|0	0|0	0|0	0|1	0|0	0|0	0|0
1	1781	4	C	A	.	PASS	.	GT	0|0	1|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0
1	2213	5	C	T	.	PASS	.	GT	0|0	0|0	1|0	1|0	0|0	1|1	0|0	0|0	0|0	0|1	1|0	1|0	0|0	0|1	0|1	0|1	0|0	1|1	0|0	0|1
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
haplotypes,sequence_length,trees,mutations,segregating_sites,pi_per_site,tajimas_d
40,1000000,1435,1615,1613,0.00038484615384615445,0.055877114232897165
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--samples` | Number of diploid-style individuals | 20 | 1 to 500 |
| `--ploidy` | Ploidy | 2 | 1 to 4 |
| `--ne` | Effective population size | 10000 | 10 to 100000 |
| `--length` | Sequence length (bp) | 1000000 | 1000 to 20000000 |
| `--recomb` | Recombination rate per bp per generation | 1e-08 | 0 to 0.0001 |
| `--mu` | Mutation rate per bp per generation | 1e-08 | 0 to 0.0001 |
| `--growth` | Population growth rate per generation (0 = constant size) | 0 | 0 to 0.05 |
| `--model` | Ancestry model | hudson | hudson, smc_prime, dtwf |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_msprime.py` wraps three msprime calls: `Demography.isolated_model` for the single population, `sim_ancestry` for the genealogy and `sim_mutations` for the variants. It then writes four files.

- `run_log.txt` has one line: "done: 40 haplotypes, 1435 trees, 1611 sites". The 20 individuals give 40 haplotypes. The genome has 1435 distinct trees. Mutations fell on 1611 sites.
- `sim.vcf` has 20 sample columns (tsk_0 to tsk_19) with phased genotypes such as `0|1`, one row per site. The first site is at position 19. The helper adds 1 to every position, because VCF is 1-based and tskit allows a site at position 0.
- `sim.trees` is the tree sequence (286,796 bytes). Load it with `tskit.load("sim.trees")` to compute anything the summary does not.
- `summary.csv` has one data row: 40 haplotypes, length 1,000,000, 1435 trees, 1615 mutations, 1613 segregating sites, pi 0.000385 per bp and Tajima's D 0.056.

Check pi against theory. With Ne 10,000 and mu 1e-8, theta = 4 Ne mu = 0.0004 per bp. The observed pi is 0.000385, and Tajima's D near 0 agrees with a constant-size neutral population.

The `segregating_sites` column (1613) is 2 more than the 1611 sites. tskit counts a site with three alleles twice, once for each allele beyond the first, so 2 sites here carry a third allele.

## Your own runs

Each run below changes one value from the example (seed 42, 20 individuals, 1 Mb). Each run used the recipe's prebuilt image.

- **Larger population.** `--ne 50000` gave 6978 trees, 8405 sites and pi 0.00196. Five times the Ne gave about five times the diversity (0.000385 to 0.00196) and about five times the sites.
- **No recombination.** `--recomb 0` gave 1 tree, 995 sites, pi 0.000182 and Tajima's D -0.83. One tree means one genealogy for the whole sequence.
- **Growth.** `--growth 0.01` gave 103 trees, 106 sites, pi 0.0000103 and Tajima's D -2.15. A positive rate means the population grew toward the present, so the ancestors were small and coalesce quickly.
- **Another seed.** `--seed 43` gave 1488 trees, 1661 sites and Tajima's D -0.16. Replicates differ, so report a distribution over many seeds.
- **Other ancestry models.** `--model smc_prime` gave 1497 trees, 1637 sites and pi 0.000354. With Ne 1000, `--model dtwf` gave 129 trees and 181 sites, and `hudson` gave 148 trees and 165 sites.

## Pitfalls

- **Negative growth rates can hang.** A negative rate makes the population larger the further back in time you go, so lineages may never meet. A run with `--growth -0.001` had not finished after 30 minutes. The recipe therefore accepts only rates of 0 and above.
- **Samples are individuals.** `--samples 20` with ploidy 2 gives 40 genomes. Set `--ploidy 1` for haploid data.
- **Rates are per bp per generation.** Human-scale values are near 1e-8.
- **DTWF needs an explicit population size and is slower.** The msprime documentation says DTWF is generation-by-generation and more costly than the coalescent at large Ne. Use it for small populations or the recent past.

## Further reading

- msprime quickstart: https://tskit.dev/msprime/docs/stable/quickstart.html
- Ancestry models (Hudson, SMC, DTWF): https://tskit.dev/msprime/docs/stable/ancestry.html
- Installation: https://tskit.dev/msprime/docs/stable/installation.html
- Source: https://github.com/tskit-dev/msprime
- Paper: Baumdicker F et al. (2022) Efficient ancestry and mutation simulation with msprime 1.0. Genetics 220:iyab229. https://doi.org/10.1093/genetics/iyab229

---

Cite: Baumdicker F, et al. (2022). Efficient ancestry and mutation simulation with msprime 1.0. Genetics 220:iyab229. doi:10.1093/genetics/iyab229

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/msprime).
