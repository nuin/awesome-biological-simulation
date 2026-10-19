# pIRS

> Simulate paired-end Illumina reads from a reference FASTA using empirical base-calling, indel and GC-bias profiles.

Licence: GPL-2.0-or-later · [Source code](https://github.com/galaxy001/pirs)

## What it simulates

pIRS (profile-based Illumina paired-end reads simulator) simulates Illumina reads from a reference FASTA. It cuts fragments with a normal length distribution, then adds errors drawn from profiles measured on real sequencing data.

The inputs are a FASTA file, a read length, a coverage and an insert length. The outputs are two FASTQ files plus logs of every read, the insert lengths and the error positions.

Three empirical profiles shape the reads:

- A base-calling profile gives substitution errors and quality scores for each cycle. The bundled profile is `humNew.PE100`, built from human data with 100 bp reads.
- An indel profile gives sequencing-error insertions and deletions. The bundled one comes from PhiX.
- A GC-bias profile lowers the coverage of fragments with extreme GC content.

## When to use it

Use pIRS when error and quality patterns must look like real Illumina data. Typical questions:

- Does my trimming or error-correction step work on position-dependent errors?
- How does GC bias change coverage in my target?
- Does my pipeline cope with realistic quality strings?

[wgsim](wgsim.md) and [DWGSIM](dwgsim.md) use a flat error rate and plant variants for you. Use them when you need a truth set of SNPs. [InSilicoSeq](insilicoseq.md) fits better when the input is several genomes at different abundances. pIRS has a separate `pirs diploid` command to make a variant copy of a genome, and that command is not part of the example.

## Install it yourself

The Bioconda package is `pirs` 2.0.2. The recipe builds for `linux/amd64` only, so on an ARM machine it runs under emulation.

```bash
conda create -n pirs -c conda-forge -c bioconda pirs=2.0.2
conda activate pirs
```

The minimal command takes a FASTA file and an output prefix:

```bash
pirs simulate -l 100 -x 5 -m 180 -v 18 -S 42 --threads=1 -o sim reference.fa
```

- `-l` sets the read length. The bundled profile covers up to 100 bp.
- `-x` sets the average coverage.
- `-m` sets the mean insert length. The default is 180.
- `-v` sets the insert standard deviation. The default is 10% of the mean.
- `-S` sets the seed.
- `--threads=1` keeps the run reproducible. With more threads each thread uses its own generator.
- `-o` sets the output prefix.
- `-e` sets a substitution error rate. Without it the profile's own rate applies.
- `--no-gc-bias`, `--no-indels` and `--no-subst-errors` switch the three models off.
- `-d` marks a diploid input and halves the coverage, so give the two sequences from `pirs diploid`.

## Run the tested example

This recipe builds pIRS in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.6 s. pIRS has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [pirs-recipe.tar.gz](https://biosimhub.pages.dev/guides/pirs/pirs-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pirs-recipe.tar.gz
   cd pirs
   sh run.sh
   ```

![Terminal recording of the pIRS example run](https://biosimhub.pages.dev/media/pirs/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/pirs:2.0.2 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pirs:2.0.2 pirs simulate -l 100 -x 5 -m 180 -v 18 -S 42 \
    --threads=1 -o /work/out/sim /work/in/reference.fa > out/pirs_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `pirs_log.txt` | 4.5 KB |
| `sim_100_180.error_rate.distr` | 2.8 KB |
| `sim_100_180.insert_len.distr` | 1013 B |
| `sim_100_180.read.info` | 72.8 KB |
| `sim_100_180_1.fq` | 107.3 KB |
| `sim_100_180_2.fq` | 107.3 KB |

<details><summary>First lines of <code>pirs_log.txt</code></summary>

```
[pIRS] Program:        pirs (Profile-based Illumina pair-end Reads Simulator)
[pIRS] Version:        2.0.0
[pIRS] Author:         Jianying Yuan (BGI-Shenzhen)
[pIRS] Contact:        yuanjianying@genomics.org.cn
[pIRS] Compile Date:   Feb 22 2022 time: 04:10:07
[pIRS] Current time:   Mon Oct 12 06:07:27 2026
[pIRS] Command line:   pirs simulate -l 100 -x 5 -m 180 -v 18 -S 42 --threads=1 -o /work/out/sim /work/in/reference.fa
[pIRS] 
[pIRS] Loading base-calling profile /opt/conda/share/pirs/Base-Calling_Profiles/humNew.PE100.matrix.gz
[pIRS] Loaded base-calling profile header:
[pIRS]    num_ref_bases      = 4
[pIRS]    num_cycles         = 200
```

</details>

<details><summary>First lines of <code>sim_100_180.error_rate.distr</code></summary>

```
# File "/work/out/sim_100_180.error_rate.distr": generated at Mon Oct 12 06:07:27 2026 by the command:
#     pirs simulate -l 100 -x 5 -m 180 -v 18 -S 42 --threads=1 -o /work/out/sim /work/in/reference.fa
#
# This file shows the error position distribution of the simulated reads.
# The cycle number indicates the position in the two reads.  The frequency
# and average rate of errors in each position is provided.
#
# The total number of read pairs that were simulated was 500.
# Each read was 100 base pairs long, so there were 200 cycles.
# Substitution errors were simulated using the quality transition mode algorithm,
# using the default error rate of the base-calling profile:
# "/opt/conda/share/pirs/Base-Calling_Profiles/humNew.PE100.matrix.gz"
```

</details>

<details><summary>First lines of <code>sim_100_180.insert_len.distr</code></summary>

```
# File "/work/out/sim_100_180.insert_len.distr": generated at Mon Oct 12 06:07:27 2026 by the command:
#     pirs simulate -l 100 -x 5 -m 180 -v 18 -S 42 --threads=1 -o /work/out/sim /work/in/reference.fa
#
# This file shows the length distribution of the simulated inserts.
# We were trying to simulate inserts with a mean length of 180 and a
# standard deviation of 18.  The actual mean is 180.384, and the actual
# standard deviation is 18.5168.
#
# insert_len	frequency
127	1
131	1
132	1
```

</details>

<details><summary>First lines of <code>sim_100_180.read.info</code></summary>

```
# File "/work/out/sim_100_180.read.info": generated at Mon Oct 12 06:07:27 2026 by the command:
#     pirs simulate -l 100 -x 5 -m 180 -v 18 -S 42 --threads=1 -o /work/out/sim /work/in/reference.fa
# 
# This file is a log of every read that was simulated.  It shows
# exactly where each read came from and the substitution errors,
# insertions, and deletions (if any) that were made to it.
#
# The following lists the parameters of the simulation:
#
# Input reference sequence files:   /work/in/reference.fa
# Read length:                      100
# Insert length mean:               180
```

</details>

<details><summary>First lines of <code>sim_100_180_1.fq</code></summary>

```
@read_180_1/1
TACAATGATTATGTCCTTCCGTTTCACACCTCCATACCAATGTGGCAAGTCGACACTTAATCGGCCCTTTTGACTGCTCAGATTACATTTACCATTAACT
+
FHHHHHGHHHEFFHHHHHHHGHHHHHHHHHHHHHHHHHHHHH=<BBEFHHFGGGHHHEHFHHHFCHHHHEHFFHHHHHHHHHED?CCDEGCEFCED56GF
@read_180_2/1
TATCTATATAAGCAGGGGAGGGGAAACATTTGTTCTCGGCCGGTGACTCCTAATGCTAAGACATTTCCCTTCAGGGGGGGCTCCCCCGCGATGCCATAAA
+
EEFFC@9BBFEEHHHHHHDCDEEG>8?<=DE=AGGE;+'5@EDHHHHHHEDDHC@@CC773EFBFHHDDCFHB<CFGHEGHHFECFFHHFFFFHHHHGHH
@read_180_3/1
GTGCCGAGTATTTTTCTTTGGACATTGCCGGATGGACATTTCAGCAGTTCTCTGAGGGGTCCGACTGTTAGAATTGCCTCACGTGAAGCTACAGCGCTCA
+
DB@GHHHEDHHGD?@EFGHFHHCDBFHGBGHHHFHFEHHHHHFHFACDHHHHHGEHHHHHHHC>@CA@>E.<B:.9D;<@=CE@?6@A?EFHHHC?=.<<
```

</details>

<details><summary>First lines of <code>sim_100_180_2.fq</code></summary>

```
@read_180_1/2
AGAAGCTCTTTGCACCAAGATCTAATTAGCGATTCAGTTACTGATACACGATTGAAAGTAAGTTAATGGTAAATGTAATCTGAGCAGTCAACAGGGCCGA
+
HHHHHHHHHHEGGDEB@BAABFFHGE@BEBHHHHHHHGHHHBFF7188;A>>4++>4?9>>=;69>36HHHFGE8DCDHFA@AHHCCD:</%/63<7CEE
@read_180_2/2
GAGGTATCATGCGAATTGGCCGGCTAGTTGGACATTAGATGAAGCTAACCTACCACAGTGATATAATGTCGCACTGTCGTGCCTGCTTCAGCTGGTTGCT
+
HEGDHHHHHE>:>;BGE79/:6;;<E88A?GGHHHHHDFHHFHHHHHHHHGHHHHHHHDGH@598CHHD?EEBCCEFGGHF?<BEGEDFFDCCE>DFDFE
@read_180_3/2
GAACGACCGGGCTCCCTCCTCCTCGGCGCAGGTCAAACCCTCAGGAAGCCGTTGTCCTAGTTGGCTAATTCTTCCACTCTGAGCGCTGTAGCTTCACGTG
+
HHHHHGHHHHFFBEHGHHHHHE@FHHHFFFHHHHHFHHHHHFHHGGGCFFHEHHHFFHHB>CHEBFFFFHEEE@FGD>?HHHHHFFHGHHFFHFGBHHE9
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-l` | Read length (The bundled base-calling profile covers reads up to 100 bp.) | 100 | 20 to 100 |
| `-x` | Average coverage | 5 | 0.1 to 50 |
| `-m` | Mean insert length | 180 | 100 to 1000 |
| `-v` | Insert length standard deviation | 18 | 1 to 200 |
| `-S` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The reference is one 20,000 bp sequence called `synthetic_ref`. The run asks for 5x coverage with 100 bp reads. That gives 20,000 times 5 divided by 200 bases per pair, or 500 read pairs.

`sim_100_180_1.fq` and `sim_100_180_2.fq` each hold 500 records and are 109,892 bytes. The names in the file encode the mean insert, so `sim_100_180` means reads of 100 bp and an insert of 180 bp. Read names look like `@read_180_1/1`. Quality characters use the Phred+33 offset and vary along each read, from `H` (Phred 39) down to `5` and below.

`pirs_log.txt` (4,577 bytes in the example) reports what was loaded and what happened:

- The base-calling profile has 4 reference bases, 200 cycles and 41 quality scores.
- The GC-bias profile `humNew.gcdep_200.dat` was chosen for this insert length. Its relative abundance is 0.78 at 20% GC, 0.97 at 30% GC and 0.06 at 80% GC.
- 500 of 500 read pairs were simulated, with 360 substitution errors, an average rate of 0.360%.
- There were 3 deletions and no insertions.
- 21.14% of fragments were affected by GC bias.

`sim_100_180.insert_len.distr` shows the realized insert lengths. The target was 180 with a standard deviation of 18. The actual mean was 180.384 and the actual standard deviation was 18.5168.

`sim_100_180.read.info` (74,531 bytes) has one line per read. The columns are read ID, reference file, contig, position, orientation, insert size, masked end length, substitutions, insertions and deletions. The line `read_180_1/2 ... 18912 - 160 0 92,A->C;` says read 2 of the first pair lies on the minus strand at position 18912, comes from a 160 bp insert and carries the substitution `92,A->C`. This file is the truth for scoring a mapper.

`sim_100_180.error_rate.distr` lists the error frequency and rate for each of the 200 cycles. The first 10 cycles of the example have no errors.

The log prints pIRS version 2.0.0 although the package is 2.0.2.

## Your own runs

These runs used the recipe's image and the example reference. Compare each with the baseline above.

- **Higher coverage.** Set `-x 20`. The run makes 2,000 pairs and the FASTQ files grow from 109,892 to 440,893 bytes. The average substitution error rate is 0.384% and the realized insert mean is 179.468.

- **Longer inserts.** Set `-m 400 -v 40`. The realized insert mean is 399.468. The log still loads `humNew.gcdep_200.dat`, so the GC profile did not change at this insert length. The FASTQ names become `sim_100_400_1.fq`.

- **Your own error rate.** Add `-e 0.01`. The average substitution error rate in the log becomes 1.247% against the 1.0% requested. The documentation warns that the realized rate can be off by 20% or more.

## Pitfalls

- The bundled base-calling profile covers reads up to 100 bp. The recipe limits `-l` to 100.
- The realized error rate differs from `-e`. Read the final rate in `pirs_log.txt` and adjust.
- Several threads make a run non-reproducible. Use `--threads=1` with `-S`.
- Coverage is for a haploid genome. For a diploid input pass `-d`, or you get twice the reads you wanted.
- Output names carry the read length and insert, as in `sim_100_180_1.fq`. Match them with `sim_*_1.fq`.

## Further reading

- pIRS README, with all options: https://github.com/galaxy001/pirs
- Hu X et al. (2012). pIRS: profile-based Illumina pair-end reads simulator. Bioinformatics 28:1533-1535. https://doi.org/10.1093/bioinformatics/bts187

---

Cite: Hu X, Yuan J, Shi Y, Lu J, Liu B, Li Z, Chen Y, Mu D, Zhang H, Li N, Yue Z, Bai F, Li H, Fan W (2012). pIRS, profile-based Illumina pair-end reads simulator. Bioinformatics 28:1533-1535. doi:10.1093/bioinformatics/bts187

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pirs).
