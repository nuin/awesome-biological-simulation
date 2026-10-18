# tyssue

> Relax a planar epithelium vertex model (line tension, contractility, area elasticity) to its energy minimum and return cell geometry and a picture.

Licence: GPL-3.0 · [Source code](https://github.com/DamCB/tyssue)

## What it simulates

tyssue is a Python library for mechanical models of epithelia. Its main focus is vertex models. A vertex model draws a sheet of cells as polygons that share corners (vertices). Each cell has an area, a perimeter and edges. An energy function sums the mechanical terms. The solver moves the vertices to lower that energy.

The example builds a flat sheet from a 6 by 6 grid, trims the border cells, and gets 20 cells with 38 vertices and 100 half-edges. It then applies three energy terms and relaxes the sheet to a local energy minimum:

- **Line tension** on every edge, with random noise on each edge.
- **Perimeter contractility** per cell.
- **Area elasticity**, which pulls each cell toward a preferred area.

The key assumption is that the tissue is a 2D sheet at the apical surface, in a quasi-static state. The solver finds an energy minimum. It does not follow time. The result is the shape of the sheet at that minimum.

## When to use it

Use tyssue to ask how cell-level mechanics set tissue shape:

- How do tension and contractility change cell area and the number of sides?
- Where does the sheet settle for a given set of parameters?
- Which cells shrink first when a few edges are stiffer?

On biosimhub, [pyafv](pyafv.md) models cells as active Voronoi cells that can detach and move, which fits migrating or fragmenting tissue. [Artistoo](artistoo.md) fits cells that deform and crawl on a pixel grid. tyssue fits a fixed network of polygons with a defined energy.

## Install it yourself

The conda-forge package is `tyssue`. The dry run `micromamba create -n t --dry-run -c conda-forge -c bioconda tyssue=0.9.0` resolves tyssue 0.9.0 with Python 3.9.23.

```
conda create -n tyssue -c conda-forge python=3.9 "numpy<2" "pandas<2" scipy matplotlib-base pytables quantities
conda activate tyssue
conda install -c conda-forge --no-deps tyssue=0.9.0
```

The recipe's image pins `numpy<2` and `pandas<2`. tyssue 0.9.0 still calls `DataFrame.append`, which pandas marks as deprecated. The minimal script below is the recipe's helper script without the CSV and plot code. It uses tyssue's own API:

```python
from tyssue import Sheet
from tyssue.dynamics import effectors, model_factory
from tyssue.geometry.sheet_geometry import SheetGeometry as geom
from tyssue.solvers.quasistatic import QSSolver

sheet = Sheet.planar_sheet_3d("epithelium", nx=6, ny=6, distx=1.0, disty=1.0)
sheet.sanitize(trim_borders=True, order_edges=True)
geom.update_all(sheet)
sheet.update_specs({
    "edge": {"is_active": 1, "line_tension": 0.12},
    "face": {"is_alive": 1, "contractility": 0.04, "prefered_area": 1.0,
             "area_elasticity": 1.0, "prefered_vol": 1.0, "vol_elasticity": 0.0},
    "vert": {"is_active": 1},
}, reset=True)
geom.update_all(sheet)
model = model_factory([effectors.LineTension, effectors.FaceContractility,
                       effectors.FaceAreaElasticity])
res = QSSolver().find_energy_min(sheet, geom, model)
```

## Run the tested example

This recipe builds tyssue in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 2.5 s. tyssue has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [tyssue-recipe.tar.gz](https://biosimhub.pages.dev/guides/tyssue/tyssue-recipe.tar.gz) (Dockerfile, run_tyssue.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf tyssue-recipe.tar.gz
   cd tyssue
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/tyssue:0.9.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/tyssue:0.9.0 python /opt/run_tyssue.py --nx 6 --ny 6 --line_tension 0.12 \
    --contractility 0.04 --area_elasticity 1 --prefered_area 1 \
    --tension_noise 0.3 --seed 42 > out/tyssue_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `faces.csv` | 2.1 KB |
| `tissue.png` | 40.5 KB |
| `tyssue_log.txt` | 184 B |
| `vertices.csv` | 1.6 KB |

<details><summary>First lines of <code>faces.csv</code></summary>

```
face,x,y,z,num_sides,area,perimeter,area_before,perimeter_before
0,1.4461743027922045,1.594321003088373,0.0,4,0.3973141732340618,2.5992142233611757,0.5,3.118033988749895
1,2.140127713028317,1.4481599532585803,0.0,5,0.5704570110071464,3.004948049229293,0.875,3.618033988749895
2,2.960077890449565,1.4563004496183578,0.0,5,0.5679843964307245,2.9208290098828202,0.875,3.618033988749895
3,3.7452782829737408,1.5420420285442824,0.0,5,0.5232244064713104,2.847221326529319,0.875,3.618033988749895
4,4.286068244913458,1.5885846034236277,0.0,3,0.2221548207615831,2.185507804243771,0.1875,2.4270509831248424
5,1.1429710078934872,2.1635623753914217,0.0,4,0.4385191328025162,2.743690977181359,0.5,3.118033988749895
6,1.786187635042718,2.1629884809355073,0.0,6,0.5342358000041688,2.7529708422380796,1.0,3.73606797749979
7,2.543174006106908,2.1061412729383795,0.0,6,0.5600149244651911,2.795190441045679,1.0,3.73606797749979
8,3.3526317264105483,2.1340755466278973,0.0,6,0.5734021365595661,2.826590131770921,1.0,3.73606797749979
9,4.183185835483529,2.159217842468147,0.0,6,0.60010786507298,2.975949352735045,1.0,3.73606797749979
10,1.3117593627586541,2.896559868225618,0.0,6,0.6203976775001425,3.0170587071141766,1.
```

</details>

<details><summary>First lines of <code>tyssue_log.txt</code></summary>

```
C++ extension are not available for this version
20 cells, 38 vertices, 100 half-edges
energy 10.08372 -> 8.92660, solver success: True
mean area 0.7812 -> 0.5042; sd 0.2769 -> 0.1275
```

</details>

<details><summary>First lines of <code>vertices.csv</code></summary>

```
vert,x,y,z
0,0.7752737637709365,2.574332322916486,0.0
1,1.6762774412378028,3.081939049250525,0.0
2,2.5023157224478085,2.5635450157345008,0.0
3,0.894955864866123,3.3295213072386356,0.0
4,1.4153794387662055,3.291575267511788,0.0
5,2.95498668356753,1.887270066708205,0.0
6,2.9212740306200047,2.3439943643545447,0.0
7,3.7747767788792768,2.342962637497827,0.0
8,3.3190132917587976,2.5966441258251245,0.0
9,3.3919625346736004,1.1148495320919476,0.0
10,3.3471418331580103,1.655838244039304,0.0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--nx` | Cells along x (grid) | 6 | 3 to 16 |
| `--ny` | Cells along y (grid) | 6 | 3 to 16 |
| `--line_tension` | Edge line tension (With the default elasticity, values of 0.25 and above shrink most cells to near-zero area while the solver still reports success.) | 0.12 | 0 to 2 |
| `--contractility` | Perimeter contractility | 0.04 | 0 to 2 |
| `--area_elasticity` | Area elasticity | 1 | 0.01 to 10 |
| `--prefered_area` | Preferred cell area | 1 | 0.1 to 5 |
| `--tension_noise` | Relative random noise on edge tension | 0.3 | 0 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe's helper script `run_tyssue.py` wraps the script above. It adds noise to the edge tensions (`line_tension *= 1 + noise * N(0,1)`, clipped to plus or minus 2), then writes files and a picture.

The log (`tyssue_log.txt`, 184 bytes) has three result lines. `20 cells, 38 vertices, 100 half-edges` is the sheet. `energy 10.08372 -> 8.92660, solver success: True` is the energy before and after the relaxation. `mean area 0.7812 -> 0.5042; sd 0.2769 -> 0.1275` is the cell area. The mean area is below the preferred area of 1 because line tension and contractility pull cells smaller. The spread of areas halves. The first log line, `C++ extension are not available for this version`, is a warning from the conda build.

`faces.csv` (2177 bytes) has one row per cell with `x,y,z,num_sides,area,perimeter` and the `area_before` and `perimeter_before` columns. Cell 0 has 4 sides and went from area 0.5 to 0.397. Cell 1 has 5 sides and went from 0.875 to 0.570. `vertices.csv` (1673 bytes) holds the 38 vertex positions, and `tissue.png` colors each polygon by area.

## Your own runs

Copy the docker run line from the recipe and change values.

1. **No noise.** Set `--tension_noise 0`. The energy went from 10.15994 to 9.00786. The mean area ended at 0.5014 and the standard deviation at 0.1203. Less variation in the starting tension gave a slightly lower spread of areas.
2. **Stronger tension.** Set `--line_tension 0.5`. The energy went from 22.93773 to 10.04602 and the solver still reported success. Mean area and its standard deviation both printed 0.0000. The cells collapsed.
3. **Bigger sheet.** Set `--nx 10 --ny 10`. The log reads `72 cells, 142 vertices, 396 half-edges` and `energy 36.22168 -> 31.07401`. The mean area went from 0.8976 to 0.5393. The recipe accepts 3 to 16 cells per side.

## Pitfalls

- **Solver success can hide collapsed cells.** The line tension 0.5 run reported `solver success: True` with zero-area cells. Check `area` in `faces.csv`.
- **The final area differs from the preferred area.** With the defaults, the mean area ended at 0.50 against a preferred 1.0. Raise `--prefered_area` or lower the tension to move it back. The parameter name is spelled `prefered_area`, as in tyssue.
- **Border cells are removed.** A 6 by 6 grid gives 20 cells. Count cells in `faces.csv`.
- **The seed drives only the noise.** In the helper it sets the random edge tensions. Compare runs at one seed.
- **pandas version.** The recipe's image pins `pandas<2`. The log prints `FutureWarning` lines about `DataFrame.append` and `level=` arguments from tyssue 0.9.0. Keep the pins from the install section.

## Further reading

- Documentation: https://tyssue.readthedocs.io/en/latest/
- Source and README: https://github.com/DamCB/tyssue
- Theis S, Suzanne M, Gay G (2021). Tyssue, an epithelium simulation library. J Open Source Softw 6(62):2973. https://doi.org/10.21105/joss.02973

---

Cite: Theis S, Suzanne M, Gay G (2021). Tyssue, an epithelium simulation library. Journal of Open Source Software 6(62):2973. doi:10.21105/joss.02973

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/tyssue).
