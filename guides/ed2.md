# ED2 (Ecosystem Demography)

> Run the Ecosystem Demography model on a 4-patch temperate forest stand at 44.5 N with synthetic weather, and get monthly carbon fluxes, leaf area and biomass.

Licence: CC-BY-4.0 · [Source code](https://github.com/EDmodel/ED2)

## What it simulates

ED2 (Ecosystem Demography model, version 2) simulates a forest as a set of patches, each holding cohorts of trees. A cohort is a group of identical trees of one plant functional type (PFT) and one size. Light, water and carbon are computed for every cohort at a short time step (30 minutes in this recipe). Over longer steps, trees grow, die, reproduce and move between size classes, and patches are disturbed.

Each cohort has leaf, sapwood, root and storage pools. Photosynthesis is computed per cohort, and the canopy shades itself layer by layer. Soil temperature, soil water and snow are solved in layers under the canopy. The outputs are carbon, water and energy fluxes, leaf area index (LAI) and biomass.

The example is a 6-month point simulation at 44.5 N, 71.5 W (New Hampshire) starting on 1 April 2004. The stand has 4 patches and 20 cohorts of five PFTs: early, mid and late hardwoods, late conifers and northern pines. The initial basal area is about 31 m2/ha, with 1321 stems per hectare. The weather is synthetic: a generator writes hourly temperature, radiation, rain, humidity and wind in ED2's HDF5 format, with a mean annual temperature near 6 C and 764 mm of rain in the first weather year (seed 1). The numbers are for learning how the model responds, not for predicting a site.

## When to use it

Use ED2 to ask how forest carbon uptake, water use and biomass respond to temperature, rain and CO2 when tree size structure and competition for light matter.

- Use [NicheMapR](nichemapr.md) for a single animal in a microclimate. ED2 has no animals.
- For population genetics, use [SLiM](slim.md) or [msprime](msprime.md).
- A real study needs observed weather, an inventory of the site and soil data. This recipe supplies none of those.

## Install it yourself

ED2 is Fortran 90 and is not packaged on conda-forge. The repository's `Dockerfile.gnu` builds it on Ubuntu 22.04 with gfortran, OpenMPI and HDF5:

```
git clone https://github.com/EDmodel/ED2.git
cd ED2/ED/build
./install.sh -k E -g -p docker.gnu     # needs libhdf5-openmpi-dev, mpif90, BLAS and LAPACK
```

The binary is `ed_*-opt` in the build folder and takes a namelist: `ed2 -f ED2IN`. The recipe's image pins commit 0a57f1b and is 231 MB. It sets `OMP_NUM_THREADS=1` to match the one-CPU job limit.

## Run the tested example

This recipe builds ED2 (Ecosystem Demography) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 32 s.

1. Download [ed2-recipe.tar.gz](https://biosimhub.pages.dev/guides/ed2/ed2-recipe.tar.gz) (Dockerfile, ED_MET_DRIVER_HEADER.in, genmet.c, init, run_ed2.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf ed2-recipe.tar.gz
   cd ed2
   sh run.sh
   ```

![Terminal recording of the ED2 (Ecosystem Demography) example run](https://biosimhub.pages.dev/media/ed2/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/ed2:2.2.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/ed2:2.2.0 bash /opt/run_ed2.sh --months 6 --warming 0 \
    --precip 1 --co2 370 --soil 5 --seed 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `ed2.log` | 12.1 KB |
| `monthly.csv` | 642 B |
| `run_log.txt` | 159 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/ed2/result-dark.png"><img src="https://biosimhub.pages.dev/media/ed2/result.png" alt="Plot of the ED2 (Ecosystem Demography) example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>ed2.log</code></summary>

```
 [+] Load_Ed_Ecosystem_Params...
----------------------------------------
  Treefall disturbance parameters:
  - LAMBDA_REF  =  1.25000E-02
  - LAMBDA_EFF  =  1.25000E-02
  - TIME2CANOPY =  0.00000E+00
----------------------------------------
 [+] Checking for XML config...
==================================================
==================================================
   WARNING! WARNING! WARNING! WARNING! WARNING!   
--------------------------------------------------
```

</details>

<details><summary>First lines of <code>monthly.csv</code></summary>

```
year,month,air_temp_c,precip_mm_day,gpp_kgc_m2_yr,npp_kgc_m2_yr,plant_resp_kgc_m2_yr,het_resp_kg_m2_yr,nep_kg_m2_yr,transp_mm_day,lai,agb_kgc_m2
2004,4,5.51,1.46,0.565265,0.181482,0.383782,0.111148,0.0703343,0.205,1.41976,5.88011
2004,5,12.17,2.42,1.48008,0.904771,0.575305,0.517228,0.387543,0.683,2.25037,6.1067
2004,6,16.85,1.14,2.64627,1.84223,0.804038,0.544239,1.29799,1.471,4.57814,6.03259
2004,7,18.90,3.15,2.59615,1.66969,0.926463,0.99852,0.67117,1.476,4.54179,6.03014
2004,8,17.13,1.26,2.29154,1.4517,0.839841,0.805177,0.646522,1.246,4.50075,6.02774
2004,9,12.71,1.75,1.58459,0.944563,0.640022,0.275709,0.668854,0.770,4.46452,6.02231
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
2004: rain 764 mm (before scaling)
2005: rain 787 mm (before scaling)
done: 6 monthly means from 2004-04, 183 days simulated, 5 patches, 43 cohorts at the end
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--months` | Simulated months (from 1 April 2004) | 6 | 1 to 18 |
| `--warming` | Air temperature offset (K) | 0 | -5 to 8 |
| `--precip` | Precipitation multiplier | 1 | 0.3 to 2 |
| `--co2` | Atmospheric CO2 (umol/mol) | 370 | 200 to 1000 |
| `--soil` | Soil texture class (1 sand, 2 loamy sand, 3 sandy loam, 4 silt loam, 5 loam, 6 sandy clay loam, 7 silty clay loam, 8 clay loam, 9 sandy clay, 10 silty clay, 11 clay) | 5 | 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11 |
| `--seed` | Weather seed | 1 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_ed2.sh` writes an `ED2IN` namelist from the parameters, generates the weather, runs `ed2` and converts the monthly HDF5 files to a table with `h5dump`. The run took 32 s.

- `run_log.txt` (159 bytes) reports the weather generator's rain totals and "done: 6 monthly means from 2004-04, 183 days simulated, 5 patches, 43 cohorts at the end". The stand went from 4 patches and 20 cohorts to 5 and 43 during the run.
- `monthly.csv` (642 bytes) has one row per month: air temperature, precipitation, GPP, NPP, plant and heterotrophic respiration, NEP, transpiration, LAI and above-ground biomass.
- `ed2.log` (12,343 bytes) is the last 300 lines of the model log.

Fluxes are monthly mean rates in kgC per m2 per year. GPP rises from 0.565 in April to 2.646 in June, 2.596 in July and 1.585 in September. July GPP of 2.6 kgC/m2/yr is about 7 gC/m2/day. LAI goes from 1.42 in April to 4.58 in June as the hardwoods leaf out, then stays near 4.5. Above-ground biomass is 5.88 kgC/m2 in April and 6.03 in September. NEP is positive in all 6 months, 0.07 in April and 1.30 in June.

## Your own runs

Each run changes one parameter from the example and took 33 to 34 s. Values below are monthly means over the 6 months.

- **Warming.** `--warming 4` raised mean air temperature from 11.9 to 15.3 C. April GPP rose from 0.565 to 0.670. June to September GPP fell, for example July from 2.596 to 2.470, and mean NEP fell from 0.535 to 0.296 as heterotrophic respiration rose from 0.465 to 0.560.
- **Drought.** `--precip 0.4` cut rain by 60 percent. GPP held through July (2.380 against 2.596), then fell to 1.227 in August and 0.220 in September, against 2.292 and 1.585. LAI fell from 4.46 to 4.16 by September.
- **Elevated CO2.** `--co2 700` raised mean GPP from 1.595 to 2.251 kgC/m2/yr and July GPP from 2.596 to 3.712. Transpiration fell in the same month, from 1.476 to 1.266 mm/day.

## Pitfalls

- **The weather is invented.** Compare scenarios with each other. Do not compare totals with a flux tower. The seed changes cloud and rain timing but not the climate.
- **Six months is the default for speed.** Twelve months of the same stand took 58 s on 1 CPU in testing. The recipe limits runs to 18 months.
- **Short runs show the growing season, not stand change.** Above-ground biomass moved from 5.88 to 6.03 kgC/m2 in the 6 months, so differences between scenarios are mostly in fluxes.
- **Soil input files can force TOPMODEL.** Initialisation mode 3 turns on the TOPMODEL lateral-flow hydrology, which stopped this stand with a "bad bf" error. The recipe uses mode 6, which leaves TOPMODEL off.
- **Three more inputs are mandatory.** The model needs a phenology file, a patch file and a cohort file for the site. The recipe supplies all three for the example stand.

## Further reading

- Source and Docker build: https://github.com/EDmodel/ED2
- Model wiki and namelist reference: https://github.com/EDmodel/ED2/wiki
- Medvigy D, Wofsy SC, Munger JW, Hollinger DY, Moorcroft PR (2009). Mechanistic scaling of ecosystem function and dynamics in space and time: Ecosystem Demography model version 2. J Geophys Res 114:G01002. https://doi.org/10.1029/2008JG000812

---

Cite: Medvigy D, Wofsy SC, Munger JW, Hollinger DY, Moorcroft PR (2009). Mechanistic scaling of ecosystem function and dynamics in space and time: Ecosystem Demography model version 2. Journal of Geophysical Research 114:G01002. doi:10.1029/2008JG000812

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/ed2).
