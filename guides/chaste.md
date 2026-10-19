# Chaste

> Grow a monolayer of proliferating cells on a Voronoi mesh with spring forces, and record cell number and colony radius every simulated hour.

Licence: BSD-3-Clause · [Source code](https://github.com/Chaste/Chaste)

## What it simulates

Chaste (Cancer, Heart and Soft Tissue Environment) is a C++ library for multiscale simulation of tissues. Its cell-based component models each cell as an agent with its own cell-cycle clock, and moves the cells with mechanical forces. Its other components solve ODEs and PDEs for cell signalling, cardiac electrophysiology and continuum tissue mechanics.

The example uses the cell-based component to grow a monolayer. Cells sit on the nodes of a mesh whose cell boundaries come from a Voronoi tessellation of the cell centres. Each pair of neighbouring cells pulls or pushes with a linear spring force (the Meineke et al. 2001 model). Every cell runs a stochastic cell cycle (`UniformCellCycleModel`) that draws its length uniformly between a minimum and a maximum number of hours. A cell that reaches the end of its cycle divides, and the mesh is rebuilt.

The assumptions are a flat 2D sheet, no contact inhibition (every cell divides when its clock ends), no nutrient or signal fields, and overdamped motion with a time step of 1/120 hour. The default is a 6 by 6 honeycomb patch of 36 cells, run for 48 simulated hours.

## When to use it

Use Chaste to ask how cell-level rules (cycle length, spring stiffness, division) set the growth and shape of a tissue patch, or as a base for crypt, cardiac or tumour models built from the same library.

- For active Voronoi cells that detach and migrate, [pyafv](pyafv.md) is smaller.
- For a fixed network of polygons in an epithelium with an energy function, [tyssue](tyssue.md) fits better.
- For cells that deform on a pixel grid, use [Artistoo](artistoo.md).

## Install it yourself

Chaste has a CMake build and many dependencies: Boost, HDF5, VTK, PETSc, ParMETIS, SUNDIALS, Xerces-C and CodeSynthesis XSD. On Ubuntu 24.04 all of them come from apt (the recipe lists the packages). The repository also has a `docker` folder and a user-projects mechanism.

The recipe pins commit 0be956b of the Chaste repository and replaces the stock cardiac apps with one file, `CellPop.cpp`, which is the source of the example:

```
cmake -S Chaste -B build -G Ninja -DCMAKE_BUILD_TYPE=Release
cmake --build build --target CellPop -j 3
```

The configure step took 64 s and the build 443 s on 3 cores. Only the libraries `CellPop` needs are compiled. The image is 1.43 GB because of the VTK shared libraries.

## Run the tested example

This recipe builds Chaste in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 3.2 s.

1. Download [chaste-recipe.tar.gz](https://biosimhub.pages.dev/guides/chaste/chaste-recipe.tar.gz) (CellPop.cpp, Dockerfile, run_cellpop.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf chaste-recipe.tar.gz
   cd chaste
   sh run.sh
   ```

![Terminal recording of the Chaste example run](https://biosimhub.pages.dev/media/chaste/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/chaste:2026.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/chaste:2026.1 bash /opt/chaste/run_cellpop.sh 6 6 48 15 12 14 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `final_cells.csv` | 11.2 KB |
| `population.csv` | 709 B |
| `run_log.txt` | 1.8 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/chaste/result-dark.png"><img src="https://biosimhub.pages.dev/media/chaste/result.png" alt="Plot of the Chaste example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>final_cells.csv</code></summary>

```
x,y,age_h
-6.51304,-2.59802,0.3
-0.310881,-3.56698,9.525
7.33322,-6.70021,9.50833
3.93837,-5.12017,10.4333
4.59525,-5.75712,5.88333
7.07049,-5.87708,7.91667
-4.21651,-4.37134,4.58333
-2.19776,-3.0424,4.76667
3.31558,-4.52905,11.5167
3.87745,0.755947,3.38333
7.89787,-1.14686,11.575
```

</details>

<details><summary>First lines of <code>population.csv</code></summary>

```
time_h,cells,radius
1,41,3.42044
2,44,3.46962
3,45,3.59026
4,50,3.63307
5,52,3.51387
6,54,3.62574
7,55,3.58484
8,57,3.79832
9,58,3.77931
10,61,3.86302
11,65,3.93508
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Copyright (c) 2005-2026, University of Oxford.
All rights reserved.

University of Oxford means the Chancellor, Masters and Scholars of the
University of Oxford, having an administrative office at Wellington
Square, Oxford OX1 2JD, UK.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:
 * Redistributions of source code must retain the above copyright notice,
   this list of conditions and the following disclaimer.
 * Redistributions in binary form must reproduce the above copyright notice,
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `cols` | Initial cells across | 6 | 2 to 10 |
| `rows` | Initial rows of cells | 6 | 2 to 10 |
| `end_time` | Simulated time (hours) | 48 | 1 to 72 |
| `stiffness` | Spring stiffness | 15 | 1 to 20 |
| `min_cycle` | Shortest cell cycle (hours) | 12 | 10 to 40 |
| `max_cycle` | Longest cell cycle (hours) | 14 | 11 to 48 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`CellPop` takes six numbers and a seed. It advances the simulation one hour at a time and writes one row per hour.

- `population.csv` (709 bytes) has the hour, the number of cells and the colony radius (largest distance from the centroid, in Chaste length units, where a cell has a resting spring length of 1). The 36 starting cells become 41 after 1 hour, 67 after 12 hours, 128 after 24 hours, 247 after 36 hours and 477 after 48 hours. The radius goes from 3.42 to 11.12.
- `final_cells.csv` (11,419 bytes) has one row for each of the 477 cells: x, y and age in hours since the cell's last division. The ages run from 0.2 to 12.96 h with a mean of 6.36 h, below the longest cycle of 14 h.
- `run_log.txt` (1,846 bytes) holds Chaste's licence banner and the last line "done: 477 cells at t=48 h".

Growth is exponential with a doubling time near the mean cycle length of 13 h. From 36 cells, 48 h is 3.7 mean cycles, and 36 times 2 to the power 3.7 is about 470, which matches 477. The doubling time between hour 24 and hour 48 is 24 divided by log2(477/128), which is 12.6 h. The initial birth times are staggered at random, so early divisions are spread across the first 14 h.

Chaste's own visualisation files (`results.viznodes` and others) are written to `/tmp/chaste_out` inside the container and discarded.

## Your own runs

Each run changes one thing from the example (6 by 6 cells, 48 h, stiffness 15, cycle 12 to 14 h, seed 42) and took 1 to 3 s.

- **Another seed.** `seed 43` gave 450 cells and a radius of 10.27 at 48 h, against 477 and 11.12. Stochastic cycles and division directions differ between seeds, so repeat with several seeds before comparing parameters.
- **Slower cell cycle.** A cycle of 20 to 24 h gave 175 cells and a radius of 6.65 at 48 h. That is a 4.9-fold increase in 48 h, or a doubling time of about 21 h.
- **A smaller patch.** A 3 by 3 start gave 132 cells at 48 h (from 9 cells) and a radius of 5.57.
- **Spring stiffness.** Stiffness 5, 15 and 20 all gave 477 cells, because the count depends only on the cell cycles. The radii were 10.05, 11.12 and 10.69. The stiffness changes how cells push each other apart, but with one seed the order is not monotonic, so treat the difference as noise.

## Pitfalls

- **Stiff springs break the time step.** Stiffness 40 stopped the run after 42 h with "Cells are moving by 2.00776, which is more than the AbsoluteMovementThreshold". With seed 7, stiffness 25 and 30 failed in the first hour, although both ran with seed 42. The recipe limits stiffness to 20.
- **Cell number grows exponentially.** A 2 by 2 patch with a 4 to 5 h cycle for 72 h reaches about 262,000 cells and did not finish in 6 minutes before it was killed. The recipe rejects runs that are expected to exceed 6000 cells, and also rejects a maximum cycle that is not above the minimum.
- **No contact inhibition.** Colonies grow without limit. Add a cell-cycle model that depends on neighbours, or a boundary, before comparing with an experiment.
- **Chaste warnings are not errors.** A line such as "Triangle has produced a zero area (collinear) element" can appear in `run_log.txt`. The run still ends with a "done:" line.
- **Lengths have no physical unit.** Scale by the real cell diameter yourself.

## Further reading

- Documentation and tutorials: https://chaste.github.io/
- Source: https://github.com/Chaste/Chaste
- Cooper FR, et al. (2020). Chaste: Cancer, Heart and Soft Tissue Environment. J Open Source Softw 5(47):1848. https://doi.org/10.21105/joss.01848
- Meineke FA, Potten CS, Loeffler M (2001). Cell migration and organization in the intestinal crypt using a lattice-free model. Cell Prolif 34:253-266. https://doi.org/10.1046/j.0960-7722.2001.00216.x

---

Cite: Cooper FR, et al. (2020). Chaste: Cancer, Heart and Soft Tissue Environment. Journal of Open Source Software 5(47):1848. doi:10.21105/joss.01848

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/chaste).
