# PBSIM2

> Simulate PacBio and Oxford Nanopore long reads from a reference genome using an HMM model of quality scores.

Licence: GPL-2.0 · [Source code](https://github.com/yukiteruono/pbsim2)

## What it simulates

PBSIM2 turns a reference FASTA into long reads that look like PacBio or Oxford Nanopore output. It draws read lengths from a gamma-type length model, cuts them from random positions on the reference, and adds errors. A hidden Markov model (HMM) trained on real runs sets the quality codes, which sets where the errors fall. You give it a reference, a chemistry model and a depth. It returns a FASTQ, a MAF alignment of each read to the reference, and a copy of the reference.

Key assumptions: read length follows the mean and standard deviation you set, and the mix of substitutions, insertions and deletions follows the ratio you set. The ratio is a global fixed mix. It does not depend on sequence context.

## When to use it

- Test an assembler, mapper or variant caller on long reads with a known truth (the MAF file lists every error).
- Compare how P6C4 (PacBio) and R103 (Nanopore) error profiles change an alignment.
- Plan coverage: set `--depth` and count the reads you get.

Alternatives: [PBSIM3](pbsim3.md) adds multi-pass reads, transcript and template modes and newer ONT models. [SimLoRD](simlord.md) models PacBio errors that fall with the number of passes. [CycSim](cycsim.md) makes errors depend on the surrounding k-mer. Use [wgsim](wgsim.md) or [DWGSIM](dwgsim.md) for short reads.

## Install it yourself

PBSIM2 2.0.1 is on bioconda. The recipe builds it for linux/amd64 only. A dry-run resolve on linux-64 picked build `h9948957_4` (378 kB), so on Apple Silicon run it through emulation.

```
conda create -n pbsim2 -c conda-forge -c bioconda pbsim2=2.0.1
conda activate pbsim2
```

The six HMM models (P4C2, P5C3, P6C4, R94, R95, R103) are in `$CONDA_PREFIX/data`. Minimal command:

```
pbsim --hmm_model $CONDA_PREFIX/data/R103.model --depth 5 reference.fa
```

Defaults from the program's usage text: prefix `sd`, depth 20, mean length 9000, SD 7000, minimum length 100, maximum 1,000,000, mean accuracy 0.85, ratio 6:50:54 (substitution:insertion:deletion), seed taken from the clock.

## Run the tested example

This recipe builds PBSIM2 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s. PBSIM2 has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [pbsim2-recipe.tar.gz](https://biosimhub.pages.dev/guides/pbsim2/pbsim2-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pbsim2-recipe.tar.gz
   cd pbsim2
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/pbsim2:2.0.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pbsim2:2.0.1 pbsim --hmm_model /opt/conda/data/R103.model \
    --difference-ratio 23:31:46 --depth 5 --length-mean 3000 \
    --length-sd 1000 --length-min 100 --accuracy-mean 0.85 \
    --seed 42 --prefix sim /work/in/reference.fa > out/pbsim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `pbsim_log.txt` | 0 B |
| `sim_0001.fastq` | 587.4 KB |
| `sim_0001.maf` | 630.0 KB |
| `sim_0001.ref` | 59.4 KB |

<details><summary>First lines of <code>sim_0001.fastq</code></summary>

```
@S1_1
ACGACAAAATGTTCAAGTAAGGCGTGCAAGGCGTAAGCCCTCACCTGGTTAATAGAGTTAAACGCCAAGGCGCCAATCCGGAGTGCTGCGTTTTCACATAGTTCTCAGTTCACAGGGCAATCAACCCAATCCGTAAGTAAGATGGGTGGGCAGCAAGCGTACCATTACTCCTGCCCATTACACTTAAAGGGCCAACTAAT
```

</details>

<details><summary>First lines of <code>sim_0001.maf</code></summary>

```
a
s ref 53253 3688 + 60000 A-GAGAAAAT-ATTCAAGTAAGGCGGTGCAAGGCGTAAGC-CATACACCTGGTTAATAGAGTTAAACGCCAAGTGCGCCAATCCGGAGTGCTGCGTTCTTCACATAGTTCTCAGTTCCACACC-GCCAATCAACCCAAT-CGTCAAGTAAGCATGAGGTGGGCAGCCAGCCGTAC
```

</details>

<details><summary>First lines of <code>sim_0001.ref</code></summary>

```
>synthetic_ref
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

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `/opt/conda/data/….model` | Quality HMM model (P* are PacBio chemistries, R* are Oxford Nanopore pore versions) | R103 | P4C2, P5C3, P6C4, R94, R95, R103 |
| `--difference-ratio` | Substitution:insertion:deletion ratio (6:50:54 is the PacBio default, 23:31:46 suits Nanopore) | 23:31:46 | 6:50:54, 23:31:46, 10:60:30 |
| `--depth` | Coverage depth | 5 | 0.1 to 50 |
| `--length-mean` | Mean read length | 3000 | 100 to 100000 |
| `--length-sd` | Read length standard deviation | 1000 | 0 to 50000 |
| `--length-min` | Minimum read length | 100 | 10 to 10000 |
| `--accuracy-mean` | Mean read accuracy | 0.85 | 0.6 to 0.99 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example simulates 5x on a 60,000 bp reference with the R103 Nanopore model and ratio 23:31:46. `pbsim_log.txt` is empty because the example saves only stdout. The run summary goes to stderr.

- `sim_0001.fastq` (601,470 bytes): 93 reads, 300,000 bases in total, exactly 5 x 60,000. Mean length is 3,226 bp for a requested mean of 3,000. IDs run `@S1_1`, `@S1_2` and so on.
- `sim_0001.maf` (645,111 bytes): one `a` block per read. The first `s` line is the reference (`ref 53253 3688 + 60000`: start, aligned length, strand, source size). The second is the read (`S1_1 0 3643 + 3643`). Gaps (`-`) mark insertions and deletions.
- `sim_0001.ref`: the input sequence, named `synthetic_ref`.

Counting columns in the MAF gives 319,919 alignment columns with 86.5% identity. Of the errors, 23.1% are substitutions, 30.9% insertions and 46.0% deletions. That matches the 23:31:46 ratio you asked for.

## Your own runs

All runs below use the recipe's image and the example reference with seed 42.

- **PacBio model, deeper.** P6C4, ratio 6:50:54, depth 20, mean length 9000, SD 7000. Result: 138 reads, 1,200,000 bases, mean length 8,696, longest read 41,394. Substitutions fall to 5.4% of errors, insertions 45.3%, deletions 49.3%.
- **Higher accuracy.** Same as the example but `--accuracy-mean 0.95`. Result: 100 reads, identity 96.0% (86.5% before), so the error rate drops from 13.5% to 4.0% of columns.
- **Seeds.** Seed 42 twice gives byte-identical FASTQ files. Seed 7 gives 104 reads with 86.0% identity.

With your own genome, mount the FASTA and keep depth near 20 to start. Multi-FASTA input produces `sim_0001`, `sim_0002` and so on, one set per sequence.

## Pitfalls

- **Ratio defaults suit PacBio.** The default 6:50:54 gives insertion-heavy reads. For Nanopore the authors recommend about 23:31:46. Set it with `--difference-ratio`.
- **Accuracy is a target for the model.** The example asked for 0.85 and got 86.5% identity. Check the MAF before you rely on a number.
- **Length defaults are long.** The default mean is 9,000 with SD 7,000. On a 60 kb reference that gives few, very long reads. Set `--length-mean` and `--length-sd` for your genome.
- **Model path.** `--hmm_model` needs a file path. The models sit under `$CONDA_PREFIX/data`, so pass the full path.
- **Unseeded runs differ.** Without `--seed` the clock is the seed, so two runs give different reads.

## Further reading

- Source and usage: https://github.com/yukiteruono/pbsim2
- Ono Y, Asai K, Hamada M (2021). PBSIM2. Bioinformatics 37:589-595. https://doi.org/10.1093/bioinformatics/btaa835

---

Cite: Ono Y, Asai K, Hamada M (2021). PBSIM2. Bioinformatics 37:589-595. doi:10.1093/bioinformatics/btaa835

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pbsim2).
