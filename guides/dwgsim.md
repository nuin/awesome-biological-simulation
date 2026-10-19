# DWGSIM

> Simulate paired-end Illumina-like reads from a reference genome, with SNPs, indels, and sequencing errors.

Licence: GPL-2.0-or-later · [Source code](https://github.com/nh13/DWGSIM)

## What it simulates

DWGSIM simulates paired-end reads from a reference FASTA. It plants random SNPs and indels in a diploid copy of the reference. It then samples read pairs from the two haplotypes and adds substitution errors.

The inputs are a FASTA file and a read count. The outputs are FASTQ files, a mutation list in text form and the same mutations as a VCF. Each read name records where the read came from and how many errors and variants it carries.

Key assumptions:

- The genome is diploid unless you pass `-H`. Each mutation sits on strand 1, strand 2 or both.
- Errors are substitutions with a per-base rate that may ramp along the read. Quality values vary around a mean with a standard deviation of 2 (`-Q`).
- 5% of read pairs are random DNA unrelated to the reference (`-y 0.05`).
- Fragment lengths follow a normal distribution around the outer distance.

## When to use it

Use DWGSIM when you need a truth set. The VCF lists every planted variant with its phase, so you can score a variant caller or check mapper accuracy. It also simulates SOLiD and Ion Torrent reads.

[wgsim](wgsim.md) on biosimhub has the same read model with a simpler output and constant quality. Pick wgsim when you only need reads. [pIRS](pirs.md) fits better when you need empirical Illumina quality and indel error profiles. [InSilicoSeq](insilicoseq.md) fits better when the input is a mix of genomes.

## Install it yourself

The Bioconda package is `dwgsim` 1.1.14. The program prints its version as 0.1.14.

```bash
conda create -n dwgsim -c conda-forge -c bioconda dwgsim=1.1.14
conda activate dwgsim
```

A micromamba 2.0.5 dry run of `bioconda::dwgsim=1.1.14` resolves.

The minimal command takes a FASTA and an output prefix:

```bash
dwgsim -N 10000 -1 70 -2 70 -e 0.02 -E 0.02 -d 500 -s 50 -r 0.001 -R 0.1 -z 42 \
  reference.fa sim
```

- `-N` sets the number of read pairs. Use `-C` for a mean coverage instead.
- `-1` and `-2` set the read lengths. The default is 70.
- `-e` and `-E` set the error rate of read 1 and read 2. A value such as `0.01-0.1` ramps from 1% at the read start to 10% at the end.
- `-d` is the outer distance between the ends. `-i` switches it to the inner distance.
- `-s` is the standard deviation of that distance.
- `-r` is the mutation rate. `-R` is the fraction that are indels. `-X` is the indel extension probability (default 0.30).
- `-y` is the fraction of random reads (default 0.05).
- `-H` makes the genome haploid.
- `-z` sets the seed. The default of -1 uses the clock.

## Run the tested example

This recipe builds DWGSIM in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.9 s.

1. Download [dwgsim-recipe.tar.gz](https://biosimhub.pages.dev/guides/dwgsim/dwgsim-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf dwgsim-recipe.tar.gz
   cd dwgsim
   sh run.sh
   ```

![Terminal recording of the DWGSIM example run](https://biosimhub.pages.dev/media/dwgsim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/dwgsim:1.1.14 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/dwgsim:1.1.14 dwgsim -N 10000 -1 70 -2 70 -e 0.02 -E 0.02 \
    -d 500 -s 50 -r 0.001 -R 0.1 -z 42 /work/in/reference.fa sim > out/dwgsim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `dwgsim_log.txt` | 0 B |
| `sim.bfast.fastq.gz` | 1.2 MB |
| `sim.bwa.read1.fastq.gz` | 668.8 KB |
| `sim.bwa.read2.fastq.gz` | 669.2 KB |
| `sim.mutations.txt` | 332 B |
| `sim.mutations.vcf` | 1.2 KB |

<details><summary>First lines of <code>sim.mutations.txt</code></summary>

```
chr_example	1356	C	M	1
chr_example	4918	T	W	2
chr_example	5813	T	Y	1
chr_example	9527	A	C	3
chr_example	10106	T	Y	2
chr_example	11234	A	M	1
chr_example	11521	A	R	2
chr_example	13821	T	-	1
chr_example	15797	A	T	3
chr_example	17154	C	S	1
chr_example	17670	G	R	1
chr_example	18602	G	S	1
```

</details>

<details><summary>First lines of <code>sim.mutations.vcf</code></summary>

```
##fileformat=VCFv4.1
##contig=<ID=chr_example,length=20000>
##INFO=<ID=AF,Number=A,Type=Float,Description="Allele Frequency">
##INFO=<ID=pl,Number=1,Type=Integer,Description="Phasing: 1 - HET contig 1, #2 - HET contig #2, 3 - HOM both contigs">
##INFO=<ID=mt,Number=1,Type=String,Description="Variant Type: SUBSTITUTE/INSERT/DELETE">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
chr_example	1356	.	C	A	100	PASS	AF=0.5;pl=1;mt=SUBSTITUTE
chr_example	4918	.	T	A	100	PASS	AF=0.5;pl=2;mt=SUBSTITUTE
chr_example	5813	.	T	C	100	PASS	AF=0.5;pl=1;mt=SUBSTITUTE
chr_example	9527	.	A	C	100	PASS	AF=1.0;pl=3;mt=SUBSTITUTE
chr_example	10106	.	T	C	100	PASS	AF=0.5;pl=2;mt=SUBSTITUTE
chr_example	11234	.	A	C	100	PASS	AF=0.5;pl=1;mt=SUBSTITUTE
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-N` | Read pairs | 10000 | 1 to 2000000 |
| `-1` | Length of read 1 | 70 | 20 to 500 |
| `-2` | Length of read 2 | 70 | 20 to 500 |
| `-e` | Error rate of read 1 | 0.02 | 0 to 0.5 |
| `-E` | Error rate of read 2 | 0.02 | 0 to 0.5 |
| `-d` | Outer distance between reads | 500 | 0 to 100000 |
| `-s` | Standard deviation of the distance | 50 | 0 to 10000 |
| `-r` | Mutation rate | 0.001 | 0 to 0.5 |
| `-R` | Fraction of mutations that are indels | 0.1 | 0 to 1 |
| `-z` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The reference is one 20,000 bp sequence. The run writes 10,000 pairs of 70 bp.

`sim.bwa.read1.fastq.gz` (684,881 bytes) and `sim.bwa.read2.fastq.gz` (685,275 bytes) hold read 1 and read 2 in matching order, for tools such as BWA. `sim.bfast.fastq.gz` (1,278,133 bytes) holds both reads interleaved. The recipe leaves it out of the listed outputs, but the program writes it.

A read name looks like this:

```
@chr_example_2742_3080_0_1_0_0_1:0:0_1:0:0_0/1
```

The fields are contig, start of read 1, start of read 2, strand of each read, a random flag for each read, then errors, SNPs and indels for read 1 and for read 2, then a read number. This pair has 1 error in each read and no variants. The DWGSIM documentation lists all 14 fields.

`sim.mutations.txt` has 14 lines and 332 bytes. The columns are contig, position, reference base, new base and strand. Strand 1 or 2 is heterozygous and 3 is homozygous. This run has 7 on strand 1, 5 on strand 2 and 2 homozygous. Heterozygous SNPs use IUPAC codes, so `C M` is a C that is C or A. Each deleted base gets its own line with `-` as the new base.

`sim.mutations.vcf` (1,192 bytes) holds the same 14 variants: 13 substitutions and 1 deletion (`AT` to `A` at 13820). The `pl` tag gives the phase (1, 2 or 3) and `AF` is 0.5 for heterozygous and 1.0 for homozygous sites.

`dwgsim_log.txt` is empty in the recipe, because DWGSIM writes its messages to standard error. Add `2>&1` when you run it yourself. The messages report the contig length (20,000) and the progress of the 10,000 pairs.

Counting the read 1 names gives 468 random reads out of 10,000, which matches the 5% default. Read 1 carries 13,350 errors, which is 1.33 per read. The nominal 70 bp times 2% is 1.4, and the gap comes from the random reads.

## Your own runs

These runs used the recipe's image and reference. Compare each with the baseline above.

**No random reads and a low error rate.** Add `-y 0` and set `-e 0.005 -E 0.005`. Random reads drop from 468 to 0. Read 1 errors drop from 13,350 to 3,497, which is 0.35 per read and matches 70 bp times 0.5%.

**Haploid genome.** Add `-H`. The run still plants 14 mutations, and every one has strand value 3 in `sim.mutations.txt`. The first VCF lines carry `AF=1.0` and `pl=3`.

**A mutation-rich genome.** Set `-r 0.005`. The mutation list grows from 14 to 96 lines. The read 1 names report 1,832 SNP overlaps and 466 indel overlaps, against 257 and 24 in the baseline.

To use your own genome, replace `reference.fa`.

## Pitfalls

- The default seed is the clock. Pass `-z` to repeat a run.
- 5% of pairs are random DNA unless you pass `-y 0`. A mapper evaluation will show 5% unmapped pairs that are correct behavior.
- Both `-N` and `-C` exist. The default `-C` is 100 and `-N` is -1, so give one of them on purpose. The example sets `-N`.
- `-d` is the outer distance. With 70 bp reads and `-d 500` the inner gap is 360 bp. Add `-i` if you prefer to give the inner distance.
- The longest insertion is 255 bp, per the documentation.
- The log file is empty without `2>&1`.

## Further reading

- DWGSIM documentation on simulating reads: https://github.com/nh13/DWGSIM/blob/main/docs/03_Simulating_Reads.md
- DWGSIM repository: https://github.com/nh13/DWGSIM

---

Cite: Homer N. DWGSIM, https://github.com/nh13/DWGSIM

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/dwgsim).
