# NeuroML2 / pyNeuroML / LEMS

> Run a NeuroML2 model described in LEMS (a single-compartment Hodgkin-Huxley cell with a current pulse) with pyNeuroML and the bundled jNeuroML simulator.

Licence: LGPL-3.0 · [Source code](https://github.com/NeuroML/pyNeuroML)

## What it simulates

NeuroML2 is an XML standard for models of neurons, ion channels, synapses and networks. LEMS (Low Entropy Model Specification) is the underlying language that defines the model types and the simulation: which component to run, for how long, and what to record. pyNeuroML is one Python package that reads, writes, runs and analyses these files. It builds on libNeuroML and PyLEMS, and it bundles the jNeuroML Java application.

What it can do with a LEMS file:

- Run it with jNeuroML (the default), or with PyLEMS.
- Export it to simulator code for NEURON, NEST, Brian 2 and NetPyNE, and run that.
- Plot cell morphologies, voltage traces and channel kinetics, and analyse ion channels.

The biosimhub recipe runs the single-compartment Hodgkin-Huxley example from the pyNeuroML repository (`LEMS_NML2_Ex5_DetCell.xml`). A cell with sodium, potassium and leak channels receives a 0.08 nA current pulse from 100 ms for 100 ms. The simulation records the membrane voltage and the gating variables m, h and n. Parameters are the simulated time and the time step. Everything else lives in the XML files, which you can replace.

Key assumptions come from the model files: fixed-step integration, units as written in the NeuroML, and one cell in one population.

## When to use it

Use pyNeuroML when a model is already in NeuroML2, or when you want one description that several simulators can run. It suits shared channel and cell models, and checking that exports give the same behaviour in different engines.

Alternatives:

- [PyLEMS](pylems.md) is the pure Python LEMS interpreter that pyNeuroML can call. It has no Java dependency.
- NEURON, NEST and Brian 2 are the simulators that pyNeuroML exports to. Write the model for one of them directly when you do not need portability.
- [XPPAUT](xppaut.md) fits a small set of differential equations when you need bifurcation analysis rather than a described cell.

## Install it yourself

PyPI, pinned to version 1.3.22 (released 2 June 2026). The wheel is pure Python. The README lists a Java runtime, Graphviz `dot` and lxml as dependencies.

```bash
python3 -m venv nml && . nml/bin/activate
pip install pyneuroml==1.3.22
pynml -h
```

On Ubuntu, the README installs the system packages with `sudo apt-get install python-lxml graphviz openjdk-11-jdk`. Extras such as `pyneuroml[neuron]`, `pyneuroml[brian]` and `pyneuroml[netpyne]` pull in other backends. pyNeuroML is not on conda-forge or Bioconda, so the biosimhub image uses a Python base image with a headless Java runtime.

## A first run

Adapted from the pyNeuroML README (https://github.com/NeuroML/pyNeuroML) and the example folder (https://github.com/NeuroML/pyNeuroML/tree/master/examples).

Get `LEMS_NML2_Ex5_DetCell.xml` and the four NeuroML files it includes from the example folder: `NML2_SingleCompHHCell.nml`, `NaConductance.channel.nml`, `KConductance.channel.nml` and `LeakConductance.channel.nml`. Keep them in one folder and run:

```bash
pynml LEMS_NML2_Ex5_DetCell.xml -nogui
```

`-nogui` skips the plot windows. Without it, the four `Display` elements in the LEMS file open as plots. The `Simulation` element sets `length="300ms"` and `step="0.01ms"`; edit them to change the run.

In the recipe's copy of the example the files are renamed `lems.xml`, `cell.nml`, `na.nml`, `k.nml` and `leak.nml`, and the `Include` and `include href` lines match. A driver script copies them to a writable folder, sets the length and step, and removes the `results/` prefix from the output file names.

## Run the tested example

This recipe builds NeuroML2 / pyNeuroML / LEMS in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3 s.

1. Download [pyneuroml-recipe.tar.gz](https://biosimhub.pages.dev/guides/pyneuroml/pyneuroml-recipe.tar.gz) (Dockerfile, run_pynml.py, example lems.xml, cell.nml, na.nml, k.nml, leak.nml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pyneuroml-recipe.tar.gz
   cd pyneuroml
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pyneuroml:1.3.22 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pyneuroml:1.3.22 python /opt/run_pynml.py --length-ms 300 --step-ms 0.01 /work/in/lems.xml /work/in/cell.nml /work/in/na.nml /work/in/k.nml /work/in/leak.nml > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cell.nml` | 2.3 KB |
| `ex5_v.dat` | 625.0 KB |
| `ex5_vars.dat` | 1.2 MB |
| `k.nml` | 2.1 KB |
| `leak.nml` | 561 B |
| `lems.xml` | 3.3 KB |
| `na.nml` | 2.4 KB |
| `report.txt` | 220 B |
| `run_log.txt` | 22 B |

<details><summary>First lines of <code>cell.nml</code></summary>

```
<?xml version="1.0" encoding="UTF-8"?>

<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta4.xsd"
         id="NML2_SingleCompHHCell">

    <!-- Single compartment cell with HH channels -->
     
    <!-- This is a "pure" NeuroML 2 file. It can be included in a LEMS file for use in a simulaton 
    by the LEMS interpreter, see LEMS_NML2_Ex5_DetCell.xml -->    
    
```

</details>

<details><summary>First lines of <code>ex5_v.dat</code></summary>

```
0.0	-0.065	
1.0E-5	-0.0649997	
2.0E-5	-0.064999394	
3.0E-5	-0.064999096	
4.0E-5	-0.0649988	
5.0E-5	-0.06499851	
6.0E-5	-0.06499821	
7.0E-5	-0.06499792	
8.0E-5	-0.06499763	
9.0E-5	-0.064997345	
1.0E-4	-0.064997055	
1.1E-4	-0.06499677	
```

</details>

<details><summary>First lines of <code>ex5_vars.dat</code></summary>

```
0.0	0.052932486	0.5961208	0.3176769	
1.0E-5	0.052932486	0.5961208	0.3176769	
2.0E-5	0.052932486	0.5961208	0.3176769	
3.0E-5	0.052932486	0.5961208	0.3176769	
4.0E-5	0.052932564	0.5961207	0.31767693	
5.0E-5	0.05293272	0.5961207	0.31767693	
6.0E-5	0.052932948	0.59612066	0.31767696	
7.0E-5	0.052933246	0.59612066	0.317677	
8.0E-5	0.052933607	0.5961206	0.31767705	
9.0E-5	0.052934032	0.5961205	0.31767708	
1.0E-4	0.052934516	0.5961204	0.31767714	
1.1E-4	0.052935056	0.5961203	0.3176772	
```

</details>

<details><summary>First lines of <code>k.nml</code></summary>

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta4.xsd" 
         id="KConductance">

    <notes>Channel file containing a single channel description</notes>

    <ionChannel id="KConductance" conductance="10pS" type="ionChannelHH" species="k">

        <notes>HH K Channel</notes>
                
```

</details>

<details><summary>First lines of <code>leak.nml</code></summary>

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta4.xsd" 
         id="LeakConductance">

    <notes>Channel file containing a single Channel description</notes>

    <ionChannelHH id="LeakConductance" conductance="10pS">
        <notes>Leak conductance</notes>
    </ionChannelHH>

```

</details>

<details><summary>First lines of <code>lems.xml</code></summary>

```
<Lems>

    <!-- Example with Simple cell specifying segment details-->

    <!-- This is a file which can be read and executed by the LEMS Interpreter.
         It imports the LEMS definitions of the core NeuroML 2 Components, 
         imports in "pure" NeuroML 2 and contains some LEMS elements for running 
         a simulation -->


    <Target component="sim1" reportFile="report.txt"/>

```

</details>

<details><summary>First lines of <code>na.nml</code></summary>

```
<?xml version="1.0" encoding="ISO-8859-1"?>
<neuroml xmlns="http://www.neuroml.org/schema/neuroml2" 
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" 
         xsi:schemaLocation="http://www.neuroml.org/schema/neuroml2 https://raw.github.com/NeuroML/NeuroML2/development/Schemas/NeuroML2/NeuroML_v2beta4.xsd" 
         id="NaConductance">

    <notes>Channel file containing a single Channel description</notes>

    <ionChannel id="NaConductance" conductance="10pS" type="ionChannelHH" species="na">

        <notes>HH Na Channel</notes>
                
```

</details>

<details><summary>First lines of <code>report.txt</code></summary>

```
# Report of running simulation with jLEMS v0.12.0
Simulator=jLEMS
SimulatorVersion=0.12.0
SimulationFile=/work/out/lems.xml
StartTime=2026-10-18 05:27:03
SetupTime=0.567
RealSimulationTime=0.925
SimulationSaveTime=0.003
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
pynml lems.xml -nogui
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--length-ms` | Simulated time (ms) | 300 | 10 to 5000 |
| `--step-ms` | Time step (ms) | 0.01 | 0.001 to 0.1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The LEMS file declares two output files:

- `ex5_v.dat`: the membrane voltage of `hhpop[0]`. The first column is time, the second is voltage. Values are in SI units: seconds and volts.
- `ex5_vars.dat`: time, then the sodium activation `m`, the sodium inactivation `h` and the potassium activation `n`.
- `report.txt`: the run report named in the LEMS `Target` element.
- `run_log.txt`: the standard output of `pynml`.

The example plots a `spiking` trace next to the voltage, so the pulse is meant to make the cell fire. In a Hodgkin-Huxley cell the sodium gate m rises fast at a spike, while h and n change more slowly. Plot the columns against time to check; no spike counts are quoted here.

## Pitfalls

- **Java is required.** Without a Java runtime, `pynml` cannot run the bundled jNeuroML jar.
- **Include paths are relative.** The LEMS `Include file` and the NeuroML `include href` names must match the actual file names. A renamed file breaks the model.
- **Output files go next to the LEMS file.** In a read-only folder the run fails; copy the files to a writable folder first.
- **The `Display` elements need a screen.** Use `-nogui` on servers.
- **Units in the file.** Quantities with units (for example `0.08nA`, `300ms`) are converted to SI internally; always include the unit.

## Further reading

- Repository and README: https://github.com/NeuroML/pyNeuroML
- pyNeuroML documentation: https://pyneuroml.readthedocs.io/en/development/
- NeuroML documentation: https://docs.neuroml.org/
- Vella M, Cannon RC, Crook S, et al. (2014). libNeuroML and PyLEMS: using Python to combine procedural and declarative modeling approaches in computational neuroscience. Frontiers in Neuroinformatics 8:38. https://doi.org/10.3389/fninf.2014.00038
- Cannon RC, et al. (2014). LEMS: a language for expressing complex biological models in concise and hierarchical form and its use in underpinning NeuroML 2. Frontiers in Neuroinformatics 8:79. https://doi.org/10.3389/fninf.2014.00079
- Gleeson P, et al. (2010). NeuroML: a language for describing data driven models of neurons and networks with a high degree of biological detail. PLoS Computational Biology 6(6):e1000815. https://doi.org/10.1371/journal.pcbi.1000815

---

Cite: Vella M, Cannon RC, Crook S, et al. (2014). libNeuroML and PyLEMS, using Python to combine procedural and declarative modeling approaches in computational neuroscience. Frontiers in Neuroinformatics 8:38. doi:10.3389/fninf.2014.00038

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pyneuroml).
