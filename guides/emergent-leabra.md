# Emergent / Leabra

> Build and run biologically based neural network models of cognition in Go, using the Leabra algorithm and a Cogent Core graphical interface.

Licence: BSD-3-Clause · [Source code](https://github.com/emer/emergent)

## What it simulates

Emergent is a Go toolkit for neural network models of the brain and mind. It defines the structure of a network (layers, pathways, neurons, synapses), the environments that present patterns to it, parameter styling, logging and a 3D network viewer. The learning and activation code comes from algorithm packages built on top of it.

The best known is Leabra: Local, Error-driven and Associative, Biologically Realistic Algorithm. It uses point neurons with inhibitory competition (k-winners-take-all) and balances error-driven learning with Hebbian learning. A newer package, axon, implements biologically detailed spiking networks, and the README says it can use the GPU. The textbook Computational Cognitive Neuroscience ships 26 Leabra simulations that students run for teaching.

## When to use it

Use Emergent and Leabra to study learning, memory and cognition with models that follow the textbook, or to teach with the textbook's simulations.

- Use Brian 2 or NEST for spiking networks where you want to specify membrane equations and compare with spiking data.
- Use PyTorch-style tools for abstract deep networks. The project's eTorch package lets the Emergent viewer show PyTorch networks.
- Use [PyNN](pynn.md) for a simulator-independent description of spiking networks.

The README says branches differ: `main` is the in-development v2 on Cogent Lab, `leabra` works with the current Leabra and teaching simulations, and `v1` is the old GoKi-based version.

## Install

Emergent is a Go module, `github.com/emer/emergent/v2`. Its `go.mod` asks for Go 1.25.6 and depends on Cogent Core and Cogent Lab. The latest tag is `v2.0.0-dev0.1.14`, a development version. An older v1 line has tag v1.3.44 (February 2023).

There is no pip or conda package. The README sends you to the Cogent Core install instructions (https://cogentcore.org/core/install) and says that once they are done, `core run [platform]` runs a simulation, where the platform can be your local system, `android`, `ios` or `web`. The Leabra repository is at https://github.com/emer/leabra, and the textbook simulations at https://github.com/CompCogNeuro/sims.

Emergent is documented as a guide only on this site. Its models build as a desktop or web application with a graphical interface, and they need the Go toolchain and the Cogent Core platform packages on the machine. The licence is BSD-3-Clause.

## A first run

The Leabra `ra25` example, a Random Associator with 25 patterns, is the template project. Adapted from the [ra25 README](https://github.com/emer/leabra/blob/main/examples/ra25/README.md): install the Cogent Core prerequisites, clone the Leabra repository, go into `examples/ra25` and run

```
core run
```

The window has a toolbar, a set of `Sim` fields on the left, and tabs on the right with the network view and log plots. The README suggests turning off the `ViewOn` flag or switching to a graph tab to speed up training.

To run without the interface, the README says to build the program and pass any argument, for example

```
./ra25 -help
```

and that passing any argument runs the model without the GUI, saving log files and, optionally, final weights files for each run.

## Reading the output

In the GUI the output is plots and tables:

- The training plots show error and percent correct per epoch. The README's parameter-search recipe uses `FirstZero`, the epoch at which the network first reached zero errors, as the measure of learning speed.
- `RunStats` is a table of summary statistics over multiple runs, such as the mean `FirstZero` epoch and the mean `PctCor` over the last 10 epochs.
- The test buttons run the network on the patterns without changing training. `TstTrlPlot` shows performance on each item, and `TstTrlLog` shows the input and output activations.

The README's exercise compares the `Base` parameter set with a `NoMomentum` set. After 10 runs each, `Base` is slightly faster, the README says. In headless mode the same logs go to files.

## Pitfalls

- **Branch mix-ups.** Use the same branch for emergent and leabra. The README separates `main`, `leabra` and `v1`.
- **Moving target.** The `main` branch is in active development and tags carry the `dev` label.
- **Go version.** The module requires a recent Go. Older toolchains refuse to build it.
- **GUI dependencies.** Cogent Core needs platform graphics libraries. See its install page for your system.
- **Slow viewing.** Updating the network view each step slows training a lot.
- **Documentation age.** The README says the wiki can be out of date and suggests reading the source.

## Further reading

- Project page: https://emersim.org
- Emergent: https://github.com/emer/emergent
- Leabra: https://github.com/emer/leabra
- Textbook and simulations: https://compcogneuro.org, https://github.com/CompCogNeuro/sims
- axon: https://github.com/emer/axon
- Paper: Aisa B, Mingus B, O'Reilly R (2008). The Emergent neural modeling system. Neural Networks 21(8):1146-1152. https://doi.org/10.1016/j.neunet.2008.06.016

---

Cite: Aisa B, Mingus B, O'Reilly R (2008). The Emergent neural modeling system. Neural Networks 21(8):1146-1152. doi:10.1016/j.neunet.2008.06.016

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/emergent-leabra).
