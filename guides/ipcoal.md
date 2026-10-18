# ipcoal

> Simulate gene genealogies and SNPs along a species tree under the multispecies coalescent with recombination and mutation.

Licence: MIT · [Source code](https://github.com/eaton-lab/ipcoal)

## What it simulates

ipcoal simulates gene genealogies and DNA variants along a species tree under the multispecies coalescent. It builds on [msprime](msprime.md) for the simulation and adds a species-tree interface, per-locus genealogy tables and tools for phylogenetic analysis. You give it a species tree with branch lengths in generations, an effective population size, the number of samples per tip, the number of loci and sites, and mutation and recombination rates.

It returns the local gene tree for every stretch of sequence between recombination breakpoints, plus the SNPs that fell on them. The key assumption is that gene trees can differ from the species tree through incomplete lineage sorting: two lineages that fail to coalesce inside a short branch may coalesce deeper, in a different order. The recipe's helper script uses one Ne for every branch. Loci are unlinked from each other and recombine only inside a locus.

## When to use it

Use ipcoal to ask how often gene trees disagree with the species tree for a given Ne and branch length. It also generates test data for species-tree and gene-tree inference methods, and for checking a phylogenetic pipeline against a known truth.

- Use msprime when you have one population or a custom demography and want a VCF with full control over the model.
- Use [stdpopsim](stdpopsim.md) for published models of a real species.

## Run it in your browser

ipcoal has no browser version on biosimhub. Use the install route below.

## Install it yourself

The conda command resolves for ipcoal 0.5.0:

```
micromamba create -n ipcoal -c conda-forge ipcoal=0.5.0
```

The ipcoal docs also list `pip install ipcoal`. A minimal run in Python, without the recipe's helper script:

```python
import ipcoal, toytree

tree = toytree.tree("((A:200000,B:200000):200000,(C:200000,D:200000):200000);")
model = ipcoal.Model(tree, Ne=100_000, nsamples=2, mut=1e-8, recomb=1e-9,
                     seed_trees=1, seed_mutations=1)
model.sim_loci(nloci=3, nsites=1000)
print(model.df[["locus", "start", "end", "nsnps"]])
```

In the recipe's 0.5.0 image, locus 0 split into 5 genealogy segments with 3, 11, 9, 3 and 0 SNPs. The table `model.df` has one row per segment.

## Run the tested example

This recipe builds ipcoal in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 1.8 s.

1. Download [ipcoal-recipe.tar.gz](https://biosimhub.pages.dev/guides/ipcoal/ipcoal-recipe.tar.gz) (Dockerfile, run_ipcoal.py, example tree.nwk, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf ipcoal-recipe.tar.gz
   cd ipcoal
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/ipcoal:0.5.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/ipcoal:0.5.0 python /opt/run_ipcoal.py --tree /work/in/tree.nwk \
    --ne 100000 --nsamples 2 --nloci 5 --nsites 2000 \
    --mut 1e-08 --recomb 1e-09 --seed 42 > out/ipcoal_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `gene_trees.nwk` | 6.5 KB |
| `genealogies.csv` | 6.9 KB |
| `ipcoal.vcf` | 15.7 KB |
| `ipcoal_log.txt` | 37 B |
| `summary.txt` | 137 B |

<details><summary>First lines of <code>gene_trees.nwk</code></summary>

```
((B_0:202832.22897653581458,B_1:202832.22897653581458):493997.51184521906544,((C_0:29803.66954242020438,C_1:29803.66954242020438):375896.78558616386726,((A_0:7393.38376990589677,A_1:7393.3837699058967
((C_0:29803.66954242020438,C_1:29803.66954242020438):375896.78558616386726,((D_0:60578.62713538375829,D_1:60578.62713538375829):341592.42803757940419,((A_0:7393.38376990589677,A_1:7393.38376990589677)
((C_0:200410.59705667701201,C_1:200410.59705667701201):482715.47098539210856,((D_0:143582.99554709793301,D_1:143582.99554709793301):357458.73584046511678,(A_1:262929.17927234375384,(A_0:256796.7911238
((A_1:262929.17927234375384,(A_0:256796.79112389695365,(B_0:3835.15448568532611,B_1:3835.15448568532611):252961.63663821163937):6132.38814844680019):420196.88876972533762,((D_0:143582.99554709793301,D
((A_1:262929.17927234375384,(A_0:256796.79112389695365,(B_0:3835.15448568532611,B_1:3835.15448568532611):252961.63663821163937):6132.38814844680019):420196.88876972533762,((D_0:143582.99554709793301,D
((A_1:262929.17927234375384,(A_0:256796.79112389695365,(B_0:3835.15448568532611,B_1:3835.15448568532611):252961.63663821163937):6132.38814844680019):262048.00522619322874,((D_0:143582.99554709793
```

</details>

<details><summary>First lines of <code>genealogies.csv</code></summary>

```
locus,start,end,nbps,nsnps,tidx,genealogy
0,0,115,115,1,0,"((B_0:202832.22897653581458,B_1:202832.22897653581458):493997.51184521906544,((C_0:29803.66954242020438,C_1:29803.66954242020438):375896.78558616386726,((A_0:7393.38376990589677,A_1:7
0,115,2000,1885,40,1,"((C_0:29803.66954242020438,C_1:29803.66954242020438):375896.78558616386726,((D_0:60578.62713538375829,D_1:60578.62713538375829):341592.42803757940419,((A_0:7393.38376990589677,A_
1,0,521,521,16,0,"((C_0:200410.59705667701201,C_1:200410.59705667701201):482715.47098539210856,((D_0:143582.99554709793301,D_1:143582.99554709793301):357458.73584046511678,(A_1:262929.17927234375384,(
1,521,844,323,12,1,"((A_1:262929.17927234375384,(A_0:256796.79112389695365,(B_0:3835.15448568532611,B_1:3835.15448568532611):252961.63663821163937):6132.38814844680019):420196.88876972533762,((D_0:143
1,844,1526,682,20,2,"((A_1:262929.17927234375384,(A_0:256796.79112389695365,(B_0:3835.15448568532611,B_1:3835.15448568532611):252961.63663821163937):6132.38814844680019):420196.88876972533762,((D_0:14
1,1526,2000,474,8,3,"((A_1:262929.17927234375384,(A_0:256796.79112389695365,(B_0:3835.15448568532611,B_1:3835.15448568532611):252961.63663821163937):6132
```

</details>

<details><summary>First lines of <code>ipcoal.vcf</code></summary>

```
##fileformat=VCFv4.2
##fileDate=2026-10-12 06:06:41.216471
##source=ipcoal-v.0.5.0
##reference=true_simulated_ancestral_sequence
##contig=<ID=0,length=2000>
##contig=<ID=1,length=2000>
##contig=<ID=2,length=2000>
##contig=<ID=3,length=2000>
##contig=<ID=4,length=2000>
##FORMAT=<ID=GT,Number=1,Type=String,Description="Genotype">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO	FORMAT	A_0	A_1	B_0	B_1	C_0	C_1	D_0	D_1
1	22	.	C	A	99	PASS	.	GT	1|1	1|1	0|0	0|0	1|1	1|1	1|1	1|1
```

</details>

<details><summary>First lines of <code>ipcoal_log.txt</code></summary>

```
done 19 genealogy segments, 274 SNPs
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
seed	42
species_tree	((A:200000,B:200000):200000,(C:200000,D:200000):200000);
loci	5
sites_per_locus	2000
genealogy_segments	19
snps	274
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--ne` | Effective population size (Ne) | 100000 | 10 to 10000000 |
| `--nsamples` | Haploid samples per tip | 2 | 1 to 20 |
| `--nloci` | Number of unlinked loci | 5 | 1 to 200 |
| `--nsites` | Sites per locus | 2000 | 1 to 100000 |
| `--mut` | Mutation rate per site per generation | 1e-08 | 0 to 0.001 |
| `--recomb` | Recombination rate per site per generation | 1e-09 | 0 to 0.001 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper script `run_ipcoal.py` reads your Newick tree with toytree, builds `ipcoal.Model` with the same seed for trees and mutations, calls `sim_loci`, writes the VCF with `model.write_vcf`, and saves `model.df` as CSV. The example tree is `((A:200000,B:200000):200000,(C:200000,D:200000):200000);`. It has four tips, and each tip is sampled twice, so the data have 8 sequences named A_0, A_1, B_0 and so on.

- `ipcoal_log.txt`: "done 19 genealogy segments, 274 SNPs". Five loci of 2000 sites each, cut by recombination into 19 segments, with 274 SNPs.
- `genealogies.csv`: columns `locus,start,end,nbps,nsnps,tidx,genealogy`. Locus 0 has two rows. Positions 0 to 115 (115 bp) carry 1 SNP, and positions 115 to 2000 (1885 bp) carry 40 SNPs, each with its own Newick tree. Locus 1 splits at 521 and 844.
- `gene_trees.nwk`: the same 19 trees, one per line. Branch lengths are in generations. The first tree joins B_0 and B_1 at 202,832 generations and C_0 and C_1 at 29,804.
- `ipcoal.vcf`: contigs 0 to 4 of length 2000, with 8 sample columns (A_0, A_1, B_0, B_1, C_0, C_1, D_0, D_1).
- `summary.txt`: seed, the tree, 5 loci, 2000 sites per locus, 19 segments and 274 SNPs.

The species tree groups A with B and C with D. The first gene tree has the B pair outermost and the second has the C pair outermost, so both disagree with it. Gene trees that differ from the species tree are incomplete lineage sorting, the effect ipcoal is built to study.

## Your own runs

Each run changes one value from the example (Ne 100,000, 2 samples per tip, 5 loci, seed 42).

- **Smaller Ne.** `--ne 10000` gave 5 genealogy segments and 141 SNPs, down from 19 and 274. With a tenth of the Ne there are fewer recombination breakpoints and fewer SNPs, because both depend on coalescent time, which scales with Ne.
- **No recombination.** `--recomb 0` gave 5 segments (one per locus) and 309 SNPs.
- **More loci.** `--nloci 20` gave 100 segments and 1010 SNPs. Four times the loci gave about four times the SNPs.
- **More samples per tip.** `--nsamples 4` gave 24 segments and 341 SNPs, with 16 sequences in the VCF.

## Pitfalls

- **Branch lengths are generations.** The tree you give is in generations. Branch lengths in substitutions per site would make every split a fraction of a generation old.
- **Mutation rate is per site per generation.** The default 1e-8 gives about 2.7 SNPs per 100 sites for the example (274 over 10,000 sites). Short loci need a larger rate or more sites to have any SNPs.
- **Loci are independent.** Recombination acts within a locus. For linked sequence, use one locus with more sites.
- **Same seed for trees and mutations.** The recipe's helper script uses one seed for both. Change `--seed` to get a new replicate.
- **Tip names set the sample names.** Sequences are named `<tip>_<n>`, so a tip called "A" is sampled as A_0, A_1.

## Further reading

- Documentation: https://eaton-lab.org/ipcoal/
- Source: https://github.com/eaton-lab/ipcoal
- Paper: McKenzie PF, Eaton DAR (2020) ipcoal: an interactive Python package for simulating and analyzing genealogies and sequences on a species tree or network. Bioinformatics 36:4193-4196. https://doi.org/10.1093/bioinformatics/btaa486

---

Cite: McKenzie PF, Eaton DAR (2020). ipcoal: an interactive Python package for simulating and analyzing genealogies and sequences on a species tree or network. Bioinformatics 36:4193-4196. doi:10.1093/bioinformatics/btaa486

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/ipcoal).
