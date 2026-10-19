# DendroPy

> Simulate a birth-death or coalescent tree, then evolve a DNA alignment on it under the HKY model, with DendroPy's Python simulation routines.

Licence: BSD-3-Clause · [Source code](https://github.com/jeetsukumaran/DendroPy)

## What it simulates

DendroPy is a Python library for phylogenetic computing. Most of it reads, writes, edits and summarises trees and character matrices in formats such as NEXUS, Newick, NeXML, PHYLIP and FASTA. A smaller part simulates. This guide covers the simulation part.

For trees, the `dendropy.simulate.treesim` module offers a continuous-time birth-death process (`birth_death_tree`), a discrete-time birth-death process, a pure-birth tree, Kingman coalescent trees (`pure_kingman_tree`) and a coalescent tree contained in a species tree (`contained_coalescent_tree`). For characters, `dendropy.model.discrete` evolves DNA sequences down a tree under the HKY85 or Jukes-Cantor model with a function such as `hky85_chars`. The Seq-Gen primer page says this native code is pure Python and therefore slow, and that DendroPy can call Seq-Gen for more models.

Key assumptions: a birth-death tree has constant per-lineage rates unless you ask for evolving rates, coalescent trees come from a neutral population of one size, and sites evolve independently under one substitution model.

## When to use it

Use DendroPy when the simulation is one step in a Python workflow that also parses, edits or measures trees, for example simulating many trees, computing a statistic and saving the results.

- Use [Seq-Gen](seq-gen.md) or [Pyvolve](pyvolve.md) when the sequence model is the main point, such as GTR, amino-acid or codon models.
- Use [msprime](msprime.md) or [ipcoal](ipcoal.md) for coalescent genealogies with recombination and large samples.
- Use [AliSim](alisim.md) for alignments with indels and complex mixtures.

## Install

DendroPy is BSD-3-Clause licensed. The current release is 5.1.1, on PyPI and Bioconda (noarch). It needs Python 3.7 or later:

```bash
python3 -m pip install dendropy==5.1.1
# or
conda create -n dendropy -c conda-forge -c bioconda dendropy=5.1.1
```

The project README gives `python -m pip install dendropy` and also names the conda-forge channel. Only PyPI and Bioconda were checked for this guide.

## A first run

Adapted from the Tree Simulation and Generation primer (https://jeetsukumaran.github.io/DendroPy/primer/treesims.html) and the docstring of `dendropy.model.discrete.hky85_chars`. The code has not been run for this guide.

```python
import random
from dendropy.simulate import treesim
from dendropy.model.discrete import hky85_chars

rng = random.Random(42)
tree = treesim.birth_death_tree(birth_rate=1.0, death_rate=0.5,
                                num_extant_tips=10, rng=rng)
tree.print_plot()
chars = hky85_chars(seq_len=500, tree_model=tree,
                    mutation_rate=0.1, kappa=2.0, rng=rng)
chars.write(path="alignment.fasta", schema="fasta")
```

The primer's own example uses `ntax=10`. DendroPy 5 still accepts `ntax` but marks it deprecated in favour of `num_extant_tips`. Growth stops when the tree has that many extant tips or reaches `max_time`. Extinct lineages are removed unless you ask to keep them.

The recipe below wraps this in a script with a choice of birth-death or coalescent trees. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds DendroPy in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.9 s.

1. Download [dendropy-recipe.tar.gz](https://biosimhub.pages.dev/guides/dendropy/dendropy-recipe.tar.gz) (Dockerfile, run_dendropy.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf dendropy-recipe.tar.gz
   cd dendropy
   sh run.sh
   ```

![Terminal recording of the DendroPy example run](https://biosimhub.pages.dev/media/dendropy/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/dendropy:5.1.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/dendropy:5.1.1 python /opt/run_dendropy.py --tree-model birth-death \
    --taxa 10 --birth-rate 1 --death-rate 0.5 \
    --pop-size 1 --length 500 --kappa 2 --mutation-rate 0.1 \
    --seed 42 > out/dendropy_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `alignment.fasta` | 5.0 KB |
| `dendropy_log.txt` | 24 B |
| `summary.txt` | 121 B |
| `tree.nwk` | 386 B |

<details><summary>First lines of <code>alignment.fasta</code></summary>

```
>T1
TAGGTTTGGCGCCCAAAGGAGAAACGTCGGTGACCAGCCTAGGAGTAAGAACTTTTAGGAATACCTTAAC
TTCGGTGCAAAGATACTGAGTTATCTGGAAGCCCGCCTCCTTGGAGGGACGACCTCTCGTGTATCTGACA
CGTGCTAGCAGATACGCATAAATTGACTAATGGCTTTGTAATACATTCGGGAACATATCTTTGGCATCGG
TCATCGCAGTTCGATAACCTGTGACTTCGACGGCAGAGCGAGATTGTGCCGGTTAGCGGATAATAATGTT
TGGACAGTTTCATCCGGAACGGTTCGTTACATCTTCTAACGACTAACAGCCCATCCTATGCCCCTTGGTT
GCCCGCGTTTGAGGACTACTACTCTCGCGATAATGAATGACTTCCCGTGTTCGTGTCTAGTATCGTTGAT
GCAACCCCTCAAGGGTTCTGCCTCCTGGTCCCCTCGTCGAACGGCGCCCTAGCGCAGCCCAGCGTGAGCG
TGTTCCCCAA

>T2
TAAGTTTGGGGCTTAAAGGAGAAACGCCAGTGACCAGCCTAGGAGTAATAACTACCAGGACTGCCTTAAC
```

</details>

<details><summary>First lines of <code>dendropy_log.txt</code></summary>

```
done 10 taxa, 500 sites
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
seed	42
tree_model	birth-death
taxa	10
tree_height_time_units	7.6751
expected_substitutions_root_to_tip	0.7675
sites	500
```

</details>

<details><summary>First lines of <code>tree.nwk</code></summary>

```
[&R] ((T1:1.605236007555839,(((T10:0,T3:0):0.15627176596877973,T2:0.15627176596877973):0.15941633916666442,T6:0.31568810513544415):1.2895479024203949):0.10257391809350587,((T4:1.472584516826539,(T7:0.
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--tree-model` | Tree model | birth-death | birth-death, coalescent |
| `--taxa` | Tips | 10 | 3 to 200 |
| `--birth-rate` | Birth rate (birth-death) | 1 | 1 to 10 |
| `--death-rate` | Death rate (birth-death | 0.5 | 0 to 0.9 |
| `--pop-size` | Population size (coalescent) | 1 | 0.01 to 1000000 |
| `--length` | Sites | 500 | 10 to 20000 |
| `--kappa` | Transition/transversion ratio (kappa) | 2 | 0.1 to 50 |
| `--mutation-rate` | Substitutions per site per tree time unit | 0.1 | 0.001 to 5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe writes three files:

- `tree.nwk`: the simulated tree in Newick form. The primer shows birth-death tips labelled `T1`, `T2` and so on, and the coalescent option in the recipe uses the same labels. Branch lengths are in the process's own time units.
- `alignment.fasta`: one DNA sequence per tip.
- `summary.txt`: the seed, tree model, number of tips, the tree height in time units, and the height times the mutation rate, which is the expected number of substitutions per site from root to tip.

Check the last number before reading anything into the alignment. If it is far above 1, sites are close to saturated and tips look unrelated. If it is near 0, most columns are constant.

## Pitfalls

- **Pass your own generator.** Without `rng`, DendroPy uses a global generator. Give the same `random.Random(seed)` to the tree and sequence functions to reproduce a run, as the recipe does.
- **Total extinction.** With a death rate close to the birth rate, every lineage can die out. The default `repeat_until_success=True` restarts the process, which can take long. Keep the death rate well below the birth rate.
- **Tree time units are not substitutions.** Birth-death branch lengths are in time. `mutation_rate` converts them into expected substitutions per site.
- **Coalescent scale.** `pure_kingman_tree` takes `pop_size`, and branch lengths scale with it.
- **Pure Python is slow for long alignments.** Move to Seq-Gen or Pyvolve for large simulations.
- **Taxon namespaces.** A tree and its character matrix must share one `TaxonNamespace`. The simulation functions do this for you. Trees read from separate files do not.

## Further reading

- Documentation: https://jeetsukumaran.github.io/DendroPy/
- Source: https://github.com/jeetsukumaran/DendroPy
- Moreno MA, Holder MT, Sukumaran J (2024). DendroPy 5: a mature Python library for phylogenetic computing. Journal of Open Source Software 9:6943. https://doi.org/10.21105/joss.06943
- Sukumaran J, Holder MT (2010). DendroPy: a Python library for phylogenetic computing. Bioinformatics 26:1569-1571. https://doi.org/10.1093/bioinformatics/btq228

---

Cite: Moreno MA, Holder MT, Sukumaran J (2024). DendroPy 5: a mature Python library for phylogenetic computing. Journal of Open Source Software 9:6943. doi:10.21105/joss.06943

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/dendropy).
