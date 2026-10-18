# Mason (SeqAn)

> Simulate paired-end Illumina reads from a reference genome with Mason 2, writing FASTQ files and a SAM file of the true alignments.

Licence: BSD-3-Clause · [Source code](https://github.com/seqan/seqan/tree/main/apps/mason2)

## What it simulates

Mason is a set of small programs from the SeqAn library that simulate sequencing data. The SeqAn 2.5.2 source contains Mason version 2.0.13. The tools are:

- `mason_genome`: random genome sequences of lengths you choose.
- `mason_variator`: SNPs, small indels and structural variants (insertions, deletions, inversions, duplications, translocations), written as a VCF file and optionally as altered FASTA.
- `mason_simulator`: reads from a reference, with an optional VCF applied first.
- `mason_materializer`, `mason_methylation`, `mason_splicing` and `mason_frag_sequencing`: apply a VCF to a FASTA file, simulate methylation levels, build a transcriptome from a GFF file, and sample fragments.

The read simulator cuts fragments from the (optionally mutated) sequence, then reads one end or both ends. It has error models for Illumina, 454 and Sanger reads. It can also write a SAM file with the true alignment of every read, and it supports bisulfite sequencing.

The biosimhub recipe wraps `mason_simulator` for paired-end Illumina reads from a FASTA file. Parameters are the number of read pairs, read length, mean and standard deviation of the fragment size, the average per-base mismatch probability and a seed.

Key assumptions in the Illumina model: fragment sizes follow a normal distribution (default mean 300, standard deviation 30), and errors are drawn from position-dependent mismatch, insertion and deletion probabilities (default mismatch 0.004, insertion and deletion 0.00005 each). Base qualities are generated to match.

## When to use it

Use Mason when you need reads with a known origin and a variant file in one toolchain. A typical chain is `mason_variator` to plant variants, then `mason_simulator` with the resulting VCF to read from the mutated haplotype, then your mapper or caller, then a comparison with the SAM file of true positions.

Alternatives:

- [wgsim](wgsim.md) is a one-command paired-end simulator with a flat error rate. It is simpler and has no VCF input.
- [DWGSIM](dwgsim.md) writes a VCF of the planted variants and supports Ion Torrent and SOLiD modes.
- [pIRS](pirs.md) fits when the error pattern should follow empirical Illumina quality and base-calling profiles.

## Install it yourself

Conda, pinned to the current Bioconda build (Mason 2.0.13, built from SeqAn 2.5.2). Linux builds exist for x86-64 and aarch64; macOS builds exist for x86-64 and arm64.

```bash
conda create -n mason -c conda-forge -c bioconda mason=2.0.13
conda activate mason
mason_simulator --version
```

The package installs `mason_genome`, `mason_variator`, `mason_materializer`, `mason_simulator`, `mason_methylation`, `mason_splicing` and `mason_frag_sequencing`. SeqAn itself is distributed under the BSD 3-clause licence.

## A first run

Adapted from the Mason Simulator README (https://github.com/seqan/seqan/blob/seqan-v2.5.2/apps/mason2/README.mason_simulator) and the Mason Genome README.

Make a 50 kb random genome with one sequence, then simulate 1000 paired-end reads from it. Writing two read files makes the run paired-end. The `-oa` option writes the true alignments.

```bash
mason_genome -l 50000 -o genome.fa
mason_simulator -ir genome.fa -n 1000 -o reads_1.fq -or reads_2.fq \
  -oa alignments.sam --seed 42
```

To plant variants first, simulate them and pass the VCF to the simulator:

```bash
mason_variator -ir genome.fa -ov variants.vcf
mason_simulator -ir genome.fa -iv variants.vcf -n 1000 \
  -o reads_1.fq -or reads_2.fq -oa alignments.sam
```

## Run the tested example

This recipe builds Mason (SeqAn) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.4 s.

1. Download [mason-recipe.tar.gz](https://biosimhub.pages.dev/guides/mason/mason-recipe.tar.gz) (Dockerfile, run_mason.py, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf mason-recipe.tar.gz
   cd mason
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/mason:2.0.13 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/mason:2.0.13 python /opt/run_mason.py --reference /work/in/reference.fa \
    --pairs 2000 --readlen 100 --frag-mean 300 \
    --frag-sd 30 --mismatch 0.004 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `alignments.sam` | 1.3 MB |
| `reads_1.fq` | 432.5 KB |
| `reads_2.fq` | 432.5 KB |
| `reference.fa` | 19.8 KB |
| `reference.fa.fai` | 27 B |
| `run_log.txt` | 225 B |

<details><summary>First lines of <code>alignments.sam</code></summary>

```
@HD	VN:1.4
@SQ	SN:chr_example	LN:20000
simulated.1	99	chr_example	14434	255	100M	=	14617	283	ATGCGGAACTCGCCTGGCGTAGTTAAAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTA	HIHHHIGFIIGHHHIHFIFHGIIHGIIFCEIAEIICHIIFCIGIE
simulated.1	147	chr_example	14617	255	100M	=	14434	-283	TCTCGACACTTTGCCCAATCACACGAGTAACTTGTAGTAGGGGACGTTCGCCTTTGTCCACTCACTCCTGGGGGAGTGGGAAGATATCCATTTCAACTTG	C0CII0I1FIBI@EII@?IH>I;DIEIIIGECIIIFFIB@FIG
simulated.2	83	chr_example	15564	255	100M	=	15349	315	CTAACTTGACGCCCCATAGGTTCTTGGTCTAGCGGCTACGCCTTCTGAATTGAAATGGATGTCCCATTCAAACAGCCCGGTCGAACAGCTCATATATGTC	GIBIII1IIIID<BIEHADBHIIIIII2IIIFIC>IH<CDGHIII
simulated.2	163	chr_example	15349	255	100M	=	15564	-315	AGCAATGACAATACCCTACTGAGTATCAGTGTAATCTGTGCACCCGTGCACCGGTCGTCTAGAATGAACCTACCTTCGTGAATAAATGATACATGTTCCC	IIIHIHGHIIHIIGHIIDHHGGIGHIIGIIFGIIHIBEDI@IG
simulated.3	83	chr_example	3243	255	100M	=	3079	264	CACGTTCGGCTAGAATGAGCTGCCTTTCCACTAACATCACTCGCCCCATACAATCGTTCACACTGCGCGGGCCCTAGTCGCACTCCTGTAAGACAGTGAT	I:IAB?GIIIIIBI>IIIFIIG>@FGIIFGHIG:IIAIH8GEIFIII
simulated.3	163	chr_example	3079	255	100M	=	3243	-264	ACGGTGTCCAGCCGCCCTCAGTGTATCGTAGGGTAGTGTATTCCAAGTCGTTGACAGACGGGGCGTATACCTGGATTGAGTTGGCTGCGACGAATTTTTA	I
```

</details>

<details><summary>First lines of <code>reads_1.fq</code></summary>

```
@simulated.1/1
ATGCGGAACTCGCCTGGCGTAGTTAAAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTA
+
HIHHHIGFIIGHHHIHFIFHGIIHGIIFCEIAEIICHIIFCIGIEDIFIDIBIIEIICIE>IEI?IIIIAIGIHII:IICFIIIIDI;DAI8IIIIIIIB
@simulated.2/1
GACATATATGAGCTGTTCGACCGGGCTGTTTGAATGGGACATCCATTTCAATTCAGAAGGCGTAGCCGCTAGACCAAGAACCTATGGGGCGTCAAGTTAG
+
IHHHHIHHHIIIHFGIIEGHDFIBIEGIIIIIIIIBEF@IHIIGGIIHIDCEIIEIIIHGDC<HI>CIFIII2IIIIIIHBDAHEIB<DIIII1IIIBIG
@simulated.3/1
ATCACTGTCTTACAGGAGTGCGACTAGGGCCCGCGCAGTGTGAACGATTGTATGGGGCGAGTGATGTTAGTGGAAAGGCAGCTCATTCTAGCCGAACGTG
+
IHIIIHIIHIGIIIIFIHGIIIGIIGFIBIFEIICIIGDDDIGEIBHEI>IIHIIIFIEG8HIAII:GIHGFIIGF@>GIIFIII>IBIIIIIG?BAI:I
```

</details>

<details><summary>First lines of <code>reads_2.fq</code></summary>

```
@simulated.1/2
CAAGTTGAAATGGATATCTTCCCACTCCCCCAGGAGTGAGTGGACAAAGGCGAACGTCCCCTACTACAAGTTACTCGTGTGATTGGGCAAAGTGTCGAGA
+
HIIHIIIHGIIHFIIGIIHGGDHGHFIAEDIHIIIEEEFFIICIIFIIDCIIFCIEIGIF@BIFFIIICEGIIIEID;I>HI?@IIE@IBIF1I0IIC0C
@simulated.2/2
AGCAATGACAATACCCTACTGAGTATCAGTGTAATCTGTGCACCCGTGCACCGGTCGTCTAGAATGAACCTACCTTCGTGAATAAATGATACATGTTCCC
+
IIIHIHGHIIHIIGHIIDHHGGIGHIIGIIFGIIHIBEDI@IGIBDFBIDII9GIEIEHEIIIED?IFI<FIAIBHEEEAIB8IIIIIII'?IIIAI;DG
@simulated.3/2
ACGGTGTCCAGCCGCCCTCAGTGTATCGTAGGGTAGTGTATTCCAAGTCGTTGACAGACGGGGCGTATACCTGGATTGAGTTGGCTGCGACGAATTTTTA
+
IHHHIIIHHIIIHIHIIHGIHIFGIGEDIHFIIIEFIDI>IIIIIDIGDI,IIIGIIIIGD@BIIIIIII@EE>BEIIIIIFIAC@I>IIICI@BDH:C>
```

</details>

<details><summary>First lines of <code>reference.fa</code></summary>

```
>chr_example random 20 kb sequence
GCTAAAGACAATTACATAACATACACGTCAGCACGAAACTTGTTGGCCCAGTGTGAATCGCTTAAGGGTT
AAGTAAGTGTGATGCATACGCCTTTACTTGCTGTGTCCACCCCATCGGACTGGCATTTTTATTACACTCA
GAAACAGAACTCGGGTAATTTTGACAGGTCACGCAGAGGCGCGCCCTCCTGAAGTGCGTGGACACTCGCT
ATGAATCTCTGATTTACCCACTCTGCCAAACTCCAGCGCGGTCAGTTCCATCACCCTAAGTAACCGAATA
ATGCGTTCGCTCTATTGACTACGACGCGCTCATTCCCTTGTCGGAGAGTTATGGAACAAGGACGCTGTCT
GAGACTAGAAGACAGATAGTGCACACGACCGGCGTCGGAGAAACTCTATTTGCCGCCTGACAAGTCAATG
CGATCCGTAGGGGCAGCGCAGTATGCCAAGACTATAGGCACTGTCGCATCACAAACGATTAACTGATAAA
TGAGCCCTTTATGACACGGGCATATGACTGGTTTACGATAGTATGTCCAACGGCGAGCTTTACATTTGCT
GTGAGAGGTACAGGGATTAGTGAGAAGCCGTGCGTATCAATTCGTACCTTGGGGGTCGTTACCACTCTGT
TCCCACGAGCGGCATTTCTGGATGGCCAGCTTTTGACATTTAATTTCACCCATAAACCAGCGTAAAGCTG
CAAGTGGCTCCATGAACTTAGCTGCTAGTGTCAGACTCGCCTCGGATCCTTACTACACTAACTTGAACGC
```

</details>

<details><summary>First lines of <code>reference.fa.fai</code></summary>

```
chr_example	20000	35	70	71
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
mason_simulator -ir reference.fa -n 2000 -o reads_1.fq -or reads_2.fq -oa alignments.sam --illumina-read-length 100 --fragment-mean-size 300 --fragment-size-std-dev 30 --illumina-prob-mismatch 0.004 -
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--pairs` | Read pairs | 2000 | 1 to 1000000 |
| `--readlen` | Read length | 100 | 20 to 250 |
| `--frag-mean` | Mean fragment size | 300 | 50 to 2000 |
| `--frag-sd` | Fragment size standard deviation | 30 | 1 to 500 |
| `--mismatch` | Average per-base mismatch probability | 0.004 | 0 to 0.2 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `reads_1.fq` and `reads_2.fq`: FASTQ files, one record per read, in the same order. Read names start with `simulated.` by default (option `--read-name-prefix`). With `--embed-read-info` the name also carries the read's origin.
- `alignments.sam`: one alignment per read at its true position on the reference, with a CIGAR string that records the simulated insertions and deletions. A mapper's output can be compared with it directly.
- `run_log.txt`: the standard output of `mason_simulator`, with the command line the recipe used.

Illumina reads have a fixed length (default 100). Quality values follow the begin and end means set by `--illumina-quality-mean-begin` and `--illumina-quality-mean-end`.

## Pitfalls

- **The default seed is 0.** Two runs without `--seed` are identical; change the seed to get a new sample.
- **`-n` counts fragments.** With two output files it is the number of read pairs; with one it is the number of reads.
- **Fragments must be longer than the reads.** For 454 or Sanger reads, raise `--fragment-mean-size` as the README example does, or reads are longer than the fragments.
- **Index files.** Mason works with a FASTA index (`.fai`) next to the reference. In a read-only input folder, copy the FASTA somewhere writable first. The recipe does this.
- **Variants apply to the VCF's haplotypes.** Without `-iv`, reads come from the reference, so there are no variants to find.
- **Version numbers differ.** Mason 2.0.13 ships inside SeqAn 2.5.2; the old README header still says 2.0.0-beta1.

## Further reading

- Mason README and tool READMEs: https://github.com/seqan/seqan/tree/seqan-v2.5.2/apps/mason2
- Project page: https://www.seqan.de/apps/mason.html
- Bioconda package: https://anaconda.org/bioconda/mason
- Holtgrewe M (2010). Mason, a read simulator for second generation sequencing data. Technical Report TR-B-10-06, Institut fuer Mathematik und Informatik, Freie Universitaet Berlin.

---

Cite: Holtgrewe M (2010). Mason, a read simulator for second generation sequencing data. Technical Report TR-B-10-06, Institut fuer Mathematik und Informatik, Freie Universitaet Berlin.

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/mason).
