# RSEM (rsem-simulate-reads)

> Fit an RSEM expression model on a small synthetic RNA-seq sample, then simulate new single-end RNA-seq reads from that model with rsem-simulate-reads.

Licence: GPL-3.0 · [Source code](https://github.com/deweylab/RSEM)

## What it simulates

RSEM is a program for estimating gene and isoform expression from RNA-seq reads. Its `rsem-simulate-reads` command goes the other way. It generates RNA-seq reads from an expression profile and a sequencing model that RSEM learned from a real sample.

Three inputs define a simulation:

- A reference built with `rsem-prepare-reference` from a genome and a GTF file (or from transcript sequences).
- An estimated model file, `sample.stat/sample.model`, written by `rsem-calculate-expression`. It holds the fragment length distribution, the read start position distribution and the sequencing error model. It also decides whether reads are single-end or paired-end, and whether they carry quality scores.
- An isoform results file, `sample.isoforms.results`. The simulator reads only its TPM column, so a hand-made expression profile needs only that column changed.

Two more arguments are theta0, the fraction of reads that come from background noise instead of a transcript, and N, the number of reads.

The biosimhub recipe has no real sample to learn from. A driver script builds an RSEM reference from an uploaded genome and GTF, writes a synthetic single-end training sample from the annotated transcripts, fits the model with Bowtie 2, and then simulates. The simulated reads therefore reflect a model fitted to synthetic data.

## When to use it

Use `rsem-simulate-reads` when a pipeline should be tested against reads that mimic one real library's fragment sizes, error profile and expression levels, and you want the true read origin in every header.

Alternatives:

- Polyester (an R package) and Flux Simulator are dedicated RNA-seq simulators. Neither is on biosimhub.
- [InSilicoSeq](insilicoseq.md) simulates Illumina reads from genomes, with abundance levels, for metagenomes.
- [wgsim](wgsim.md) and [DWGSIM](dwgsim.md) simulate DNA reads and have no expression model.

## Install it yourself

Conda, pinned to Bioconda 1.3.3 (builds for linux-64, linux-aarch64, osx-64 and osx-arm64). RSEM needs an aligner for the training step; Bowtie 2 is on Bioconda.

```bash
conda create -n rsem -c conda-forge -c bioconda rsem=1.3.3 bowtie2=2.5.5
conda activate rsem
rsem-prepare-reference --help
```

The Bioconda package pulls in R, because of the differential-expression helpers. The latest GitHub release is v1.3.3. To build from source, see the Compilation section of the README.

## A first run

Adapted from the README, sections Example and Simulation (https://github.com/deweylab/RSEM#simulation).

The README example prepares a reference, estimates expression for a sample called `mmliver_single_quals`, then simulates with the model it learned:

```bash
rsem-prepare-reference --gtf mm9.gtf --bowtie2 /data/mm9 /ref/mouse_0
rsem-calculate-expression --bowtie2 --fragment-length-mean 150.0 \
  --fragment-length-sd 35.0 /data/mmliver.fq /ref/mouse_0 mmliver_single_quals
rsem-simulate-reads /ref/mouse_0 \
  mmliver_single_quals.stat/mmliver_single_quals.model \
  mmliver_single_quals.isoforms.results 0.2 50000000 simulated_reads
```

The README uses Bowtie in its example; `--bowtie2` selects Bowtie 2 instead. The README suggests theta0 from the first value of the third line of `sample.stat/sample.theta`, and N from the fourth number of the first line of `sample.stat/sample.cnt`. Add `--seed <uint32>` for repeatable draws.

## Run the tested example

This recipe builds RSEM (rsem-simulate-reads) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 1.1 s.

1. Download [rsem-recipe.tar.gz](https://biosimhub.pages.dev/guides/rsem/rsem-recipe.tar.gz) (Dockerfile, run_rsem.py, example genome.fa, annotation.gtf, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf rsem-recipe.tar.gz
   cd rsem
   sh run.sh
   ```

![Terminal recording of the RSEM (rsem-simulate-reads) example run](https://biosimhub.pages.dev/media/rsem/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/rsem:1.3.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/rsem:1.3.3 python3 /opt/run_rsem.py --genome /work/in/genome.fa \
    --gtf /work/in/annotation.gtf --train-reads 4000 \
    --reads 2000 --readlen 50 --theta0 0.02 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `ref.1.bt2` | 4.0 MB |
| `ref.2.bt2` | 1.1 KB |
| `ref.3.bt2` | 44 B |
| `ref.4.bt2` | 1.1 KB |
| `ref.chrlist` | 10 B |
| `ref.grp` | 8 B |
| `ref.idx.fa` | 4.4 KB |
| `ref.n2g.idx.fa` | 4.4 KB |
| `ref.rev.1.bt2` | 4.0 MB |
| `ref.rev.2.bt2` | 1.1 KB |
| `ref.seq` | 4.7 KB |
| `ref.ti` | 427 B |
| `ref.transcripts.fa` | 4.4 KB |
| `run_log.txt` | 14.1 KB |
| `sim.fq` | 229.2 KB |
| `sim.sim.genes.results` | 241 B |
| `sim.sim.isoforms.results` | 305 B |
| `train.fq` | 448.1 KB |
| `trained.genes.results` | 250 B |
| `trained.isoforms.results` | 314 B |
| `trained.log` | 200 B |
| `trained.stat/trained.cnt` | 55 B |
| `trained.stat/trained.model` | 34.8 KB |
| `trained.stat/trained.theta` | 166 B |

<details><summary>First lines of <code>ref.chrlist</code></summary>

```
chrT	9000
```

</details>

<details><summary>First lines of <code>ref.grp</code></summary>

```
1
3
4
5
```

</details>

<details><summary>First lines of <code>ref.idx.fa</code></summary>

```
>geneA.1
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
>geneA.2
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
>geneB.1
CCACGTGACACGGGCTCTGCAATGGTTGATGTTCAAATTTGCCATGAGCGAAGCTTCCCTATAAAAACTTTCCCGATCGCCTGGCTGGAACACATGCGTATTTAGTGGGCCCGAAGCTCGTCACCGGTTAAAGGTTAGGTGGGGCCTTCTTCATGTGCCCGATGACCGGACACGAATCTAATCAAGCATCAATGGTTACA
```

</details>

<details><summary>First lines of <code>ref.n2g.idx.fa</code></summary>

```
>geneA.1
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
>geneA.2
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
>geneB.1
CCACGTGACACGGGCTCTGCAATGGTTGATGTTCAAATTTGCCATGAGCGAAGCTTCCCTATAAAAACTTTCCCGATCGCCTGGCTGGAACACATGCGTATTTAGTGGGCCCGAAGCTCGTCACCGGTTAAAGGTTAGGTGGGGCCTTCTTCATGTGCCCGATGACCGGACACGAATCTAATCAAGCATCAATGGTTACA
```

</details>

<details><summary>First lines of <code>ref.seq</code></summary>

```
1100 1100
geneA.1
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
900 900
geneA.2
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1500 1500
geneB.1
CCACGTGACACGGGCTCTGCAATGGTTGATGTTCAAATTTGCCATGAGCGAAGCTTCCCTATAAAAACTTTCCCGATCGCCTGGCTGGAACACATGCGTATTTAGTGGGCCCGAAGCTCGTCACCGGTTAAAGGTTAGGTGGGGCCTTCTTCATGTGCCCGATGACCGGACACGAATCTAATCAAGCATCAATGGTTACA
```

</details>

<details><summary>First lines of <code>ref.ti</code></summary>

```
4 0
geneA.1
geneA
chrT
+ 1100
2 201 700 1001 1600
gene_id "geneA"; transcript_id "geneA.1"; exon_number "1";
geneA.2
geneA
chrT
+ 900
2 201 700 1201 1600
```

</details>

<details><summary>First lines of <code>ref.transcripts.fa</code></summary>

```
>geneA.1
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
>geneA.2
CTAGGGGCTCTGTAGGTGTAGCAACCCTTTGACTGACGGGCATCTTCGAGGCATGATGCAGTTCTCTCACAGTTGCGTCGTACGCTGGCGTAACACACTGTATACATCCCAAAGTTTCGAAATCCGTCGGGCTACGCCGACCGTCCTACGGGCGGGCAACCTGTGCTAACTTTCGAGACCAGAACAAAACATGCTACCCG
>geneB.1
CCACGTGACACGGGCTCTGCAATGGTTGATGTTCAAATTTGCCATGAGCGAAGCTTCCCTATAAAAACTTTCCCGATCGCCTGGCTGGAACACATGCGTATTTAGTGGGCCCGAAGCTCGTCACCGGTTAAAGGTTAGGTGGGGCCTTCTTCATGTGCCCGATGACCGGACACGAATCTAATCAAGCATCAATGGTTACA
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
rsem-prepare-reference --gtf /work/in/annotation.gtf --bowtie2 /work/in/genome.fa ref
rsem-extract-reference-transcripts ref 0 /work/in/annotation.gtf None 0 /work/in/genome.fa
Parsing gtf File is done!
/work/in/genome.fa is processed!
4 transcripts are extracted.
Extracting sequences is done!
Group File is generated!
Transcript Information File is generated!
Chromosome List File is generated!
Extracted Sequences File is generated!

rsem-preref ref.transcripts.fa 1 ref
```

</details>

<details><summary>First lines of <code>sim.fq</code></summary>

```
@0_1_3_1022
ATCGATTTTTTCGACCCGTTTCGACTGAGAAACACACTCCGCTCCGATAT
+
EAA8>876>G;A7CB56IDFH958I8A;A@5>5;?A=76;I<9>6EB9<?
@1_1_3_505
ACTTCTCACCACTGCTTTTCATAGGCTTTGACACCGAATTAGTCGCAGGT
+
H;6@9?5I;F=D:@FA<I:A@:7;E865I>E=9;55F9CCDEEA6H<B7H
@2_1_3_601
GTCCGGTCTAGGAATGACTGCCTTTGCCATCGTCTAGTCAAAGGGTTATG
+
99H6A;C8GHBE;B7G>E98=GG@;E7G<;G7:9B=5F<G;58?@=?9C7
```

</details>

<details><summary>First lines of <code>sim.sim.genes.results</code></summary>

```
gene_id	transcript_id(s)	length	effective_length	count	TPM	FPKM
geneA	geneA.1,geneA.2	967.85	768.85	410.00	239164.66	271934.67
geneB	geneB.1	1500.00	1301.00	500.00	172364.39	195981.52
geneC	geneC.1	1000.00	801.00	1051.00	588470.96	669102.43
```

</details>

<details><summary>First lines of <code>sim.sim.isoforms.results</code></summary>

```
transcript_id	gene_id	length	effective_length	count	TPM	FPKM	IsoPct
geneA.1	geneA	1100	901.00	163.00	81136.76	92254.00	33.93
geneA.2	geneA	900	701.00	247.00	158027.90	179680.66	66.07
geneB.1	geneB	1500	1301.00	500.00	172364.39	195981.52	100.00
geneC.1	geneC	1000	801.00	1051.00	588470.96	669102.43	100.00
```

</details>

<details><summary>First lines of <code>train.fq</code></summary>

```
@train0
GGCCTCTCGAGTGCGGTTAGGGTATGCTTTAGTATCAGACACGTAGCCTG
+
<<98F7GB657;<EH5F;IFB<CG=5:B?=9;?87A8@@H=6CF8A7F>I
@train1
TCGGCGGCTCCACTCACGACCGCTCATAGCAGCGACTCAAGGTTTGTTCT
+
;76<>7<8A=CI@:@@;=I7HI:F<:CA=IF<?6<6?A=7;G?;IDAIC9
@train2
TATGGAATAGTGGAAGCATGCCGAGACAACCGCGGAAAACCTATGTGGTC
+
F=GBGA@<9ED7689I:BH7AAHCE=F58F=I?8>B:C5=E:E8I>IEH;
```

</details>

<details><summary>First lines of <code>trained.genes.results</code></summary>

```
gene_id	transcript_id(s)	length	effective_length	expected_count	TPM	FPKM
geneA	geneA.1,geneA.2	954.38	755.38	792.00	242804.26	276280.38
geneB	geneB.1	1500.00	1301.00	999.00	177820.84	202337.51
geneC	geneC.1	1000.00	801.00	2004.00	579374.90	659254.98
```

</details>

<details><summary>First lines of <code>trained.isoforms.results</code></summary>

```
transcript_id	gene_id	length	effective_length	expected_count	TPM	FPKM	IsoPct
geneA.1	geneA	1100	901.00	256.66	66013.98	75115.52	27.19
geneA.2	geneA	900	701.00	535.34	176790.28	201164.87	72.81
geneB.1	geneB	1500	1301.00	999.00	177820.84	202337.51	100.00
geneC.1	geneC	1000	801.00	2004.00	579374.90	659254.98	100.00
```

</details>

<details><summary>First lines of <code>trained.log</code></summary>

```
4000 reads; of these:
  4000 (100.00%) were unpaired; of these:
    0 (0.00%) aligned 0 times
    3243 (81.08%) aligned exactly 1 time
    757 (18.93%) aligned >1 times
100.00% overall alignment rate
```

</details>

<details><summary>First lines of <code>trained.stat/trained.cnt</code></summary>

```
0 4000 0 4000
4000 0 757
4757 1
0	0
1	3243
2	757
Inf	0
```

</details>

<details><summary>First lines of <code>trained.stat/trained.model</code></summary>

```
1

0.5

99 300 201
5.147496463e-05 5.749171711e-05 6.414044936e-05 7.147862865e-05 7.956790448e-05 8.847429782e-05 9.826838616e-05 0.0001090254827 0.000120825808 0.0001337546511 0.0001479025198 0.0001633652751 0.0001802
```

</details>

<details><summary>First lines of <code>trained.stat/trained.theta</code></summary>

```
5
0.0512499999999999 0.0642105270564726 0.133789472943528 0.24975 0.500999999999999
0.0512499999999999 0.0642105270564726 0.133789472943528 0.24975 0.500999999999999
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--train-reads` | Reads in the synthetic training sample | 4000 | 500 to 200000 |
| `--reads` | Reads to simulate | 2000 | 1 to 1000000 |
| `--readlen` | Read length | 50 | 25 to 150 |
| `--theta0` | Fraction of reads from background noise | 0.02 | 0 to 0.5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

With the output name `sim`:

- `sim.fq`: simulated reads. A FASTQ file appears when the model came from FASTQ reads. FASTA (`sim.fa`) appears for models trained without quality scores. Paired-end models give `_1` and `_2` files.
- `sim.sim.isoforms.results` and `sim.sim.genes.results`: expression levels measured by counting where each simulated read came from. These are the truth to compare with a quantifier's estimate.
- `trained.isoforms.results` and `trained.genes.results`: the estimate from the training sample, which defines the TPM values the simulation used.

Each read header follows `@_rid_dir_sid_pos[_insertL]`. `rid` is the read index from 0. `dir` is 0 for the forward strand and 1 for the reverse. `sid` is the transcript index, with 0 meaning background noise. `pos` is the 0-based start in that strand of the transcript. `insertL` appears for paired-end reads only.

## Pitfalls

- **The bioconda `rsem-simulate-reads` can crash.** On biosimhub the bioconda 1.3.3 build ended with a segmentation fault at the simulation step, on arm64 and x86-64, after fitting fine. RSEM 1.3.3 built from the GitHub tag simulated the same model without error, so the recipe builds from source with Debian's bowtie2 2.5.0. If the conda install crashes the same way, build from source (`make` and `make install` in the release tarball).

- **A learned model is required.** There is no default model. Without real reads you must use synthetic training reads, as the recipe does, or a model file from a published run.
- **Single-end needs a fragment length distribution.** The README stresses that accurate `--fragment-length-mean` and `--fragment-length-sd` matter for single-end data.
- **theta0 and N come from the training sample.** Defaults are not guessed; the README shows where to read them.
- **The expression profile is editable.** Change only the TPM column of `sample.isoforms.results`, and keep the file format.
- **The recipe's training sample is idealised.** Reads with a fixed expression profile, no sequencing errors and random base qualities between Phred 20 and 40 give a model with no sequencing errors, and the simulated reads inherit that.
- **Allele-specific references.** Use `sample.alleles.results` instead of the isoforms file for those.
- **Memory and image size.** The Bioconda package brings R and its packages; the image is large.

## Further reading

- Repository and README: https://github.com/deweylab/RSEM
- Command documentation: https://deweylab.github.io/RSEM/rsem-calculate-expression.html and https://deweylab.github.io/RSEM/rsem-prepare-reference.html
- Li B, Dewey CN (2011). RSEM: accurate transcript quantification from RNA-Seq data with or without a reference genome. BMC Bioinformatics 12:323. https://doi.org/10.1186/1471-2105-12-323

---

Cite: Li B, Dewey CN (2011). RSEM, accurate transcript quantification from RNA-Seq data with or without a reference genome. BMC Bioinformatics 12:323. doi:10.1186/1471-2105-12-323

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/rsem).
