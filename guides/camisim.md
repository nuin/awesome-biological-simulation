# CAMISIM

> Simulate microbial communities with abundance profiles, time series and strain diversity, and produce metagenome reads plus gold standards for assembly, binning and profiling.

Licence: Apache-2.0 · [Source code](https://github.com/CAMI-challenge/CAMISIM)

## What it simulates

CAMISIM builds a simulated microbial community and then sequences it in silico. It was written for the CAMI benchmarking challenges, so it also writes the answers a benchmark needs: which read came from which genome, what a perfect assembly looks like, and what the true taxonomic profile is.

The pipeline has four steps, from the project's user manual:

1. **Validate the genomes.** For a de novo design, sequences shorter than 1000 bp are removed and the rest are checked for valid characters.
2. **Design the community.** Either from a taxonomic profile in BIOM format, matched to complete NCBI genomes, or de novo from genomes you give it. The de novo design draws genomes across novelty categories (new strain, species, genus, family, order) to spread them over the tree. It can add related strains made with sgEvolver. Abundances come from a log-normal distribution (mu 1 and sigma 2 by default). Time series and differential-abundance sets add noise or draw further samples.
3. **Simulate reads.** Each genome is covered in proportion to its abundance, genome size and the sample size. Simulators are ART (Illumina), wgsim, or NanoSim 3 (Oxford Nanopore).
4. **Make gold standards.** A perfect assembly per sample and pooled, read-to-genome mappings, and a taxonomic profile per sample. Reads can be anonymised and shuffled.

Version 2.0 is a Nextflow pipeline. The earlier Python standalone is kept at tag `1.31-final` and no longer updated. A script, `convert_config.py`, converts a version 1 config file to version 2, with no guarantee of correctness.

## When to use it

Use CAMISIM when a benchmark needs a whole metagenome with ground truth: tools for binning, taxonomic profiling or assembly.

- Use [InSilicoSeq](insilicoseq.md) when you already have the genomes and want Illumina reads with error models and an abundance distribution, without the design step.
- Use [gargammel](gargammel.md) for ancient-DNA mixtures of endogenous and contaminant reads.
- Use [wgsim](wgsim.md) for reads from a single genome.

CAMISIM is heavier than these. The manual says a small simulation fits a laptop with 4 GB RAM, while realistic sets of hundreds of genomes can need hundreds of gigabytes of memory and disk.

## Install

No container recipe is provided for CAMISIM. The pipeline asks Nextflow to create conda environments for its tools at run time through mamba, which needs network access on first use. It also downloads genomes from NCBI in profile mode. A sandbox with no network cannot do either, so this page gives instructions only.

The manual lists three requirements: a Linux system (the only one tested), Nextflow, and mamba or conda. Nextflow and mamba are both available from conda channels.

```bash
conda create -n camisim -c conda-forge -c bioconda nextflow mamba
conda activate camisim
git clone https://github.com/CAMI-challenge/CAMISIM
cd CAMISIM
```

The latest GitHub release is 2.0.1 (March 2026). The repository bundles an NCBI taxonomy dump from 2017 (and one from 2018) and a small set of default genomes.

## A first run

Adapted from the [user manual](https://github.com/CAMI-challenge/CAMISIM/wiki/User-manual) and the [use cases page](https://github.com/CAMI-challenge/CAMISIM/wiki/Use-Cases). From the repository folder, a de novo run with the shipped defaults is:

```bash
nextflow run main.nf
```

The defaults in `pipelines/metagenomic/config/metagenomic.config` are: two samples of 0.05 Gbp each, the ART simulator, a gold-standard assembly per sample and pooled, anonymised reads, and a fixed seed (632741178). The default genome list holds two genomes in `defaults/genomes`. Output goes to `nextflow_out` in the project directory.

Other cases from the manual:

```bash
nextflow run main.nf --params.biom_profile "${projectDir}/defaults/mini.biom"   # from a profile
nextflow run main.nf --type "nanosim3"                                          # other simulator
```

The `type` option takes `art`, `nanosim3` or `wgsim`. Other settings, such as `size`, `number_of_samples` and `seed`, are set in `nextflow.config`.

## Reading the output

The manual describes this layout under the output folder:

- `distributions/distribution_{i}.txt`: genome ID and relative abundance for sample i. The abundance counts genomes, not bases. Two genomes at 0.5 each, one twice as long, give the long one two thirds of the sequence.
- `source_genomes/*.fa`: the genomes used, with unique sequence names.
- `sample_{i}/reads/`: simulated reads. With anonymisation on, `anonymous_reads.fq` is the only FASTQ.
- `sample_{i}/reads/reads_mapping.tsv`: anonymous read ID, genome ID, taxonomic ID and original read ID.
- `sample_{i}/bam/`: one BAM per genome with the true read positions.
- `sample_{i}/contigs/anonymous_gsa.fasta` and `gsa_mapping.tsv`: the perfect assembly and its mapping.
- `anonymous_gsa_pooled.fasta`: the perfect assembly pooled over samples.
- `taxonomic_profile_{i}.txt`: the true profile.
- `seed/seed*.txt`: the seeds used. Reuse `used_initial_seed` to reproduce a run.

## Pitfalls

- **Network is needed at first run.** Environments are built by mamba, and a profile run downloads genomes. Leaving `ncbi_taxdump_file` empty downloads a fresh taxonomy.
- **Sizes grow fast.** The `size` setting is in Gbp per sample, and mapping files add to it. Start with the default 0.05.
- **Abundance is per genome.** Compare abundances as genome counts, not base shares.
- **Profile mode needs complete genomes.** An OTU maps to a genome only within the same family. Unmapped OTUs stay unmapped unless you ask for random genomes.
- **Version 1 and 2 differ.** Older tutorials use a Python script and an INI file. Use the 2.0 pages, or check out `1.31-final` for the old workflow.
- **Linux only.** The manual says the pipeline has been tested on Linux only.

## Further reading

- User manual: https://github.com/CAMI-challenge/CAMISIM/wiki/User-manual
- Configuration options: https://github.com/CAMI-challenge/CAMISIM/wiki/Configuration-File-Options
- File formats: https://github.com/CAMI-challenge/CAMISIM/wiki/File-Formats
- Source: https://github.com/CAMI-challenge/CAMISIM
- Paper: Fritz A, Hofmann P, et al. (2019). CAMISIM: simulating metagenomes and microbial communities. Microbiome 7:17. https://doi.org/10.1186/s40168-019-0633-6

---

Cite: Fritz A, Hofmann P, Majda S, et al. (2019). CAMISIM: simulating metagenomes and microbial communities. Microbiome 7:17. doi:10.1186/s40168-019-0633-6

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/camisim).
