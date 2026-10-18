# PhysiCell

> Off-lattice 2-D agent-based model of proliferating cells with cycle phases, apoptosis, adhesion, repulsion and optional random motility; writes live and dying cell counts over time and SVG snapshots.

Licence: BSD-3-Clause · [Source code](https://github.com/MathCancer/PhysiCell)

## What it simulates

PhysiCell simulates individual cells as soft spheres in continuous space. Each cell has its own volume, cell-cycle phase, death state and movement. Cells push apart when they overlap and pull together within a short adhesion range. A solver for diffusing chemicals (BioFVM) runs under the cells on a grid, so oxygen, drugs or signals can be secreted and taken up.

The biosimhub recipe compiles PhysiCell 1.14.2 with its `template` sample project. That project has one cell type with a flow-cytometry cycle (G0/G1, S, G2, M, with phase durations of 300, 480, 240 and 60 minutes), apoptosis, an optional random walk and one substrate that cells neither make nor use. Cells start at random positions in a 1000 by 1000 micron 2-D domain. Time is in minutes.

## When to use it

Use PhysiCell to ask how cell-level rules produce tissue-level behavior: tumor growth, necrotic cores, immune attack, or crowding that slows division.

- Use [Artistoo](artistoo.md) when cell shape matters and cells deform or crawl on a pixel grid.
- Use [tyssue](tyssue.md) or [PyAFV](pyafv.md) for confluent epithelia drawn as polygons.
- Use [GillesPy2](gillespy2.md) when you track molecule counts in one well-mixed compartment, not cells in space.

The template has no cell rules, no oxygen dependence and no cell types beyond one. Real PhysiCell work edits the settings XML and the C++ in `custom_modules/`.

## Install it yourself

PhysiCell is C++ and builds with `make`. The recipe's Dockerfile pins tag 1.14.2 (commit dbd3499) and runs, on Debian 12 with g++ 12:

```
git clone --depth 1 --branch 1.14.2 https://github.com/MathCancer/PhysiCell
cd PhysiCell
make template
make -j4
./project config/PhysiCell_settings.xml
```

The stock Makefile compiles with `-march=native -mfpmath=both -m64`. On Linux aarch64, g++ rejects the last two. The recipe replaces the flags with `-O3 -fomit-frame-pointer -fopenmp -std=c++11`, which builds on arm64 and also gives a binary that runs on any CPU of that architecture. PhysiCell writes its results into the folder named in `<save><folder>` of the settings file, here `output`, and the folder must exist before the run.

## Run the tested example

This recipe builds PhysiCell in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 17.6 s.

1. Download [physicell-recipe.tar.gz](https://biosimhub.pages.dev/guides/physicell/physicell-recipe.tar.gz) (Dockerfile, run_physicell.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf physicell-recipe.tar.gz
   cd physicell
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/physicell:1.14.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/physicell:1.14.2 python3 /opt/run_physicell.py --cells 10 --max-time 4320 \
    --g1-duration 300 --apoptosis-rate 5.31667e-05 \
    --speed 0 --adhesion 0.4 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cell_counts.csv` | 381 B |
| `config_used.xml` | 12.4 KB |
| `final.svg` | 20.2 KB |
| `initial.svg` | 3.8 KB |
| `run_log.txt` | 104 B |
| `summary.csv` | 125 B |

<details><summary>First lines of <code>cell_counts.csv</code></summary>

```
time_min,live_cells,dead_cells,mean_volume_um3,mean_radius_from_centre_um
0,10,0,2494.0,402.9
360,10,0,2945.0,402.9
720,9,1,3903.6,387.7
1080,13,0,3183.4,373.5
1440,16,0,3446.1,363.7
1800,19,0,3712.5,391.0
2160,25,1,3328.7,375.4
2520,31,1,3285.8,379.4
2880,38,0,3231.8,384.3
3240,42,3,3590.6,381.9
3600,49,3,3656.0,398.1
```

</details>

<details><summary>First lines of <code>config_used.xml</code></summary>

```
<PhysiCell_settings version="devel-version">

    <domain>
        <x_min>-500</x_min>
        <x_max>500</x_max>
        <y_min>-500</y_min>
        <y_max>500</y_max>
        <z_min>-10</z_min>
        <z_max>10</z_max>
        <dx>20</dx>
        <dy>20</dy>
        <dz>20</dz>
```

</details>

<details><summary>First lines of <code>final.svg</code></summary>

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with PhysiCell (http://PhysiCell.MathCancer.org/) -->
<svg 
 xmlns:dc="http://purl.org/dc/elements/1.1/" 
 xmlns:cc="http://creativecommons.org/ns#" 
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
 xmlns:svg="http://www.w3.org/2000/svg" 
 xmlns="http://www.w3.org/2000/svg" 
 version="1.1" 
 width="1000" 
 height="1070" 
 id="svg2">
```

</details>

<details><summary>First lines of <code>initial.svg</code></summary>

```
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!-- Created with PhysiCell (http://PhysiCell.MathCancer.org/) -->
<svg 
 xmlns:dc="http://purl.org/dc/elements/1.1/" 
 xmlns:cc="http://creativecommons.org/ns#" 
 xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#" 
 xmlns:svg="http://www.w3.org/2000/svg" 
 xmlns="http://www.w3.org/2000/svg" 
 version="1.1" 
 width="1000" 
 height="1070" 
 id="svg2">
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
PhysiCell finished in 16.9 s; 13 progress lines
done: 10 cells at 0 min, 75 live and 3 dead at 4320 min
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
seed,initial_cells,final_time_min,final_live_cells,final_dead_cells,fold_change_live,wall_seconds
42,10,4320,75,3,7.5,16.9
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--cells` | Initial cells | 10 | 1 to 200 |
| `--max-time` | Simulated time (minutes) | 4320 | 360 to 10080 |
| `--g1-duration` | Mean G0/G1 duration (minutes) | 300 | 60 to 2000 |
| `--apoptosis-rate` | Apoptosis rate (1/min) | 5.31667e-05 | 0 to 0.01 |
| `--speed` | Random motility speed (micron/min | 0 | 0 to 5 |
| `--adhesion` | Cell-cell adhesion strength (micron/min) | 0.4 | 0 to 5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_physicell.py` edits the template settings, runs the compiled `project` on one thread, and reads each saved snapshot (`output*_cells.mat`). It writes six files.

- `cell_counts.csv` has one row per 360 simulated minutes. Columns are live cells, dying cells, mean cell volume and mean distance from the domain centre. A dying cell is in apoptosis and leaves the table after its 516-minute apoptosis phase.
- `summary.csv` has one row: seed 42, 10 initial cells, 4320 min, 75 live cells, 3 dying cells, a fold change of 7.5 and a wall time of 16.9 s.
- `initial.svg` and `final.svg` draw each cell as a circle with its nucleus. The final picture has 156 circles, which is 78 cells at two circles each (75 live and 3 dying).
- `config_used.xml` is the exact settings file for the run.
- `run_log.txt` has two lines: the wall time and the cell totals.

The live count rises from 10 to 75 over 4320 minutes, which is 3 days. The mean cycle is about 1080 minutes (300 + 480 + 240 + 60). Four mean cycles would give 16-fold growth. The run gives 7.5-fold, because every cell starts at the beginning of G0/G1 and the first division is delayed: the count stays at 10 until 720 minutes and reaches 13 at 1080 minutes. Mean volume starts at 2494 cubic microns, the default cell volume, and varies between 2945 and 3904 as cells grow before they divide.

## Your own runs

Each run changes one value from the example (seed 42, 10 cells, 4320 min). Each ran in the recipe's sandbox on one CPU, in 14 to 17 s.

- **Faster G0/G1.** `--g1-duration 100` gave 168 live cells (16.8-fold) instead of 75. A shorter first phase shortens the whole cycle from about 1080 to 880 minutes.
- **Higher apoptosis.** `--apoptosis-rate 0.002` (about 38 times the default 5.3e-5 per minute) gave 0 live cells. The count fell from 10 to 5 at 360 minutes, 1 at 1080 minutes and 0 at 1440 minutes.
- **Another seed.** `--seed 43` gave 108 live cells, against 75 for seed 42. Cell positions and phase durations are random, so report a distribution over many seeds.
- **Motility and strong adhesion.** `--speed 1 --adhesion 4` gave 88 live cells and a mean distance from the centre of 462 microns, against 405 for the example.

## Pitfalls

- **Runtime scales with the diffusion step.** The template uses a diffusion step of 0.01 minutes on a 50 by 50 grid. A 7200-minute run with 5 cells took 35 s on one CPU, and the 4320-minute default takes about 17 s. The recipe caps the run at 10,080 minutes.
- **Output grows fast.** The stock settings save every 60 minutes, and a 7200-minute run wrote 871 files. The recipe saves every 360 minutes and keeps the raw files in a temporary folder.
- **The seed lives in the settings.** In 1.14, set `<options><random_seed>`. A `random_seed` user parameter still works but prints a warning.
- **The thread count is in the settings.** The template asks for 6 OpenMP threads. The recipe sets 1.
- **Dying cells vanish.** Apoptotic cells lyse and are removed, so the dying-cell column can drop back to 0.

## Further reading

- Source and sample projects: https://github.com/MathCancer/PhysiCell
- Project site and user guide: http://physicell.org
- Paper: Ghaffarizadeh A et al. (2018) PhysiCell: an open source physics-based cell simulator for 3-D multicellular systems. PLoS Comput Biol 14(2):e1005991. https://doi.org/10.1371/journal.pcbi.1005991

---

Cite: Ghaffarizadeh A, Heiland R, Friedman SH, Mumenthaler SM, Macklin P (2018). PhysiCell: an open source physics-based cell simulator for 3-D multicellular systems. PLoS Comput Biol 14(2):e1005991. doi:10.1371/journal.pcbi.1005991

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/physicell).
