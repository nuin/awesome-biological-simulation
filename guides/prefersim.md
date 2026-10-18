# PReFerSim

> Forward simulation under the Poisson Random Field model with a two-epoch demography and a point or gamma distribution of selection coefficients; returns SFS, SNP counts and per-site output.

Licence: GPL-3.0-or-later · [Source code](https://github.com/LohmuellerLab/PReFerSim)

## What it simulates

PReFerSim simulates allele frequencies under the Poisson Random Field model. New mutations arise each generation, their number drawn from a Poisson distribution. Each mutation then moves through the population by Wright-Fisher drift with selection, independently of every other mutation. Sites are unlinked, which is why one run of 10 million sites equals ten runs of 1 million sites (the manual says so). That independence makes it fast.

You give a mutation rate, a distribution of fitness effects (DFE) and a demographic history made of epochs. Output files report the number of segregating sites per generation, the site frequency spectrum (SFS), genetic load, fixed and lost mutations and the frequency of every segregating mutation at the end.

Key assumptions: independent sites, a dominance coefficient h of 0.5 (additive) unless you change it, and a derived allele with selection coefficient s. In the manual's fitness scheme the genotype A1A2 has fitness 1 - h(2s) and A2A2 has 1 - 2s, where A2 is the derived allele. A positive s therefore means a harmful derived allele.

## When to use it

Use it to ask what SFS or load a demographic history and a DFE produce, or to follow the trajectory of alleles that end at a given frequency. Typical questions: how much does a bottleneck change genetic load, and what does a gamma DFE look like in an exome-sized sample.

Alternatives:

- [simuPOP](simupop.md) fits better when sites are linked and you want recombination.
- [stdpopsim](stdpopsim.md) fits better when you want a published demographic model as the starting point.

## Install it yourself

PReFerSim 1.0 is on bioconda, with builds listed for linux-64 and osx-64.

```
conda create -n prefersim -c conda-forge -c bioconda prefersim=1.0
```

A micromamba dry run did not finish (downloads from conda.anaconda.org timed out), so the version rests on the anaconda.org index. The manual also describes compiling `PReFerSim.c` with `gcc -g -o PReFerSim PReFerSim.c -lm -lgsl -lgslcblas -O3`, which needs GSL.

The program takes a parameter file and a replicate number. The random seed and generator come from GSL environment variables:

```
GSL_RNG_SEED=42 GSL_RNG_TYPE=mrg PReFerSim params.txt 1
```

A minimal `params.txt` (keys are `Name: value`, any capitalization):

```
MutationRate: 80
DFEType: point
DFEPointSelectionCoefficient: 0
DemographicHistory: demography.txt
PrintSegSiteInfo: 1
PrintSFS: 1
```

The demography file has one epoch per line, oldest first: `<population size in chromosomes> <generations>`.

## Run the tested example

This recipe builds PReFerSim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.4 s. PReFerSim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [prefersim-recipe.tar.gz](https://biosimhub.pages.dev/guides/prefersim/prefersim-recipe.tar.gz) (Dockerfile, run_prefersim.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf prefersim-recipe.tar.gz
   cd prefersim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/prefersim:1.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/prefersim:1.0 python /opt/run_prefersim.py --mutation-rate 80 \
    --dfe point --s 0 --shape 0.184 --scale 319.8626 \
    --scaling 1000 --ne-anc 10000 --gen-anc 1 \
    --ne-now 5000 --gen-now 100 --seed 42 > out/prefersim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `prefersim.1.fixed_sites_out.txt` | 1.4 KB |
| `prefersim.1.full_out.txt` | 6.5 KB |
| `prefersim.1.gen_load_out.txt` | 910 B |
| `prefersim.1.num_snp_out.txt` | 211 B |
| `prefersim.1.s_out.txt` | 910 B |
| `prefersim.1.sfs_out.txt` | 39 B |
| `prefersim.1.sum_daf_out.txt` | 910 B |
| `prefersim_log.txt` | 562 B |

<details><summary>First lines of <code>prefersim.1.fixed_sites_out.txt</code></summary>

```
0	0	0.000000
19	0	0.000000
12	0	0.000000
9	0	0.000000
13	0	0.000000
27	0	0.000000
12	0	0.000000
13	0	0.000000
19	0	0.000000
19	0	0.000000
17	0	0.000000
10	0	0.000000
```

</details>

<details><summary>First lines of <code>prefersim.1.full_out.txt</code></summary>

```
1	2.000000e-04	0.000000e+00	101	2108
1	2.000000e-04	0.000000e+00	101	2107
1	2.000000e-04	0.000000e+00	101	2106
1	2.000000e-04	0.000000e+00	101	2105
1	2.000000e-04	0.000000e+00	101	2104
1	2.000000e-04	0.000000e+00	101	2103
1	2.000000e-04	0.000000e+00	101	2102
1	2.000000e-04	0.000000e+00	101	2101
1	2.000000e-04	0.000000e+00	101	2100
1	2.000000e-04	0.000000e+00	101	2099
1	2.000000e-04	0.000000e+00	101	2098
1	2.000000e-04	0.000000e+00	101	2097
```

</details>

<details><summary>First lines of <code>prefersim.1.gen_load_out.txt</code></summary>

```
0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.
```

</details>

<details><summary>First lines of <code>prefersim.1.num_snp_out.txt</code></summary>

```
0	0	0	0	0	0	1	2	1	0	0	0	0	0	1	1	0	1	2	2	1	1	4	0	2	2	2	3	1	1	5	1	4	2	2	4	1	6	0	6	3	4	7	3	3	3	1	3	6	5	6	10	1	3	5	3	4	5	5	8	5	4	5	4	4	3	5	7	7	11	9	3	7	5	3	8	4	3	4	9	9	6	10	3	5	9	12	6	7	7	10	7	8	8	8	12	7	
```

</details>

<details><summary>First lines of <code>prefersim.1.s_out.txt</code></summary>

```
0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.
```

</details>

<details><summary>First lines of <code>prefersim.1.sfs_out.txt</code></summary>

```
4	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	0	
```

</details>

<details><summary>First lines of <code>prefersim.1.sum_daf_out.txt</code></summary>

```
0.000000	0.000000	0.000000	0.000000	0.000000	0.000000	0.050000	0.100000	0.050000	0.000000	0.000000	0.000000	0.000000	0.000000	0.050000	0.050000	0.000000	0.050000	0.100000	0.100000	0.050000	0.050000	0.
```

</details>

<details><summary>First lines of <code>prefersim_log.txt</code></summary>

```

Parameter List

MutationRate: 80.000000
DFEType: point
DFEPointSelectionCoefficient: 0.000000
DemographicHistory: /tmp/demography.txt
PrintSNPNumber: 1
PrintSumOfS: 1
PrintSumDAF: 1
PrintGenLoad: 1
PrintFixedSites: 1
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--mutation-rate` | Mutation rate (new mutations per generation | 80 | 0.1 to 2000 |
| `--dfe` | Distribution of fitness effects | point | point, gamma |
| `--s=…` | Selection coefficient (point DFE) | 0 | -0.5 to 0.5 |
| `--shape` | Gamma shape (gamma DFE) | 0.184 | 0.01 to 10 |
| `--scale` | Gamma scale (gamma DFE) | 319.8626 | 0.1 to 100000 |
| `--scaling` | Gamma scaling factor (gamma DFE) | 1000 | 1 to 1000000 |
| `--ne-anc` | Ancestral size in chromosomes (2N) | 10000 | 100 to 100000 |
| `--gen-anc` | Ancestral epoch length (generations) | 1 | 1 to 100000 |
| `--ne-now` | Current size in chromosomes (2N) | 5000 | 100 to 100000 |
| `--gen-now` | Current epoch length (generations) | 100 | 1 to 100000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper `run_prefersim.py` writes `/tmp/demography.txt` and `/tmp/params.txt` from the command-line options, switches on seven output options, sets `GSL_RNG_SEED` and `GSL_RNG_TYPE=mrg`, and runs `PReFerSim /tmp/params.txt 1`. Files get the prefix `prefersim` and the replicate number 1.

The example has two epochs: 10000 chromosomes for 1 generation, then 5000 for 100 generations. The log says 32 mutations arrived before epoch 1 began and 2109 arose in total. The manual gives a Poisson mean of 40 new mutations per generation for a mutation rate of 80. The run averaged about 21 per generation, probably because the input scales with the current size: 5000 chromosomes is half the ancestral 10000.

- `fixed_sites_out.txt` has 101 rows (one per generation). Columns are mutations lost, mutations fixed and the sum of s of fixed mutations. Summed over rows, 1925 mutations were lost and 0 fixed.
- 2109 - 1925 leaves 184 segregating mutations. `full_out.txt` has exactly 184 rows: replicate, frequency, s, generation of origin and ID. The first row is `1 2e-04 0 101 2108`, a new mutation at frequency 1/5000, which shows the population size is counted in chromosomes.
- `num_snp_out.txt`, `sum_daf_out.txt`, `gen_load_out.txt` and `s_out.txt` each hold 101 tab-separated values. The last value of `num_snp_out.txt` is 4, and the last of `sum_daf_out.txt` is 0.2.
- `sfs_out.txt` has 19 counts. The sample size n defaults to 20 in the manual. The first count is 4 and the rest are 0, so the sample holds four singletons. Four sites at 1/20 sum to 0.2, matching `sum_daf_out.txt`.

With no burn-in, nearly all variation is under 100 generations old. This is why the SFS is so sparse.

## Your own runs

Every run changes one or more options. Each used seed 42 and one run only.

- `--s 0.01` (harmful derived allele): 2095 mutations, 145 segregating, 6 singletons in the sample.
- `--s=-0.01` (beneficial): 2060 mutations, 188 segregating, 12 singletons.
- `--dfe gamma`, default shape 0.184, scale 319.8626 and scaling 1000: 2097 mutations, 161 segregating, 8 singletons.
- `--ne-anc 1000 --gen-anc 8000 --ne-now 100 --gen-now 100` (the manual's Bottleneck.txt epochs): 319,342 mutations, 291 fixed, 105 segregating. The SFS has all 19 classes filled, 89 polymorphic sites in the sample, and the final sum of derived allele frequency is 41.35.

The first three are single seeds, so their differences cannot be separated from sampling noise. Run many seeds before reading selection effects from a 100-generation run.

## Pitfalls

- Sizes are in chromosomes (2N), as the manual states. 5000 means 2500 diploids.
- The default ancestral epoch is 1 generation, so there is no burn-in. The manual suggests about 16N generations in the first epoch to reach mutation-selection balance.
- Negative values break the helper's option parser when written with a space. The recipe writes `--s=-0.01`; `--s -0.01` exits with a usage error.
- Sign of s: positive means the derived allele is harmful.
- The manual advises keeping the mutation rate (theta) at or below 2000 and says a run cannot exceed 2,000,000,000 sites.
- Use a different `GSL_RNG_SEED` for every replicate. Reusing it repeats the run.

## Further reading

- Source, examples and manual: https://github.com/LohmuellerLab/PReFerSim
- PReFerSim manual (PDF): https://raw.githubusercontent.com/LohmuellerLab/PReFerSim/master/PReFerSim_Manual_v2.pdf
- Ortega-Del Vecchyo D, Marsden CD, Lohmueller KE (2016). Bioinformatics 32:3516-3518. https://doi.org/10.1093/bioinformatics/btw478

---

Cite: Ortega-Del Vecchyo D, Marsden CD, Lohmueller KE (2016). PReFerSim, fast simulation of demography and selection under the Poisson Random Field model. Bioinformatics 32:3516-3518. doi:10.1093/bioinformatics/btw478

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/prefersim).
