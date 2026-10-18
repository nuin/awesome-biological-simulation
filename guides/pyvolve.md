# Pyvolve

> Simulate nucleotide, amino-acid or codon sequence alignments along an input phylogeny (Newick) under a continuous-time Markov substitution model.

Licence: BSD-2-Clause · [Source code](https://github.com/sjspielman/pyvolve)

## What it simulates

Pyvolve is a Python module that evolves sequences along a Newick tree under a continuous-time Markov model. It supports nucleotide, amino-acid and codon models. You build a model, attach it to a partition of sites, and give both to an evolver that walks the tree from a random root and returns the tip alignment.

The recipe wraps that in one script, `run_pyvolve.py`. Three model families are available:

- **Nucleotide:** a model with a transition/transversion ratio kappa.
- **Amino acid:** the JTT, WAG or LG matrix.
- **Codon:** the MG model with kappa and omega (dN/dS), so nonsynonymous changes are scaled by omega.

Key assumptions: sites are independent, one model covers the whole tree and all sites in a partition, and there are no insertions or deletions. Rate variation across sites is optional and gamma-distributed.

## When to use it

Use Pyvolve for codon evolution under a chosen dN/dS, for protein sequences with a standard matrix, or when you want to script several partitions with different models from Python.

Alternatives:

- [Seq-Gen](seq-gen.md) is a one-line command for HKY, GTR and protein matrices. It has no codon model.
- [Bio++ bppseqgen](bppseqgen.md) fits when you want the model written as a text description.
- [SimProt](simprot.md) fits when your question involves indels.

## Install it yourself

Conda, pinned to 1.1.0:

```bash
conda create -n pyvolve -c conda-forge -c bioconda pyvolve=1.1.0
conda activate pyvolve
```

The command resolves (pyvolve 1.1.0, 88 MB of dependencies). The project README also gives `pip install pyvolve`. Biopython, SciPy and NumPy are required.

Minimal use of the Python API, with gamma rate variation:

```python
import pyvolve
tree = pyvolve.read_tree(file="tree.nwk")
model = pyvolve.Model("nucleotide", {"kappa": 2}, alpha=0.5, num_categories=4)
part = pyvolve.Partition(models=model, size=500)
evolver = pyvolve.Evolver(tree=tree, partitions=part)
evolver(seqfile="alignment.fasta", ratefile="site_rates.txt",
        infofile="model_info.txt", seed=42)
```

## Run the tested example

This recipe builds Pyvolve in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 1 s.

1. Download [pyvolve-recipe.tar.gz](https://biosimhub.pages.dev/guides/pyvolve/pyvolve-recipe.tar.gz) (Dockerfile, run_pyvolve.py, example tree.nwk, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pyvolve-recipe.tar.gz
   cd pyvolve
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pyvolve:1.1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pyvolve:1.1.0 python /opt/run_pyvolve.py --tree /work/in/tree.nwk \
    --model nucleotide --aa-matrix JTT --length 500 \
    --kappa 2 --omega 0.5 --alpha 0 --categories 4 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `alignment.fasta` | 2.5 KB |
| `model_info.txt` | 86 B |
| `run_log.txt` | 45 B |

<details><summary>First lines of <code>alignment.fasta</code></summary>

```
>A
CCTGATTTACCTGTCAGACGTCTTTAGTAGGTCCAAACAGGTGTATCCGAAATGGTCGAA
GCGTGGGCACACTGACCGGTGCTATAGCACAGCCAGCAGTAGCTTGCCTTCAGGTCTGCG
GGGCGCCAATTTGCTATCCACCTGCCAGCATTAGACCAGTATAAGCTTCGCGTTAACTTG
TTACTGCTGCTAATAAGTACTTGAAAAGAGTGATGGAATCACCTCGAGGAACTGTTCTAA
ATAAGTGCCCGTCAAGTAATATCGTACTAAGAAGACCGTTAAAAGGACGATATACTCTTG
TAGGTCCGCTACTACCCACTTCAGTATGGCGAGTGGAGATATTGTTTCGCGAGGCATTCG
TAAAGCTGCTTGTCGATCCGGCTTTCGTACGCGCACTCCCCCGATTTTATGGATGCATAT
GAAAGTAGATTTATAGAGGTTAGACGTGAGATGGAATCTGGATCGGGTAGGCAACCCTGC
TAGCACTAGGCGGCTGCATG
>B
TTTGATTTACCTGTCAGGCGTCTTTACTAGGTCCAAACAGTTGTTTCCGAAATGGTCGAA
```

</details>

<details><summary>First lines of <code>model_info.txt</code></summary>

```
Partition_Index	Model_Name	Rate_Category	Rate_Probability	Rate_Factor
1	None	1	1.0	1.0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
model=nucleotide sites=500 alpha=0.0 seed=42
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--model` | Sequence type | nucleotide | nucleotide, amino_acid, codon |
| `--length` | Sites (codons for the codon model) | 500 | 10 to 20000 |
| `--aa-matrix` | Amino-acid matrix | JTT | JTT, WAG, LG |
| `--kappa` | Transition/transversion ratio (kappa) | 2 | 0.1 to 50 |
| `--omega` | dN/dS (omega | 0.5 | 0 to 10 |
| `--alpha` | Gamma shape for rate variation (0 = none) | 0 | 0 to 50 |
| `--categories` | Gamma rate categories | 4 | 2 to 20 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example tree is `((A:0.1,B:0.1):0.05,(C:0.12,D:0.08):0.07,E:0.2);`, five taxa, run as nucleotide, 500 sites, kappa 2, seed 42.

- `alignment.fasta` (2560 bytes): five sequences of 500 bases, 60 per line. Of 500 columns, 265 vary. Taxa A and E are 0.35 substitutions per site apart and differ at 153 sites (69 transitions, 84 transversions).
- `model_info.txt` (86 bytes): one row, rate category 1 with probability 1.0 and rate factor 1.0. This means no rate variation.
- `run_log.txt` (45 bytes): `model=nucleotide sites=500 alpha=0.0 seed=42`.

With alpha above 0 the evolver also writes a site-rate file, and `model_info.txt` lists one row per gamma category. The script wraps four calls: `pyvolve.read_tree`, `pyvolve.Model`, `pyvolve.Partition` and `pyvolve.Evolver`.

## Your own runs

- **Codon model, omega 0.1 against 1.** Run with 300 codons (900 bases) with kappa 2. Counting codons that differ between taxa A and E: at omega 0.1 there were 69 synonymous and 22 nonsynonymous differences. At omega 1 there were 23 synonymous and 73 nonsynonymous. Purifying selection removes most amino-acid changes while synonymous ones accumulate.

- **Protein, WAG, 200 sites.** The alignment holds amino-acid letters, for example `SQTQWYSSDVIV...` for taxon A.

- **Gamma rate variation with alpha 0.5.** Set `--alpha 0.5` in the recipe. `model_info.txt` then lists four categories with probability 0.25 each and rate factors 0.0334, 0.2519, 0.8203 and 2.8944. `site_rates.txt` put 132, 121, 126 and 121 of the 500 sites in categories 1 to 4. Variable columns dropped from 265 to 182, because most sites now evolve slowly.

## Pitfalls

- **Rate variation is a keyword argument.** In your own scripts pass `alpha` and `num_categories` to `pyvolve.Model(...)` as keyword arguments, as in the Python example above. Put inside the parameter dictionary they are ignored without an error, and every site stays in one category.
- **Codon length is in codons.** `--length 300` for the codon model gives sequences of 900 bases.
- **The seed must be an integer.** The source asserts `isinstance(seed, int)`. Two runs with seed 42 gave byte-identical alignments.
- **Tree needs branch lengths.** The tree reader takes them from the Newick file. Rescale the tree if you want more or less divergence; `Evolver` also takes `scale_tree`.
- **Output format is FASTA unless you ask otherwise.** `seqfmt` accepts any Biopython alignment format, such as `phylip-relaxed`.
- **Rate files are separate.** The per-site category file and the per-category rate file are two outputs; read both to know how fast each site evolved.

## Further reading

- Project and README: https://github.com/sjspielman/pyvolve
- API documentation: https://sjspielman.github.io/pyvolve/
- User manual (PDF): https://github.com/sjspielman/pyvolve/blob/master/user_manual/pyvolve_manual.pdf
- Spielman SJ, Wilke CO (2015). Pyvolve: a flexible Python module for simulating sequences along phylogenies. PLoS ONE 10(9):e0139047. https://doi.org/10.1371/journal.pone.0139047

---

Cite: Spielman SJ, Wilke CO (2015). Pyvolve, a flexible Python module for simulating sequences along phylogenies. PLoS ONE 10:e0139047. doi:10.1371/journal.pone.0139047

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pyvolve).
