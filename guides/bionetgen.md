# BioNetGen

> Generate the reaction network of a rule-based model written in BNGL, then simulate it with the actions in the file (ODE, SSA, or network-free NFsim).

Licence: MIT · [Source code](https://github.com/RuleWorld/bionetgen)

## What it simulates

BioNetGen simulates rule-based models of biochemical systems, such as signal transduction, metabolism and gene regulation, written in the BioNetGen language (BNGL). A BNGL file declares parameters, molecule types, seed species, observables and reaction rules. A rule describes a transformation that applies to every species that matches its pattern. A short list of rules can therefore stand for thousands of reactions.

BioNetGen works in two ways.

- **Network-based.** The `generate_network` action expands the rules into a full reaction network (a `.net` file). `simulate` then integrates it as ODEs or runs a stochastic simulation (SSA) on it, with the `run_network` program.
- **Network-free.** The NFsim engine simulates the rules directly and never builds the network. It suits models where the network is too large to generate.

The README describes the code as a mixture of Perl, C++ and Python. Network generation is in Perl and the simulator is in C++. The simulation actions are written at the end of the model file.

## When to use it

Use BioNetGen when one protein has several sites or states, so that listing every species by hand is impractical, and you want an ODE or SSA result from the generated network.

- Use [KaSim / KappaTools](kasim-kappatools.md) when you work in the Kappa language, or when you only want agent-based network-free simulation.
- Use [libRoadRunner](libroadrunner.md) when the model is already an SBML file and you want fast ODE solutions of it. BioNetGen can export SBML from a generated network.
- Use [COPASI](copasi.md) for parameter estimation and steady-state analysis of a species-level model.

## Install it yourself

There are two routes, both from the project's documents.

**Release archive.** The README says to download the latest release for your system, unpack it and run it with Perl. The current release is BioNetGen 2.9.3 (April 2025). The Linux archive is `BioNetGen-2.9.3-linux.tar.gz`, from https://github.com/RuleWorld/bionetgen/releases/tag/BioNetGen-2.9.3. It holds `BNG2.pl`, the `Perl2` modules, `bin/run_network`, `bin/NFsim` and example models in `Models2`. The compiled programs in the Linux archive are 64-bit x86 ELF files.

**PyBioNetGen.** The quickstart uses a command-line wrapper:

```bash
pip install bionetgen==0.8.7
bionetgen -h
```

The package exists on PyPI as `bionetgen` 0.8.7 (MIT). The documentation says Perl must be installed as well.

The recipe below uses the release archive, pinned by its SHA-256 sum, plus Perl from conda-forge. It does not use PyBioNetGen. The image is linux/amd64 because the archive's binaries are x86.

## Run the tested example

This recipe builds BioNetGen in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.8 s. BioNetGen has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [bionetgen-recipe.tar.gz](https://biosimhub.pages.dev/guides/bionetgen/bionetgen-recipe.tar.gz) (Dockerfile, example model.bngl, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf bionetgen-recipe.tar.gz
   cd bionetgen
   sh run.sh
   ```

![Terminal recording of the BioNetGen example run](https://biosimhub.pages.dev/media/bionetgen/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/bionetgen:2.9.3 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/bionetgen:2.9.3 perl /opt/BioNetGen/BNG2.pl --outdir /work/out /work/in/model.bngl > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `model.cdat` | 15.8 KB |
| `model.gdat` | 15.8 KB |
| `model.net` | 562 B |
| `run_log.txt` | 1.7 KB |

<details><summary>First lines of <code>model.cdat</code></summary>

```
#              time                  S1                  S2                  S3
 0.000000000000e+00  9.900000000000e+01  1.000000000000e+00  0.000000000000e+00
 1.500000000000e-01  9.887298896527e+01  1.075660494638e+00  5.135054009089e-02
 3.000000000000e-01  9.873656109523e+01  1.156857056019e+00  1.065818487495e-01
 4.500000000000e-01  9.859005797142e+01  1.243964983987e+00  1.659770445983e-01
 6.000000000000e-01  9.843278097762e+01  1.337380536004e+00  2.298384863768e-01
 7.500000000000e-01  9.826399010529e+01  1.437521196549e+00  2.984886981595e-01
 9.000000000000e-01  9.808290282070e+01  1.544825857765e+00  3.722713215394e-01
 1.050000000000e+00  9.788869269881e+01  1.659755016707e+00  4.515522844848e-01
 1.200000000000e+00  9.768048848443e+01  1.782790669066e+00  5.367208464998e-01
 1.350000000000e+00  9.745737334617e+01  1.914435982211e+00  6.281906716228e-01
 1.500000000000e+00  9.721838444864e+01  2.055214754544e+00  7.264007968151e-01
```

</details>

<details><summary>First lines of <code>model.gdat</code></summary>

```
#              time                   S                   I                   R
 0.000000000000e+00  9.900000000000e+01  1.000000000000e+00  0.000000000000e+00
 1.500000000000e-01  9.887298896527e+01  1.075660494638e+00  5.135054009089e-02
 3.000000000000e-01  9.873656109523e+01  1.156857056019e+00  1.065818487495e-01
 4.500000000000e-01  9.859005797142e+01  1.243964983987e+00  1.659770445983e-01
 6.000000000000e-01  9.843278097762e+01  1.337380536004e+00  2.298384863768e-01
 7.500000000000e-01  9.826399010529e+01  1.437521196549e+00  2.984886981595e-01
 9.000000000000e-01  9.808290282070e+01  1.544825857765e+00  3.722713215394e-01
 1.050000000000e+00  9.788869269881e+01  1.659755016707e+00  4.515522844848e-01
 1.200000000000e+00  9.768048848443e+01  1.782790669066e+00  5.367208464998e-01
 1.350000000000e+00  9.745737334617e+01  1.914435982211e+00  6.281906716228e-01
 1.500000000000e+00  9.721838444864e+01  2.055214754544e+00  7.264007968151e-01
```

</details>

<details><summary>First lines of <code>model.net</code></summary>

```
# Created by BioNetGen 2.9.3
begin parameters
    1 N              1.0e2  # Constant
    2 I0             1  # Constant
    3 R0             2.5  # Constant
    4 g              0.33  # Constant
    5 b              (g*R0)/N  # ConstantExpression
    6 _InitialConc1  N-I0  # ConstantExpression
end parameters
begin species
    1 S() _InitialConc1
    2 I() I0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
BioNetGen version 2.9.3
Reading from file /work/in/model.bngl (level 0)
Read 5 parameters.
Read 2 species.
Read 3 observable(s).
Read 2 reaction rule(s).
ACTION: generate_network( model )
Iteration   0:     2 species      0 rxns  0.00e+00 CPU s
Iteration   1:     3 species      2 rxns  1.00e-02 CPU s
Iteration   2:     3 species      2 rxns  0.00e+00 CPU s
Cumulative CPU time for each rule
Rule   1:     1 reactions 1.00e-02 CPU s 1.00e-02 CPU s/rxn
```

</details>


## A first run

Adapted from the BioNetGen quickstart: https://bionetgen.readthedocs.io/en/latest/bng_quickstart.html

Save this as `SIR.bngl`. It is an epidemic model with susceptible (S), infected (I) and recovered (R) individuals.

```
begin model

begin parameters
  N  1.0e2
  I0 1
  R0 2.5
  g  0.33
  b  g*R0/N
end parameters

begin species
  S() N-I0
  I() I0
end species

begin observables
  Molecules S S()
  Molecules I I()
  Molecules R R()
end observables

begin reaction rules
  R1: S + I -> I + I b
  R2: I -> R g
end reaction rules

end model

# Actions
generate_network({overwrite=>1})
simulate({method=>"ode",t_end=>30,n_steps=>200})
```

The quickstart runs it with `bionetgen run -i SIR.bngl -o sir_output`. With the release archive, the equivalent is:

```bash
perl BNG2.pl --outdir sir_output SIR.bngl
```

The `--outdir` option is listed in the script's usage text.

## Reading the output

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

BioNetGen names its outputs after the model file. For a file named `model.bngl` expect:

- `model.net`: the generated network, with the parameters, species, reactions and observable groups as numbered lists.
- `model.gdat`: the observables over time. One row per output point, one column per observable (`S`, `I`, `R` in the example), with time first.
- `model.cdat`: the concentration of every species in the network over time.

The example has 200 steps to time 30, so the data files have 201 rows including time 0. The action in the file fixes this. The three observables sum to N at every step, because the rules only move individuals between classes. That check catches a mistyped rule.

## Pitfalls

- **Actions live in the model file.** The recipe passes no simulation settings. To change the end time or method, edit the `simulate` call.
- **Output names follow the input name.** Upload a file with another base name and the outputs change with it.
- **Large rule sets can generate huge networks.** If `generate_network` runs out of time or memory, switch to NFsim with `simulate({method=>"nf", ...})`, which never builds the network.
- **Perl is required.** Without it, `BNG2.pl` does not start. On Windows the install notes recommend Strawberry Perl or conda-forge Perl.
- **Stochastic runs need a seed.** The ODE example is deterministic. For SSA add `seed=>` to the `simulate` call so a result can be repeated.

## Further reading

- Project and README: https://github.com/RuleWorld/bionetgen
- Quickstart and tutorials: https://bionetgen.readthedocs.io/en/latest/bng_quickstart.html
- PyBioNetGen on PyPI: https://pypi.org/project/bionetgen/
- Site: https://bionetgen.org
- Paper: Harris LA et al. (2016) BioNetGen 2.2: advances in rule-based modeling. Bioinformatics 32:3366-3368. https://doi.org/10.1093/bioinformatics/btw469

---

Cite: Harris LA et al. (2016). BioNetGen 2.2: advances in rule-based modeling. Bioinformatics 32:3366-3368. doi:10.1093/bioinformatics/btw469

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/bionetgen).
