# gargammel

> Simulate ancient DNA sequencing reads (short fragments with deamination damage and Illumina errors) from a reference FASTA.

Licence: GPL-3.0-only · [Source code](https://github.com/grenaud/gargammel)

## What it simulates

gargammel simulates sequencing reads from ancient DNA. It draws short fragments from a genome, damages them with the Briggs deamination model, adds sequencing adapters and passes the result to the ART Illumina simulator for errors and quality scores.

The inputs are a reference FASTA and the damage and fragment settings. The outputs are paired FASTQ files and a FASTA of the undamaged fragments, which gives the truth for every read.

Key assumptions:

- Ancient fragments are short, and reads longer than the fragment run into the adapter.
- Cytosines deaminate to uracil far more often in single-stranded overhangs at fragment ends than in the double-stranded middle. A deaminated C reads as T.
- The Briggs model has four parameters, written `v,l,d,s`: the probability that a molecule has a nick, the geometric parameter for the overhang length, the deamination rate in double-stranded regions and the deamination rate in single-stranded regions.
- A double-stranded library shows C to T at the 5' end and G to A at the 3' end.

## When to use it

Use gargammel to test ancient DNA tools. Typical questions:

- Does my damage-aware mapper keep reads with 20% C to T at the first base?
- Does adapter trimming cope with 60 bp fragments and 75 bp reads?
- Does a damage estimator such as mapDamage recover the settings I put in?

[wgsim](wgsim.md), [DWGSIM](dwgsim.md) and [pIRS](pirs.md) on biosimhub give modern-DNA reads with no fragmentation or damage. [InSilicoSeq](insilicoseq.md) fits better when the sample is a mix of genomes. gargammel itself can also mix endogenous, present-day human and microbial sources. The biosimhub example uses one source only.

## Install it yourself

The Bioconda package is `gargammel` 1.1.4. The conda package gives the four programs and the `gargammel` wrapper.

```bash
conda create -n gargammel -c conda-forge -c bioconda gargammel=1.1.4 samtools
conda activate gargammel
```

The wrapper expects a directory with `endo/`, `cont/` and `bact/` subfolders. The recipe skips it, because in the recipe's image the wrapper stopped on a parse error at the end of the file and dropped the last record. The recipe chains the four programs instead, and you can do the same:

```bash
samtools faidx ref.fa
fragSim -n 2002 -l 60 -m 0 -M 1000 ref.fa > frag.fa
deamSim -damage 0.03,0.4,0.01,0.3 frag.fa > deam.fa
adptSim -l 75 -artp adpt.fa deam.fa
art_illumina -ss HS25 -amp -na -p -i adpt.fa -l 75 -c 1 -o sim_
```

- `fragSim -l 60` makes fragments of fixed length 60. `-f` takes a table of lengths and frequencies. The `gargammel` wrapper also takes `--loc` and `--scale` for a log-normal length.
- `deamSim -damage v,l,d,s` takes the four Briggs values.
- `adptSim -l 75` adds adapters and splits each fragment into two 75 bp reads.
- `art_illumina -ss HS25` adds errors and quality with the HiSeq 2500 profile.

## Run the tested example

This recipe builds gargammel in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.6 s.

1. Download [gargammel-recipe.tar.gz](https://biosimhub.pages.dev/guides/gargammel/gargammel-recipe.tar.gz) (Dockerfile, run_gargammel.py, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf gargammel-recipe.tar.gz
   cd gargammel
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/gargammel:1.1.4 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/gargammel:1.1.4 python /opt/run_gargammel.py --reference /work/in/reference.fa \
    --n 2000 --length 60 --readlen 75 --nick 0.03 \
    --overhang 0.4 --dsdeam 0.01 --ssdeam 0.3 \
    --platform HS25 > out/gargammel_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `fragments.fa` | 181.5 KB |
| `gargammel_log.txt` | 1.2 KB |
| `sim_1.fq` | 370.8 KB |
| `sim_2.fq` | 370.8 KB |

<details><summary>First lines of <code>fragments.fa</code></summary>

```
>synthetic_ref:-:14254:14314:60e
GGCTCGTTGTGGGATTGCCGGTCGGGGCCTCCCGCTAAGGAGCACCTAGTTTTGAGGTAT
>synthetic_ref:-:5284:5344:60e
CGCTAGTACCGCATACCTCTCCAGGCTCACCAGCACTACCAGACATCCTGAATGCGCCGC
>synthetic_ref:+:1439:1499:60e
GGTTAAATTGGACGTCTTCCCACTCCGTTGCTGCGTGTCTAGGCGGTTTAGCGTAAGCGA
>synthetic_ref:+:19018:19078:60e
CAATCGTGTATCAGTAACTGAATCGCTAATTAGATCTTGGTGCAAAGAGCTTCTTCAGTT
>synthetic_ref:+:19327:19387:60e
ACGATCTCTATTCATTCACCAACAGCAGTCCCGAAGCCCAAACTCAATATTCGGTTTTGG
>synthetic_ref:-:9523:9583:60e
CCGGTGGAAACATTACTCGGCAGTCCACTCTTCGACTTAGAGTCGCCCTGCGCATATAAA
```

</details>

<details><summary>First lines of <code>gargammel_log.txt</code></summary>

```
samtools faidx /tmp/garg/ref.fa
fragSim -tag e -n 2002 -m 0 -M 1000 -l 60 /tmp/garg/ref.fa
deamSim -damage 0.03,0.4,0.01,0.3 /tmp/garg/frag.fa
adptSim -f AGATCGGAAGAGCACACGTCTGAACTCCAGTCACCGATTCGATCTCGTATGCCGTCTTCTGCTTG -s AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATTT -l 75 -artp /tmp/garg/adpt.fa /tmp/garg/deam.fa
art_illumina -ss HS25 -amp -na -p -i /tmp/garg/adpt.fa -l 75 -c 1 -o /work/out/sim_

    ====================ART====================
             ART_Illumina (2008-2016)          
          Q Version 2.5.8 (June 6, 2016)       
     Contact: Weichun Huang <whduke@gmail.com> 
    -------------------------------------------

```

</details>

<details><summary>First lines of <code>sim_1.fq</code></summary>

```
@synthetic_ref:-:14254:14314:60e-2/1
GGCTCGTTGTGGGATTGCCGGTCGGGGCCTCCCGCTAAGGAGCACCTAGTTTTGAGGTATAGATCGGAAGAGCAC
+
CCCCAGGGEGG1GGGGGFGG@CGGGGGGGGGGGGGGGGFGGGGGGGGGGCGGFGGGGG1GFGGGEGGGG@GGGG1
@synthetic_ref:-:5284:5344:60e-2/1
CGCTAGTACCGCATACCTCTCCAGGCTCACCAGCACTACCAGACATCCTGAATGCGCCACAGATCGGAAGAGCAC
+
BBCCCGGGGGGGGGGGG1GFG1FFGGGGGGGGGGGBGGGGGGGGGGGGGGDFGGGGGE1<G0GGGGG/DGGGGGG
@synthetic_ref:+:1439:1499:60e-2/1
GGTTAAATTGGACGTCTTCCCACTCCGTTGCTGCGTGTCTAGGCGGTTTAGCGTAAGCGAAGATCGGAAGAGCAC
+
<CCCCGGGGGGGGGGGGGGGGGGGGGGGG1GGGGGGGGGGGGGGGGGG:FGGGGGGCGGG/GGGGGGGGGGGGEG
```

</details>

<details><summary>First lines of <code>sim_2.fq</code></summary>

```
@synthetic_ref:-:14254:14314:60e-2/2
ATACCTCAAAACTAGGTGCTCCTTAGCGGGAGGCCCCGACCGGCAATCCCACAACGAGCCAGATCGGAAGAGCGT
+
C@CBCGGGGFGGGGGGGGGGG>GGGGD/GG1GGGGGGG:G1GGG/GDGGGGFGGGCEGDGGFGGGGGFGGGGGEG
@synthetic_ref:-:5284:5344:60e-2/2
GTGGCGCATTCAGGATGTCTGGTAGTGCTGGTGAGCCTGGAGAGGTATGCGGTACTAGCGAGATCGGAAGAGCGT
+
:CC0BGDGGGGGGGGGGGGG<FG<GBGGGGGGCGGGGGGEEGG1GGGGGGCG/GGGGGG0CGGFGGG0CGEG1GG
@synthetic_ref:+:1439:1499:60e-2/2
TCGCTTACGCTAAACCGCCTAGACACGCAGCAACGGAGTGGGAAGACGTCCAATTTAACCAGATCGGAAGAGCGT
+
CCCCCGGFGGGGGGGGG=F;GGGGGGG@GGGGGGGGGGGGGGGGGGGGGG:GGGGGGGGGGGCGGGDGGGFGGGG
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--n` | Number of fragments | 2000 | 1 to 500000 |
| `--length` | Fragment length (bp) | 60 | 20 to 300 |
| `--readlen` | Read length | 75 | 20 to 250 |
| `--platform` | Illumina platform | HS25 | GA2, HS20, HS25, HSXt, MSv1, MSv3 |
| `--nick` | Nick frequency (Briggs v) | 0.03 | 0 to 1 |
| `--overhang` | Overhang geometric parameter (Briggs l) | 0.4 | 0.01 to 1 |
| `--dsdeam` | Deamination in double-stranded parts (Briggs d) | 0.01 | 0 to 1 |
| `--ssdeam` | Deamination in single-stranded parts (Briggs s) | 0.3 | 0 to 1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper script `run_gargammel.py` wraps these four calls. It asks `fragSim` for two more fragments than you request (2,002 for 2,000), because the last records are dropped. It ignores the exit status of `deamSim` and `adptSim`, which complain about the end of the file. It then copies the fragment FASTA to the output. The log lists the exact commands, so you can rerun them by hand.

`fragments.fa` has 2,002 records of 60 bp and is 185,879 bytes. A name such as `synthetic_ref:-:14254:14314:60e` gives the reference, strand, start and end, then the tag `e` for the endogenous source. The sequences are undamaged.

`sim_1.fq` and `sim_2.fq` hold 2,000 read pairs each and are 379,695 bytes. Reads are 75 bp, but the fragment is 60 bp, so the last 15 bases of read 1 are adapter. The first read in the example ends with `AGATCGGAAGAGCAC`, and read 2 ends with `AGATCGGAAGAGCGT`. Trim the adapters before you map.

`gargammel_log.txt` (1,222 bytes) lists the four commands and the ART banner. It reports ART with the HiSeq 2500 profile, "Amplicon paired-end sequencing simulation" and 75 as the read length.

Comparing each read with its fragment shows the damage. The numbers below come from a fresh run of the example settings. The run is not seeded, so yours will differ slightly. C to T at read 1 position 1 was 20.4%, then 10.6%, 7.0%, 6.5%, 3.3% and 2.3% at positions 2 to 6. The middle of the fragment was 0.4%. G to A at the last six fragment positions rose from 2.6% to 16.7%, against 0.8% in the middle. The overall mismatch rate of the first 60 bases was 0.75%.

## Your own runs

These runs used the recipe's image and reference.

**Published Neandertal parameters.** Set nick 0.024, overhang 0.36, double-stranded deamination 0.0097 and single-stranded deamination 0.68, the maximum likelihood estimates of Briggs et al. C to T at the first base becomes 47.6%, then 29.2%, 20.2%, 12.4%, 9.2% and 7.1%. The overall mismatch rises to 1.39%.

**No damage.** Set double-stranded and single-stranded deamination to 0. C to T at the first base falls to 0.0%, and the overall mismatch rate falls to 0.12%. That remainder is the ART sequencing error.

**Shorter fragments.** Set the fragment length to 40 and keep the read length at 75. `fragments.fa` shrinks to 145,982 bytes, and 35 bases of every read are adapter. The FASTQ files stay near 380 kB, because the reads keep their 75 bp length.

**A reproducible run.** The recipe's helper script does not pass seeds, so two runs give different files. Running the four programs by hand with `--seed 1` for `fragSim`, `--seed 2` for `deamSim` and `-rs 4` for `art_illumina` gave the same MD5 twice (`cee158ac8465378e3e1a3039a092446d` for read 1). `adptSim` in 1.1.4 rejects `--seed` and was deterministic here without it.

## Pitfalls

- Version 1.1.4 doubles the terminal damage. The current README says versions before 1.1.5 put C to T at about 44% at the first base for the Neandertal parameters, against the 21% of Briggs et al. This run gave 47.6%. Use a newer release for realistic rates.
- The order is `v,l,d,s`: nick, overhang, double-stranded, single-stranded. Swapping `d` and `s` puts the high rate in the double-stranded middle of the fragment.
- A fixed fragment length is unrealistic. Real ancient fragments have a skewed length distribution, so give `fragSim` a frequency file when it matters.
- The reads carry adapters when the fragment is shorter than the read. Trim them, or set the read length at or below the fragment length.
- The recipe's helper script is not seeded. Chain the programs by hand with seeds when you need an exact repeat.
- In the wrapper, `--comp 0,0.08,0.92` means 8% present-day human contamination, so the order is bacterial, contaminant and endogenous.

## Further reading

- gargammel repository and README, including the Briggs model section: https://github.com/grenaud/gargammel
- Renaud G et al. (2017). gargammel, a sequence simulator for ancient DNA. Bioinformatics 33:577-579. https://doi.org/10.1093/bioinformatics/btw670
- Briggs AW et al. (2007). Patterns of damage in genomic DNA sequences from a Neandertal. PNAS 104:14616-14621. https://doi.org/10.1073/pnas.0704665104

---

Cite: Renaud G, Hanghoj K, Willerslev E, Orlando L (2017). gargammel, a sequence simulator for ancient DNA. Bioinformatics 33:577-579. doi:10.1093/bioinformatics/btw670

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/gargammel).
