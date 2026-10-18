# PBSIM3

> Simulate Oxford Nanopore and PacBio RS II (CLR) long reads from a reference genome using built-in quality-score HMM error models.

Licence: GPL-2.0-only · [Source code](https://github.com/yukiteruono/pbsim3)

## What it simulates

PBSIM3 simulates PacBio and Oxford Nanopore reads from a genome, a transcript list or a set of templates. The example uses whole-genome mode with a quality-score HMM. The HMM is trained on real reads and ties each base's quality code to its chance of being an error. You give a genome, a model, a depth and length settings. It returns a gzipped FASTQ, a gzipped MAF alignment and a copy of the reference.

Key assumptions: read lengths follow a distribution set by mean and standard deviation, and the substitution:insertion:deletion mix follows `--difference-ratio`. The default ratio, 6:55:39, is for PacBio RS II.

## When to use it

- Generate ONT or RS II reads with a truth alignment to benchmark mappers and assemblers.
- Simulate multi-pass (circular consensus style) reads with `--pass-num`.
- Simulate transcriptome (`--strategy trans`) or template (`--strategy templ`) reads.

Alternatives: [PBSIM2](pbsim2.md) has more chemistry models (P4C2, P5C3, P6C4, R94, R95, R103). [SimLoRD](simlord.md) models PacBio errors that fall as passes rise. [CycSim](cycsim.md) ties errors to the local k-mer.

## Install it yourself

PBSIM3 3.0.5 is on bioconda. A dry-run resolve on linux-aarch64 picked build `h163da20_2` (8 MB download).

```
conda create -n pbsim3 -c conda-forge -c bioconda pbsim3=3.0.5
conda activate pbsim3
```

Models sit in `$CONDA_PREFIX/data`: QSHMM-ONT, QSHMM-ONT-HQ and QSHMM-RSII (quality-score), plus ERRHMM models for RS II, Sequel and ONT. Minimal command:

```
pbsim --strategy wgs --method qshmm --qshmm $CONDA_PREFIX/data/QSHMM-ONT.model --depth 5 --genome reference.fa
```

Defaults from the usage text: prefix `sd`, depth 20, mean length 9000, SD 7000, mean accuracy 0.85, one pass.

## Run the tested example

This recipe builds PBSIM3 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.3 s.

1. Download [pbsim3-recipe.tar.gz](https://biosimhub.pages.dev/guides/pbsim3/pbsim3-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pbsim3-recipe.tar.gz
   cd pbsim3
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pbsim3:3.0.5 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pbsim3:3.0.5 pbsim --strategy wgs --method qshmm --qshmm /opt/conda/data/QSHMM-ONT.model \
    --depth 5 --length-mean 3000 --length-sd 1000 \
    --accuracy-mean 0.85 --seed 42 --genome /work/in/reference.fa \
    --prefix sim
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `sim_0001.fq.gz` | 315.5 KB |
| `sim_0001.maf.gz` | 180.0 KB |
| `sim_0001.ref` | 59.4 KB |

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
| `/opt/conda/data/….model` | Error model (Quality-score HMM; ONT or PacBio RS II) | QSHMM-ONT | QSHMM-ONT, QSHMM-ONT-HQ, QSHMM-RSII |
| `--depth` | Coverage depth | 5 | 0.1 to 50 |
| `--length-mean` | Mean read length | 3000 | 100 to 50000 |
| `--length-sd` | Read length standard deviation | 1000 | 0 to 20000 |
| `--accuracy-mean` | Mean read accuracy | 0.85 | 0.5 to 0.99 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example runs 5x on a 60,000 bp reference with QSHMM-ONT, mean length 3000, SD 1000.

- `sim_0001.fq.gz` (323,122 bytes): 95 reads, 300,002 bases, mean length 3,158, range 808 to 5,658.
- `sim_0001.maf.gz` (184,323 bytes): the read-to-reference alignments. Counting columns gives 86% identity. Errors split 6.0% substitutions, 55.3% insertions and 38.7% deletions. That is the default 6:55:39 ratio.
- `sim_0001.ref` (60,873 bytes): the reference, named `synthetic_ref`.

The ONT model with the default ratio gives RS II style errors. The first variation below changes that.

The example command is the plain `pbsim` binary. No helper script is involved. It reads the model from `/opt/conda/data` inside the image, and the run takes about 0.3 seconds.

## Your own runs

All runs use the example reference and seed 42.

- **ONT ratio.** Add `--difference-ratio 39:24:36`, the ratio the usage text recommends for ONT. Result: 100 reads, errors 39.0% substitutions, 24.5% insertions, 36.5% deletions. Identity is 86.3%.
- **High-accuracy model.** Use QSHMM-ONT-HQ with `--accuracy-mean 0.95`. Result: 103 reads, identity 94.5%, error rate 5.5% of columns.
- **Multi-pass.** QSHMM-RSII with `--pass-num 10`. Result: `sim_0001.maf.gz` (1.6 MB) and `sim_0001.ref`. No FASTQ and no BAM appeared in the output folder of the recipe's image. The upstream README says multi-pass output is a BAM and lists SAMtools as optional. Check that your install has SAMtools if you need it.

## Pitfalls

- **Ratio and model are separate.** Choosing an ONT model does not change the ratio. Set `--difference-ratio 39:24:36` yourself.
- **Use the HQ model above 90% accuracy.** The documentation recommends QSHMM-ONT-HQ for mean accuracy of 90% or higher.
- **Each strategy has its own input flag.** `--strategy wgs` reads `--genome`, `trans` reads `--transcript` and `templ` reads `--template`. A transcript file is tab-delimited: ID, sense count, antisense count, sequence.
- **Sample mode is WGS only.** `--method sample` cannot combine with multi-pass, transcripts or templates.
- **Default lengths are long.** Mean 9000 and SD 7000 suit large genomes. Set both for small references.

## Further reading

- Source and usage: https://github.com/yukiteruono/pbsim3
- Ono Y, Hamada M, Asai K (2022). PBSIM3. NAR Genom Bioinform 4:lqac092. https://doi.org/10.1093/nargab/lqac092

---

Cite: Ono Y, Hamada M, Asai K (2022). PBSIM3. NAR Genom Bioinform 4:lqac092. doi:10.1093/nargab/lqac092

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pbsim3).
