# BBTools randomreads.sh

> Simulate paired Illumina-style or PacBio-style reads from a reference with planted SNPs and indels, using randomreads.sh from the BBTools suite.

Licence: BSD-3-Clause-LBNL · [Source code](https://github.com/bbushnell/BBTools)

## What it simulates

`randomreads.sh` is the read simulator in BBTools, the Java suite from the Joint Genome Institute that also holds BBMap, BBDuk and BBMerge. It draws reads at random positions from a reference FASTA, plants mutations in them, and adds quality scores and substitution errors. Read names record the genomic origin of every read.

The usage text lists what you can set:

- **Layout:** single or paired reads, read length (`length=`, or `minlength` and `maxlength`), insert size range, and a number of reads (`reads=`) or a target coverage (`coverage=`).
- **Mutations:** the chance that a read carries SNPs, insertions, deletions, substitutions or N blocks (`snprate`, `insrate`, `delrate`, `subrate`, `nrate`), with maxima per read and length limits for each type. With a rate X, a read gets at least one mutation with chance X, at least two with chance X squared, and so on.
- **Illumina quality:** `minq`, `midq` and `maxq`, with `qv` to vary quality by tile. Errors are added from the quality values after the mutations.
- **PacBio mode:** `pacbio=t` with an error rate drawn between `pbmin` (0.13) and `pbmax` (0.17).
- **Extras:** `metagenome=t` gives each scaffold a random exponential coverage, `amp=` imitates multiple-displacement amplification, and `addcigar=t` writes a truth CIGAR into the read name.

## When to use it

Use it to make quick test reads with a known origin for BBMap, BBMerge or any mapper, since BBTools can grade mapping accuracy straight from the read names. It is also handy when you already use BBTools and want no extra dependency.

- Use [wgsim](wgsim.md) or [DWGSIM](dwgsim.md) when you need a truth VCF of planted variants. `randomreads.sh` writes mutations into reads but no variant list.
- Use [InSilicoSeq](insilicoseq.md) for metagenomes with an abundance model and trained error profiles.
- Use [pIRS](pirs.md) when you want empirical Illumina quality and indel profiles.

## Install

The BBTools repository reports version 40.05. Bioconda carries `bbmap` 40.05 with `randomreads.sh` among its scripts, for linux-64, linux-aarch64, osx-64 and osx-arm64.

```bash
conda create -n bbtools -c conda-forge -c bioconda bbmap=40.05
conda activate bbtools
randomreads.sh --help
```

The README's other route is to download the archive from SourceForge, unpack it and run the scripts in place. BBTools needs Java 8 or higher (the README recommends Java 25 or later) and bash is recommended.

The licence is a modified BSD from Lawrence Berkeley National Laboratory. It allows use and redistribution if the copyright notice and disclaimer stay, and the README says BBTools is free for unlimited use. GitHub reports it as "NOASSERTION" because it is a custom text.

## A first run

Adapted from the usage text printed by [`randomreads.sh`](https://github.com/bbushnell/BBTools/blob/master/randomreads.sh), whose minimal form is:

```bash
randomreads.sh ref=reference.fa out=reads.fq length=100 reads=10000
```

The recipe makes 5000 read pairs of 100 bp into two files, with a 10% chance of a SNP per read, 2% for an insertion, 2% for a deletion, base quality 20 to 36 and a fixed seed.

## Run the tested example

This recipe builds BBTools randomreads.sh in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.7 s.

1. Download [bbtools-randomreads-recipe.tar.gz](https://biosimhub.pages.dev/guides/bbtools-randomreads/bbtools-randomreads-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bbtools-randomreads-recipe.tar.gz
   cd bbtools-randomreads
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/bbtools-randomreads:40.05 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bbtools-randomreads:40.05 randomreads.sh -Xmx700m ref=/work/in/reference.fa out1=reads_R1.fq out2=reads_R2.fq reads=5000 length=100 paired=t snprate=0.1 insrate=0.02 delrate=0.02 minq=20 maxq=36 midq=28 simplenames=t seed=42 overwrite=t > out/randomreads_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `randomreads_log.txt` | 0 B |
| `reads_R1.fq` | 1.6 MB |
| `reads_R2.fq` | 1.6 MB |
| `ref/genome/1/chr1.chrom.gz` | 5.9 KB |
| `ref/genome/1/info.txt` | 173 B |
| `ref/genome/1/scaffolds.txt.gz` | 223 B |
| `ref/genome/1/summary.txt` | 218 B |

<details><summary>First lines of <code>reads_R1.fq</code></summary>

```
@SYN_0_1710_1809_174_+_9710_1_._chr{example$random$20$kb$sequence&0_1784_1883_174_-_9784_1_._chr{example$random$20$kb$sequence 1:
AGGGTCAGCCGTGATTCCGATTCGATTAGACTGGTCCCCACGGGTCCATGAGTACGAGGAAACTCGGTATCGAGCCTAAAAGTTATAAGGCATCTCGCCC
+
8?;B=>9@C@G?A=GD?>B@EFABA<<<FFH@B9?<;DDB@D@8>:=;@BE8BBE>A=C=@8B@@A@8<=:>;A9B<=ACA?;=8G8=>8D8:8A8@9@8
@SYN_1_18918_19093_225_+_26918_1_._chr{example$random$20$kb$sequence&1_19119_19218_225_-_27119_1_._chr{example$random$20$kb$sequence 1:
GATTATGTCCTTCCGTTTCACACCTCCATACCAATGTGGCAAGTCGACACTTAATCGGCCCTTTTGACTAGAGCTTCTTCAGTTGCAGTGCACGACAACT
+
6:778:=<=A=>CF?D@E?E9@B>A@=ECA@::DA?>D??<=?9<=;>B7?DB??A?@:7=B@>>@B@?A?6>9@>8:<66>::<C?F>6?>=:=?6:6<
@SYN_2_6019_6118_167_+_14019_1_._chr{example$random$20$kb$sequence&2_6086_6185_167_-_14086_1_._chr{example$random$20$kb$sequence 1:
CACTAATAATTATCCATCGGTTTAAGATCCGAAAATTTGATGATGTATTATATATTAATGATGATCGTTAGAGGCTATTCTGAGACGACACGCTCGCACT
+
?>AAACCCECEDGGDEFCBDBGEDFBDDDGEFEA@DEECEDGD;?BGCFFD>@AFDDB?DBAAFA<E?>DACCACA<?CBC=DE@BAA?@><<>>;79<7
```

</details>

<details><summary>First lines of <code>reads_R2.fq</code></summary>

```
@SYN_0_1710_1809_174_+_9710_1_._chr{example$random$20$kb$sequence&0_1784_1883_174_-_9784_1_._chr{example$random$20$kb$sequence 2:
CTACGCCCTGGAACGAGAGTGCGCTAGCCATTATAGCTGGTGATGGAGAACTACCCATACGTCGTTACTTTCCTGGGCGAGATGCCTTATAACTTTTAGG
+
666<677>6A<>=6969@>;<:6<AB8AB=6;6B;6;<7<A;<>;;<D6>>?6=:?;=@9;BA;>666>DA6DB@7@?D<9;>>>@?=:<@:D8>8:96:
@SYN_1_18918_19093_225_+_26918_1_._chr{example$random$20$kb$sequence&1_19119_19218_225_-_27119_1_._chr{example$random$20$kb$sequence 2:
TAGGGACGGAACTGCCTCTATCTAGTGACGATAAGGGAGAGGTATGAGTAGTATACTCACTCGACTGGCTCGCCCCGGCATGGGACACTCAAGACCACTG
+
755:=58B=A8>AE>5A??<958:;D5=:<@5A8;7BC>:6:;<6?9??@<;:8;7@@5?>=>78><AC7>>@=<C?><>8A?>E:A;;>>?>:<@<:;5
@SYN_2_6019_6118_167_+_14019_1_._chr{example$random$20$kb$sequence&2_6086_6185_167_-_14086_1_._chr{example$random$20$kb$sequence 2:
TTAGACTCCTCGTTGGCGGCCAGACGGCAGTCTTGCGGTAGATTCGAGTCCTATGTTACTCCGAGCAAGTGCGAGCGTGTCGTCTCAGAATAGCCTCTAA
+
18;9391;;=74@A>:7=;>@8<::6;:86;;9>?<<<;9:>>=?:9?<7>4A=??=9>==<=??>?=;=>A;>=?>?=>A=4A?=@2@@=??;<>:=97
```

</details>

<details><summary>First lines of <code>ref/genome/1/info.txt</code></summary>

```
#Chromosome sizes
#Generated on	Sun Oct 18 04:18:33 UTC 2026
#Version	5
#chrom	scaffolds	contigs	length	defined	undefined	startPad	stopPad
1	1	1	36001	20000	16001	8000	8000
```

</details>

<details><summary>First lines of <code>ref/genome/1/summary.txt</code></summary>

```
#Summary
#Generated on	Sun Oct 18 04:18:33 UTC 2026
#Version	5
chroms	1
bases	36001
defined	20000
undefined	16001
contigs	1
scaffolds	1
interpad	500
source	/work/in/reference.fa
bytes	20321
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `reads=…` | Read pairs | 5000 | 1 to 500000 |
| `length=…` | Read length | 100 | 30 to 300 |
| `snprate=…` | Probability a read gets a SNP | 0.1 | 0 to 1 |
| `insrate=…` | Probability a read gets an insertion | 0.02 | 0 to 1 |
| `delrate=…` | Probability a read gets a deletion | 0.02 | 0 to 1 |
| `minq=…` | Minimum base quality | 20 | 2 to 40 |
| `midq=…` | Average base quality | 28 | 2 to 40 |
| `maxq=…` | Maximum base quality | 36 | 2 to 40 |
| `seed=…` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `reads_R1.fq` and `reads_R2.fq` hold the two ends in matching order. Quality letters follow the `minq`, `midq` and `maxq` range you set. With `simplenames=t` each header names the contig and position the read came from.
- A BBMap-style index (a `ref/` folder) is built in the working directory from `ref=`, as the usage text describes for `build=` and `midpad=`. It is not a result.
- `randomreads_log.txt` may be empty. The script echoes its Java command and prints progress to standard error, and the recipe saves only standard output.

Two checks on a run. Count the read pairs, which should equal `reads=`. Then map the reads back to the reference with any aligner: reads with planted mutations should show mismatches or gaps, and the share should track `snprate`, `insrate` and `delrate`.

## Pitfalls

- **Rates are per read.** `snprate=0.1` means a read has a 10% chance of at least one SNP, not a 10% base mutation rate. A read can carry up to `maxsnps=3` SNPs by default.
- **Mutations are not recorded as variants.** There is no VCF. Truth lives in the read names, and `addcigar=t` adds a truth CIGAR.
- **Insert size defaults depend on read length.** Set `mininsert` and `maxinsert` for a specific library. The insert distribution is Gaussian by default, with a standard deviation of one sixth of the range.
- **Keep `midq` between `minq` and `maxq`.** The usage text defines midq as the approximate average.
- **An index is built next to the output.** The script passes `build=1`. Several runs in one folder with different references need different `build=` values, or separate folders.
- **Memory is detected automatically.** In a container, set `-Xmx` yourself, as the recipe does with `-Xmx700m`.
- **Seed.** The usage text lists `seed=0` as the default and `-1` for a random seed. The recipe passes a fixed positive seed.

## Further reading

- Usage text of the script: https://github.com/bbushnell/BBTools/blob/master/randomreads.sh
- BBTools README: https://github.com/bbushnell/BBTools
- Citation page: https://github.com/bbushnell/BBTools/blob/master/docs/citation.txt
- Project site: https://bbmap.org

---

Cite: Bushnell B. BBTools. https://sourceforge.net/projects/bbmap/ (citation format given in docs/citation.txt of the repository).

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bbtools-randomreads).
