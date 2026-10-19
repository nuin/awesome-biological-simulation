# scrm

> Simulate genome-scale samples under the coalescent with recombination (ms-compatible output) using the sequential coalescent approximation.

Licence: GPL-3.0-or-later · [Source code](https://github.com/scrm/scrm)

## What it simulates

scrm simulates samples of DNA sequences under the coalescent with recombination. It uses a sequential approximation of the recombining genealogy. The README says it can simulate chromosome-scale sequences without a measurable reduction of linkage between sites. Its command line and output copy `ms`, the classic coalescent simulator by Richard Hudson.

You give it a number of haplotypes, a number of independent loci, a mutation rate (theta) and a recombination rate (rho) with a locus length. It returns, for each locus, the positions of the variable sites and a 0/1 matrix of haplotypes. A 1 is the derived allele.

The assumptions: neutral mutations under an infinite-sites model, a randomly mating population of constant size unless you add migration or size-change options, and no selection. Theta is 4 N0 u and rho is 4 N0 r, both for the whole locus, where N0 is the reference population size.

## When to use it

Use scrm when you need ms-format output for software that reads it, or very long sequences with many sites. It also covers island models, population splits and exponential growth through ms options.

- Use [msprime](msprime.md) for VCF and tree sequence output, or when you want to compute statistics from the genealogy directly.
- Use [stdpopsim](stdpopsim.md) when you want a published species model instead of hand-set theta and rho.

The scrm repository is marked inactive (stable, no active development). It is GPL-3.0-or-later.

## Install it yourself

The bioconda package resolves for scrm 1.7.4 on Linux x86-64:

```
micromamba create -n scrm -c conda-forge -c bioconda scrm=1.7.4
```

You can also build from source. The scrm wiki gives `./configure`, then `make`, which produces a binary called `scrm`. Prebuilt packages are listed at https://scrm.github.io.

The command syntax is `scrm <nhap> <nrep> [options]`. A minimal run of 10 haplotypes at 3 loci:

```
scrm 10 3 -t 20 -seed 42
```

The options used by the example are `-t <theta>` (mutation rate, per locus), `-r <rho> <L>` (recombination rate per locus and locus length in bp) and `-seed <n>`.

## Run the tested example

This recipe builds scrm in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s. scrm has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [scrm-recipe.tar.gz](https://biosimhub.pages.dev/guides/scrm/scrm-recipe.tar.gz) (Dockerfile, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf scrm-recipe.tar.gz
   cd scrm
   sh run.sh
   ```

![Terminal recording of the scrm example run](https://biosimhub.pages.dev/media/scrm/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/scrm:1.7.4 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/scrm:1.7.4 scrm 10 3 -t 20 -r 20 100000 -seed 42 > out/scrm_output.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `scrm_output.txt` | 3.7 KB |

<details><summary>First lines of <code>scrm_output.txt</code></summary>

```
scrm 10 3 -t 20 -r 20 100000 -seed 42
42

//
segsites: 54
positions: 0.0191011 0.0563062 0.0770632 0.103708 0.108667 0.110212 0.112217 0.120599 0.126527 0.12865 0.133119 0.150902 0.173942 0.219011 0.241947 0.248282 0.264078 0.271235 0.296043 0.323865 0.33309
000001010001001110111000100000111100100000010010001010
000000010001001111100001011111000001011111000000010100
000000010001101110001110100000111010000000110000110100
110110001110010000001100100000111000000000010000000001
000001010001001110111000100000111100100000010000001000
001000010001010000001000100000111100100000011100001000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `samples` | Number of haplotypes | 10 | 2 to 1000 |
| `replicates` | Independent loci (replicates) | 3 | 1 to 1000 |
| `-t` | Mutation rate theta (4 Ne mu per locus) | 20 | 0 to 10000 |
| `-r` | Recombination rate rho (4 Ne r per locus) | 20 | 0 to 10000 |
| `length` | Locus length (sites) | 100000 | 2 to 1000000000 |
| `-seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example command is `scrm 10 3 -t 20 -r 20 100000 -seed 42`. The output file is 3801 bytes. Its structure, as the scrm wiki describes it:

- Line 1 repeats the command. Line 2 is the seed, here 42. Those two lines are enough to repeat the run.
- Each locus starts with `//`, then `segsites: <n>`, then `positions:` with one value per site, then one row of 0s and 1s per haplotype.
- Positions run from 0 to 1 along the locus. Multiply by 100,000 to get a position in the example.

The three loci have 54, 64 and 74 segregating sites. Each matrix has 10 rows (haplotypes) and as many columns as segsites. The first locus has 54 positions and 54 columns.

Check the numbers against theory. With theta 20 and 10 haplotypes, the expected number of segregating sites is theta times the sum of 1/i for i = 1 to 9, which is 20 x 2.83 = 56.6. A run of 1000 loci with theta 20 and no recombination gave a mean of 56.9 sites. The three loci here (54, 64, 74) are single draws from that distribution. The expected number depends on theta. Rho changes how the sites are linked.

## Your own runs

All runs use 10 haplotypes and seed 42.

- **Raise theta.** `-t 100 -r 20 100000` gave 249, 339 and 248 sites. Five times the theta gave about five times the sites.
- **Count the local trees.** `-T -r 20 100000` prints each local tree in brackets, one line per tree. That gave 70 trees. `-r 200 100000` gave 664 trees. With `-r 0` there is one tree and scrm prints no bracketed length.
- **Add structure.** `-I 2 5 5 0.5` (two populations with 5 haplotypes each, migration rate 0.5) gave a mean of 154 sites over 300 loci, against 58 for one population. Each subpopulation has size N0, so the whole metapopulation is twice as large. With migration rate 10 the mean fell to 116.
- **Run without a seed.** Two runs of `scrm 10 1 -t 5` printed seeds 2063506610 and 2332714344. scrm picks a seed from the operating system and prints it on line 2. Use that seed with `-seed` to reproduce the run.

## Pitfalls

- **Theta and rho are per locus.** A theta of 20 is the value for the whole locus. Convert from per-bp rates with theta = 4 N0 u L.
- **`-r` takes two numbers.** Write the rho and then the locus length in bp, as in `-r 20 100000`.
- **Unsupported ms options.** scrm cannot simulate gene conversion (`-c`) or a fixed number of segregating sites (`-s`). Its `-ema` takes no population-number argument.
- **Options in time order.** With `-es` (admixture), sort timed options by time. scrm reports an error if you do not.
- **Time units.** Times in scrm options are in units of 4 N0 generations.

## Further reading

- Command line options: https://github.com/scrm/scrm/wiki/Command-Line-Options
- Output format: https://github.com/scrm/scrm/wiki/Output
- Source: https://github.com/scrm/scrm
- Downloads: https://scrm.github.io
- Paper: Staab PR, Zhu S, Metzler D, Lunter G (2015) scrm: efficiently simulating long sequences using the approximated coalescent with recombination. Bioinformatics 31:1680-1682. https://doi.org/10.1093/bioinformatics/btu861

---

Cite: Staab PR, Zhu S, Metzler D, Lunter G (2015). scrm. Bioinformatics 31:1680-1682. doi:10.1093/bioinformatics/btu861

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/scrm).
