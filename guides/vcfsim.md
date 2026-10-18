# vcfsim

> Simulate all-sites VCF files with configurable missing data from msprime coalescent simulations.

Licence: MIT · [Source code](https://github.com/samuk-lab/vcfsim)

## What it simulates

vcfsim writes simulated VCF files that contain every site, variant or not, and lets you mask some of the data as missing. It draws genealogies and mutations from a coalescent simulation and then writes them as a VCF. The conda package depends on [msprime](msprime.md), and the output header names tskit as the source.

Input is a sample size, a sequence length, ploidy, effective population size Ne, a per-site mutation rate mu, the percentage of missing sites, the percentage of missing genotypes and a seed. Output is one VCF per replicate.

Key assumptions: one randomly mating population of constant size Ne (a two-population split is available through `--population_mode 2` and `--div_time`), and missing data added after the simulation. Per the README, `--percent_missing_sites` gives uniform missingness across sites. Four HMM options give clustered missingness instead.

## When to use it

Use it to test a variant-calling or filtering pipeline on data where you know the truth, to see how missing data changes estimates of diversity (pi) or Fst, or to make an all-sites VCF for tools that need invariant sites.

Alternatives on biosimhub:

- msprime fits better when you also want a tree sequence and summary statistics, since vcfsim builds on it for the VCF-with-missing-data case.
- [stdpopsim](stdpopsim.md) fits better when you want a published demographic model (human, fly or Arabidopsis).

## Install it yourself

vcfsim 1.2.2 is a noarch bioconda package. The index lists dependencies on ipython, msprime, numpy, pandas and Python 3.6 or newer.

```
conda create -n vcfsim_env -c conda-forge -c bioconda python=3.10 vcfsim=1.2.2
```

The README gives `conda create -n vcfsim_env python=3.10` followed by `conda install bioconda::vcfsim`. This rests on the anaconda.org index.

The minimal command, which needs `--seed`, both missing-data percentages and one sample option (`--sample_size`, `--samples` or `--samples_file`):

```
vcfsim --seed 1234 --sequence_length 10000 --sample_size 10 \
  --percent_missing_sites 0 --percent_missing_genotypes 0 --output_file sim
```

Without `--output_file`, the VCF goes to standard output. `vcfsim --help` lists all options.

## Run the tested example

This recipe builds vcfsim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.7 s.

1. Download [vcfsim-recipe.tar.gz](https://biosimhub.pages.dev/guides/vcfsim/vcfsim-recipe.tar.gz) (Dockerfile, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf vcfsim-recipe.tar.gz
   cd vcfsim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/vcfsim:1.2.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/vcfsim:1.2.2 vcfsim --chromosome 1 --replicates 1 --seed 1234 \
    --sequence_length 10000 --ploidy 2 --Ne 100000 \
    --mu 1e-06 --percent_missing_sites 0 --percent_missing_genotypes 0 \
    --output_file sim --sample_size 10
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `sim1234.vcf` | 643.8 KB |

<details><summary>First lines of <code>sim1234.vcf</code></summary>

```
##fileformat=VCFv4.2
##source=tskit 1.0.3
##FILTER=<ID=PASS,Description="All filters passed">
##contig=<ID=1,length=10000>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	tsk_1	tsk_2	tsk_3	tsk_4	tsk_5	tsk_6	tsk_7	tsk_8	tsk_9	tsk_10
1	1	.	A	G,C,T	.	PASS	.	GT	2|0	1|1	3|1	1|1	1|1	1|1	1|3	2|3	0|1	3|1
1	2	.	C	T	.	PASS	.	GT	0|0	1|1	0|1	1|1	1|1	1|1	1|0	1|0	0|1	0|1
1	3	.	T	G,A,C	.	PASS	.	GT	0|0	2|2	0|3	3|1	1|3	2|3	2|0	2|0	0|3	0|2
1	4	.	C	.	.	PASS	.	GT	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0
1	5	.	A	G	.	PASS	.	GT	0|0	1|1	0|1	1|0	0|1	1|1	1|0	1|0	0|1	0|1
1	6	.	T	.	.	PASS	.	GT	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0	0|0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--sample_size` | Number of samples | 10 | 2 to 200 |
| `--sequence_length` | Sequence length (bp) | 10000 | 100 to 1000000 |
| `--ploidy` | Ploidy | 2 | 1 to 4 |
| `--Ne` | Effective population size | 100000 | 10 to 10000000 |
| `--mu` | Mutation rate per site per generation | 1e-06 | 1e-11 to 0.001 |
| `--percent_missing_sites` | Percent of sites missing | 0 | 0 to 100 |
| `--percent_missing_genotypes` | Percent of genotypes missing | 0 | 0 to 100 |
| `--replicates` | Replicate VCFs | 1 | 1 to 5 |
| `--seed` | Seed | 1234 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example calls `vcfsim` directly. It took 0.7 seconds and wrote `sim1234.vcf` (659,275 bytes). The name is the `--output_file` value followed by the seed.

The header declares VCF 4.2, source tskit 1.0.3, one contig of length 10000 and one `GT` field. The ten samples are named `tsk_1` to `tsk_10`. With `--ploidy 2` each genotype is phased, like `2|0`.

Counting the records gives:

- 10,000 rows, one per base pair. This is the "all sites" property.
- 8690 rows have an ALT allele, and 4342 of those have two or three ALT alleles (the first row is `A G,C,T`).
- 1310 rows are invariant, with ALT `.`.
- No genotype is missing, as set by the two percent flags.

Many rows carry several ALT alleles because mu and Ne are large: 4 x 100,000 x 1e-6 = 0.4 expected differences per site between two sequences. Repeated mutations at one site are common at that rate.

## Your own runs

- `--mu 1e-08`: 236 of 10,000 rows have an ALT allele and 2 are multiallelic.
- `--mu 1e-08 --percent_missing_sites 20 --percent_missing_genotypes 10`: 8000 rows remain. Sites were dropped, leaving 1592 gaps in the POS column. Of 80,000 genotypes, 8000 (10%) are `.|.`.
- `--mu 1e-08 --replicates 3 --ploidy 1`: files `sim1234.vcf`, `sim1235.vcf` and `sim1236.vcf`. The seed rises by one per replicate. Genotypes are single alleles such as `0`. ALT rows are 152, 104 and 112. Haploid samples give 10 sequences instead of 20, so fewer variants than the diploid run.

## Pitfalls

- The two missing-data flags are percentages from 0 to 100. A value of 0.1 means 0.1%.
- Missing sites drop out of the VCF entirely. The 20% run has 8000 rows, so row counts shrink and positions skip.
- Genotype missingness shows as `.|.` for a whole diploid genotype.
- The example's defaults (mu 1e-6, Ne 100,000) give many multiallelic sites. Lowering mu to 1e-8 cut ALT rows to 236, with 2 multiallelic. Check that your downstream tool accepts multiple ALT alleles.
- `--replicates` changes the seed per file (seed, seed + 1, ...). Do not pass the same seed in two separate calls and expect different files.
- `--percent_missing_sites` is required unless you use the four HMM options. Omitting it fails with `ValueError: Either --percent_missing_sites must be provided, or all four HMM parameters must be specified.`

## Further reading

- Source and README: https://github.com/samuk-lab/vcfsim
- Goulart P, Samuk K (2026). vcfsim: flexible simulation of all-sites VCFs with missing data. BMC Bioinformatics. https://doi.org/10.1186/s12859-026-06453-9
- msprime documentation: https://tskit.dev/msprime/docs/stable/

---

Cite: Goulart P, Samuk K (2026). vcfsim. BMC Bioinformatics. doi:10.1186/s12859-026-06453-9

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/vcfsim).
