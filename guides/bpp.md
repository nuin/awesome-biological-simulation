# BPP simulator

> Simulate gene trees and DNA alignments at many loci under the multispecies coalescent from a species tree with divergence times and population sizes.

Licence: AGPL-3.0-only · [Source code](https://github.com/bpp/bpp)

## What it simulates

BPP is a Bayesian program for the multispecies coalescent (MSC). Its main use is inference of species trees, divergence times and population sizes from sequence alignments. The `--simulate` mode, which replaces the older MCcoal program, goes the other way. Given a species tree with divergence times (tau) and population-size parameters (theta), it simulates gene trees and DNA alignments at many loci.

The simulator covers:

- **MSC:** gene trees drawn from the coalescent inside each species, with lineages sorting between species.
- **MSC-I and MSC-M:** the same with introgression events or continuous migration between species.
- **Substitution models:** JC69 or GTR with gamma rate variation among sites, with different parameters per locus if you ask for them.
- **Clock violations:** locus rates and rate drift among lineages.

Times and sizes are in expected substitutions per site. A theta of 0.01 means two sequences from one population differ at about 1 percent of sites.

## When to use it

Use it to test species-tree or species-delimitation methods on data with a known history, to see how much gene-tree discord a set of divergence times and sizes produces, or to feed data back into BPP itself.

Alternatives:

- [msprime](msprime.md) simulates the same coalescent with demographic models and writes tree sequences.
- [ipcoal](ipcoal.md) simulates genealogies and sequences on a species tree from Python.
- [scrm](scrm.md) simulates the coalescent with recombination and writes ms-format output.

## Install

The project publishes static binaries for Linux x86-64 and aarch64, macOS and Windows. The current release is v4.8.7. On Linux x86-64, from the README:

```bash
wget https://github.com/bpp/bpp/releases/download/v4.8.7/bpp-4.8.7-linux-x86_64.tar.gz
tar zxvf bpp-4.8.7-linux-x86_64.tar.gz
bpp-4.8.7-linux-x86_64/bin/bpp --version
```

For Linux aarch64 use `bpp-4.8.7-linux-aarch64.tar.gz`. Both archives exist (checked with HTTP requests, about 3.4 MB and 3.2 MB). To build from source you need GCC 4.7 or newer and run `make` in the `src/` folder. The licence is the GNU Affero General Public License v3.

There is no conda-forge or Bioconda package under the name `bpp` that carries this program. The recipe downloads the release archive and checks its SHA-256 sum. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## A first run

Adapted from the [BPP manual, section "Simulating Gene Trees and Alignments Using BPP"](https://bpp.github.io/bpp-manual/bpp-4-manual/). The control file names the output files, the species tree and the data size:

```text
seed = 12345
seqfile = MySeq.txt
treefile = MyTree.tre
Imapfile = MyImap.txt
modelparafile = modelparas.txt
species&tree = 4  A  B  C  D
                  3  2  1  1
                  ((A #0.01, B #0.01) :0.01 #0.01, (C, D) :0.011 #0.01) : 0.012 #0.01;
phase = 1 1 0 0
loci&length = 20 500
model = 7
Qrates = 0  10 5 5 5 5 10
basefreqs = 0  10 10 10 10
alpha_siterate = 0  100 20 5
```

Run it with:

```bash
bpp --simulate MCcoal.ctl
```

The manual's own example uses 100 loci of 1000 sites. The recipe uses 20 loci of 500 sites so it is quick. In the tree, the number after a colon is a divergence time (tau) and the number after `#` is a theta. The second row of `species&tree` gives the sample per species: sequences when `phase` is 0, diploid individuals when it is 1.

## Run the tested example

This recipe builds BPP simulator in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.2 s.

1. Download [bpp-recipe.tar.gz](https://biosimhub.pages.dev/guides/bpp/bpp-recipe.tar.gz) (Dockerfile, example control.ctl, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bpp-recipe.tar.gz
   cd bpp
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/bpp:4.8.7 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bpp:4.8.7 bpp --simulate /work/in/control.ctl > out/bpp_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `MyImap.txt` | 35 B |
| `MySeq.txt` | 77.1 KB |
| `MySeq.txt.full` | 132.0 KB |
| `MySeq.txt.rand` | 132.0 KB |
| `MyTree.tre` | 8.2 KB |
| `bpp_log.txt` | 1.3 KB |
| `modelparas.txt` | 2.2 KB |

<details><summary>First lines of <code>MyImap.txt</code></summary>

```
a1	A
a2	A
a3	A
b1	B
b2	B
c1	C
d1	D
```

</details>

<details><summary>First lines of <code>MySeq.txt</code></summary>

```


7 500 

A^a1        TGGATATGTA GATYCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA WACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGARAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACY CTCTAATAAC T
A^a2        TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
A^a3        TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
B^b1        TGGATATGTA GATTCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACMCA TACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAGAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACC CTCTAATAAC T
B^b2        TGGATATGTA GATTCACCCA ACGAGGASGG TTAATATTAC AGCTGATGTC AACAGACCCA TACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAGAAGTTT AACCATGCA
```

</details>

<details><summary>First lines of <code>MySeq.txt.full</code></summary>

```


12 500 

A^a1a       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
A^a1b       TGGATATGTA GATTCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA TACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAGAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACC CTCTAATAAC T
A^a2a       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
A^a2b       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
A^a3a       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGC
```

</details>

<details><summary>First lines of <code>MySeq.txt.rand</code></summary>

```


12 500 

A^a1a       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACC CTCTAATAAC T
A^a1b       TGGATATGTA GATTCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA TACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAGAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
A^a2a       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
A^a2b       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGCAT ATAGCAAACT CCACAGTTTC AATATCCACC CGTGCTCACT CTCTAATAAC T
A^a3a       TGGATATGTA GATCCACCCA ACGAGGAGGG TTAATATTAC AGCTGATGTC AACAGACCCA AACTTAGCAT TGTTTAAAAG GATATCATCA ACAACTTCTT AGAAAAGTTT AACCATGC
```

</details>

<details><summary>First lines of <code>MyTree.tre</code></summary>

```
((((((A^a1a:0.0002167956,(A^a2b:0.0001819463,A^a3a:0.0001819463):0.0000348493):0.0003623138,A^a2a:0.0005791094):0.0000648252,A^a3b:0.0006439345):0.0113792236,C^c1:0.0120231581):0.0014082940,(A^a1b:0.0
((((((((A^a1a:0.0030790727,A^a2a:0.0030790727):0.0034782450,A^a3b:0.0065573177):0.0011393377,((A^a1b:0.0000834996,A^a2b:0.0000834996):0.0032752375,A^a3a:0.0033587371):0.0043379183):0.0027420877,B^b1a:
((((((A^a1a:0.0016301087,A^a1b:0.0016301087):0.0002943679,A^a3a:0.0019244766):0.0070496674,((A^a3b:0.0034343804,A^a2a:0.0034343804):0.0014349899,A^a2b:0.0048693703):0.0041047737):0.0010561774,(B^b1a:0
((((((A^a1a:0.0013210998,A^a2b:0.0013210998):0.0015800430,(((A^a1b:0.0003902197,A^a3b:0.0003902197):0.0007604602,A^a2a:0.0011506800):0.0004930603,A^a3a:0.0016437403):0.0012574026):0.0085398427,(B^b1b:
((((((A^a1a:0.0002699155,A^a3a:0.0002699155):0.0025254736,A^a3b:0.0027953892):0.0010377949,(A^a2a:0.0024161003,A^a2b:0.0024161003):0.0014170838):0.0104773020,(A^a1b:0.0110188849,B^b1b:0.0110188849):0.
((((((A^a1a:0.0001465906,(A^a2b:0.0001455820,A^a3a:0.0001455820):0.0000010087):0.0009199942,A^a1b:0.0010665848):0.0007993924,A^a2a:0.0018659772):0.0011103501,A^a3b:0.0029763273):0.0072406661,(((B
```

</details>

<details><summary>First lines of <code>bpp_log.txt</code></summary>

```
bpp v4.8.7_linux_aarch64, 8GB RAM, 16 cores
https://github.com/bpp/bpp

Site rates: alpha sampled from Gamma(100.000000,20.000000), K = 5
Auto-selected SIMD ISA: NEON

Substitution model: GTR with generated rates from Dirichlet
                    10.000000 5.000000 5.000000 5.000000 5.000000 10.000000
Base frequencies: generated from Dirichlet
                  a_T=10.000000 a_C=10.000000 a_A=10.000000 a_G=10.000000
4 species: A (3) B (2) C (1) D (1)
  ((A #0.010000: 0.010000, B #0.010000: 0.010000) #0.010000: 0.002000, (C: 0.011000, D: 0.011000) #0.010000: 0.001000) #0.010000;
```

</details>

<details><summary>First lines of <code>modelparas.txt</code></summary>

```
locus	a(TC)	b(TA)	c(TG)	d(CA)	e(CG)	f(AG)	pi_T	pi_C	pi_A	pi_G	alpha
1  0.275460  0.060703  0.120976  0.203205  0.101730  0.237926 0.296318 0.247247 0.303993 0.152442  4.630726
2  0.148305  0.106060  0.269441  0.107679  0.109991  0.258524 0.285677 0.234798 0.252834 0.226691  5.538123
3  0.294924  0.104435  0.141543  0.082021  0.146177  0.230900 0.353918 0.165650 0.191076 0.289357  5.152971
4  0.230911  0.113852  0.091590  0.194474  0.098660  0.270513 0.271207 0.267636 0.198265 0.262891  4.432118
5  0.232768  0.085858  0.209571  0.177775  0.107404  0.186624 0.266478 0.259918 0.216911 0.256694  4.948607
6  0.248804  0.216844  0.228487  0.022571  0.086287  0.197006 0.365759 0.089844 0.268785 0.275611  4.468738
7  0.273890  0.107417  0.109209  0.238331  0.069947  0.201208 0.228717 0.312052 0.266532 0.192700  4.888978
8  0.256600  0.163560  0.131803  0.112362  0.143491  0.192184 0.298580 0.246387 0.170902 0.284131  5.393962
9  0.299486  0.141666  0.149462  0.109619  0.051360  0.248407 0.195509 0.289456 0.221974 0.293060  4.876060
10  0.240643  0.120680  0.112355  0.216675  0.105707  0.203939 0.257245 0.185691 0.323848 0.233215  4.533669
11  0.129520  0.133925  0.177512  0.083422  0.12218
```

</details>


## Reading the output

Following the manual:

- `MySeq.txt`: the alignments for all loci, one after the other. With `phase = 1` for a species, pairs of sequences are merged into unphased diploid individuals, with heterozygous sites shown as ambiguity codes (Y, R, M, K, S, W).
- `MySeq_full.txt`: the same data before unphasing, with fully resolved haplotypes.
- `MyTree.tre`: the true gene tree of each locus in Newick format, followed by the tree height (TH) and total length (TL) in brackets.
- `modelparas.txt`: one line per locus with the GTR parameters, the locus rate and the lineage rates.
- `MyImap.txt`: the map from individual names to species.

The screen output lists the model, the species tree and a table of populations and ancestors. Read it first: the manual says to confirm the program read the control file as intended.

## Pitfalls

- **A positive seed repeats the data exactly.** Use `seed = -1` to take a seed from the clock for new data each time.
- **Rates for migration changed meaning.** In BPP 4.4 to 4.7 the number in the migration block was the expected number of migrants per generation. From 4.8.0 it is the mutation-scaled rate w, and BPP does not warn about the difference.
- **Theta is needed only where two or more sequences are sampled.** Values for species with one sequence are ignored.
- **Phasing multiplies the sequence count.** A species with 3 individuals and `phase = 1` gives 6 haplotypes.
- **Comment out `seqfile` to get gene trees only.** The sequence files grow quickly with many loci.
- **Lint the file first.** The manual describes a linter, `bpp-lint`, with an `-s` flag for simulation control files.

## Further reading

- Project: https://github.com/bpp/bpp
- BPP documentation project: https://bpp.github.io/bpp-manual/
- Original manual (PDF): https://github.com/bpp/bpp/releases/download/v4.8.7/bpp4DOC.pdf
- Flouri T, Jiao X, Rannala B, Yang Z (2018). Species tree inference with BPP using genomic sequences and the multispecies coalescent. Mol Biol Evol 35:2585-2593. https://doi.org/10.1093/molbev/msy147
- Flouri T, Jiao X, Rannala B, Yang Z (2020). A Bayesian implementation of the multispecies coalescent model with introgression for phylogenomic analysis. Mol Biol Evol 37:1211-1223. https://doi.org/10.1093/molbev/msz296

---

Cite: Flouri T, Jiao X, Rannala B, Yang Z (2018). Species tree inference with BPP using genomic sequences and the multispecies coalescent. Mol Biol Evol 35:2585-2593. doi:10.1093/molbev/msy147

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bpp).
