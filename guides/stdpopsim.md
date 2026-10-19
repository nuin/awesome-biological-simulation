# stdpopsim

> Simulate genomes under curated published demographic models (human, fly, Arabidopsis) with msprime, returning tree sequences, a VCF and summary statistics.

Licence: GPL-3.0 · [Source code](https://github.com/popsim-consortium/stdpopsim)

## What it simulates

stdpopsim runs a published demographic model for a real species and returns a tree sequence. It is a catalog layer on top of a simulation engine ([msprime](msprime.md) by default, [SLiM](slim.md) optionally). The catalog supplies the species' recombination and mutation rates, genetic maps and the demographic history. You choose the species, the model, the genome region and how many individuals to sample from each population.

The example here uses the Gutenkunst et al. (2009) three-population out-of-Africa model for humans (id `OutOfAfrica_3G09`, populations YRI, CEU and CHB). The helper simulates neutral variation along a generic contig with a uniform recombination rate. The assumptions are those of the chosen model: fitted population sizes, split times and migration rates, neutral mutations and no selection.

## When to use it

Use stdpopsim when you want realistic neutral data for a known species without writing a demography yourself. Typical questions: how much diversity and Fst should a 3-population human model give, and what does a summary statistic look like under a published history.

- Use msprime when your demography is your own, or you need full control of ploidy, growth and ancestry model. stdpopsim calls msprime underneath.
- Use SLiM when you need selection that stdpopsim's built-in distributions cannot express. stdpopsim can also drive SLiM, with `-e slim`.

## Install it yourself

On Linux x86-64 the conda-forge package resolves:

```
micromamba create -n sps -c conda-forge --strict-channel-priority stdpopsim=0.3.0
```

On Linux ARM the same dry-run failed, because the package requires SLiM and conda-forge has no ARM build of it. That is why the recipe's image runs as linux/amd64.

The stdpopsim tutorial gives this command-line form: species first, then options, then `population:count` pairs.

```
stdpopsim HomSap -s 1 -c chr22 --left 10000000 --right 10500000 \
  -d OutOfAfrica_2T12 -o x.ts AFR:2 EUR:3
```

In the recipe's 0.3.0 image this wrote a tree sequence with 10 sample genomes and 1147 variant sites. Put `-s` (the seed) after the species name. Always use `-o`, because without it the binary output goes to your terminal.

The minimal Python API:

```python
import stdpopsim

species = stdpopsim.get_species("HomSap")
model = species.get_demographic_model("OutOfAfrica_3G09")
contig = species.get_contig(length=100_000, mutation_rate=model.mutation_rate)
ts = stdpopsim.get_engine("msprime").simulate(model, contig, {"YRI": 5, "CEU": 5}, seed=1)
```

This gave 20 genomes, 141 trees and 295 sites.

## Run the tested example

This recipe builds stdpopsim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 2.9 s. stdpopsim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [stdpopsim-recipe.tar.gz](https://biosimhub.pages.dev/guides/stdpopsim/stdpopsim-recipe.tar.gz) (Dockerfile, run_stdpopsim.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf stdpopsim-recipe.tar.gz
   cd stdpopsim
   sh run.sh
   ```

![Terminal recording of the stdpopsim example run](https://biosimhub.pages.dev/media/stdpopsim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/stdpopsim:0.3.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/stdpopsim:0.3.0 python /opt/run_stdpopsim.py --scenario homsap_ooa3 \
    --n1 10 --n2 10 --n3 0 --length 200000 --seed 42 > out/stdpopsim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `sim.trees` | 87.5 KB |
| `sim.vcf` | 74.4 KB |
| `stdpopsim_log.txt` | 302 B |
| `summary.csv` | 212 B |

<details><summary>First lines of <code>sim.vcf</code></summary>

```
##fileformat=VCFv4.2
##source=tskit 1.0.3
##FILTER=<ID=PASS,Description="All filters passed">
##contig=<ID=1,length=200001>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	tsk_0	tsk_1	tsk_2	tsk_3	tsk_4	tsk_5	tsk_6	tsk_7	tsk_8	tsk_9	tsk_10	tsk_11	tsk_12	tsk_13	tsk_14	tsk_15	tsk_16	tsk_17	tsk_18	tsk_19
1	84	0	G	T	.	PASS	.	GT	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|1	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0
1	426	1	A	T	.	PASS	.	GT	0|0	1|1	1|1	0|1	1|0	1|0	1|1	0|1	0|1	0|1	1|1	1|0	1|1	0|1	1|1	0|0	1|0	1|1	1|0	1|1
1	511	2	A	C	.	PASS	.	GT	1|1	0|0	0|0	1|0	0|1	0|1	0|0	1|0	0|0	0|0	0|0	0|1	0|0	1|0	0|0	1|1	0|1	0|0	0|1	0|0
1	1142	3	C	T	.	PASS	.	GT	0|0	1|1	1|1	0|1	1|0	1|0	1|1	0|1	1|1	1|1	1|1	1|0	1|1	0|1	1|1	0|0	1|0	1|1	1|0	1|1
1	1197	4	A	C	.	PASS	.	GT	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|1	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0
1	1207	5	A	G	.	PASS	.	GT	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	1|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0
```

</details>

<details><summary>First lines of <code>stdpopsim_log.txt</code></summary>

```
Homo sapiens, model OutOfAfrica_3G09 (Three population out-of-Africa)
contig 200000 bp, seed 42, trees 287, mutations 702
all 40 701 0.0006218076923076913 -0.9209088349863743
YRI 20 598 0.0007395789473684151 -0.5122124200255639
CEU 20 253 0.0004077368421052629 0.597278570308385
Fst YRI vs CEU: 0.0756
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
scope,samples,segregating_sites,pi_per_bp,tajima_d
all,40,701,0.0006218076923076913,-0.9209088349863743
YRI,20,598,0.0007395789473684151,-0.5122124200255639
CEU,20,253,0.0004077368421052629,0.597278570308385
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--scenario` | Species and demographic model | homsap_ooa3 | homsap_ooa3, homsap_ooa2, homsap_africa, dromel_ooa2, aratha_3epoch |
| `--n1` | Individuals sampled from population 1 | 10 | 0 to 200 |
| `--n2` | Individuals sampled from population 2 (if the model has one) | 10 | 0 to 200 |
| `--n3` | Individuals sampled from population 3 (if the model has one) | 0 | 0 to 200 |
| `--length` | Contig length (bp) | 200000 | 1000 to 10000000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper script `run_stdpopsim.py` maps a scenario name to a species and model id, builds a generic contig of the length you set, and calls the msprime engine. Three details matter. It passes the mutation rate the model was fitted with (the tutorial warns that the species default can give too little diversity for this model). It samples `--n1`, `--n2` and `--n3` diploid individuals from the model's sampling populations in order. It then computes the statistics with tskit.

The log from the example (seed 42, 200 kb, 10 YRI and 10 CEU individuals):

- 287 trees and 702 mutations.
- All 40 genomes: 701 segregating sites, pi 0.000622 per bp, Tajima's D -0.92.
- YRI (20 genomes): 598 sites, pi 0.000740, D -0.51. CEU (20 genomes): 253 sites, pi 0.000408, D 0.60.
- Fst between YRI and CEU: 0.0756.

CEU has about 55% of the YRI diversity (0.000408 against 0.000740) and a positive D. That is the signature of the out-of-Africa bottleneck. `summary.csv` holds the same rows; `segregating_sites` is a count and `pi_per_bp` is per base pair. `sim.vcf` has 20 sample columns, tsk_0 to tsk_19 (10 individuals per population), and `sim.trees` is 89,580 bytes.

## Your own runs

- **Add the third population.** `--n3 10` (CHB) gave 60 genomes, 406 trees, 931 mutations, and Fst YRI vs CEU 0.0642. CHB had pi 0.000599 and D 0.67.
- **Longer contig.** `--length 1000000` gave 1948 trees, 4001 mutations and Fst 0.0773. The Fst moved from 0.0756 to 0.0773, so 200 kb is already close.
- **Another species.** `--scenario dromel_ooa2` (Drosophila, African and European populations) gave 92,390 trees and 10,577 mutations on 200 kb. Pi was 0.0111 in AFR and 0.00513 in EUR, with Fst 0.159. Fly diversity is about 15 times the human values.
- **Another seed.** `--seed 7` gave Fst 0.0580 and 366 trees. A single 200 kb run is a noisy estimate of Fst, so repeat it over seeds.

## Pitfalls

- **Samples are diploid individuals.** `--n1 10` makes 20 genomes. The log's sample counts are genomes.
- **Population order.** `--n1`, `--n2` and `--n3` follow the model's sampling populations, YRI, CEU, CHB for the human model. Check the order in the log before you read the rows.
- **Mutation rate choice.** The model's fitted rate is not the species default. For the human model the tutorial lists 2.35e-8 per bp for the model and 1.29e-8 for the species. The helper uses the model's rate.
- **Generic contig.** The helper uses a uniform recombination rate. A chromosome genetic map needs the command line. Use `-c chr22 -g HapMapII_GRCh38`.
- **Terminal output.** Run the command line with `-o file.ts`, or you will print binary data.

## Further reading

- Tutorial (CLI and Python API): https://stdpopsim.readthedocs.io/en/stable/tutorial.html
- Source: https://github.com/popsim-consortium/stdpopsim
- Paper: Adrion JR et al. (2020) A community-maintained standard library of population genetic models. eLife 9:e54967. https://doi.org/10.7554/eLife.54967

---

Cite: Adrion JR et al. (2020) A community-maintained standard library of population genetic models. eLife 9:e54967. doi:10.7554/eLife.54967

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/stdpopsim).
