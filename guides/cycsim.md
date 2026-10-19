# CycSim

> Simulate context-aware long reads from a reference genome using a trained CycSim error model.

Licence: MIT · [Source code](https://github.com/BioEarthDigital/CycSim)

## What it simulates

CycSim simulates long reads whose errors depend on the surrounding sequence. First `cycsim train` reads real reads aligned to a reference and learns, for each k-mer (11 bases by default), how often errors occur and of what type. It also learns read lengths. Then `cycsim sim` samples reads from a genome using that model. You give a trained model and a reference. It returns aligned reads in BAM format.

Key assumptions: error behavior is the same for the same k-mer context, and the read-length profile matches the training data. A model made from one chemistry does not carry over to another.

## When to use it

- Simulate reads for a chemistry that has a trained model: the README lists CycloneSEQ S1, CycloneSEQ HD118, PacBio HiFi and ONT Q20.
- Train a model on your own run (HiFi or nanopore) to get errors that follow its context bias.
- Compare against context-free simulators.

Alternatives on biosimhub: [PBSIM3](pbsim3.md) uses quality-score HMMs for ONT and PacBio. [SimLoRD](simlord.md) models PacBio pass counts. [PBSIM2](pbsim2.md) is the older HMM tool.

## Install it yourself

CycSim 1.0.4 is on bioconda. It is built for linux/amd64 only. A dry run under emulation was killed, so the check is the recipe's image: it holds `cycsim-1.0.4-h4eafe19_0` installed from the same channels.

```
conda create -n cycsim -c conda-forge -c bioconda cycsim=1.0.4
conda activate cycsim
```

Train and simulate:

```
cycsim train -t 8 -r nanopore reads.bam reference.fa -o model.cy
cycsim sim -t 8 -d 30 model.cy reference.fa -o sim.bam
```

`-r` takes `hifi` or `nanopore`. `sim` defaults from the help text: 3 threads, depth 30, minimum aligned length 1000, maximum 500,000, noise 0.000001, seed 0 (random). `-D` sets total bases instead of depth.

## Run the tested example

This recipe builds CycSim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 21.7 s. CycSim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [cycsim-recipe.tar.gz](https://biosimhub.pages.dev/guides/cycsim/cycsim-recipe.tar.gz) (Dockerfile, example model.mod, reference.fa, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf cycsim-recipe.tar.gz
   cd cycsim
   sh run.sh
   ```

![Terminal recording of the CycSim example run](https://biosimhub.pages.dev/media/cycsim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/cycsim:1.0.4 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/cycsim:1.0.4 cycsim sim -t 1 -s 42 -D 100000 -m 1000 -M 500000 \
    -n 1e-06 /work/in/model.mod /work/in/reference.fa \
    -o reads.bam > out/cycsim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cycsim_log.txt` | 0 B |
| `reads.bam` | 93.0 KB |

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `-D` | Total bases to simulate | 100000 | 1000 to 200000000 |
| `-m` | Minimum aligned read length | 1000 | 100 to 100000 |
| `-M` | Maximum aligned read length | 500000 | 1000 to 1000000 |
| `-n` | Proportion of random error bases | 1e-06 | 0 to 0.1 |
| `-s` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example uses a shipped model (`model.mod`, 154,172 bytes) and a 20,000 bp reference. `-D 100000` asks for about 100,000 bases. The output `reads.bam` holds the simulated reads with their alignments; convert it with `samtools fastq reads.bam` if your pipeline wants FASTQ.

Decoded, the file has an unsorted header with one reference (`synthetic_ref`, 20,000) and 23 reads. They total 102,461 bases, with lengths from 2,516 to 5,955 (mean 4,455). Read names carry the origin, for example `000_1_synthetic_ref_6103_8957_0_2847_0_0_0`. Alignment columns: 100,471 matches or mismatches, 1,990 insertions and 1,802 deletions, an indel rate of 3.6%. `cycsim_log.txt` is empty.

## Your own runs

All runs use seed 42 and one thread.

- **Same seed, same reads.** A second run gives an identical BAM after decompression. The help warns that read order can vary with several threads.
- **More bases.** `-D 400000`. Result: 99 reads, 400,074 bases, indel rate unchanged at 3.6%.
- **Longer minimum.** `-m 3000`. Result: 21 reads, shortest 3,315, mean 4,879. Indel rate 3.7%.
- **Context-free errors.** Add `-g`. Result: 25 reads, indel rate 3.7%. On this small example both modes give similar indel totals (3.7% and 3.6%).

Two notes for your own runs. The model file ends in `.mod` here and `.cy` in the README. The example loads the `.mod` file, so the extension does not matter to the tool. The log is empty because the tool prints nothing on success.

## Pitfalls

- **Output is BAM.** Name it `.bam` in your own runs so tools open it correctly.
- **Model and chemistry must match.** Train on reads from the same platform you want to simulate.
- **Maximum length is a cap.** The example sets `-M 500000` but the longest read is 5,955 bp. The reference is 20 kb and the model sets the length profile.
- **Seed 0 means random.** The default seed gives different reads each run.
- **Memory.** Training loads up to 1 Gb of bases at once (`-b`). The recipe's container allows 3 GB.

## Further reading

- Source and models: https://github.com/BioEarthDigital/CycSim
- Hu et al. Context-aware simulation enables systematic optimization of long-read mapping parameters. GigaScience (2026). https://doi.org/10.1093/gigascience/giag079

---

Cite: Hu et al. CycSim, a context-based long-read simulator. GigaScience (2026). doi:10.1093/gigascience/giag079

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cycsim).
