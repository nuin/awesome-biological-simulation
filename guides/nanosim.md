# NanoSim

> Simulate Oxford Nanopore genomic reads from a reference genome using a pre-trained error and read-length model.

Licence: GPL-3.0-only · [Source code](https://github.com/BirolLab/NanoSim)

## What it simulates

NanoSim simulates Oxford Nanopore reads. It works in two stages. Characterization (`read_analysis.py`) takes real ONT reads and a reference, aligns them with minimap2 (or LAST), and learns the read length distribution, the error rates (mismatch, insertion, deletion), error context and, with `--fastq`, base quality distributions. Simulation (`simulator.py`) uses those profiles to produce reads from a reference.

Modes:

- `genome`: genomic reads from a genome FASTA. Circular or linear genomes, optional chimeric reads and homopolymer modelling.
- `transcriptome`: cDNA and direct RNA reads from a transcriptome, with intron retention and expression levels from a TSV file (Trans-NanoSim).
- `metagenome`: reads from several genomes with abundance levels, including abundance variation between samples (Meta-NanoSim).

Simulated reads fall into two classes. "Aligned" reads follow the learned error profile. "Unaligned" reads are random sequence that no aligner would place. Their share comes from the training data.

The biosimhub recipe runs genome mode with one pre-trained model: human HG002, ONT Kit 14 (R10 chemistry), basecalled with Dorado, trained on 1 million subsampled reads. Parameters are the number of reads, minimum and maximum read length and a seed. It applies the human read-length and error profile to whatever genome you upload.

## When to use it

Use NanoSim when error profiles should come from real data rather than a fixed rate, or when you need transcriptome or metagenome ONT reads.

Alternatives:

- [PBSIM2](pbsim2.md) simulates PacBio and ONT reads from an HMM of quality scores and a fixed difference ratio.
- [PBSIM3](pbsim3.md) simulates PacBio and ONT reads in whole-genome, transcript and template modes.
- [SimLoRD](simlord.md) simulates PacBio reads with an error model that follows the number of passes around the template.

## Install it yourself

Conda, pinned to Bioconda 3.2.3 (noarch, so it works on x86-64 and arm64 Linux and macOS):

```bash
conda create -n nanosim -c conda-forge -c bioconda nanosim=3.2.3
conda activate nanosim
simulator.py -h
```

The package pins `scikit-learn ~=0.23.2` and `numpy <1.24` because the pre-trained models are tightly tied to the scikit-learn version. The README warns that models built with older scikit-learn fail on newer versions with `No module named 'sklearn.neighbors.kde'`. Models trained by the v3.2.1 and later releases use scikit-learn 0.23.2.

Pre-trained models are not in the conda package. Download them from the `pre-trained_models` folder of the repository (https://github.com/BirolLab/NanoSim/tree/master/pre-trained_models). Each is a tarball of about 13 to 78 MB. The Kit 14 human model used by the recipe is `human_giab_hg002_sub1M_kitv14_dorado_v3.2.1.tar.gz`. Unpack it; the model prefix is the folder name plus `/training`.

## A first run

Adapted from the README usage section (https://github.com/BirolLab/NanoSim#usage).

Simulate 200 reads from a genome FASTA with the model above, in FASTQ format, with length limits:

```bash
simulator.py genome -rg reference.fa \
  -c human_giab_hg002_sub1M_kitv14_dorado_v3.2.1/training \
  -o sim -n 200 -min 200 -max 20000 --seed 42 --fastq
```

To train your own profile from reads (the step that needs real data), the README gives the characterization form:

```bash
read_analysis.py genome -i reads.fastq -rg reference.fa -o training --fastq
```

Add `-dna_type circular` to the simulator for a circular genome such as a bacterial chromosome. Add `--perfect` for error-free reads with only the length distribution.

## Run the tested example

This recipe builds NanoSim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.7 s.

1. Download [nanosim-recipe.tar.gz](https://biosimhub.pages.dev/guides/nanosim/nanosim-recipe.tar.gz) (Dockerfile, example reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf nanosim-recipe.tar.gz
   cd nanosim
   sh run.sh
   ```

![Terminal recording of the NanoSim example run](https://biosimhub.pages.dev/media/nanosim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/nanosim:3.2.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/nanosim:3.2.3 simulator.py genome -rg /work/in/reference.fa \
    -c /opt/models/human_giab_hg002_sub1M_kitv14_dorado_v3.2.1/training \
    -o sim -n 200 -min 200 -max 20000 --seed 42 \
    --fastq -t 1 > out/nanosim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `nanosim_log.txt` | 980 B |
| `sim_aligned_error_profile` | 994.1 KB |
| `sim_aligned_reads.fastq` | 3.0 MB |
| `sim_unaligned_reads.fastq` | 0 B |

<details><summary>First lines of <code>nanosim_log.txt</code></summary>

```

running the code with following parameters:

ref_g /work/in/reference.fa
model_prefix /opt/models/human_giab_hg002_sub1M_kitv14_dorado_v3.2.1/training
out sim
number [200]
coverage None
perfect False
homopolymer False
dna_type linear
strandness None
```

</details>

<details><summary>First lines of <code>sim_aligned_error_profile</code></summary>

```
Seq_name	Seq_pos	error_type	error_length	ref_base	seq_base
synthetic-ref_3393_aligned_0_R_35_12609_1	11721	mis	1	G	C
synthetic-ref_3393_aligned_0_R_35_12609_1	11618	mis	1	A	C
synthetic-ref_3393_aligned_0_R_35_12609_1	11532	del	1	G	-
synthetic-ref_3393_aligned_0_R_35_12609_1	11529	mis	1	T	G
synthetic-ref_3393_aligned_0_R_35_12609_1	11245	mis	2	AC	CT
synthetic-ref_3393_aligned_0_R_35_12609_1	10426	del	1	A	-
synthetic-ref_3393_aligned_0_R_35_12609_1	9918	mis	1	T	C
synthetic-ref_3393_aligned_0_R_35_12609_1	9233	ins	1	-	A
synthetic-ref_3393_aligned_0_R_35_12609_1	9201	del	2	TT	--
synthetic-ref_3393_aligned_0_R_35_12609_1	9199	mis	1	A	T
synthetic-ref_3393_aligned_0_R_35_12609_1	9194	mis	1	C	G
```

</details>

<details><summary>First lines of <code>sim_aligned_reads.fastq</code></summary>

```
@synthetic-ref_3393_aligned_0_R_35_12609_1
CGTTACACCTTGAATTCCGGACCGGAATGACTACTTTTTGAAGCAAATGAATATAGCTGCACTCCTTGGACGACCTTAGGACCCCGAAATAAAAGCGCCGTACCTGACTACCAGGGGGATCATGATTCCCAGGTGCACTGCGTCGAGGTGCCCTTCAGTCCGGCCGGACCGGGGCTTAAGCAGGTGTTAAGAGAGGGTTT
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-n` | Reads | 200 | 1 to 50000 |
| `-min` | Minimum read length | 200 | 50 to 100000 |
| `-max` | Maximum read length | 20000 | 100 to 1000000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

In the 3.2.3 source, with `-o sim` and `--fastq` the simulator writes:

- `sim_aligned_reads.fastq`: reads that follow the error profile.
- `sim_unaligned_reads.fastq`: random reads with error rates above 90%. The README says they "cannot be aligned". The number is drawn from the training data.
- `sim_aligned_error_profile`: for each read, the position, error type and original and new bases of every introduced error.

Without `--fastq` the reads are FASTA. Read headers carry the origin, as in the README: `>ref|NC-001143|-[chromosome=XI]_115406_aligned_16565_R_92_12710_2` means chromosome XI, start 115406, an aligned read, index 16565, reverse strand, and a head, middle and tail of 92, 12710 and 2 bases. Those figures come from the README example, not from a recipe run.

## Pitfalls

- **Seeding.** `--seed` is parsed, but the 3.2.3 `simulator.py` calls `np.random.seed()` and `random.seed()` without arguments inside the loop that starts the simulation processes. That replaces the seed. Run twice and compare the files before relying on it.
- **Human read lengths on small genomes.** The model carries human read lengths. Use `-max` so reads fit the sequence you provide.
- **Haploid references.** Coverage mode (`-x`) assumes a haploid reference. A diploid FASTA doubles the coverage.
- **scikit-learn versions.** The README reports that models trained by the user work with scikit-learn 1.0.2, while the pre-trained ones need 0.22.1 or 0.23.x.
- **Reads for training are real data.** The recipe cannot train a model; it only uses the downloaded one.
- **Output names.** The README names `simulated_reads.fasta`; the 3.2.3 code splits aligned and unaligned reads into separate files.

## Further reading

- Repository and README: https://github.com/BirolLab/NanoSim
- Yang C, Chu J, Warren RL, Birol I (2017). NanoSim: nanopore sequence read simulator based on statistical characterization. GigaScience 6(4):gix010. https://doi.org/10.1093/gigascience/gix010
- Hafezqorani S, et al. (2020). Trans-NanoSim characterizes and simulates nanopore RNA-sequencing data. GigaScience 9(6):giaa061. https://doi.org/10.1093/gigascience/giaa061
- Yang C, et al. (2023). Characterization and simulation of metagenomic nanopore sequencing data with Meta-NanoSim. GigaScience 12:giad013. https://doi.org/10.1093/gigascience/giad013

---

Cite: Yang C, Chu J, Warren RL, Birol I (2017). NanoSim, nanopore sequence read simulator based on statistical characterization. GigaScience 6(4):gix010. doi:10.1093/gigascience/gix010

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/nanosim).
