# The Virtual Brain (TVB)

> Simulate large-scale brain network dynamics, here a stochastic linear model on the bundled 76-region human connectome, and save the regional time series.

Licence: GPL-3.0-or-later · [Source code](https://github.com/the-virtual-brain/tvb-root)

## What it simulates

The Virtual Brain (TVB) simulates the activity of the whole brain as a network. Each node is a brain region. Each node runs a neural mass model, a few equations that describe the average activity of a population of neurons. The nodes are joined by a connectome: a matrix of connection strengths and a matrix of tract lengths, which together with a conduction speed give signal delays.

You choose a neural mass model (Generic 2D oscillator, Wilson-Cowan, Jansen-Rit, Reduced Wong-Wang, Epileptor and others), a coupling function, an integrator (deterministic or stochastic) and one or more monitors. Monitors turn the regional activity into the signals an experiment records: raw state variables, temporally averaged activity, EEG, MEG or the fMRI BOLD signal.

Time is in milliseconds. The default human connectivity ships with 76 regions.

TVB comes in two packages. `tvb-library` is the scientific library: a plain Python package that runs simulations and analyses and stores nothing. `tvb-framework` adds a database, a workflow manager and a web interface.

## When to use it

Use TVB to ask what a given anatomical network does dynamically: how structure shapes resting-state correlation, how a lesion or a changed coupling alters the rhythm, how a model of seizure spread behaves.

- Use [NGC-Learn](ngclearn.md) for small spiking circuits where the learning rule is the question.
- Use [Arbor](arbor.md) or [NetPyNE](netpyne.md) when single cells with dendrites matter more than whole-brain structure.
- Use [SimNIBS](simnibs.md) when the question is the electric field a stimulation coil or electrode produces in the head, not the neural dynamics.

## Install

The current release is 2.10.0 on PyPI and on conda-forge (checked with the PyPI JSON API and the anaconda.org API). The project README recommends a dedicated Python environment:

```
pip install tvb-library
pip install tvb-framework
```

`tvb-library` alone is enough for scripted simulations. Conda-forge also has `tvb-library` 2.10.0 (linux-64, osx-64, win-64, no ARM build) and a `tvb-data` 2.0 package with the example datasets:

```
micromamba create -n tvb -c conda-forge tvb-library=2.10.0 tvb-data=2.0
```

The README also offers a TVB_Distribution download that bundles Python, TVB and all dependencies. Unzip it and run `tvb_start`. To start the web interface from a pip install, run `python -m tvb.interfaces.web.run WEB_PROFILE`. It listens on port 8080.

## Run the tested example

This recipe builds The Virtual Brain (TVB) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 9.2 s. The Virtual Brain (TVB) has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [tvb-recipe.tar.gz](https://biosimhub.pages.dev/guides/tvb/tvb-recipe.tar.gz) (Dockerfile, run_tvb.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf tvb-recipe.tar.gz
   cd tvb
   sh run.sh
   ```

![Terminal recording of the The Virtual Brain (TVB) example run](https://biosimhub.pages.dev/media/tvb/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/tvb:2.10.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/tvb:2.10.0 python /opt/run_tvb.py --length-ms 10000 --coupling 0.0002 \
    --gamma -0.01 --speed 1 --noise 0.001 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 143 B |
| `summary.csv` | 6.4 KB |
| `timeseries.npz` | 640.3 KB |
| `timeseries.png` | 93.5 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/tvb/result-dark.png"><img src="https://biosimhub.pages.dev/media/tvb/result.png" alt="Plot of the The Virtual Brain (TVB) example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
2026-10-18 05:44:52,792 - WARNING - tvb.basic.readers - File 'hemispheres' not found in ZIP.
regions=76 samples=1000 length_ms=10000.0 seed=42
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
region,mean,std,min,max
rA1,-0.07178861737415124,0.38190291652283415,-1.126315729937588,0.9180093390404143
rA2,0.07012541229661419,0.30922515024543706,-0.9257975436783803,1.0717923190119867
rAMYG,-0.039415147706000915,0.34125901819103627,-0.9391970570778202,0.9699060764054065
rCCA,-0.012769694799919016,0.3725476996939286,-1.137038182271481,1.1103868736491966
rCCP,-0.12240400969096948,0.36090817150796173,-1.065721781535834,0.9267704572776618
rCCR,-0.05254335057873147,0.29702430680538316,-1.036304975324167,0.8278785408449428
rCCS,-0.06538733142162734,0.3448064462633734,-1.0780533468127627,0.863231589400466
rFEF,-0.05491091732590663,0.33976806967956635,-1.198527322105275,1.0036378408011448
rG,-0.007934556555956781,0.3133795492452216,-0.936422978375272,1.209286328659833
rHC,0.03349717850807467,0.3236519406236413,-0.960053080021449,1.0791238112985115
rIA,-0.04572785530880443,0.35277281405539973,-1.1542276805939904,1.0341707920705958
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--length-ms` | Simulated time (ms) | 10000 | 1000 to 60000 |
| `--coupling` | Linear coupling strength a | 0.0002 | 0 to 0.01 |
| `--gamma` | Decay rate gamma | -0.01 | -1 to -0.0001 |
| `--speed` | Conduction speed (mm/ms) | 1 | 0.1 to 100 |
| `--noise` | Additive noise intensity | 0.001 | 0 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

The example is a stochastic linear model on the default connectivity, from the TVB demo notebook "Exploring longer time series". A `Simulator` gets a connectivity, a coupling, an integrator, a model and a monitor. `configure()` checks and prepares it. `run()` returns one `(time, data)` pair per monitor.

```python
import numpy
from tvb.simulator.lab import *

connectivity = connectivity.Connectivity.from_file()
connectivity.speed = numpy.array([1.0])

sim = simulator.Simulator(
    connectivity=connectivity,
    coupling=coupling.Linear(a=numpy.array([2e-4])),
    integrator=integrators.EulerStochastic(dt=10.0),
    model=models.Linear(gamma=numpy.array([-1e-2])),
    monitors=(monitors.Raw(),),
    simulation_length=60e3,
).configure()

(time, data), = sim.run()
```

The notebook runs 60 seconds of simulated time and plots every region as a grey line. The recipe shortens that to 10 seconds.

Adapted from <https://docs.thevirtualbrain.org/demos/exploring_longer_time_series.ipynb>.

## Reading the output

`data` is a four-dimensional array with axes (time, state variable, region, mode). The linear model has one state variable and one mode, so `data[:, 0, :, 0]` is a time-by-region matrix. `time` is in milliseconds. With `monitors.Raw()` one sample is stored per integration step, so the step `dt=10.0` ms sets the sample spacing.

The recipe's driver script saves that matrix with the region labels (`timeseries.npz`), a per-region table of mean, standard deviation, minimum and maximum (`summary.csv`), and a plot of all region traces against time in seconds (`timeseries.png`).

With a negative `gamma` each region decays to zero and the noise keeps pushing it away, so every trace is a noisy fluctuation around zero. Coupling `a` mixes the regions: raise it and neighbouring regions' traces correlate more. TVB's own tools for longer series are `TimeSeriesRegion` (wrap the array with the connectivity) and `TimeSeriesInteractive` (a scrollable viewer).

## Pitfalls

- **Array parameters.** Model and coupling parameters are NumPy arrays, such as `numpy.array([2e-4])`. A bare float is rejected or misread. Region-specific values are arrays with one entry per region.
- **Units.** Time is milliseconds and conduction speed is mm/ms. The tract lengths in the default connectivity are millimetres.
- **Four-dimensional output.** Index state variable and mode explicitly. Forgetting `[:, 0, :, 0]` gives a shape that no 2D plot accepts.
- **Data package.** `Connectivity.from_file()` with no argument reads the 76-region demo connectome from the `tvb-data` package. Install it or point `from_file` at your own zip.
- **Where the library keeps files.** TVB keeps a working folder for logs and temporary files. In a read-only container, set `TVB_STORAGE` to a writable path.
- **Licence field.** The repository's LICENSE file states GPL version 3 or any later version. Some catalogues list a different licence.

## Further reading

- Documentation: https://docs.thevirtualbrain.org/
- Python demos (notebooks): https://docs.thevirtualbrain.org/demos/Demos.html
- Source: https://github.com/the-virtual-brain/tvb-root
- Paper: Sanz Leon P et al. (2013). The Virtual Brain: a simulator of primate brain network dynamics. Frontiers in Neuroinformatics 7:10. https://doi.org/10.3389/fninf.2013.00010

---

Cite: Sanz Leon P, Knock SA, Woodman MM, Domide L, Mersmann J, McIntosh AR, Jirsa V (2013). The Virtual Brain: a simulator of primate brain network dynamics. Frontiers in Neuroinformatics 7:10. doi:10.3389/fninf.2013.00010

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/tvb).
