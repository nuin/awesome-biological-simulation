# simuPOP

> Forward-time Wright-Fisher simulation of a diploid population with mutation, recombination and optional selection, returning allele-frequency trajectories and heterozygosity.

Licence: GPL-2.0 · [Source code](https://github.com/BoPeng/simuPOP)

## What it simulates

simuPOP simulates a population forward in time, one generation after another, with every individual stored. The recipe here runs a diploid Wright-Fisher population of N individuals with several biallelic loci. Each generation the population is built by random mating from the previous one. Mating includes recombination between adjacent loci, symmetric mutation between the two alleles, and optional selection.

Input is a handful of numbers: population size, number of loci, generations, starting frequency of allele 1, mutation rate, recombination rate, selection coefficient and seed. Output is a CSV with the frequency of allele 1 at every locus in every generation, plus the heterozygosity averaged over loci.

Key assumptions of this recipe: generations do not overlap, mating is random, the population size is constant, and selection acts only on locus 0. The fitness of the three genotypes at locus 0 is 1, 1 + s/2 and 1 + s (additive, or genic, selection). Recombination rate 0.5 between neighbours means the loci are unlinked.

## When to use it

Use it to watch drift, mutation, selection and linkage act on a small population and to see how much one run varies from the next. Typical questions: how fast does heterozygosity fall at N = 200, how often does a neutral allele at 50% fix within 100 generations, how long does an allele with s = 0.1 take to sweep.

Alternatives on biosimhub:

- [fwdpy11](fwdpy11.md) fits better when you want a sampled VCF, the site frequency spectrum and diversity statistics from a neutral population with recombination.
- [SLiM](slim.md) fits better when you want to write the model yourself as a SLiM (Eidos) script and upload it.

## Install it yourself

simuPOP 1.1.17 is on conda-forge (builds listed for linux-64, osx-64 and win-64) and on PyPI (1.1.17 has wheels for macOS and a source archive; PyPI's newest release is 1.1.18).

```
conda create -n simupop -c conda-forge simupop=1.1.17
# or
pip install simuPOP==1.1.17
```

The recipe pins 1.1.17 so results match the example below. The build list comes from the anaconda.org package index.

A minimal simuPOP script, without the recipe's helper script. It starts 5 loci at frequency 0.5 and prints the frequency at locus 0 every 50 generations:

```python
import simuPOP as sp
sp.setOptions(seed=42)          # omit and every run differs
pop = sp.Population(size=200, loci=[5])
sp.initGenotype(pop, freq=[0.5, 0.5])
pop.evolve(
    initOps=sp.InitSex(),
    matingScheme=sp.RandomMating(),
    postOps=[sp.Stat(alleleFreq=[0], step=50),
             sp.PyEval(r'"gen %d freq %.3f\n" % (gen, alleleFreq[0][1])', step=50)],
    gen=100)
```

Without `setOptions`, two runs of this script printed gen 0 frequencies of 0.470 and 0.475. The reference is at https://bopeng.github.io/simuPOP/userGuide.html.

## Run the tested example

This recipe builds simuPOP in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.3 s. simuPOP has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [simupop-recipe.tar.gz](https://biosimhub.pages.dev/guides/simupop/simupop-recipe.tar.gz) (Dockerfile, run_simupop.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf simupop-recipe.tar.gz
   cd simupop
   sh run.sh
   ```

![Terminal recording of the simuPOP example run](https://biosimhub.pages.dev/media/simupop/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/simupop:1.1.17 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/simupop:1.1.17 python /opt/run_simupop.py --popsize 200 --loci 5 \
    --generations 100 --freq 0.5 --mut 0.0001 \
    --recomb 0.5 --sel 0 --seed 42 > out/simupop_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `allele_freqs.csv` | 4.7 KB |
| `simupop_log.txt` | 74 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/simupop/result-dark.png"><img src="https://biosimhub.pages.dev/media/simupop/result.png" alt="Plot of the simuPOP example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>allele_freqs.csv</code></summary>

```
generation,freq_locus0,freq_locus1,freq_locus2,freq_locus3,freq_locus4,mean_heterozygosity
0,0.52,0.5225,0.5225,0.4675,0.4775,0.5
1,0.4975,0.485,0.5125,0.485,0.4925,0.509
2,0.5,0.5025,0.515,0.4625,0.495,0.484
3,0.5025,0.4625,0.52,0.4525,0.5275,0.49000000000000005
4,0.49,0.4575,0.4875,0.445,0.5325,0.475
5,0.4625,0.45,0.555,0.44,0.5675,0.49400000000000005
6,0.475,0.4275,0.515,0.4125,0.595,0.516
7,0.4925,0.435,0.5325,0.4,0.5925,0.503
8,0.5075,0.415,0.5675,0.3975,0.59,0.513
9,0.48,0.4525,0.51,0.3725,0.56,0.496
10,0.5025,0.435,0.51,0.3925,0.5825,0.487
```

</details>

<details><summary>First lines of <code>simupop_log.txt</code></summary>

```
generations 100 mean heterozygosity 0.288
selected locus frequency 0.8925
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--popsize` | Diploid population size | 200 | 10 to 20000 |
| `--loci` | Number of biallelic loci | 5 | 1 to 50 |
| `--generations` | Generations | 100 | 1 to 2000 |
| `--freq` | Initial frequency of allele 1 | 0.5 | 0 to 1 |
| `--mut` | Symmetric mutation rate per locus | 0.0001 | 0 to 0.1 |
| `--recomb` | Recombination rate between adjacent loci | 0.5 | 0 to 0.5 |
| `--sel` | Selection coefficient for allele 1 at locus 0 (additive) | 0 | -0.9 to 5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper script `run_simupop.py` wraps the same API. It creates the population, draws starting genotypes with `initGenotype`, adds a `MapSelector` for locus 0 when `--sel` is not zero, adds `SNPMutator(u=mut, v=mut)`, mates with `RandomMating` (using `Recombinator` when `--recomb` is above zero), and records statistics after every generation.

`allele_freqs.csv` has a header and 101 rows, generation 0 to 100 (4814 bytes). Columns are `generation`, `freq_locus0` to `freq_locus4`, and `mean_heterozygosity`.

- Generation 0 is not exactly 0.5. Locus 0 starts at 0.52 because `initGenotype` samples genotypes at random.
- Locus 0 drifts to 0.8725 at generation 50 and 0.8925 at generation 100. With `--sel 0` this is pure drift.
- Mean heterozygosity falls from 0.5 to 0.288.

`simupop_log.txt` repeats the end state: `generations 100 mean heterozygosity 0.288` and `selected locus frequency 0.8925`. The second line names locus 0 even when selection is off.

Drift predicts heterozygosity falling by a factor of (1 - 1/2N) per generation. For N = 200 and 100 generations the expected mean is 0.389, so 0.288 is a low draw for 5 loci. With N = 2000 (below) the observed 0.4889 sits next to the expected 0.4877.

## Your own runs

All runs keep the example's other values.

- `--popsize 2000`: locus 0 ends at 0.555 and heterozygosity at 0.4889. Larger populations drift less.
- `--sel 0.1`: locus 0 reaches 0.95 at generation 50 and 1.0 at generation 100. Mean heterozygosity at the end is 0.355 because the selected locus has no variation left.
- `--seed 43` with the example settings: locus 0 ends at 0.2175 and heterozygosity at 0.312. The same settings gave 0.8925 with seed 42.
- `--mut 0.01`: heterozygosity ends at 0.474 and locus 0 at 0.4875. Frequent mutation keeps both alleles in the population.

## Pitfalls

- One run is one draw. Seed 42 and seed 43 end at 0.8925 and 0.2175 for the same neutral locus. Run many seeds before drawing a conclusion.
- `mean_heterozygosity` averages all loci, including the selected one. In the `--sel 0.1` run locus 0 ends fixed at 1.0, so it adds zero heterozygosity to the average.
- `--sel` acts on locus 0 only, and positive values favour allele 1. Other loci stay neutral.
- `--recomb 0.5` means free recombination. Values near 0 make loci move together, which matters only with selection on locus 0.
- Mutation is symmetric (the same rate each way), so it pulls frequencies toward 0.5.

## Further reading

- simuPOP user guide: https://bopeng.github.io/simuPOP/userGuide.html
- Reference manual: https://bopeng.github.io/simuPOP/refManual.html
- Source and install notes: https://github.com/BoPeng/simuPOP
- Peng B, Kimmel M (2005). Bioinformatics 21:3686-3687. https://doi.org/10.1093/bioinformatics/bti584

---

Cite: Peng B, Kimmel M (2005). simuPOP: a forward-time population genetics simulation environment. Bioinformatics 21:3686-3687. doi:10.1093/bioinformatics/bti584

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simupop).
