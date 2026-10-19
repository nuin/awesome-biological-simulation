# neurolib

> Simulate one whole-brain-model node, an AdEx mean-field excitatory and inhibitory population (ALNModel), and write its firing-rate time series.

Licence: MIT · [Source code](https://github.com/neurolib-dev/neurolib)

## What it simulates

neurolib simulates activity of the whole brain as a network of brain areas. Each area is one "neural mass": a model of the average firing of a whole population of neurons, not of single cells. Areas are coupled through a structural connectivity matrix (how strongly area i drives area j) and a delay matrix (how long the signal takes, from fibre length).

The main model is `ALNModel`. Each area holds an excitatory and an inhibitory population, described by a mean-field reduction of adaptive exponential integrate-and-fire (AdEx) neurons. Other models include a Fitzhugh-Nagumo oscillator (`FHNModel`) and a Wilson-Cowan model. Output is a firing-rate time series per area. With `bold=True` neurolib also runs a Balloon-Windkessel model and returns a simulated fMRI BOLD signal.

On top of the simulator sit three tools: parameter exploration over a grid (`BoxSearch`), evolutionary optimization to fit parameters to data (`Evolution`, with `adaptive` and `nsga2` algorithms), and an optimal control module that computes a stimulus to reach a target activity.

## When to use it

Use neurolib when you want to fit a network of brain areas to resting-state functional connectivity, or map how the dynamics of one area change with its inputs.

- Use NEST or Brian 2 when you need individual spiking neurons, not population averages.
- Use [Jaxley](jaxley.md) when you need detailed single-neuron biophysics with gradients.
- Use The Virtual Brain when you want a larger library of neural mass models and a GUI.

neurolib does not model dendrites, ion channels or single spikes. It is also a research code base: the last PyPI release is 0.6.2, and the GitHub releases page lists v0.7.0 from April 2024.

## Install

neurolib needs Python 3. The project README gives:

```
pip install neurolib
```

PyPI lists 0.6.2 as the current release (pure-Python wheel). The package pulls in numpy, scipy, numba, xarray, pandas, h5py, pypet, deap and jitcdde. It is not on conda-forge. The README also describes a source install: clone the repository, then `pip install -r requirements.txt` and `pip install .`. The source route includes the `examples/` notebooks and tests, which the wheel does not.

The licence is MIT.

## A first run

The README's single-node example runs one ALN area with a little noise and plots the rates. Adapted from the [neurolib README](https://github.com/neurolib-dev/neurolib#single-node):

```python
from neurolib.models.aln import ALNModel
import matplotlib.pyplot as plt

model = ALNModel()
model.params['sigma_ou'] = 0.1   # add some noise
model.run()

plt.plot(model.t, model.output.T)
plt.show()
```

The first `run()` compiles the integration loop with numba, so it takes longer than the next ones. `model.params['duration']` sets the length in ms (default 2000).

The same README shows the whole-brain step: load the bundled example data with `Dataset("gw")`, pass its `Cmat` and `Dmat` to `ALNModel`, set `duration` and call `model.run(bold=True)`. It warns that 80 regions for 5 minutes of model time can take several minutes of computing.

## Run the tested example

This recipe builds neurolib in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 4.6 s.

1. Download [neurolib-recipe.tar.gz](https://biosimhub.pages.dev/guides/neurolib/neurolib-recipe.tar.gz) (Dockerfile, run_neurolib.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf neurolib-recipe.tar.gz
   cd neurolib
   sh run.sh
   ```

![Terminal recording of the neurolib example run](https://biosimhub.pages.dev/media/neurolib/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/neurolib:0.6.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/neurolib:0.6.2 python /opt/run_neurolib.py --duration 2000 \
    --mue 0.5 --mui 0.5 --sigma-ou 0.1 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `rates.csv` | 1.4 MB |
| `rates.png` | 40.8 KB |
| `run_log.txt` | 114 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/neurolib/result-dark.png"><img src="https://biosimhub.pages.dev/media/neurolib/result.png" alt="Plot of the neurolib example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>rates.csv</code></summary>

```
time_ms,rate_exc_hz,rate_inh_hz
1.000000000000000056e-01,1.329234464205768074e+00,8.480320229474112637e+01
2.000000000000000111e-01,1.261223588589255096e+00,7.661354366615935874e+01
3.000000000000000444e-01,1.199793664903650470e+00,7.045098940359756057e+01
4.000000000000000222e-01,1.141654607849971859e+00,6.556570271082875934e+01
5.000000000000000000e-01,1.084718568494551283e+00,6.140287580140036283e+01
6.000000000000000888e-01,1.031006028580702116e+00,5.795025327614889221e+01
7.000000000000000666e-01,9.779852477497025243e-01,5.478342879578703162e+01
8.000000000000000444e-01,9.315671483233407546e-01,5.193185476817552626e+01
9.000000000000000222e-01,8.880421266167946026e-01,4.919055322618905990e+01
1.000000000000000000e+00,8.458351637783987353e-01,4.691207518517955322e+01
1.100000000000000089e+00,8.026900491324568954e-01,4.483277104495313381e+01
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 20000 samples, dt 0.1 ms, mean excitatory rate over the second half 1.583 Hz, mean inhibitory rate 3.105 Hz
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--duration` | Duration (ms) | 2000 | 100 to 20000 |
| `--mue` | Mean external input to the excitatory population (mV/ms) | 0.5 | 0 to 3 |
| `--mui` | Mean external input to the inhibitory population (mV/ms) | 0.5 | 0 to 3 |
| `--sigma-ou` | Noise strength (Ornstein-Uhlenbeck sigma) | 0.1 | 0 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

After `run()` the model object holds the results:

- `model.t` is the time axis in ms.
- `model.output` and `model.rates_exc` are the excitatory firing rates, one row per brain area. `rates_inh` holds the inhibitory rates. Rates are in Hz.
- With `bold=True`, `model.BOLD.BOLD` holds the simulated BOLD signal and `model.BOLD.t` its time axis.

To judge a network fit, the README computes a functional connectivity matrix from BOLD with `func.fc()` and correlates it with each subject's empirical matrix using `func.matrix_correlation()`. It states that a value above 0.5 is a good rule of thumb. In the README's output the mean correlation over the dataset's subjects is 0.58, with per-subject values from 0.34 to 0.72 (numbers from the README).

For an exploration, `search.loadResults()` fills `search.dfResults` and `search.results`, which you then reduce to a figure such as maximum firing rate over the two input axes.

## Pitfalls

- **Units.** Time is in ms and input means (`mue_ext_mean`, `mui_ext_mean`) are in mV/ms. Rates are in Hz.
- **First run is slow.** Numba compilation happens on the first call in each Python process.
- **Version drift.** PyPI is at 0.6.2 while GitHub has a newer v0.7.0 tag. `pip install neurolib` gives 0.6.2, so the source tree may show features the wheel lacks.
- **Reproducibility.** The default parameters call `np.random.seed(None)` when the model is built, which reseeds numpy. Pass `ALNModel(seed=42)` to fix noise and initial conditions.
- **Long runs.** Whole-brain BOLD runs scale with regions times duration. Start with a short `duration`.
- **Many dependencies.** The install pulls in numba, pypet, deap and jitcdde. Use a fresh virtual environment.

## Further reading

- Documentation: https://neurolib-dev.github.io/
- Gentle introduction: https://caglorithm.github.io/notebooks/neurolib-intro/
- Example notebooks: https://github.com/neurolib-dev/neurolib/tree/master/examples
- Source: https://github.com/neurolib-dev/neurolib
- Paper: Cakan C, Jajcay N, Obermayer K (2021). neurolib: A Simulation Framework for Whole-Brain Neural Mass Modeling. Cognitive Computation 15:1132-1152. https://doi.org/10.1007/s12559-021-09931-9

---

Cite: Cakan C, Jajcay N, Obermayer K (2021). neurolib: A Simulation Framework for Whole-Brain Neural Mass Modeling. Cognitive Computation 15:1132-1152. doi:10.1007/s12559-021-09931-9

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/neurolib).
