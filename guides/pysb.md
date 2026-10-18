# PySB

> Build a rule-based model in Python, let BioNetGen expand it to reactions, and integrate the ODEs with SciPy.

Licence: BSD-2-Clause · [Source code](https://github.com/pysb/pysb)

## What it simulates

PySB is a Python framework for rule-based models of biochemistry. You declare monomers (molecules with named binding and modification sites), parameters, and rules such as "a ligand with a free site binds a receptor with a free site". You do not list every reaction yourself.

A rule can cover many species. A protein with three phosphorylation sites has eight states, and a few rules generate all of them and the reactions between them. PySB passes the model to BioNetGen, which expands the rules into the species and reactions. PySB then simulates in one of several ways: SciPy ODE integration, a stochastic solver (through StochKit or BioNetGen), or network-free simulation with BioNetGen's NFsim or Kappa's KaSim.

Key assumptions: well-mixed compartments, mass-action kinetics unless you write an expression, and (for the ODE path) concentrations treated as continuous.

## When to use it

- Your system has combinatorial states, such as multi-site phosphorylation or receptor oligomers, and writing out every reaction is not practical.
- You want the model as Python code that you can version, test and script.
- You want one model run with several engines (ODE, stochastic, network-free) for comparison.

Alternatives:

- [Tellurium](tellurium.md) is simpler when the reaction list is short and written by hand.
- [GillesPy2](gillespy2.md) gives exact stochastic runs for an explicit reaction list.
- [AMICI](amici.md) can import PySB models and returns parameter sensitivities.

## Install

PySB 1.17.0 is the current release on PyPI (BSD-2-Clause, Python 3.11 or newer). The project docs recommend conda:

```bash
conda install -c alubbock pysb
```

That channel holds pysb 1.17.0 for linux-64, osx-64 and win-64. With pip, the docs say you must install BioNetGen yourself, either in the default path (`/usr/local/share/BioNetGen` on Mac and Linux) or at a folder named in the `BNGPATH` environment variable. Perl is also required.

```bash
pip install pysb==1.17.0
# download BioNetGen 2.9.3 from https://github.com/RuleWorld/bionetgen/releases
export BNGPATH=/path/to/BioNetGen-2.9.3
```

The recipe on this page does the pip route in a Python 3.11 image. It downloads the BioNetGen 2.9.3 Linux tarball and checks its SHA-256 digest. It targets linux/amd64 because that archive bundles x86-64 binaries.

## A first run

Adapted from the PySB [tutorial](https://github.com/pysb/pysb/blob/master/doc/tutorial.rst). It defines one molecule that is made at 3 copies per second and integrates for 60 seconds:

```python
from pysb import *
from pysb.integrate import Solver

Model()
Monomer('A')
Parameter('k', 3.0)
Rule('synthesize_A', None >> A(), k)

t = [0, 10, 20, 30, 40, 50, 60]
solver = Solver(model, t)
solver.run()
print(solver.y[:, 0])
```

The tutorial shows the result `[0, 30, 60, 90, 120, 150, 180]`. This is a straight line of 3 per second.

The recipe is a different script. It builds one of two bundled models and writes CSV files. `ligand_receptor` is a reversible binding rule with a bond between two sites. `robertson` is the stiff three-species system from `pysb/examples/robertson.py`.

## Run the tested example

This recipe builds PySB in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.6 s. PySB has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [pysb-recipe.tar.gz](https://biosimhub.pages.dev/guides/pysb/pysb-recipe.tar.gz) (Dockerfile, run_pysb.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pysb-recipe.tar.gz
   cd pysb
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/pysb:1.17.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pysb:1.17.0 python /opt/run_pysb.py --model ligand_receptor \
    --tend 40 --points 101 --kf 0.01 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `observables.csv` | 3.5 KB |
| `run_log.txt` | 86 B |
| `species.csv` | 3.5 KB |

<details><summary>First lines of <code>observables.csv</code></summary>

```
time,L_free,R_free,complex
0,100,50,0
0.4,84.933565,34.933568,15.066431
0.8,76.043461,26.043457,23.956544
1.2,70.389631,20.389612,29.610394
1.6,66.62092,16.620885,33.379126
2,64.029482,14.029442,35.970571
2.4,62.209278,12.209236,37.790776
2.8,60.911583,10.911541,39.088472
3.2,59.976555,9.9765137,40.0235
3.6,59.297687,9.2976452,40.702368
4,58.802072,8.8020296,41.197984
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
model=ligand_receptor species=3 reactions=2 rules=1 observables=L_free,R_free,complex
```

</details>

<details><summary>First lines of <code>species.csv</code></summary>

```
time,L(r=None),R(l=None),L(r=1) % R(l=1)
0,100,50,0
0.4,84.933565,34.933568,15.066431
0.8,76.043461,26.043457,23.956544
1.2,70.389631,20.389612,29.610394
1.6,66.62092,16.620885,33.379126
2,64.029482,14.029442,35.970571
2.4,62.209278,12.209236,37.790776
2.8,60.911583,10.911541,39.088472
3.2,59.976555,9.9765137,40.0235
3.6,59.297687,9.2976452,40.702368
4,58.802072,8.8020296,41.197984
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--model` | Bundled model | ligand_receptor | ligand_receptor, robertson |
| `--tend` | End time | 40 | 0.001 to 100000 |
| `--points` | Output time points | 101 | 2 to 5000 |
| `--kf` | Binding rate kf (ligand_receptor only) | 0.01 | 1e-05 to 100 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- **Observables.** `observables.csv` has a time column and one column per observable. An observable is a sum over every species that matches a pattern, for example all complexes that contain a bound ligand.
- **Species.** `species.csv` has one column per generated species. Species names show the bond pattern, for example `L(r=1) % R(l=1)`.
- **Log line.** `run_log.txt` reports how many species, reactions and rules the model has. For `ligand_receptor` the rule count is 1 and the species count is 3.
- **Mass balance.** In `ligand_receptor`, free ligand plus complex stays equal to the initial ligand at every time point.

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Pitfalls

- **BioNetGen is a separate install with pip.** Without it, model generation fails even though `import pysb` works. Check `BNGPATH`.
- **PySB statements assign names for you.** `Monomer('A')` creates a Python variable `A`. Do not reuse those names for other things.
- **Stiff systems need care.** The Robertson model is the standard stiff test. Set tolerances through `integrator_options` as the example script does.
- **Speed.** The docs list Cython as an optional extra that speeds up ODE integration. Without it the integrator is slower.
- **Large state spaces.** Network generation can explode for rules with many sites. Network-free simulation avoids generating the species at all.
- **Temporary files.** BioNetGen writes into a temporary directory. On systems where `/tmp` forbids execution or is read-only, set `TMPDIR` to a writable folder.

## Further reading

- Repository: https://github.com/pysb/pysb
- Documentation: https://docs.pysb.org/en/latest/
- Installation chapter: https://github.com/pysb/pysb/blob/master/doc/installation.rst
- BioNetGen: https://github.com/RuleWorld/bionetgen
- Lopez CF, Muhlich JL, Bachman JA, Sorger PK (2013). Programming biological models in Python using PySB. Mol Syst Biol 9:646. https://doi.org/10.1038/msb.2013.1

---

Cite: Lopez CF, Muhlich JL, Bachman JA, Sorger PK (2013). Programming biological models in Python using PySB. Mol Syst Biol 9:646. doi:10.1038/msb.2013.1

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pysb).
