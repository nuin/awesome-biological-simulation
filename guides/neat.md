# NEAT

> Simulate Illumina-like reads with empirical error models, insert random variants at a chosen rate, and write the true variants (golden VCF) and true alignments (golden BAM).

Licence: BSD-3-Clause · [Source code](https://github.com/ncsa/NEAT)

## What it simulates

NEAT (NExt-generation sequencing Analysis Toolkit) simulates sequencing reads from a reference genome. It samples fragments, inserts random variants, and adds sequencing errors and quality scores from empirical models. By default the models come from human Illumina data. NEAT can also learn mutation, fragment-length, error, quality-score and GC-bias models from your own data.

Its main output is a pair of truth files. The golden VCF lists every variant NEAT inserted. The golden BAM holds the reads aligned to where they came from. You can run an aligner and variant caller on the FASTQ and compare the result with the truth.

NEAT 4 reads its settings from a YAML config file, not from command-line flags. The README names the main keys: `reference`, `read_len`, `coverage`, `ploidy`, `paired_ended`, `fragment_mean`, `fragment_st_dev`, `mutation_rate`, `produce_bam`, `produce_vcf` and `rng_seed`. It supports SNPs, indels of any length, inversions, translocations and duplications, and can model targeted sequencing from a BED file.

Key assumptions: reads follow the error and mutation models you give or the default human model, and variants are inserted independently unless you supply a VCF.

## When to use it

Use NEAT to produce benchmark data with a known answer, for example to measure how many inserted variants an aligner and caller recover.

- Use [DWGSIM](dwgsim.md) or [wgsim](wgsim.md) when you want fast Illumina-like reads with simple error rates and no learned models.
- Use [InSilicoSeq](insilicoseq.md) for metagenomic read sets with abundance profiles.
- Use [VISOR](visor.md) when the variants of interest are large structural variants on two haplotypes.

## Install

NEAT is BSD-3-Clause licensed. The current release is 4.7.1 (September 2026). Bioconda carries it as a noarch Python package that needs Python 3.10 or later:

```bash
conda create -n neat -c conda-forge -c bioconda neat=4.7.1
conda activate neat
neat --help
```

The README also describes an install from a clone with `conda env create -f environment.yml` and `poetry install`. It notes that NEAT is tested on Linux and that Windows users should use WSL. Install `bcftools` if you want to inspect the VCF files.

## A first run

Adapted from the README (https://github.com/ncsa/NEAT#usage). The commands have not been run for this guide. Write a config file:

```yaml
reference: hg19.fa
read_len: 126
produce_bam: True
produce_vcf: True
paired_ended: True
fragment_mean: 300
fragment_st_dev: 30
```

Then run the simulator. `-o` is the output folder and `-p` an optional file name prefix:

```bash
neat read-simulator -c neat_config.yml -o simulated_reads/ -p sample
```

The recipe below wraps this in a small script that writes the config from your parameters. It uses the 13 kb H1N1 influenza genome shipped in the NEAT repository, with 10x coverage and 100-base paired reads. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds NEAT in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.6 s.

1. Download [neat-recipe.tar.gz](https://biosimhub.pages.dev/guides/neat/neat-recipe.tar.gz) (Dockerfile, run_neat.py, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf neat-recipe.tar.gz
   cd neat
   sh run.sh
   ```

![Terminal recording of the NEAT example run](https://biosimhub.pages.dev/media/neat/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/neat:4.7.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/neat:4.7.1 python /opt/run_neat.py --reference /work/in/reference.fa \
    --read-len 100 --coverage 10 --ploidy 2 --paired true \
    --fragment-mean 300 --fragment-sd 30 --mutation-rate 0.01 \
    --bam true --seed 42 > out/neat_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `neat_config.yml` | 274 B |
| `neat_log.txt` | 5.8 KB |
| `sim_golden.bam` | 124.5 KB |
| `sim_golden.bam.bai` | 656 B |
| `sim_golden.vcf.gz` | 1.2 KB |
| `sim_golden.vcf.gz.tbi` | 238 B |
| `sim_r1.fastq.gz` | 57.6 KB |
| `sim_r2.fastq.gz` | 57.7 KB |
| `simulation_summary.json` | 1.5 KB |

<details><summary>First lines of <code>neat_config.yml</code></summary>

```
reference: /work/in/reference.fa
read_len: 100
coverage: 10.0
ploidy: 2
paired_ended: true
mutation_rate: 0.01
produce_bam: true
produce_vcf: true
produce_fastq: true
min_mutations: 1
overwrite_output: true
threads: 1
```

</details>

<details><summary>First lines of <code>neat_log.txt</code></summary>

```
2026-10-18 05:19:19,406:INFO:neat.common.logging:writing log to: None
2026-10-18 05:19:19,406:INFO:neat.read_simulator.runner:Using configuration file neat_config.yml
2026-10-18 05:19:19,407:INFO:neat.read_simulator.runner:Saving output files to /work/out
2026-10-18 05:19:19,408:INFO:neat.read_simulator.utils.options:Run Configuration...
2026-10-18 05:19:19,408:INFO:neat.read_simulator.utils.options:Input fasta: /work/in/reference.fa
2026-10-18 05:19:19,408:INFO:neat.read_simulator.utils.options:Outputting files to /work/out
2026-10-18 05:19:19,409:INFO:neat.read_simulator.utils.options:Producing the following files:
	- /work/out/sim_r1.fastq.gz
	- /work/out/sim_r2.fastq.gz
	- /work/out/sim_golden.bam
	- /work/out/sim_golden.vcf.gz

```

</details>

<details><summary>First lines of <code>simulation_summary.json</code></summary>

```
{
  "schema_version": "1",
  "neat_version": "4.7.1",
  "run": {
    "started_at": "2026-10-18T05:19:19Z",
    "completed_at": "2026-10-18T05:19:19Z",
    "duration_seconds": 0.336,
    "config_file": "/work/out/neat_config.yml",
    "output_dir": "/work/out",
    "output_prefix": "sim"
  },
  "config": {
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--read-len` | Read length | 100 | 50 to 300 |
| `--coverage` | Mean coverage | 10 | 0.5 to 50 |
| `--ploidy` | Ploidy | 2 | 1 to 4 |
| `--paired` | Paired-end reads | true | true, false |
| `--fragment-mean` | Fragment length mean (paired-end) | 300 | 100 to 1000 |
| `--fragment-sd` | Fragment length standard deviation (paired-end) | 30 | 1 to 300 |
| `--mutation-rate` | Mutation rate (variants per base) | 0.01 | 0 to 0.3 |
| `--bam` | Write the golden BAM | true | true, false |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

Expect these files in the output folder:

- Paired-end FASTQ files named like `sim_r1.fastq.gz` and `sim_r2.fastq.gz`. Single-end runs write one FASTQ.
- A golden VCF named like `sim_golden.vcf.gz`, with the inserted variants plus coverage and allele-balance information.
- A golden BAM named like `sim_golden.bam`, coordinate-sorted, showing where each read originated.
- `simulation_summary.json`, which records the run configuration. The README says every run writes it.
- `neat_config.yml`, the config the script generated.

The README suggests quick checks. `samtools flagstat` on the BAM should show mapped reads when coverage is above 0. `bcftools stats sim_golden.vcf.gz | grep "^SN"` lists variant counts you can compare with the mutation rate. The number of variants per reference base should be on the order of the rate you set.

For a caller benchmark, the README describes `neat compare-vcfs golden.vcf called.vcf`, which uses `hap.py` and tags each missed variant with a reason.

## Pitfalls

- **Config, not flags.** NEAT 4 deprecated most command-line options. NEAT 3.4 was the last release fully supported through the command line.
- **Ploidy.** The README's minimal example uses ploidy 4, while its parameter list gives 2 as the default. Set `ploidy` explicitly.
- **FASTQ order is not shuffled.** Reads come in roughly random fragment-sampling order. The README shows `seqkit shuffle` for tools that assume a shuffled file.
- **Overwrites.** Without `overwrite_output: true`, NEAT stops if output files exist. The recipe turns it on.
- **Small genomes need `min_mutations`.** The README advises at least one so each contig gets a variant. The recipe sets it to 1.
- **Realized depth can be below the request.** Short inserts carry fewer genomic bases and mates overlap.
- **Chromosome names must agree** across the reference, BED files and VCFs.

## Further reading

- Source and README: https://github.com/ncsa/NEAT
- Stephens ZD, Hudson ME, Mainzer LS, Taschuk M, Weber MR, Iyer RK (2016). Simulating next-generation sequencing datasets from empirical mutation and sequencing models. PLoS ONE 11:e0167047. https://doi.org/10.1371/journal.pone.0167047
- Allen JM, Gandhi KR, Alhazmy R, Wasnik Y, Fliege CE (2026). Enhancing next-generation sequencing simulation: updates to NEAT. Journal of Open Source Software 11:9056. https://doi.org/10.21105/joss.09056

---

Cite: Stephens ZD, Hudson ME, Mainzer LS, Taschuk M, Weber MR, Iyer RK (2016). Simulating next-generation sequencing datasets from empirical mutation and sequencing models. PLoS ONE 11:e0167047. doi:10.1371/journal.pone.0167047

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/neat).
