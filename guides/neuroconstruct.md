# neuroConstruct

> A Java application for building networks of multicompartmental neurons in 3D space, which then generates scripts for NEURON, GENESIS and other simulators.

Licence: GPL-2.0 · [Source code](https://github.com/NeuralEnsemble/neuroConstruct)

## What it simulates

neuroConstruct is a desktop application for designing 3D networks of detailed neurons. It does not integrate equations itself. You build the model in its interface, and it writes input for an external simulator and runs it.

The model has these parts:

- **Cells**: multicompartmental morphologies with ion channel distributions, synapses and passive properties. Cells, channels and networks can be stored in NeuroML.
- **Placement**: cells are packed into 3D regions as cell groups.
- **Connectivity**: rules connect cell groups through synaptic connections.
- **Stimulation and recording**: inputs to cells and recordings from them.

From that project, neuroConstruct generates scripts for NEURON and GENESIS, as the catalog entry says, and the INSTALL file also names MOOSE and PSICS as targets. It can import and export NeuroML. The simulation itself runs in the target simulator. The application has a 3D view of cells and networks.

## When to use it

Use it to build a network of morphologically detailed cells without writing simulator scripts, to move a model between simulators through NeuroML, or to teach compartmental modelling with a graphical front end.

The latest GitHub release is v1.7.5 (September 2023), and the repository was last pushed to in September 2026.

Alternatives:

- [PyLEMS](pylems.md) and the NeuroML2 tools described in [NeuroML2 / pyNeuroML / LEMS](pyneuroml.md) work from NeuroML and LEMS files in scripts, with no GUI.
- NEURON, with its own GUI and Python interface, is the usual choice when you already know what the model should be.
- [Neuronify](neuronify.md) is a much simpler tool, using integrate-and-fire neurons, aimed at teaching.

## Install it yourself

There is no recipe on biosimhub for this tool. It is a Java desktop application with a 3D view and needs a display, and it relies on a separate simulator install (NEURON is the easiest) to run models. A hosted sandbox with no display and no network cannot run it.

Per the repository INSTALL file:

1. Install Java.
2. Get the latest binary release from https://github.com/NeuralEnsemble/neuroConstruct/releases. The GitHub release v1.7.5 lists no downloadable files, so for that release use the source install below, or the installers linked from https://neuroconstruct.org/download/.
3. Unzip into a folder named `neuroConstruct` in your home directory (Linux, Mac) or on `C:\` (Windows). The folder must not carry the version number.
4. Run the start script:

```bash
cd ~/neuroConstruct
bash nC.sh
```

From source, the INSTALL file gives:

```bash
git clone git://github.com/NeuralEnsemble/neuroConstruct.git
cd neuroConstruct
./updatenC.sh
ant run
```

To run the models it generates, install NEURON (named as the easiest in the INSTALL file), GENESIS, MOOSE or PSICS. The license is GPL-2.0.

## A first run

There is no scripted first run from the project's documentation that fits here, so this section describes the application's start options. Adapted from the usage text in https://github.com/NeuralEnsemble/neuroConstruct/blob/master/src/ucl/physiol/neuroconstruct/gui/MainApplication.java.

```bash
./nC.sh -help
./nC.sh -neuroml2 model.nml
./nC.sh -python
```

- `-neuroml model.xml` and `-neuroml2 model.nml` import a NeuroML file and create a new project.
- `-python [projectfile]` starts a Jython scripting interface.
- `-sims projectfile` opens a project with the tree-based simulation browser.
- `-lastproj` reopens the last project.

The repository includes example projects in `testProjects/`, and the Open Source Brain models can be fetched with `osb/checkOsb.sh -u`.

## Reading the output

Output depends on the target simulator and on the recordings set up in the project. The application has a simulation browser (start option `-sims`) for finished runs. The 3D view shows cell shapes and connections.

## Pitfalls

- **A second program is needed.** neuroConstruct does not run the simulation. Without NEURON or another supported simulator installed, you can only build and export models.
- **Folder name.** The binary install expects a folder called `neuroConstruct`, not one with a version number.
- **Building from source.** `./nC.sh -make` compiles the code with `javac`, so a JDK is needed, not only a Java runtime.
- **Docs have moved.** The old URL `www.neuroconstruct.org` now redirects to `neuroconstruct.org`.
- **Newer NeuroML work.** Current NeuroML2 tools are developed in the pyNeuroML and jNeuroML projects.

## Further reading

- Repository: https://github.com/NeuralEnsemble/neuroConstruct
- Install notes: https://github.com/NeuralEnsemble/neuroConstruct/blob/master/INSTALL.md
- Project site: https://neuroconstruct.org/
- Gleeson P, Steuber V, Silver RA (2007). neuroConstruct: a tool for modeling networks of neurons in 3D space. Neuron 54(2):219-235. https://doi.org/10.1016/j.neuron.2007.03.025

---

Cite: Gleeson P, Steuber V, Silver RA (2007). neuroConstruct: a tool for modeling networks of neurons in 3D space. Neuron 54(2):219-235. doi:10.1016/j.neuron.2007.03.025

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/neuroconstruct).
