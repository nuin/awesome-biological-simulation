# Goo

> Grow and divide 3D deformable cells with cloth physics in headless Blender, and log cell count, volume, shape and spread per minute.

Licence: BSD-3-Clause · [Source code](https://github.com/megasonlab/goo)

## What it simulates

Goo simulates animal cells as deformable 3D objects. Each cell is a closed surface mesh that Blender treats as cloth with internal pressure, so a cell resists compression like a fluid-filled balloon. Cells grow toward a target volume, divide, stick to neighbours of the same type and bump into each other. Blender does the physics and Goo adds the cell biology on top, in Python.

The example starts with 2 cells of about 14 um3 each. Every cell grows toward a 60 um3 target. A cell divides when its volume reaches a threshold drawn from a normal distribution with mean 50 um3 and standard deviation 1 um3. Adhesion strength between cells of the same type is 500. One frame is one simulated minute, and the example runs 90 frames.

Goo also has molecules that diffuse, gene networks that act on cell properties, and data export to HDF5. This recipe uses growth, division, adhesion and optional random motion.

## When to use it

Use Goo when cell shape matters, not only cell position:

- How do adhesion and growth set the packing and shape of a young embryo or an organoid?
- How fast does a clump expand when cells divide at a given size?
- Do cells keep a round shape, or do neighbours deform them?

For vertex models of flat epithelial sheets, use [tyssue](tyssue.md). For cells as pixels on a lattice, [Artistoo](artistoo.md) is cheaper to run. Goo costs more per cell, and run time grows with the number of cells.

## Install it yourself

Goo runs inside Blender, and Blender is the supported entry point. The project documents Blender 4.0 LTS as the recommended version and says Blender 4.5 is not supported because of RoadRunner (the gene-network engine). The upstream route is `make setup` in a clone of https://github.com/megasonlab/goo, which asks for the path to your Blender executable and installs the Python dependencies for it.

The recipe's image does the same by hand on Linux x86_64:

1. Download the Blender 4.0.2 tarball from download.blender.org and unpack it.
2. Install the dependencies into a folder with Blender's own Python: NumPy 1.26.4, SciPy 1.14.0, h5py, tifffile, xarray, antimony and libroadrunner 2.7.
3. Copy the `src/goo` folder from commit a248b93 into that folder and put it on `PYTHONPATH`.
4. Provide `libpython3.10.so.1.0`. The Linux build of Blender 4.0 ships no libpython shared library, and libroadrunner fails to import without one. The image copies it from the official Python 3.10 image.

Then run a script headless:

```
blender -b --factory-startup --python-exit-code 1 --python my_script.py
```

The `--python-exit-code 1` flag makes Blender exit with code 1 when the script raises an error.

## Run the tested example

This recipe builds Goo in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 35.2 s. Goo has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [goo-recipe.tar.gz](https://biosimhub.pages.dev/guides/goo/goo-recipe.tar.gz) (Dockerfile, run_goo.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf goo-recipe.tar.gz
   cd goo
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/goo:a248b93 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/goo:a248b93 /opt/blender/blender -b --factory-startup \
    --python-exit-code 1 --python /opt/run_goo.py -- \
    --cells 2 --frames 90 --target_volume 60 --division_volume 50 \
    --adhesion 500 --motion 0 --seed 2024
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cells.csv` | 678 B |
| `frames.csv` | 2.9 KB |
| `run_log.txt` | 88 B |

<details><summary>First lines of <code>cells.csv</code></summary>

```
name,x_um,y_um,z_um,volume_um3,sphericity
A1.0.0.0,-0.981,-2.553,-2.635,22.53,0.8805
A2.0.0.0,-1.411,2.119,-2.283,22.54,0.8875
A1.1.0.0,-3.160,-1.826,1.659,22.09,0.8809
A2.1.0.0,1.446,1.872,1.972,22.91,0.8834
A2.1.1.0,-2.856,2.755,1.183,23.51,0.8709
A1.1.1.0,0.557,-1.588,3.721,22.93,0.8856
A1.0.1,2.870,-1.809,-0.901,49.07,0.9824
A2.0.1.0,3.249,1.758,-1.404,23.41,0.8782
A2.1.0.1,0.733,2.059,3.606,23.99,0.8896
A2.0.0.1,-0.577,2.085,-3.788,22.85,0.8982
A2.0.1.1,2.203,2.706,-0.753,20.28,0.8495
```

</details>

<details><summary>First lines of <code>frames.csv</code></summary>

```
frame,cells,total_volume_um3,mean_volume_um3,mean_sphericity,radius_of_gyration_um
1,2,28.14,14.07,0.9870,1.750
2,2,28.48,14.24,0.9874,1.750
3,2,29.22,14.61,0.9882,1.750
4,2,30.28,15.14,0.9884,1.750
5,2,31.59,15.79,0.9880,1.750
6,2,33.12,16.56,0.9876,1.750
7,2,34.89,17.44,0.9875,1.750
8,2,36.87,18.43,0.9876,1.749
9,2,39.04,19.52,0.9877,1.748
10,2,41.38,20.69,0.9877,1.747
11,2,43.81,21.91,0.9878,1.746
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
90 frames: 15 cells, mean volume 24.5 um3, sphericity 0.886, radius of gyration 3.74 um
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--cells` | Starting cells | 2 | 1 to 6 |
| `--frames` | Frames (1 frame = 1 simulated minute) | 90 | 10 to 150 |
| `--target_volume` | Target cell volume (um3) | 60 | 20 to 150 |
| `--division_volume` | Division volume (um3) | 50 | 20 to 150 |
| `--adhesion` | Homotypic adhesion strength | 500 | 0 to 5000 |
| `--motion` | Random motion strength | 0 | 0 to 1000 |
| `--seed` | Seed | 2024 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper `run_goo.py` builds the cells, steps the Blender timeline one frame at a time and writes three files.

- `run_log.txt`: "90 frames: 15 cells, mean volume 24.5 um3, sphericity 0.886, radius of gyration 3.74 um".
- `frames.csv` has one row per frame: cell count, total volume, mean volume, mean sphericity and radius of gyration (the root-mean-square distance of the cell centres from their centroid, in um).
- `cells.csv` lists the 15 cells at the last frame with position, volume and sphericity. The names follow the lineage: `A1.0.0.0` descends from the first starting cell A1.

Total volume rises from 28.1 um3 at frame 1 to 67.9 at frame 20 and 367.6 at frame 90. The count stays at 2 until frame 33, reaches 3 at frame 34 and 4 at frame 35, then 8 at frame 62 and 15 at frame 90. Mean sphericity falls from 0.987 at frame 1 to 0.886 at frame 90. A sphericity of 1 is a sphere. The radius of gyration grows from 1.75 to 3.74 um as the clump expands.

Most cells at frame 90 are at 20 to 24 um3, which is the size of a daughter after division. One cell is at 49.1 um3 (sphericity 0.982), just under the division threshold.

## Your own runs

Each run changes one value from the example (seed 2024, 90 frames, 2 cells). Time is wall-clock under x86_64 emulation on an Apple-silicon host and varies with load.

| Change | Cells | Mean volume (um3) | Sphericity | Radius of gyration (um) | Time |
|---|---|---|---|---|---|
| Example | 15 | 24.5 | 0.886 | 3.74 | 12 s |
| Seed 7 | 14 | 26.7 | 0.898 | 3.76 | 14 s |
| Division volume 35 | 32 | 25.3 | 0.896 | 4.50 | 38 s |
| Adhesion 0 | 13 | 28.5 | 0.908 | 4.22 | 11 s |
| Adhesion 2000 | 8 | 42.0 | 0.891 | 2.97 | 16 s |
| Random motion 300 | 11 | 34.6 | 0.908 | 3.32 | 14 s |
| 4 starting cells | 29 | 25.6 | 0.901 | 5.16 | 27 s |
| Target 100, division 80 | 4 | 61.6 | 0.987 | 3.29 | 7 s |

- **Adhesion.** With adhesion 0 the clump had a radius of gyration of 4.22 um (13 cells). With adhesion 2000 it was 2.97 um (8 cells). The cell counts differ, so the two radii are not directly comparable.
- **Bigger cells.** With target 100 and division 80, cells grew to a mean of 61.6 um3 and stayed round (sphericity 0.987). The count reached only 4.
- **Seeds.** Seed 7 gave 14 cells against 15. The seed changes the division thresholds, so the timing shifts.
- **Repeats.** Two 60-frame runs with the same seed gave identical `frames.csv` files.

## Pitfalls

- **The cell count drives the cost.** Run time grows with the number of cells. The example took 35 s in the sandbox capture and 12 s in a separate run on the same host, so load matters. A 120-frame run from the same start reached 32 cells and took 119 s. The recipe caps frames at 150.
- **Blender prints "Dependency cycle detected" warnings.** They come from the cloth and collision modifiers. A 120-frame log reached 63 MB, so the recipe discards the console output and keeps only the CSV files.
- **Python errors are easy to miss.** Pass `--python-exit-code 1`, or a failed script looks like a successful Blender run.
- **Blender 4.0 only.** The Goo documentation does not support Blender 4.5.
- **Volumes are in um3 and time is in minutes.** The script sets Blender units to micrometres and one frame to one minute.
- **No rendering.** The recipe runs the physics and writes tables. For images, run Goo in the Blender GUI or use the renderer in `goo.Simulator`.

## Further reading

- Source and documentation: https://github.com/megasonlab/goo and https://megasonlab.github.io/goo/
- Example scripts: `simulations/` in the repository, such as `3_volume_dividing_cells.py`
- Data export format: the "Export data" page of the documentation
- Citation: Ruzette AA, Dai C, Megason S. Goo: a library to simulate 3D biological cells, tissues and embryos in Blender (software, Harvard Medical School). The project has no journal paper.

---

Cite: Ruzette AA, Dai C, Megason S. Goo: a library to simulate 3D biological cells, tissues and embryos in Blender (software, Harvard Medical School). https://github.com/megasonlab/goo

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/goo).
