# bioCRNpyler

> Compile a gene-expression circuit (constitutive gene or a repressor pair) into a chemical reaction network, export it as SBML, and integrate its mass-action time course.

Licence: BSD-3-Clause · [Source code](https://github.com/BuildACell/bioCRNpyler)

## What it simulates

bioCRNpyler compiles a description of biological parts into a chemical reaction network (CRN). You declare DNA assemblies (promoter, ribosome binding site, protein), choose a mixture that says how transcription, translation and dilution work, and the library writes the reactions and rate laws. The network can be exported as SBML or handed to a simulator.

The recipe here fixes the circuit to one of two shapes and integrates the result as deterministic ODEs with scipy. In the `constitutive` circuit, gene 1 makes protein P1 from an always-on promoter. In the `repressor` circuit, gene 2 makes P2 constitutively, and P2 represses the promoter of gene 1 through a negative Hill function.

Assumptions: well-mixed concentrations in micromolar, rates per second, no noise, and a mixture without explicit RNA polymerase or ribosomes (`SimpleTxTlDilutionMixture`). Every species is lost by dilution, and mRNA is lost faster through an extra degradation term.

## When to use it

- Use it to write a circuit once and get its reactions, an SBML file and a time course from the same description.
- Use it to see how a model changes when only the mixture changes (simple, resource-aware, cell-free), which is the library's main idea.
- For stochastic single-cell traces of a network you already have as reactions, [GillesPy2](gillespy2.md) fits better.

## Install it yourself

The recipe image installs python 3.12, python-libsbml 5.20.4, numpy, scipy, matplotlib, networkx and bokeh from conda-forge, then bioCRNpyler 1.3.4 from PyPI:

```
micromamba create -n bcp -c conda-forge python=3.12 pip python-libsbml numpy scipy matplotlib-base networkx bokeh
micromamba run -n bcp pip install --no-deps biocrnpyler==1.3.4
```

The image leaves out `fa2_modified`, which needs a C compiler to build. Compiling a CRN, SBML export and the simulation below all work without it.

## Run the tested example

This recipe builds bioCRNpyler in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.9 s.

1. Download [biocrnpyler-recipe.tar.gz](https://biosimhub.pages.dev/guides/biocrnpyler/biocrnpyler-recipe.tar.gz) (Dockerfile, run_biocrn.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf biocrnpyler-recipe.tar.gz
   cd biocrnpyler
   sh run.sh
   ```

![Terminal recording of the bioCRNpyler example run](https://biosimhub.pages.dev/media/biocrnpyler/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/biocrnpyler:1.3.4 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/biocrnpyler:1.3.4 python /opt/run_biocrn.py --circuit repressor \
    --dna 0.01 --ktx 0.05 --ktl 0.05 --dilution 0.000578 \
    --rna_deg 0.005 --kd 0.5 --hill 2 --tmax 10000 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `crn.txt` | 891 B |
| `model.xml` | 8.8 KB |
| `run_log.txt` | 101 B |
| `summary.json` | 194 B |
| `timecourse.csv` | 11.2 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/biocrnpyler/result-dark.png"><img src="https://biosimhub.pages.dev/media/biocrnpyler/result.png" alt="Plot of the bioCRNpyler example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>crn.txt</code></summary>

```
Species(N = 6) = {
    rna[G2] (@ 0.01),  
    dna[G2] (@ 0.01),  
    rna[G1] (@ 0.01),  
    dna[G1] (@ 0.01),  
    protein[P2] (@ 0),  
    protein[P1] (@ 0),  
}

Reactions (10) = [
0. dna[G1] --> dna[G1]+rna[G1]
 Kf = k dna[G1] / ( 1 + (protein[P2]/K)^2.0 )
```

</details>

<details><summary>First lines of <code>model.xml</code></summary>

```
<?xml version="1.0" encoding="UTF-8"?>
<sbml xmlns="http://www.sbml.org/sbml/level3/version2/core" level="3" version="2">
  <model id="biocrnpyler_485010" name="biocrnpyler_485010" substanceUnits="mole" timeUnits="sec" volumeUnits="litre" areaUnits="square_metre" lengthUnits="metre" extentUnits="mole">
    <listOfUnitDefinitions>
      <unitDefinition id="square_metre">
        <listOfUnits>
          <unit kind="metre" exponent="2" scale="0" multiplier="1"/>
        </listOfUnits>
      </unitDefinition>
      <unitDefinition id="sec">
        <listOfUnits>
          <unit kind="second" exponent="1" scale="0" multiplier="1"/>
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 6 species, 10 reactions, protein_P2=7.727, rna_G1=0.000374, protein_P1=0.03903, rna_G2=0.08964
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "species": 6,
 "reactions": 10,
 "final_uM": {
  "protein_P2": 7.727421411546531,
  "rna_G1": 0.00037401921307239383,
  "protein_P1": 0.03902543866341233,
  "rna_G2": 0.08963786303334562
 }
}
```

</details>

<details><summary>First lines of <code>timecourse.csv</code></summary>

```
time_s,dna_G1,protein_P2,rna_G1,protein_P1,dna_G2,rna_G2
0.0,0.01,0,0,0,0.01,0
50.0,0.01,0.0282574,0.0218007,0.0282507,0.01,0.0218165
100.0,0.01,0.102593,0.0379238,0.102239,0.01,0.0383231
150.0,0.01,0.210284,0.048516,0.207065,0.01,0.0508123
200.0,0.01,0.341746,0.053384,0.327894,0.01,0.0602619
250.0,0.01,0.48977,0.053266,0.450832,0.01,0.0674115
300.0,0.01,0.648941,0.0497892,0.565451,0.01,0.0728211
350.0,0.01,0.815204,0.044602,0.665823,0.01,0.076914
400.0,0.01,0.985526,0.0388804,0.749704,0.01,0.0800108
450.0,0.01,1.15765,0.0333103,0.817186,0.01,0.0823539
500.0,0.01,1.32991,0.0282314,0.869583,0.01,0.0841267
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--circuit` | Circuit | repressor | constitutive, repressor |
| `--dna` | DNA concentration per gene (uM) | 0.01 | 0.0001 to 10 |
| `--ktx` | Transcription rate (1/s) | 0.05 | 0.0001 to 5 |
| `--ktl` | Translation rate (1/s) | 0.05 | 0.0001 to 5 |
| `--dilution` | Dilution rate (1/s) | 0.000578 | 1e-05 to 0.1 |
| `--rna_deg` | Extra mRNA degradation (1/s) | 0.005 | 0.0001 to 1 |
| `--kd` | Repressor dissociation constant (uM) | 0.5 | 0.001 to 100 |
| `--hill` | Repressor Hill coefficient | 2 | 1 to 4 |
| `--tmax` | Simulated time (s) | 10000 | 100 to 100000 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper `run_biocrn.py` builds the circuit, calls `compile_crn()`, then integrates the reactions for 10,000 s. The run took 1.9 s.

- `run_log.txt` has one line: "done: 6 species, 10 reactions, protein_P2=7.727, rna_G1=0.000374, protein_P1=0.03903, rna_G2=0.08964". Concentrations are micromolar at 10,000 s.
- `crn.txt` lists 6 species and 10 reactions. Reaction 0 is the repressed transcription of gene 1: rate = k [dna_G1] / (1 + ([P2]/K)^2), with k = 0.05 per s and K = 0.5 uM. The other rate laws are mass action: translation at 0.05 per s, dilution at 0.000578 per s (a 20 minute half-life) and mRNA degradation at 0.005 per s on top of dilution.
- `model.xml` is the same network as SBML Level 3 (8,962 bytes).
- `timecourse.csv` has 201 rows from 0 to 10,000 s.
- `summary.json` repeats the final concentrations.

Check the constitutive gene against the steady-state formula. Gene 2 gives mRNA = ktx x DNA / (dilution + mRNA degradation) = 0.05 x 0.01 / 0.005578 = 0.0896 uM, matching rna_G2 = 0.08964. Protein = ktl x mRNA / dilution = 0.05 x 0.0896 / 0.000578 = 7.75 uM. The run gives 7.727, because 10,000 s is 5.8 protein lifetimes and the protein is 99.7 % of the way there.

The repressed gene shows the delay of a regulatory loop. P1 follows P2 up at first: at 250 s P1 is 0.451 uM and P2 is 0.490 uM. P1 peaks at 0.970 uM near 750 s, when P2 has reached 2.16 uM and transcription of gene 1 is already cut to 1/(1 + 4.3^2) = 5 %. P1 then falls to 0.039 uM at 10,000 s, 0.5 % of P2.

## Your own runs

Each run changes one value from the example. Each ran in the recipe's image.

- **No repressor.** `--circuit constitutive` gave 3 species, 5 reactions and P1 = 7.727 uM, the same as P2 in the default run. The circuit with repression ends 200 times lower.
- **Weaker repression.** `--kd 5` gave P1 = 2.353 uM at the end, with a peak of 3.73 uM at 2,300 s. A 10-fold higher dissociation constant leaves 60 times more P1.
- **Gentler switch.** `--hill 1` gave P1 = 0.484 uM at the end and a peak of 1.16 uM at 1,200 s. Hill coefficient 2 repressed harder.
- **Faster growth.** `--dilution 0.002` gave P2 = 1.786 uM and P1 = 0.130 uM. Faster dilution lowers both proteins, and P1 peaked at 0.606 uM at 550 s.
- **Ten times more DNA.** `--dna 0.1` gave P2 = 77.27 uM, P1 = 0.0158 uM and a P1 overshoot of 2.65 uM at 500 s. More DNA gives a bigger overshoot and a stronger final repression.

## Pitfalls

- **No seed.** The ODE model is deterministic, so the same inputs always give the same numbers.
- **Initial concentrations in `crn.txt`.** The species table lists mRNA at 0.01 uM, because bioCRNpyler attaches the assembly's initial concentration to the transcript too. The helper script starts at DNA only, so the time course begins with mRNA at 0.
- **Concentrations get large.** The default rates are the library's E. coli defaults. High DNA, transcription and translation rates give protein in the tens of micromolar, which is above a real cell.
- **Two loss terms for mRNA.** mRNA loses dilution plus `--rna_deg`. Setting `--rna_deg` to 0 fails inside bioCRNpyler, which needs positive rates. The recipe's minimum is 0.0001.
- **Two rate laws only.** The helper integrates mass action and the negative Hill law. A different promoter or mixture in your own script may produce other propensities, which the helper stops on.

## Further reading

- SBML: http://sbml.org
- Source: https://github.com/BuildACell/bioCRNpyler
- Paper: Poole W et al. (2022) BioCRNpyler: Compiling chemical reaction networks from biomolecular parts in diverse contexts. PLoS Comput Biol 18:e1009987. https://doi.org/10.1371/journal.pcbi.1009987

---

Cite: Poole W, Pandey A, Shur A, Tuza ZA, Murray RM (2022). BioCRNpyler: Compiling chemical reaction networks from biomolecular parts in diverse contexts. PLoS Comput Biol 18:e1009987. doi:10.1371/journal.pcbi.1009987

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/biocrnpyler).
