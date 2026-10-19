# PyNN

> Describe a spiking network once in PyNN and run it; this run uses the Brian 2 back end to drive integrate-and-fire cells with DC currents and record membrane potentials and spikes.

Licence: CECILL-2.1 · [Source code](https://github.com/NeuralEnsemble/PyNN)

## What it simulates

PyNN is a Python interface for describing spiking neural networks. You write the model once: populations of neurons, projections (synapse sets) between them, stimuli and recordings. PyNN then hands the model to a simulator back end. It does not integrate equations itself.

The back ends named in the project documentation are NEURON, NEST, Brian 2 and Arbor, plus some neuromorphic hardware systems. PyNN supplies standard cell and synapse models (for example `IF_curr_exp`, `IF_cond_exp`, `HH_cond_exp`, `EIF_cond_exp_isfa_ista`) that the project says were verified to give the same behaviour on the different back ends. It also supplies connectivity algorithms (all-to-all, random, distance-dependent, small-world) and records data in the Neo format.

## When to use it

Use PyNN when you want a network model that can run on more than one simulator, or when you want to move an existing model to a different back end with few edits.

- Use NEST directly for the largest point-neuron networks and access to every NEST model.
- Use Brian 2 directly when you want to write your own equations as strings.
- Use NEURON directly for detailed morphologies and custom mechanisms.
- Use [neurolib](neurolib.md) when the unit of the model is a brain area, not a neuron.

PyNN adds a layer. Features that exist in only one simulator may be out of reach through the common API, though the documentation says native cell types can be used with a given back end.

## Install

PyNN 0.13.0 is the current release on PyPI (requires Python 3.10 or newer; wheel `pynn-0.13.0-py3-none-any.whl`). The installation page gives:

```
pip install PyNN
```

PyNN depends on numpy, lazyarray and Neo. You also need at least one simulator. The package declares extras for them: `PyNN[brian2]`, `PyNN[neuron]`, `PyNN[arbor]`, `PyNN[nestml]` and `PyNN[plotting]`. NEST is not a pip extra; the installation page points to the NEST site (it lists NEST 3.4 to 3.7 as working). NEURON installs with `pip install neuron` and Brian 2 with `pip install brian2`. The NEURON back end compiles NMODL files the first time it is imported, so it needs a C compiler.

The licence is CeCILL-2.1, which the PyNN introduction describes as equivalent to and compatible with the GPL. The GitHub release list ends at 0.12.1, while PyPI and `pyproject.toml` are at 0.13.0.

## A first run

The `examples/current_injection.py` script injects four current waveforms into four integrate-and-fire cells. Adapted from [examples/current_injection.py](https://github.com/NeuralEnsemble/PyNN/blob/master/examples/current_injection.py), shortened to one cell type and a DC source:

```python
import pyNN.brian2 as sim      # or pyNN.nest, pyNN.neuron

sim.setup()
cells = sim.Population(4, sim.IF_curr_exp(v_thresh=-55.0, tau_refrac=5.0, tau_m=10.0))
for cell in cells:
    cell.inject(sim.DCSource(amplitude=0.5, start=50.0, stop=400.0))
cells.record("v")
sim.run(500.0)
vm = cells.get_data().segments[0].filter(name="v")[0]
sim.end()
```

The original script takes the back end as its first argument, so `python current_injection.py --plot-figure brian2` runs the same code on Brian 2. The back end name is the module name under `pyNN`.

## Run the tested example

This recipe builds PyNN in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 5.3 s.

1. Download [pynn-recipe.tar.gz](https://biosimhub.pages.dev/guides/pynn/pynn-recipe.tar.gz) (Dockerfile, run_pynn.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pynn-recipe.tar.gz
   cd pynn
   sh run.sh
   ```

![Terminal recording of the PyNN example run](https://biosimhub.pages.dev/media/pynn/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pynn:0.13.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pynn:0.13.0 python /opt/run_pynn.py --cells 4 --amplitude 0.5 \
    --duration 500 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 54 B |
| `spikes.csv` | 13 B |
| `vm.csv` | 630.1 KB |
| `vm.png` | 34.5 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/pynn/result-dark.png"><img src="https://biosimhub.pages.dev/media/pynn/result.png" alt="Plot of the PyNN example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 4 cells, 500.0 ms, spikes per cell [0, 0, 0, 0]
```

</details>

<details><summary>First lines of <code>spikes.csv</code></summary>

```
cell,time_ms
```

</details>

<details><summary>First lines of <code>vm.csv</code></summary>

```
time_ms,v_cell0_mV,v_cell1_mV,v_cell2_mV,v_cell3_mV
0.000000000000000000e+00,-6.500000000000000000e+01,-6.500000000000000000e+01,-6.500000000000000000e+01,-6.500000000000000000e+01
1.000000000000000056e-01,-6.499999999999998579e+01,-6.499999999999998579e+01,-6.499999999999998579e+01,-6.499999999999998579e+01
2.000000000000000111e-01,-6.499999999999997158e+01,-6.499999999999997158e+01,-6.499999999999997158e+01,-6.499999999999997158e+01
2.999999999999999889e-01,-6.499999999999995737e+01,-6.499999999999995737e+01,-6.499999999999995737e+01,-6.499999999999995737e+01
4.000000000000000222e-01,-6.499999999999994316e+01,-6.499999999999994316e+01,-6.499999999999994316e+01,-6.499999999999994316e+01
5.000000000000000000e-01,-6.499999999999992895e+01,-6.499999999999992895e+01,-6.499999999999992895e+01,-6.499999999999992895e+01
5.999999999999999778e-01,-6.499999999999991473e+01,-6.499999999999991473e+01,-6.499999999999991473e+01,-6.499999999999991473e+01
6.999999999999999556e-01,-6.499999999999990052e+01,-6.499999999999990052e+01,-6.499999999999990052e+01,-6.499999999999990052e+01
8.000000000000000444e-01,-6.499999999999988631e+01,-6.499999999999988631e+01,-6.499999999999988631e+01,-6.4999999999
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--cells` | Cells | 4 | 1 to 50 |
| `--amplitude` | Largest DC amplitude (nA) | 0.5 | 0 to 2 |
| `--duration` | Duration (ms) | 500 | 100 to 5000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`cells.get_data()` returns a Neo `Block`. Its first segment holds the recordings of the first run:

- `segments[0].filter(name="v")[0]` is an analog signal of membrane potential in mV, one column per cell, with a `times` axis in ms.
- `segments[0].spiketrains` lists one spike train per cell, in ms. Record spikes with `cells.record("spikes")`.
- `sim.record(...)` with a file name writes the same data to disk. The script above saves a pickle under `Results/`.

With `--plot-figure` the script also saves a PNG of the membrane potentials. A cell driven by a larger current crosses `v_thresh` sooner and fires more often. A cell with no spike shows a charge curve toward a plateau below threshold.

## Pitfalls

- **Times are in ms and currents in nA.** Cell parameters use PyNN units, not each simulator's units.
- **The back end is an import.** You choose it with `import pyNN.<name> as sim`. Keep that one line as the only simulator-specific import to keep the script portable.
- **Seeds.** Pass an explicit `NumpyRNG(seed=...)` to connectors and random distributions. Back ends also have their own random streams.
- **NEURON compile step.** The first import compiles mechanisms and fails without a compiler.
- **Back-end versions.** The installation page lists the NEST releases it works with (3.4 to 3.7). Check the page before pairing PyNN with a newer NEST.
- **Brian 2 code generation.** Brian 2 compiles generated code by default. On a machine without a compiler, set `brian2.prefs.codegen.target = "numpy"` before running.

## Further reading

- Documentation: https://neuralensemble.org/docs/PyNN/
- Installation: https://neuralensemble.org/docs/PyNN/installation.html
- Examples: https://neuralensemble.org/docs/PyNN/examples.html
- Source: https://github.com/NeuralEnsemble/PyNN
- Paper: Davison AP, Bruderle D, Eppler JM, Kremkow J, Muller E, Pecevski DA, Perrinet L, Yger P (2009). PyNN: a common interface for neuronal network simulators. Frontiers in Neuroinformatics 2:11. https://doi.org/10.3389/neuro.11.011.2008

---

Cite: Davison AP, Bruderle D, Eppler JM, Kremkow J, Muller E, Pecevski DA, Perrinet L, Yger P (2009). PyNN: a common interface for neuronal network simulators. Front Neuroinform 2:11. doi:10.3389/neuro.11.011.2008

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pynn).
