# Parcels

> Track passive particles through an analytic Stommel gyre ocean flow with a chosen integration scheme, optional random-walk diffusion and a writable trajectory file.

Licence: MIT · [Source code](https://github.com/Parcels-code/Parcels)

## What it simulates

Parcels (Probabilistic Ocean Analysis Lagrangian Simulator) moves virtual particles through a gridded velocity field. Each particle is a point that drifts with the local current. At every time step an integration scheme turns the current at the particle position into a displacement. Typical uses are plastic debris, larvae, oil and floats in model or satellite ocean data.

The recipe runs Parcels 4.0.2 on an analytic flow, so it needs no data download. The flow is the Stommel gyre that Parcels ships for its own tests: a 10,000 km square basin with a narrow, fast western boundary current and a slow return flow in the interior. The helper script `run_parcels.py` releases particles at random inside a box, advects them for a number of days and writes their positions every 5 days.

## When to use it

Use Parcels to follow where passive material goes in a given current field, or to test how the integration scheme and time step change a trajectory.

- Use [OpenDrift](opendrift.md) when you need ready-made drift models for oil, fish eggs or search and rescue, with wind and wave drag built in.
- Use [Agents.jl](agents-jl.md) or [AgentPy](agentpy.md) when particles must interact with each other or follow behaviour rules.

## Install it yourself

Parcels installs from conda-forge:

```
micromamba create -n parcels -c conda-forge parcels=4.0.2
```

This resolved on linux-aarch64 (Python 3.11). The recipe image is 2.2 GB. The helper imports the flow generator `parcels._datasets.structured.generated.stommel_gyre_dataset`. It is a private module, so its path may change between Parcels versions. For real data, build the fieldset from your own NetCDF or Zarr files with `parcels.FieldSet.from_sgrid_conventions` or one of the `parcels.convert` functions, such as `nemo_to_sgrid`.

## Run the tested example

This recipe builds Parcels in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 6.6 s.

1. Download [parcels-recipe.tar.gz](https://biosimhub.pages.dev/guides/parcels/parcels-recipe.tar.gz) (Dockerfile, run_parcels.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf parcels-recipe.tar.gz
   cd parcels
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/parcels:4.0.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/parcels:4.0.2 python /opt/run_parcels.py --particles 200 \
    --x0 0.1 --x1 0.2 --y0 0.4 --y1 0.6 --days 200 \
    --dt-hours 6 --scheme rk4 --speed 1 --kh 0 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 145 B |
| `summary.csv` | 211 B |
| `trajectories.csv` | 311.4 KB |
| `trajectories.parquet` | 137.6 KB |

<details><summary>First lines of <code>run_log.txt</code></summary>

```
INFO: Output files are stored in trajectories.parquet
done: 200 of 200 particles alive after 200 days, mean displacement 1419 km (parcels 4.0.2)
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
metric,value
particles_released,200
particles_alive_at_end,200
mean_displacement_km,1418.7
max_displacement_km,3043.9
end_centroid_x_km,980.7
end_centroid_y_km,5557.8
end_spread_x_km,484.7
end_spread_y_km,997.4
```

</details>

<details><summary>First lines of <code>trajectories.csv</code></summary>

```
id,t,x,y
0,0.0,1.773956e+06,5.5548095e+06
1,0.0,1.4388785e+06,5.943653e+06
2,0.0,1.8585978e+06,5.0014825e+06
3,0.0,1.697368e+06,4.287795e+06
4,0.0,1.0941774e+06,4.0278725e+06
5,0.0,1.9756224e+06,4.459312e+06
6,0.0,1.7611398e+06,4.2636445e+06
7,0.0,1.7860642e+06,5.3553175e+06
8,0.0,1.1281136e+06,4.243665e+06
9,0.0,1.450386e+06,5.01266e+06
10,0.0,1.370798e+06,5.388525e+06
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--particles` | Number of particles | 200 | 1 to 5000 |
| `--x0` | Release box west edge (fraction of basin) | 0.1 | 0 to 0.99 |
| `--x1` | Release box east edge (fraction of basin) | 0.2 | 0.01 to 1 |
| `--y0` | Release box south edge (fraction of basin) | 0.4 | 0 to 0.99 |
| `--y1` | Release box north edge (fraction of basin) | 0.6 | 0.01 to 1 |
| `--days` | Run length (days) | 200 | 1 to 1000 |
| `--dt-hours` | Time step (hours) | 6 | 0.1 to 48 |
| `--scheme` | Advection scheme | rk4 | rk4, rk2, euler |
| `--speed` | Flow speed scale (1 = peak about 0.5 m/s) | 1 | 0.1 to 5 |
| `--kh` | Horizontal diffusivity Kh (m2/s | 0 | 0 to 10000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example releases 200 particles uniformly in a box that spans 10% to 20% of the basin in x (1,000 to 2,000 km) and 40% to 60% in y (4,000 to 6,000 km). It integrates 200 days with RK4 and a 6 hour step. The run took 6.6 s.

- `run_log.txt` has the line "done: 200 of 200 particles alive after 200 days, mean displacement 1419 km (parcels 4.0.2)".
- `trajectories.csv` has 8,200 rows: 200 particles at 41 output times (day 0 to day 200 every 5 days). Columns are `id`, `t` (seconds; the last is 17,280,000) and `x`, `y` in metres. `trajectories.parquet` (140,923 bytes) is the same data as written by Parcels.
- `summary.csv` lists the metrics. Mean displacement is 1418.7 km and the maximum is 3043.9 km. The cloud centroid ended at x 980.7 km, y 5557.8 km. The spread (standard deviation) is 484.7 km in x and 997.4 km in y.

The cloud started 1,000 km wide in x and 2,000 km tall in y. A gyre stretches and folds a cloud, which is why the y spread (997 km) is larger than the x spread (485 km). The particles moved about 1,419 km in 200 days, a mean net speed of 0.08 m/s. The flow speed scale of 1 gives peak boundary-current velocities near 0.5 m/s, so particles that stay in the interior move far slower than that.

## Your own runs

Each run changes one setting. Every run used the example's seed 42 and a fresh output directory.

- **Euler scheme.** `--scheme euler` with the 6 h step gave a mean displacement of 1531.5 km and a centroid at (1062.6, 5682.5) km. RK4 gave 1418.7 km. Euler is first order and drifts off the true streamlines. With `--dt-hours 24` Euler gave 2068.8 km, so the error grows with the step.
- **RK2 and RK4 at a 24 hour step.** RK4 gave 1418.7 km with a 24 h step, the same as with 6 h. RK2 gave 1421.7 km. The higher-order schemes tolerate a 4 times longer step here.
- **Diffusion.** `--kh 1000` (1000 m2/s of random walk on top of the current) gave a mean displacement of 1701.4 km and a y spread of 1228.3 km. `--kh 5000` gave 2378.8 km and a spread of 1839.8 km, and 6 of 200 particles left the basin and were deleted.
- **Faster flow.** `--speed 2` gave a mean displacement of 1508.5 km and a centroid at y 4654.9 km. Doubling the speed did not double the displacement, because the particles had been carried around the gyre by then.
- **Another release box.** A box at 40% to 50% in x and 10% to 20% in y gave a mean displacement of 8066.5 km. The particles went west, then north in the boundary current, and ended near y 9,028.6 km.
- **Another seed.** `--seed 43` gave 1440.2 km. The seed sets the release positions and the diffusion noise.

## Pitfalls

- **Large time steps with Euler.** Euler at 24 h overshot by 46% compared with RK4. Use RK4 unless you have a reason not to.
- **Diffusion changes the mean as well as the spread.** The Kh kernel adds a Wiener increment to each particle. The 200-particle mean displacement rose from 1418.7 km to 1701.4 km at Kh 1000, because spreading particles reach faster parts of the flow.
- **Particles can leave the domain.** The helper deletes particles that leave the grid, which the summary shows as `particles_alive_at_end`. Parcels would otherwise stop with an out-of-bounds error.
- **Do not reuse a deleted output folder in quick succession.** On a bind-mounted Docker volume, recreating the same directory right before a run made the parquet file fail to open in 3 of 8 runs. Fresh directories gave 0 failures in 8 runs.
- **Parcels 4 differs from version 3.** Output is Parquet, not Zarr, and the Python API has changed. Code written for 3.x needs porting.

## Further reading

- Parcels documentation: https://docs.parcels-code.org/en/latest/
- Source: https://github.com/Parcels-code/Parcels
- Paper: Lange M, van Sebille E (2017) Parcels v0.9: prototyping a Lagrangian ocean analysis framework for the petascale age. Geoscientific Model Development 10:4175-4186. https://doi.org/10.5194/gmd-10-4175-2017
- Paper: Delandmeter P, van Sebille E (2019) The Parcels v2.0 Lagrangian framework: new field interpolation schemes. Geoscientific Model Development 12:3571-3584. https://doi.org/10.5194/gmd-12-3571-2019

---

Cite: Lange M, van Sebille E (2017). Parcels v0.9: prototyping a Lagrangian ocean analysis framework for the petascale age. Geoscientific Model Development 10:4175-4186. doi:10.5194/gmd-10-4175-2017

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/parcels).
