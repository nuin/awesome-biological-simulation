# KaSim / KappaTools

> Simulate a rule-based Kappa model stochastically with the network-free KaSim engine (through the kappy Python client) and return the observables over time.

Licence: LGPL-3.0-only · [Source code](https://github.com/Kappa-Dev/KappaTools)

## What it simulates

KappaTools simulates rule-based models of protein interactions written in the Kappa language. A model declares agents (for example a protein A with a binding site x), rules that rewrite patterns of agents and bonds, initial agent counts, and observables to record. KaSim, the simulator, runs the model stochastically in continuous time. Kappy is the Python client that starts KaSim, runs a model and returns the recorded observables.

KaSim is network-free. It does not list every possible molecular complex before it starts. It keeps the current set of agents and applies rules to them. This matters when a few sites per protein produce more complexes than any reaction list could hold.

The suite also holds KaSa, a static analyser for Kappa models, and tools for extracting stories from simulation traces. This guide covers simulation.

A rule fires with a stochastic rate. In the README example `A(x[.]), A(x[.]) <-> A(x[1]), A(x[1]) @ 1e-2,1` two free A agents bind through x at rate 0.01 and the bond breaks at rate 1. The notation `x[.]` means site x is free. `x[1]` means site x is bound, and bond label 1 pairs the two ends.

## When to use it

Use KappaTools when proteins have several binding or modification sites and the number of complexes is too large to enumerate. Use it also when you want the simulation to follow single agents and bonds, with random events and small counts.

- Use [BioNetGen](bionetgen.md) when you prefer the BNGL language, want an ODE solution of the generated network, or need both network-based and network-free simulation from one input.
- Use [GillesPy2](gillespy2.md) for a reaction network with a few species, where you list the reactions yourself.
- Use [COPASI](copasi.md) for deterministic time courses, steady states and parameter fitting of a species-level model.

## Install it yourself

The project README lists three routes.

1. Download the Electron app from the nightly builds page (https://tools.kappalanguage.org/nightly-builds/). The command-line binaries are in its `resources/bin` folder.
2. Build from source with opam and dune. The README gives `opam install --deps-only .` followed by `dune build`.
3. Install the Python client with pip:

```bash
python3 -m venv kappa
. kappa/bin/activate
pip install kappy==4.1.2
```

The command resolves. PyPI lists kappy 4.1.2 with wheels for Linux x86_64 and macOS. Each wheel contains the compiled agents (`KaSimAgent`, `KaSaAgent`, `KappaSwitchman` and `KaMoHa`) in `kappy/bin`. The wheel does not ship the `KaSim` command-line program. The latest GitHub release is v4.1.3.1 (October 2024). The kappy wheels on PyPI are one release behind it.

There is also a browser version, which needs no install: https://tools.kappalanguage.org/try/.

The recipe below installs kappy 4.1.2 into a Python 3.12 image on linux/amd64, because the wheels exist for no other Linux architecture.

## Run the tested example

This recipe builds KaSim / KappaTools in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.1 s. KaSim / KappaTools has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [kasim-kappatools-recipe.tar.gz](https://biosimhub.pages.dev/guides/kasim-kappatools/kasim-kappatools-recipe.tar.gz) (Dockerfile, run_kappa.py, example model.ka, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf kasim-kappatools-recipe.tar.gz
   cd kasim-kappatools
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/kasim-kappatools:4.1.2 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/kasim-kappatools:4.1.2 python /opt/run_kappa.py /work/in/model.ka \
    --time 10 --period 0.1 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `plot.json` | 1.8 KB |
| `run_log.txt` | 28 B |

<details><summary>First lines of <code>plot.json</code></summary>

```
{"legend": ["[T]", "|A(x[.])|"], "series": [[10.0, 62.0], [9.9, 62.0], [9.8, 68.0], [9.700000000000001, 58.0], [9.600000000000001, 50.0], [9.5, 52.0], [9.4, 64.0], [9.3, 58.0], [9.200000000000001, 54.
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
kappy: 0 plot rows, seed 42
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--time` | Simulated time | 10 | 0.001 to 100000 |
| `--period` | Plot period | 0.1 | 0.0001 to 1000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the Kappy section of the project README: https://github.com/Kappa-Dev/KappaTools

```python
import kappy

model_text = "%agent: A(x)\nA(x[.]), A(x[.]) <-> A(x[1]), A(x[1]) @ 1e-2,1\n%plot: |A(x[.])|\n%init: 100 A()"

client = kappy.KappaStd()
client.add_model_string(model_text)
client.project_parse()
client.simulation_start(kappy.SimulationParameter(.1, "[T] > 10"))
client.wait_for_simulation_stop()
print(client.simulation_plot())
```

`SimulationParameter(plot_period, pause_condition)` takes the interval between recorded points and a Kappa boolean expression that stops the run. Here the run stops once the simulated time `[T]` passes 10. The call also accepts `seed=`, which makes a run repeatable. The recipe's `run_kappa.py` wraps these calls, takes the model as a file and sets the seed.

For the command-line program, the README gives `bin/KaSim kappa_file_1 ... kappa_file_n -l 100 -p 0.5 -o data_file`. This simulates 100 time units and writes a point every 0.5 time units, 200 points in all.

## Reading the output

The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

`simulation_plot()` returns the recorded observables. In the README example it is a list of `[time, value]` rows, newest first, one column per observable. The observable here is `|A(x[.])|`, the number of A agents whose site x is free. The README output ends with `[0.0, 100.0]` (all 100 agents free at time 0) and shows `[0.1, 62.0]` at the first plot step. These numbers come from that README, not from the recipe.

The recipe's helper writes two files:

- `plot.json` has the response exactly as kappy returned it.
- `observables.csv` has a `time` column plus one column per observable, sorted by time. The helper writes it only when the response has `legend` and `time_series` entries.

With 100 agents and these rates, the free count should fall from 100 and then fluctuate around a plateau. The fluctuations are real, because the counts are small. Run several seeds and compare.

## Pitfalls

- **Rates are per rule instance.** KaSim applies the rate to each way the left-hand side matches the current state. A bimolecular rule therefore slows as agents run out. Do not copy concentration-based rate constants from an ODE model without converting them.
- **The stop condition is an expression.** `"[T] > 10"` stops on simulated time. Use `"[E] > 100000"` to stop on event count instead, which is useful when time barely advances.
- **Time units are yours.** Kappa has no built-in unit. The unit is whatever your rates use.
- **Small models still need many runs.** A single trajectory is one sample. Report a mean and a spread over seeds.
- **Version lag.** The wheel (4.1.2) and the GitHub release (v4.1.3.1) differ. Check the web app or the Electron app if you need a newer behaviour.
- **Plot rows are newest first** in the README output. Sort by time before plotting.

## Further reading

- Project and README: https://github.com/Kappa-Dev/KappaTools
- Kappy API documentation: https://kasim.readthedocs.io/en/latest/kappy.html
- Kappa language site: https://kappalanguage.org
- Browser app: https://tools.kappalanguage.org/try/
- kappy on PyPI: https://pypi.org/project/kappy/
- Paper: Boutillier P et al. (2018) The Kappa platform for rule-based modeling. Bioinformatics 34:i583-i592. https://doi.org/10.1093/bioinformatics/bty272

---

Cite: Boutillier P et al. (2018). The Kappa platform for rule-based modeling. Bioinformatics 34:i583-i592. doi:10.1093/bioinformatics/bty272

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/kasim-kappatools).
