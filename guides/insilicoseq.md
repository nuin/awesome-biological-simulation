# InSilicoSeq

> Simulate Illumina metagenomic reads from a multi-FASTA of genomes using built-in error models and an abundance distribution.

Licence: MIT · [Source code](https://github.com/HadrienG/InSilicoSeq)

## What it simulates

InSilicoSeq (ISS) simulates Illumina reads from a set of genomes mixed at chosen abundances. It was written for metagenomes, and it also works for one genome.

The inputs are a multi-FASTA file where each record is one genome, a number of reads, an error model and an abundance distribution. The outputs are two FASTQ files (R1 and R2) and a table with the abundance of each genome.

Key assumptions:

- Abundance is the share of reads that come from a genome. It ignores genome length, so it does not equal the number of cells.
- Quality scores and errors come from kernel density estimators fitted to real runs. They cover substitutions, insertions and deletions.
- Pre-built models exist for MiSeq, HiSeq, NovaSeq and NextSeq. The biosimhub example offers the first three.
- Abundances are drawn at random from the chosen distribution, and the seed fixes the draw.

## When to use it

Use ISS to test a metagenome pipeline with a known community. Typical questions:

- Does my taxonomic profiler recover a log-normal community of 20 species?
- How does 300 bp MiSeq versus 125 bp HiSeq read length change assembly?
- How low can a genome's abundance go before my binner misses it?

[wgsim](wgsim.md), [DWGSIM](dwgsim.md) and [pIRS](pirs.md) on biosimhub simulate one reference at a time and plant variants or use flat error rates. Use them for variant calling. [gargammel](gargammel.md) fits better for ancient DNA, because it adds fragmentation and damage.

## Install it yourself

The Bioconda and PyPI package is `InSilicoSeq` 2.0.1.

```bash
conda create -n iss -c conda-forge -c bioconda insilicoseq=2.0.1
conda activate iss
# or
pip install InSilicoSeq==2.0.1
```

A micromamba 2.0.5 dry run of the conda command resolves. The pip version requires Biopython, NumPy, pysam and SciPy.

The minimal command takes a multi-FASTA file and an output prefix:

```bash
iss generate --genomes genomes.fa --model miseq --n_reads 10000 \
  --abundance lognormal --cpus 1 --seed 42 --output iss_reads
```

- `--model` is `miseq`, `hiseq`, `novaseq` or `nextseq`, or the path to a model file made with `iss model`.
- `--n_reads` is the total number of reads. It accepts suffixes such as `0.5M`.
- `--abundance` is `lognormal` (the default), `uniform`, `halfnormal`, `exponential` or `zero_inflated_lognormal`.
- `--abundance_file` gives the abundances yourself, one genome per line, summing to 1.
- `--cpus` defaults to 2.
- `--draft` takes contig files, and treats all contigs in a file as one genome.
- `--gc_bias`, `--compress` and `--store_mutations` switch on GC bias, gzip output and a VCF.

## Run the tested example

This recipe builds InSilicoSeq in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 8.3 s.

1. Download [insilicoseq-recipe.tar.gz](https://biosimhub.pages.dev/guides/insilicoseq/insilicoseq-recipe.tar.gz) (Dockerfile, example genomes.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf insilicoseq-recipe.tar.gz
   cd insilicoseq
   sh run.sh
   ```

![Terminal recording of the InSilicoSeq example run](https://biosimhub.pages.dev/media/insilicoseq/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/insilicoseq:2.0.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/insilicoseq:2.0.1 iss generate --genomes /work/in/genomes.fa \
    --model miseq --n_reads 10000 --abundance lognormal \
    --cpus 1 --seed 42 --output iss_reads > out/iss_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `iss_log.txt` | 0 B |
| `iss_reads.iss.tmp.0.vcf` | 0 B |
| `iss_reads_R1.fastq` | 3.0 MB |
| `iss_reads_R2.fastq` | 3.0 MB |
| `iss_reads_abundance.txt` | 56 B |

<details><summary>First lines of <code>iss_reads_R1.fastq</code></summary>

```
@genome_A_0_0/1
AACTACGCGGTTCTTAAAGTCGTCTTTCCTAGGTTGAACTTCTACTTGCACACTGGTCATTGTGCGCTTGTGGTAAGTGCGCCCGCTATTCCAACTTCGTGAGCATGGTACACTTAAGGGAGTAGGCGGCGGAACCTGGTCGAGAATTATAAATATCGATTGCACTTGTATTGAATCGCATGAGACGCCGACGATTTTGT
+
CCCCCGGGEGGGGGGGGGGGGGGGGGGFGGFGGGGGGGGGEGGGGGGGGGGGGGFGFGGGGGGGGGFGGG:GGGGFGGGGGFGGGGGGFGGGGGGGCFCGGGGGGGGEGFGGGGGFGGGGGFGGGG7GGFFGGGGGGGGFGGG?GGAFGFEGGFGGFGGGGGCGFE<GG7GFGDGFGCFBGGEGGGGE?GGGFFGGGGG:
@genome_A_1_0/1
CGGAAAAGCCCGTCAGACAGGCGACGAGTACAATGCATTCTAACGTTATCCAATCAAGGACACAGCGTCTCGCTCGGTTCCCCTTGCCGATGCGAGACTAAAATTGCCAAGAAACCAGCCAGTGTTCGCTCTCAGCTCGGACCGGTAGCGCCGCACTTGCAGTTCAGGTCGGTCATCCATCCACAATCTGGACGAAGGGG
+
CCCCCFGGFFG9EGGFG@FGDEF6ECE@GGGGF<FGGF@DEGFEGGC<@C@BC@G9FEG<EGGGC@GGFFCG@CEFC:FCF<FF,C:6GCGBFGFEECGGG9FG<,FFG9G<::GFECGCGCBC?FD<GBEGF4GF?5FECGF5=:F+DFG=F,F,?F38FFDEC8<3FC=?G,C@C*FG@CFC,@A;DFF;,GE,FF=?
@genome_A_2_0/1
ATAATGGTTTGATTGGACCGGTACTGCATATTAACTTGGCTGTACCAATTCGAAAGTTTCGAATTGTGCGCCCTATGCAGTCTCCGTCTAATTTTAGGGGGTAGATAGTGTTCATAGGCACGGGTCACGATCGTCACCAAGAATACAACCATGCTTGTTGACTGGCTATTCGGTAAAGGTCCTGTGCCTATGCCGGGTTC
+
CCCCCGGGGGGGGGCGGGGGGGGGGFGGGGGCFGGGGGGGFGGGGGGGGGAGGFGEFGGGGGGGFGGDGFGGGGGGGFGGGGGGGFEGGGGGGGGGGGGGGGGGGECGGGGGGGGGCGGGGGGGGGGGFGGGFGGFFGFGG
```

</details>

<details><summary>First lines of <code>iss_reads_R2.fastq</code></summary>

```
@genome_A_0_0/2
ATAACAAGTGGGGGGCGCAAGGTTATAATAAGTCCTTGTTCGCCTAAAGAAACAATAACTCTTTTGGATAGTAGTCATACAAACTGGCAATCTCGTAACAAACATGGCCGAGGCGGATCAATTAGCCCAATCCTCTGCTCTCCACACGCACTGTATCACCAGTGAGAAGCTTAGGCGACATAAACTCATGCCAAGCTCGG
+
CCCCCEGGGGGGGGGGGGGGGGGGGCGFFGGGGGGGGGGGFGGGGGGFGDGGGGGGGGGGGGFFCFGFGGCGGFGGGGGGGGGGGGGGGGGGGFGGGGGG:GEGGGGGGGGGGGGDGCGGGGEEGGDCGCGGCCGGGGGGGFCGGGGCG3G=CCGGGGFFGEG,G9GGG;GGFGGFGGG7DGGFGCAFDF8GGGFCGG;G
@genome_A_1_0/2
TCCAGGCATCAGTAGAAATGTAAAACGGGGGTGAAAGCCACCATGGGGAGGGCGCACGCCTTGAGAAAAAGATAGTGCCTAACTGGAATAGGCTACTATAGGCCATTCACGGGTGAGTTTCCCGGCATAGGCGGAGACACGGCTACAAGTGATGGCACCACAAATATATTCTGTGATGCGCGTGGTTAGCCTCCATCGGC
+
BCCCCGGGGGGDGGGGGGGGCGGGGGGGGGGGFGGFGGGGGGGGGGGGGDGGFGGGGFFGGGGGGGGGGGFGFGGGGGGGGGGGGGGGCGGFGGCGGGGGGGGGGCGFFDGGGCGGGGGGGF<G:GGGGGGGGGGGGGGGGFCFFFF<7GGFGEGGAFGGFGCGDGGGFDCCCGE9GGGGAEGG?GCCFFF8GC:GGGGF
@genome_A_2_0/2
CAACCAACGGCAATGCATAAGCGGGGAAAAACCAACCACGCGGTAAGAGAGGAAATCAGTATGAAAGACTGTCGACTCTCGATGTAATTCCGCAACATTTTTGCTATGAAAGATGTCTCTGAAGGTAATTAATCCCAACTAAAAGGTAGTACAACGTAGGGTAGTCACACCTTCGGTCGTGGGTTGTACGATAACTCCCT
+
CACC<GDGFGG6GGGGGDCGFGGFDGEGFG<GFGBGGC;,GGGCFGFG@GFFGGG<<GGD99GCECE8F8GCFGGFDEGGGFGF6FG@G@F9FGDGGGAE<GGFGFF7G9GGF,B@C4GFACDFEGEGG<G5GBGGFF?,A
```

</details>

<details><summary>First lines of <code>iss_reads_abundance.txt</code></summary>

```
genome_A	0.6536174529063914
genome_B	0.3463825470936087
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--model` | Error model | miseq | miseq, hiseq, novaseq |
| `--abundance` | Abundance distribution | lognormal | lognormal, uniform, halfnormal, exponential |
| `--n_reads` | Number of reads (About 0.65 s and 0.6 MB of FASTQ per 1000 reads; larger runs would pass the 600 s and 500 MB job limits.) | 10000 | 100 to 300000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The input has two genomes, `genome_A` and `genome_B`, 20,000 bp each.

`iss_reads_R1.fastq` and `iss_reads_R2.fastq` are 3,122,780 bytes each. Each holds 5,000 reads of 301 bases, because ISS counts the reads of a pair separately: `--n_reads 10000` gives 5,000 pairs. The documentation lists the MiSeq model as 300 bp, and this run produced 301. Names look like `@genome_A_0_0/1`, with the source genome first and the mate (`/1` or `/2`) last.

`iss_reads_abundance.txt` has two lines:

```
genome_A	0.6536174529063914
genome_B	0.3463825470936087
```

The abundances sum to 1. Counting the read names gives 3,268 pairs from genome A (65.4%) and 1,732 from genome B (34.6%). That is about 98x coverage for A and 52x for B, since 3,268 pairs of 602 bases cover 20,000 bp 98 times.

`iss_log.txt` is empty in the recipe because ISS logs to standard error. With `2>&1` it shows lines such as `Using kde ErrorModel`, `Setting random seed to 42`, `Using lognormal abundance distribution` and `Generating 10000 reads`.

`iss_reads.iss.tmp.0.vcf` is an empty 0-byte file left by the run. Ignore it. Add `--store_mutations` if you want a real VCF.

## Your own runs

These runs used the recipe's image and the example genomes. The first two took 13 s and 14 s.

**HiSeq model.** Set `--model hiseq`. Reads are 126 bases and each FASTQ is 1,372,780 bytes against 3,122,780. The abundances stay at 0.654 and 0.346 and the pair counts stay at 3,268 and 1,732, because the seed fixes the abundance draw and the model does not touch it.

**Uniform abundance.** Set `--abundance uniform`. The table reads 0.5 and 0.5, and each genome gets 2,500 pairs.

**More reads and another seed.** Set `--n_reads 20000 --seed 7`. The abundance draw changes to 0.896 for genome A and 0.104 for genome B. The pair counts are 8,963 and 1,037, and each FASTQ grows to 6,247,780 bytes. A two-genome community can come out very uneven with a log-normal draw. Run several seeds when the result depends on the community.

For your own community, put each genome as one record in the FASTA file, and name the records as you want them to appear in the read names.

## Pitfalls

- `--n_reads` counts reads. For 10,000 pairs ask for 20,000.
- Abundance is a read share. A 5 Mb genome and a 50 kb phage at equal abundance get equal reads, so the phage is 100 times deeper. Use `--coverage` or `--coverage_file` when you want depth.
- Every FASTA record is a genome. A draft assembly with 200 contigs gives 200 genomes unless you pass it with `--draft`.
- `--gc_bias` can drop reads, so the total can fall below `--n_reads`.
- The default is 2 CPUs. The recipe sets `--cpus 1` to match its 1-CPU container.
- The default seed is random. Pass `--seed` to repeat a run, and note it.

## Further reading

- InSilicoSeq documentation on generating reads: https://insilicoseq.readthedocs.io/en/latest/iss/generate.html
- Error models: https://insilicoseq.readthedocs.io/en/latest/iss/model.html
- Installation: https://insilicoseq.readthedocs.io/en/latest/iss/install.html
- Gourle H et al. (2019). Simulating Illumina metagenomic data with InSilicoSeq. Bioinformatics 35:521-522. https://doi.org/10.1093/bioinformatics/bty630

---

Cite: Gourle H, Karlsson-Lindsjo O, Hayer J, Bongcam-Rudloff E (2019). Simulating Illumina metagenomic data with InSilicoSeq. Bioinformatics 35:521-522. doi:10.1093/bioinformatics/bty630

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/insilicoseq).
