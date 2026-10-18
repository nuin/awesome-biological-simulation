# VarSim

> Simulate a diploid human genome with germline and somatic SNVs, indels and structural variants, generate reads from it, and score alignments and variant calls against the truth.

Licence: BSD-2-Clause · [Source code](https://github.com/bioinform/varsim)

## What it simulates

VarSim has two jobs. It simulates a diploid genome by inserting variants into a reference, and it checks how well an aligner or variant caller recovers them. The project describes it as a simulation and validation framework for high-throughput sequencing, with cancer applications.

Variants come from three sources, set through `varsim.py` options:

- **Small variants** (SNPs, insertions, deletions, MNPs and complex events), sampled from an input VCF such as dbSNP with `--vc_in_vcf`. Counts are set with `--vc_num_snp`, `--vc_num_ins`, `--vc_num_del`, `--vc_num_mnp` and `--vc_num_complex`. `--vc_prop_het` sets the heterozygous share.
- **Structural variants** (insertions, deletions, duplications and inversions), sampled from the Database of Genomic Variants with `--sv_dgv`. Counts use `--sv_num_ins`, `--sv_num_del`, `--sv_num_dup` and `--sv_num_inv`, and inserted sequences come from `--sv_insert_seq`.
- **Somatic variants**, through the helper `varsim_somatic.py`. The project calls this workflow early-stage and says the somatic route samples from the COSMIC database.

After building the two haplotypes, VarSim simulates reads with ART or DWGSIM (`--simulator`), with settings for read length, fragment size, number of lanes and total coverage. It writes the reads and a truth VCF.

## When to use it

Use VarSim for a human-scale benchmark where you need both the reads and the truth VCF, and then want to compare your own alignments and calls with that truth. It only supports the human genome, per the project's system requirements.

- Use [DWGSIM](dwgsim.md) for a small, quick set of reads with planted SNPs and indels from any reference. VarSim can call DWGSIM as its read simulator.
- Use [BAMSurgeon](bamsurgeon.md) when you want to spike variants into reads you already have, for example a real normal sample.
- Use [wgsim](wgsim.md) for reads with random mutations and no extra inputs.

## Install

No container recipe is provided for VarSim. The project's quickstart needs a human reference of about 3 GB, extra data files downloaded from the web, a Java 8 JDK, a Python 2 Miniconda, a Maven and Ant build, and the project states that read simulation needs 32 GB of free RAM. A small sandbox with no network cannot hold that, so this page gives instructions only.

The latest GitHub release is v0.8.6 (September 2020) and includes a prebuilt `varsim-0.8.6.tar.gz` (about 15 MB). To build from source, the README gives:

```bash
git clone https://github.com/bioinform/varsim.git
cd varsim
./build.sh
```

`build.sh` downloads the tools it needs into an `opt` folder: JDK 8, Miniconda 2 with pysam, PyVCF, pybedtools, SciPy and samtools 1.9, Maven, Ant, bzip2 and the ART binaries. Plan for either ART or DWGSIM to be installed. A Dockerfile in the `docker` folder builds an image that runs the same `build.sh`.

## A first run

Adapted from the [project page](https://bioinform.github.io/varsim/) and `tests/quickstart_test/quickstart.sh` in the repository. The quickstart downloads the `hs37d5` reference and two data files (`insert_seq.txt` and a DGV supporting-variants file), then runs:

```bash
cd tests/quickstart_test
./quickstart.sh
```

Inside, the call to `varsim.py` sets a read length of 100, 300 SNPs, 10 insertions, 10 deletions, 5 MNPs, 5 complex variants, thousands of structural variants (2000 insertions, 2000 deletions, 200 duplications, 1000 inversions), a mean fragment size of 350 with a standard deviation of 50, three lanes and total coverage of 1. The page says it generates very low coverage data and that you raise `--total_coverage` for more.

## Reading the output

By the project page, the reads and truth appear in `out`:

- `out/lane*.fq.gz`: the simulated reads, one set per lane.
- `out/simu.truth.vcf`: every variant that was inserted. The quickstart passes `--id simu`.

To validate results from your own pipeline, align the reads and call variants, then run:

```bash
python compare_vcf.py --true_vcf out/simu.truth.vcf --out_dir validation \
  --reference hs37d5.fa --vcfs calls.vcf
```

This writes `validation/augmented_report.json`, which loads in the Variant Compare web app, plus `augmented_tp.vcf.gz`, `augmented_fn.vcf.gz` and `augmented_fp.vcf.gz` for true positives, false negatives and false positives. For alignments, `java -jar VarSim.jar samcompare -prefix simu <BAMs>` writes a JSON file for the Alignment Compare web app.

## Pitfalls

- **Memory.** The project asks for 32 GB of free RAM for variant simulation and read generation, and 8 GB for validation.
- **Human only.** Other species are not supported.
- **Old toolchain.** The build pins JDK 8 and a Python 2 Miniconda, so expect to use the Docker route on a current system.
- **Disk.** The page says to have free space for twice the number of reads generated.
- **Somatic needs COSMIC.** The two COSMIC VCFs are downloaded separately from the COSMIC site, and the page calls the somatic workflow under construction.
- **Pre-generated data.** The project hosts reads and variants in a requester-pays Amazon S3 bucket, `s3://varsim`, which needs an AWS account.

## Further reading

- Project page with quick start guides: https://bioinform.github.io/varsim/
- Source and issues: https://github.com/bioinform/varsim
- Paper: Mu JC et al. (2015). VarSim: a high-fidelity simulation and validation framework for high-throughput genome sequencing with cancer applications. Bioinformatics 31:1469-1471. https://doi.org/10.1093/bioinformatics/btu828

---

Cite: Mu JC, Mohiyuddin M, Li J, Bani Asadi N, Gerstein MB, Abyzov A, Wong WH, Lam HYK (2015). VarSim: a high-fidelity simulation and validation framework for high-throughput genome sequencing with cancer applications. Bioinformatics 31:1469-1471. doi:10.1093/bioinformatics/btu828

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/varsim).
