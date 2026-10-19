# LRSim

> Simulate 10x Genomics-style linked reads (barcoded molecules, two haplotypes with random variants) from a reference FASTA.

Licence: MIT · [Source code](https://github.com/aquaskyline/LRSIM)

## What it simulates

LRSim simulates 10x Genomics linked reads. It builds two haplotypes from a reference by adding SNPs, indels, duplications, inversions and translocations. It cuts long molecules from them and drops several molecules into each of many partitions. Each partition gets one barcode. Paired-end Illumina-style reads (made with [DWGSIM](dwgsim.md)) from the molecules in a partition share that barcode. You give a reference and the variant, molecule and read settings. It returns barcoded FASTQ files, the two haplotype FASTAs and BED files of the variants.

Key assumptions: molecule length follows the mean you set, molecules per partition is an average, and the ratio of homozygous to heterozygous variants is fixed at 1:2.

## When to use it

- Test a linked-read phasing or SV caller with known haplotypes.
- Study how molecule length and partition load change barcode sharing.
- Make truth sets of structural variants on a small genome.

Alternatives: DWGSIM and [wgsim](wgsim.md) simulate plain paired-end reads with no barcodes. [PBSIM3](pbsim3.md) and [SimLoRD](simlord.md) simulate long reads directly.

## Install it yourself

LRSim 1.0 is on bioconda for linux-64 (dry-run resolved, build `pl5321hbcd995c_0`, 17 MB). The package is a Perl pipeline with DWGSIM, SURVIVOR and samtools inside.

```
conda create -n lrsim -c conda-forge -c bioconda lrsim=1.0
conda activate lrsim
```

Minimal command (the barcode list ships with the package):

```
lrsim -r reference.fa -p lr -b $CONDA_PREFIX/share/lrsim/4M-with-alts-february-2016.txt -x 0.02 -t 1 -f 5 -m 5
```

Defaults from the help text: 2 haplotypes, 1 SNP per 1000 bp, 1000 indels (1 to 50 bp), 100 each of duplications, inversions and translocations (1000 to 10000 bp), read-pair outer distance 350 (SD 35), 600 million pairs, 100 kb molecules, 1500 thousand partitions, 10 molecules per partition, 8 DWGSIM threads. The defaults suit a human genome. The example overrides them for a 60 kb reference.

## Run the tested example

This recipe builds LRSim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 14.6 s. LRSim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [lrsim-recipe.tar.gz](https://biosimhub.pages.dev/guides/lrsim/lrsim-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf lrsim-recipe.tar.gz
   cd lrsim
   sh run.sh
   ```

![Terminal recording of the LRSim example run](https://biosimhub.pages.dev/media/lrsim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/lrsim:1.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/lrsim:1.0 lrsim -o -r /work/in/reference.fa -p lr -b /opt/conda/share/lrsim/4M-with-alts-february-2016.txt \
    -d 2 -z 2 -x 0.02 -f 5 -m 5 -t 1 -1 1000 -4 5 -7 1 -0 1 -5 100 -6 500 -8 100 -9 500 \
    -i 350 -s 35 > out/lrsim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `_Inline/.lock` | 0 B |
| `_Inline/config-x86_64-linux-thread-multi-5.032001` | 206 B |
| `_Inline/lib/auto/simulateLinkedReads_pl_4e07/simulateLinkedReads_pl_4e07.inl` | 1.0 KB |
| `_Inline/lib/auto/simulateLinkedReads_pl_4e07/simulateLinkedReads_pl_4e07.so` | 20.5 KB |
| `lr.0.fp` | 472.9 KB |
| `lr.0.manifest` | 409.3 KB |
| `lr.0.sort.manifest` | 409.3 KB |
| `lr.1.fp` | 473.4 KB |
| `lr.1.manifest` | 409.3 KB |
| `lr.1.sort.manifest` | 409.3 KB |
| `lr.dwgsim.0.12.fastq` | 9.5 MB |
| `lr.dwgsim.1.12.fastq` | 9.5 MB |
| `lr.hap.0.clean.fasta` | 60.0 KB |
| `lr.hap.0.clean.fasta.fai` | 42 B |
| `lr.hap.0.fasta` | 59.7 KB |
| `lr.hap.1.clean.fasta` | 60.0 KB |
| `lr.hap.1.clean.fasta.fai` | 42 B |
| `lr.hap.1.fasta` | 59.8 KB |
| `lr.hap.hetA.bed` | 856 B |
| `lr.hap.hetA.insertions.fa` | 53 B |
| `lr.hap.hetB.bed` | 580 B |
| `lr.hap.hetB.insertions.fa` | 81 B |
| `lr.hap.homAB.bed` | 574 B |
| `lr.hap.homAB.insertions.fa` | 40 B |
| `lr.hap.parameter` | 629 B |
| `lr.hapA.fasta` | 59.7 KB |
| `lr.hapB.fasta` | 59.8 KB |
| `lr.status` | 2.8 KB |
| `lr_S1_L001_R1_001.fastq.gz` | 1.2 MB |
| `lr_S1_L001_R2_001.fastq.gz` | 1.3 MB |
| `lr_S1_L002_R1_001.fastq.gz` | 1.3 MB |
| `lr_S1_L002_R2_001.fastq.gz` | 1.3 MB |
| `lrsim_log.txt` | 0 B |

<details><summary>First lines of <code>_Inline/config-x86_64-linux-thread-multi-5.032001</code></summary>

```
version : 0.87
languages : %
    C : C
    Foo : Foo
    foo : Foo
types : %
    C : compiled
    Foo : interpreted
modules : %
    C : Inline::C
    Foo : Inline::Foo
suffixes : %
```

</details>

<details><summary>First lines of <code>_Inline/lib/auto/simulateLinkedReads_pl_4e07/simulateLinkedReads_pl_4e07.inl</code></summary>

```
md5 : 4e0722ffaa544b99f7939592138adc6e
name : simulateLinkedReads_pl_4e07
version : ""
language : C
language_id : C
installed : 0
date_compiled : Mon Oct 12 06:07:00 2026
inline_version : 0.87
ILSM : %
    module : Inline::C
    suffix : so
    type : compiled
```

</details>

<details><summary>First lines of <code>lr.0.manifest</code></summary>

```
7362670	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
7077752	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
8093874	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
8093206	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
5982072	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
1211806	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
1477944	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
455556	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
4218800	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
5155984	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
440896	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
3817440	TTTGTGTAGTGGGTTG	AAAFFFKKKKKKKKKK
```

</details>

<details><summary>First lines of <code>lr.0.sort.manifest</code></summary>

```
0	AACATCGAGTGTCTCA	AAAFFFKKKKKKKKKK
664	CGTGTCTTCTTCGGTC	AAAFFFKKKKKKKKKK
1328	CGTGTGGCAGGGTCAA	AAAFFFKKKKKKKKKK
1992	GGCTCGACAGTGGGAT	AAAFFFKKKKKKKKKK
2656	TGATTCTGTTCCCTAC	AAAFFFKKKKKKKKKK
3320	ACCATTTCAAGCGCTC	AAAFFFKKKKKKKKKK
3980	CTTATACTCCTCCTAG	AAAFFFKKKKKKKKKK
4644	CCGGTAGTCAAGAGGC	AAAFFFKKKKKKKKKK
5968	GACACATAGGACTGGT	AAAFFFKKKKKKKKKK
7292	TAAGGCTGTGATAAAC	AAAFFFKKKKKKKKKK
7952	CGTCTACAGAGGGCGA	AAAFFFKKKKKKKKKK
8616	TACCTATGTATTCGCA	AAAFFFKKKKKKKKKK
```

</details>

<details><summary>First lines of <code>lr.1.manifest</code></summary>

```
4440218	GTACGATTCTTAACCT	AAAFFFKKKKKKKKKK
4188026	GTACGATTCTTAACCT	AAAFFFKKKKKKKKKK
5008152	GTACGATTCTTAACCT	AAAFFFKKKKKKKKKK
1929436	GTACGATTCTTAACCT	AAAFFFKKKKKKKKKK
2242864	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
3626830	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
3062148	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
6006180	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
9769810	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
9771150	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
9793854	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
7755640	GCTCTGTGTCTAGGGA	AAAFFFKKKKKKKKKK
```

</details>

<details><summary>First lines of <code>lr.1.sort.manifest</code></summary>

```
0	ACTGCTCGTGGTCGTC	AAAFFFKKKKKKKKKK
664	CGGTACGCAATACGCT	AAAFFFKKKKKKKKKK
1328	CGATAACAGATATGCA	AAAFFFKKKKKKKKKK
1992	AGGTAAATCAAGGCTT	AAAFFFKKKKKKKKKK
2656	TTTGCGCGTCATGTTG	AAAFFFKKKKKKKKKK
3320	GCGCCAATCACAGAGG	AAAFFFKKKKKKKKKK
3980	CTTTGCGAGATGTGGC	AAAFFFKKKKKKKKKK
4644	GGATGTTCAGTCGTGC	AAAFFFKKKKKKKKKK
5308	GGAACTTAGAGCTGCA	AAAFFFKKKKKKKKKK
5968	CTCGTACCAGGAAGGG	AAAFFFKKKKKKKKKK
6628	GACGGCTAGTTCACTG	AAAFFFKKKKKKKKKK
7292	CTCGAGGAGTCGGGAT	AAAFFFKKKKKKKKKK
```

</details>

<details><summary>First lines of <code>lr.dwgsim.0.12.fastq</code></summary>

```
@chr1_20031_19789_1_0_0_0_0:0:0_1:0:0_0/1
TTTGCAGTGCAACAGCATAATACTGACTAATGGACGTCATCCCTCGGCGTGATTCACTACACGAAAGCTAGTCACTGCCCTCGAGACTACACTTCCCATCCACAGAGAACGGGTCCGACCGGGAACACCACCCGC
+
IFEGGGEHHEGFEGGFEDGFDDDGAABCGCGDAB=CEBBBFABC@BBCBA=AAAA@AAA?AAB@C@@>A@?C?A?>B@@?@A?>?A>@>@?@=@<@>>?=C==?:>?=<>?=>@>@>@>@@<======9<?>>==
@chr1_20031_19789_1_0_0_0_0:0:0_1:0:0_0/2
ATCCTATGAGGAACCAGGGTTGACTATCAAACAGCCCCCTCCGGTGCTGAGAAGCTCGCGCTGGAAACTATACCTCCTCCCCTCCATGAAAATGGAACGCTCAACTGCAAATTGACTGTTATGCTACCCCAATTGTGGCACTCCGCGTTGA
+
HGHIGEIHIFFCIEBFEFDAHBDCDDCBDFFFCDCBBEEACB>DBE?@A>BDA??BABAA>CA@>@>@@?>@>?CACA@B?A?A=??A>?@@?>???<?A@B?>>B@@=>=>=@>?@>?>=A>??@>>?<B>=D><?;9;;<:>>>?;=;>
@chr1_15121_14943_1_0_0_0_0:0:0_0:0:0_1/1
CAAGCCCTTGCCCGTGTTCAAGGTGAGTAAGACGGTCTTAAGTTGAAGGTGTGCTGTGGGGAGAAGGTCCGGGTGGTTACCGTAAAGGAGCTGACTTAAATCAGATATTGCAAAGGTTGCGGATGGTTTCGACGT
+
IIHGIHGGFHDICGEIEHDGHDGECCADFBCBEBBGACEEADCABAA@ACACACA@:@A@@BC>AACA?AB@??@??@BB>A?A=@>??<?@A:?>><>9A>>>D?@?<?><C@?B?>?<=<>===??>@=>>=@
```

</details>

<details><summary>First lines of <code>lr.dwgsim.1.12.fastq</code></summary>

```
@chr1_20078_19836_1_0_0_0_0:0:0_1:0:0_0/1
CTAATGGACGTCATCCCTCGGCGTGATTCACTACACGAAAGCTAGTCACTGCCCTCGAGACTACACTTCCCATCCACAGAGAACGGGTCCGACCGGGAACACCACCCGCCTCCATTAGTACTCTCTGCAATGAAG
+
IFEGGGEHHEGFEGGFEDGFDDDGAABCGCGDAB=CEBBBFABC@BBCBA=AAAA@AAA?AAB@C@@>A@?C?A?>B@@?@A?>?A>@>@?@=@<@>>?=C==?:>?=<>?=>@>@>@>@@<======9<?>>==
@chr1_20078_19836_1_0_0_0_0:0:0_1:0:0_0/2
GCTTCGAAGACTTAGCATGGCCATAAATCCTATGAGGAACCAGGGTTGACTATCAAACAGCCCCCTCCGGTGCTGAGAAGCTCGCGCTGGAAAGTATACCTCCTCCCCTCCATGTAAATCGAACGCTCAACTGCAAATTGACTGTTATGCT
+
HGHIGEIHIFFCIEBFEFDAHBDCDDCBDFFFCDCBBEEACB>DBE?@A>BDA??BABAA>CA@>@>@@?>@>?CACA@B?A?A=??A>?@@?>???<?A@B?>>B@@=>=>=@>?@>?>=A>??@>>?<B>=D><?;9;;<:>>>?;=;>
@chr1_15156_14978_1_0_0_0_0:0:0_0:0:0_1/1
TAAGTTGAAGGTGTGCTGTGGGGAGAAGGTCCGGGTGGTTACCGTAAAGGAGCTGACTTAAATCAGATATTGCAAAGGTTGCGGATGGTTTCGACGTTCCCCATTTTTTGCCTCCCAGGTGCTCAGTTCAATAGC
+
IIHGIHGGFHDICGEIEHDGHDGECCADFBCBEBBGACEEADCABAA@ACACACA@:@A@@BC>AACA?AB@??@??@BB>A?A=@>??<?@A:?>><>9A>>>D?@?<?><C@?B?>?<=<>===??>@=>>=@
```

</details>

<details><summary>First lines of <code>lr.hap.0.clean.fasta</code></summary>

```
>chr1
CAGATTTTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGT
CCCACCTGGTGATCCTATGCTTGTGAGTACCCAGAAAATAGCGACGGACCGCGGTGTTAAGTGTCGAGCT
ACATCACTTCTCATGTAGCCAGAAAGCTGCAACTCATCGACTCTATGTAGTGACCGCGTCGATGTCAAAC
CCCGGGGGGAGCTCAGATATCCGATACAGGGATGAAGAAATAACCTCATCCCATTGGTGACGAAAGGTTG
TAAGTAGCTGGCCGCCGAGATAGCTGAGCGGCGAACCACTAGAAAAGGTTCAGACCCCGGAGCCCAGCCG
TCACGATTGTTATGCGTATAAGCCCGGTTCACTACGTCCGTTCTGGCAAGCCGGGGCTAATCCGTCATTG
TCAAGAGACATCTTTCGTCTCATTAGGCTACTAACGCCGCCGGGTCGTTACTCGAAATCGATTTGATCGA
TCTGCAAGGTGCTGTCTAGATAGATACCATGGCCCGGAAGTACGGGCTTCTGGCGCATGTCGCACTCGTC
CCTGGTCACGAACTGTACAAACATTGGACACTCTTTCCCGTTCTGGTACAAAATGTGCTCCAATCATGCA
TGAAACATATACATCGCTTGGGCCACGTAGTCTAGAGCACACTAAATGAGACATCTTAGAGGAGATAGGC
GTAGATCCGGTTACTAGCCGTGATGCAAGGTGGGGGAACGGGATGTTGTAACATGCGGGTGTGCACGCCA
```

</details>

<details><summary>First lines of <code>lr.hap.0.clean.fasta.fai</code></summary>

```
chr1	39948	6	70	71
chr2	20578	40531	70	71
```

</details>

<details><summary>First lines of <code>lr.hap.0.fasta</code></summary>

```
>chr1
CAGATTTTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGTCCCACCTGGTGATCCTATGCTTGTGAGTAC
CCAGAAAATAGCGACGGACCGCGGTGTTAAGTGTCGAGCTACATCACTTCTCATGTAGCCAGAAAGCTGCAACTCATCGACTCTATGTAGTGACCGCGTC
GATGTCAAACCCCGGGGGGAGCTCAGATATCCGATACAGGGATGAAGAAATAACCTCATCCCATTGGTGACGAAAGGTTGTAAGTAGCTGGCCGCCGAGA
TAGCTGAGCGGCGAACCACTAGAAAAGGTTCAGACCCCGGAGCCCAGCCGTCACGATTGTTATGCGTATAAGCCCGGTTCACTACGTCCGTTCTGGCAAG
CCGGGGCTAATCCGTCATTGTCAAGAGACATCTTTCGTCTCATTAGGCTACTAACGCCGCCGGGTCGTTACTCGAAATCGATTTGATCGATCTGCAAGGT
GCTGTCTAGATAGATACCATGGCCCGGAAGTACGGGCTTCTGGCGCATGTCGCACTCGTCCCTGGTCACGAACTGTACAAACATTGGACACTCTTTCCCG
TTCTGGTACAAAATGTGCTCCAATCATGCATGAAACATATACATCGCTTGGGCCACGTAGTCTAGAGCACACTAAATGAGACATCTTAGAGGAGATAGGC
GTAGATCCGGTTACTAGCCGTGATGCAAGGTGGGGGAACGGGATGTTGTAACATGCGGGTGTGCACGCCACTAAGACGAAACCTAGTGCCTCTTGCTAGT
CATTATTAGTACGAAGGGTTGTGCTCCGATAGTTGAAAATGTGGTGTTATGCTCACGGCGTGGTGTGTCTTTAACCCCAAGCTATCAATACTGAATAGGC
TACATATGTTATACTCCGTGTCGTAAGGATGACGGCTCCGCTACTGGTGGTCTGTCGCCTCAGCCGTTGACCGCAACACCGTGAAGCACGGGTAAGGCAG
CAGAAAGGCGAGAACTGCAGGAGAGCGTATTTGCGGAACCCTGAGGGTCTAGAGAGTCCACCTGGGCCTTTACGGAACTATATTGGTTTAATAAAACGGG
```

</details>

<details><summary>First lines of <code>lr.hap.1.clean.fasta</code></summary>

```
>chr1
CAGATTTTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGT
CCCACCTGGTGATCCTATGCTTGTGAGTACCCAGAAAATAGCGACGGACCGCGGTGTTAAGTGTCGAGCT
ACATCACTTCTCATGTAGCCAGAAAGCTGCAACTCATCGACTCTATGTAGTGACCGCGTCGATGTCAAAC
CCCGGGGGGAGCTCAGATATCCGATACAGGGATGAAGAAATAACCTCATCCCATTGGTGACGAAAGGTTG
TAAGTAGCTGGCCGCCGAGATAGCTGAGCGGCGAACCACTAGAAAAGGTTCAGACCCCGGAGCCCAGCCG
TCACGATTGTTATGCGTATAAGCCCGGTTCACTACGTCCGTTCTGGCAAGCCGGGGCTAATCCGTCATTG
TCAAGAGACATCTTTCGTCTCATTAGGCTACTAACGCCGCCGGGTCGTTACTCGAAAAGCAGGTGGAATT
GGTGTATTCAGCTTGCTCGATTTGATCGATCTGCAAGGTGCTGTCTAGATAGATACCATGGCCCGGAAGT
ACGGGCTTCTGGCGCATGTCGCACTCGTCCCTGGTCACGAACTGTACAAACATTGGACACTCTTTCCCGT
TCTGGTACAAAATGTGCTCCAATCATGCATGAAACATATACATCGCTTGGGCCACGTAGTCTAGAGCACA
CTAAATGAGACATCTTAGAGGAGATAGGCGTAGATCCGGTTACTAGCCGTGATGCAAGGTGGGGGAACGG
```

</details>

<details><summary>First lines of <code>lr.hap.1.clean.fasta.fai</code></summary>

```
chr1	40041	6	70	71
chr2	20550	40626	70	71
```

</details>

<details><summary>First lines of <code>lr.hap.1.fasta</code></summary>

```
>chr1
CAGATTTTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGTCCCACCTGGTGATCCTATGCTTGTGAGTAC
CCAGAAAATAGCGACGGACCGCGGTGTTAAGTGTCGAGCTACATCACTTCTCATGTAGCCAGAAAGCTGCAACTCATCGACTCTATGTAGTGACCGCGTC
GATGTCAAACCCCGGGGGGAGCTCAGATATCCGATACAGGGATGAAGAAATAACCTCATCCCATTGGTGACGAAAGGTTGTAAGTAGCTGGCCGCCGAGA
TAGCTGAGCGGCGAACCACTAGAAAAGGTTCAGACCCCGGAGCCCAGCCGTCACGATTGTTATGCGTATAAGCCCGGTTCACTACGTCCGTTCTGGCAAG
CCGGGGCTAATCCGTCATTGTCAAGAGACATCTTTCGTCTCATTAGGCTACTAACGCCGCCGGGTCGTTACTCGAAAAGCAGGTGGAATTGGTGTATTCA
GCTTGCTCGATTTGATCGATCTGCAAGGTGCTGTCTAGATAGATACCATGGCCCGGAAGTACGGGCTTCTGGCGCATGTCGCACTCGTCCCTGGTCACGA
ACTGTACAAACATTGGACACTCTTTCCCGTTCTGGTACAAAATGTGCTCCAATCATGCATGAAACATATACATCGCTTGGGCCACGTAGTCTAGAGCACA
CTAAATGAGACATCTTAGAGGAGATAGGCGTAGATCCGGTTACTAGCCGTGATGCAAGGTGGGGGAACGGGATGTTGTAACATGCGGGTGTGCACGCCAC
TAAGACGAAACCTAGTGCCTCTTGCTAGTCATTATTAGTACGAAGGGTTGTGCTCCGATAGTTGAAAATGTGGTGTTATGCTCACGGCGTGGTGTGTCTT
TAACCCCAAGCTATCAATACTGAATAGGCTACATATGTTATACTCCGTGTCGTAAGGATGACGGCTCCGCTACTGGTGGTCTGTCGCCTCAGCCGTTGAC
CGCAACACCGTGAAGCACGGGTAAGGCAGCAGAAAGGCGAGAACTGCAGGAGAGCGTATTTGCGGAACCCTGAGGGTCTAGAGAGTCCACCTGGGCCTTT
```

</details>

<details><summary>First lines of <code>lr.hap.hetA.bed</code></summary>

```
chr1	1938	chr1	1939	SNP
chr1	2331	chr1	2332	SNP
chr1	4316	chr1	4317	SNP
chr1	7958	chr1	7959	SNP
chr1	10836	chr1	10837	SNP
chr1	10945	chr1	10946	SNP
chr1	11418	chr1	11419	SNP
chr1	11463	chr1	11464	SNP
chr1	15804	chr1	15805	SNP
chr1	16588	chr1	16589	SNP
chr1	22495	chr1	22496	SNP
chr1	24401	chr1	24402	SNP
```

</details>

<details><summary>First lines of <code>lr.hap.hetA.insertions.fa</code></summary>

```
>chr2_9443
TATGCCGGAGCGTACTCAGGGGATAAGGGAGGAGACTGAAC
```

</details>

<details><summary>First lines of <code>lr.hap.hetB.bed</code></summary>

```
chr1	2267	chr1	2268	SNP
chr1	4252	chr1	4253	SNP
chr1	4889	chr1	4890	SNP
chr1	6920	chr1	6921	SNP
chr1	6966	chr1	6967	SNP
chr1	9541	chr1	9542	SNP
chr1	10947	chr1	10948	SNP
chr1	14386	chr1	14387	SNP
chr1	15703	chr1	15704	SNP
chr1	19893	chr1	19894	SNP
chr1	21973	chr1	21974	SNP
chr1	27070	chr1	27071	SNP
```

</details>

<details><summary>First lines of <code>lr.hap.hetB.insertions.fa</code></summary>

```
>chr2_3514
TCGTCAGATCGGA
>chr1_8470
CGACAAGAGCTACGCCATTCCCCTCTTATTCACCCCCTGAACAC
```

</details>

<details><summary>First lines of <code>lr.hap.homAB.bed</code></summary>

```
chr1	165	chr1	166	SNP
chr1	667	chr1	668	SNP
chr1	1065	chr1	1066	SNP
chr1	8684	chr1	8685	SNP
chr1	10174	chr1	10175	SNP
chr1	15962	chr1	15963	SNP
chr1	18084	chr1	18085	SNP
chr1	22083	chr1	22084	SNP
chr1	22627	chr1	22628	SNP
chr1	36896	chr1	36897	SNP
chr1	37589	chr1	37590	SNP
chr1	38759	chr1	38760	SNP
```

</details>

<details><summary>First lines of <code>lr.hap.homAB.insertions.fa</code></summary>

```
>chr1_9258
TCGTAGAGTGCCCACATGACTCGCAACC
```

</details>

<details><summary>First lines of <code>lr.hap.parameter</code></summary>

```
PARAMETER FILE: DO JUST MODIFY THE VALUES AND KEEP THE SPACES!
DUPLICATION_minimum_length: 100
DUPLICATION_maximum_length: 500
DUPLICATION_number: 1
INDEL_minimum_length: 1
INDEL_maximum_length: 50
INDEL_number: 5
TRANSLOCATION_minimum_length: 100
TRANSLOCATION_maximum_length: 500
TRANSLOCATION_number: 1
INVERSION_minimum_length: 100
INVERSION_maximum_length: 500
```

</details>

<details><summary>First lines of <code>lr.hapA.fasta</code></summary>

```
>chr1
CAGATTTTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGTCCCACCTGGTGATCCTATGCTTGTGAGTAC
CCAGAAAATAGCGACGGACCGCGGTGTTAAGTGTCGAGCTACATCACTTCTCATGTAGCCAGAAAGCTGCAACTCATCGACTCTATGTAGTGACCGCGTC
GATGTCAAACCCCGGGGGGAGCTCAGATATCCGATACAGGGATGAAGAAATAACCTCATCCCATTGGTGACGAAAGGTTGTAAGTAGCTGGCCGCCGAGA
TAGCTGAGCGGCGAACCACTAGAAAAGGTTCAGACCCCGGAGCCCAGCCGTCACGATTGTTATGCGTATAAGCCCGGTTCACTACGTCCGTTCTGGCAAG
CCGGGGCTAATCCGTCATTGTCAAGAGACATCTTTCGTCTCATTAGGCTACTAACGCCGCCGGGTCGTTACTCGAAATCGATTTGATCGATCTGCAAGGT
GCTGTCTAGATAGATACCATGGCCCGGAAGTACGGGCTTCTGGCGCATGTCGCACTCGTCCCTGGTCACGAACTGTACAAACATTGGACACTCTTTCCCG
TTCTGGTACAAAATGTGCTCCAATCATGCATGAAACATATACATCGCTTGGGCCACGTAGTCTAGAGCACACTAAATGAGACATCTTAGAGGAGATAGGC
GTAGATCCGGTTACTAGCCGTGATGCAAGGTGGGGGAACGGGATGTTGTAACATGCGGGTGTGCACGCCACTAAGACGAAACCTAGTGCCTCTTGCTAGT
CATTATTAGTACGAAGGGTTGTGCTCCGATAGTTGAAAATGTGGTGTTATGCTCACGGCGTGGTGTGTCTTTAACCCCAAGCTATCAATACTGAATAGGC
TACATATGTTATACTCCGTGTCGTAAGGATGACGGCTCCGCTACTGGTGGTCTGTCGCCTCAGCCGTTGACCGCAACACCGTGAAGCACGGGTAAGGCAG
CAGAAAGGCGAGAACTGCAGGAGAGCGTATTTGCGGAACCCTGAGGGTCTAGAGAGTCCACCTGGGCCTTTACGGAACTATATTGGTTTAATAAAACGGG
```

</details>

<details><summary>First lines of <code>lr.hapB.fasta</code></summary>

```
>chr1
CAGATTTTCATATTATGCAGAAAATCTACTTCGCCTGATACGAGTCGGTTATCTTCGGATACTGTATAGTCCCACCTGGTGATCCTATGCTTGTGAGTAC
CCAGAAAATAGCGACGGACCGCGGTGTTAAGTGTCGAGCTACATCACTTCTCATGTAGCCAGAAAGCTGCAACTCATCGACTCTATGTAGTGACCGCGTC
GATGTCAAACCCCGGGGGGAGCTCAGATATCCGATACAGGGATGAAGAAATAACCTCATCCCATTGGTGACGAAAGGTTGTAAGTAGCTGGCCGCCGAGA
TAGCTGAGCGGCGAACCACTAGAAAAGGTTCAGACCCCGGAGCCCAGCCGTCACGATTGTTATGCGTATAAGCCCGGTTCACTACGTCCGTTCTGGCAAG
CCGGGGCTAATCCGTCATTGTCAAGAGACATCTTTCGTCTCATTAGGCTACTAACGCCGCCGGGTCGTTACTCGAAAAGCAGGTGGAATTGGTGTATTCA
GCTTGCTCGATTTGATCGATCTGCAAGGTGCTGTCTAGATAGATACCATGGCCCGGAAGTACGGGCTTCTGGCGCATGTCGCACTCGTCCCTGGTCACGA
ACTGTACAAACATTGGACACTCTTTCCCGTTCTGGTACAAAATGTGCTCCAATCATGCATGAAACATATACATCGCTTGGGCCACGTAGTCTAGAGCACA
CTAAATGAGACATCTTAGAGGAGATAGGCGTAGATCCGGTTACTAGCCGTGATGCAAGGTGGGGGAACGGGATGTTGTAACATGCGGGTGTGCACGCCAC
TAAGACGAAACCTAGTGCCTCTTGCTAGTCATTATTAGTACGAAGGGTTGTGCTCCGATAGTTGAAAATGTGGTGTTATGCTCACGGCGTGGTGTGTCTT
TAACCCCAAGCTATCAATACTGAATAGGCTACATATGTTATACTCCGTGTCGTAAGGATGACGGCTCCGCTACTGGTGGTCTGTCGCCTCAGCCGTTGAC
CGCAACACCGTGAAGCACGGGTAAGGCAGCAGAAAGGCGAGAACTGCAGGAGAGCGTATTTGCGGAACCCTGAGGGTCTAGAGAGTCCACCTGGGCCTTT
```

</details>

<details><summary>First lines of <code>lr.status</code></summary>

```
Mon Oct 12 06:07:00 2026: lr.status
Mon Oct 12 06:07:00 2026: Variant simulation mode enabled
Mon Oct 12 06:07:00 2026: SURVIVOR start
Mon Oct 12 06:07:00 2026: Running: /opt/conda/share/lrsim/SURVIVOR 0 /work/in/reference.fa lr.hap.parameter 0 lr.hap 1000
Mon Oct 12 06:07:00 2026: SURVIVOR end
Mon Oct 12 06:07:00 2026: Build genome index start
Mon Oct 12 06:07:00 2026: /opt/conda/share/lrsim/faFilter.pl lr.hap.0.fasta 0 > lr.hap.0.clean.fasta
Mon Oct 12 06:07:00 2026: /opt/conda/share/lrsim/faFilter.pl lr.hap.1.fasta 0 > lr.hap.1.clean.fasta
Mon Oct 12 06:07:00 2026: /opt/conda/share/lrsim/samtools faidx lr.hap.0.clean.fasta
Mon Oct 12 06:07:00 2026: /opt/conda/share/lrsim/samtools faidx lr.hap.1.clean.fasta
Mon Oct 12 06:07:00 2026: Build genome index end
Mon Oct 12 06:07:00 2026: DWGSIM round 0 thread 0 start
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-x` | Million read pairs in total (Intermediate files count toward the 500 MB job output limit (about 1.4 GB per million pairs). Too many pairs for a small reference makes LRSim stall until the time limit.) | 0.02 | 0.001 to 0.1 |
| `-f` | Mean molecule length (kbp) | 5 | 1 to 200 |
| `-m` | Average molecules per partition | 5 | 1 to 50 |
| `-t` | Partitions (thousands) | 1 | 1 to 100 |
| `-1` | One SNP per this many bp | 1000 | 10 to 1000000 |
| `-4` | Number of indels | 5 | 0 to 10000 |
| `-7` | Number of duplications and of inversions | 1 | 0 to 100 |
| `-0` | Number of translocations | 1 | 0 to 100 |
| `-i` | Outer distance between read ends | 350 | 100 to 2000 |
| `-s` | Standard deviation of the distance | 35 | 0 to 500 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The reference has 2 contigs (`chr1`, `chr2`) totalling 60,000 bp. The run takes about 15 seconds.

- `lr_S1_L001_R1_001.fastq.gz`, `..._R2_...`, `lr_S1_L002_...`: 4 files, about 10,000 pairs each, 20,011 pairs in total for the 0.02 million requested. Reads are 151 bases. R1 begins with a 16-base barcode whose quality string is `AAAFFFKKKKKKKKKK`. Lane 1 R1 has 571 distinct barcodes.
- `lr.hap.0.fasta`, `lr.hap.1.fasta` and `.clean.fasta` versions: the haplotypes. Clean haplotype 0 is 39,948 bp on `chr1` and 20,578 on `chr2`.
- `lr.hap.hetA.bed`, `hetB.bed`, `homAB.bed`: 29, 23 and 22 variants. By type: 60 SNP (60,000 bp at 1 per 1000), 4 INS, 4 DEL, 1 DUP, 1 INV and 4 TRA entries.
- `lr.0.manifest`, `lr.1.manifest` and their `sort` versions map reads to barcodes.
- `lr.hap.parameter`, `lr.status`: the settings used and a step log.
- `_Inline/`: compiled Perl helper code. `lr.dwgsim.*.fastq` are 10 MB intermediates.

## Your own runs

- **Longer molecules.** Change `-f 5` to `-f 20`. Result: the same 20,000 pairs, but the manifests list 888 and 852 distinct barcodes (haplotypes 0 and 1) against 571 and 582.
- **More variants.** `-1 200 -4 50`. Result: 298 SNPs and 53 insertions plus 28 deletions across the three BED files (60,000 / 200 = 300 SNPs expected).

## Pitfalls

- **Too many pairs for a small genome.** The run can stall for a long time. Keep `-x` low for a reference under 1 Mb.
- **Heavy disk use.** About 1.4 GB per million read pairs, mostly intermediates.
- **Human defaults on a small genome.** 1000 indels, 100 translocations of 1000 to 10000 bp do not fit 60 kb. Set `-4`, `-7`, `-0` and the length options `-5`, `-6`, `-8`, `-9`.
- **`-o` skips parameter checks.** The example uses it. Without it, check that the settings agree with each other.
- **Variant counts differ from the numbers asked for.** The example asked for 5 indels and 1 translocation and the BED files list 8 indels and 4 TRA lines. Count the BED files before you use them as a truth set.

## Further reading

- Source and options: https://github.com/aquaskyline/LRSIM
- Luo R, Sedlazeck FJ, Darby CA, Kelly SM, Schatz MC (2017). LRSim. Comput Struct Biotechnol J 15:478-484. https://doi.org/10.1016/j.csbj.2017.10.002

---

Cite: Luo R, Sedlazeck FJ, Darby CA, Kelly SM, Schatz MC (2017). LRSim, a linked-reads simulator generating insights for better genome partitioning. Comput Struct Biotechnol J 15:478-484. doi:10.1016/j.csbj.2017.10.002

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/lrsim).
