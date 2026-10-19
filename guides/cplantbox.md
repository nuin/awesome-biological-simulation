# CPlantBox

> Grow a three-dimensional root system from a species parameter set and write its geometry, growth curve and per-order statistics.

Licence: GPL-3.0 · [Source code](https://github.com/Plant-Root-Soil-Interactions-Modelling/CPlantBox)

## What it simulates

CPlantBox grows a plant architecture in 3D, one organ at a time. The example grows only a root system. A seed produces a primary root. Each root elongates, bends toward gravity, and sprouts lateral roots of the next order at set spacings. A parameter set gives, for each root order, the maximal length, the growth rate, the spacing of laterals, the radius, the insertion angle and the strength of gravitropism. Each value has a mean and a standard deviation, so the seed changes the architecture.

The output is a set of root segments with positions, radii and creation times. From these you compute total length, surface, volume, depth and spread. The same engine also grows stems and leaves, and the CPlantBox project couples the plant to water flow, carbon transport and soil models. This recipe uses the structural part only.

Units are centimetres and days. The model has no soil, so roots grow in free space with gravitropism alone.

## When to use it

Use CPlantBox to generate virtual root systems of known species and ask what architecture traits do:

- How much root length and depth does a species reach in 30 days?
- What does a longer inter-lateral distance or weaker gravitropism change?
- Which root order carries most of the length?

It also produces input geometry for water-uptake and soil models. This recipe does not model water flow, carbon or soil.

## Install it yourself

Wheels are on PyPI for Linux x86_64, macOS arm64 and Windows, for Python 3.11 to 3.14:

```
python3 -m venv cpb && . cpb/bin/activate
pip install cplantbox==2.1.1
```

The package declares NumPy, SciPy and Matplotlib as dependencies. The recipe's image installs only `cplantbox` and `numpy` (`--no-deps`), which is enough for this script. The parameter sets ship inside the package, under `plantbox.data_path()`. A minimal run:

```python
import plantbox as pb

rs = pb.Plant()
rs.readParameters(pb.data_path() + "/structural/rootsystem/Anagallis_femina_Leitner_2010.xml")
rs.setSeed(1)
rs.initialize(False)
for day in range(30):
    rs.simulate(1, False)
print(pb.SegmentAnalyser(rs).getSummed("length"))
```

This printed 937.9 (cm). The recipe's image uses linux/amd64, because the Linux wheels are x86_64 only.

## Run the tested example

This recipe builds CPlantBox in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.4 s. CPlantBox has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [cplantbox-recipe.tar.gz](https://biosimhub.pages.dev/guides/cplantbox/cplantbox-recipe.tar.gz) (Dockerfile, run_cplantbox.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf cplantbox-recipe.tar.gz
   cd cplantbox
   sh run.sh
   ```

![Terminal recording of the CPlantBox example run](https://biosimhub.pages.dev/media/cplantbox/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/cplantbox:2.1.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/cplantbox:2.1.1 python /opt/run_cplantbox.py --plant Anagallis_femina_Leitner_2010 \
    --days 30 --lmax_scale 1 --ln_scale 1 --tropism_scale 1 \
    --seed 1
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `growth.csv` | 844 B |
| `orders.csv` | 190 B |
| `roots.vtp` | 162.9 KB |
| `run_log.txt` | 113 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/cplantbox/result-dark.png"><img src="https://biosimhub.pages.dev/media/cplantbox/result.png" alt="Plot of the CPlantBox example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>growth.csv</code></summary>

```
day,length_cm,surface_cm2,volume_cm3
1,5.068,1.429,0.03328
2,18.721,4.101,0.08065
3,40.898,8.011,0.14218
4,73.401,13.294,0.21795
5,110.873,19.217,0.29980
6,153.316,25.798,0.38821
7,198.863,32.750,0.47963
8,247.180,40.029,0.57360
9,295.412,47.293,0.66702
10,341.729,54.312,0.75760
11,389.519,61.493,0.84920
```

</details>

<details><summary>First lines of <code>orders.csv</code></summary>

```
subType,name,organs,length_cm,mean_length_cm
1,primaryroot,1,32.481,32.481
2,1storderlaterals,37,297.812,8.049
3,2ndorderlaterals,494,216.488,0.438
4,3rdorderlaterals,984,391.133,0.397
```

</details>

<details><summary>First lines of <code>roots.vtp</code></summary>

```
<?xml version="1.0"?><VTKFile type="PolyData" version="0.1" byte_order="LittleEndian">
<PolyData>
<Piece NumberOfLines="3076" NumberOfPoints="3077">
<CellData Scalars=" CellData">
<DataArray type="Float32" Name="radius" NumberOfComponents="1" format="ascii" >
0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 0.05 
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Anagallis_femina_Leitner_2010: 30 days, 1516 roots, length 937.9 cm, max depth 34.5 cm, max radial spread 5.6 cm
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--plant` | Root-system parameter set | Anagallis_femina_Leitner_2010 | Anagallis_femina_Leitner_2010, Zea_mays_1_Leitner_2010, Brassica_napus_a_Leitner_2010, Lupinus_albus_Leitner_2014, Medicago_truncatula_Postma_2011, Triticum_aestivum_a_Bingham_2011 |
| `--days` | Simulation time (days) | 30 | 1 to 60 |
| `--lmax_scale` | Multiplier on maximal root length | 1 | 0.2 to 3 |
| `--ln_scale` | Multiplier on distance between laterals | 1 | 0.2 to 3 |
| `--tropism_scale` | Multiplier on tropism strength | 1 | 0 to 3 |
| `--seed` | Seed | 1 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_cplantbox.py` scales three groups of parameters, simulates day by day, and writes four files.

- `run_log.txt`: "30 days, 1516 roots, length 937.9 cm, max depth 34.5 cm, max radial spread 5.6 cm". The parameter set is Anagallis femina (Leitner 2010).
- `growth.csv` has one row per day with total root length, surface and volume. Length is 5.1 cm on day 1, 341.7 cm on day 10, 744.2 cm on day 20 and 937.9 cm on day 30. Growth is 40 cm per day between days 10 and 20 and 19 cm per day between days 20 and 30.
- `orders.csv` has one row per root order. The primary root is 1 root of 32.5 cm. First-order laterals are 37 roots totalling 297.8 cm (mean 8.0 cm). Second-order laterals are 494 roots totalling 216.5 cm. Third-order laterals are 984 roots totalling 391.1 cm. The orders add up to the 1516 roots.
- `roots.vtp` (166,832 bytes) holds 3076 root segments with radius, order (`subType`) and creation time. Open it in ParaView to see the 3D system.

A plain-text check: the primary root of the parameter file has a maximal length of 33.4 cm, and the simulated root reached 32.5 cm. Because the model is stochastic, a single root differs from its mean.

## Your own runs

Each run changes one value from the example (Anagallis, 30 days, seed 1).

| Change | Roots | Length (cm) | Max depth (cm) | Max spread (cm) |
|---|---|---|---|---|
| Example | 1516 | 937.9 | 34.5 | 5.6 |
| Seed 2 | 1311 | 842.5 | 36.6 | 8.9 |
| 60 days | 1840 | 1127.6 | 47.3 | 5.6 |
| Maximal length x2 | 7361 | 6775.9 | 51.0 | 9.3 |
| Lateral spacing x2 | 345 | 368.3 | 40.7 | 4.7 |
| Tropism strength x0 | 1597 | 983.4 | 13.9 | 13.2 |

- **Maximal length x2.** Doubling every order's maximal length gave 7.2 times the total length. The primary root was 55.8 cm against 32.5 cm.
- **Lateral spacing x2.** Doubling the distance between laterals cut the root count to 345 and the length to 368 cm.
- **No gravitropism.** With the tropism multiplier at 0, the max depth fell to 13.9 cm and the radial spread rose to 13.2 cm. Roots no longer turn downward.
- **Other species.** Zea mays (Leitner 2010) gave 8748 roots, 9067.9 cm total length and a depth of 81.7 cm in 30 days. Brassica napus (Leitner 2010) gave 262 roots, 1519.2 cm and a depth of 96.8 cm, with 93.9 cm of tap root.
- **Repeats.** Two runs with seed 1 gave a byte-identical `roots.vtp`.

## Pitfalls

- **Root order labels vary by file.** In the maize file, subType 4 is named "primaryroot" and holds 30 roots of 77.9 cm on average (shoot-borne roots), and `orders.csv` prints the name from the file.
- **One seed is one plant.** Seeds 1 and 2 differ by 10% in total length. Run many seeds before you compare two parameter sets.
- **Growth levels off.** Doubling the time from 30 to 60 days added 20% length (937.9 to 1127.6 cm) for this species.
- **The parameter multipliers apply to all orders.** The helper scales every root order except the undefined type 0. For a single order, edit the parameters in Python.
- **A harmless message appears.** `Organism::organTypeNumber: unknown organ type name reference` is printed on load. The run is unaffected.

## Further reading

- Source and installation: https://github.com/Plant-Root-Soil-Interactions-Modelling/CPlantBox
- Tutorial scripts: `tutorial/examples/` in the repository, such as `example2f_sensitivity.py`
- Wheel build notes: `doxygen/wheels.md` in the repository
- Paper: Zhou X-R et al. (2020) CPlantBox, a whole-plant modelling framework for the simulation of water- and carbon-related processes. in silico Plants 2(1):diaa001. https://doi.org/10.1093/insilicoplants/diaa001

---

Cite: Zhou X-R, Schnepf A, Vanderborght J, Leitner D, Lacointe A, Vereecken H, Lobet G (2020). CPlantBox, a whole-plant modelling framework for the simulation of water- and carbon-related processes. in silico Plants 2(1):diaa001. doi:10.1093/insilicoplants/diaa001

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/cplantbox).
