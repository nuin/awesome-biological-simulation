# OpenDrift

> Drift a cloud of surface particles under constant current, wind and horizontal diffusion with the OceanDrift model, and write NetCDF trajectories and a summary checked against the hand-computed displacement.

Licence: GPL-2.0 · [Source code](https://github.com/OpenDrift/opendrift)

## What it simulates

OpenDrift is a Python framework for trajectory modelling in the ocean and atmosphere. A model moves a cloud of elements (particles) with the local current, the wind and random turbulence, one time step at a time. It reads the forcing from reader objects (ocean model files, wind files, a landmask) or from constants. Subclasses add physics for oil, fish eggs, plastic, icebergs and search and rescue.

The recipe uses the generic `OceanDrift` model with constant forcing and no data files. That keeps the example small and lets you check the answer by hand. The helper script `run_opendrift.py` releases a Gaussian cloud, drifts it for a number of hours and compares the centroid with the displacement from the formula (current + windage x wind) x time.

## When to use it

Use OpenDrift to follow material that floats or drifts at the surface, with wind drag on top of the current, and to run an ensemble from uncertain forcing.

- Use [Parcels](parcels.md) when you have a gridded velocity field and want control over the integration scheme and the grid interpolation.
- Use [Agents.jl](agents-jl.md) or [AgentPy](agentpy.md) for particles that follow behaviour rules or interact.

## Install it yourself

OpenDrift installs from conda-forge:

```
micromamba create -n opendrift -c conda-forge opendrift=1.14.12
```

This resolved on linux-aarch64 with Python 3.11. In the 1.14.12 image, `opendrift.__version__` printed 1.14.11. The package pulls in a large scientific stack: importing `opendrift.models.oceandrift` raised the process to 1,570 MB of resident memory, and the example peaked at 2,535 MB. For real work, add reader files with `o.add_reader(...)`.

## Run the tested example

This recipe builds OpenDrift in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 10.1 s.

1. Download [opendrift-recipe.tar.gz](https://biosimhub.pages.dev/guides/opendrift/opendrift-recipe.tar.gz) (Dockerfile, run_opendrift.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf opendrift-recipe.tar.gz
   cd opendrift
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/opendrift:1.14.12 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/opendrift:1.14.12 python /opt/run_opendrift.py --particles 500 \
    --lon 4.5 --lat 60 --radius 100 --hours 24 \
    --step-minutes 10 --current-u 0.2 --current-v 0 \
    --wind-u 0 --wind-v 0 --windage 0.02 --diffusivity 0 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `drift.nc` | 124.6 KB |
| `final_positions.csv` | 11.5 KB |
| `run_log.txt` | 93 B |
| `summary.csv` | 229 B |

<details><summary>First lines of <code>final_positions.csv</code></summary>

```
id,lon,lat
0,4.810575,60.000828
1,4.809445,60.001709
2,4.810826,59.998741
3,4.812411,60.0005
4,4.809252,59.999413
5,4.809254,59.999557
6,4.812502,59.999466
7,4.811045,59.999222
8,4.808836,60.000038
9,4.810643,59.999249
10,4.808849,60.00024
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: 500 particles, 24 h, centroid moved 17281 m east and 3 m north (expected 17280 m, 0 m)
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
metric,value
particles,500
hours,24.0
centroid_east_m,17280.69921875
centroid_north_m,3.0
expected_east_m,17280.0
expected_north_m,0.0
spread_east_m,98.0
spread_north_m,97.7
final_centroid_lon,4.80969
final_centroid_lat,60.00003
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--particles` | Number of particles | 500 | 1 to 5000 |
| `--lon` | Release longitude | 4.5 | -180 to 180 |
| `--lat` | Release latitude | 60 | -80 to 80 |
| `--radius` | Release radius (m) | 100 | 0 to 50000 |
| `--hours` | Run length (hours) | 24 | 1 to 240 |
| `--step-minutes` | Time step (minutes) | 10 | 1 to 120 |
| `--current-u` | Eastward current (m/s) | 0.2 | -3 to 3 |
| `--current-v` | Northward current (m/s) | 0 | -3 to 3 |
| `--wind-u` | Eastward wind (m/s) | 0 | -40 to 40 |
| `--wind-v` | Northward wind (m/s) | 0 | -40 to 40 |
| `--windage` | Wind drift factor (fraction of wind speed) | 0.02 | 0 to 0.1 |
| `--diffusivity` | Horizontal diffusivity (m2/s) | 0 | 0 to 1000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example releases 500 particles at 4.5 E, 60 N with a Gaussian radius of 100 m. A constant eastward current of 0.2 m/s acts for 24 hours with a 10 minute step. The wind is 0, so the windage has no effect. The run took 10.1 s.

- `run_log.txt` has the line "done: 500 particles, 24 h, centroid moved 17281 m east and 3 m north (expected 17280 m, 0 m)".
- `final_positions.csv` has one row per particle with `id`, `lon` and `lat`, for example particle 0 at 4.810575 E, 60.000828 N.
- `summary.csv` compares simulation and formula. The centroid moved 17,280.7 m east and 3.0 m north against 17,280.0 m and 0 m expected. The cloud spread is 98.0 m east-west and 97.7 m north-south, the same as the release radius, because nothing spreads the cloud yet. The final centroid is 4.80969 E, 60.00003 N.
- `drift.nc` (127,541 bytes) is OpenDrift's own NetCDF output, hourly. Open it with `xarray.open_dataset`.

The check is plain arithmetic: 0.2 m/s x 86,400 s = 17,280 m. The centroid matches within 1 m, so the advection and the conversion from metres to degrees both work. The helper converts degrees with WGS84 constants at the release latitude. A spherical conversion left the result 0.4% short in an earlier test.

## Your own runs

Each run changes one or two settings from the example and used seed 42 unless noted.

- **Wind.** `--wind-u 10 --wind-v 5 --windage 0.03` moved the centroid 43,276.8 m east and 12,962.2 m north. The formula gives (0.2 + 0.03 x 10) x 86,400 = 43,200 m east and 0.03 x 5 x 86,400 = 12,960 m north. Wind at 3% of its speed adds 0.3 m/s east and 0.15 m/s north to the drift.
- **Diffusion.** `--diffusivity 10` (10 m2/s) raised the spread to 1,312.7 m east-west and 1,316.3 m north-south. Theory for a random walk is sqrt(2 K t) = sqrt(2 x 10 x 86,400) = 1,315 m. The centroid still moved 17,316 m east. With `--seed 43` the spread was 1,323.8 m and 1,292.2 m, and the centroid was 84.6 m south of the release latitude.
- **More diffusion.** `--diffusivity 100 --particles 2000` gave a spread of 4,218.7 m and 4,244.2 m. Theory gives 4,157 m, and 2,000 particles agree within 2%.
- **Northward current, other latitude.** `--current-u 0 --current-v 0.5 --hours 48 --lat 45` gave 86,397.3 m north and 0.7 m east, against 86,400 m expected. The final latitude was 45.77743 N.

## Pitfalls

- **Memory.** A limit of 2,048 MB killed the example with exit code 137 (out of memory). The recipe uses 3,072 MB. The container is killed without a Python error message.
- **Constant forcing is a test, not an ocean.** The recipe applies one current everywhere. Real forcing needs reader files with time and space variation, and a landmask. The recipe turns the automatic landmask off so the run needs no network or coastline data.
- **Diffusion scales with the square root of time.** Spread grows as sqrt(2 K t), so 4 times the duration gives 2 times the spread.
- **Windage is a fraction of wind speed.** The recipe default is 0.02, and the allowed range is 0 to 0.1. A drift factor of 0.03 gave the wind run above.
- **Release spread.** A 100 m Gaussian radius gives a 98 m spread at the start. Use a small radius when you want to see the diffusion cleanly.

## Further reading

- OpenDrift documentation: https://opendrift.github.io
- Source: https://github.com/OpenDrift/opendrift
- Paper: Dagestad K-F, Roehrs J, Breivik O, Adlandsvik B (2018) OpenDrift v1.0: a generic framework for trajectory modelling. Geoscientific Model Development 11:1405-1420. https://doi.org/10.5194/gmd-11-1405-2018

---

Cite: Dagestad K-F, Roehrs J, Breivik O, Adlandsvik B (2018). OpenDrift v1.0: a generic framework for trajectory modelling. Geoscientific Model Development 11:1405-1420. doi:10.5194/gmd-11-1405-2018

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/opendrift).
