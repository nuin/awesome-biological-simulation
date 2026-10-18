# Simbrain

> A visual desktop program for building, running and analysing neural networks (rate and spiking) and embodied agents in simulated worlds, for teaching and exploration.

Licence: GPL-2.0-or-later · [Source code](https://github.com/simbrain/simbrain)

## What it simulates

Simbrain is a free, open-source tool for building, running and analysing neural networks. You work on screen. A workspace holds windows: a network editor, plots, simulated worlds and tables. You draw neurons and synapses, set their rules, and press play.

Neurons can follow rate rules (linear, sigmoidal, decay, Hopfield-style) or spiking rules (integrate-and-fire, Izhikevich, FitzHugh-Nagumo, Morris-Lecar, adaptive exponential). Synapses can be static or learn through Hebbian, Oja or STDP rules. Ready-made network types include feed-forward networks trained by backpropagation, competitive networks, Hopfield networks, restricted Boltzmann machines, self-organising maps, simple recurrent networks and a convolutional network.

Couplings link a network to other components. A network can drive an agent in an object-world, read from a data table, or feed a plot. The worlds include an odor world, a 3D world, a text world and an image world. This lets you embody a network and watch how it behaves.

Simbrain is built in Kotlin and Java. The current default branch is Simbrain 4; the older Simbrain 3 lives on its own branch.

## When to use it

Use Simbrain for teaching and for exploratory modelling: show a class how a Hopfield network settles, how a learning rule changes weights, or how a small network steers an agent. The project also has a free textbook on neural networks.

- Use [NGC-Learn](ngclearn.md) to script spiking circuits with local learning in code.
- Use [NetPyNE](netpyne.md) or [Arbor](arbor.md) when you need detailed cells and large networks.
- Use [sPyNNaker](spynnaker.md) when the network must run on neuromorphic hardware.

## Install

There is no runnable recipe here, because Simbrain is a desktop application that needs a display. Install it on your own computer.

The current release is 4.2.0, published on 17 August 2026. Download it from https://simbrain.net/downloads/. The page lists:

- cross-platform ZIP (`Simbrain4.2.0_full.zip`, 144 MB);
- Linux AppImage for x86-64 and for ARM64;
- Mac disk images for Apple Silicon and for Intel;
- a Windows installer (`.msi`).

The same files are on the GitHub release page. Simbrain is not on PyPI or conda-forge. To build from source, see the wiki linked from the repository; the project uses Gradle.

The licence is the GNU General Public License, version 2 or later, taken from the source file headers. The repository's LICENSE file is the GPL version 2.

## A first run

The Quick Start page says the fastest way to see Simbrain work is to run a pre-built simulation: open one from the Simulations menu and press play in the workspace toolbar. Many simulations have an info panel on the side that explains what the simulation shows. Toggle it from View, Show/hide info panel.

To build a network yourself, open a network window, then use the keyboard shortcuts the docs recommend ("if you are going to invest time in learning one thing, learn the shortcuts"). Most operations need the network window in focus. The Wand tool, "Connect from selection" and "Connect to neighbors" build structure quickly. When you first launch the program, onboarding windows appear. Dismiss them, or bring them back with File, Reset onboarding windows.

Adapted from <https://docs.simbrain.net/docs/quickstart.html>.

## Reading the output

Simbrain shows results live. Neurons and synapses are drawn in the network window and change as the simulation runs. Plots attach to the network: time series, bar charts, raster plots, histograms, heat maps and a projection plot that reduces high-dimensional activity to two dimensions.

Because the main output is visual, you read it by watching. A settling Hopfield network shows activations falling into a stored pattern. A raster plot of a spiking network shows spike times per neuron. A training run shows the error plot dropping as weights update.

## Pitfalls

- **Version mismatch.** Simbrain 3 and 4 are different code lines. Use the Simbrain3 branch and the v3 site (https://v3.simbrain.net) for old material.
- **Window focus.** Most network operations act on the selected network window. Click it first.
- **Update order.** Networks update in a defined order. Check the Workspace Update and Network Update pages when results look odd.
- **Not a batch tool.** It is built for interactive use. Large parameter sweeps belong in a scripted tool.
- **Pick the right download.** Choose the Mac image that matches your processor (Apple Silicon or Intel) and the Linux AppImage that matches your architecture.

## Further reading

- Project site: https://simbrain.net/
- Documentation: https://docs.simbrain.net/
- Quick start: https://docs.simbrain.net/docs/quickstart.html
- Source: https://github.com/simbrain/simbrain
- Paper: Tosi Z, Yoshimi J (2016). Simbrain 3.0: a flexible, visually-oriented neural network simulator. Neural Networks 83:1-10. https://doi.org/10.1016/j.neunet.2016.07.005

---

Cite: Tosi Z, Yoshimi J (2016). Simbrain 3.0: a flexible, visually-oriented neural network simulator. Neural Networks 83:1-10. doi:10.1016/j.neunet.2016.07.005

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simbrain).
