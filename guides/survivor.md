# SURVIVOR

> Simulate structural variants (deletions, duplications, inversions, translocations, insertions) and SNPs on a reference genome, writing the altered FASTA and a list of the planted events.

Licence: MIT · [Source code](https://github.com/fritzsedlazeck/SURVIVOR)

## What it simulates

SURVIVOR is a command-line toolset for structural variants (SVs), written in C++. This guide covers its simulation commands. It also merges, filters, converts and summarises SV calls in VCF files, which the guide only mentions.

The simulation commands are:

- `simSV` takes a reference FASTA and a parameter file. It plants deletions and insertions (called INDEL in the parameter file), duplications, inversions and translocations, plus SNPs at a frequency you give. It writes the altered genome and the list of planted events.
- `scanreads` learns an error profile (read length distribution and per-position match, mismatch, insertion and deletion ratios) from mapped long reads.
- `simreads` simulates long reads (PacBio or Oxford Nanopore style) from a reference and an error profile at a chosen coverage. The repository ships two profiles, one for Nanopore (NA12878) and one for PacBio (HG002).
- `eval` compares the VCF from an SV caller with the planted events and reports sensitivity and false discovery rate.

The biosimhub recipe wraps `simSV` only. Its inputs are a reference FASTA, a parameter file, a SNP frequency and a coordinate mode.

Key assumptions: each event type has a length range and a count in the parameter file. Event positions are random. Translocations are balanced exchanges between two sequences, so the reference needs at least two.

## When to use it

Use SURVIVOR to build a truth set for SV callers: plant a known number of events, simulate reads, call, then score with `eval`. It also fits when you want to merge calls from several callers, which the other simulators here do not cover.

Alternatives:

- [Mason](mason.md) plants SNPs, small indels and SVs with `mason_variator` and simulates Illumina reads in the same toolchain.
- [simuG](simug.md) simulates SNPs, indels and SVs for genome comparison work and writes a VCF of what it planted.
- [DWGSIM](dwgsim.md) simulates short reads with SNPs and small indels. It does not simulate large SVs.

## Install it yourself

Conda, pinned to the Bioconda build of 1.0.7. Builds exist for linux-64, linux-aarch64, osx-64 and osx-arm64. The latest tag on the GitHub release page is v1.0.6; the Bioconda recipe builds the 1.0.7 source archive.

```bash
conda create -n survivor -c conda-forge -c bioconda survivor=1.0.7
conda activate survivor
SURVIVOR
```

Running `SURVIVOR` with no arguments prints the command list. To build from source, the README gives:

```bash
git clone https://github.com/fritzsedlazeck/SURVIVOR.git
cd SURVIVOR/Debug
make
```

## A first run

Adapted from the SURVIVOR wiki, Home page (https://github.com/fritzsedlazeck/SURVIVOR/wiki).

Generate a parameter file, edit the numbers (keep the line order and the spaces), then simulate:

```bash
SURVIVOR simSV parameter_file
SURVIVOR simSV ref.fa parameter_file 0.1 0 simulated
```

The arguments after the parameter file are the SNP frequency (0 to 1), the coordinate mode and the output prefix. Mode `0` reports coordinates for simulating reads from the altered genome and mapping them to the original reference. Mode `1` reports them for mapping real reads to the altered genome.

To score a caller afterwards, the wiki gives:

```bash
SURVIVOR eval caller.vcf simulated.bed 10 eval_res
```

The `10` is the largest distance in base pairs allowed between a called and a planted breakpoint.

## Run the tested example

This recipe builds SURVIVOR in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.2 s.

1. Download [survivor-recipe.tar.gz](https://biosimhub.pages.dev/guides/survivor/survivor-recipe.tar.gz) (Dockerfile, example reference.fa, params.txt, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf survivor-recipe.tar.gz
   cd survivor
   sh run.sh
   ```

![Terminal recording of the SURVIVOR example run](https://biosimhub.pages.dev/media/survivor/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/survivor:1.0.7 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/survivor:1.0.7 SURVIVOR simSV /work/in/reference.fa /work/in/params.txt 0.001 0 sim > out/survivor_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `survivor_log.txt` | 43 B |

<details><summary>First lines of <code>survivor_log.txt</code></summary>

```
# Chrs passed size threshold:2
generate SV
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `snp_rate` | SNP frequency (0 to 1) | 0.001 | 0 to 0.2 |
| `mode` | Coordinate mode (0 reports coordinates for simulating reads from the altered genome and mapping them to the original; 1 reports them for mapping real reads to the altered genome) | 0 | 0, 1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

With the prefix `sim`:

- `sim.fasta`: the reference with all events and SNPs applied.
- `sim.bed`: one line per event: start chromosome, start position, end chromosome, end position, then the type (DEL, DUP, INV, TRA, INS). A translocation has two lines, one per exchanged breakpoint, as the wiki explains.
- `sim.insertions.fa`: the inserted sequences.
- `sim.vcf`: the planted events as a VCF file.
- `survivor_log.txt`: the program's standard output.

The wiki shows what `eval` prints at the end: a line such as `Overall: 20 11/0/0/0/9 0/0/0/0/0 0/0/0/0/0 1 0`. It reads as 20 SVs simulated, then the found, missed and additional counts by type (DEL/DUP/INV/TRA/INS), then sensitivity and false discovery rate. That example comes from the wiki, not from a recipe run.

## Pitfalls

- **The simulation cannot be seeded.** The source calls `srand(time(NULL))`, so two runs in different seconds give different genomes. Keep `sim.bed` and `sim.fasta` from the run you want to reuse.
- **Translocations need two or more sequences.** The program stops with an error if the parameter file asks for translocations and the FASTA has one.
- **Sequence length limits.** Event lengths must fit inside the sequences. A message about sequences too small for the simulation means the length ranges are too large for the reference.
- **The parameter file is positional.** Change values only; do not add, remove or reorder lines.
- **Merging is a different job.** `SURVIVOR merge` and the other comparison commands take VCF input and do not simulate.
- **Read simulation needs a profile.** `simreads` takes the reference, an error profile, a coverage and a prefix, in that order.

## Further reading

- Repository and README: https://github.com/fritzsedlazeck/SURVIVOR
- Wiki: https://github.com/fritzsedlazeck/SURVIVOR/wiki
- Methods and parameters: https://github.com/fritzsedlazeck/SURVIVOR/wiki/Methods-and-Parameter
- Jeffares DC, Jolly C, Hoti M, et al. (2017). Transient structural variations have strong effects on quantitative traits and reproductive isolation in fission yeast. Nature Communications 8:14061. https://doi.org/10.1038/ncomms14061

---

Cite: Jeffares DC, Jolly C, Hoti M, et al. (2017). Transient structural variations have strong effects on quantitative traits and reproductive isolation in fission yeast. Nature Communications 8:14061. doi:10.1038/ncomms14061

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/survivor).
