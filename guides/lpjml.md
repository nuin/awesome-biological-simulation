# LPJmL

> Dynamic global vegetation, water and carbon model with crops, run here on the bundled two-grid-cell test data set.

Licence: AGPL-3.0-or-later · [Source code](https://github.com/PIK-LPJmL/LPJmL)

## What it simulates

LPJmL (Lund-Potsdam-Jena managed Land) is a dynamic global vegetation model written in C. The Potsdam Institute for Climate Impact Research (PIK) maintains it. It simulates natural vegetation, agriculture and hydrology on a grid, one cell at a time, with the carbon, water and nitrogen cycles linked. Natural plant types compete and change with climate. Crops, managed grassland and wood plantations are added through land-use input.

You run it with a configuration file in JSON-like syntax (`.cjson`). The file names the input data (climate, soil, land use and more), the output variables, the run settings and the years. Typical global runs have two parts. A spinup brings vegetation and soil carbon to equilibrium under cycled climate. A transient run then follows the observed years from the restart file the spinup wrote.

This site's recipe runs the model on the 2-cell test data set that ships with the code. That data set exists to test an installation. It does not support scientific conclusions.

## When to use it

Use LPJmL for questions about land-surface carbon and water at regional to global scale: how vegetation, crops and runoff respond to climate and land use. Global input data sets and a cluster are usual.

- Use [AquaCrop](aquacrop.md) when you need a field-scale crop yield model driven by daily weather and soil data.
- Use [NetLogo](netlogo.md) when you want to build a small ecological model with individual agents and no gridded forcing.
- Use LPJmL when the grid is large, vegetation must change over time, and carbon and water must balance.

## Install

The README gives these dependencies: a C compiler such as GCC, GNU Make, the JSON-C library, and optionally NetCDF, Udunits-2 and MPI. On Debian or Ubuntu the INSTALL file lists:

```bash
sudo apt-get install libnetcdf-dev libudunits2-dev libjson-c-dev
sudo apt-get install mpich          # optional, for the parallel build
```

Then build from a clone:

```bash
git clone https://github.com/PIK-LPJmL/LPJmL.git
cd LPJmL
./configure.sh
make
```

`configure.sh` picks the makefile for your system. It builds a parallel version when it detects MPI, and it accepts `-nompi`. `make` builds `bin/lpjml`, and `make lpjcheck` builds a checker for configuration files. The repository's `VERSION` file reads 6.1.9, and the tag `v6.1.9` marks that commit. The GitHub Releases page lists v6.0.6 (25 March 2026) as its latest release, so the tag is newer than the release. The recipe below builds `v6.1.9` serially. It needs the `cpp` package at run time, because LPJmL passes the configuration file through the C preprocessor.

LPJmL is under the GNU Affero General Public License. The recipe installs the unmodified upstream source. The AGPL requires you to offer source to the users of a network service if you change the code.

## A first run

Adapted from the INSTALL.md in the repository, https://github.com/PIK-LPJmL/LPJmL/blob/master/INSTALL.md, and the `test` target of the Makefile.

The INSTALL file says to run a minimum 2-cell simulation with `make test`. That target creates the `output` and `restart` folders and runs two stages:

```bash
bin/lpjml -DTESTCASE_2CELL lpjml_config.cjson
bin/lpjml -DTESTCASE_2CELL -DFROM_RESTART lpjml_config.cjson
```

The `-D` option defines a macro for the preprocessor. `TESTCASE_2CELL` points the input at the `testcase_2cell/` folder, and `FROM_RESTART` switches the configuration to the second stage. In the shipped configuration the first stage has `nspinup` 3799 years and writes a restart file. The second stage starts from that restart file and sets `nspinup` to 420, `firstyear` to 1901 and `lastyear` to 2019.

## Run the tested example

This recipe builds LPJmL in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 98.5 s. LPJmL has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [lpjml-recipe.tar.gz](https://biosimhub.pages.dev/guides/lpjml/lpjml-recipe.tar.gz) (Dockerfile, run.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf lpjml-recipe.tar.gz
   cd lpjml
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/lpjml:6.1.9 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/lpjml:6.1.9 /usr/local/bin/run-lpjml spinup 2100 > out/lpjml_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `globalflux_spinup.csv` | 803.0 KB |
| `globalflux_spinup.csv.json` | 861 B |
| `lpjml/config_run.cjson` | 33.5 KB |
| `lpjml/include/agriculture.h` | 2.4 KB |
| `lpjml/include/agriculture_grass.h` | 1.8 KB |
| `lpjml/include/agriculture_tree.h` | 1.7 KB |
| `lpjml/include/biomass_grass.h` | 1.7 KB |
| `lpjml/include/biomass_tree.h` | 2.1 KB |
| `lpjml/include/biomes.h` | 1.8 KB |
| `lpjml/include/bstruct.h` | 6.8 KB |
| `lpjml/include/bstruct_intern.h` | 4.1 KB |
| `lpjml/include/buffer.h` | 1.6 KB |
| `lpjml/include/cdf.h` | 9.0 KB |
| `lpjml/include/cell.h` | 15.3 KB |
| `lpjml/include/channel.h` | 3.1 KB |
| `lpjml/include/climate.h` | 8.4 KB |
| `lpjml/include/climbuf.h` | 3.5 KB |
| `lpjml/include/conf.h` | 11.9 KB |
| `lpjml/include/config.h` | 20.2 KB |
| `lpjml/include/coord.h` | 3.0 KB |
| `lpjml/include/coupler.h` | 3.7 KB |
| `lpjml/include/couplerpar.h` | 1.9 KB |
| `lpjml/include/cpl.h` | 3.1 KB |
| `lpjml/include/crop.h` | 9.0 KB |
| `lpjml/include/cropdates.h` | 3.1 KB |
| `lpjml/include/date.h` | 2.1 KB |
| `lpjml/include/discharge.h` | 4.5 KB |
| `lpjml/include/efr.h` | 3.4 KB |
| `lpjml/include/errmsg.h` | 3.5 KB |
| `lpjml/include/grass.h` | 5.0 KB |
| `lpjml/include/grassland.h` | 3.6 KB |
| `lpjml/include/hash.h` | 1.7 KB |
| `lpjml/include/header.h` | 8.4 KB |
| `lpjml/include/hydrotope.h` | 3.0 KB |
| `lpjml/include/icefrac.h` | 1.6 KB |
| `lpjml/include/image.h` | 7.4 KB |
| `lpjml/include/input.h` | 1.6 KB |
| `lpjml/include/intlist.h` | 1.7 KB |
| `lpjml/include/landuse.h` | 10.0 KB |
| `lpjml/include/list.h` | 1.7 KB |
| `lpjml/include/lpj.h` | 6.0 KB |
| `lpjml/include/manage.h` | 2.6 KB |
| `lpjml/include/managepar.h` | 6.6 KB |
| `lpjml/include/natural.h` | 2.0 KB |
| `lpjml/include/numeric.h` | 4.3 KB |
| `lpjml/include/outfile.h` | 2.7 KB |
| `lpjml/include/output.h` | 7.5 KB |
| `lpjml/include/param.h` | 9.1 KB |
| `lpjml/include/pft.h` | 18.7 KB |
| `lpjml/include/pftlist.h` | 2.2 KB |
| `lpjml/include/pftpar.h` | 2.4 KB |
| `lpjml/include/pnet.h` | 4.2 KB |
| `lpjml/include/queue.h` | 1.9 KB |
| `lpjml/include/reservoir.h` | 4.8 KB |
| `lpjml/include/soil.h` | 22.5 KB |
| `lpjml/include/soilpar.h` | 1.6 KB |
| `lpjml/include/spitfire.h` | 5.3 KB |
| `lpjml/include/stand.h` | 6.4 KB |
| `lpjml/include/swap.h` | 2.4 KB |
| `lpjml/include/timing.h` | 1.9 KB |
| `lpjml/include/tree.h` | 8.0 KB |
| `lpjml/include/types.h` | 9.1 KB |
| `lpjml/include/units.h` | 2.6 KB |
| `lpjml/include/urban.h` | 1.4 KB |
| `lpjml/include/wetland.h` | 1.4 KB |
| `lpjml/include/woodplantation.h` | 1.6 KB |
| `lpjml/input.cjson` | 5.4 KB |
| `lpjml/input_netcdf.cjson` | 6.1 KB |
| `lpjml/lpjml_config.cjson` | 33.5 KB |
| `lpjml/output/globalflux_spinup.csv` | 803.0 KB |
| `lpjml/output/globalflux_spinup.csv.json` | 861 B |
| `lpjml/output/lpjml_config_spinup.json` | 238.2 KB |
| `lpjml/output/spinup.log` | 468.6 KB |
| `lpjml/par/hydro.cjson` | 1.3 KB |
| `lpjml/par/lpjparam.cjson` | 11.4 KB |
| `lpjml/par/manage_irrig_systems_with_dummy_laimax_data.cjson` | 37.4 KB |
| `lpjml/par/netcdf.cjson` | 4.0 KB |
| `lpjml/par/netcdf.json` | 2.7 KB |
| `lpjml/par/outputvars.cjson` | 73.1 KB |
| `lpjml/par/pft.cjson` | 289.8 KB |
| `lpjml/par/soil.cjson` | 11.0 KB |
| `lpjml/par/soil_rock_ice.cjson` | 11.5 KB |
| `lpjml/restart/restart_1700_nv.lpj` | 26.4 KB |
| `lpjml/testcase_2cell/CH4_concentration_1700-2022.dat` | 4.3 KB |
| `lpjml/testcase_2cell/country_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/country_testcase_2cell.clm.json` | 12.1 KB |
| `lpjml/testcase_2cell/crop_phu_testcase_2cell.clm` | 11.2 KB |
| `lpjml/testcase_2cell/crop_phu_testcase_2cell.clm.json` | 2.2 KB |
| `lpjml/testcase_2cell/drainage_testcase_2cell.clm` | 75 B |
| `lpjml/testcase_2cell/drainage_testcase_2cell.clm.json` | 1.2 KB |
| `lpjml/testcase_2cell/elevation_testcase_2cell.clm` | 63 B |
| `lpjml/testcase_2cell/elevation_testcase_2cell.clm.json` | 1.1 KB |
| `lpjml/testcase_2cell/fertilizer_testcase_2cell.clm` | 39.6 KB |
| `lpjml/testcase_2cell/fertilizer_testcase_2cell.clm.json` | 1.8 KB |
| `lpjml/testcase_2cell/global_co2_ann_1700_2022.txt` | 4.1 KB |
| `lpjml/testcase_2cell/globalflux.csv` | 282.6 KB |
| `lpjml/testcase_2cell/globalflux.csv.json` | 1.0 KB |
| `lpjml/testcase_2cell/globalflux_spinup.csv` | 1.4 MB |
| `lpjml/testcase_2cell/globalflux_spinup.csv.json` | 924 B |
| `lpjml/testcase_2cell/grassland_lsuha_testcase_2cell.clm` | 63 B |
| `lpjml/testcase_2cell/grassland_lsuha_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/grid_testcase_2cell.clm` | 59 B |
| `lpjml/testcase_2cell/grid_testcase_2cell.clm.json` | 942 B |
| `lpjml/testcase_2cell/human_ignition_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/human_ignition_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/humid_testcase_2cell.clm` | 339.4 KB |
| `lpjml/testcase_2cell/humid_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/hydro_testcase_2cell.clm` | 71 B |
| `lpjml/testcase_2cell/hydro_testcase_2cell.clm.json` | 1.2 KB |
| `lpjml/testcase_2cell/input_testcase_2cell.cjson` | 4.7 KB |
| `lpjml/testcase_2cell/irrig_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/irrig_testcase_2cell.clm.json` | 1.2 KB |
| `lpjml/testcase_2cell/kbf_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/kbf_testcase_2cell.clm.json` | 1.7 KB |
| `lpjml/testcase_2cell/lakes_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/lakes_testcase_2cell.clm.json` | 1.2 KB |
| `lpjml/testcase_2cell/landfrac_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/landfrac_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/landuse_testcase_2cell.clm` | 259.1 KB |
| `lpjml/testcase_2cell/landuse_testcase_2cell.clm.json` | 1.7 KB |
| `lpjml/testcase_2cell/lightning_testcase_2cell.clm` | 155 B |
| `lpjml/testcase_2cell/lightning_testcase_2cell.clm.json` | 1.7 KB |
| `lpjml/testcase_2cell/lwnet_testcase_2cell.clm` | 169.7 KB |
| `lpjml/testcase_2cell/lwnet_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/manure_testcase_2cell.clm` | 39.6 KB |
| `lpjml/testcase_2cell/manure_testcase_2cell.clm.json` | 1.6 KB |
| `lpjml/testcase_2cell/nh4_deposition_testcase_2cell.clm` | 16.2 KB |
| `lpjml/testcase_2cell/nh4_deposition_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/no3_deposition_testcase_2cell.clm` | 16.2 KB |
| `lpjml/testcase_2cell/no3_deposition_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/popnum_testcase_2cell.clm` | 1.2 KB |
| `lpjml/testcase_2cell/popnum_testcase_2cell.clm.json` | 1.2 KB |
| `lpjml/testcase_2cell/prec_testcase_2cell.clm` | 169.7 KB |
| `lpjml/testcase_2cell/prec_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/reservoir_testcase_2cell.clm` | 139 B |
| `lpjml/testcase_2cell/reservoir_testcase_2cell.clm.json` | 1.2 KB |
| `lpjml/testcase_2cell/residue_testcase_2cell.clm` | 10.4 KB |
| `lpjml/testcase_2cell/residue_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/sdate_testcase_2cell.clm` | 155 B |
| `lpjml/testcase_2cell/sdate_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/slope_max_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/slope_max_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/slope_mean_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/slope_mean_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/slope_min_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/slope_min_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/soil_ph_testcase_2cell.clm` | 67 B |
| `lpjml/testcase_2cell/soil_ph_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/soil_testcase_2cell.clm` | 61 B |
| `lpjml/testcase_2cell/soil_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/swdown_testcase_2cell.clm` | 169.7 KB |
| `lpjml/testcase_2cell/swdown_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/tillage_testcase_2cell.clm` | 211 B |
| `lpjml/testcase_2cell/tillage_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/tmax_testcase_2cell.clm` | 169.7 KB |
| `lpjml/testcase_2cell/tmax_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/tmin_testcase_2cell.clm` | 169.7 KB |
| `lpjml/testcase_2cell/tmin_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/tmp_testcase_2cell.clm` | 169.7 KB |
| `lpjml/testcase_2cell/tmp_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml/testcase_2cell/wateruse_testcase_2cell.clm` | 1.4 KB |
| `lpjml/testcase_2cell/wateruse_testcase_2cell.clm.json` | 1.3 KB |
| `lpjml/testcase_2cell/windspeed_testcase_2cell.clm` | 169.7 KB |
| `lpjml/testcase_2cell/windspeed_testcase_2cell.clm.json` | 1.5 KB |
| `lpjml_config_spinup.json` | 238.2 KB |
| `lpjml_stdout.txt` | 0 B |
| `spinup.log` | 468.6 KB |

<details><summary>First lines of <code>globalflux_spinup.csv</code></summary>

```
Year,NEP,GPP,NPP,RH,estabc,negc_fluxes,firec,NBP,NBP_nat,transp,evap,interc,CH4 emiss.,CH4 oxid,CH4 sink,CH4 fire,prec,SoilC,SoilC_slow,LitC,VegC,Soil_CH4,nuptake,ndemand,nlosses,ninflux,estabn,negn_f
(AD),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 dm3/yr),(1e+15 dm3/yr),(1e+15 dm3/yr),(1e+15 gCH4/yr),(1e+15 g
-400,-0.00505119,0,0,0.00505119,2.86626e-06,0,0,-0.00504833,-0.00504833,0,0.00244279,0,0,6.92635e-07,-5.22966e-07,0,0.00476041,0.199002,0.0679541,0,2.86626e-06,9.38341e-10,0,0,0.000203976,5.06315e-07,
-399,-0.00470432,2.33327e-05,1.20308e-05,0.00471635,2.82485e-06,0,0,-0.00470149,-0.00470149,1.85294e-08,0.00265073,2.73599e-08,4.09883e-11,7.14886e-07,-5.55626e-07,0,0.00519326,0.194288,0.0678927,1.18
-398,-0.00449369,0.000140098,7.5504e-05,0.0045692,2.58481e-06,0,0,-0.00449111,-0.00449111,7.98497e-07,0.00241184,8.90209e-08,4.48237e-11,7.81389e-07,-6.06096e-07,0,0.00407644,0.189728,0.0678311,9.0991
-397,-0.00403154,0.000811247,0.000437644,0.00446919,1.50417e-06,0,1.15891e-17,-0.00403004,-0.00403004,3.16247e-05,0.00217501,8.6051e-07,2.43923e-10,7.17812e-07,-5.49326e-07,1.23617e-19,0.00404666
```

</details>

<details><summary>First lines of <code>globalflux_spinup.csv.json</code></summary>

```
{
  "sim_name" : "LPJmL Run",
  "source" : "LPJmL C Version 6.1.9",
  "history" : "Sun Oct 18 13:33:36 2026: lpjml -DTESTCASE_2CELL config_run.cjson",
  "global_attrs" :
  {
    "GIT_repo" : "https://github.com/PIK-LPJmL/LPJmL",
    "GIT_hash" : "",
    "institution" : "Potsdam Institute for Climate Impact Research",
    "contact" : "",
    "comment" : ""
  },
```

</details>

<details><summary>First lines of <code>lpjml/config_run.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**           l  p  j  m  l  _  c  o  n  f  i  g  .  c  j  s  o  n                 \n**/
/**                                                                                \n**/
/** Default configuration file for LPJmL C Version 6.1.9                           \n**/
/**                                                                                \n**/
/** Configuration file is divided into five sections:                              \n**/
/**                                                                                \n**/
/**  I.   Simulation description and type section                                  \n**/
/**  II.  Input parameter section                                                  \n**/
/**  III. Input data section                                                       \n**/
/**  IV.  Output data section                                                      \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/agriculture.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                  a  g  r  i  c  u  l  t  u  r  e  .  h                         \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of agriculture stand                                           \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/agriculture_grass.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**            a  g  r  i  c  u  l  t  u  r  a  l  _  g  r  a  s  s  .  h          \n**/
/**                                                                                \n**/
/**     C implementation of LPJ                                                    \n**/
/**                                                                                \n**/
/**     Declaration of agricultural grass stand                                    \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/agriculture_tree.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**         a  g  r  i  c  u  l  t  u  r  e  _  t  r  e  e  .  h                   \n**/
/**                                                                                \n**/
/**     C implementation of LPJ                                                    \n**/
/**                                                                                \n**/
/**     Declaration of agricultural tree stand                                     \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/biomass_grass.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     b  i  o  m  a  s  s  _  g  r  a  s  s  .  h                \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of biomass  stand                                              \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/biomass_tree.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     b  i  o  m  a  s  s  _  t  r  e  e  .  h                   \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of biomass tree stand                                          \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/biomes.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                      b  i  o  m  e  s  .  h                                    \n**/
/**                                                                                \n**/
/**     extension of LPJ to classify biomes based on FPC values only               \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/bstruct.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   b  s  t  r  u  c  t  .  h                                    \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Functions for reading/writing JSON-like objects from binary file           \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/bstruct_intern.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   b  s  t  r  u  c  t  _  i  n  t  e  r  n  .  h               \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Functions for reading/writing JSON-like objects from binary file           \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/buffer.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                       b  u  f  f  e  r  .  h                                   \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/cdf.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                              c  d  f  .  h                                     \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for NetCDF interface for input/output                          \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/cell.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                      c  e  l  l  .  h                                          \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of cell datatype                                               \n**/
/**                                                                                \n**/
/**     Hierarchy:                                                                 \n**/
/**                                                                                \n**/
/**     --cell                                                                     \n**/
/**       +-Coord                                                                  \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/channel.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     c  h  a  n  n  e  l  .  h                                  \n**/
/**                                                                                \n**/
/**     Header file for communication library using TCP/IP sockets                 \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/climate.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 c  l  i  m  a  t  e  .  h                                      \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header for the climate datatype and related functions                      \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/climbuf.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 c  l  i  m  b  u  f  .  h                                      \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/conf.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                  c  o  n  f  .  h                                              \n**/
/**                                                                                \n**/
/**     Header for LPJ configuration file                                          \n**/
/**     Must be included by LPJmL configuration file                               \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/config.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   c  o  n  f  i  g  .  h                                       \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/coord.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                    c  o  o  r  d  .  h                                         \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Definition of coordinate datatype                                          \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/coupler.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                      c  o  u  p  l  e  r  .  h                                 \n**/
/**                                                                                \n**/
/**     Declaration of coupler functions and related datatypes                     \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/couplerpar.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                      c  o  u  p  l  e  r  p  a  r  .  h                        \n**/
/**                                                                                \n**/
/**     Definition of coupler input indices                                        \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/cpl.h</code></summary>

```
/****************************************************************************************/
/**                                                                                  \n**/
/**                           c  p  l  .  h                                          \n**/
/**                                                                                  \n**/
/**     Header file for parallel coupling coordinate list with domain-               \n**/
/**     decomposed arrays (2-D rectangular decompostion)                             \n**/
/**                                                                                  \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/crop.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                         c  r  o  p  .  h                                       \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for crop PFTs                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/cropdates.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 c  r  o  p  d  a  t  e  s  .  h                                \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/date.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                    d  a  t  e  .  h                                            \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/discharge.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 d  i  s  c  h  a  r  g  e  .  h                                \n**/
/**                                                                                \n**/
/**     C implementation of river routing in LPJ                                   \n**/
/**                                                                                \n**/
/**     LPJ header file for river routing                                          \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/efr.h</code></summary>

```
/***************************************************************************/
/**                                                                       **/
/**                  e f r .  h                                           **/
/**                                                                       **/
/**     C implementation of LPJ, derived from the Fortran/C++ version     **/
/**                                                                       **/
/**     Declaration of efr functions                                      **/
/**                                                                       **/
/**      written by Amandine Pastor, Wietse Franssen                      **/
/**     Wageningen univeristy, Earth system science                       **/
/**     Postbus 47                                                        **/
/**     6700AA Wageningen, Netherlands                                    **/
```

</details>

<details><summary>First lines of <code>lpjml/include/errmsg.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 e  r  r  m  s  g  .  h                                         \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Definition of error codes and error messages                               \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/grass.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   g  r  a  s  s  .  h                                          \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for grass PFTs                                                 \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/grassland.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     g  r  a  s  s  l  a  n  d  .  h                            \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of grassland stand                                             \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/hash.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                          h  a  s  h  .  h                                      \n**/
/**                                                                                \n**/
/**     C implementation of a hash table to store key/value items in a dictionary  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/header.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     h  e  a  d  e  r  .  h                                     \n**/
/**                                                                                \n**/
/**     Reading/Writing file header for LPJ related files. Detects                 \n**/
/**     whether byte order has to be changed                                       \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/hydrotope.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                         h y d r o t o p e . h                                  \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/icefrac.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     i  c  e  f  r  a  c  .  h                                  \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of datatype Icefrac                                            \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/image.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                      i  m  a  g  e  .  h                                       \n**/
/**                                                                                \n**/
/**     Declaration of IMAGE coupler functions and related datatypes               \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/input.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   i  n  p  u  t  .  h                                          \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/intlist.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   i  n  t  l  i  s  t  .  h                                    \n**/
/**                                                                                \n**/
/**     C implementation of a resizeable integer array                             \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/landuse.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 l  a  n  d  u  s  e  .  h                                      \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/list.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                          l  i  s  t  .  h                                      \n**/
/**                                                                                \n**/
/**     C implementation of a resizeable array                                     \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/lpj.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                      l  p  j  .  h                                             \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Version with managed land and river routing                                \n**/
/**                                                                                \n**/
/**     The model simulates vegetation dynamics, hydrology and soil                \n**/
/**     organic matter dynamics on an area-averaged grid cell basis using          \n**/
/**     one-year time step. Input parameters are monthly mean air                  \n**/
/**     temperature, total precipitation, short and longwave radiation,            \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/manage.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                        m  a  n  a  g  e  .  h                                  \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/managepar.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                        m  a  n  a  g  e  p  a  r  .  h                         \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Country codes for management practices                                     \m**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/natural.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     n  a  t  u  r  a  l  .  h                                  \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of natural stand                                               \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/numeric.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   n  u  m  e  r  i  c  .  h                                    \n**/
/**                                                                                \n**/
/**     Header for numerical utility routines                                      \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/outfile.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                        o  u  t  f  i  l  e  .  h                               \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for output datatype and functions                              \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/output.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                        o  u  t  p  u  t  .  h                                  \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for output datatype and functions                              \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/param.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                  p  a  r  a  m  .  h                                           \n**/
/**                                                                                \n**/
/**     Header file for LPJmL parameters                                           \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/pft.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     p  f  t  .  h                                              \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of plant functional type (PFT) datatype                        \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/pftlist.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                    p  f  t  l  i  s  t  .  h                                   \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/pftpar.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                    p  f  t  p  a  r  .  h                                      \n**/
/**                                                                                \n**/
/**     Pft parameter header, should be included in data file                      \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/pnet.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                       p  n  e  t  .  h                                         \n**/
/**                                                                                \n**/
/**     Header file for Pnet library: MPI-parallelization of networks              \n**/
/**                                                                                \n**/
/**     Implementation is described in:                                            \n**/
/**     W. von Bloh, 2008. Sequential and Parallel Implementation of               \n**/
/**     Networks. In P. beim Graben, C. Zhou, M. Thiel, and J. Kurths              \n**/
/**     (eds.), Lectures in Supercomputational Neuroscience, Dynamics in           \n**/
/**     Complex Brain Networks, Springer, 279-318.                                 \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/queue.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                       q  u  e  u  e  .  h                                      \n**/
/**                                                                                \n**/
/**     C implementation of a delay queue                                          \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/reservoir.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 r  e  s  e  r  v  o  i  r  .  h                                \n**/
/**                                                                                \n**/
/**     C implementation of reservoir operation in LPJ                             \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/soil.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                         s  o  i  l  .  h                                       \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for soil functions                                             \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/soilpar.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                  s  o  i  l  p  a  r  .  h                                     \n**/
/**                                                                                \n**/
/**     Soil parameter constants, should be included in data file                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/spitfire.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                 s  p i  t  f  i  r  e  .  h                                    \n**/
/**                                                                                \n**/
/**     Header file for Spitfire fire model                                        \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/stand.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                    s  t  a  n  d  .  h                                         \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for implementation of stands in LPJ                            \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/swap.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     s  w  a  p  .  h                                           \n**/
/**                                                                                \n**/
/**     Converts big endian into little endian and vice versa                      \n**/
/**     Needed for reading data under IA32                                         \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/timing.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     t  i  m  i  n  g  . h                                      \n**/
/**                                                                                \n**/
/**     Definition of performance timing datatype                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/tree.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                        t  r  e  e  .  h                                        \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Header file for tree PFTs                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/types.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     t  y  p  e  s  .  h                                        \n**/
/**                                                                                \n**/
/**     Definition of basic datatypes and macros                                   \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/units.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                      u  n  i  t  s  .  h                                       \n**/
/**                                                                                \n**/
/**     Header for universal constants and unit conversions                        \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/urban.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                        u  r  b  a  n  .  h                                     \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of urban stand                                                 \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/wetland.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     w  e  t  l  a  n  d  .  h                                  \n**/
/**                                                                                \n**/
/**     C implementation of LPJmL                                                  \n**/
/**                                                                                \n**/
/**     Declaration of wetland stand                                               \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
```

</details>

<details><summary>First lines of <code>lpjml/include/woodplantation.h</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                     w o o d p l a n t a t i o n . h                            \n**/
/**                                                                                \n**/
/**     Declaration of woodplantation stand                                        \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://gitlab.pik-potsdam.de/lpjml                                   \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/input.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                       i  n  p  u  t  .  c  j  s  o  n                          \n**/
/**                                                                                \n**/
/** Configuration file for input dataset for LPJ C Version 6.1.9                   \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/input_netcdf.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**        i  n  p  u  t  _  n  e  t  c  d  f  .  c  j  s  o  n                    \n**/
/**                                                                                \n**/
/** Configuration file for NetCDF input dataset for LPJmL                          \n**/
/** Version 6.1.9                                                                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
```

</details>

<details><summary>First lines of <code>lpjml/lpjml_config.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**           l  p  j  m  l  _  c  o  n  f  i  g  .  c  j  s  o  n                 \n**/
/**                                                                                \n**/
/** Default configuration file for LPJmL C Version 6.1.9                           \n**/
/**                                                                                \n**/
/** Configuration file is divided into five sections:                              \n**/
/**                                                                                \n**/
/**  I.   Simulation description and type section                                  \n**/
/**  II.  Input parameter section                                                  \n**/
/**  III. Input data section                                                       \n**/
/**  IV.  Output data section                                                      \n**/
```

</details>

<details><summary>First lines of <code>lpjml/output/globalflux_spinup.csv</code></summary>

```
Year,NEP,GPP,NPP,RH,estabc,negc_fluxes,firec,NBP,NBP_nat,transp,evap,interc,CH4 emiss.,CH4 oxid,CH4 sink,CH4 fire,prec,SoilC,SoilC_slow,LitC,VegC,Soil_CH4,nuptake,ndemand,nlosses,ninflux,estabn,negn_f
(AD),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 dm3/yr),(1e+15 dm3/yr),(1e+15 dm3/yr),(1e+15 gCH4/yr),(1e+15 g
-400,-0.00505119,0,0,0.00505119,2.86626e-06,0,0,-0.00504833,-0.00504833,0,0.00244279,0,0,6.92635e-07,-5.22966e-07,0,0.00476041,0.199002,0.0679541,0,2.86626e-06,9.38341e-10,0,0,0.000203976,5.06315e-07,
-399,-0.00470432,2.33327e-05,1.20308e-05,0.00471635,2.82485e-06,0,0,-0.00470149,-0.00470149,1.85294e-08,0.00265073,2.73599e-08,4.09883e-11,7.14886e-07,-5.55626e-07,0,0.00519326,0.194288,0.0678927,1.18
-398,-0.00449369,0.000140098,7.5504e-05,0.0045692,2.58481e-06,0,0,-0.00449111,-0.00449111,7.98497e-07,0.00241184,8.90209e-08,4.48237e-11,7.81389e-07,-6.06096e-07,0,0.00407644,0.189728,0.0678311,9.0991
-397,-0.00403154,0.000811247,0.000437644,0.00446919,1.50417e-06,0,1.15891e-17,-0.00403004,-0.00403004,3.16247e-05,0.00217501,8.6051e-07,2.43923e-10,7.17812e-07,-5.49326e-07,1.23617e-19,0.00404666
```

</details>

<details><summary>First lines of <code>lpjml/output/globalflux_spinup.csv.json</code></summary>

```
{
  "sim_name" : "LPJmL Run",
  "source" : "LPJmL C Version 6.1.9",
  "history" : "Sun Oct 18 13:33:36 2026: lpjml -DTESTCASE_2CELL config_run.cjson",
  "global_attrs" :
  {
    "GIT_repo" : "https://github.com/PIK-LPJmL/LPJmL",
    "GIT_hash" : "",
    "institution" : "Potsdam Institute for Climate Impact Research",
    "contact" : "",
    "comment" : ""
  },
```

</details>

<details><summary>First lines of <code>lpjml/output/lpjml_config_spinup.json</code></summary>

```
{
  "GIT_repo" : "https://github.com/PIK-LPJmL/LPJmL",
  "GIT_hash" : "",
  "sim_name" : "LPJmL Run",
  "sim_id" : "lpjml",
  "coupled_model" : null,
  "coupled_host" : "localhost",
  "coupled_port" : 2224,
  "start_coupling": null,
  "version" : "6.1",
  "global_attrs" : {"institution" : "Potsdam Institute for Climate Impact Research",
                    "contact" : "",
```

</details>

<details><summary>First lines of <code>lpjml/output/spinup.log</code></summary>

```
******************************************************************************
****           _     ____     _           _        __         _           ****
****          | |   |  _ \   | |_ __ ___ | |      / /_       / |          ****
****          | |   | |_) |  | | '_ ` _ \| |     | '_ \      | |          ****
****          | |___|  __/ |_| | | | | | | |___  | (_) |  _  | |          ****
****          |_____|_|   \___/|_| |_| |_|_____|  \___/  (_) |_|          ****
****                                                                      ****
****                 lpjml C Version 6.1.9 (Oct 18 2026)                  ****
****    Dynamic global vegetation model with natural and managed land     ****
****                          Compiled for Linux                          ****
****       (C) Potsdam Institute for Climate Impact Research (PIK),       ****
****                          see COPYRIGHT file                          ****
```

</details>

<details><summary>First lines of <code>lpjml/par/hydro.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                   h y d r o  .  c  j  s  o  n                                  \n**/
/**                                                                                \n**/
/** Default input parameter file for LPJmL C Version 6.1.9                         \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/par/lpjparam.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**              l  p  j  p  a  r  a  m  .  c  j  s  o  n                          \n**/
/**                                                                                \n**/
/**     LPJ parameter file for LPJmL version 6.1.9                                 \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/par/manage_irrig_systems_with_dummy_laimax_data.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**             manage_irrig_systems_with_dummy_laimax_data.cjson                  \n**/
/**                                                                                \n**/
/**     management parameter data with maximum LAI values for all crops            \n**/
/**               LPJmL Version 6.1.9                                              \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
```

</details>

<details><summary>First lines of <code>lpjml/par/netcdf.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**                           n  e  t  c  d  f  .  c  j  s  o  n                   \n**/
/**                                                                                \n**/
/**  Defines NetCDF missing values and axis names for LPJmL 6.1.9                  \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/par/netcdf.json</code></summary>

```
{
  "missing_value" : {"float" : -1e32, "short" : -9999, "int" : -999999, "byte" : 99},
  "longitude" : { "name" : "lon", "dim" : "lon", "long_name" : "Longitude","comment" : null,
                  "standard_name" : "longitude", "unit" : "degrees_east", "scale" : 1.0},
  "longitude_bnds" : { "name" : "lon_bnds", "dim" : "lon", "long_name" : null,
                       "comment" : "Longitude boundary coordinates",
                       "standard_name" : null, "unit" : null, "scale" : 1.0},
  "latitude" : { "name" : "lat", "dim" : "lat", "long_name" : "Latitude", "comment" : null,
                 "standard_name" : "latitude","unit" : "degrees_north", "scale" : 1.0},
  "latitude_bnds" : { "name" : "lat_bnds", "dim" : "lat", "long_name" : null,
                      "comment" : "Latitude boundary coordinates",
                      "standard_name" : null,"unit" : null, "scale" : 1.0},
```

</details>

<details><summary>First lines of <code>lpjml/par/outputvars.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**               o  u  t  p  u  t  v  a  r  s  .  c  j  s  o  n                   \n**/
/**                                                                                \n**/
/**  Defines array of output variables for LPJmL 6.1.9                             \n**/
/**                                                                                \n**/
/**  Monthly output rates can be rescaled to 1/day or 1/second by setting the unit \n**/
/**  to day-1 or sec-1, e.g.:                                                      \n**/
/**  "unit" : "g/m2/month"  ->  "unit" : "g m-2 day-1"                             \n**/
/**  Then output is divided my the number of days in each month                    \n**/
/**                                                                                \n**/
/**  Time step for output can be set via keyword:                                  \n**/
```

</details>

<details><summary>First lines of <code>lpjml/par/pft.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**              p  f  t  .  c  j  s  o  n                                         \n**/
/**                                                                                \n**/
/**  PFT and CFT parameter file for LPJmL version 6.1.9                            \n**/
/**  CFTs parameters must be put after PFTs                                        \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
```

</details>

<details><summary>First lines of <code>lpjml/par/soil.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**              s  o  i  l  .  c  j  s  o  n                                      \n**/
/**                                                                                \n**/
/**  Soil parameter data for LPJmL version 6.1.9                                   \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/par/soil_rock_ice.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/**              s  o  i  l  _  r  o  c  k  _  i  c  e  .  c  j  s  o  n           \n**/
/**                                                                                \n**/
/**  Soil parameter data for LPJmL version 6.1.9                                   \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/CH4_concentration_1700-2022.dat</code></summary>

```
1700 679.6275
1701 679.7059
1702 679.7843
1703 679.8627
1704 679.9412
1705 680.0196
1706 680.098
1707 680.1765
1708 680.2549
1709 680.3333
1710 680.4118
1711 680.4902
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/country_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "country_testcase_2cell.clm",
  "variable" : "country_code",
  "global_attrs" :
  {
    "title" : "country code file",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "country and region code; each grid cell is only assigned to one country, region codes are only assigned for large countries",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "<https://gadm.org/>"
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/crop_phu_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "crop_phu_testcase_2cell.clm",
  "variable" : "phusum",
  "global_attrs" :
  {
    "title" : "Phenolgocial heat unit (phu) sum for maturity data",
    "climate" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "PHU sums for cropping seasons for the standard 12 crops of LPJmL for rainfed and irrigated systems based on the GGCMI Phase 3 crop calendar",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Jägermeyr et al. (2021a).  <https://doi.org/10.5281/zenodo.5062513>, Jägermeyr et al. (2021b). <https://dx.doi.org/10.1038/s43016-021-00400-y>"
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/drainage_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "drainage_testcase_2cell.clm",
  "variable" : "drainage",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "drainage data processed with LandInG",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/elevation_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "elevation_testcase_2cell.clm",
  "variable" : "elevation",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "elevation data processed with LandInG",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/fertilizer_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "fertilizer_testcase_2cell.clm",
  "variable" : "fertilizer",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "Nitrogen fertilizer application rates combining crop-specific application rates for year 2000 with country-level application trends (LUH2) and crop-specific land use fractions from La
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention; Mueller (2012) <https://doi.org/10.5281/zenodo.5260732> for year-2000 patterns; Hurtt et a
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/global_co2_ann_1700_2022.txt</code></summary>

```
1700  276.59
1701  276.62
1702  276.65
1703  276.67
1704  276.70
1705  276.72
1706  276.75
1707  276.78
1708  276.80
1709  276.83
1710  276.86
1711  276.89
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/globalflux.csv</code></summary>

```
Year,NEP,GPP,NPP,RH,estabc,negc_fluxes,firec,area,harvestc,prod_turnoverc,NBP,NBP_nat,transp,evap,interc,wd,discharge,CH4 emiss.,CH4 oxid,CH4 sink,CH4 fire,CH4 rice,CH4 grass,CH4 agr,prec,SoilC,SoilC_
(AD),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(m2),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 dm3/yr),(1e+15 dm3/yr),(1e+15
1481,-0.00160385,0.004264,0.00174039,0.00334424,3.54181e-05,0,1.60387e-07,1.99347e+09,2.94372e-05,0,-0.00159803,-5.70139e-05,0.00117458,0.00105533,0.000321551,0,0.00274517,1.21174e-09,2.2438e-07,-1.82
1482,-0.00128555,0.00455889,0.00179487,0.00308042,3.53633e-05,0,3.47082e-05,1.99347e+09,0.000179224,0,-0.00146412,-0.000140037,0.00125172,0.000686516,0.000249627,0,0.00195278,1.47597e-09,3.65828e-07,-
1483,-0.000956645,0.00468012,0.00192685,0.00288349,3.53507e-05,0,6.87322e-08,1.99347e+09,0.000238164,0,-0.00115953,-0.000102634,0.00135165,0.000731775,0.000263082,0,0.00217346,1.73328e-09,2.81717e-07,
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/globalflux.csv.json</code></summary>

```
{
  "sim_name" : "LPJmL Run",
  "source" : "LPJmL C Version 6.1.9",
  "history" : "Tue Sep  1 13:52:03 2026: bin/lpjml -DTESTCASE_2CELL -DFROM_RESTART lpjml_config.cjson",
  "global_attrs" :
  {
    "GIT_repo" : "git@gitlab.pik-potsdam.de:lpjml/LPJmL_internal.git",
    "GIT_hash" : "86db98367a2228ff9af5aa14144938244533bd0f",
    "institution" : "Potsdam Institute for Climate Impact Research",
    "contact" : "",
    "comment" : ""
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/globalflux_spinup.csv</code></summary>

```
Year,NEP,GPP,NPP,RH,estabc,negc_fluxes,firec,NBP,NBP_nat,transp,evap,interc,CH4 emiss.,CH4 oxid,CH4 sink,CH4 fire,prec,SoilC,SoilC_slow,LitC,VegC,Soil_CH4,nuptake,ndemand,nlosses,ninflux,estabn,negn_f
(AD),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 gC/yr),(1e+15 dm3/yr),(1e+15 dm3/yr),(1e+15 dm3/yr),(1e+15 gCH4/yr),(1e+15 g
-2099,-0.00505119,0,0,0.00505119,2.86626e-06,0,0,-0.00504833,-0.00504833,0,0.00244279,0,0,6.92635e-07,-5.22966e-07,0,0.00476041,0.199002,0.0679541,0,2.86626e-06,9.38341e-10,0,0,0.000203976,5.06315e-07
-2098,-0.00470432,2.33327e-05,1.20308e-05,0.00471635,2.82485e-06,0,0,-0.00470149,-0.00470149,1.85294e-08,0.00265073,2.73599e-08,4.09883e-11,7.14886e-07,-5.55626e-07,0,0.00519326,0.194288,0.0678927,1.1
-2097,-0.00449369,0.000140098,7.5504e-05,0.0045692,2.58481e-06,0,0,-0.00449111,-0.00449111,7.98497e-07,0.00241184,8.90209e-08,4.48237e-11,7.81389e-07,-6.06096e-07,0,0.00407644,0.189728,0.0678311,9.099
-2096,-0.00403154,0.000811247,0.000437644,0.00446919,1.50417e-06,0,1.15891e-17,-0.00403004,-0.00403004,3.16247e-05,0.00217501,8.6051e-07,2.43923e-10,7.17812e-07,-5.49326e-07,1.23617e-19,0.0040466
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/globalflux_spinup.csv.json</code></summary>

```
{
  "sim_name" : "LPJmL Run",
  "source" : "LPJmL C Version 6.1.9",
  "history" : "Tue Sep  1 13:49:31 2026: bin/lpjml -DTESTCASE_2CELL lpjml_config.cjson",
  "global_attrs" :
  {
    "GIT_repo" : "git@gitlab.pik-potsdam.de:lpjml/LPJmL_internal.git",
    "GIT_hash" : "86db98367a2228ff9af5aa14144938244533bd0f",
    "institution" : "Potsdam Institute for Climate Impact Research",
    "contact" : "",
    "comment" : ""
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/grassland_lsuha_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "grassland_lsuha_testcase_2cell.clm",
  "variable" : "lsudens",
  "global_attrs" :
  {
    "title" : "livestock density file",
    "climate" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "livestock grazing densities for LPJmL simulations",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Heinke 2025 <https://doi.org/10.5281/zenodo.14946695>, Herrero 2013 <https://doi.org/10.1073/pnas.1308149110>, Heinke 2020 <https://doi.org/10.1029/2019WR026995>, Heinke 2023 <http
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/grid_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "grid_testcase_2cell.clm",
  "variable" : "grid",
  "global_attrs" :
  {
    "title" : "grid file",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "coordinates of each grid cell in the sequence grid cells are sorted in all other input files",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Harris et al. (2014).  <https://doi.org/10.1002/joc.3711>"
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/human_ignition_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "human_ignition_testcase_2cell.clm",
  "variable" : "human_ignition",
  "global_attrs" : 
  {
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "human fire ignition rates per year",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Thonicke, K., Spessa, A., Prentice, I. C., Harrison, S. P., Dong, L., and Carmona-Moreno, C. 2010: The influence of vegetation, fire spread and fire behaviour on biomass burning an
  },
  "history" : "Tue Mar 10 17:09:52 2026: mathclm -metafile float human_ignition.clm.json human_ignition2.clm",
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/humid_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "humid_testcase_2cell.clm",
  "variable" : "huss",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/hydro_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "hydro_testcase_2cell.clm",
  "variable" : "CTI values",
  "global_attrs" :
  {
    "title" : "CTI",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "HYDRO1k",
    "contact" : "Sibyll Schaphoff <Sibyll.Schaphoff@pik-potsdam-de>",
    "summary" : "includes CTI mean, standard deviation and skewness, within each cell",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "https://daac.ornl.gov/cgi-bin/dsviewer.pl?ds_id=1007, Verdin, K.L., 2017, Hydrologic Derivatives for Modeling and Applications (HDMA) database: U.S. Geological Survey data release,
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/input_testcase_2cell.cjson</code></summary>

```
/**************************************************************************************/
/**                                                                                \n**/
/** File: input_testcase_2cell.cjson                                               \n**/
/** Source: regridlpj -drainage -dir testcase_2cell testcase_2cell                 \n**/
/** Configuration file for input dataset for LPJmL C Version 6.1.7                 \n**/
/**                                                                                \n**/
/** (C) Potsdam Institute for Climate Impact Research (PIK), see COPYRIGHT file    \n**/
/** authors, and contributors see AUTHORS file                                     \n**/
/** This file is part of LPJmL and licensed under GNU AGPL Version 3               \n**/
/** or later. See LICENSE file or go to http://www.gnu.org/licenses/               \n**/
/** Contact: https://github.com/PIK-LPJmL/LPJmL                                    \n**/
/**                                                                                \n**/
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/irrig_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "irrig_testcase_2cell.clm",
  "variable" : "neighb_irrig",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "neighbor irrigation data processed with LandInG",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/kbf_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "kbf_testcase_2cell.clm",
  "variable" : "KBF",
  "global_attrs" :
  {
    "title" : "base-flow recession coefficient",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "ERMITAGE (EU 7th Framework Programme , project number 265170)",
    "contact" : "Sibyll Schaphoff <Sibyll.Schaphoff@pik-potsdam-de>",
    "summary" : "Base-flow recession coefficient determining the outflow rate from groundwater stores as a fraction of the store",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "<https://arquivo.pt/wayback/20160421113325mp_/http://ermitage.cs.man.ac.uk/sites/default/files/D5.3.pdf>, Arancibia, et al. 2010 <https://doi.org/10.5194/hess-14-2193-2010>"
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/lakes_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "lakes_testcase_2cell.clm",
  "variable" : "lake_and_river_surface_area",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "lake and river surface area fraction data processed with LandInG",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/landfrac_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "landfrac_testcase_2cell.clm",
  "variable" : "landfrac",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "Land fraction in each grid cell. Includes inland water bodies. Does not include ocean fraction of cells along coastlines",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention; Grid from CRU-TS data, land fractions from GADM version 3.6"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/landuse_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "landuse_testcase_2cell.clm",
  "variable" : "landfrac",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "Land use fractions, with fallow land added to others and an added distinction of irrigation systems",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documentation; source datasets documented therein"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/lightning_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "lightning_testcase_2cell.clm",
  "variable" : "lightning",
  "global_attrs" :
  {
    "title" : "LIS/OTD 0.5 Degree High Resolution Monthly Climatology (HRMC)",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "monthly lightning intensity",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Cecil, Daniel J. 2006. LIS/OTD 0.5 Degree High Resolution Monthly Climatology (HRMC) [indicate subset used]. Dataset available online from the NASA Global Hydrology Resource Center
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/lwnet_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "lwnet_testcase_2cell.clm",
  "variable" : "lwnet",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/manure_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "manure_testcase_2cell.clm",
  "variable" : "manure",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "Manure nitrogen application rates combining rates from Zhang et al. (2017) with land use fractions from LandInG",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention; Zhang et al. (2027) <https://doi.org/10.1594/PANGAEA.871980>"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/nh4_deposition_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "nh4_deposition_testcase_2cell.clm",
  "variable" : "nhx",
  "global_attrs" :
  {
    "title" : "ISIMIP3a N-deposition input data (v1.3)",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "ISIMIP3a N-deposition input data (v1.3). ISIMIP Repository.",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Jia Yang, Hanqin Tian (2023): ISIMIP3a N-deposition input data (v1.3). ISIMIP Repository. <https://doi.org/10.48364/ISIMIP.759077.3>"
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/no3_deposition_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "no3_deposition_testcase_2cell.clm",
  "variable" : "noy",
  "global_attrs" :
  {
    "title" : "ISIMIP3a N-deposition input data (v1.3)",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "ISIMIP3a N-deposition input data (v1.3). ISIMIP Repository.",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Jia Yang, Hanqin Tian (2023): ISIMIP3a N-deposition input data (v1.3). ISIMIP Repository. <https://doi.org/10.48364/ISIMIP.759077.3>"
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/popnum_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "popnum_testcase_2cell.clm",
  "variable" : "number_of_people",
  "global_attrs" :
  {
    "title" : "Human population density",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "gridded population density data",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Franziska Piontek, Tobias Geiger (2017): ISIMIP2b population input data (v1.0). ISIMIP Repository. https://doi.org/10.48364/ISIMIP.892838"
  },
  "history" : "Tue Mar 10 12:28:03 2026: cdf2clm -json -float -zero -o population_histsoc_0p5deg_annual_1861-2005.clm /p/projects/lpjml/inputs/public_standard/grid.clm population_histsoc_0p5deg_annual
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/prec_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "prec_testcase_2cell.clm",
  "variable" : "prec",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/reservoir_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "reservoir_testcase_2cell.clm",
  "variable" : "reservoir",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "reservoirs data processed with LandInG, equally weighting distance and catchment area size (par1)",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention"
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/residue_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "residue_testcase_2cell.clm",
  "variable" : "residuefrac",
  "global_attrs" :
  {
    "title" : "Residue recycling fraction",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Jens Heinke <heinke@pik-potsdam.de>",
    "summary" : "describes shares of residues that are recycled on the field and not removed",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Dietrich et al. (2020) <https://doi.org/10.5281/zenodo.3822084>"
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/sdate_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "sdate_testcase_2cell.clm",
  "variable" : "sdate",
  "global_attrs" :
  {
    "title" : "sdate file",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Potsdam Institute for Climate Impact Research (PIK)",
    "summary" : "sowing dates for the standard 12 crops of LPJmL for rainfed and irrigated systems based on the GGCMI Phase 3 crop calendar",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Jägermeyr et al. (2021a).  <https://doi.org/10.5281/zenodo.5062513>, Jägermeyr et al. (2021b). <https://dx.doi.org/10.1038/s43016-021-00400-y>"
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/slope_max_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "slope_max_testcase_2cell.clm",
  "variable" : "slope_30as_max",
  "global_attrs" :
  {
    "title" : "max slope",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "HYDRO1k",
    "contact" : "Sibyll Schaphoff <Sibyll.Schaphoff@pik-potsdam-de>",
    "summary" : "maximum slope occur in original 1 km spatial resolution data",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "https://www.sciencebase.gov/catalog/item/5910def6e4b0e541a03ac98c, Verdin, K.L., 2017, Hydrologic Derivatives for Modeling and Applications (HDMA) database: U.S. Geological Survey 
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/slope_mean_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "slope_mean_testcase_2cell.clm",
  "variable" : "slope_30as_mean",
  "global_attrs" :
  {
    "title" : "mean slope",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "HYDRO1k",
    "contact" : "Sibyll Schaphoff <Sibyll.Schaphoff@pik-potsdam-de>",
    "summary" : "mean slope derived form 1 km spatial resolution",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "https://www.sciencebase.gov/catalog/item/5910def6e4b0e541a03ac98c, Verdin, K.L., 2017, Hydrologic Derivatives for Modeling and Applications (HDMA) database: U.S. Geological Survey 
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/slope_min_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "slope_min_testcase_2cell.clm",
  "variable" : "slope_30as_min",
  "global_attrs" :
  {
    "title" : "min slope",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "HYDRO1k",
    "contact" : "Sibyll Schaphoff <Sibyll.Schaphoff@pik-potsdam-de>",
    "summary" : "minimum slope occur in original 1 km spatial resolution data",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "https://www.sciencebase.gov/catalog/item/5910def6e4b0e541a03ac98c, Verdin, K.L., 2017, Hydrologic Derivatives for Modeling and Applications (HDMA) database: U.S. Geological Survey 
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/soil_ph_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "soil_ph_testcase_2cell.clm",
  "variable" : "soilph",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "Soil acidity (pH) of dominant (most prominant) soil type in cell, based on HWSD",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention; FAO/IIASA/ISRIC/ISSCAS/JRC: Harmonized World Soil Database (version 1.21), FAO, Rome, Ital
  },  
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/soil_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "soil_testcase_2cell.clm",
  "variable" : "soilcode",
  "global_attrs" :
  {
    "title" : "LandInG v1 land input data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Sebastian Ostberg <ostberg@pik-potsdam.de>",
    "summary" : "Dominant (most prominant) soil type in cell, based on HWSD",
    "license" : "Creative Commons Attribution 4.0 International <https://creativecommons.org/licenses/by/4.0/>",
    "references" : "Ostberg et al. (2023) <https://doi.org/10.5194/gmd-16-3375-2023> for LandInG documention; FAO/IIASA/ISRIC/ISSCAS/JRC: Harmonized World Soil Database (version 1.21), FAO, Rome, Ital
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/swdown_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "swdown_testcase_2cell.clm",
  "variable" : "swdown",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/tillage_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "tillage_testcase_2cell.clm",
  "variable" : "with_tillage", 
  "global_attrs" :
  {
    "title" : "Porwollik et al. 2019 tillage data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "contact" : "Fabian Stenzel <stenzel@pik-potsdam.de>",
    "summary" : "Tillage data from Porwollik et al. 2019, assuming conventional tillage everywhere prior to 1974",
    "license" : "Open Data Commons Open Database License (ODbL) v1.0 <https://opendatacommons.org/licenses/odbl/1-0/>",
    "references" : "Porwollik et al. (2019) <http://dx.doi.org/10.5194/essd-11-823-2019>"
  },
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/tmax_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "tmax_testcase_2cell.clm",
  "variable" : "tmax",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/tmin_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "tmin_testcase_2cell.clm",
  "variable" : "tmin",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/tmp_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "tmp_testcase_2cell.clm",
  "variable" : "temp",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/wateruse_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "wateruse_testcase_2cell.clm",
  "variable" : "water_use",
  "global_attrs" :
  {
    "title" : "ISIMIP3a water use data",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "ISIMIP3a water use input data. ISIMIP Repository.",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Yoshihide Wada, Martina Flörke, Naota Hanasaki, Hannes Müller Schmied, Simon N. Gosling, Jacob Schewe (2022): ISIMIP3a water abstraction input data (v1.0). ISIMIP Repository. <http
```

</details>

<details><summary>First lines of <code>lpjml/testcase_2cell/windspeed_testcase_2cell.clm.json</code></summary>

```
{
  "filename" : "windspeed_testcase_2cell.clm",
  "variable" : "windspeed",
  "global_attrs" :
  {
    "title" : "GSWP3-W5E5 observational climate input data for ISIMIP3a",
    "institution" : "Potsdam Institute for Climate Impact Research (PIK)",
    "project" : "Inter-Sectoral Impact Model Intercomparison Project phase 3a (ISIMIP3a)",
    "contact" : "ISIMIP cross-sectoral science team <info@isimip.org> <https://www.isimip.org>",
    "summary" : "GSWP3 v1.09 bias-adjusted to W5E5 v2.0 with ISIMIP3BASD v2.5.0 (for 1901-1978) combined with W5E5 v2.0 (for 1979-2019)",
    "license" : "Creative Commons Zero (CC0) 1.0",
    "references" : "Kim (2017) <https://doi.org/10.20783/DIAS.501> for GSWP3; Cucchi et al. (2020) <https://doi.org/10.5194/essd-2020-28> and Lange et al. (2021) <https://doi.org/10.48364/ISIMIP.34221
```

</details>

<details><summary>First lines of <code>lpjml_config_spinup.json</code></summary>

```
{
  "GIT_repo" : "https://github.com/PIK-LPJmL/LPJmL",
  "GIT_hash" : "",
  "sim_name" : "LPJmL Run",
  "sim_id" : "lpjml",
  "coupled_model" : null,
  "coupled_host" : "localhost",
  "coupled_port" : 2224,
  "start_coupling": null,
  "version" : "6.1",
  "global_attrs" : {"institution" : "Potsdam Institute for Climate Impact Research",
                    "contact" : "",
```

</details>

<details><summary>First lines of <code>spinup.log</code></summary>

```
******************************************************************************
****           _     ____     _           _        __         _           ****
****          | |   |  _ \   | |_ __ ___ | |      / /_       / |          ****
****          | |   | |_) |  | | '_ ` _ \| |     | '_ \      | |          ****
****          | |___|  __/ |_| | | | | | | |___  | (_) |  _  | |          ****
****          |_____|_|   \___/|_| |_| |_|_____|  \___/  (_) |_|          ****
****                                                                      ****
****                 lpjml C Version 6.1.9 (Oct 18 2026)                  ****
****    Dynamic global vegetation model with natural and managed land     ****
****                          Compiled for Linux                          ****
****       (C) Potsdam Institute for Climate Impact Research (PIK),       ****
****                          see COPYRIGHT file                          ****
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `stage` | Stages to run | spinup | spinup, spinup_and_transient |
| `spinup_years` | Spinup years (natural vegetation) (The configuration check needs at least 2100 years) | 2100 | 2100 to 3799 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run-lpjml` runs the two stages in `lpjml/` and copies the contents of `output/` up. The files come from the output list in `lpjml_config.cjson`.

- `spinup.log` and `transient.log` hold what the model printed.
- `globalflux_spinup.csv` is a text file with global totals written by the first stage. `globalflux.csv` is the same kind of file from the second stage.
- `grid.bin` and variable files such as `mnpp`, `mgpp`, `mrh`, `mra`, `fpc`, `tas`, `pr` and `mrunoff` hold the transient run's output for the two cells. The configuration names the variable ids (`npp`, `gpp`, `rh`, `ra`, `fpc`, `temp`, `prec`, `runoff`) and the file for each. The files are raw binary, with a `.json` description beside each one (`json_suffix` in the configuration).
- `lpjml_config_spinup.json` and `lpjml_config_restart.json` are the preprocessed configurations the model wrote for each stage (`json_config_filename`).

Convert binary files with the utilities that `make utils` builds: `bin2cdf` for NetCDF, `printclm` for input files and `lpjprint` for restart files. The `-ofiles` option lists the output variables the model offers.

## Pitfalls

- **The spinup has a minimum length.** With the default parameters, the configuration check stops a run whose `nspinup` is below 2100: `veg_equil_year` of 900, plus 20 soil-equilibration calls 60 years apart. It prints ERROR230. The recipe accepts 2100 to 3799 years.
- **Test data only.** `testcase_2cell` has two grid cells. The default `inpath` in the configuration is a path on the developers' cluster, so a global run needs the input data from elsewhere.
- **No `cpp`, no run.** The preprocessor must be on the PATH.
- **Macros decide the configuration.** `NETCDF_INPUT`, `NO_METHANE` and `TESTCASE_2CELL` change which files and options the configuration uses.
- **Warnings stop the build.** `configure.sh` adds `-Werror` unless you pass `-noerror`, so a newer compiler can break it.
- **Restart files tie the stages together.** The second stage needs the file the first stage wrote, under the name the configuration gives.

## Further reading

- Repository and README: https://github.com/PIK-LPJmL/LPJmL
- Installation guide: https://github.com/PIK-LPJmL/LPJmL/blob/master/INSTALL.md
- Paper: Schaphoff S et al. (2018). LPJmL4 - a dynamic global vegetation model with managed land - Part 1: Model description. Geoscientific Model Development 11:1343-1375. https://doi.org/10.5194/gmd-11-1343-2018

---

Cite: Schaphoff S, von Bloh W, Rammig A, et al. (2018). LPJmL4 - a dynamic global vegetation model with managed land - Part 1: Model description. Geosci Model Dev 11:1343-1375. doi:10.5194/gmd-11-1343-2018

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/lpjml).
