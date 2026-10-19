# Bio++ bppseqgen

> Simulate DNA sequence alignments along a phylogenetic tree under an HKY85 substitution model with gamma rate variation.

Licence: CECILL-2.1 · [Source code](https://github.com/BioPP/bppsuite)

## What it simulates

bppseqgen is the sequence simulator of the Bio++ Program Suite. It evolves sequences down a tree under a substitution model you describe in text, and writes the tip alignment. Models, rate distributions and processes are declared as numbered options and then linked together.

In this recipe the declaration is: a Newick tree, an HKY85 model (kappa for the transition/transversion rate, theta for GC content), a 4-category discretised gamma distribution of rates across sites, and a homogeneous process that applies one model to the whole tree. Branch lengths come from the tree file; the log prints `Branch lengths: Input`.

Key assumptions:

- Sites are independent draws from the rate distribution.
- Every branch uses the same model (homogeneous process).
- Substitutions only. The example alignment has no gap characters.

## When to use it

Use bppseqgen when you want the model written out explicitly and reusable, or when you want to extend the same description to several models and processes later. The recipe here uses one model on one tree.

Alternatives on biosimhub:

- **[Seq-Gen](seq-gen.md)** is faster to learn for plain HKY, F84, GTR and protein matrices. It is a short command line.
- **[Pyvolve](pyvolve.md)** fits when you want codon models with dN/dS or want to build the model in Python.
- **[SimProt](simprot.md)** fits when you need indels.

## Install it yourself

Conda, pinned to the version the recipe uses:

```bash
conda create -n bpp -c conda-forge -c bioconda bppsuite=3.0.0
conda activate bpp
```

A dry run of the command resolved bppsuite 3.0.0 with about 148 MB of dependencies. Bio++ also ships Linux binaries on https://github.com/BioPP/bppsuite/releases, a Homebrew tap for macOS and an Apptainer image; the project's installation page lists them.

The tool's own command line takes `key=value` options. Minimal run on a tree file:

```bash
bppseqgen alphabet=DNA \
  "input.tree1=user(file=tree.nwk,format=Newick)" \
  "model1=JC69" \
  "process1=Homogeneous(model=1,tree=1)" \
  "simul1=Single(process=1,output.sequence.file=alignment.txt,output.sequence.format=Fasta,number_of_sites=500)" \
  --seed=42
```

In the recipe's image, this JC69 form with seed 42 wrote 6 sequences of 500 sites, 69 of them variable. Add `rate_distribution1=Gamma(n=4,alpha=0.5)` and `rate=1` in the process line, as the recipe below does, for rate variation.

## Run the tested example

This recipe builds Bio++ bppseqgen in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s.

1. Download [bppseqgen-recipe.tar.gz](https://biosimhub.pages.dev/guides/bppseqgen/bppseqgen-recipe.tar.gz) (Dockerfile, example tree.nwk, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bppseqgen-recipe.tar.gz
   cd bppseqgen
   sh run.sh
   ```

![Terminal recording of the Bio++ bppseqgen example run](https://biosimhub.pages.dev/media/bppseqgen/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/bppseqgen:3.0.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bppseqgen:3.0.0 bppseqgen alphabet=DNA 'input.tree1=user(file=/work/in/tree.nwk,format=Newick)' 'model1=HKY85(kappa=2,theta=0.5,theta1=0.5,theta2=0.5)' 'rate_distribution1=Gamma(n=4,alpha=0.5)' 'process1=Homogeneous(model=1,rate=1,tree=1)' 'simul1=Single(process=1,output.sequence.file=alignment.txt,output.sequence.format=Fasta,number_of_sites=500)' \
    --seed=42 > out/bppseqgen_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `alignment.txt` | 3.0 KB |
| `bppseqgen_log.txt` | 2.1 KB |

<details><summary>First lines of <code>alignment.txt</code></summary>

```
>human
ACGAAGAGAGCAGCCAACCCCCTATCAGATACTGCGTTGTCGATGAAGTCCGGACCAGGACTCGGGCACCGCTCTATGGCTCGTGACAATGACCGGAGCT
ATTGACGGTCCGGTCCCTAGGTCTGTTGTACCGCCGCTTGGGACACGAATCACATACGGTACGGGCCCAGGGCGAGGGTTGGTCTATGAAAGTCGCATGG
TTTTGCCATAGAGGAGATGTTTCTCTGTGTCGGACTTGCCATGTGTTTTAACCCGGAACGTTTCAAGCTATTGAATCCGGGTTGCAGTGATGGTATACCT
TTTTTATTACGATGCTGTGATATGATGTAATGAGTTCGCACCTGTTGACCAATTCACCTCAAGCGGCGGAGAATGAGGTCAACCACAAGTGACCTGTCTG
AAGAGTGCGCGTGCTCGATTACTCTCGAACTACCGCGGAGCATCAGAGCGGAGGACTAAGTACTCATACGTCATCAAGAACTGCGACCTATACCATAGCC

>chimp
ATGAAGAGAGCAGCCAACCCCCTATCAGATACTGCGTTGTCGATGAAGTCCGGACCAGGACTCGGGCACCGCTCTATGGCTCGTGACTATGACCGGAGCT
ATTGACGGTCCGGTCCCTAGGTCTGTTGTACCGCCGCTTGGGACACGAATCACATACGGTACGGGCCCAGGGCGAGGGTTGGTCTATGAAAGTCGCATGG
TTTTGCCATAGAGGAGATGTTTCTCTGTGTCGGACTTGCCATGTGTTTTAACCCGGAACGTTTCAAGCTATTGAATCCGGGTTGCGGTGATGGTATACCT
TTTCTTTTACGATGCTGTGATATGATGTAATGAGTTCGCACCTGTTGACCAATTCACCTCAAGCGGCGGAGAATGAGGTCAACCACAAGTGACCTGTCTG
```

</details>

<details><summary>First lines of <code>bppseqgen_log.txt</code></summary>

```
******************************************************************
*            Bio++ Sequence Generator, version 3.0.0             *
*                                                                *
* Authors: J. Dutheil                                            *
*          B. Boussau                       Last Modif. January 28th, 2026 *
*          L. Gueguen                                            *
*          M. Groussin                                           *
******************************************************************

Parsing options:
Random seed set to.....................: 42
Alphabet type .........................: DNA
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `model1=HKY85(kappa=…,theta={theta},theta1=0.5,theta2=0.5)` | Transition/transversion ratio (kappa) | 2 | 0.1 to 100 |
| `model1=HKY85(kappa={kappa},theta=…,theta1=0.5,theta2=0.5)` | GC content (theta) | 0.5 | 0.05 to 0.95 |
| `rate_distribution1=Gamma(n=4,alpha=…)` | Gamma shape alpha (4 rate categories) | 0.5 | 0.05 to 100 |
| `simul1=Single(process=1,output.sequence.file=alignment.txt,output.sequence.format={format},number_of_sites=…)` | Alignment length (sites) | 500 | 1 to 1000000 |
| `simul1=Single(process=1,output.sequence.file=alignment.txt,output.sequence.format=…,number_of_sites={length})` | Output format | Fasta | Fasta, Phylip, Clustal, Stockholm, Mase |
| `--seed=…` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example tree has 6 primates (human, chimp, gorilla, orangutan, macaque, baboon). The run writes `alignment.txt` (3087 bytes) and `bppseqgen_log.txt` (2149 bytes, which is the program's standard output).

The log is the record of what was simulated. It reports `Number of leaves: 6`, then the four gamma categories for alpha 0.5, each with probability 0.25:

| Category | Rate |
|---|---|
| 0 | 0.0334 |
| 1 | 0.2519 |
| 2 | 0.8203 |
| 3 | 2.8944 |

The mean rate is 1. The slowest class changes sites 87 times slower than the fastest. The log then confirms `HKY85.kappa=2` and `theta=0.5`, and ends with `Number of sites: 500`. It also warns `Parameter root.data not specified. Default used instead`, so the root sequence is the default one and no alignment supplies it.

The alignment is FASTA with 100 characters per line, 5 lines per sequence. Human to macaque is a path of 0.0678 substitutions per site, so about 34 differences are expected in 500 sites. The run shows 35 (14 transitions, 21 transversions). Across all six taxa, 57 of 500 columns vary.

## Your own runs

Changes below keep the example tree and seed 42 unless stated. Counts are for this one seed, so they show a direction and carry no average over seeds.

**Rate variation, alpha 0.05 and 100.** Variable columns went from 57 (alpha 0.5) to 44 at alpha 0.05 and to 68 at alpha 100. Strong variation puts the changes in few sites. Human to macaque differences were 26 at 0.05 and 37 at 100.

**Transition bias, kappa 20.** Human to macaque split into 29 transitions and 4 transversions, against 14 and 21 at kappa 2.

**GC content, theta 0.9.** Mean GC across the six sequences was 0.914, against 0.515 with theta 0.5.

**Output format, Phylip.** The header line reads `6 500`, followed by each name and its sequence, 100 characters per line, with continuation lines indented.

**Reproducibility.** Seed 42 twice gave identical files. A different seed (7) gave 66 variable columns and 29 human-macaque differences.

## Pitfalls

- **Sequence file goes where `output.sequence.file` says.** Standard output carries only the log. Redirect it if you want to keep it.
- **A wrong tree path fails with a short error.** With a misplaced argument the log said `File does not exists: /work/in/500` and no alignment was written. Read the first lines of the log when no alignment appears.
- **Branch lengths are used as given.** The example tree is shallow (maximum root-to-tip about 0.05), so only 57 of 500 sites vary. Rescale your tree if you want more divergence.
- **Set `--seed`.** Reruns with the same seed gave identical files in the check above.
- **Option numbers must match.** `process1` points at `model=1` and `tree=1`. If you add a second model, give it `model2` and link it in its own process.
- **The recipe fixes `theta1` and `theta2` at 0.5 and gamma at 4 categories.** Edit the command if you need other values.

## Further reading

- BppSuite manual (includes the bppseqgen section): https://pbil.univ-lyon1.fr/bpp-doc/bppsuite/bppsuite.html
- Source and releases: https://github.com/BioPP/bppsuite
- Bio++ installation: https://github.com/BioPP/bpp-documentation/wiki/Installation
- First Bio++ paper, as cited on the project page: https://doi.org/10.1186/1471-2148-8-255
- The Bio++ libraries paper: https://doi.org/10.1093/molbev/mst097

---

Cite: Bio++ Development Group. Bio++ Program Suite (bppseqgen), https://github.com/BioPP/bppsuite

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bppseqgen).
