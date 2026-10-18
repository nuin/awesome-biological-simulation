# CALVADOS

> Residue-level coarse-grained simulation of one intrinsically disordered protein in OpenMM, with radius of gyration and end-to-end distance from the trajectory.

Licence: GPL-3.0-only · [Source code](https://github.com/KULL-Centre/CALVADOS)

## What it simulates

CALVADOS is a coarse-grained model for intrinsically disordered proteins (IDPs) and multi-domain proteins, run through OpenMM. Each amino acid is one bead. Water and ions are implicit. Beads interact through a Debye-Huckel electrostatic term and a stickiness term with one parameter (lambda) per residue type, fitted to experimental radii of gyration and NMR data.

The same model reproduces how disordered proteins condense. You can run one chain to get its conformational ensemble, or many chains in a slab to see liquid-liquid phase separation. The repository's `examples` folder has single-chain, two-chain, slab, RNA and multi-domain cases. The package is described in the 2025 software paper (arXiv 2504.10408). Model versions are CALVADOS 1 (Tesei 2021), 2 (Tesei and Lindorff-Larsen 2022) and 3 (Cao 2024).

The key assumptions are a fixed residue-level model with no explicit solvent, a Langevin thermostat, and electrostatics set by the ionic strength and pH you give.

## When to use it

Use CALVADOS to predict the radius of gyration, end-to-end distance and contact map of a disordered protein, or to screen sequence variants for phase separation. It runs on a laptop CPU for one short chain.

- Use [OpenMM](openmm.md) or [GROMACS](gromacs.md) for all-atom or other force fields. CALVADOS itself is built on OpenMM.
- Use [LAMMPS](lammps.md) for generic coarse-grained or materials models.
- Use [PySAGES](pysages.md) when you need free-energy profiles along a collective variable.

## Install

CALVADOS 0.9.0 (the version in `pyproject.toml` on the main branch, commit 6981542) is not on PyPI or conda-forge. The README gives this route:

```
conda create -n calvados python=3.13
conda activate calvados
conda install -c conda-forge openmm=8.2.0 mdanalysis=2.9 mdtraj=1.11
git clone https://github.com/KULL-Centre/CALVADOS.git
cd CALVADOS
pip install .
```

Add `cudatoolkit=11.8` to the conda line for a CUDA GPU. The package requires Python 3.11 to 3.13. The pip metadata lists `openmm[cuda12]`, which pulls CUDA wheels, so the recipe here installs the dependencies from conda-forge (openmm 8.3.1, which has linux-aarch64 builds) and then installs the pinned commit with `pip install --no-deps`. A build of that image resolved and installed calvados 0.9.0. The example below was not run.

Licence: GPL-3.0-only.

## Run the tested example

This recipe builds CALVADOS in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 51.1 s.

1. Download [calvados-recipe.tar.gz](https://biosimhub.pages.dev/guides/calvados/calvados-recipe.tar.gz) (Dockerfile, run_idr.py, example sequence.fasta, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf calvados-recipe.tar.gz
   cd calvados
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/calvados:0.9.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/calvados:0.9.0 python /opt/run_idr.py --fasta /work/in/sequence.fasta \
    --temp 293.15 --ionic 0.15 --ph 7 --box 30 \
    --frames 200 --save-every 1000 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `data/cmap.npy` | 9.2 KB |
| `data/conf_prop.csv` | 133 B |
| `data/internal_distances.npy` | 672 B |
| `data/rees.npy` | 920 B |
| `data/rgs.npy` | 1.7 KB |
| `idr/checkpoint.cif` | 5.0 KB |
| `idr/checkpoint.pdb` | 2.8 KB |
| `idr/components.yaml` | 692 B |
| `idr/config.yaml` | 791 B |
| `idr/idr.dcd` | 95.6 KB |
| `idr/idr.log` | 0 B |
| `idr/idr.xml` | 9.4 KB |
| `idr/restart.chk` | 4.2 KB |
| `idr/run.py` | 823 B |
| `idr/top.cif` | 5.0 KB |
| `idr/top.pdb` | 2.8 KB |
| `run_log.txt` | 768 B |

<details><summary>First lines of <code>data/conf_prop.csv</code></summary>

```
,value,error
Rg,1.4373172967449008,0.022738608477750884
Ree,3.2412686,0.10265623300899199
nu,0.5108056427022536,0.008030596576401448
```

</details>

<details><summary>First lines of <code>idr/checkpoint.cif</code></summary>

```
data_cell
# Created with OpenMM 8.3.1, 2026-10-18
#
_cell.length_a       300.0000
_cell.length_b       300.0000
_cell.length_c       300.0000
_cell.angle_alpha     90.0000
_cell.angle_beta      90.0000
_cell.angle_gamma     90.0000
#
loop_
_atom_site.group_PDB
```

</details>

<details><summary>First lines of <code>idr/checkpoint.pdb</code></summary>

```
REMARK   1 CREATED WITH OPENMM 8.3.1, 2026-10-18
CRYST1  300.000  300.000  300.000  90.00  90.00  90.00 P 1           1 
ATOM      1  CA  ARG A   1     134.076 143.776  88.871  1.00  0.00           C  
ATOM      2  CA  ARG A   2     133.306 144.931  91.992  1.00  0.00           C  
ATOM      3  CA  GLY A   3     133.382 147.866  94.253  1.00  0.00           C  
ATOM      4  CA  GLY A   4     136.308 150.233  95.233  1.00  0.00           C  
ATOM      5  CA  ARG A   5     139.762 148.765  96.215  1.00  0.00           C  
ATOM      6  CA  GLY A   6     140.580 151.778  93.982  1.00  0.00           C  
ATOM      7  CA  GLY A   7     138.987 152.254  90.265  1.00  0.00           C  
ATOM      8  CA  TYR A   8     142.340 152.826  88.939  1.00  0.00           C  
ATOM      9  CA  ASP A   9     144.805 150.491  88.731  1.00  0.00           C  
ATOM     10  CA  ARG A  10     145.976 147.102  89.793  1.00  0.00           C  
```

</details>

<details><summary>First lines of <code>idr/components.yaml</code></summary>

```
defaults:
  molecule_type: protein
  nmol: 1
  charge_termini: both
  alpha: 0.0
  kb: 8033.0
  ffasta: /work/in/sequence.fasta
  restraint: false
  restraint_type: harmonic
  cutoff_restr: 0.9
  pdb_folder: null
  fdomains: null
```

</details>

<details><summary>First lines of <code>idr/config.yaml</code></summary>

```
box:
- 30.0
- 30.0
- 30.0
temp: 293.15
ionic: 0.15
pH: 7.0
sysname: idr
topol: center
fixed_lambda: 0.0
eps_lj: 0.2
cutoff_lj: 2.0
```

</details>

<details><summary>First lines of <code>idr/idr.xml</code></summary>

```
<?xml version="1.0" ?>
<System openmmVersion="8.3.1" type="System" version="1">
	<PeriodicBoxVectors>
		<A x="30" y="0" z="0"/>
		<B x="0" y="30" z="0"/>
		<C x="0" y="0" z="30"/>
	</PeriodicBoxVectors>
	<Particles>
		<Particle mass="158.19"/>
		<Particle mass="156.19"/>
		<Particle mass="57.05"/>
		<Particle mass="57.05"/>
```

</details>

<details><summary>First lines of <code>idr/run.py</code></summary>

```
from calvados import sim
from argparse import ArgumentParser

if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument('--path',nargs='?', default='.', const='.', type=str)
    parser.add_argument('--config',nargs='?', default='config.yaml', const='config.yaml', type=str)
    parser.add_argument('--components',nargs='?', default='components.yaml', const='components.yaml', type=str)

    args = parser.parse_args()

    path = args.path
```

</details>

<details><summary>First lines of <code>idr/top.cif</code></summary>

```
data_cell
# Created with mdtraj 1.11.2, 2026-10-18
#
_cell.length_a       300.0000
_cell.length_b       300.0000
_cell.length_c       300.0000
_cell.angle_alpha     90.0000
_cell.angle_beta      90.0000
_cell.angle_gamma     90.0000
#
loop_
_atom_site.group_PDB
```

</details>

<details><summary>First lines of <code>idr/top.pdb</code></summary>

```
REMARK   1 CREATED WITH MDTraj 1.11.2, 2026-10-18
CRYST1  300.000  300.000  300.000  90.00  90.00  90.00 P 1           1 
ATOM      1  CA  ARG A   1     144.300 144.300 144.300  1.00  0.00           C  
ATOM      2  CA  ARG A   2     144.300 144.300 148.100  1.00  0.00           C  
ATOM      3  CA  GLY A   3     144.300 144.300 151.900  1.00  0.00           C  
ATOM      4  CA  GLY A   4     144.300 144.300 155.700  1.00  0.00           C  
ATOM      5  CA  ARG A   5     144.300 148.100 155.700  1.00  0.00           C  
ATOM      6  CA  GLY A   6     144.300 148.100 151.900  1.00  0.00           C  
ATOM      7  CA  GLY A   7     144.300 148.100 148.100  1.00  0.00           C  
ATOM      8  CA  TYR A   8     144.300 148.100 144.300  1.00  0.00           C  
ATOM      9  CA  ASP A   9     144.300 151.900 144.300  1.00  0.00           C  
ATOM     10  CA  ARG A  10     144.300 151.900 148.100  1.00  0.00           C  
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Total number of components in the system: 1
Total number of molecules in the system: 1
Ashbaugh-Hatch potential between particles with lambda=1 and sigma=0.68 at 2.0 nm: -0.0051627815139227455 kJ/mol
Debye-Hückel potential between unit charges at 4.0 nm: 0.0026935555301494138 kJ/mol
34 particles in the system
---------- FORCES ----------
ah: 34 particles, 33 exclusions
yu: 34 particles, 33 exclusions
0.01 /ps 293.15 K
Running on CPU
No checkpoint file /work/out/idr/restart.chk found: Starting from new system configuration
Writing trajectory to new file /work/out/idr/idr.dcd
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--temp` | Temperature (K) | 293.15 | 250 to 400 |
| `--ionic` | Ionic strength (M) | 0.15 | 0.01 to 1 |
| `--ph` | pH | 7 | 3 to 11 |
| `--box` | Cubic box side (nm) | 30 | 10 to 100 |
| `--frames` | Frames to save | 200 | 20 to 2000 |
| `--save-every` | Integration steps between frames | 1000 | 100 to 10000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the repository's [single_IDR example](https://github.com/KULL-Centre/CALVADOS/tree/main/examples/single_IDR). Its `prepare.py` builds a `Config` and a `Components` object, writes `config.yaml`, `components.yaml` and `run.py` into a folder, and then you run:

```
python prepare.py --name FUSRGG3
python FUSRGG3/run.py --path FUSRGG3
```

The default example sets a 50 nm cubic box, 293.15 K, 0.19 M ionic strength, pH 7.5, 7000 steps between frames and 1010 frames, on the CPU platform. The recipe on this page shortens it: FUSRGG3 (34 residues, RRGGRGGYDRGGYRGRGGDRGGFRGGRGGGDRGC), a 30 nm box, 200 frames of 1000 steps, seed 42. The helper script follows `prepare.py` and adds `random_number_seed` to the config. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Reading the output

The run writes a topology (`top.pdb`), a DCD trajectory and a checkpoint into the system folder. The analysis hook in `run.py` calls `save_conf_prop`, which, per its docstring, writes:

- `rgs.npy` and `rees.npy`: radius of gyration and end-to-end distance for every frame.
- `conf_prop.csv`: summary values with block-averaged errors. For an IDR it also reports the fitted scaling exponent.
- `cmap.npy`: the contact map.
- `internal_distances.npy`: mean distance against sequence separation, for IDRs.

Skip the first frames with `start` so the chain forgets its starting conformation. For a 34-residue chain, expect a radius of gyration of a few nanometres or less. That expectation comes from the chain length and is not a measured result of this recipe.

## Pitfalls

- Frames are saved every `wfreq` steps. Total steps are frames times `wfreq`, so a long chain or a slab needs far more steps than the default example.
- The residue file matters. The example folder ships `residues_CALVADOS2.csv`. The package's own `calvados/data/residues.csv` is a newer parameter set, and the two give different results.
- Box size must exceed the extended chain. A 34-residue chain fits easily in 30 nm. A 500-residue chain needs a larger box.
- Phase-separation runs need a slab geometry, more chains and GPU time. Use the `slab_IDR` example for those.
- The topology option `center` places the chain at the box centre. Other options exist for several chains.

## Further reading

- Source and examples: https://github.com/KULL-Centre/CALVADOS
- Software paper: von Bulow S et al. (2025) Software package for simulations using the coarse-grained CALVADOS model. https://doi.org/10.48550/arXiv.2504.10408
- Tesei G, Schulze TK, Crehuet R, Lindorff-Larsen K (2021) PNAS 118:e2111696118. https://doi.org/10.1073/pnas.2111696118
- Tesei G, Lindorff-Larsen K (2022) Open Res Eur 2:94. https://doi.org/10.12688/openreseurope.14967.2
- Cao F, von Bulow S, Tesei G, Lindorff-Larsen K (2024) Protein Sci 33:e5172. https://doi.org/10.1002/pro.5172

---

Cite: Tesei G, Schulze TK, Crehuet R, Lindorff-Larsen K (2021). Accurate model of liquid-liquid phase behavior of intrinsically disordered proteins from optimization of single-chain properties. PNAS 118:e2111696118. doi:10.1073/pnas.2111696118

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/calvados).
