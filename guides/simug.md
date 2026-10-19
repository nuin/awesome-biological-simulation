# simuG

> Simulate a genome carrying random SNPs and indels relative to a reference FASTA, with the matching VCFs and coordinate map.

Licence: MIT · [Source code](https://github.com/yjx1217/simuG)

## What it simulates

simuG takes a reference genome in FASTA and returns a copy with random variants added. This recipe adds SNPs and small indels (insertions and deletions). simuG can also make copy-number changes, inversions and translocations, which this recipe does not use.

You set the number of SNPs, the transition/transversion ratio and the number of indels. simuG picks positions at random along the reference. Indel lengths follow a power law, p = C x size^(-alpha), for sizes 1 to 50, with alpha 2.0 and C 0.5 as defaults. The ratio of insertions to deletions defaults to 1.

Key assumptions: positions are uniform along the sequence, variants are independent, and the result is one haploid genome. There is no tree, no selection and no population.

## When to use it

Use simuG to build a test genome with a known truth set: a benchmark for a variant caller, an aligner or a genotyping pipeline. The VCFs list exactly what was added.

Alternatives on biosimhub:

- **[Seq-Gen](seq-gen.md), [Pyvolve](pyvolve.md) and [Bio++ bppseqgen](bppseqgen.md)** evolve sequences along a tree. They fit when you want several related sequences and a phylogeny.
- **[msprime](msprime.md) and [stdpopsim](stdpopsim.md)** fit when you want variants from a population history. They give genotypes for many samples, which simuG does not.

## Install it yourself

Conda, pinned to the recipe's version:

```bash
conda create -n simug -c conda-forge -c bioconda simug=1.0.1
conda activate simug
```

The command resolves (simug 1.0.1, about 13 MB of dependencies). The project README runs the script as `perl simuG.pl`; the conda package provides the command `simuG`.

Minimal command:

```bash
simuG -refseq ref.fa -snp_count 200 -indel_count 20 -seed 42 -prefix simulated
```

`-refseq` is required. `-snp_count` and `-indel_count` have no default value.

## Run the tested example

This recipe builds simuG in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s.

1. Download [simug-recipe.tar.gz](https://biosimhub.pages.dev/guides/simug/simug-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf simug-recipe.tar.gz
   cd simug
   sh run.sh
   ```

![Terminal recording of the simuG example run](https://biosimhub.pages.dev/media/simug/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/simug:1.0.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/simug:1.0.1 simuG -refseq /work/in/reference.fa -snp_count 200 \
    -titv_ratio 0.5 -indel_count 20 -seed 42 -prefix simulated > out/simug_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `simug_log.txt` | 1.4 KB |
| `simulated.refseq2simseq.INDEL.vcf` | 3.6 KB |
| `simulated.refseq2simseq.SNP.vcf` | 25.0 KB |
| `simulated.refseq2simseq.map.txt` | 14.5 KB |
| `simulated.simseq.genome.fa` | 58.6 KB |

<details><summary>First lines of <code>simug_log.txt</code></summary>

```

[Mon Oct 12 06:07:34 2026]
Starting simuG ..

[Mon Oct 12 06:07:34 2026]
Check specified options ..
Running simuG for SNP/INDEL simulation >>
Ignore all options for CNV/inversion/translocation simulation.

This simulation use the random seed: 42

The option snp_count has been specified: snp_count = 200
```

</details>

<details><summary>First lines of <code>simulated.refseq2simseq.INDEL.vcf</code></summary>

```
##fileformat=VCFv4.1
##fileDate=Mon Oct 12 06:07:34 2026 (GMT time)
##source=simuG.pl
##INFO=<ID=variant_type,Number=1,Type=String,Description="The type of the introduced genomic variant">
##INFO=<ID=variant_id,Number=1,Type=String,Description="The id of the introduced genomic variant">
##INFO=<ID=ref_chr,Number=1,Type=String,Description="The reference genome based chromosome ID of the introduced genomic variant">
##INFO=<ID=ref_start,Number=1,Type=String,Description="The reference genome based start coordinate of the introduced genomic variant">
##INFO=<ID=ref_end,Number=1,Type=String,Description="The reference genome based end coordinate of the introduced genomic variant">
##INFO=<ID=sim_chr,Number=1,Type=String,Description="The simulated genome based chromosome ID of the introduced genomic variant">
##INFO=<ID=sim_start,Number=1,Type=String,Description="The simulated genome based start coordinate of the introduced genomic variant">
##INFO=<ID=sim_end,Number=1,Type=String,Description="The simulated genome based end coordinate of the introduced genomic variant">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
```

</details>

<details><summary>First lines of <code>simulated.refseq2simseq.SNP.vcf</code></summary>

```
##fileformat=VCFv4.1
##fileDate=Mon Oct 12 06:07:34 2026 (GMT time)
##source=simuG.pl
##INFO=<ID=variant_type,Number=1,Type=String,Description="The type of the introduced genomic variant">
##INFO=<ID=variant_id,Number=1,Type=String,Description="The id of the introduced genomic variant">
##INFO=<ID=ref_chr,Number=1,Type=String,Description="The reference genome based chromosome ID of the introduced genomic variant">
##INFO=<ID=ref_start,Number=1,Type=String,Description="The reference genome based start coordinate of the introduced genomic variant">
##INFO=<ID=ref_end,Number=1,Type=String,Description="The reference genome based end coordinate of the introduced genomic variant">
##INFO=<ID=sim_chr,Number=1,Type=String,Description="The simulated genome based chromosome ID of the introduced genomic variant">
##INFO=<ID=sim_start,Number=1,Type=String,Description="The simulated genome based start coordinate of the introduced genomic variant">
##INFO=<ID=sim_end,Number=1,Type=String,Description="The simulated genome based end coordinate of the introduced genomic variant">
#CHROM	POS	ID	REF	ALT	QUAL	FILTER	INFO
```

</details>

<details><summary>First lines of <code>simulated.refseq2simseq.map.txt</code></summary>

```
ref_chr	ref_start	ref_end	ref_strand	ref_allele	sim_chr	sim_start	sim_end	ref_strand	sim_allele	variant_type	variant_id	donor_chr_in_ref	donor_start_in_ref	donor_end_in_ref	donor_strand_in_ref	duplica
chr1	393	393	+	C	chr1	393	393	+	A	SNP	SNP_144	.	.	.	.	.	.	.
chr1	514	514	+	G	chr1	514	514	+	C	SNP	SNP_71	.	.	.	.	.	.	.
chr1	545	545	+	A	chr1	545	545	+	T	SNP	SNP_169	.	.	.	.	.	.	.
chr1	740	740	+	T	chr1	740	740	+	G	SNP	SNP_98	.	.	.	.	.	.	.
chr1	883	883	+	C	chr1	883	883	+	T	SNP	SNP_170	.	.	.	.	.	.	.
chr1	1135	1135	+	C	chr1	1135	1135	+	G	SNP	SNP_185	.	.	.	.	.	.	.
chr1	2232	2232	+	T	chr1	2232	2232	+	A	SNP	SNP_80	.	.	.	.	.	.	.
chr1	2997	2998	+	GC	chr1	2997	2997	+	G	INDEL	INDEL_6	.	.	.	.	.	.	.
chr1	3324	3324	+	A	chr1	3323	3323	+	C	SNP	SNP_17	.	.	.	.	.	.	.
chr1	3459	3461	+	TGG	chr1	3458	3458	+	T	INDEL	INDEL_11	.	.	.	.	.	.	.
chr1	4050	4050	+	C	chr1	4047	4048	+	CC	INDEL	INDEL_3	.	.	.	.	.	.	.
```

</details>

<details><summary>First lines of <code>simulated.simseq.genome.fa</code></summary>

```
>chr1
CAGATTTTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGTCCCACCTGGTGATCCTATGCTTGTGAGTACCCAGAAAATAGCGACGGACCGCGGTGTTAAGTGTCGAGCTACATCACTTCTCATGTAGCCAGAAGGCTGCAACTCATCGACTCTATGTAGTGACCGCGTC
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-snp_count` | Number of SNPs | 200 | 0 to 1000000 |
| `-indel_count` | Number of indels | 20 | 0 to 100000 |
| `-titv_ratio` | Transition/transversion ratio | 0.5 | 0.01 to 100 |
| `-seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The reference is one 60,000 bp sequence, `chr1`. The run writes five files with the prefix `simulated`:

- `simulated.simseq.genome.fa` (59,973 bytes): the new genome. It is 59,959 bp, which is 41 bp shorter than the reference.
- `simulated.refseq2simseq.SNP.vcf` (200 records) and `simulated.refseq2simseq.INDEL.vcf` (20 records). Positions refer to the reference. The INFO field gives `variant_type`, the reference start and end, and the matching start and end in the new genome.
- `simulated.refseq2simseq.map.txt` (221 lines, a header plus 220 variants): every variant with its reference allele, new allele and both coordinate sets.
- `simug_log.txt`: the options used, including the defaults it filled in (`ins_del_ratio = 1`, `indel_size_powerlaw_alpha = 2`, `indel_size_powerlaw_constant = 0.5`).

The 20 indels are 6 insertions and 14 deletions, with a net change of -41 bp. The largest is 20 bp. The first SNPs are chr1:393 C>A, chr1:514 G>C and chr1:545 A>T. An early deletion shifts later coordinates: the insertion at reference 4050 sits at 4047 in the new genome. Use the map file to convert.

Of the 200 SNPs, 76 are transitions and 124 transversions, a ratio of 0.61 against the requested 0.5.

## Your own runs

Runs below use the example reference and seed 42 unless stated.

**Raise the Ti/Tv ratio to 4.** Transitions rose to 159 and transversions fell to 41, a ratio of 3.88. The indel set was identical: the same 20 indels and the same -41 bp change.

**Scale up to 1000 SNPs and 100 indels.** Ti/Tv came out at 0.51 (336 and 664). The indels were 44 insertions and 56 deletions, net -10 bp, largest 35 bp. The new genome is 59,990 bp.

**Deletions only.** With `-snp_count 0 -indel_count 20 -ins_del_ratio 0` all 20 indels were deletions, net -45 bp, largest 14 bp. The README says `-ins_del_ratio Inf` gives insertions only.

**A different seed.** Seed 7 moved every variant; its first SNP is chr1:28 A>C. Seed 42 run twice gave identical genomes.

## Pitfalls

- **Default Ti/Tv is 0.5.** That is the ratio you get from equal substitution rates (one transition for every two transversions). Set `-titv_ratio` to the value measured in your organism. Use `Inf` for transitions only and `0` for transversions only.
- **VCF coordinates are for the reference.** Reads aligned to the new genome use shifted positions after any indel. Convert with `map.txt`.
- **Counts are exact, positions are random.** A seed fixes the result; change it for independent replicates.
- **Indel size caps at 50 bp.** Changing `-indel_size_powerlaw_alpha` shifts the mix of small and large indels, but not the cap.
- **Each run writes one genome.** For several individuals, run simuG once per seed.

## Further reading

- Source and README: https://github.com/yjx1217/simuG
- Yue JX, Liti G (2019). simuG: a general-purpose genome simulator. Bioinformatics 35(21):4442-4444. https://doi.org/10.1093/bioinformatics/btz424

---

Cite: Yue JX, Liti G (2019). simuG, a general-purpose genome simulator. Bioinformatics 35:4442-4444. doi:10.1093/bioinformatics/btz424

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simug).
