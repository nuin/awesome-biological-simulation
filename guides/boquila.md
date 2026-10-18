# Boquila

> Select reads from a pool of candidate reads so that their nucleotide (k-mer) composition matches a model read set, to serve as bias-matched controls.

Licence: MIT · [Source code](https://github.com/CompGenomeLab/boquila)

## What it simulates

Boquila does not simulate sequencing. It picks reads from a pool of candidate reads so that the picked set has the same nucleotide composition as a model read set. The picked reads work as a control with the same sequence bias as your real data.

The inputs are a model FASTQ (the reads to imitate) and a pool FASTQ (candidates). The pool reads must be longer than the model reads. The output is a FASTQ of reads with the model's length and a composition matched to the model.

Key assumptions:

- Composition is the frequency of k-mers of one size, set by `--kmer`. Position in the read matters too, and `--sens` controls how closely the positions are matched.
- Every picked read comes from the pool. Boquila creates no new sequence and adds no errors.
- With a reference genome and a regions file, Boquila can pick reads from the genome instead of from a pool. The biosimhub example uses a pool.

## When to use it

Use Boquila when your signal reads have a sequence bias and a naive control does not. Typical questions:

- Is an enrichment real, or does it follow from the nucleotide content of my reads?
- Can I build a control set that matches the AT content of my assay?
- How different is my read set from a random draw of the genome?

[wgsim](wgsim.md), [DWGSIM](dwgsim.md) and [pIRS](pirs.md) on biosimhub create a pool: they produce reads from a reference, with longer reads than your model. Feed their output to Boquila as the pool. [gargammel](gargammel.md) creates ancient-DNA-style pools.

## Install it yourself

The Bioconda package is `boquila` 0.6.1. The recipe targets `linux/amd64`.

```bash
conda create -n boquila -c conda-forge -c bioconda boquila=0.6.1
conda activate boquila
```

You can also build it with Cargo. The README gives `cargo install --branch main --git https://github.com/CompGenomeLab/boquila.git boquila`, and the minimum Rust version is 1.55.0.

The minimal command writes the picked reads to standard output:

```bash
boquila --inseq pool.fq --kmer 1 --sens 20 --seed 42 model.fq > simulated_reads.fq
```

- `model.fq` is the positional argument: the reads to imitate.
- `--inseq` is the pool of candidate reads. Without it, you give `--ref` and `--regions`.
- `--kmer` is the k-mer size used to compare composition. The default is 1.
- `--sens` is the sensitivity, from 10 to 100. The default is 20. Higher values match position-specific composition better and run slower, in linear time.
- `--seed` fixes the random draw. Without it Boquila uses system entropy.
- `--fasta` and `--inseqFasta` switch the formats to FASTA.
- `--bed` saves the origin of each read in BED6 format when you use a reference.
- `--setQual` and `--qual` give every read one quality character.

## Run the tested example

This recipe builds Boquila in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.3 s. Boquila has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [boquila-recipe.tar.gz](https://biosimhub.pages.dev/guides/boquila/boquila-recipe.tar.gz) (Dockerfile, example reads.fq, pool.fq, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf boquila-recipe.tar.gz
   cd boquila
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/boquila:0.6.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/boquila:0.6.1 boquila --inseq /work/in/pool.fq --kmer 1 \
    --sens 20 --seed 42 /work/in/reads.fq > out/simulated_reads.fq
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `simulated_reads.fq` | 90.7 KB |

<details><summary>First lines of <code>simulated_reads.fq</code></summary>

```
@read0
ACTTTGATGTGTAGAGAAAGGAGAGGCTAGATCACTAGCT
+
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
@read1
AAATCAGTTAAGGGTTCCAAACTTCGCTGAATATTTCAGA
+
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
@read2
TAGATGCCAGGTCAATTAAAGGTTCATAACTTTCTTGCAC
+
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--kmer` | k-mer size | 1 | 1 to 6 |
| `--sens` | Sensitivity | 20 | 10 to 100 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The model file has 1,000 reads of 40 bp (92,890 bytes). The pool has 900 reads of 80 bp (155,590 bytes).

`simulated_reads.fq` has 1,000 reads of 40 bp and is 92,890 bytes, the same size as the model. Read names run `@read0`, `@read1` and so on. Every output read is an exact 40 bp stretch of one pool read on the forward strand: all 1,000 matched, and none matched on the reverse strand. The qualities are `I`, as in the model reads.

Composition shows what changed. A, C, G and T frequencies were:

| Set | A | C | G | T | A+T |
|---|---|---|---|---|---|
| Model | 0.350 | 0.150 | 0.152 | 0.348 | 69.8% |
| Pool | 0.247 | 0.255 | 0.250 | 0.248 | 49.5% |
| Output | 0.317 | 0.188 | 0.173 | 0.322 | 63.9% |

The model is AT-rich and the pool is balanced. The output moves most of the way toward the model. The sum of absolute frequency differences from the model fell from 0.408 for the pool to 0.118 for the output.

Only 760 of the 1,000 output reads are distinct. Some reads repeat, and a 900-read pool is small.

## Your own runs

These runs used the recipe's image and the example inputs. Distances below are the sum of absolute differences between the output and the model, for 1-mers.

**Highest sensitivity.** Set `--sens 100`. The A+T share becomes 68.3% against 69.8% in the model, and the 1-mer distance falls from 0.118 to 0.031. Distinct reads drop from 760 to 493.

**A larger k-mer.** Set `--kmer 3`. The A+T share falls to 58.0%, and the 1-mer distance rises to 0.236. The 3-mer distance is 0.347, against 0.238 for the `--kmer 1` output. The pool has 900 reads for 64 trinucleotide frequencies, and a larger pool is the first thing to try.

**Another seed.** Set `--seed 7`. The output differs from seed 42, and its 1-mer distance is 0.115. Run several seeds when you want a spread of control sets.

For your own data, give your reads as the model and a longer-read pool as `--inseq`.

## Pitfalls

- Pool reads must be longer than model reads.
- A small pool repeats reads. Check the number of distinct reads (760 of 1,000 here) and enlarge the pool.
- A higher `--sens` improves the match and slows the run in proportion. Raise it only when the composition is still off.
- A larger `--kmer` needs more pool reads. A 3-mer match on 900 reads was worse than a 1-mer match.
- Output goes to standard output. Redirect it with `>`.
- Qualities follow the model, or the `--qual` character with `--setQual`. FASTA input loses them.

## Further reading

- Boquila repository and README: https://github.com/CompGenomeLab/boquila
- Deniz O, Yildiz G, Adebali O (2023). Boquila, NGS read simulator to eliminate read nucleotide bias in sequence analysis. Turk J Biol 47:1-9. https://doi.org/10.55730/1300-0152.2650

---

Cite: Deniz O, Yildiz G, Adebali O (2023). Boquila, NGS read simulator to eliminate read nucleotide bias in sequence analysis. Turk J Biol 47:1-9. doi:10.55730/1300-0152.2650

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/boquila).
