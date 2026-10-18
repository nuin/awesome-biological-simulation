# squigulator

> Simulate raw nanopore signal (SLOW5/BLOW5) for DNA reads sampled from a reference genome, with R9.4.1 or R10.4.1 pore models and tunable noise.

Licence: MIT · [Source code](https://github.com/hasindu2008/squigulator)

## What it simulates

squigulator simulates raw nanopore signal: the "squiggle" of current samples a pore would record while a DNA or RNA strand moves through it. It samples read start positions from a reference, looks up the expected current level for each k-mer in a pore model, and adds Gaussian noise. The README says the simulation is deliberately simple and takes little effort to set up.

You pick a profile for the chemistry and flow cell: `dna-r9-min`, `dna-r9-prom`, `rna-r9-min`, `rna-r9-prom`, `dna-r10-min`, `dna-r10-prom`, `rna004-min` or `rna004-prom`. DNA profiles take a genome in FASTA and draw read lengths from a gamma distribution around the mean you set with `-r`. RNA profiles take a transcriptome and simulate whole transcripts. The output is a SLOW5 or BLOW5 file that a nanopore basecaller can read.

Key assumptions: reads copy the reference exactly, so there are no variants unless you add them to the reference first. Signal noise is Gaussian in amplitude, with dwell times (samples per base) drawn from a distribution you can tune.

## When to use it

Use squigulator to test basecallers, signal-level aligners and methylation or modification callers, and to produce data whose true position on the reference is known.

- Use [PBSIM3](pbsim3.md) when you only need nanopore reads as FASTQ with error profiles, without raw signal.
- Use [SimLoRD](simlord.md) for PacBio-style long reads.
- Use [VISOR](visor.md) when you want structural variants in the genome first, then reads from it. Use its haplotype FASTA files as the squigulator reference.

## Install

squigulator is MIT licensed. The current release is 0.5.0 (February 2026). Bioconda has it for linux-64, linux-aarch64, osx-64 and osx-arm64:

```bash
conda create -n squigulator -c conda-forge -c bioconda squigulator=0.5.0
conda activate squigulator
squigulator --version
```

The README also gives a precompiled x86-64 Linux binary under GitHub releases, and a build from source that needs a C99 compiler and the zlib development headers:

```bash
git clone https://github.com/hasindu2008/squigulator
cd squigulator && make
```

## A first run

Adapted from the README (https://github.com/hasindu2008/squigulator#usage) and `docs/man.md`. The commands have not been run for this guide. The simplest command is:

```bash
squigulator [OPTIONS] ref_genome.fa -o out_signal.blow5 -n NUM_READS
```

Examples from the README:

```bash
# 1000 PromethION DNA reads with perfect signals and no noise
squigulator hg38noAlt.fa -x dna-r9-prom -o reads.blow5 -n 1000 --ideal

# R10 chemistry PromethION DNA reads at 30X coverage
squigulator hg38noAlt.fa -x dna-r10-prom -o reads.blow5 -f 30
```

The README tests use a 30 kb SARS-CoV-2 reference. The recipe below draws 20 reads of about 400 bases from that genome with one thread. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds squigulator in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.3 s.

1. Download [squigulator-recipe.tar.gz](https://biosimhub.pages.dev/guides/squigulator/squigulator-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf squigulator-recipe.tar.gz
   cd squigulator
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/squigulator:0.5.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/squigulator:0.5.0 squigulator -x dna-r9-prom -n 20 -r 400 --seed 42 \
    -t 1 -o sim.slow5 -q perfect_reads.fa -c sim.paf /work/in/reference.fa
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `perfect_reads.fa` | 9.9 KB |
| `sim.paf` | 25.0 KB |
| `sim.slow5` | 333.7 KB |

<details><summary>First lines of <code>perfect_reads.fa</code></summary>

```
>S1_1!MN908947.3!10!513!-
TGACCATGAGGTGCAGTTCGAGCATCCGAACGTTTGATGAACACATAGGGCTGTTCAAGTTGAGGCAAAACGCCTTTTTCAACTTCTACTAAGCCACAAGTGCCATCTTTAAGATGTTGACGTGCCTCTGATAAGACCTCCTCCACGGAGTCTCCAAAGCCACGTACGAGCACGTCGCGAACCTGTAAAACAGGCAAACT
>S1_2!MN908947.3!15687!15891!+
CGTAAACATTTCTCAATGATGATACTCTCTGACGATGCTGTTGTGTGTTTCAATAGCACTTATGCATCTCAAGGTCTAGTGGCTAGCATAAAGAACTTTAAGTCAGTTCTTTATTATCAAAACAATGTTTTTATGTCTGAAGCAAAATGTTGGACTGAGACTGACCTTACTAAAGGACCTCATGAATTTTGCTCTCAACA
>S1_3!MN908947.3!21991!23108!-
CAAAAGAAAGTACTACTACTCTGTATGGTTGGTAACCAACACCATTAGTGGGTTGGAAACCATATGATTGTAAAGGAAAGTAACAATTAAAACCTTCAACACCATTACAAGGTGTGCTACCGGCCTGATAGATTTCAGTTGAAATATCTCTCTCAAAAGGTTTGAGATTAGACTTCCTAAACAATCTATACAGGTAATTA
>S1_4!MN908947.3!29182!29444!-
TTTGCTGTTTCTTCTGTCTCTGCGGTAAGGCTTGAGTTTCATCAGCCTTCTTCTTTTTGTCCTTTTTAGGCTCTGTTGGTGGGAATGTTTTGTATGCGTCAATATGCTTATTCAGCAAAATGACTTGATCTTTGAAATTTGGATCTTTGTCATCCAATTTGATGGCACCTGTGTAGGTCAACCACGTTCCCGAAGGTGTG
>S1_5!MN908947.3!15320!15786!-
AAAGTTCTTTATGCTAGCCACTAGACCTTGAGATGCATAAGTGCTATTGAAACACACAACAGCATCGTCAGAGAGTATCATCATTGAGAAATGTTTACGCAAATATGCGTAAAACTCATTCACAAAGTCTGTGTCAACATCTCTATTTCTATAGAGACAC
```

</details>

<details><summary>First lines of <code>sim.paf</code></summary>

```
S1_1!MN908947.3!10!513!-	4512	0	4512	-	S1_1!MN908947.3!10!513!-	498	0	498	498	498	255	sc:f:1.000000	sh:f:0.000000	ss:Z:13,12,6,15,10,10,5,7,7,11,10,11,12,10,13,1,13,4,9,13,9,11,10,11,9,12,13,8,4,2,10,
S1_2!MN908947.3!15687!15891!+	1818	0	1818	+	S1_2!MN908947.3!15687!15891!+	199	0	199	199	199	255	sc:f:1.000000	sh:f:0.000000	ss:Z:9,7,9,12,1,11,5,7,5,14,9,13,3,5,14,5,8,9,2,11,5,14,13,15,16,9,10,8,6,3,
S1_3!MN908947.3!21991!23108!-	10220	0	10220	-	S1_3!MN908947.3!21991!23108!-	1112	0	1112	1112	1112	255	sc:f:1.000000	sh:f:0.000000	ss:Z:1,8,10,9,5,15,8,8,7,12,7,3,12,11,6,9,2,15,4,7,11,18,8,11,8,11,5,1
```

</details>

<details><summary>First lines of <code>sim.slow5</code></summary>

```
#slow5_version	0.2.0
#num_read_groups	1
@asic_id	asic_id_0
@exp_start_time	2026-02-20T00:00:00Z
@experiment_name	experiment_0
@experiment_type	genomic_dna
@flow_cell_id	FAN00000
@flow_cell_product_code	FLO-PRO002
@protocol_run_id	protocol_run_0
@protocol_start_time	2026-02-20T00:00:00Z
@run_id	run_0
@sample_frequency	4000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-x` | Pore and flow cell profile | dna-r9-prom | dna-r9-min, dna-r9-prom, dna-r10-min, dna-r10-prom |
| `-n` | Reads | 20 | 1 to 2000 |
| `-r` | Mean read length (bases) | 400 | 100 to 20000 |
| `--ideal` | Noise-free signal | not set | bool |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe writes three files:

- `sim.slow5` is the signal file in the text form of SLOW5. It starts with header lines (`#slow5_version`, flow cell and sampling-rate fields), then one tab-separated row per read. The columns include `read_id`, `digitisation`, `offset`, `range`, `sampling_rate`, `len_raw_signal` and `raw_signal`, which is a comma-separated list of integer current samples. A `.blow5` extension gives the compact binary form instead.
- `perfect_reads.fa` holds the exact reference sequence behind each read. These are not basecalled reads and carry no sequencing errors. To get realistic reads, basecall the signal.
- `sim.paf` aligns each signal to its read, in the resquiggle PAF format described in the f5c documentation.

Read IDs encode where each read came from, in the form `S1_33!chr1!225258409!225267761!-` (the README's example): a read name, the contig, a 0-based start and end, and the strand. This works with the `mapeval` command in `paftools.js` from minimap2.

A useful check is that signal length is roughly read length times the mean dwell. The `docs/man.md` default dwell mean is 9.0 samples per base, so a 400-base read should have about 3600 samples.

## Pitfalls

- **Threads default to 8.** The recipe sets one thread. Raise `-t` on a larger machine.
- **`-n` and `-f` are exclusive.** Set a read count or a fold coverage, not both. `--full-contigs` is exclusive with both `-n` and `-r`.
- **DNA profiles need a genome and RNA profiles need a transcriptome.** A mismatch gives odd reads or an error.
- **No variants by default.** Apply variants with `bcftools consensus` first, as the README shows.
- **The FASTA from `-q` is perfect.** Basecalling is a separate step, for example with buttery-eel or the dorado fork named in the README.
- **Seed 0 means random.** `--seed` with a positive integer reproduces a run.
- **Noise options.** `--ideal`, `--ideal-amp` and `--ideal-time` remove noise. `--amp-noise`, `--dwell-mean` and `--dwell-std` tune it.

## Further reading

- Source and README: https://github.com/hasindu2008/squigulator
- Options: https://github.com/hasindu2008/squigulator/blob/main/docs/man.md
- Output formats: https://github.com/hasindu2008/squigulator/blob/main/docs/output.md
- Gamaarachchi H, Ferguson JM, Samarakoon H, Liyanage K, Deveson IW (2024). Simulation of nanopore sequencing signal data with tunable parameters. Genome Research 34:778-783. https://doi.org/10.1101/gr.278730.123

---

Cite: Gamaarachchi H, Ferguson JM, Samarakoon H, Liyanage K, Deveson IW (2024). Simulation of nanopore sequencing signal data with tunable parameters. Genome Research 34:778-783. doi:10.1101/gr.278730.123

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/squigulator).
