# Neuronify

> An educational app for building small neural circuits from integrate-and-fire neurons, stimulators and recording devices by drag and drop.

Licence: GPL-3.0 · [Source code](https://github.com/CINPLA/neuronify)

## What it simulates

Neuronify simulates small networks of integrate-and-fire neurons. This is one of the simplest neuron models: the membrane voltage integrates its input, a spike is emitted when it crosses a threshold, and the details of the action potential are ignored. The project's own description is "an educational neural network app using the integrate-and-fire method".

You build a circuit on a canvas. According to the eNeuro paper, the menu offers:

- **Neurons** modelled as integrate-and-fire cells with adjustable parameters, connected by synapses.
- **Stimulators**: current sources, spike generators, and visual and touch inputs (the camera or touch screen can drive the network).
- **Recording devices**: a voltmeter, a spike detector and a loudspeaker.

The app also includes premade network motifs for teaching, such as input summation, gain control by inhibition and detection of the direction of stimulus movement. The aim stated in the paper is a low entry point for students with no programming experience.

## When to use it

Use it in a classroom or for self-study to see how connectivity shapes activity: add a stimulator, a neuron and a voltmeter, change one parameter and watch the trace. It is not a research simulator. It has no scripting interface, no morphology and no way to run large networks.

Alternatives:

- [neuroConstruct](neuroconstruct.md) builds detailed multicompartmental networks and hands them to NEURON or GENESIS.
- [NeuroML2 / pyNeuroML / LEMS](pyneuroml.md) runs model descriptions in files, including integrate-and-fire cells written in LEMS.
- [XPPAUT](xppaut.md) fits when the lesson is phase planes and bifurcations rather than circuits.

## Install it yourself

There is no recipe on biosimhub for this tool. It is a graphical Qt Quick (QML) app that needs a display and touch or mouse input, so a sandbox with no display cannot run it. The project site also offers an online version ("Try online").

The project site (https://ovilab.net/neuronify) lists downloads for Windows (installer and a `.zip` that needs no admin rights), macOS, Linux via a Snap package, Android (Google Play) and iOS (App Store). On Ubuntu:

```bash
sudo snap install neuronify
neuronify
```

The latest GitHub release is v1.3.9 (June 2020), with a macOS disk image attached. The repository was last pushed to in December 2023. To build from source, the README says to install Qt, open `neuronify.pro` in Qt Creator, configure a desktop kit and press Run. Neuronify is licensed GPL-3.0.

## A first run

Adapted from the project site (https://ovilab.net/neuronify) and the eNeuro paper (https://doi.org/10.1523/ENEURO.0022-17.2017).

The paper describes the workflow: pick network elements with adjustable parameters from a menu and place them on the canvas. A minimal circuit uses three of them:

1. A stimulator (a current source or a spike generator).
2. An integrate-and-fire neuron that receives it.
3. A recording device on the neuron, such as the voltmeter or the spike detector.

Then change one parameter, for example the strength of the stimulus or the strength of a synapse to a second neuron, and compare the traces. The repository's `simulations/` folder holds premade networks (folders `tutorial`, `mix`, `sterratt` and others) as starting points.

## Reading the output

Output is on screen: voltage traces in the voltmeter, spike marks in the spike detector, and sound from the loudspeaker. Quantitative numbers are not given here, since none come from the project's documentation.

Read a voltmeter trace as follows. The slow rise is the membrane integrating input. A sharp event marks a spike. After a spike the voltage returns to a reset level. A stronger input shortens the time between spikes.

## Pitfalls

- **It is a simplified model.** Integrate-and-fire cells ignore ion channels and spike shape. Use a conductance-based tool for Hodgkin-Huxley behaviour.
- **No programmatic control.** There is no command line or Python API for batch runs.
- **Old release.** The last release is from 2020, and the build instructions in the README refer to Qt 5.4. The downloads on the project site avoid that build.
- **Camera input.** The visual sensor uses the device camera.
- **Not a hosted tool.** The biosimhub page does not run it. Use the online version or a download.

## Further reading

- Repository: https://github.com/CINPLA/neuronify
- Project site: https://ovilab.net/neuronify
- Dragly SA, Hobbi Mobarhan M, Våvang Solbrå A, et al. (2017). Neuronify: an educational simulator for neural circuits. eNeuro 4(2):ENEURO.0022-17.2017. https://doi.org/10.1523/ENEURO.0022-17.2017

---

Cite: Dragly SA, Hobbi Mobarhan M, Våvang Solbrå A, et al. (2017). Neuronify: an educational simulator for neural circuits. eNeuro 4(2):ENEURO.0022-17.2017. doi:10.1523/ENEURO.0022-17.2017

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/neuronify).
