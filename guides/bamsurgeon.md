# BAMSurgeon

> Spike synthetic SNVs into a BAM file to make a tumor-like sample with known variants for benchmarking somatic variant callers.

Licence: MIT · [Source code](https://github.com/adamewing/bamsurgeon)

## What it simulates

BAMSurgeon adds synthetic variants to reads that already exist in a BAM file. It does not simulate a genome from scratch. You give it a real or simulated alignment and a list of sites. It picks reads that cover each site, changes the base in a share of them, and realigns those reads. The result is a new BAM with a known set of variants at known allele fractions.

The package has three programs: `addsnv.py` for single-nucleotide variants, `addindel.py` for insertions and deletions, and `addsv.py` for structural variants. The main use is building a "tumor" sample from a "normal" sample, so a somatic caller can be scored against a truth list. Each run writes a VCF of the variants it added.

Key behaviour from the `addsnv.py` options: sites need a minimum depth (`--mindepth`, default 10) and a minimum number of mutated reads (`--minmutreads`, default 3). The allele fraction defaults to 0.5 (`--mutfrac`) and can be set per site in the fourth column of the site file. Output coverage must stay close to input coverage (`--coverdiff`, default 0.9).

## When to use it

Use BAMSurgeon to benchmark somatic SNV, indel or SV callers when you need truth at known allele fractions inside realistic read data. The README adds a caution: check first whether validated data such as Genome in a Bottle or the PrecisionFDA truth challenge fit your question.

- Use [DWGSIM](dwgsim.md) when you want to simulate reads and variants together from a reference, with a truth VCF.
- Use [VarSim](varsim.md) for a full human diploid genome with germline and somatic variants and read simulation.
- Use [wgsim](wgsim.md) to make the starting reads for a small test of BAMSurgeon, as the recipe does.

## Install

Bioconda carries BAMSurgeon 1.4.1 (the same version as the latest GitHub release) as a noarch package. It depends on samtools, bwa, exonerate, velvet, wgsim, picard and pysam, and those have linux-aarch64 builds.

```bash
conda create -n bamsurgeon -c conda-forge -c bioconda bamsurgeon=1.4.1
conda activate bamsurgeon
addsnv.py -h
```

The README also says BAMSurgeon runs as a standalone Python script from a clone, once SAMtools, wgsim, BWA (or another supported aligner) and pysam are on the path. On the 1.4.1 tag, `addsnv.py` needs a Picard jar for the `mem` aligner. Pass `--picardjar` or set `BAMSURGEON_PICARD_JAR`. The current main branch marks `--picardjar` as deprecated with no effect.

## A first run

Adapted from the [BAMSurgeon README](https://github.com/adamewing/bamsurgeon#getting-started), which shows `addsv.py` on bundled test data. The recipe applies the same idea to SNVs. It first builds a small normal BAM from your reference: wgsim makes error-light reads, `bwa mem` aligns them, and samtools sorts and indexes. It then writes one site per line (contig, start, end, allele fraction) and runs:

```bash
addsnv.py -v snvs.bed -f normal.bam -r ref/ref.fa -o tumor.bam \
  --aligner mem --mindepth 10 --seed 42
```

The reference must be indexed with both `bwa index` and `samtools faidx`.

## Run the tested example

This recipe builds BAMSurgeon in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 14.9 s.

1. Download [bamsurgeon-recipe.tar.gz](https://biosimhub.pages.dev/guides/bamsurgeon/bamsurgeon-recipe.tar.gz) (Dockerfile, run_bamsurgeon.sh, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bamsurgeon-recipe.tar.gz
   cd bamsurgeon
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/bamsurgeon:1.4.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bamsurgeon:1.4.1 bash /opt/run_bamsurgeon.sh /work/in/reference.fa 10 0.5 40 42 > out/bamsurgeon_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_10909_10909.log` | 7.2 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_12727_12727.log` | 6.0 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_14546_14546.log` | 7.3 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_16364_16364.log` | 7.0 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_18181_18181.log` | 6.0 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_1819_1819.log` | 5.6 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_3637_3637.log` | 4.5 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_5454_5454.log` | 6.8 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_7272_7272.log` | 5.3 KB |
| `addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_9091_9091.log` | 5.4 KB |
| `bamsurgeon_log.txt` | 23.2 KB |
| `bwa_index.log` | 364 B |
| `bwa_mem.log` | 924 B |
| `normal.bam` | 222.3 KB |
| `normal.bam.bai` | 128 B |
| `ref/ref.fa` | 19.8 KB |
| `ref/ref.fa.amb` | 10 B |
| `ref/ref.fa.ann` | 57 B |
| `ref/ref.fa.bwt` | 19.6 KB |
| `ref/ref.fa.fai` | 27 B |
| `ref/ref.fa.pac` | 4.9 KB |
| `ref/ref.fa.sa` | 9.8 KB |
| `snvs.bed` | 270 B |
| `tumor.addsnv.snvs.vcf` | 2.1 KB |
| `tumor.bam` | 224.0 KB |
| `tumor.bam.bai` | 128 B |
| `wgsim.log` | 135 B |

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_10909_10909.log</code></summary>

```
read chr_example_10812_11263_1:0:0_0:0:0_61f,10811,S CAAGGGACAATTATTCACTAGCGCGGTTTGAAGTCACGACACAGGGGGGCTAACTGCTAGCAATTGGTATGCTGATGCTAAACATAACGTTCAGCCTTCA 
read chr_example_10435_10911_0:0:0_1:0:0_8ac,10811,S CTAGGGACAATTATTCACTAGCGCGGTTTGAAGTCACGACACAGGGGGGCTAACTGCTAGCAATTGGTATGCTGATGCTAAACATAACGTTCAGCCTTAA 
read chr_example_10408_10911_0:0:0_0:0:0_b2f,10811,S CAAGGGACAATTATTCACTAGCGCGGTTTGAAGTCACGACACAGGGGGGCTAACTGCTAGCAATTGGTATGCTGATGCTAAACATAACGTTCAGCCTTAA 
read chr_example_10443_10913_0:0:0_0:0:0_db6,10813,F AGGGACAATTATTCACTAGCGCGGTTTGAAGTCACGACACAGGGGGGCTAACTGCTAGCAATTGGTATGCTGATGCTAAACATAACGTTCAGCCTTAAAA 
read chr_example_10443_10914_0:0:0_0:0:0_43,10814,F GGGACAATTATTCACTAGCGCGGTTTGAAGTCACGACACAGGGGGGCTAACTGCTAGCAATTGGTATGCTGATGCTAAACATAACGTTCAGCCTTAAAAA 
read chr_example_10819_11364_0:0:0_0:0:0_88f,10818,F CAATTATTCACTAGCGCGGTTTGAAGTCACGACACAGGGGGGCTAACTGCTAGCAATTGGTATGCTGATGCTAAACATAACGTTCAGCCTTAAAAAGGCA 
read chr_example_10820_11284_1:0:0_0:0:0_187,10819,F AATTATTCACTAGCGCGGTTTGAAGTCACGAGACAGGGGGGCTAACTGCTAGCAATTGGTATGCTGATGCTAAACATAACGTTCAGCCTTAAAAAGGCAG 
read chr_example_10451_10919_0:0:0_0:0:0_aef,10819,S AATTATTCACTAGCGCGGTTTGAAGTCACGACACAGGGGGGCTAACTGCTAGCAATTGGTATG
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_12727_12727.log</code></summary>

```
read chr_example_12298_12727_0:0:0_0:0:0_312,12627,F TAAAACCAGCTCCTAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGCATTTCATTTCCAACCAGGAACT 
read chr_example_12274_12728_0:0:0_0:0:0_f7c,12628,S AAAACCAGCTCCTAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGCATTTCATTTCCAACCAGGAACTC 
read chr_example_12631_13110_0:0:0_0:0:0_8f,12630,S AACCAGCTCCTAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGCATTTCATTTCCAACCAGGAACTCTC 
read chr_example_12633_13123_0:0:0_0:0:0_bc1,12632,F CCAGCTCCTAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGCATTTCATTTCCAACCAGGAACTCTCGC 
read chr_example_12286_12732_0:0:0_0:0:0_412,12632,S CCAGCTCCTAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGCATTTCATTTCCAACCAGGAACTCTCGC 
read chr_example_12637_13057_0:0:0_0:0:0_27c,12636,S CTCCTAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGCATTTCATTTCCAACCAGGAACTCTCGCCATA 
read chr_example_12330_12738_0:0:0_0:0:0_9dc,12638,S CCTAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGCATTTCATTTCCAACCAGGAACTCTCGCCATAAT 
read chr_example_12274_12740_0:0:0_0:0:0_1,12640,F TAAAGTGGAACATCTGGCGACCCCACAACAACAAAAATCAATAGCCAAGCACCGTCAATTTAGGC
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_14546_14546.log</code></summary>

```
read chr_example_14449_14941_0:0:0_0:0:0_47a,14448,S GGCGTAGTTAAAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTAGGAGAACAGGATCCC 
read chr_example_14450_15037_0:0:0_0:0:0_3ce,14449,S GCGTAGTTAAAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTAGGAGAACAGGATCCCA 
read chr_example_14003_14551_0:0:0_0:0:0_377,14451,F GTAGTTAAAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTAGGAGAACAGGATCCCATA 
read chr_example_14454_14922_0:0:0_0:0:0_72f,14453,S AGTTAAAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTAGGAGAACAGGATCCCATATC 
read chr_example_14454_14963_0:0:0_0:0:0_ac0,14453,S AGTTAAAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTAGGAGAACAGGATCCCATATC 
read chr_example_14459_14866_0:0:0_0:0:0_466,14458,F AAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTAGGAGAACAGGATCCCATATCCACTC 
read chr_example_14459_14914_0:0:0_0:0:0_de6,14458,F AAATAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTAAGTGAGCCTAGGAGAACAGGATCCCATATCCACTC 
read chr_example_14462_14995_0:0:0_0:0:0_66f,14461,F TAGCCAACAGTCGGTGCCCAGACATCCAGTGTTTTCACTGGGCCAATTCGCTGGGTTCGCTA
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_16364_16364.log</code></summary>

```
read chr_example_15876_16365_0:0:0_0:0:0_78a,16265,S CGATTCCAGAGTGGCTCGACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGAATGGTTAATTCATTTACGCA 
read chr_example_15887_16367_0:0:0_0:0:0_196,16267,S ATTCCAGAGTGGCTCGACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGAATGGTTAATTCATTTACGCATC 
read chr_example_16269_16798_0:0:0_0:0:0_7c4,16268,F TTCCAGAGTGGCTCGACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGAATGGTTAATTCATTTACGCATCC 
read chr_example_15931_16370_0:0:0_0:0:0_290,16270,S CCAGAGTGGCTCGACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGAATGGTTAATTCATTTACGCATCCGA 
read chr_example_16281_16817_0:0:0_0:0:0_885,16280,F TCGACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGAATGGTTAATTCATTTACGCATCCGACCACAGTACA 
read chr_example_16283_16793_0:0:0_0:0:0_6ea,16282,F GACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGAATGGTTAATTCATTTACGCATCCGACCACAGTACAGC 
read chr_example_16284_16794_0:0:0_0:0:0_c45,16283,F ACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGAATGGTTAATTCATTTACGCATCCGACCACAGTACAGCG 
read chr_example_16284_16768_0:0:0_0:0:0_ede,16283,S ACAGTTGATGGCACCCTAGTTTCTAGTCTACGCCTCCTAATGCTTCGAAAGTGGGGGCTTGA
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_18181_18181.log</code></summary>

```
read chr_example_18088_18660_0:0:0_0:0:0_274,18087,F ATTATGATCGAATGCTAGGCTCATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCAATGACTCACAGGAACGCTAGGTGTTGACCCCCAG 
read chr_example_17724_18188_0:0:0_0:0:0_943,18088,F TTATGATCGAATGCTAGGCTCATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCAATGACTCACAGGAACGCTAGGTGTTGACCCCCAGT 
read chr_example_18091_18653_0:0:0_0:0:0_f35,18090,F ATGATCGAATGCTAGGCTCATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCAATGACTCACAGGAACGCTAGGTGTTGACCCCCAGTGC 
read chr_example_18097_18593_0:0:0_0:0:0_4aa,18096,F GAATGCTAGGCTCATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCAATGACTCACAGGAACGCTAGGTGTTGACCCCCAGTGCAGCCGG 
read chr_example_17811_18196_1:0:0_1:0:0_d47,18096,F GAATGCTAGGCTCATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCTATGACTCACAGGAACGCTAGGTGTTGACCCCCAGTGCAGCCGG 
read chr_example_18102_18636_0:0:0_0:0:0_334,18101,S CTAGGCTCATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCAATGACTCACAGGAACGCTAGGTGTTGACCCCCAGTGCAGCCGGGGGCT 
read chr_example_18104_18581_0:0:0_0:0:0_10d,18103,S AGGCTCATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCAATGACTCACAGGAACGCTAGGTGTTGACCCCCAGTGCAGCCGGGGGCTTA 
read chr_example_18110_18586_0:0:0_0:0:0_260,18109,F ATATGAGAGCTAACCAATGCTAAAGTTACAGATACTGCACGGCAATGACTCACAGGAACGCT
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_1819_1819.log</code></summary>

```
read chr_example_1720_2213_0:0:0_0:0:0_d54,1719,F CGTGATTCCGATTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGTG 
read chr_example_1402_1822_0:0:0_0:0:0_77f,1722,F GATTCCGATTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGTGACG 
read chr_example_1725_2147_0:0:0_0:0:0_ac6,1724,F TTCCGATTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGTGACGAC 
read chr_example_1726_2278_0:0:0_0:0:0_d19,1725,S TCCGATTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGTGACGACG 
read chr_example_1363_1827_0:0:0_0:0:0_206,1727,S CGATTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGTGACGACGTA 
read chr_example_1330_1827_0:0:0_0:0:0_6ae,1727,S CGATTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGTGACGACGTA 
read chr_example_1731_2258_0:0:0_0:0:0_f8f,1730,F TTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGTGACGACGTATGG 
read chr_example_1733_2368_0:0:0_0:0:0_47b,1732,S CGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCCAGGAAAGT
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_3637_3637.log</code></summary>

```
read chr_example_3538_4034_0:0:0_0:0:0_d78,3537,S GAGCTTCACATCTGGCGCCGTGTGCCTAACACTGGATCGTAGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCA 
read chr_example_3540_4052_0:0:0_0:0:0_355,3539,F GCTTCACATCTGGCGCCGTGTGCCTAACACTGGATCGTAGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCAGT 
read chr_example_3540_3994_0:0:0_1:0:0_513,3539,S GCTTCACATCTGGCGCCGTGTGCCTAACACTGGATCGTAGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCAGT 
read chr_example_3161_3640_0:0:0_0:0:0_f8,3540,S CTTCACATCTGGCGCCGTGTGCCTAACACTGGATCGTAGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCAGTC 
read chr_example_3543_4120_0:0:0_0:0:0_7a9,3542,F TCACATCTGGCGCCGTGTGCCTAACACTGGATCGTAGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCAGTCGT 
read chr_example_3561_4013_0:0:0_0:0:0_134,3560,F GCCTAACACTGGATCGTAGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCAGTCGTTAGGTGTTGACTTCGACG 
read chr_example_3561_4040_0:0:0_1:0:0_adb,3560,F GCCTAACACTGGATCGTAGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCAGTCGTTAGGTGTTGACTTCGACG 
read chr_example_3177_3661_0:0:0_1:0:0_3bd,3561,F CCTAACACTGGATCGTTGTGGGGTATTGAAATTGCTAGTCAGCCATCGCGATTATTGGGCTAGCCACGCGAGTGCAGTCGTTAGGTG
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_5454_5454.log</code></summary>

```
read chr_example_4965_5456_0:0:0_0:0:0_e85,5356,F CGGACGACATTCCGAAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAAACGATTAGG 
read chr_example_4986_5460_0:0:0_1:0:0_8e0,5360,F CGACATTCCGAAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAAACGATTAGCGCAT 
read chr_example_4911_5461_0:0:0_0:0:0_392,5361,F GACATTCCGAAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAAACGATTAGGGCATA 
read chr_example_5364_5914_1:0:0_0:0:0_ef,5363,F CATTCCGAAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAACCGATTAGGGCATAGG 
read chr_example_5365_5886_0:0:0_0:0:0_d11,5364,S ATTCCGAAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAAACGATTAGGGCATAGGC 
read chr_example_5368_5845_0:0:0_1:0:0_32c,5367,F CCGAAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAAACGATTAGGGCATAGGCCTG 
read chr_example_4961_5468_0:0:0_1:0:0_1c2,5368,F CGAAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAAACGATTAGGGCATACGCCTGG 
read chr_example_5023_5470_0:0:0_0:0:0_e09,5370,S AAGTTGATTCTAGAGGCACCACGACCCTGAAGATACCTGTGACAGTCTCGCTAGGTTTAATTCCTTCAGTAGTCAAAACGATTAGGG
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_7272_7272.log</code></summary>

```
read chr_example_7173_7616_1:0:0_0:0:0_8cb,7172,F CTTATAATCACCGTGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAAGATACTCAGATCAACCCCGGTAGTCTCTACGTCTCGAGTCTTAC 
read chr_example_6734_7272_0:0:0_0:0:0_9f0,7172,S CTTATAATCACCGTGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAAGATACTCAGATCAACCCCGGTAGTCTCGACGTCTCGAGTCTTAC 
read chr_example_6839_7273_0:0:0_0:0:0_5fc,7173,F TTATAATCACCGTGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAAGATACTCAGATCAACCCCGGTAGTCTCGACGTCTCGAGTCTTACA 
read chr_example_7176_7641_0:0:0_0:0:0_283,7175,F ATAATCACCGTGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAAGATACTCAGATCAACCCCGGTAGTCTCGACGTCTCGAGTCTTACAAG 
read chr_example_6768_7276_0:0:0_0:0:0_c85,7176,S TAATCACCGTGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAAGATACTCAGATCAACCCCGGTAGTCTCGACGTCTCGAGTCTTACAAGA 
read chr_example_6792_7282_0:0:0_0:0:0_7f5,7182,F CCGTGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAAGATACTCAGATCAACCCCGGTAGTCTCGACGTCTCGAGTCTTACAAGATAAACA 
read chr_example_7184_7661_0:0:0_0:0:0_50d,7183,S CGTGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAAGATACTCAGATCAACCCCGGTAGTCTCGACGTCTCGAGTCTTACAAGATAAACAC 
read chr_example_6811_7285_0:0:0_1:0:0_c27,7185,F TGCGCGCACGAAGAAATTTGATCACTGGTAGGGAAATATATAACATACTCAGATCAACCCCGGTAGTCTCGACGTCTCGAGTCTTA
```

</details>

<details><summary>First lines of <code>addsnv_logs_tumor.bam/tumor.bam.haplo_chr_example_9091_9091.log</code></summary>

```
read chr_example_8994_9505_0:0:0_0:0:0_e03,8993,S TGAACGCCCTCGGGCGATTGTGACTATCTTTGACTCGAGGTGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGCGTT 
read chr_example_8687_9096_0:0:0_0:0:0_d22,8996,S ACGCCCTCGGGCGATTGTGACTATCTTTGACTCGAGGTGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGCGTTTGC 
read chr_example_9000_9505_0:0:0_0:0:0_9f8,8999,F CCCTCGGGCGATTGTGACTATCTTTGACTCGAGGTGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGCGTTTGCTCA 
read chr_example_9001_9473_0:0:0_0:0:0_d8a,9000,F CCTCGGGCGATTGTGACTATCTTTGACTCGAGGTGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGCGTTTGCTCAT 
read chr_example_8574_9100_0:0:0_0:0:0_2a8,9000,S CCTCGGGCGATTGTGACTATCTTTGACTCGAGGTGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGCGTTTGCTCAT 
read chr_example_9002_9558_0:0:0_0:0:0_ed8,9001,S CTCGGGCGATTGTGACTATCTTTGACTCGAGGTGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGCGTTTGCTCATG 
read chr_example_8641_9102_0:0:0_0:0:0_108,9002,F TCGGGCGATTGTGACTATCTTTGACTCGAGGTGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGCGTTTGCTCATGT 
read chr_example_8691_9104_0:0:0_1:0:0_e28,9004,S GGGCGATTGTGACTATCTTTGACTCGAGGGGTGAAGCTCGCTCTGAAAATGTCCTCGTATCTCAGCCCAAGAAGGGAGAGGGCTGC
```

</details>

<details><summary>First lines of <code>bamsurgeon_log.txt</code></summary>

```
ERROR StatusConsoleListener Could not determine local host name
 java.net.UnknownHostException: jdk.internal.util.Exceptions$NonSocketInfo@2c35e84705a16c6f44de: Temporary failure in name resolution
	at java.base/java.net.InetAddress.getLocalHost(InetAddress.java:1800)
	at org.apache.logging.log4j.core.util.NetUtils.getLocalHostname(NetUtils.java:56)
	at org.apache.logging.log4j.core.LoggerContext.lambda$setConfiguration$0(LoggerContext.java:615)
	at java.base/java.util.concurrent.ConcurrentHashMap.computeIfAbsent(ConcurrentHashMap.java:1724)
	at org.apache.logging.log4j.core.LoggerContext.setConfiguration(LoggerContext.java:615)
	at org.apache.logging.log4j.core.LoggerContext.reconfigure(LoggerContext.java:694)
	at org.apache.logging.log4j.core.LoggerContext.reconfigure(LoggerContext.java:711)
	at org.apache.logging.log4j.core.LoggerContext.start(LoggerContext.java:253)
	at org.apache.logging.log4j.core.impl.Log4jContextFactory.getContext(Log4jContextFactory.java:155)
	at org.apache.logging.log4j.core.impl.Log4jContextFactory.getContext(Log4jContextFactory.java:47)
```

</details>

<details><summary>First lines of <code>bwa_index.log</code></summary>

```
[bwa_index] Pack FASTA... 0.00 sec
[bwa_index] Construct BWT for the packed sequence...
[bwa_index] 0.00 seconds elapse.
[bwa_index] Update BWT... 0.00 sec
[bwa_index] Pack forward-only FASTA... 0.00 sec
[bwa_index] Construct SA from BWT and Occ... 0.00 sec
[main] Version: 0.7.19-r1273
[main] CMD: bwa index ref/ref.fa
[main] Real time: 0.011 sec; CPU: 0.005 sec
```

</details>

<details><summary>First lines of <code>bwa_mem.log</code></summary>

```
[M::bwa_idx_load_from_disk] read 0 ALT contigs
[M::process] read 8000 sequences (800000 bp)...
[M::mem_pestat] # candidate unique pairs for (FF, FR, RF, RR): (0, 4000, 0, 0)
[M::mem_pestat] skip orientation FF as there are not enough pairs
[M::mem_pestat] analyzing insert size distribution for orientation FR...
[M::mem_pestat] (25, 50, 75) percentile: (466, 498, 533)
[M::mem_pestat] low and high boundaries for computing mean and std.dev: (332, 667)
[M::mem_pestat] mean and std.dev: (499.21, 49.39)
[M::mem_pestat] low and high boundaries for proper pairs: (265, 734)
[M::mem_pestat] skip orientation RF as there are not enough pairs
[M::mem_pestat] skip orientation RR as there are not enough pairs
[M::mem_process_seqs] Processed 8000 reads in 0.095 CPU sec, 0.096 real sec
```

</details>

<details><summary>First lines of <code>ref/ref.fa</code></summary>

```
>chr_example random 20 kb sequence
GCTAAAGACAATTACATAACATACACGTCAGCACGAAACTTGTTGGCCCAGTGTGAATCGCTTAAGGGTT
AAGTAAGTGTGATGCATACGCCTTTACTTGCTGTGTCCACCCCATCGGACTGGCATTTTTATTACACTCA
GAAACAGAACTCGGGTAATTTTGACAGGTCACGCAGAGGCGCGCCCTCCTGAAGTGCGTGGACACTCGCT
ATGAATCTCTGATTTACCCACTCTGCCAAACTCCAGCGCGGTCAGTTCCATCACCCTAAGTAACCGAATA
ATGCGTTCGCTCTATTGACTACGACGCGCTCATTCCCTTGTCGGAGAGTTATGGAACAAGGACGCTGTCT
GAGACTAGAAGACAGATAGTGCACACGACCGGCGTCGGAGAAACTCTATTTGCCGCCTGACAAGTCAATG
CGATCCGTAGGGGCAGCGCAGTATGCCAAGACTATAGGCACTGTCGCATCACAAACGATTAACTGATAAA
TGAGCCCTTTATGACACGGGCATATGACTGGTTTACGATAGTATGTCCAACGGCGAGCTTTACATTTGCT
GTGAGAGGTACAGGGATTAGTGAGAAGCCGTGCGTATCAATTCGTACCTTGGGGGTCGTTACCACTCTGT
TCCCACGAGCGGCATTTCTGGATGGCCAGCTTTTGACATTTAATTTCACCCATAAACCAGCGTAAAGCTG
CAAGTGGCTCCATGAACTTAGCTGCTAGTGTCAGACTCGCCTCGGATCCTTACTACACTAACTTGAACGC
```

</details>

<details><summary>First lines of <code>ref/ref.fa.amb</code></summary>

```
20000 1 0
```

</details>

<details><summary>First lines of <code>ref/ref.fa.ann</code></summary>

```
20000 1 11
0 chr_example random 20 kb sequence
0 20000 0
```

</details>

<details><summary>First lines of <code>ref/ref.fa.fai</code></summary>

```
chr_example	20000	35	70	71
```

</details>

<details><summary>First lines of <code>snvs.bed</code></summary>

```
chr_example	1818	1819	0.5
chr_example	3636	3637	0.5
chr_example	5454	5455	0.5
chr_example	7272	7273	0.5
chr_example	9090	9091	0.5
chr_example	10909	10910	0.5
chr_example	12727	12728	0.5
chr_example	14545	14546	0.5
chr_example	16363	16364	0.5
chr_example	18181	18182	0.5
```

</details>

<details><summary>First lines of <code>tumor.addsnv.snvs.vcf</code></summary>

```
##fileformat=VCFv4.1
##fileDate=2026-10-18
##phasing=none
##contig=<ID=chr_example,length=20000>
##INDIVIDUAL=TRUTH
##SAMPLE=<ID=TRUTH,Individual="TRUTH",Description="BAMSurgeon spike-in">
##INFO=<ID=CIPOS,Number=2,Type=Integer,Description="Confidence interval around POS for imprecise variants">
##INFO=<ID=IMPRECISE,Number=0,Type=Flag,Description="Imprecise structural variation">
##INFO=<ID=PRECISE,Number=0,Type=Flag,Description="Precise structural variation">
##INFO=<ID=SVTYPE,Number=1,Type=String,Description="Type of structural variant">
##INFO=<ID=SVLEN,Number=1,Type=Integer,Description="Difference in length between REF and ALT alleles">
##INFO=<ID=SOMATIC,Number=0,Type=Flag,Description="Somatic mutation in primary">
```

</details>

<details><summary>First lines of <code>wgsim.log</code></summary>

```
[wgsim] seed = 42
[wgsim_core] calculating the total length of the reference sequence...
[wgsim_core] 1 sequences, total length: 20000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `snvs` | SNVs to add | 10 | 1 to 200 |
| `vaf` | Allele fraction of each SNV | 0.5 | 0.05 to 1 |
| `coverage` | Coverage of the normal BAM | 40 | 20 to 100 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `normal.bam` and its index are the unmodified reads from the helper step.
- `tumor.bam` is the same reads with the chosen bases changed in a share of reads at each site. Index it before use.
- `tumor.addsnv.snvs.vcf` lists the added variants. By the 1.4.1 source the name is the output BAM name, `.addsnv.`, and the site file name. The header marks the sample as `SPIKEIN` and carries `SOMATIC` and `VAF` INFO fields.
- `snvs.bed` is the site list the helper wrote.

Open `tumor.bam` and `normal.bam` side by side in a viewer at one of the sites. About the requested allele fraction of reads should carry the new base in `tumor.bam`. Small samples show noise, since depth is finite: a site with 40 reads at 0.5 fraction is a binomial draw, not exactly 20.

If a site is skipped, the log on standard error says why. Common reasons are low depth, a nearby SNP that would create a haplotype conflict, or a coverage change after realignment. Check that the VCF row count matches the number of sites you requested.

## Pitfalls

- **Coverage rules drop sites.** Sites under the minimum depth are skipped, and a run with no successful mutation exits with "no succesful mutations".
- **The aligner must match the data.** The default is `backtrack` (`bwa aln`). The recipe uses `mem`, matching how the normal BAM was made. The 1.4.1 source also lists novoalign, gsnap, STAR, bowtie2, tmap, bwakit and minimap2, and some need extra `--alignopts`.
- **Nearby sites merge into haplotypes.** With `-z` above 0, sites within that distance are mutated together.
- **Variants are drawn, not chosen.** The alternate base is random unless you add it as a fifth column.
- **Truth is only as good as the realignment.** A caller can miss a variant for reasons that come from the aligner, not the caller. Read the BAMSurgeon paper before you quote sensitivity.
- **Use `--tmpdir` on a writable disk.** The tool writes many temporary BAMs and merges them.

## Further reading

- README: https://github.com/adamewing/bamsurgeon
- Manual (PDF in the repository): https://github.com/adamewing/bamsurgeon/tree/master/doc
- Bioconda recipe: https://bioconda.github.io/recipes/bamsurgeon/README.html
- Paper: Ewing AD et al. (2015). Combining tumor genome simulation with crowdsourcing to benchmark somatic single-nucleotide-variant detection. Nature Methods 12:623-630. https://doi.org/10.1038/nmeth.3407

---

Cite: Ewing AD, Houlahan KE, Hu Y, et al.; ICGC-TCGA DREAM Somatic Mutation Calling Challenge participants (2015). Combining tumor genome simulation with crowdsourcing to benchmark somatic single-nucleotide-variant detection. Nature Methods 12:623-630. doi:10.1038/nmeth.3407

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bamsurgeon).
