# Seq-Gen

> Simulate the evolution of nucleotide or amino-acid sequences along a phylogenetic tree under Markov substitution models.

Licence: BSD-3-Clause · [Source code](https://github.com/rambaut/Seq-Gen)

## What it simulates

Seq-Gen evolves DNA or protein sequences down a phylogenetic tree you supply. It draws a random root sequence, then walks each branch and applies substitutions under a continuous-time Markov model. The output is an alignment of the tip sequences, one row per leaf.

Branch lengths are expected substitutions per site. A branch of 0.3 changes about 30% of sites, with multiple hits on the same site counted. The `-s` option multiplies every branch length by one constant.

Key assumptions:

- Sites evolve independently.
- There are no insertions or deletions, so every output is gap-free.
- The root is random. For nucleotides the default base frequencies are equal.
- Rates are the same at every site unless you add gamma rate variation (`-a`) or invariable sites (`-i`).

Nucleotide models are HKY, F84 and GTR. Amino-acid models include JTT, WAG, PAM, BLOSUM, MTREV and CPREV, plus LG and a user-defined GENERAL matrix.

## When to use it

Use Seq-Gen to make a quick alignment with a known tree and known model, for example to test a phylogeny program or to get a null distribution for a statistic. It runs in a fraction of a second for 5 taxa and 1000 sites.

Alternatives on biosimhub:

- **[Pyvolve](pyvolve.md)** is better when you need a codon model with dN/dS, or want to script models and partitions from Python.
- **[Bio++ bppseqgen](bppseqgen.md)** is better when you want a model written as a text description, with several models or processes in one run.
- **[SimProt](simprot.md)** is better when the question involves indels, since Seq-Gen never writes a gap.

## Install it yourself

Conda, pinned to the recipe's version:

```bash
conda create -n seqgen -c conda-forge -c bioconda seq-gen=1.3.5
conda activate seqgen
```

The command resolves on bioconda (package seq-gen 1.3.5, 70 kB). From source, the repository README says to run `make` inside `source/`; the binary `seq-gen` is created there.

The minimal command reads a Newick file and writes PHYLIP to standard output:

```bash
seq-gen -mHKY -l1000 -z42 -op tree.nwk > alignment.phy
```

`-m` picks the model (required), `-l` the length, `-z` the seed, `-op` PHYLIP output. Run `seq-gen` with no arguments to print the full option list.

## Run the tested example

This recipe builds Seq-Gen in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s.

1. Download [seq-gen-recipe.tar.gz](https://biosimhub.pages.dev/guides/seq-gen/seq-gen-recipe.tar.gz) (Dockerfile, example tree.nwk, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf seq-gen-recipe.tar.gz
   cd seq-gen
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/seq-gen:1.3.5 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/seq-gen:1.3.5 seq-gen -mHKY -l1000 -n1 -s1 -z42 -op -q /work/in/tree.nwk > out/alignment.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `alignment.txt` | 4.9 KB |

<details><summary>First lines of <code>alignment.txt</code></summary>

```
 5 1000
A         CGTGGTGGACAAACTTGAGGAATCTTAAATCTCGGATTCGGCAAGTTAGATGACGAGCATCGTCTATTGGTCCAAAGACGCGCTAATCCAGTCCAAGTAATTTCTGTGTATCAGACATCTCGTGTGATCGGCAATAAATCTCACAAACTCGTTGATCGGTTGGCCTACGGCGGTGCTGCCGTGTTGGATC
B         CGTGATGCACAAACTCGAGGAATGTTAAATAGCCGTTTGGCCGAGTCACATGACGGGCATGCTCTATTTGGCCAACGACGCGCTAATGTAGCCCGAAGAATATCTGTTGGTCAGAGCTGTCGCGTGATCGGCACCAAATCTCACACTAGGCTAGATCGATTGGCCAACTGCGGGGCTGCCAATTGGCATC
C         CTTAGTTTATAAGATCGAGGAAGGTAATAGTGAGGTAACGGCAACTCCCATGACTTATTGGTCCAAAATGTCCAAAGTCGAGCTGTTCCAGTACGAGAAATTCCTCTTAATCAGAGACCTCGCGACATCGGCAGTACATCTCGAAATGGGGGTAAGTGATAGGCCGCCCGCGAGGCGGCCCTGTTGGACG
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-m…` | Substitution model | HKY | HKY, F84, GTR, JTT, WAG, PAM, BLOSUM, MTREV, CPREV |
| `-l…` | Sequence length | 1000 | 1 to 1000000 |
| `-n…` | Datasets | 1 | 1 to 1000 |
| `-s…` | Branch length scale | 1 | 0.0001 to 1000 |
| `-a{value}` | Gamma shape alpha (optional) | not set | 0.001 to 1000 |
| `-z…` | Seed | 42 | 1 to 2147483647 |
| `-o…` | Output format (p PHYLIP, r relaxed PHYLIP, n NEXUS) | p | p, r, n |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example tree is `((A:0.1,B:0.2):0.05,(C:0.3,D:0.15):0.1,E:0.25);`, five taxa. The run writes one file, `alignment.txt`, 5063 bytes.

The first line is ` 5 1000`: 5 sequences, 1000 sites. Each following line is a taxon name (A to E) padded to 10 characters, then 1000 bases. PHYLIP here is not wrapped.

Taxa A and B are joined through branches of 0.1 and 0.2, so the expected distance is 0.3 substitutions per site. The example shows 233 differences in 1000 sites (0.233). That is lower than 0.3 because some sites mutate twice or mutate back.

Of those 233 differences, 71 are transitions and 162 are transversions. The ratio is 0.44. Section "Pitfalls" explains why.

## Your own runs

Each run below used the example tree, HKY, 1000 sites, seed 42, and changed one option. All numbers compare taxa A and B.

**Raise the transition/transversion ratio (`-t 4`).** Transitions went from 71 to 163 and transversions from 162 to 59. Total differences stayed near the same (222 against 233).

**Add gamma rate variation (`-a 0.2`).** Low alpha concentrates change in a few fast sites. Differences between A and B fell to 139. Columns identical across all five taxa rose from 325 to 714.

**Lengthen the tree (`-s 3`).** Every branch is tripled. Differences between A and B rose to 515 (0.515), and only 43 columns stayed identical across all taxa. With four equally frequent bases the observed difference cannot pass 0.75, so long branches saturate.

**Protein, two datasets (`-mWAG -l300 -n2 -on`).** The output is NEXUS with two `Begin DATA` blocks, each with `NTAX=5 NCHAR=300` and `DATATYPE=PROTEIN`.

**Reproducibility.** Seed 42 twice gave byte-identical files. Seed 43 differed from the first character of the first sequence.

## Pitfalls

- **Default ts/tv is 0.5.** Without `-t`, HKY runs with TS/TV 0.5, which the manual says gives equal instantaneous rates of transitions and transversions. The example's 71 transitions to 162 transversions shows it. Set `-t` to the ratio you estimated from your data.
- **`-s 0` fails.** Seq-Gen printed `Bad Branch Length Scale: -s0` and wrote nothing. Use a small positive value. With `-s 0.0001` taxa A and B were identical.
- **FASTA needs a file name.** The usage text says `-y` (output file name) is required for FASTA. Writing to standard output works for PHYLIP, relaxed PHYLIP and NEXUS (`-op`, `-or`, `-on`).
- **Strict PHYLIP pads names to 10 characters.** Use `-or` for relaxed PHYLIP, which the manual says allows names up to 256 characters.
- **Branch lengths are in substitutions per site.** A tree whose lengths are in years or generations needs rescaling first, with `-s` or with `-d` (the manual says `-d` works only on rooted ultrametric trees).
- **Ancestral sequences and site rates are opt-in.** `-wa` writes internal-node sequences. `-wr` writes site rates to the screen (stderr). The alignment file does not contain them.

## Further reading

- Seq-Gen manual: http://rambaut.github.io/Seq-Gen/manual
- Source and releases: https://github.com/rambaut/Seq-Gen
- Rambaut A, Grassly NC (1997). Seq-Gen: an application for the Monte Carlo simulation of DNA sequence evolution along phylogenetic trees. CABIOS 13:235-238. https://doi.org/10.1093/bioinformatics/13.3.235

---

Cite: Rambaut A, Grassly NC (1997). Seq-Gen. CABIOS 13:235-238. doi:10.1093/bioinformatics/13.3.235

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/seq-gen).
