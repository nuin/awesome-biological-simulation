# CNApy

> Desktop application for constraint-based modelling of metabolic networks, with FBA, FVA, elementary flux modes, strain design and interactive flux maps.

Licence: Apache-2.0 · [Source code](https://github.com/cnapy-org/CNApy)

## What it simulates

CNApy is a graphical program for constraint-based reconstruction and analysis (COBRA) of stoichiometric metabolic models. It does not simulate time. A model is a set of reactions with flux bounds, and a method looks for steady-state flux distributions inside those bounds.

The README lists these methods:

- Flux balance analysis (FBA) and flux variability analysis (FVA).
- Yield optimisation, based on linear-fractional programming, and phase plane analyses.
- Making measured in vivo flux scenarios stoichiometrically feasible, optionally by changing the biomass reaction.
- Elementary flux modes (EFM).
- Thermodynamic methods based on OptMDFpathway.
- Strain design with OptKnock, RobustKnock, OptCouple and minimal cut sets, through the StrainDesign package.

It also shows results as interactive, editable metabolic maps, including Escher maps, and it creates and edits models. Models load and save as SBML. Some methods come from cobrapy.

## When to use it

Use CNApy when you want to inspect a genome-scale model by hand: set a medium, run FBA, see the fluxes on a map, change a bound and run again. It suits teaching and exploration. It also suits strain design, where the dialogs for knockout and cut-set methods save writing scripts.

- Use [ReFramed](reframed.md) when you want FBA, FVA or pFBA from a Python script on a server.
- Use [COPASI](copasi.md) when the model has kinetics and you need time courses.
- Use [libRoadRunner](libroadrunner.md) for fast ODE simulation of an SBML model.

## Install

CNApy is a desktop GUI. This site gives no ready-to-run recipe for it, because it has no batch interface to put in a container. Install it on your own computer. The README gives four ways.

1. **Installer.** Download `install_cnapy_here.bat` (Windows) or `install_cnapy_here.sh` (Linux and macOS) from the v1.2.8 release page, put it in an empty folder and run it. It uses micromamba. Afterwards start CNApy from the desktop icon or `run_cnapy.sh`.
2. **pip.** `pip install cnapy`, then run `cnapy` or `python -m cnapy`. The README says this works with Python 3.10 only, and the PyPI metadata requires `==3.10.*`.
3. **conda or mamba.** Create an environment, then use pip inside it:

```bash
conda create --name cnapy-1.2.8 python=3.10 pip openjdk -c conda-forge
conda activate cnapy-1.2.8
pip install cnapy
```

   The README notes that the cnapy conda package on anaconda.org is not updated because of licensing uncertainties. Use the pip route.
4. **Development setup.** Clone the repository and run `uv run cnapy.py`.

The current release is v1.2.8 (2 April 2026). If CNApy reports a Java error, install an OpenJDK, which the conda command above already does.

CNApy ships with the open-source solver GLPK. The user guide says SCIP is faster for strain design and thermodynamic calculations, and that CNApy bundles the community editions of CPLEX and Gurobi. These editions are limited to models with up to 1000 variables. Larger models need full licences of those commercial solvers.

## A first run

Adapted from the CNApy guide: https://cnapy-org.github.io/CNApy-guide/

1. Start CNApy. It opens with an empty project.
2. Choose "Download CNApy example projects..." in the Projects menu, or follow the first-start-up prompt. The example projects include interactive maps of E. coli models such as ECC2 and iML1515.
3. Open a project from the Project menu, for instance `ECC2comp.cna`. A `.cna` file holds the model and its maps.
4. In the reaction list, the Scenario column holds scenario values. Type a single number to fix a flux, or a pair such as `-10, 1.2` to set lower and upper bounds. A scenario value overrides the model's bounds without changing the model.
5. Run FBA from the menu bar or the toolbar. The Flux column fills with the result, and the map shows the fluxes in colour.
6. Run FVA. The LB and UB columns then show the minimum and maximum flux of each reaction.

To start from your own network, use "New project from SBML" in the Project menu, or type reactions such as `A + 2 B -> C` in the reaction form.

The window has a reaction, metabolite and gene list on the right, a map view above an embedded Jupyter console on the left, and a menu bar with a toolbar on top. The console gives programmatic access to the model.

## Reading the output

FBA gives one flux per reaction, in the Flux column and on the map. The objective is the model's objective, or the scenario objective if you set one in the Scenario tab. Exchange reactions show uptake and secretion. FVA gives a range per reaction. A reaction with a narrow range is tightly determined by the objective and the scenario. A wide range means the model leaves it free.

Scenarios save as `.scen` files, and a flux analysis cache can be switched on in the configuration dialog so that results reload without recomputing. No numbers are quoted here, because the project documents give none for a specific run.

## Pitfalls

- **Python 3.10 only for pip.** Other Python versions fail at install.
- **Windows multiprocessing.** The guide says to set the number of processes to 1 on Windows, because multiprocessing performs poorly there.
- **Solver limits.** The bundled commercial solvers stop at 1000 variables. Switch the default solver in the COBRApy configuration dialog, or install the full versions with the wizards under the Config menu.
- **Scenario against model.** A scenario value outside the reaction's bounds replaces them. The box frame turns yellow in that case. Delete the scenario value to go back to the model bounds.
- **Not CellNetAnalyzer.** The README notes that the MATLAB program CellNetAnalyzer is a separate project and does not work with CNApy.

## Further reading

- Source and README: https://github.com/cnapy-org/CNApy
- User guide: https://cnapy-org.github.io/CNApy-guide/
- Example projects: https://github.com/cnapy-org/CNApy-projects/releases/latest
- Paper: Thiele S et al. (2022) CNApy: a CellNetAnalyzer GUI in Python for analyzing and designing metabolic networks. Bioinformatics 38:1467-1469. https://doi.org/10.1093/bioinformatics/btab828

---

Cite: Thiele S, von Kamp A, Bekiaris PS, Schneider P, Klamt S (2022). CNApy: a CellNetAnalyzer GUI in Python for analyzing and designing metabolic networks. Bioinformatics 38:1467-1469. doi:10.1093/bioinformatics/btab828

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cnapy).
