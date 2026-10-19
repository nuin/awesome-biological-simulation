# AliSim (IQ-TREE 2)

> Simulate DNA alignments along a tree under the HKY model with gamma rate variation and insertions and deletions, using the AliSim module of IQ-TREE.

Licence: GPL-2.0-only · [Source code](https://github.com/iqtree/iqtree3)

## What it simulates

AliSim is the sequence-alignment simulator built into IQ-TREE. It evolves a root sequence down a phylogenetic tree and returns the tip sequences as a multiple sequence alignment. It handles DNA, amino-acid, codon, binary and morphological data. Models include the standard substitution models, rate variation across sites (invariant sites, discrete or continuous gamma, free-rate), mixture and non-reversible models, and insertions and deletions.

You give a tree with branch lengths, a model string such as `HKY{2.0}+F{0.2/0.3/0.1/0.4}+G4{0.5}`, and optionally a root sequence length. Branch lengths are expected substitutions per site. The tree may contain multifurcations.

The authors describe an approach that adapts between a rate-matrix method and a probability-matrix method for speed. Their paper reports one million sequences or sites in 1.3 hours using 1.3 GB of memory.

Key assumptions: sites evolve independently under the model you give, the tree is fixed, and without indel rates the alignment has no gaps.

## When to use it

Use AliSim to generate alignments with a known tree and model, for example to test tree inference, model selection or a parametric bootstrap, or when you need indels or complex mixtures in one tool.

- Use [Seq-Gen](seq-gen.md) for a one-line HKY, GTR or protein simulation with no indels.
- Use [Pyvolve](pyvolve.md) for codon models with a chosen dN/dS from Python.
- Use [Bio++ bppseqgen](bppseqgen.md) when you want the model written as a text description.
- Use [SimProt](simprot.md) for protein evolution with indels.

## Install

IQ-TREE is GPL-2.0 licensed. The current release is v3.1.4 (September 2026). Bioconda builds it for linux-64, linux-aarch64, osx-64 and osx-arm64, and installs the command `iqtree3`, with `iqtree` as a link:

```bash
conda create -n iqtree -c conda-forge -c bioconda iqtree=3.1.4
conda activate iqtree
iqtree3 --version
```

The AliSim page says to use IQ-TREE 2.4.0 or later. In IQ-TREE 2 the command is `iqtree2 --alisim`, and it should accept the same options. The catalog entry names IQ-TREE 2. This guide installs version 3 because that is the version the project now documents and the current Bioconda build.

## A first run

Adapted from the AliSim tutorial (https://iqtree.github.io/doc/AliSim). The commands have not been run for this guide. With the tree file `tree.nwk`:

```
(A:0.3544,(B:0.1905,C:0.1328):0.0998,D:0.0898);
```

this command simulates a Jukes-Cantor alignment and writes `alignment.phy`:

```bash
iqtree3 --alisim alignment -m "JC" -t tree.nwk
```

The tutorial shows the output as a PHYLIP file with a header of 4 sequences by 1000 sites. Add `-seed 123` to make the run reproducible, `--length 5000` to change the root length, `--out-format fasta` for FASTA, and `--indel 0.03,0.1` for insertion and deletion rates relative to substitutions.

The recipe below simulates 1000 sites on an 8-tip tree under HKY with kappa 2, fixed base frequencies, 4 gamma categories and indels. A short shell script builds the model string from the numbers, because the server does not pass braces in arguments. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds AliSim (IQ-TREE 2) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.6 s.

1. Download [alisim-recipe.tar.gz](https://biosimhub.pages.dev/guides/alisim/alisim-recipe.tar.gz) (Dockerfile, run_alisim.sh, example tree.nwk, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf alisim-recipe.tar.gz
   cd alisim
   sh run.sh
   ```

![Terminal recording of the AliSim (IQ-TREE 2) example run](https://biosimhub.pages.dev/media/alisim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/alisim:3.1.4 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/alisim:3.1.4 sh /opt/run_alisim.sh /work/in/tree.nwk 1000 2 0.5 0.03 0.1 42 > out/alisim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `alisim_log.txt` | 1.8 KB |
| `input.nwk` | 94 B |
| `input.nwk.log` | 1.8 KB |
| `sim.fa` | 8.7 KB |
| `sim.unaligned.fa` | 7.3 KB |

<details><summary>First lines of <code>alisim_log.txt</code></summary>

```
IQ-TREE version 3.1.4 for Linux ARM 64-bit built Sep 29 2026
Developed by Bui Quang Minh, Thomas Wong, Nhan Ly-Trong, Huaiyan Ren
Contributed by Lam-Tung Nguyen, Dominik Schrempf, Chris Bielow,
Olga Chernomor, Michael Woodhams, Diep Thi Hoang, Heiko Schmidt

Host:    01e43f28a295 (SSE4.2, 7 GB RAM)
Command: iqtree3 --alisim sim -m HKY{2}+F{0.3/0.2/0.2/0.3}+G4{0.5} -t input.nwk --length 1000 --indel 0.03,0.1 --out-format fasta -seed 42
Seed:    42 (Using SPRNG - Scalable Parallel Random Number Generator)
Time:    Sun Oct 18 04:46:17 2026
Kernel:  SSE2 - 1 threads (16 CPU cores detected)

[Alignment Simulator] Executing
```

</details>

<details><summary>First lines of <code>input.nwk</code></summary>

```
((A:0.10,B:0.12):0.05,(C:0.08,D:0.10):0.07,((E:0.15,F:0.11):0.04,(G:0.09,H:0.13):0.06):0.03);
```

</details>

<details><summary>First lines of <code>input.nwk.log</code></summary>

```
IQ-TREE version 3.1.4 for Linux ARM 64-bit built Sep 29 2026
Developed by Bui Quang Minh, Thomas Wong, Nhan Ly-Trong, Huaiyan Ren
Contributed by Lam-Tung Nguyen, Dominik Schrempf, Chris Bielow,
Olga Chernomor, Michael Woodhams, Diep Thi Hoang, Heiko Schmidt

Host:    01e43f28a295 (SSE4.2, 7 GB RAM)
Command: iqtree3 --alisim sim -m HKY{2}+F{0.3/0.2/0.2/0.3}+G4{0.5} -t input.nwk --length 1000 --indel 0.03,0.1 --out-format fasta -seed 42
Seed:    42 (Using SPRNG - Scalable Parallel Random Number Generator)
Time:    Sun Oct 18 04:46:17 2026
Kernel:  SSE2 - 1 threads (16 CPU cores detected)

[Alignment Simulator] Executing
```

</details>

<details><summary>First lines of <code>sim.fa</code></summary>

```
>A        
GCTACTGGATTAAATCTTTAAAGGCCATTGAAACGT-CTTTCGGTAGGACTAAATC-AGTAAGTTGA-TATAGTTTCATTTACACTTATACTGATTAAAGCCTGTGAAAAGGATAAGGGTAAATAG-TAGAAAACCATAGGGTAAGAT-TATGGGCATTTGAACATTTGCGGTAGCT------------------ATTGT
>B        
GCTATGGGATTAAATCTTTAAAGCCCATC---------TTTCGTCAGGACTAAGTC-AGCATGATGAGTATAGTTTAATTTACACTTATACCGATTAAAGCCTGTGAAA--GATAAGGGTAAATAGTTAGAAC--CATAGGGTAAGAT-TAAGGGCATTTGTACGTTTGCAGTAGCT------------------ATTGT
>C        
GCTATGGGTTTAAATCTGCAAAGGCTATAGTAATGT-CTTTTGTCATGGCTATTT--TGTAAGATAAGAATATTTTAATTTACCATCATACCGATCAAAGCCTGTGTATAGGATAA---CAAAT-------------------------------------GACATC
```

</details>

<details><summary>First lines of <code>sim.unaligned.fa</code></summary>

```
>A
GCTACTGGATTAAATCTTTAAAGGCCATTGAAACGTCTTTCGGTAGGACTAAATCAGTAAGTTGATATAGTTTCATTTACACTTATACTGATTAAAGCCTGTGAAAAGGATAAGGGTAAATAGTAGAAAACCATAGGGTAAGATTATGGGCATTTGAACATTTGCGGTAGCTATTGTATAATTTGTTGTCATAGTCTAAC
>B
GCTATGGGATTAAATCTTTAAAGCCCATCTTTCGTCAGGACTAAGTCAGCATGATGAGTATAGTTTAATTTACACTTATACCGATTAAAGCCTGTGAAAGATAAGGGTAAATAGTTAGAACCATAGGGTAAGATTAAGGGCATTTGTACGTTTGCAGTAGCTATTGTGTAATTTGTTGTCATAGTCTAACTTCGCGTTTC
>C
GCTATGGGTTTAAATCTGCAAAGGCTATAGTAATGTCTTTTGTCATGGCTATTTTGTAAGATAAGAATATTTTAATTTACCATCATACCGATCAAAGCCTGTGTATAGGATAACAAATGACATCGGCGGTAGCTACTTTTTAATTAGTTCTCATAGTCTGTTCGCATTTTGGGGTTGCCAGTGACATTAAGAGACACATT
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `length` | Root sequence length | 1000 | 10 to 100000 |
| `kappa` | Transition/transversion ratio (kappa) | 2 | 0.1 to 50 |
| `alpha` | Gamma shape (4 rate categories) | 0.5 | 0.05 to 100 |
| `insertion` | Insertion rate relative to substitutions | 0.03 | 0.001 to 1 |
| `deletion` | Deletion rate relative to substitutions | 0.1 | 0.001 to 1 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

With `--alisim sim --out-format fasta`, AliSim writes `sim.fa`. The recipe collects every file that starts with `sim`.

- `sim.fa` has one sequence per tip, named after the tree's tip labels. Gaps (`-`) mark positions deleted in that lineage or inserted in other lineages.
- With `--indel`, the tutorial says AliSim also writes `sim_withoutgaps.fa`, the same sequences with the gaps removed. `--no-export-sequence-wo-gaps` turns that off.
- IQ-TREE also writes a log file with the run messages.

The tutorial's note on indels matters here: the aligned length can exceed `--length` because insertions add columns. Compare the number of columns with the root length you asked for. For a rate-variation check, count constant columns. Under `+G4{0.5}` many columns barely change and a few change often, so you should see more constant columns than under a single rate.

## Pitfalls

- **Set a seed.** Without `-seed`, AliSim uses the CPU clock, and two runs started together can give identical alignments.
- **Branch lengths are in substitutions per site.** Long branches saturate, so the alignment looks random.
- **Unspecified frequencies are random.** For `HKY{2.0}` with no `+F`, AliSim draws base frequencies from empirical distributions. Give `+F{...}` for a fixed answer.
- **Model strings need quotes.** The braces and slashes would otherwise be read by the shell.
- **Indel size distribution.** The default is Zipfian with exponent 1.7 and a maximum of 100. Change it with `--indel-size`.
- **Version names.** A script written for `iqtree2` needs the name `iqtree3` to run on version 3, and the reverse.
- **Multiple outputs.** `--num-alignments 3` writes `sim_1`, `sim_2` and `sim_3` files, not one.

## Further reading

- Tutorial: https://iqtree.github.io/doc/AliSim
- Source: https://github.com/iqtree/iqtree3
- Ly-Trong N, Naser-Khdour S, Lanfear R, Minh BQ (2022). AliSim: a fast and versatile phylogenetic sequence simulator for the genomic era. Molecular Biology and Evolution 39:msac092. https://doi.org/10.1093/molbev/msac092
- Ly-Trong N, Barca GMJ, Minh BQ (2023). AliSim-HPC: parallel sequence simulator for phylogenetics. Bioinformatics 39:btad540. https://doi.org/10.1093/bioinformatics/btad540

---

Cite: Ly-Trong N, Naser-Khdour S, Lanfear R, Minh BQ (2022). AliSim: a fast and versatile phylogenetic sequence simulator for the genomic era. Molecular Biology and Evolution 39:msac092. doi:10.1093/molbev/msac092

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/alisim).
