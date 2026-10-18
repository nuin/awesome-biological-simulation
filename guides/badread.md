# Badread

> Simulate imperfect Oxford Nanopore or PacBio long reads from a reference, with realistic errors, chimeras, junk and random reads, glitches and adapters.

Licence: GPL-3.0-only · [Source code](https://github.com/rrwick/Badread)

## What it simulates

Badread simulates long reads (Oxford Nanopore or PacBio) from a reference FASTA, with the faults real long reads have. It does not aim to copy one platform exactly. It gives you control over how bad the reads are, so you can test what a pipeline does when they get worse.

Each read is built in steps. Badread picks a fragment length from a gamma distribution, then picks a fragment type: a piece of the reference (either strand, with looping over circular contigs), a low-complexity junk fragment, or random sequence. It adds adapters, may join extra fragments to make a chimera, inserts glitches (short stretches of random sequence or lost sequence), picks a target read identity, and adds errors until the read reaches that identity. Quality scores come from a separate model.

Inputs are a FASTA file and a quantity (a depth such as `5x`, or a base count such as `250M`). Output is a FASTQ stream on standard output. Per-contig depth can be set in the FASTA header (`depth=15`), and `circular=true` marks a circular contig.

## When to use it

Use Badread to stress-test tools that take long reads: assemblers, polishers, chimera detectors and read-QC scripts. Raise the chimera, junk and glitch rates and watch where a tool breaks.

- Use [PBSIM3](pbsim3.md) when you want ONT or PacBio reads with a truth alignment (MAF) and quality-score models trained on real data.
- Use [SimLoRD](simlord.md) for PacBio SMRT reads with a pass-number error model.
- Use [CycSim](cycsim.md) when errors should depend on the local k-mer.

The author states that Badread does not try to imitate real reads better than other simulators. It aims for control over read quality.

## Install

Bioconda carries Badread 0.4.2 as a noarch package. The package depends on python-edlib, SciPy, NumPy and Matplotlib, and python-edlib has linux-64, linux-aarch64, osx-64 and osx-arm64 builds.

```bash
conda create -n badread -c conda-forge -c bioconda badread=0.4.2
conda activate badread
badread --version
```

The project README gives `pip3 install git+https://github.com/rrwick/Badread.git` (needs Git and Python 3.6 or later) as the main route. The latest GitHub release is v0.4.2. Badread runs on macOS and Linux.

## A first run

Adapted from the Quick usage section of the [Badread README](https://github.com/rrwick/Badread#quick-usage). The default settings imitate mediocre Oxford Nanopore R10.4.1 reads:

```bash
badread simulate --reference ref.fasta --quantity 50x | gzip > reads.fastq.gz
```

The recipe below uses a 20 kb reference, 5x depth, fragments of mean 3000 bp and a fixed seed, so a run is short.

## Run the tested example

This recipe builds Badread in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.2 s.

1. Download [badread-recipe.tar.gz](https://biosimhub.pages.dev/guides/badread/badread-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf badread-recipe.tar.gz
   cd badread
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/badread:0.4.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/badread:0.4.2 badread simulate --reference /work/in/reference.fa \
    --quantity 5x --length 3000,1500 --identity 95,99,2.5 \
    --error_model nanopore2023 --qscore_model nanopore2023 \
    --junk_reads 1 --random_reads 1 --chimeras 1 \
    --seed 42 > out/badread_reads.fastq
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `badread_reads.fastq` | 204.9 KB |

<details><summary>First lines of <code>badread_reads.fastq</code></summary>

```
@b0c5d3d5-c755-2c99-c349-95ff67432c04 chr_example,+strand,7314-9975 length=2663 error-free_length=2688 read_identity=92.447%
GTTTCAGTTACGTATTGCTAGTATAGCGCTGGGGCGGTCCATTCTTCATAAGCCTAACGAACTGACTGCGTATCGTTATCCCGCCTCCCCTGGACAAAAAAGCTGGTTCAGCCTTTCTTCATTGGTGTATTATCGGATTAACTTGGTGGTCTAAGGGCGGGTTACCCGCTGTCTACGACAAGTTATCCGACCTGCTACTA
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `…x` | Depth of coverage | 5 | 0.5 to 30 |
| `…,{length_sd}` | Mean fragment length | 3000 | 200 to 100000 |
| `{length_mean},…` | Fragment length standard deviation | 1500 | 50 to 100000 |
| `…,{identity_max},{identity_sd}` | Mean read identity (percent) | 95 | 60 to 99 |
| `{identity_mean},…,{identity_sd}` | Maximum read identity (percent) | 99 | 61 to 100 |
| `{identity_mean},{identity_max},…` | Read identity standard deviation | 2.5 | 0.1 to 15 |
| `--error_model` | Error model | nanopore2023 | nanopore2023, nanopore2020, nanopore2018, pacbio2021, pacbio2016, random |
| `--qscore_model` | Quality score model | nanopore2023 | nanopore2023, nanopore2020, nanopore2018, pacbio2021, pacbio2016, random, ideal |
| `--junk_reads` | Junk reads (percent) | 1 | 0 to 20 |
| `--random_reads` | Random reads (percent) | 1 | 0 to 20 |
| `--chimeras` | Chimera rate (percent) | 1 | 0 to 20 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The FASTQ header of each read starts with a random UUID and then lists tags. From the Badread source (`simulate.py`): `length=` is the read length, `error-free_length=` is the fragment length before errors, and `read_identity=` is the identity the read reached, as a percent. A read from junk sequence carries `junk_seq`, a read from random sequence carries `random_seq`, and a chimera carries `chimera`. Reads from the reference also record the contig name and the strand (`+strand` or `-strand`).

Badread writes progress and a parameter summary to standard error, not to the FASTQ. The recipe keeps only standard output, so the log is not saved.

Check three things in your own run. The read identity column should centre near the mean you set with `--identity`. The share of junk and random reads should be about 2% at the defaults (1% each). The total bases should be close to depth times reference length.

The error and qscore models are separate options. The README lists `nanopore2023` (default, R10.4.1), `nanopore2020` (R9.4.1), `nanopore2018`, `pacbio2016` (RS II), `pacbio2021` (Sequel IIe HiFi) and `random` for errors. The qscore models add `ideal`, where scores are unrealistically informative.

## Pitfalls

- **Identity has two forms.** Three numbers (`95,99,2.5`) are mean, maximum and standard deviation of a beta distribution. Two numbers (`20,4`) are a Phred-score mean and standard deviation, meant for high-accuracy reads such as HiFi. The recipe exposes the three-number form only.
- **Lengths describe fragments.** Adapters, glitches, chimeras and indel-biased errors change the final read length.
- **Defaults assume a large genome.** The default fragment length is `15000,13000`. The source exits with "are your read lengths incompatible with your reference contig lengths?" when no fragment fits a contig, so set `--length` below the contig length.
- **It is slow on large inputs.** The README says Badread repeatedly aligns each read to its fragment to hit the target identity, and links a wiki page on running it in parallel.
- **Adapters are on by default.** Reads carry Nanopore ligation adapters unless you pass empty adapter sequences.
- **No truth alignment.** The output has no CIGAR or MAF. Use [PBSIM3](pbsim3.md) if you need one.

## Further reading

- README with all options: https://github.com/rrwick/Badread
- Error models: https://github.com/rrwick/Badread/wiki/Error-models
- Definition of identity: https://github.com/rrwick/Badread/wiki/Definition-of-identity
- Paper: Wick RR (2019). Badread: simulation of error-prone long reads. Journal of Open Source Software 4(36):1316. https://doi.org/10.21105/joss.01316

---

Cite: Wick RR (2019). Badread: simulation of error-prone long reads. Journal of Open Source Software 4(36):1316. doi:10.21105/joss.01316

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/badread).
