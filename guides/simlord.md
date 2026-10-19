# SimLoRD

> Simulate PacBio SMRT long reads (with pass-dependent insertion, deletion and substitution errors) from a reference FASTA.

Licence: MIT · [Source code](https://bitbucket.org/genomeinformatics/simlord/)

## What it simulates

SimLoRD simulates PacBio SMRT long reads from a reference FASTA. Its error model follows the number of passes a molecule gets around the circular template. More passes give a more accurate consensus read. Each read draws a pass count, and the insertion, deletion and substitution probabilities fall with it. You give a reference, a coverage and a read-length rule. It returns a FASTQ, and optionally a SAM of the true alignments.

Key assumptions: the single-pass error rates are the ones you set (defaults 0.11 insertion, 0.04 deletion, 0.01 substitution), and the pass count follows a fitted chi-squared model capped by `--max-passes` (default 40).

## When to use it

- Test a PacBio-oriented pipeline across a range of accuracy, from noisy single-pass to near-perfect consensus reads.
- Draw read lengths from a log-normal distribution, a fixed length, or the lengths in your own FASTQ.
- Get the true origin of each read from the header.

Alternatives on biosimhub: [PBSIM2](pbsim2.md) and [PBSIM3](pbsim3.md) use quality-score HMMs and cover Nanopore too. [CycSim](cycsim.md) learns errors from real reads and ties them to the local sequence.

## Install it yourself

SimLoRD 1.0.4 is on bioconda (dry-run resolved on linux-aarch64 to build `py310h5cfe7d9_6`, 34 kB).

```
conda create -n simlord -c conda-forge -c bioconda simlord=1.0.4
conda activate simlord
```

Minimal command:

```
simlord --read-reference reference.fa --coverage 5 --fixed-readlength 1000 --no-sam sim
```

The last argument is the output prefix. The reads go to `sim.fastq`. Without `--no-sam` it also aligns every read and writes `sim.sam`. Other options: `--num-reads` (default 1000) instead of `--coverage`, `--gzip`, `--without-ns`, and `--generate-reference GC LENGTH` to make a random genome.

## Run the tested example

This recipe builds SimLoRD in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.8 s.

1. Download [simlord-recipe.tar.gz](https://biosimhub.pages.dev/guides/simlord/simlord-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf simlord-recipe.tar.gz
   cd simlord
   sh run.sh
   ```

![Terminal recording of the SimLoRD example run](https://biosimhub.pages.dev/media/simlord/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/simlord:1.0.4 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/simlord:1.0.4 simlord --read-reference /work/in/reference.fa \
    --coverage 5 --fixed-readlength 1000 --prob-ins 0.11 \
    --prob-del 0.04 --prob-sub 0.01 --max-passes 40 \
    --no-sam sim > out/simlord_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `sim.fastq` | 213.6 KB |
| `simlord_log.txt` | 0 B |

<details><summary>First lines of <code>sim.fastq</code></summary>

```
@m0/1000/CCS Read=0;length=1000bp;startpos=2421;chromosome=synthetic_ref;numberOfErrors=21;totalErrorProb=0.0271;passes=3.672087738420167;passesLeft=3;passesRight=4;cutPosition=328
AGTGTTCGCATCTGGCGCTCAGATTTTAAGTTAATCTGCCGAACCGTCGGCTTTCGCAGGTCCAGTATCACTGTCTTACAGGAGTGCGACTAGGGCCCGCGCAGTGTGAACGATTGTATGGGGCGAGTGATGTTAGTGGAAAGGCAGCTCATTCTAGCCGACGTGGCCAATGCCTAACCACTCCGTGCCGTAGATACGTA
+
22222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222222
@m1/1000/CCS Read=1;length=1000bp;startpos=4665;chromosome=synthetic_ref;numberOfErrors=2;totalErrorProb=0.0010;passes=9.453415682616459;passesLeft=9;passesRight=10;cutPosition=547
TTAGTTAAGAGGGTGCAAGCGGAGTGAAAATCGG
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--coverage` | Coverage | 5 | 0.1 to 50 |
| `--fixed-readlength` | Fixed read length | 1000 | 100 to 20000 |
| `--prob-ins` | Insertion probability (single pass) | 0.11 | 0 to 0.3 |
| `--prob-del` | Deletion probability (single pass) | 0.04 | 0 to 0.3 |
| `--prob-sub` | Substitution probability (single pass) | 0.01 | 0 to 0.3 |
| `--max-passes` | Maximum number of passes | 40 | 1 to 100 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The reference is one 20,000 bp sequence named `synthetic_ref`. At 5x with fixed 1000 bp reads, SimLoRD writes 100 reads (100,000 bases) into `sim.fastq` (218,756 bytes). `simlord_log.txt` is empty.

The first header reads:

```
@m0/1000/CCS Read=0;length=1000bp;startpos=2421;chromosome=synthetic_ref;numberOfErrors=21;totalErrorProb=0.0271;passes=3.67;passesLeft=3;passesRight=4;cutPosition=328
```

- `startpos` is the 0-based origin on the reference.
- `numberOfErrors=21` is the count of inserted, deleted and changed bases in this read.
- `passes=3.67` is the pass count. Fewer passes mean more errors. The second read has 9.45 passes and 2 errors.
- Quality values are one flat character (`2`, Phred 17) on every base. They carry no per-base information.

Across the 100 reads the mean is 4.98 errors per 1000 bp and 9.88 passes.

## Your own runs

- **Single pass.** Add `--max-passes 1`. Result: 100 reads, all with `passes=1`, and a mean of 173.0 errors per read (17.3%) against 4.98 before.
- **Real-looking lengths.** Replace `--fixed-readlength 1000` with `--lognorm-readlength` and use coverage 10. Result: 24 reads, 212,073 bases, mean 8,836 bp. Coverage targets total bases (10 x 20,000 = 200,000), so a long-tailed length draw gives fewer reads.
- **Your genome.** Mount your FASTA, keep `--no-sam` while you tune, and drop it when you need truth alignments.

## Pitfalls

- **Error rates are single-pass rates.** `--prob-ins`, `--prob-del` and `--prob-sub` describe a one-pass read. Multi-pass reads get fewer errors, so the reads you see are cleaner than those values.
- **Flat quality scores.** Tools that use base qualities see no signal here. Do not use these FASTQs to test quality filtering.
- **Coverage is by bases.** The read count depends on the length rule. Use `--num-reads` for an exact count.
- **SAM output costs time.** Without `--no-sam`, SimLoRD aligns every read and writes a SAM file. Large genomes need the extra time and disk.
- **No seed option.** The help lists no seed flag, so runs are not repeatable.

## Further reading

- Source: https://bitbucket.org/genomeinformatics/simlord/
- PyPI: https://pypi.org/project/SimLoRD/
- Stocker BK, Koster J, Rahmann S (2016). SimLoRD. Bioinformatics 32:2704-2706. https://doi.org/10.1093/bioinformatics/btw286

---

Cite: Stocker BK, Koster J, Rahmann S (2016). SimLoRD, simulation of long read data. Bioinformatics 32:2704-2706. doi:10.1093/bioinformatics/btw286

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simlord).
