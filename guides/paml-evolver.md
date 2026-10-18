# PAML evolver

> Simulate nucleotide sequence alignments along a given tree under JC69 to REV substitution models with discrete-gamma rate variation, driven by a PAML control file.

Licence: GPL-3.0-only · [Source code](https://github.com/abacus-gene/paml)

## What it simulates

`evolver` is the simulation program inside PAML. It simulates sequence alignments along a phylogeny you supply, and it can also generate random trees. Three simulators share the program:

- **Nucleotides (option 5):** JC69, K80, F81, F84, HKY85, T92, TN93 or REV (GTR), with optional discrete-gamma rate variation across sites.
- **Codons (option 6):** codon models with a dN/dS ratio (omega), including branch, site and branch-site variants.
- **Amino acids (option 7):** empirical matrices with optional gamma rates.

Each run writes many replicate data sets into one file. The guide covers option 5. Sites are independent, there are no insertions or deletions, and one model applies to all branches unless you pick a codon branch model.

## When to use it

Use `evolver` to make test data for the other PAML programs (`baseml`, `codeml`, `mcmctree`), to check a method against data with a known truth, or to study how tree length and branch lengths affect an estimate. It reads its parameters from a plain control file, so a run is fully described by one file.

Alternatives:

- [Pyvolve](pyvolve.md) takes the same kind of inputs from Python and adds partitions with different models.
- [Seq-Gen](seq-gen.md) is a single command for nucleotide and protein alignments.
- [Bio++ bppseqgen](bppseqgen.md) writes the model as a text description and offers more rate-variation options.

## Install

PAML 4.10.10 is on Bioconda for linux-64, linux-aarch64, osx-64 and osx-arm64 (checked on anaconda.org):

```bash
conda create -n paml -c conda-forge -c bioconda paml=4.10.10
conda activate paml
```

The package puts `evolver`, `baseml`, `codeml`, `mcmctree` and the other PAML programs on the path. PAML is released under the GPL v3. The project wiki also describes building from source with `make -f Makefile` in the `src/` folder: https://github.com/abacus-gene/paml/wiki/Installation

## A first run

The control file `MCbase.dat` has two parts. The first lines are read by the program: output format, random seed, number of sequences, sites and replicates, tree length, the tree, the model number, the substitution parameters, gamma shape and categories, and base frequencies in the order T, C, A, G. Everything after the line of equals signs is notes.

Adapted from the [Evolver wiki page](https://github.com/abacus-gene/paml/wiki/Evolver) and `examples/MCbase.dat` in the repository. The recipe below uses that example with 500 sites, 3 replicates and a seed of 123. Run it with the option number and the control file:

```bash
evolver 5 MCbase.dat
```

A tree length of `-1` tells `evolver` to use the branch lengths in the tree as given. A positive tree length rescales the branch lengths so they sum to that value. A model of 7 is REV, and its five rate parameters are listed in the file.

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds PAML evolver in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.2 s.

1. Download [paml-evolver-recipe.tar.gz](https://biosimhub.pages.dev/guides/paml-evolver/paml-evolver-recipe.tar.gz) (Dockerfile, example control.dat, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf paml-evolver-recipe.tar.gz
   cd paml-evolver
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/paml-evolver:4.10.10 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/paml-evolver:4.10.10 evolver 5 /work/in/control.dat > out/evolver_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `ancestral.txt` | 5.4 KB |
| `evolver.out` | 0 B |
| `evolver_log.txt` | 735 B |
| `mc.txt` | 8.3 KB |
| `siterates.txt` | 12.1 KB |

<details><summary>First lines of <code>ancestral.txt</code></summary>

```

Ancestral sequences generated during simulation (check against mc.txt)
((1, 2), 3, (4, 5));
   6..7     7..1     7..2     6..3     6..8     8..4     8..5  
[replicate 1]
     3    500
node6                           CTTTATAGCT GACCTGCAAA ATCAATTCCC CGATTGGTCG CCCCCGCCTT AACCCACCTT CCTCTCCTGC GGACCTAGTT AATGCACCTC ATACCTATCT TATAATCATC GACCTTGTTA CCAACACCTA AGTGCTGCAG TGCCACTTAT AAC
node7                           CTTTATAGCT GACCTGCAAA ATCAATTCCC CGATTGGTCG CCCCCACCTT AACCCACCTT CCTCTCCTGC GGACTTAGTT AATGCACCTC ATACCTATCT TATAATCATC GACCTTGTTA CCAACGCCTA AGTGCTGCAG TGCCACTTAT AAC
node8                           TTTTATAGCT GACCTGCAAA ATCAATTCCC CGATTGGTCG CCCCCGCCTT AACCCATCTC CCTCTCCTGC GGACTTAGTT AATGCATCTC ATACCTATCC TATAATCATC GACCTTGTTA CCAACACCTA AGTGCTGCAG TGCCACTTAT AAC

[replicate 2]
     3    500
```

</details>

<details><summary>First lines of <code>evolver_log.txt</code></summary>

```
EVOLVER in paml version 4.10.10, 29 Jan 2026

Reading options from data file /work/in/control.dat

Simulated data will go into mc.txt.

5 seqs, 500 sites, 3 replicate(s)
Seq file will be about 8K bytes.
tree length = 0.993

Model tree & branch lengths:
((Human: 0.056647, Chimpanzee: 0.071554): 0.028080, Gorilla: 0.075518, (Orangutan: 0.259783, Gibbon: 0.400727): 0.100618);
```

</details>

<details><summary>First lines of <code>mc.txt</code></summary>

```


5 500 

Human       CTTTATAGCT GACCTGCAAA ATCAATTCCC CGATTGGTCG CCCCCACCTT AACCCACCTT CCTCTCCTGC GGACTTAGTT AATGCACCTT ATACCTATCT TATAATCATC GACCTTGTTA CCAACACCTA AGTGCTGCAG TGCCACTTAT AACACATTAC GCAGATTCTC T
Chimpanzee  CTTTGTAGCT GACCTGCGAA ATCAATTCCC CGATTGGTTG CCCCCACCTC AACCCACCCC CCTCTCCTGC GGACCTAGTT AATGCACATT ATACCTATCT CATAATCATC GACCTTGTTA CCAACGCTTA AGTGCTGCAG TGCTACTTAT AACTCATTAC GCAGATTCTC T
Gorilla     TTTTATAGCT GACCTGCAAA ATCAATTCCC CGATTGGTTG CCCCCGCCCC AACCCACCTT TCTCTCCTGC GGACCTAGTT AATGCACCTT ATACCTATCT CATAATCATC GACCCTGTTA CCAACACCTA AGTGCTGCAG TGCCATTTAT AGCACATTAC GCAGATTCTC T
Orangutan   CTTTCTAGTT GACCTGCAGA ATCAATCCCC CGACTAGTTG CCCCCTCCTT AACCCACCTC TCTCTTTTGC AGACGTAGTT AATGTACCTC ATACCTATCC TATAATCATC GACCTCGTTA CCAACGTCTA AGTGCTGCAG TGCCACTTAT AACACATCGC GTAGATTCTC T
Gibbon      CTTTATAACT AATCTGCAAA ATCAGTTCCC CGGTTAGTTG CCCCCGCCTC AACCCACCTC CCTATCCTGC GGACCTCGTT AATACATCTC ATACCTATCC CATAATCATC GATCC
```

</details>

<details><summary>First lines of <code>siterates.txt</code></summary>

```

Rates for sites

[replicate 1]
 3.9783  0.1908  0.8031  0.0009  3.9783  0.8031  0.0009  0.8031  0.1908  0.1908 

 0.8031  0.0009  0.1908  0.0270  0.0009  0.1908  0.0270  3.9783  0.8031  0.0270 

 0.0270  0.1908  0.0270  0.0009  3.9783  0.0270  0.8031  0.0270  0.1908  3.9783 

 0.0009  0.8031  0.1908  0.0270  0.0009  3.9783  0.1908  0.0009  3.9783  0.1908 

```

</details>


## Reading the output

The outputs below follow the program source and the wiki. The recipe's recorded output files are listed with the recipe.

- `mc.txt`: the alignments, one block per replicate, in PAML format (format option 0). Format option 2 or 3 writes `mc.nex` instead, for PAUP*.
- `ancestral.txt`: the simulated sequence at every internal node of each replicate, so the true ancestors can be compared with reconstructions.
- `siterates.txt`: the relative rate drawn for each site, written when the gamma shape is above 0.
- `evolver.out`: output of the tree options (1 to 4 and 8).
- The screen output echoes the values the program read. Check it, because a misplaced number changes the model without an error.

## Pitfalls

- **Base frequencies have a fixed order.** They are T, C, A, G, not A, C, G, T.
- **Kappa means different things.** In HKY85 a value of 1 means no transition bias. In F84 a value of 0 means none. TN93 needs two values and REV needs five.
- **Only the first block is read.** Keep every parameter line in place and change only the values. The notes after the equals signs are ignored.
- **Gamma needs both numbers.** Use alpha 0 for equal rates across sites. A categories value of 0 selects the continuous gamma.
- **Trees carry branch lengths in substitutions per site.** The names in the tree become the sequence names.
- **The seed is a single integer.** The file asks for an odd number. Keep it fixed to repeat a run.
- **Large runs grow fast.** The program prints the expected size of the sequence file before it starts.

## Further reading

- Project and README: https://github.com/abacus-gene/paml
- Evolver wiki page: https://github.com/abacus-gene/paml/wiki/Evolver
- Example control files: https://github.com/abacus-gene/paml/tree/master/examples (`MCbase.dat`, `MCcodon.dat`, `MCaa.dat`, `MCbaseRandomTree.dat`)
- Yang Z (2007). PAML 4: Phylogenetic Analysis by Maximum Likelihood. Mol Biol Evol 24:1586-1591. https://doi.org/10.1093/molbev/msm088

---

Cite: Yang Z (2007). PAML 4: Phylogenetic Analysis by Maximum Likelihood. Mol Biol Evol 24:1586-1591. doi:10.1093/molbev/msm088

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/paml-evolver).
