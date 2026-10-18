# SimProt

> Protein sequence evolution with indels along a tree; writes the true alignment.

Licence: GPL-3.0-or-later (developer's rights; UHN notice kept) · [Source code](https://github.com/nuin/simprot)

**[Run SimProt in your browser](https://biosimhub.pages.dev/run/simprot/index.html)**: Protein sequence evolution with indels along a tree; writes the true alignment. Nothing to install; the first visit downloads about 0 MB.

## What it simulates

SimProt evolves protein sequences with indels down a tree and writes the true alignment. It starts from a random root sequence. On each branch it applies amino-acid substitutions from an empirical matrix (PAM, JTT or PMB) and insertion and deletion events. Branch lengths are expected substitutions per site.

Paulo Nuin wrote SimProt in Elisabeth Tillier's lab at the University Health Network (UHN), Toronto. Pang, Smith, Nuin and Tillier described it in 2005. Indel lengths follow the empirical distribution of Qian and Goldstein, reparameterised so it applies to sequences diverged for different times. A Zipfian model (Benner) is the alternative.

Key assumptions: sites evolve independently apart from indels, rates across sites follow a gamma distribution, and the tree is bifurcating. The true alignment records which residues share an ancestor, so you can score an aligner against it.

## When to use it

Use SimProt to benchmark multiple sequence aligners, tree builders or homology detection on proteins where the true alignment is known.

Alternatives on biosimhub:

- **[Pyvolve](pyvolve.md)** and **[Seq-Gen](seq-gen.md)** simulate protein substitutions with standard matrices. They write no gaps, so they fit when indels are not the question.
- **[Bio++ bppseqgen](bppseqgen.md)** fits when you want the substitution model written out explicitly, again without indels.

## Run it in your browser

The page compiles the C++ program to WebAssembly. Nothing is uploaded. Controls:

- **Newick tree:** the box holds an example of 40 taxa (seq81 to seq120). Paste your own bifurcating tree with branch lengths.
- **Seed:** 42 by default. The same parameters and seed give the same output.
- **Root length:** residues in the root sequence (100 by default).
- **Substitution model:** PAM, JTT or PMB (default PMB).
- **Gamma alpha:** shape for rate variation across sites. 1 by default. Enter -1 for equal rates.
- **Indel frequency:** 0.03 by default. Higher means more indel events per branch.
- **Indel model:** Qian-Goldstein (default), Benner or None.
- **Branch scale:** multiplies every branch length (1 by default).

Click Run. The status line reads `Done: 40 sequences in N ms` and the box shows the true alignment in FASTA with gaps. The browser build shows only the alignment. The command-line program also writes the ungapped sequences and an indel log.

Limits: one tree per run, and the build is single-threaded.

## Install it yourself

The repository README gives a CMake build. Build from source with CMake and a C++20 compiler:

```bash
git clone https://github.com/nuin/simprot
cd simprot/simprot-cpp
cmake -B build -DCMAKE_BUILD_TYPE=Release
cmake --build build --target simprot
```

The build was checked at commit d564bd8, the commit the browser page is built from. On macOS the default build also compiles the test suite, and that step failed on Catch2, so name the `simprot` target as above. Minimal run:

```bash
./build/simprot -f tree.nwk -r 100 -S 42 -a alignment.fa -s sequences.fa -o indels.log
```

For the default parameters, the native alignment and the browser alignment were byte-identical.

## Reading the output

With the defaults (40-taxon tree, root 100, PMB, alpha 1, indel frequency 0.03, Qian-Goldstein, seed 42):

- The alignment has 40 sequences and 109 columns. 19 columns hold at least one gap.
- The ungapped sequences are 98 to 102 residues long, around the 100-residue root.
- The indel log lists 17 events: 8 insertions and 9 deletions, the longest 2 residues. Each event appears as a line `>distance d` (the branch length) followed by `Ins n` or `Del n`, with n the event length.

Gap columns are the part that substitution-only simulators cannot give you. A gap in the true alignment marks a residue that was inserted or deleted along the tree.

## Your own runs

Each change is from the defaults, seed 42, 40-taxon example tree.

**Indel model None.** The alignment has 100 columns, no gaps, and all sequences have 100 residues. Substitutions only.

**Indel frequency 0.1.** 134 columns, 62 with gaps, 44 events (24 insertions), longest 4. Frequency 0.03 gave 17 events.

**Benner indel model.** 133 columns, 39 events (27 insertions), longest 4.

**Branch scale 2 and 0.5.** At 2 the alignment has 117 columns and 24 events. At 0.5 it has 100 columns, 3 events and 3 gap columns. Indels accumulate with branch length.

**Gamma alpha.** Identity between the first and last taxon over ungapped columns was 0.289 at alpha 1, 0.220 with equal rates (-1) and 0.360 at alpha 0.3. This is one pair in one run, so it shows direction only. Low alpha makes a few sites fast and many slow.

**Matrix.** PAM 0.278, JTT 0.320, PMB 0.289 for the same pair and seed. The matrices differ in rate scaling and exchange pattern.

**Seed 7** gave 118 columns against 109. **Root length 300** gave 357 columns.

## Pitfalls

- **Use the program's own help for flags.** In the C++ build `-b` is the indel model and `-t` is the branch scale. The repository README's option table lists `-b` as branch scale, but the program uses `-t` for that.
- **-1 means equal rates for alpha.** An alpha of 0 does not give equal rates.
- **Bifurcating trees only.** The README says so. Resolve polytomies first. Zero-length branches are accepted, as in the example tree.
- **Branch lengths are substitutions per site.** Rescale trees in years or generations with the branch scale.
- **Indel counts vary by seed.** Seed 42 gave 17 events and seed 7 gave a different alignment length (118 columns). Run many seeds for benchmarks.
- **Licence.** SimProt is GPL-3.0-or-later to the extent the developer holds rights. The original UHN notice stays and says the program may not be sold. See the NOTICE file in the repository.

## Further reading

- Source: https://github.com/nuin/simprot
- Pang A, Smith AD, Nuin PAS, Tillier ERM (2005). SIMPROT: using an empirically determined indel distribution in simulations of protein evolution. BMC Bioinformatics 6:236. https://doi.org/10.1186/1471-2105-6-236
- Nuin PAS, Wang Z, Tillier ERM (2006). The accuracy of several multiple sequence alignment methods for proteins. BMC Bioinformatics 7:471, cited in the repository README.

---

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simprot).
