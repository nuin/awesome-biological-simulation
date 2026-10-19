# PyLEMS

> Run a LEMS (Low Entropy Model Specification) model file, such as an ODE-based neuron or synapse model, and write its output files.

Licence: LGPL-3.0-only · [Source code](https://github.com/LEMS/pylems)

## What it simulates

PyLEMS runs models written in LEMS, the Low Entropy Model Specification. LEMS is a declarative XML language for models built from physical quantities with dimensions and units. NeuroML2 neuron and synapse models are written in it.

A LEMS file has two layers. A `ComponentType` defines state variables, parameters and equations, much like a class. A `Component` gives one instance its parameter values. The `Simulation` says which component to run, for how long and what to record. PyLEMS builds the objects, integrates the equations and writes the recorded values to files.

The example is a cell whose voltage relaxes to a resting value: `dv/dt = (vrest - v) / tau`. It starts at -40 mV, rests at -70 mV and has tau = 20 ms. The LEMS documentation shows the same format for integrate-and-fire cells and bi-exponential synapses.

The key assumptions are fixed-step integration and the units in the file. In the output, voltages are in volts and times in seconds, whatever units the file uses.

## When to use it

- You have a LEMS or NeuroML2 model and want a quick run without Java or a GUI.
- You want to check what a LEMS file does before sending it to a larger simulator.
- You teach model description languages and want a short example that runs in a second.

PyLEMS handles part of the language only. Its README lists examples that do not run (NeuroML examples 4, 12 and 14, and LEMS examples 4 and 5) and elements it does not support (KSChannel, Property, PathParameter and Assertions). For those models, use jLEMS or a NeuroML tool. [XPPAUT](xppaut.md) fits when you write the ODEs directly and want phase-plane work. [GillesPy2](gillespy2.md) fits when copy numbers are small and noise matters.

## Install it yourself

Pinned to 0.6.8. The conda-forge package is `pylems`:

```
micromamba create -n lems -c conda-forge pylems=0.6.8
micromamba activate lems
```

The project also documents `pip install pylems`.

The command line, as printed by `pylems -h` in the 0.6.8 container:

```
pylems [-h] [-I <Include directory>] [-nogui] [-dlems] <LEMS file>
```

`-nogui` parses and simulates without plots. `-I` adds a directory to search for included files. `-dlems` exports the model as distilled LEMS in JSON.

Minimal run:

```
pylems -nogui decay.xml
```

Without `-nogui`, PyLEMS tries to open plot windows.

## Run the tested example

This recipe builds PyLEMS in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.3 s.

1. Download [pylems-recipe.tar.gz](https://biosimhub.pages.dev/guides/pylems/pylems-recipe.tar.gz) (Dockerfile, example model.xml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pylems-recipe.tar.gz
   cd pylems
   sh run.sh
   ```

![Terminal recording of the PyLEMS example run](https://biosimhub.pages.dev/media/pylems/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pylems:0.6.8 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pylems:0.6.8 pylems -nogui /work/in/model.xml > out/pylems_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `decay.dat` | 89.4 KB |
| `pylems_log.txt` | 157 B |

<details><summary>First lines of <code>decay.dat</code></summary>

```
0   -0.04015   
0.0001   -0.040299249999999995   
0.0002   -0.040447753749999996   
0.00030000000000000003   -0.04059551498125   
0.0004   -0.040742537406343746   
0.0005   -0.040888824719312024   
0.0006000000000000001   -0.041034380595715465   
0.0007000000000000001   -0.04117920869273689   
0.0008000000000000001   -0.041323312649273206   
0.0009000000000000002   -0.04146669608602684   
0.0010000000000000002   -0.04160936260559671   
0.0011000000000000003   -0.04175131579256872   
```

</details>

<details><summary>First lines of <code>pylems_log.txt</code></summary>

```
Parsing and resolving model: /work/in/model.xml
Building simulation
Running simulation
Processing results
Going to save 2001x1 data points to file decay.dat
```

</details>


## Reading the output

The example file `decay.xml` is a complete LEMS model. It declares dimensions (`time`, `voltage`) and units (`s`, `ms`, `V`, `mV`). It defines `OutputColumn`, `OutputFile` and `Simulation` types, plus the `decayCell` type with the equation above. Then it creates one `decayCell` with `tau="20ms" v0="-40mV" vrest="-70mV"` and a simulation of 200 ms with a 0.1 ms step. The `Target` line names the simulation to run.

The recipe's container runs `pylems -nogui` with no helper script.

- `pylems_log.txt` (157 bytes): five lines: `Parsing and resolving model`, `Building simulation`, `Running simulation`, `Processing results`, then `Going to save 2001x1 data points to file decay.dat`.
- `decay.dat` (91,583 bytes): 2,001 lines of two columns, time in seconds and voltage in volts. The first line is `0   -0.04015`.

The first line shows the step rule. The value -0.04015 V is -40 mV plus one step of (-70 - -40) / 20 ms x 0.1 ms = -0.15 mV. So each row holds the voltage after the step that starts at its time stamp. The integration is forward Euler by that arithmetic. The last row, at 0.2 s, is -0.0699987 V, within 0.002 mV of the rest value.

## Your own runs

Each run used the recipe's image and command with a changed model file.

- **Slower cell, different rest** (`tau="50ms"`, `vrest="-65mV"`). The log and file are the same size (2,001 rows). The first row is -0.04005 V, because the first step is smaller. The last row is -0.0645449 V. The analytic answer after 200 ms is -64.542 mV, so the difference is 0.003 mV.

- **Coarser step** (`step="5ms"`, original tau and rest). The log reports `40x1 data points`, and `decay.dat` has 40 rows. The first row is -0.0475 V, which is -40 mV minus 7.5 mV in one step. The 5 ms file's row stamped 0.02 s is -62.88 mV for the step that ends at 25 ms, where the analytic value is -61.40 mV. The error is 1.5 mV. The 0.1 ms file's row stamped 0.02 s is -59.05 mV at 20.1 ms, against -59.02 mV analytic, an error of 0.03 mV.

- **Your own model.** Copy a NeuroML2 example or write a `ComponentType` of your own. Keep the `Simulation` block and `Target`, change `length`, `step` and the output file name, and check that the log reports the number of rows you expect.

## Pitfalls

- **Output units are SI.** A 20 ms constant becomes 0.02, and -70 mV becomes -0.07. Multiply by 1000 before comparing with mV values in a paper.
- **The first row is already one step in.** Row 1 at t = 0 holds the voltage after the first step. The initial value is missing, so add it yourself if you plot from the file.
- **Step size sets accuracy.** Forward Euler with a 5 ms step against a 20 ms time constant gave a 1.5 mV error in the example. As a rule of thumb, use steps of at most tau / 100.
- **Missing `-nogui`.** Without it, PyLEMS shows plots, per its help text. Add the flag in scripts and containers.
- **Unsupported elements.** A model with KSChannel or Assertions will not run. Check the PyLEMS README list before debugging your file.

## Further reading

- PyLEMS source and README: https://github.com/LEMS/pylems
- PyLEMS API documentation: https://pylems.readthedocs.io/en/latest/
- LEMS documentation: https://lems.github.io/LEMS/
- Paper: Vella M et al. (2014), Front Neuroinform 8:38, https://doi.org/10.3389/fninf.2014.00038

---

Cite: Vella M, Cannon RC, Crook S, Davison AP, Ganapathy G, Robinson HPC, Silver RA, Gleeson P (2014). libNeuroML and PyLEMS: using Python to combine procedural and declarative modeling approaches in computational neuroscience. Front Neuroinform 8:38. doi:10.3389/fninf.2014.00038

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pylems).
