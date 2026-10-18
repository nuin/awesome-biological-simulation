# SLiM

> Forward-time, individual-based population genetics simulation scripted in Eidos. Upload a SLiM script; files it writes are returned.

Licence: GPL-3.0-or-later · [Source code](https://github.com/MesserLab/SLiM)

## What it simulates

SLiM is a forward-time, individual-based genetics simulator. You write the model as a script in Eidos, SLiM's own language. SLiM then evolves the population one tick at a time, creating offspring, applying recombination, mutation and selection, and removing dead individuals. In the default Wright-Fisher model one tick is one generation.

The input is your script and an optional seed. The output is whatever the script prints or writes: log text, genome samples in ms or VCF format, or full population dumps.

SLiM makes no assumption beyond the ones you script. The example is neutral: 500 diploid individuals, random mating, a 100 kb genome, mutation rate 1e-7 and recombination rate 1e-8 per bp. Selection, spatial models, non-Wright-Fisher life cycles and multiple populations are all scripted the same way.

## When to use it

Use SLiM when the model needs selection, an unusual life cycle, space or custom events that a coalescent simulator cannot express. Its manual includes over 200 recipes.

- Use [msprime](msprime.md) when the model is neutral. A backward simulation only follows the sampled lineages.
- Use [fwdpy11](fwdpy11.md) when you want forward simulation from Python instead of Eidos.
- Use [stdpopsim](stdpopsim.md) for a published model of a real species, which can also run on SLiM with `-e slim`.

## Install it yourself

The conda command resolves for SLiM 5.2 on Linux x86-64:

```
micromamba create -n slim -c conda-forge -c bioconda slim=5.2
```

The SLiM site also offers a macOS installer and a source archive (manual chapter 2 covers installation on all platforms). The command line is `slim [options] script.slim`:

```
slim -s 42 neutral.slim
slim -d N=1000 -s 42 neutral.slim
```

`-s` (also `-seed`) sets the random seed. `-d NAME=value` defines a constant that the script can read. Both are described in the SLiM manual. The recipe's 5.2 image reports "SLiM version 5.2".

## Run the tested example

This recipe builds SLiM in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.3 s. SLiM has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [slim-recipe.tar.gz](https://biosimhub.pages.dev/guides/slim/slim-recipe.tar.gz) (Dockerfile, example script.slim, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf slim-recipe.tar.gz
   cd slim
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/slim:5.2 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/slim:5.2 slim -s 42 /work/in/script.slim > out/slim_output.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `sample.txt` | 1.2 KB |
| `slim_output.txt` | 309 B |

<details><summary>First lines of <code>sample.txt</code></summary>

```
//
segsites: 43
positions: 0.011710117101171 0.013210132101321 0.014900149001490 0.041080410804108 0.041820418204182 0.109951099510995 0.137661376613766 0.144711447114471 0.145511455114551 0.179901799017990 0.2111521
0011100001000000101000101100111011011010000
0001100000000100000000101000110101001000010
0000010100100000000100111001100001100101101
0011100001000000101000101100111011011000000
1000010100110011010001101001100001100101101
0000010110100000000000101011100001100101101
0000010110100000000000101011100001100101101
0101101000001000000010101100110001001000000
0101101000001000000010101100110001001000000
```

</details>

<details><summary>First lines of <code>slim_output.txt</code></summary>

```
// Initial random seed:
42

// RunInitializeCallbacks():
initializeMutationRate(1e-07);
initializeMutationType(1, 0.5, "f", 0);
initializeGenomicElementType(1, m1, 1);
initializeGenomicElement(g1, 0, 99999);
initializeRecombinationRate(1e-08);

// Starting run at tick <start>:
1 
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-s` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example script is SLiM manual recipe 4.1, a basic neutral simulation:

```
initialize() {
	initializeMutationRate(1e-7);
	initializeMutationType("m1", 0.5, "f", 0.0);
	initializeGenomicElementType("g1", m1, 1.0);
	initializeGenomicElement(g1, 0, 99999);
	initializeRecombinationRate(1e-8);
}
1 early() { sim.addSubpop("p1", 500); }
2000 late() {
	p1.outputMSSample(10, filePath="sample.txt");
	catn("Segregating mutations: " + size(sim.mutations));
}
```

Mutation type m1 has dominance 0.5 and a fixed selection coefficient of 0.0, so it is neutral. At tick 1 a population p1 of 500 individuals is created. At tick 2000 the script writes a sample of 10 genomes and prints how many mutations segregate in the whole population.

- `slim_output.txt` (309 bytes) starts with the seed (42), echoes each initialization call, then prints the script's `catn` line: "Segregating mutations: 142".
- `sample.txt` (1241 bytes) is ms format: a `//` line, `segsites: 43`, a `positions:` line with 43 values between 0 and 1, then 10 rows of 43 characters, one per genome. A 1 is the mutant allele.

So 142 mutations segregate in 1000 genomes, and 43 of them vary within the 10 sampled. The expected diversity is theta = 4 N mu L = 4 x 500 x 1e-7 x 100,000 = 20. For 10 genomes the expected number of segregating sites at equilibrium is 20 x 2.83 = 56.6. The run stops at tick 2000 (4 N), before equilibrium, and one draw gave 43.

## Your own runs

The example stops at tick 2000. To compare population sizes, a variant script reads N with `-d`, runs for 10 N ticks and writes the same sample. The change is in the first lines:

```
initialize() {
	if (!exists("N")) defineConstant("N", 500);
	...
}
1 early() {
	sim.addSubpop("p1", N);
	community.rescheduleScriptBlock(s1, ticks=10 * N);
}
s1 99999 late() { p1.outputMSSample(10, filePath="sample.txt"); ... }
```

- **Population size.** With `-d N=500`, seeds 1, 2 and 3 gave 56, 77 and 91 segregating sites in the sample (159, 153 and 176 segregating mutations in the population). With `-d N=2000` they gave 201, 231 and 330 sites. The means are 75 and 254, a ratio of 3.4 for a 4-fold larger N. Theta scales with N, and the expected values are 57 and 226.
- **Seed.** The example script with `-s 7` gave 54 segregating sites in the sample and 148 mutations in the population, against 43 and 142 for seed 42.
- **Your own script.** Change the mutation rate, add a second mutation type with a nonzero selection coefficient, or add `p2` and a migration rate. The manual's recipes are the place to start.

## Pitfalls

- **A final block needs a tick.** A variant with `late()` and no tick number stopped after tick 1 with exit code 0 and wrote no sample. Give the final block an explicit tick, or reschedule it as above.
- **Output goes to the working directory.** A relative path such as `sample.txt` is written where SLiM runs.
- **Burn-in.** A run of 4 N ticks (the example) has not reached equilibrium diversity. Use 10 N or more for equilibrium statistics.
- **Constants set with `-d` must be defined.** A script that reads `N` fails with an undefined identifier unless you pass `-d N=...` or guard it with `exists("N")`, as the manual describes.
- **Seeds.** The same script, seed and SLiM version repeat a run. Change `-s` for a replicate.

## Further reading

- SLiM home page: https://messerlab.org/slim/
- SLiM 5.2 manual (PDF, with recipes): https://github.com/MesserLab/SLiM/releases/download/v5.2/SLiM_Manual.pdf
- Source: https://github.com/MesserLab/SLiM
- Paper: Haller BC, Messer PW (2023) SLiM 4. Mol Biol Evol 40:msad007. https://doi.org/10.1093/molbev/msad007

---

Cite: Haller BC, Messer PW (2023). SLiM 4. Mol Biol Evol 40:msad007. doi:10.1093/molbev/msad007

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/slim).
