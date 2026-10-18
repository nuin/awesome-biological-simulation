# wgsim

> Simulate paired-end Illumina-like reads from a reference genome, with sequencing errors, SNPs and small indels.

Licence: MIT · [Source code](https://github.com/lh3/wgsim)

## What it simulates

wgsim simulates paired-end short reads from a reference FASTA. It first adds random SNPs and indels to the reference. It then cuts read pairs from the mutated sequence and adds substitution errors.

The inputs are a FASTA file, a read-pair count and a few rates. The outputs are two FASTQ files and a list of the mutations it planted. It writes the true read coordinates and the number of errors into each read name.

Key assumptions:

- Every position has the same error rate. Errors never create indels.
- Every base gets the same quality character, so quality scores carry no information.
- The genome is diploid by default. Each mutation lands on one or both haplotypes by chance.
- Fragment lengths follow a normal distribution around the outer distance.

## When to use it

Use wgsim when you need reads with a known truth and speed matters more than realism. Typical questions:

- Does my mapper place reads correctly at 1% error?
- Does my SNP caller find the planted variants at 30x?
- Does my pipeline run end to end on a small input?

[DWGSIM](dwgsim.md) on biosimhub adds a VCF of the planted variants, a per-read error rate range and Ion Torrent and SOLiD modes. Use it when you need a truth VCF. [pIRS](pirs.md) fits better when the error pattern matters, because it uses empirical quality and base-calling profiles. [InSilicoSeq](insilicoseq.md) fits better for metagenomes.

## Install it yourself

The Bioconda package is `wgsim` 1.0. The program reports itself as version 0.3.1-r13.

```bash
conda create -n wgsim -c conda-forge -c bioconda wgsim=1.0
conda activate wgsim
```

A micromamba 2.0.5 dry run of this command resolves. To build from source, the README gives `gcc -g -O2 -Wall -o wgsim wgsim.c -lz -lm`.

The minimal command writes reads to two files and the mutation list to standard output:

```bash
wgsim -N 10000 -1 100 -2 100 -e 0.01 -d 500 -s 50 -r 0.001 -R 0.15 -S 42 \
  reference.fa reads_1.fq reads_2.fq > mutations.txt
```

- `-N` sets the number of read pairs. The default is 1,000,000.
- `-1` and `-2` set the read lengths. The default is 70.
- `-e` sets the base error rate. The default is 0.02.
- `-d` sets the outer distance between the two read ends, including both reads. The default is 500.
- `-s` sets the standard deviation of that distance. The default is 50.
- `-r` sets the mutation rate. The default is 0.001.
- `-R` sets the fraction of mutations that are indels. The default is 0.15.
- `-X` sets the probability that an indel is extended by one base. The default is 0.30.
- `-S` sets the seed.
- `-h` switches to haplotype mode. With the example settings it gives 14 mutations, all flagged homozygous.

## Run the tested example

This recipe builds wgsim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s.

1. Download [wgsim-recipe.tar.gz](https://biosimhub.pages.dev/guides/wgsim/wgsim-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf wgsim-recipe.tar.gz
   cd wgsim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/wgsim:1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/wgsim:1.0 wgsim -N 10000 -1 100 -2 100 -e 0.01 -d 500 \
    -s 50 -r 0.001 -R 0.15 -S 42 /work/in/reference.fa reads_1.fq reads_2.fq > out/mutations.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `mutations.txt` | 332 B |
| `reads_1.fq` | 2.4 MB |
| `reads_2.fq` | 2.4 MB |

<details><summary>First lines of <code>mutations.txt</code></summary>

```
chr_example	1356	C	M	+
chr_example	4918	T	W	+
chr_example	5813	-	T	-
chr_example	9526	T	A	-
chr_example	10105	T	Y	+
chr_example	11233	A	M	+
chr_example	11520	A	R	+
chr_example	13820	A	-	-
chr_example	15796	T	G	-
chr_example	17153	C	S	+
chr_example	17669	T	-	-
chr_example	18600	C	M	+
```

</details>

<details><summary>First lines of <code>reads_1.fq</code></summary>

```
@chr_example_10173_10627_2:0:0_0:0:0_0/1
TAGTGCAGACATTGCGCAAGTAGTTAGGGTAGGGCCGCGCGAAGCCTTGCGGCCCTAAACACGACTGTTGACCCGTCGAGCGTGTGCAGTTCAACATGAG
+
5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555
@chr_example_7601_8080_1:0:0_0:0:0_1/1
GATGGTATGGTGTAGCTCATATACATCATTGGGTGCGAGAGTTCGGTTCCACTGCAGAGACCCCGGTAGACGTGGTCCCCTATTTCACTAAATTCGAGGG
+
5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555
@chr_example_12995_13437_0:0:0_3:0:0_2/1
AGAGCTAGCTGCCTTTGGGTACAATCGAAATTTCTTACATGAAGGCGAGCCAGTTCCACTTCTGGCGCGACCGAAGCGAATTTAGCCCGAGTACGCTGGC
+
5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555
```

</details>

<details><summary>First lines of <code>reads_2.fq</code></summary>

```
@chr_example_10173_10627_2:0:0_0:0:0_0/2
ACGCGGACTCGGCAACTGGCATGTCTGAATGTCTAGCTAGAAAATCTGGTAATGGTCTATGGATTCATCCGCGCTATCCTCCAGGTTGGGGTGAGACTAG
+
5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555
@chr_example_7601_8080_1:0:0_0:0:0_1/2
GACGAGGATCTACCCACAAACGGCAAGCACCTAAACCAAAGGTTGTACATAGTTTTCAGTACAGGTAAGAGCACTTCGGGCGGCGAAAGGTGGCTGCATA
+
5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555
@chr_example_12995_13437_0:0:0_3:0:0_2/2
TGGCTATATCCAATCCGAGTCAAGATCAACTCGAGCATGAGCTAACTCAGGAGTAAATGCAATGTCAAATGCCAATTCGTGGGAGGCATTCGTCCTACAT
+
5555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555555
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-N` | Read pairs | 10000 | 1 to 5000000 |
| `-1` | Length of read 1 | 100 | 20 to 1000 |
| `-2` | Length of read 2 | 100 | 20 to 1000 |
| `-e` | Base error rate | 0.01 | 0 to 0.5 |
| `-d` | Outer distance between reads | 500 | 0 to 100000 |
| `-s` | Standard deviation of the distance | 50 | 0 to 10000 |
| `-r` | Mutation rate | 0.001 | 0 to 0.5 |
| `-R` | Fraction of mutations that are indels | 0.15 | 0 to 1 |
| `-S` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The reference is one 20,000 bp sequence called `chr_example`. The run makes 10,000 pairs of 100 bp, which is 2 Mb of reads and about 100x coverage.

`mutations.txt` has 14 lines and 332 bytes. Each line has five columns: contig, position, reference base, new base and a flag. The flag `-` marks a homozygous change and `+` marks a heterozygous one. Heterozygous SNPs use IUPAC codes, so `C M` means the site is C on one haplotype and A on the other. In this run 5 mutations are homozygous and 9 are heterozygous. Of the 14, 11 are SNPs and 3 are indels (one insertion and two deletions). The expected count at `-r 0.001` is 20, so 14 is a normal draw for a small genome.

`reads_1.fq` and `reads_2.fq` each hold 10,000 records and are 2,464,679 bytes. A read name looks like this:

```
@chr_example_10173_10627_2:0:0_0:0:0_0/1
```

The fields are contig, start, end, then errors, SNPs and indels for read 1, then the same three counts for read 2, then a hex read number. This pair spans 10173 to 10627, so its outer distance is 455 bp. Read 1 carries 2 errors. Reading all 10,000 names gives a mean outer distance of 500.3 bp with a standard deviation of 50.3, which matches `-d 500 -s 50`. Read 1 has 10,015 errors in total, which is 1.00 per 100 bp read and matches `-e 0.01`.

Every quality string is `5` repeated 100 times. Phred 20 plus the 33 offset is the character `5`. The source computes it from the error rate, so the quality never varies along a read.

Each error replaces a base with the next one in the order A, C, G, T. The source applies `(c + 1) & 3`, so A becomes C, C becomes G, G becomes T and T becomes A.

## Your own runs

These runs use the example's reference and settings. Change one value at a time and compare with the baseline above.

**No sequencing errors.** Set `-e 0`. Read 1 error count falls from 10,015 to 0. The quality character changes from `5` to `I`. The mutation list is identical because the seed and mutation rate are the same.

**A mutation-rich genome.** Set `-r 0.01 -R 0.5`. The mutation list grows from 14 to 209 lines, with 106 homozygous and 103 heterozygous. The read 1 names report 3,929 SNP overlaps and 4,289 indel overlaps in total, against 320 and 110 in the baseline.

**A shorter library.** Set `-d 300 -s 30`. The measured outer distance becomes 300.2 bp with a standard deviation of 30.2.

**Another seed.** Set `-S 7`. The mutation list has 26 lines (9 homozygous, 17 heterozygous) against 14 for seed 42. Run several seeds when a result depends on which sites got mutated.

To use your own genome, replace `reference.fa`. Sequences shorter than `-d` plus three standard deviations are skipped, with a message on standard error.

## Pitfalls

- The default seed is the clock. Without `-S` two runs differ. Always set `-S` and record it.
- `-d` is the outer distance, which includes both reads. With 100 bp reads and `-d 500`, the gap between the reads is 300 bp. Use `-d` of at least twice the read length to avoid overlap.
- The mutation list goes to standard output and the log goes to standard error. Forget the `>` redirect and the list scrolls past in the terminal.
- Quality scores are constant. Quality-aware tools such as base recalibration or quality trimming see no signal. Use pIRS or DWGSIM when quality matters.
- The mutation count is random. At `-r 0.001` on 20 kb the expectation is 20, and seeds 42 and 7 gave 14 and 26. Compare a caller against the planted list in `mutations.txt` and not against the rate.

## Further reading

- wgsim repository and README: https://github.com/lh3/wgsim
- wgsim source (`wgsim.c`), which defines the error model and the read name format: https://github.com/lh3/wgsim/blob/master/wgsim.c

---

Cite: Li H. wgsim, https://github.com/lh3/wgsim

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/wgsim).
