# SimVascular

> Desktop pipeline from medical images to patient-specific blood flow simulation, with finite-element solvers and reduced-order models.

Licence: BSD-3-Clause · [Source code](https://github.com/SimVascular/SimVascular)

## What it simulates

SimVascular is an interactive application for building patient-specific models of blood vessels from 3D medical images and simulating blood flow in them. The project calls it the only fully open-source package that covers the whole pipeline, from image segmentation to flow analysis.

The pipeline has five stages, as in the project's Getting Started page:

- **Paths:** centerlines along the vessels of interest.
- **Segmentations:** vessel cross-sections drawn along each path on the image.
- **Solid model:** a surface built by lofting the segmentations together.
- **Mesh:** a finite-element volume mesh of the solid model.
- **Simulation:** a CFD run on the mesh with boundary conditions at the inlets and outlets.

According to the project site, the solvers cover 3D finite-element hemodynamics (Navier-Stokes with a fixed wall, and fluid-structure interaction with the coupled momentum method or an arbitrary Lagrangian-Eulerian method), cardiac electrophysiology and active contraction, and reduced-order 0D and 1D models. 0D and 1D models can be coupled to the 3D domain as boundary conditions.

## When to use it

Use SimVascular when the geometry comes from a scan: aortic and coronary flow, grafts, aneurysms, pulmonary and congenital heart cases. The documentation has worked clinical cases (coronary, aortofemoral and pulmonary models). The Vascular Model Repository, a sister project, holds ready-made models and boundary conditions to start from.

Alternatives:

- [openCARP](opencarp.md) simulates the electrical activity of the heart.
- [SOFA Framework](sofa-framework.md) simulates deformable tissue in real time with finite elements.
- [OpenSim](opensim.md) models whole-body musculoskeletal motion.

## Install

SimVascular is a desktop application built on the MITK framework with a graphical interface, and the project distributes it through installers on simtk.org (https://simtk.org/frs/index.php?group_id=188) and as source on GitHub. The licence is the BSD licence (three clauses, Stanford University, the Regents of the University of California and others), with separate terms for external packages such as ITK, VTK and TetGen. The newest GitHub release is tagged `2025-June-original-externals`.

This guide has no container recipe. The workflow runs through the graphical interface: you draw paths and segmentations on the image by hand. Large CFD runs are meant for multi-core or cluster hardware, and the project offers a supercomputing gateway for them. A fixed command that runs in a short unattended job does not describe that work, so the guide does not make one.

The solvers are also published as separate command-line projects on GitHub: svMultiPhysics, svOneDSolver, svZeroDSolver, svMorph and svVascularize. The Python interface exposes the modeling, meshing, path planning, segmentation and geometry modules inside the application.

## A first run

The tutorial on the Getting Started page, adapted here as a plan: https://simvascular.github.io/documentation/getting_started.html

1. Start SimVascular and create a project.
2. Add the image data, then create vessel paths.
3. Create segmentations along the paths.
4. Create the solid model, then the finite-element mesh.
5. Create the CFD simulation and set the boundary conditions.
6. Run the solver and open the results.

A demo project for the tutorial is on the download page. Use it to see what the finished files look like before you segment your own image.

## Reading the output

The CFD solver writes flow results on the mesh at saved time steps, mainly pressure and velocity, and the application can load them for inspection. The documentation covers the CFD results and the 0D model outputs on the CFD and ROM pages. The project does not quote one set of numbers for every case, so read the values from your own run and compare them with the clinical case in the docs when your model matches one.

## Pitfalls

- **Boundary conditions decide the answer.** Outlet pressures and inflow waveforms come from measurement or from a reduced-order model, and the flow solution is only as good as they are. The references page groups the literature on this under boundary conditions.
- **Segmentation quality sets mesh quality.** A rough lofted surface gives a bad volume mesh, so check the solid model before meshing.
- **Mesh refinement matters.** Wall-bounded flow needs fine elements near the wall.
- **Large runs need HPC.** Workstation runs of 3D models can be slow, and the project's gateway exists for that reason.
- **Learn the application first.** The tutorial on a demo project is the intended starting point.
- **Clinical use is not covered by this guide.** The software is a research pipeline.

## Further reading

- Website and documentation: https://simvascular.github.io
- Source: https://github.com/SimVascular/SimVascular
- Downloads: https://simtk.org/frs/index.php?group_id=188
- Vascular Model Repository: https://www.vascularmodel.com/
- Updegrove A, Wilson NM, Merkow J, Lan H, Marsden AL, Shadden SC (2017). SimVascular: an open source pipeline for cardiovascular simulation. Ann Biomed Eng 45:525-541. https://doi.org/10.1007/s10439-016-1762-8

---

Cite: Updegrove A, Wilson NM, Merkow J, Lan H, Marsden AL, Shadden SC (2017). SimVascular: an open source pipeline for cardiovascular simulation. Ann Biomed Eng 45:525-541. doi:10.1007/s10439-016-1762-8

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simvascular).
