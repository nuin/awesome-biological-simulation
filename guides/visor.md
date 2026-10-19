# VISOR

> Insert haplotype-specific structural variants (deletions, inversions, duplications and more) into a reference, then simulate paired-end short reads from both haplotypes.

Licence: LGPL-3.0-only · [Source code](https://github.com/davidebolo1993/VISOR)

## What it simulates

VISOR (the VarIant SimulatOR) inserts structural variants and small variants into a reference genome, one haplotype at a time, and then simulates sequencing reads from the altered haplotypes. It supports short reads (Illumina-like, paired-end), long reads (Oxford Nanopore and PacBio-like), bulk and Strand-seq data, and 10x Genomics linked reads (beta).

It works in modules. HACk, the haplotype creator, takes a reference FASTA and one BED file of variants per haplotype and writes a FASTA per haplotype. SHORtS simulates short reads from those haplotypes. LASeR simulates long reads. XENIA simulates linked reads. The reads are aligned and returned as a sorted BAM.

The variant types in the HACk BED include deletion, inversion, tandem duplication, inverted tandem duplication, insertion, tandem repeat expansion and contraction, new perfect or approximate tandem repeats, cut-paste and copy-paste translocations, reciprocal translocation, SNP and MNP. SHORtS and LASeR can also mimic tumour purity, subclones and aneuploidy, and a per-region capture bias for exome or panel data.

Key assumptions: you decide where every variant goes, there is no population-genetic or mutation-process model, and reads come from the haplotype FASTA files you built.

## When to use it

Use VISOR to build a truth set of structural variants in known positions and to test an SV caller on short or long reads.

- Use [SimuG](simug.md) when you want random SNPs, indels and SVs at set rates instead of a list.
- Use [NEAT](neat.md) for small variants with learned error models and a golden VCF.
- Use [LRSim](lrsim.md) for 10x-style linked reads from two random haplotypes.

## Install

VISOR is LGPL-3.0 licensed. The current GitHub release is v1.1.2.1 (November 2023). Bioconda has the same version as a noarch package, but one of its dependencies, `pywgsim`, is built only for linux-64 and osx-64:

```bash
conda create -n visor -c conda-forge -c bioconda visor=1.1.2.1
conda activate visor
VISOR --help
```

The documentation (https://davidebolo1993.github.io/visordoc/installation/installation.html) also covers an install from source with Python 3.8, a cloned repository, `pip install -r requirements.txt` and `python setup.py install`. Since v1.1 it needs `bedtools`, `minimap2` and `samtools` on the PATH, with `samtools` and `htslib` at 1.9 or later and `minimap2` at 2.17 or later. A Docker image, `davidebolo1993/visor`, exists.

## A first run

Adapted from the Use cases page (https://davidebolo1993.github.io/visordoc/usecases/usecases.html). The commands have not been run for this guide. Write a HACk BED with three variants, then build the haplotype and simulate reads:

```bash
echo -e "chr22\t15000000\t16000000\tdeletion\tNone\t0\nchr22\t20000000\t21000000\tinversion\tNone\t0\nchr22\t30000000\t31000000\ttandem duplication\t2\t0" > HACk.h1.bed
VISOR HACk -g chr22.fa -b HACk.h1.bed -o hack.1.out

cut -f1,2 hack.1.out/*.fai > haplochroms.dim.tsv
awk 'OFS=FS="\t"''{print $1, "1", $2, "100.0", "100.0"}' haplochroms.dim.tsv > shorts.laser.simple.bed
VISOR SHORtS -g chr22.fa -s hack.1.out -b shorts.laser.simple.bed -o shorts.1.out --threads 7 --coverage 5
```

The recipe below uses a two-contig 100 kb random reference that was written for it, one BED per haplotype, and a script that builds the SHORtS region file. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds VISOR in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 8.9 s. VISOR has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [visor-recipe.tar.gz](https://biosimhub.pages.dev/guides/visor/visor-recipe.tar.gz) (Dockerfile, run_visor.py, example reference.fa, haplotype1.bed, haplotype2.bed, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf visor-recipe.tar.gz
   cd visor
   sh run.sh
   ```

![Terminal recording of the VISOR example run](https://biosimhub.pages.dev/media/visor/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/visor:1.1.2.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/visor:1.1.2.1 python /opt/run_visor.py --reference /work/in/reference.fa \
    --hap1 /work/in/haplotype1.bed --hap2 /work/in/haplotype2.bed \
    --coverage 4 --read-length 100 --error 0.01 > out/visor_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `hack/h1.fa` | 98.3 KB |
| `hack/h1.fa.fai` | 42 B |
| `hack/h2.fa` | 100.3 KB |
| `hack/h2.fa.fai` | 42 B |
| `haplotype1.fa` | 98.3 KB |
| `haplotype2.fa` | 100.3 KB |
| `reads.bam` | 213.2 KB |
| `reads.bam.bai` | 216 B |
| `reference.fa` | 99.3 KB |
| `reference.fa.fai` | 42 B |
| `regions.bed` | 50 B |
| `shorts/sim.srt.bam` | 213.2 KB |
| `shorts/sim.srt.bam.bai` | 216 B |
| `summary.txt` | 57 B |
| `visor_log.txt` | 4.2 KB |

<details><summary>First lines of <code>hack/h1.fa</code></summary>

```
>chr1
AAGAAATACAAGGCGGGCGGGACACCGGGGTATATTAATGTCAGCACCGACGTCATATAG
GATACTTTGCTATGAGACGCGTTCCTAGATCGCCGAGTTTTGTATTAGACAGGTTCAGGC
ATACGGGACACAAAATACCGGGCAATGCTAATTGCAGTATCTGATCAGAGTATCGCAAGT
CAGTTAGGAGGAGTATTTCGATCTTCAAAGCCCGTTTACGATCAGCTAGCAATGGTAGTT
TACCTAGGGGTTCAACCAAAGGAGATTCGTACATGTCACCCCCTATTTAGCGAACTTACT
TAATATTACAGTGGTTTAATACCACTCTCAGGGACACGTGTGTTTGAACCCCACGAGGGC
ACATCACGCTTTCTAGACTAGCCCAGCTTTCACTTCGTGAGAGTGATCGTTCATTTATTT
AACAACGAGATAGCTTAATAAAACCGCTATAAAAAGGGACAGTGATCCAGGAAGTAAGTG
TCGCCCGGGGATCTGTTTCCTAAACACAGTATTGGGGAGTTGTTAACGGTACTACGATTG
TTACACTCAATTGCACGTGACATTCACAGTCCACCGCTACATGCTAGCGACTTAACCGAT
TATGGTTTTCAGCACTGCAACTAAGATTCCGCACAATCTACGGCGTTTCACCACTGTCGT
```

</details>

<details><summary>First lines of <code>hack/h1.fa.fai</code></summary>

```
chr1	57999	6	60	61
chr2	41001	58978	60	61
```

</details>

<details><summary>First lines of <code>hack/h2.fa</code></summary>

```
>chr1
AAGAAATACAAGGCGGGCGGGACACCGGGGTATATTAATGTCAGCACCGACGTCATATAG
GATACTTTGCTATGAGACGCGTTCCTAGATCGCCGAGTTTTGTATTAGACAGGTTCAGGC
ATACGGGACACAAAATACCGGGCAATGCTAATTGCAGTATCTGATCAGAGTATCGCAAGT
CAGTTAGGAGGAGTATTTCGATCTTCAAAGCCCGTTTACGATCAGCTAGCAATGGTAGTT
TACCTAGGGGTTCAACCAAAGGAGATTCGTACATGTCACCCCCTATTTAGCGAACTTACT
TAATATTACAGTGGTTTAATACCACTCTCAGGGACACGTGTGTTTGAACCCCACGAGGGC
ACATCACGCTTTCTAGACTAGCCCAGCTTTCACTTCGTGAGAGTGATCGTTCATTTATTT
AACAACGAGATAGCTTAATAAAACCGCTATAAAAAGGGACAGTGATCCAGGAAGTAAGTG
TCGCCCGGGGATCTGTTTCCTAAACACAGTATTGGGGAGTTGTTAACGGTACTACGATTG
TTACACTCAATTGCACGTGACATTCACAGTCCACCGCTACATGCTAGCGACTTAACCGAT
TATGGTTTTCAGCACTGCAACTAAGATTCCGCACAATCTACGGCGTTTCACCACTGTCGT
```

</details>

<details><summary>First lines of <code>hack/h2.fa.fai</code></summary>

```
chr1	63002	6	60	61
chr2	37999	64065	60	61
```

</details>

<details><summary>First lines of <code>haplotype1.fa</code></summary>

```
>chr1
AAGAAATACAAGGCGGGCGGGACACCGGGGTATATTAATGTCAGCACCGACGTCATATAG
GATACTTTGCTATGAGACGCGTTCCTAGATCGCCGAGTTTTGTATTAGACAGGTTCAGGC
ATACGGGACACAAAATACCGGGCAATGCTAATTGCAGTATCTGATCAGAGTATCGCAAGT
CAGTTAGGAGGAGTATTTCGATCTTCAAAGCCCGTTTACGATCAGCTAGCAATGGTAGTT
TACCTAGGGGTTCAACCAAAGGAGATTCGTACATGTCACCCCCTATTTAGCGAACTTACT
TAATATTACAGTGGTTTAATACCACTCTCAGGGACACGTGTGTTTGAACCCCACGAGGGC
ACATCACGCTTTCTAGACTAGCCCAGCTTTCACTTCGTGAGAGTGATCGTTCATTTATTT
AACAACGAGATAGCTTAATAAAACCGCTATAAAAAGGGACAGTGATCCAGGAAGTAAGTG
TCGCCCGGGGATCTGTTTCCTAAACACAGTATTGGGGAGTTGTTAACGGTACTACGATTG
TTACACTCAATTGCACGTGACATTCACAGTCCACCGCTACATGCTAGCGACTTAACCGAT
TATGGTTTTCAGCACTGCAACTAAGATTCCGCACAATCTACGGCGTTTCACCACTGTCGT
```

</details>

<details><summary>First lines of <code>haplotype2.fa</code></summary>

```
>chr1
AAGAAATACAAGGCGGGCGGGACACCGGGGTATATTAATGTCAGCACCGACGTCATATAG
GATACTTTGCTATGAGACGCGTTCCTAGATCGCCGAGTTTTGTATTAGACAGGTTCAGGC
ATACGGGACACAAAATACCGGGCAATGCTAATTGCAGTATCTGATCAGAGTATCGCAAGT
CAGTTAGGAGGAGTATTTCGATCTTCAAAGCCCGTTTACGATCAGCTAGCAATGGTAGTT
TACCTAGGGGTTCAACCAAAGGAGATTCGTACATGTCACCCCCTATTTAGCGAACTTACT
TAATATTACAGTGGTTTAATACCACTCTCAGGGACACGTGTGTTTGAACCCCACGAGGGC
ACATCACGCTTTCTAGACTAGCCCAGCTTTCACTTCGTGAGAGTGATCGTTCATTTATTT
AACAACGAGATAGCTTAATAAAACCGCTATAAAAAGGGACAGTGATCCAGGAAGTAAGTG
TCGCCCGGGGATCTGTTTCCTAAACACAGTATTGGGGAGTTGTTAACGGTACTACGATTG
TTACACTCAATTGCACGTGACATTCACAGTCCACCGCTACATGCTAGCGACTTAACCGAT
TATGGTTTTCAGCACTGCAACTAAGATTCCGCACAATCTACGGCGTTTCACCACTGTCGT
```

</details>

<details><summary>First lines of <code>reference.fa</code></summary>

```
>chr1
AAGAAATACAAGGCGGGCGGGACACCGGGGTATATTAATGTCAGCACCGACGTCATATAG
GATACTTTGCTATGAGACGCGTTCCTAGATCGCCGAGTTTTGTATTAGACAGGTTCAGGC
ATACGGGACACAAAATACCGGGCAATGCTAATTGCAGTATCTGATCAGAGTATCGCAAGT
CAGTTAGGAGGAGTATTTCGATCTTCAAAGCCCGTTTACGATCAGCTAGCAATGGTAGTT
TACCTAGGGGTTCAACCAAAGGAGATTCGTACATGTCACCCCCTATTTAGCGAACTTACT
TAATATTACAGTGGTTTAATACCACTCTCAGGGACACGTGTGTTTGAACCCCACGAGGGC
ACATCACGCTTTCTAGACTAGCCCAGCTTTCACTTCGTGAGAGTGATCGTTCATTTATTT
AACAACGAGATAGCTTAATAAAACCGCTATAAAAAGGGACAGTGATCCAGGAAGTAAGTG
TCGCCCGGGGATCTGTTTCCTAAACACAGTATTGGGGAGTTGTTAACGGTACTACGATTG
TTACACTCAATTGCACGTGACATTCACAGTCCACCGCTACATGCTAGCGACTTAACCGAT
TATGGTTTTCAGCACTGCAACTAAGATTCCGCACAATCTACGGCGTTTCACCACTGTCGT
```

</details>

<details><summary>First lines of <code>reference.fa.fai</code></summary>

```
chr1	60000	6	60	61
chr2	40000	61012	60	61
```

</details>

<details><summary>First lines of <code>regions.bed</code></summary>

```
chr1	1	63002	100.0	100.0
chr2	1	41001	100.0	100.0
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
contig_lengths_max_over_haplotypes
chr1	63002
chr2	41001
```

</details>

<details><summary>First lines of <code>visor_log.txt</code></summary>

```
+ VISOR HACk -g reference.fa -b /work/in/haplotype1.bed /work/in/haplotype2.bed -o hack


	 ___      ___ ___  ________  ________  ________     
	|\  \    /  /|\  \|\   ____\|\   __  \|\   __  \    
	\ \  \  /  / | \  \ \  \___|\ \  \|\  \ \  \|\  \   
	 \ \  \/  / / \ \  \ \_____  \ \  \\\  \ \   _  _\  
	  \ \    / /   \ \  \|____|\  \ \  \\\  \ \  \\  \| 
	   \ \__/ /     \ \__\____\_\  \ \_______\ \__\\ _\ 
	    \|__|/       \|__|\_________\|_______|\|__|\|__| v1.1.2
	                     \|_________|                   
                                                    	                                                                        
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--coverage` | Mean coverage | 4 | 0.5 to 20 |
| `--read-length` | Read length | 100 | 50 to 250 |
| `--error` | Base error rate | 0.01 | 0 to 0.1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

HACk writes one FASTA and index per haplotype (`h1.fa`, `h2.fa`) in its output folder. The recipe copies them as `haplotype1.fa` and `haplotype2.fa`. A haplotype with a deletion is shorter than the reference, and one with a tandem duplication is longer, so check the sizes in the `.fai` files against the BED.

The recipe also writes:

- `regions.bed`: the SHORtS region file, one line per contig from base 1 to the longest haplotype length, with capture bias 100.0 and purity 100.0.
- `reads.bam` and its index: the sorted alignment of the simulated read pairs. The recipe passes `--tag`, so each read carries a haplotype tag (HP) and a clone tag (CL).
- `summary.txt`: contig lengths used for the region file.

Open the BAM in a genome viewer. A deletion on one haplotype should show roughly half the coverage across the deleted interval. A duplication should show extra coverage, and its edges can show read pairs with unexpected orientation or distance. Check each against the BED you wrote.

## Pitfalls

- **Coordinates are BED style.** HACk needs six columns: contig, start, end, type, information, and the length of random non-template sequence to add. The information column depends on the type, for example `None` for deletion and an integer for tandem duplication.
- **Overlapping variants are skipped.** When variants overlap, only the first is kept.
- **Translocations touch other haplotypes.** A translocation can create haplotypes that the BED list does not name directly.
- **Match the reference.** SHORtS and LASeR need the same reference FASTA that HACk used.
- **No seed option.** Repeated runs on the same inputs can differ.
- **Use low coverage for tests.** The documentation advises it to speed up the alignment step.
- **Haplotype lengths differ.** Compute the SHORtS region ends from the largest length per contig, as the documentation does, so the read count is right.
- **XENIA is beta.** The documentation warns that issues may appear.

## Further reading

- Source: https://github.com/davidebolo1993/VISOR
- Documentation: https://davidebolo1993.github.io/visordoc/
- Bolognini D, Sanders A, Korbel JO, Magi A, Benes V, Rausch T (2019). VISOR: a versatile haplotype-aware structural variant simulator for short- and long-read sequencing. Bioinformatics 36:1267-1269. https://doi.org/10.1093/bioinformatics/btz719

---

Cite: Bolognini D, Sanders A, Korbel JO, Magi A, Benes V, Rausch T (2019). VISOR: a versatile haplotype-aware structural variant simulator for short- and long-read sequencing. Bioinformatics 36:1267-1269. doi:10.1093/bioinformatics/btz719

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/visor).
