# OpenFE

> Plan a relative hydration free-energy network for a set of ligands, atom-mapped and written as transformation files for OpenMM; planning only, no simulation.

Licence: MIT · [Source code](https://github.com/OpenFreeEnergy/openfe)

## What it simulates

OpenFE (Open Free Energy) sets up and runs alchemical free-energy calculations with molecular dynamics. Its main use is the relative binding free energy (RBFE) of a series of similar ligands to one protein. It also does relative hydration free energies (RHFE), absolute binding and solvation, and plain molecular dynamics.

In a relative calculation one ligand is turned into another. A single hybrid topology holds the shared core once and the differing atoms separately. The change is made in two environments, the protein site and solvent for RBFE, or solvent and vacuum for RHFE. The difference of the two legs gives the relative free energy. Sampling runs in OpenMM with replica exchange.

The workflow has three stages: plan a network of ligand pairs (which pairs to transform, and how to map atoms between them), run each transformation, then gather the results.

## When to use it

- You have a congeneric ligand series and a protein structure, and want a ranking by predicted affinity.
- You need a reproducible, file-based workflow: each transformation is a JSON file that can run on any machine.
- You want a Python API to build your own networks and protocols.

Alternatives:

- [OpenMM](openmm.md) gives raw molecular dynamics, which OpenFE uses as its engine.
- [openmmtools](openmmtools.md) holds the multistate samplers that free-energy protocols build on.
- [GROMACS](gromacs.md) has its own free-energy methods for users who prefer that engine.

## Install

The current release is 1.13.0 (conda-forge, noarch package, Python 3.12 or newer, MIT licence). The project's installation page recommends micromamba:

```
micromamba create -n openfe -c conda-forge openfe=1.13.0
micromamba activate openfe
openfe --help
```

The installation page also describes a `conda-lock` file for reproducible builds. It states that OpenMM 8.3.0 is not supported and that only POSIX systems (macOS, Linux) are.

It installs the same conda package into a micromamba image.

## Run the tested example

This recipe builds OpenFE in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 34.2 s. OpenFE has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [openfe-recipe.tar.gz](https://biosimhub.pages.dev/guides/openfe/openfe-recipe.tar.gz) (Dockerfile, plan_network.py, example ligands.sdf, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf openfe-recipe.tar.gz
   cd openfe
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/openfe:1.13.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/openfe:1.13.0 python /opt/driver/plan_network.py /work/in/ligands.sdf \
    --mapper KartografAtomMapper --network generate_minimal_spanning_network \
    --atom-max-distance 0.95 --central-ligand 0 \
    --repeats 3 > out/openfe_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `network.tar.gz` | 14.7 KB |
| `network/ligand_network.graphml` | 22.8 KB |
| `network/network.json` | 47.0 KB |
| `network/transformations/rhfe_benzaldehyde_solvent_styrene_solvent.json` | 13.5 KB |
| `network/transformations/rhfe_benzaldehyde_vacuum_styrene_vacuum.json` | 13.1 KB |
| `network/transformations/rhfe_benzene_solvent_benzaldehyde_solvent.json` | 12.6 KB |
| `network/transformations/rhfe_benzene_solvent_benzonitrile_solvent.json` | 12.2 KB |
| `network/transformations/rhfe_benzene_solvent_toluene_solvent.json` | 12.8 KB |
| `network/transformations/rhfe_benzene_vacuum_benzaldehyde_vacuum.json` | 12.2 KB |
| `network/transformations/rhfe_benzene_vacuum_benzonitrile_vacuum.json` | 11.8 KB |
| `network/transformations/rhfe_benzene_vacuum_toluene_vacuum.json` | 12.3 KB |
| `network/transformations/rhfe_phenol_solvent_anisole_solvent.json` | 13.3 KB |
| `network/transformations/rhfe_phenol_vacuum_anisole_vacuum.json` | 12.9 KB |
| `network/transformations/rhfe_toluene_solvent_phenol_solvent.json` | 13.3 KB |
| `network/transformations/rhfe_toluene_vacuum_phenol_vacuum.json` | 12.9 KB |
| `network_files.txt` | 942 B |
| `openfe_log.txt` | 2.6 KB |
| `settings.yaml` | 131 B |

<details><summary>First lines of <code>network/ligand_network.graphml</code></summary>

```
<graphml xmlns="http://graphml.graphdrawing.org/xmlns" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://graphml.graphdrawing.org/xmlns http://graphml.graphdrawing.org/x
  <key id="d2" for="edge" attr.name="annotations" attr.type="string" />
  <key id="d1" for="edge" attr.name="mapping" attr.type="string" />
  <key id="d0" for="node" attr.name="moldict" attr.type="string" />
  <graph edgedefault="directed">
    <node id="mol0">
      <data key="d0">{":version:": 1, "__module__": "gufe.components.smallmoleculecomponent", "__qualname__": "SmallMoleculeComponent", "atoms": [[6, 0, 0, false, 0, 0, {"PartialCharge": -0.209}, 3], 
```

</details>

<details><summary>First lines of <code>network/network.json</code></summary>

```
[["SmallMoleculeComponent-515a10e182c4be17c1f458889d593ebf", {"atoms": [[6, 0, 0, false, 0, 0, {"PartialCharge": 0.113825}, 4], [1, 0, 0, false, 0, 0, {"PartialCharge": 0.043825}, 1], [8, 0, 0, false,
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzaldehyde_solvent_styrene_solvent.json</code></summary>

```
[["SmallMoleculeComponent-264d143096cec5cd96edb8ec9a12e57a", {"atoms": [[6, 0, 0, false, 0, 0, {"PartialCharge": -0.209}, 3], [1, 0, 0, false, 0, 0, {"PartialCharge": 0.11349999999999999}, 1], [1, 0, 
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzaldehyde_vacuum_styrene_vacuum.json</code></summary>

```
[["SmallMoleculeComponent-264d143096cec5cd96edb8ec9a12e57a", {"atoms": [[6, 0, 0, false, 0, 0, {"PartialCharge": -0.209}, 3], [1, 0, 0, false, 0, 0, {"PartialCharge": 0.11349999999999999}, 1], [1, 0, 
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzene_solvent_benzaldehyde_solvent.json</code></summary>

```
[["SmallMoleculeComponent-49f192f8e32a0f762b18aefeb49df64d", {"atoms": [[8, 0, 0, false, 0, 0, {"PartialCharge": -0.5281714285714286}, 3], [1, 0, 0, false, 0, 0, {"PartialCharge": -0.00287142857142857
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzene_solvent_benzonitrile_solvent.json</code></summary>

```
[["SmallMoleculeComponent-37406b3456e2e0d6a725bee53864e983", {"atoms": [[7, 0, 0, false, 0, 0, {"PartialCharge": -0.3638}, 2], [6, 0, 0, false, 0, 0, {"PartialCharge": 0.2338}, 2], [6, 0, 0, true, 0, 
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzene_solvent_toluene_solvent.json</code></summary>

```
[["SmallMoleculeComponent-968963ed255971967893031da5a98ab8", {"atoms": [[1, 0, 0, false, 0, 0, {"PartialCharge": 0.04403306666666667}, 1], [1, 0, 0, false, 0, 0, {"PartialCharge": 0.04403306666666667}
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzene_vacuum_benzaldehyde_vacuum.json</code></summary>

```
[["SmallMoleculeComponent-49f192f8e32a0f762b18aefeb49df64d", {"atoms": [[8, 0, 0, false, 0, 0, {"PartialCharge": -0.5281714285714286}, 3], [1, 0, 0, false, 0, 0, {"PartialCharge": -0.00287142857142857
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzene_vacuum_benzonitrile_vacuum.json</code></summary>

```
[["SmallMoleculeComponent-37406b3456e2e0d6a725bee53864e983", {"atoms": [[7, 0, 0, false, 0, 0, {"PartialCharge": -0.3638}, 2], [6, 0, 0, false, 0, 0, {"PartialCharge": 0.2338}, 2], [6, 0, 0, true, 0, 
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_benzene_vacuum_toluene_vacuum.json</code></summary>

```
[["SmallMoleculeComponent-968963ed255971967893031da5a98ab8", {"atoms": [[1, 0, 0, false, 0, 0, {"PartialCharge": 0.04403306666666667}, 1], [1, 0, 0, false, 0, 0, {"PartialCharge": 0.04403306666666667}
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_phenol_solvent_anisole_solvent.json</code></summary>

```
[["SmallMoleculeComponent-515a10e182c4be17c1f458889d593ebf", {"atoms": [[6, 0, 0, false, 0, 0, {"PartialCharge": 0.113825}, 4], [1, 0, 0, false, 0, 0, {"PartialCharge": 0.043825}, 1], [8, 0, 0, false,
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_phenol_vacuum_anisole_vacuum.json</code></summary>

```
[["SmallMoleculeComponent-515a10e182c4be17c1f458889d593ebf", {"atoms": [[6, 0, 0, false, 0, 0, {"PartialCharge": 0.113825}, 4], [1, 0, 0, false, 0, 0, {"PartialCharge": 0.043825}, 1], [8, 0, 0, false,
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_toluene_solvent_phenol_solvent.json</code></summary>

```
[["SmallMoleculeComponent-b3a8ec292a1fb906cbf0983e06ebecf6", {"atoms": [[6, 0, 0, true, 0, 0, {"PartialCharge": -0.09442307692307692}, 3], [6, 0, 0, true, 0, 0, {"PartialCharge": -0.16592307692307692}
```

</details>

<details><summary>First lines of <code>network/transformations/rhfe_toluene_vacuum_phenol_vacuum.json</code></summary>

```
[["SmallMoleculeComponent-b3a8ec292a1fb906cbf0983e06ebecf6", {"atoms": [[6, 0, 0, true, 0, 0, {"PartialCharge": -0.09442307692307692}, 3], [6, 0, 0, true, 0, 0, {"PartialCharge": -0.16592307692307692}
```

</details>

<details><summary>First lines of <code>network_files.txt</code></summary>

```
network/ligand_network.graphml 23354
network/network.json 48178
network/transformations/rhfe_benzaldehyde_solvent_styrene_solvent.json 13828
network/transformations/rhfe_benzaldehyde_vacuum_styrene_vacuum.json 13394
network/transformations/rhfe_benzene_solvent_benzaldehyde_solvent.json 12928
network/transformations/rhfe_benzene_solvent_benzonitrile_solvent.json 12516
network/transformations/rhfe_benzene_solvent_toluene_solvent.json 13068
network/transformations/rhfe_benzene_vacuum_benzaldehyde_vacuum.json 12494
network/transformations/rhfe_benzene_vacuum_benzonitrile_vacuum.json 12082
network/transformations/rhfe_benzene_vacuum_toluene_vacuum.json 12634
network/transformations/rhfe_phenol_solvent_anisole_solvent.json 13665
network/transformations/rhfe_phenol_vacuum_anisole_vacuum.json 13231
```

</details>

<details><summary>First lines of <code>openfe_log.txt</code></summary>

```
openfe plan-rhfe-network -M /work/in/ligands.sdf -s settings.yaml -o network --n-protocol-repeats 3 -n 1
RHFE-NETWORK PLANNER
______________________

Parsing in Files: 
	Got input: 
		Small Molecules: SmallMoleculeComponent(name=benzene) SmallMoleculeComponent(name=toluene) SmallMoleculeComponent(name=phenol) SmallMoleculeComponent(name=benzonitrile) SmallMoleculeComponent(name=a
		Solvent: SolventComponent(name=O, Na+, Cl-)

Using Options:
	Mapper: <KartografAtomMapper-92be13375caab9a5f2ecbf75d925982f>
	Mapping Scorer: <function default_lomap_score at 0x7fffbecb1dd0>
```

</details>

<details><summary>First lines of <code>settings.yaml</code></summary>

```
network:
  method: generate_minimal_spanning_network
mapper:
  method: KartografAtomMapper
  settings:
    atom_max_distance: 0.95
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--mapper` | Atom mapper | KartografAtomMapper | KartografAtomMapper, LomapAtomMapper |
| `--network` | Network layout | generate_minimal_spanning_network | generate_minimal_spanning_network, generate_minimal_redundant_network, generate_radial_network |
| `--atom-max-distance` | Max atom distance for mapping (A; Lomap max3d) | 0.95 | 0.3 to 2 |
| `--central-ligand` | Central ligand index (radial network only) | 0 | 0 to 50 |
| `--repeats` | Protocol repeats per transformation | 3 | 1 to 10 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

The recipe covers the planning stage only. A free-energy simulation is not part of the example, because production runs are long. The recipe's helper script runs `openfe plan-rhfe-network` on a set of seven benzene derivatives whose partial charges are already in the SDF file (the file comes from the OpenFE test data, MIT licence):

```
openfe plan-rhfe-network -M ligands.sdf -s settings.yaml -o network --n-protocol-repeats 3 -n 1
```

The settings file follows https://docs.openfree.energy/en/stable/guide/cli/cli_yaml.html. The default it describes is a minimal spanning network with the Kartograf atom mapper:

```
network:
  method: generate_minimal_spanning_network
mapper:
  method: KartografAtomMapper
  settings:
    atom_max_distance: 0.95
```

The same page lists the other choices the recipe exposes: `LomapAtomMapper`, and the network planners `generate_radial_network`, `generate_minimal_spanning_network` and `generate_minimal_redundant_network`. A radial network needs a central ligand, given as an index or a name.

Without partial charges in the SDF file, planning assigns them (AM1-BCC through AmberTools by default) and the command prints that this may be slow. The example file avoids that step.

To run one transformation from the plan on your own machine, the CLI basics page gives:

```
openfe quickrun transformation.json -o result.json -d workdir
```

`openfe gather` then collects result files into a table.

## Reading the output

The planner saves its results as JSON files for `quickrun`: one file per transformation, and per the 1.13.0 changelog also an AlchemicalNetwork JSON and a LigandNetwork graphml file. The graphml file can be drawn with `openfe view-ligand-network`. Each transformation JSON holds the two chemical systems, the atom mapping and the protocol settings, including the number of repeats.

The recipe packs the directory into `network.tar.gz` and lists file names and sizes in `network_files.txt`. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below. For seven ligands, a minimal spanning network connects them with the fewest edges that join every ligand into one graph. A radial network joins all to one central ligand. A redundant network adds extra edges, which allows cycle checks.

A real run writes a result JSON per transformation (`-o result.json`), and `openfe gather` collects them into a TSV file.

## Pitfalls

- **Planning is not a prediction.** The recipe produces inputs. A free energy needs `quickrun` on every edge, and each edge runs several repeats of replica-exchange sampling.
- **Atom mapping decides quality.** Large changes in size or charge between ligands make poor transformations. Look at the network before running it.
- **Charges are slow to generate.** Provide ligands with partial charges, or run `openfe charge-molecules` once and reuse the file.
- **OpenMM 8.3.0 is unsupported.** Pin the OpenMM version the project lists.
- **Memory.** Planning loads all ligands and builds mappings; the recipe allows 3 GB.

## Further reading

- Documentation: https://docs.openfree.energy
- CLI settings file: https://docs.openfree.energy/en/stable/guide/cli/cli_yaml.html
- Source: https://github.com/OpenFreeEnergy/openfe
- Software citation: OpenFreeEnergy team, OpenFE (Zenodo). https://doi.org/10.5281/zenodo.8344247

---

Cite: OpenFreeEnergy team (2023). OpenFE: Open Free Energy toolkit (software). Zenodo. doi:10.5281/zenodo.8344247

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openfe).
