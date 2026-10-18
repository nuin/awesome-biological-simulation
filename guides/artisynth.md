# ArtiSynth

> Java toolkit for combined rigid-body, finite-element and muscle simulation of anatomy, with an interactive 3D editor.

Licence: BSD-2-Clause · [Source code](https://github.com/artisynth/artisynth_core)

## What it simulates

ArtiSynth simulates the mechanics of anatomical structures. A model is built from three kinds of part:

- **Particles and rigid bodies**, joined by joints, springs and constraints.
- **Finite-element (FEM) bodies** with linear or nonlinear materials, for soft tissue.
- **Point-to-point muscles** that act between attachment points on bodies. The muscles can be driven by excitation signals or solved for by an inverse controller.

Contact and bilateral or unilateral constraints couple the parts, so a bone, a muscle and a block of soft tissue can interact in one model. Time advances in steps. The project describes the system as a 3D mechanical modeling toolkit for biomechanical and biomedical work, and it also runs general mechanical models.

Models are Java classes. A root model class adds a `MechModel` in its `build` method, then adds particles, bodies, springs and muscles to it. The NetDemo tutorial in the repository builds a net of 8 by 8 spring-connected balls in this way, with gravity set on the `MechModel`. A graphical interface lets you inspect components, edit properties and run the simulation.

## When to use it

Use ArtiSynth when your question is about forces and motion of soft and hard anatomy together: a jaw with muscles and a joint, a tongue as an FEM body, or a tissue block in contact with a rigid tool.

- Use [OpenSim](opensim.md) for musculoskeletal models made of bones, joints and muscle-tendon actuators, driven by motion capture data.
- Use [biorbd](biorbd.md) for rigid-body dynamics of musculoskeletal models from a script, with no GUI.
- Use [OpenMM](openmm.md) when the scale is molecular and not anatomical.

ArtiSynth is the stronger choice of the three when FEM tissue and contact matter. It is a weaker choice for batch runs on a server, because its documented workflow is interactive.

## Install

There is no recipe for ArtiSynth on this site. It is a desktop application with a Swing and OpenGL interface, and its documentation describes interactive use: pick a model from a menu and press play. Its libraries include native code for linear solvers, Java OpenGL (JOGL) and collision detection. The project program has a `-noGui` option, but this guide does not claim a headless workflow.

The project's quick installation guide (`doc/installation/quickInstallation.tex` in the repository) gives these steps for a precompiled release:

1. Use a 64-bit Windows, macOS or Linux system with an Intel processor. Apple M-series Macs can run it through Rosetta, with a 64-bit Intel-based JDK.
2. Install a full Java Development Kit (JDK), version 8 or higher. A runtime-only JRE is not enough. Check with `javac -version`.
3. Download the latest precompiled release zip from https://www.artisynth.org/downloads and unzip it into a folder without spaces in its name.
4. On Windows, click `bin\artisynth.bat`. On macOS and Linux, run `bin/artisynth` from a terminal.

The repository's `VERSION` file reads `artisynth_core_3.9`. The repository carries no release tags, so the version comes from that file. For model development the project recommends cloning the repository from GitHub into the Eclipse IDE, with guides for Windows, macOS and Linux at https://www.artisynth.org/installGuides.

On macOS the first model run may produce a security error for the untrusted native libraries. The install guide has a section on handling it.

## A first run

Adapted from the quick installation guide above and from the model guide (`doc/modelguide/overview.tex`).

1. Start ArtiSynth with `bin/artisynth`.
2. Open the **Models** menu and choose a demo. The repository's `demoModels.txt` lists the banner demos, among them "Spring Net" (`artisynth.demos.tutorial.NetDemo`), "Toy Muscle Arm" (`artisynth.demos.tutorial.ToyMuscleArm`) and "Newtons Cradle" (`artisynth.demos.mech.NewtonsCradle`).
3. Press the play button at the top right to start the simulation, and press it again to stop.

To load a model from the command line, pass its class name:

```bash
bin/artisynth -model artisynth.demos.tutorial.NetDemo
```

The model guide documents `-model <classname>`. The built-in help lists further options, including `-play` (start at once), `-playFor <seconds>`, `-exitOnBreak` and `-noGui`.

To change a demo, add the `bin` folder to your Path, edit the demo's `.java` file under `src/artisynth/demos`, then run `compile` in that folder.

## Reading the output

There is no results file. The output is the 3D view and the properties of the components.

- **Viewer.** Bodies, FEM meshes, muscles and markers move as the simulation plays.
- **Property panels.** Select a component to see and change properties such as stiffness, damping, mass and muscle excitation.
- **Timeline.** Probes appear on the timeline. Input probes feed values to a model. Output probes display values over time. The model guide uses output probes to record each muscle's tension force (the `forceNorm` property) in its muscle-material example.

The units are set by the model. NetDemo, for example, uses a gravity of -980 along z, which fits centimetres and seconds.

## Pitfalls

- **JDK, not JRE.** The install guide requires a full JDK.
- **Intel libraries.** The precompiled native libraries are Intel builds, so Apple silicon machines depend on Rosetta and an Intel JDK.
- **Units are yours.** ArtiSynth does not enforce a unit system. Mixing metres with a gravity of -980 gives wrong motion.
- **Path with spaces.** The guide advises a folder name without spaces.
- **Models are code.** Changing geometry or materials means editing and compiling Java, unless a property is exposed in the panels.

## Further reading

- Website and documentation: https://www.artisynth.org and https://www.artisynth.org/doc
- Installation guides: https://www.artisynth.org/installGuides
- Source: https://github.com/artisynth/artisynth_core
- Paper: Lloyd JE, Stavness I, Fels S (2012). ArtiSynth: A Fast Interactive Biomechanical Modeling Toolkit Combining Multibody and Finite Element Simulation. https://doi.org/10.1007/8415_2012_126

---

Cite: Lloyd JE, Stavness I, Fels S (2012). ArtiSynth: A Fast Interactive Biomechanical Modeling Toolkit Combining Multibody and Finite Element Simulation. In: Soft Tissue Biomechanical Modeling for Computer Assisted Surgery, pp 355-394. doi:10.1007/8415_2012_126

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/artisynth).
