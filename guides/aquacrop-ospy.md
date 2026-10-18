# AquaCrop-OSPy

> Simulate crop growth, soil water balance and yield for one crop, soil and daily weather record with the FAO AquaCrop water-productivity model in Python.

Licence: Apache-2.0 · [Source code](https://github.com/aquacropos/aquacrop)

## What it simulates

AquaCrop-OSPy simulates how a crop uses water. It is a Python port of the AquaCrop-OS model, which follows the FAO AquaCrop model. You give it daily weather, a soil, a crop and a planting date. It returns canopy cover, biomass, root depth, soil water and yield for each season.

The model is water-driven. Biomass grows in proportion to transpiration, and yield is a harvest index times biomass. Water stress lowers canopy growth, stomatal conductance and the harvest index. You can leave the field rainfed or add irrigation rules. The soil is a stack of layers with a water balance for evaporation, runoff, drainage and capillary rise.

The authors state that it mirrors most features of FAO AquaCrop 7.1. Salinity stress, fertility stress, weed management and perennial herbaceous crops are not yet in it. It is not an official FAO release.

## When to use it

Use AquaCrop-OSPy to ask how yield responds to rainfall, irrigation depth or soil type for one field, or to compare irrigation rules over many seasons.

- Use [PCSE](pcse.md) when you want WOFOST or LINTUL models, which grow the crop from light and temperature and track nitrogen.
- Use [DSSAT-CSM](dssat-csm.md) when you need a crop-specific process model with cultivar coefficients and detailed soil carbon and nitrogen.
- Use [APSIM Next Generation](apsim-next-generation.md) when you need a whole farming system with rotations, livestock or tree crops.

## Install

```
pip install aquacrop==3.1.0
```

PyPI lists aquacrop 3.1.0 as the current release. It is a pure-Python wheel of about 10.7 MB that includes the example weather files. It needs Python 3.9 or later, numpy, pandas, tqdm, matplotlib and seaborn. The repository LICENSE is Apache-2.0, and the wheel carries the same text, although the PyPI classifier says MIT.

The README says that if you see "No module named aquacrop.scripts.initiate_library", you should run `python -m aquacrop.scripts.initiate_library`, or set `os.environ['DEVELOPMENT'] = 'DEVELOPMENT'` before importing aquacrop. Those notes date from the releases that used numba compilation, and the 3.1.0 source no longer depends on numba.

## A first run

Adapted from the [README](https://github.com/aquacropos/aquacrop#readme) and the [first notebook](https://aquacropos.github.io/aquacrop/notebooks/AquaCrop_OSPy_Notebook_1/). It grows winter wheat on a sandy loam with the bundled Tunis weather record.

```python
from aquacrop import AquaCropModel, Soil, Crop, InitialWaterContent
from aquacrop.utils import prepare_weather, get_filepath

weather_file_path = get_filepath('tunis_climate.txt')
model_os = AquaCropModel(
    sim_start_time="1979/10/01",
    sim_end_time="1985/05/30",
    weather_df=prepare_weather(weather_file_path),
    soil=Soil(soil_type='SandyLoam'),
    crop=Crop('Wheat', planting_date='10/01'),
    initial_water_content=InitialWaterContent(value=['FC']),
)
model_os.run_model(till_termination=True)
print(model_os.get_simulation_results())
```

## Run the tested example

This recipe builds AquaCrop-OSPy in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.7 s.

1. Download [aquacrop-ospy-recipe.tar.gz](https://biosimhub.pages.dev/guides/aquacrop-ospy/aquacrop-ospy-recipe.tar.gz) (Dockerfile, run_aquacrop.py, example weather.txt, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf aquacrop-ospy-recipe.tar.gz
   cd aquacrop-ospy
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/aquacrop-ospy:3.1.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/aquacrop-ospy:3.1.0 python /opt/run_aquacrop.py --weather /work/in/weather.txt \
    --crop Wheat --soil SandyLoam --start-year 1979 \
    --end-year 1985 --plant-month 10 --plant-day 1 \
    --end-month 5 --end-day 30 --smt 0 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `crop_growth.csv` | 246.8 KB |
| `run_log.txt` | 1.2 KB |
| `seasons.csv` | 635 B |
| `water_flux.csv` | 222.5 KB |

<details><summary>First lines of <code>crop_growth.csv</code></summary>

```
time_step_counter,season_counter,dap,gdd,gdd_cum,z_root,canopy_cover,canopy_cover_ns,biomass,biomass_ns,harvest_index,harvest_index_adj,DryYield,FreshYield,YieldPot
0.0,0.0,1.0,21.5,21.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
1.0,0.0,2.0,20.0,41.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
2.0,0.0,3.0,20.0,61.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
3.0,0.0,4.0,20.0,81.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
4.0,0.0,5.0,22.5,104.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
5.0,0.0,6.0,21.5,125.5,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
6.0,0.0,7.0,20.5,146.0,0.3,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
7.0,0.0,8.0,20.0,166.0,0.31429501214065503,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
8.0,0.0,9.0,21.5,187.5,0.346665127763267,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
9.0,0.0,10.0,23.5,211.0,0.3755580119871119,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
10.0,0.0,11.0,23.0,234.0,0.4021130549386273,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
crop=Wheat soil=SandyLoam seasons=6 irrigation_smt=0.0
 Season crop Type Harvest Date (YYYY/MM/DD)  Harvest Date (Step)  Dry yield (tonne/ha)  Fresh yield (tonne/ha)  Yield potential (tonne/ha)  Seasonal irrigation (mm)
      0     Wheat                1980-04-15                  196              8.940140                9.933489                    8.945246                         0
      1     Wheat                1981-04-16                  562              8.309577                9.232863                    8.314556                         0
      2     Wheat                1982-04-16                  927              9.136122               10.151246                    9.141264                         0
      3     Wheat                1983-04-16                 1292              8.811568                9.790631                    8.816327                         0
      4     Wheat                1984-04-15                 1657              8.682660                9.647400                    8.687385                         0
      5     Wheat                1985-04-16                 2023              8.925063                9.916737                    8.930517                 
```

</details>

<details><summary>First lines of <code>seasons.csv</code></summary>

```
Season,crop Type,Harvest Date (YYYY/MM/DD),Harvest Date (Step),Dry yield (tonne/ha),Fresh yield (tonne/ha),Yield potential (tonne/ha),Seasonal irrigation (mm)
0,Wheat,1980-04-15,196,8.940139992051638,9.933488880057375,8.945245964389658,0
1,Wheat,1981-04-16,562,8.309577107885946,9.232863453206607,8.314556160671174,0
2,Wheat,1982-04-16,927,9.136121791929964,10.151246435477738,9.141264043953123,0
3,Wheat,1983-04-16,1292,8.811568263004462,9.79063140333829,8.816326641857502,0
4,Wheat,1984-04-15,1657,8.682660046213236,9.64740005134804,8.687385444728276,0
5,Wheat,1985-04-16,2023,8.925063176721025,9.916736863023361,8.930517288425316,0
```

</details>

<details><summary>First lines of <code>water_flux.csv</code></summary>

```
time_step_counter,season_counter,dap,Wr,z_gw,surface_storage,IrrDay,Infl,Runoff,DeepPerc,TileDrain,CR,GwIn,Es,EsPot,Tr,TrPot
0.0,0.0,1.0,63.08,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,2.9223537809004467,3.74,0.0,0.0
1.0,0.0,2.0,61.31,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.7703616568708913,3.3000000000000003,0.0,0.0
2.0,0.0,3.0,59.980000000000004,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.3300274259348617,3.19,0.0,0.0
3.0,0.0,4.0,58.65,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.3275990973529077,3.9600000000000004,0.0,0.0
4.0,0.0,5.0,57.56,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.0863545719718577,3.9600000000000004,0.0,0.0
5.0,0.0,6.0,56.79,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7740321885941913,3.3000000000000003,0.0,0.0
6.0,0.0,7.0,55.76,,0.0,0.0,1.2,0.0,0.0,0.0,0.0,0.0,2.2306987915473995,3.08,0.0,0.0
7.0,0.0,8.0,56.74,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.2181611399036816,2.8600000000000003,0.0,0.0
8.0,0.0,9.0,64.43,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,1.114384656684353,3.4100000000000006,0.0,0.0
9.0,0.0,10.0,70.09,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.9366680155680653,3.63,0.0,0.0
10.0,0.0,11.0,73.78999999999999,,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.7028694423823987,3.3000000000000003,0.0,0.0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--crop` | Crop | Wheat | Wheat, Maize, Potato, Barley, Cotton, Sorghum, Soybean, Sunflower, Tomato, SugarBeet |
| `--soil` | Soil texture class | SandyLoam | Sand, LoamySand, SandyLoam, Loam, SiltLoam, Silt, SandyClayLoam, ClayLoam, SiltClayLoam, SandyClay, SiltClay, Clay |
| `--start-year` | First year (planting year) | 1979 | 1979 to 2001 |
| `--end-year` | Last year (year of the final harvest) | 1985 | 1980 to 2002 |
| `--plant-month` | Planting month | 10 | 1 to 12 |
| `--plant-day` | Planting day | 1 | 1 to 28 |
| `--end-month` | Simulation end month | 5 | 1 to 12 |
| `--end-day` | Simulation end day | 30 | 1 to 31 |
| `--smt` | Irrigation soil-moisture target (percent of TAW | 0 | 0 to 100 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`get_simulation_results()` returns one row per season. Its columns are Season, crop Type, Harvest Date (YYYY/MM/DD), Harvest Date (Step), Dry yield (tonne/ha), Fresh yield (tonne/ha), Yield potential (tonne/ha) and Seasonal irrigation (mm). A rainfed run shows 0 mm irrigation. Compare dry yield with yield potential to see how much water stress cost.

The recipe's helper script writes that table to `seasons.csv`, and it adds two daily tables.

- `crop_growth.csv` has one row per day with growing degree days, root depth (z_root), canopy cover with and without stress, biomass, harvest index and the running yield columns.
- `water_flux.csv` has one row per day with irrigation (IrrDay), infiltration, runoff, deep percolation, soil evaporation (Es) and transpiration (Tr), each with its potential value (EsPot, TrPot).

Dry years show up as a gap between Tr and TrPot, then as a gap between dry yield and yield potential. The recipe's `run_log.txt` repeats the season table.

## Pitfalls

- **The weather file has a fixed layout.** `prepare_weather` reads seven whitespace-separated columns: day, month, year, minimum and maximum temperature, precipitation and reference evapotranspiration. It asserts the count. Compute ET0 yourself, because the model does not derive it from radiation or wind.
- **The simulation window must cover the weather.** The bundled Tunis file runs from 1979 to 2002. The model needs a weather row for every simulated day, so keep the start and end dates inside that range.
- **Start the simulation on the planting date.** The notebook uses the same month and day for both. The recipe's helper does the same, so a start year and a planting date define the first season.
- **Crop names matter.** `Wheat` runs on calendar days. `WheatGDD` runs on growing degree days and needs temperatures to match.
- **The recipe caps the planting day at 28.** That avoids invalid dates in short months; keep the end day valid for its month too.
- **Irrigation needs a rule.** Without an `IrrigationManagement` object the field is rainfed. The recipe's soil-moisture target sets method 1 for every growth stage.
- **Results are for one field.** Spatial variation, pests and management beyond the listed options are outside the model.

## Further reading

- Documentation: https://aquacropos.github.io/aquacrop/
- Source: https://github.com/aquacropos/aquacrop
- PyPI: https://pypi.org/project/aquacrop/
- Paper: Kelly T, Foster T (2021). AquaCrop-OSPy: Bridging the gap between research and practice in crop-water modeling. Agricultural Water Management 254:106976. https://doi.org/10.1016/j.agwat.2021.106976
- FAO AquaCrop: https://www.fao.org/aquacrop

---

Cite: Kelly T, Foster T (2021). AquaCrop-OSPy, bridging the gap between research and practice in crop-water modeling. Agricultural Water Management 254:106976. doi:10.1016/j.agwat.2021.106976

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/aquacrop-ospy).
