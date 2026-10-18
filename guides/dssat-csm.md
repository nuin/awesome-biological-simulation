# DSSAT-CSM

> Simulate one maize crop season (growth, soil water, nitrogen, yield) for a Gainesville, Florida nitrogen and irrigation experiment with the DSSAT cropping system model.

Licence: BSD-3-Clause · [Source code](https://github.com/DSSAT/dssat-csm-os)

## What it simulates

DSSAT-CSM is the cropping system model of the DSSAT suite. It simulates one crop on one field, day by day, from planting to harvest. It follows crop development, leaf area, biomass, yield, soil water, soil nitrogen and soil organic matter, driven by daily weather, a soil profile, a cultivar and the management you set. The suite covers more than 45 crops, each with its own crop module.

An experiment is a plain-text FileX with sections for treatments, cultivars, fields, initial conditions, planting, irrigation, fertilizer and simulation controls. A treatment is a set of levels from those sections. The weather file (`.WTH`) and the soil file (`.SOL`) sit in their own folders. The crop file extension names the crop: `.MZX` is maize.

The recipe runs experiment UFGA8201 from the DSSAT data repository: maize at Gainesville, Florida in 1982, with rainfed, irrigated and vegetative-stress water treatments crossed with low and high nitrogen. That gives six treatments.

## When to use it

Use DSSAT-CSM for field-scale questions on yield, water and nitrogen under a cultivar and management, especially where cultivar coefficients exist.

- Use [PCSE](pcse.md) when you want to script WOFOST or LINTUL from Python and swap process modules.
- Use [AquaCrop-OSPy](aquacrop-ospy.md) when you want a simpler water-driven model with few parameters.
- Use [APSIM Next Generation](apsim-next-generation.md) when you need rotations, trees or livestock in one framework.

## Install

The Windows release is an installer from https://dssat.net/. On Linux and macOS you build the source:

```
git clone --depth 1 --branch v4.8.6.0 https://github.com/DSSAT/dssat-csm-os
cd dssat-csm-os && mkdir build && cd build
cmake .. -DCMAKE_BUILD_TYPE=RELEASE -DCMAKE_INSTALL_PREFIX=$HOME/dssat
make && make install
```

This needs CMake and a Fortran compiler such as gfortran. The README says the default build type is DEBUG, so ask for RELEASE. The latest release is v4.8.6.0, with notes dated 2026-07-01. The source is BSD-3-Clause.

`make install` copies the program `dscsm048`, a `run_dssat` wrapper and the `Data` folder (genotype files, code tables and the `DSSATPRO.L48` path file) to the prefix. The crop experiments, weather and soil files live in a second repository, https://github.com/DSSAT/dssat-csm-data, which the README says to combine with the first. That repository has the same v4.8.6.0 tag and no licence file, so the recipe fetches it when you build the image and does not copy it. Copy it into the install prefix, and set `DSSAT_HOME` to the prefix if the program does not find `DSSATPRO.L48` in the current directory.

## A first run

Adapted from the usage text in [`Utilities/CheckRunMode.f90`](https://github.com/DSSAT/dssat-csm-os/blob/v4.8.6.0/Utilities/CheckRunMode.f90). Command-line mode `C` runs one treatment of one experiment file from the current directory:

```
cd $HOME/work
cp $DSSAT_HOME/Maize/UFGA8201.MZX $DSSAT_HOME/Weather/UFGA8201.WTH .
$DSSAT_HOME/dscsm048 C UFGA8201.MZX 1
```

The other modes in the same text are `A` (all treatments in a FileX), `B` (a batch file such as `DSSBatch.v48`), `D`, `E`, `F`, `G`, `I`, `L`, `N`, `Q`, `S`, `T` and `Y`. A leading 8-character model name, for example `MZCER048`, overrides the default model for the crop.

## Run the tested example

This recipe builds DSSAT-CSM in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1 s. DSSAT-CSM has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [dssat-csm-recipe.tar.gz](https://biosimhub.pages.dev/guides/dssat-csm/dssat-csm-recipe.tar.gz) (Dockerfile, run_dssat.sh, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf dssat-csm-recipe.tar.gz
   cd dssat-csm
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/dssat-csm:4.8.6.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/dssat-csm:4.8.6.0 sh /opt/run_dssat.sh 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `DSSAT48.INH` | 4.2 KB |
| `DSSAT48.INP` | 5.5 KB |
| `ET.OUT` | 23.6 KB |
| `EnvSum.OUT` | 2.0 KB |
| `Evaluate.OUT` | 927 B |
| `GHG.OUT` | 16.6 KB |
| `INFO.OUT` | 5.8 KB |
| `MgmtEvent.OUT` | 1.8 KB |
| `MgmtOps.OUT` | 11.7 KB |
| `Mulch.OUT` | 6.5 KB |
| `N2O.OUT` | 68.0 KB |
| `OUTPUT.LST` | 1.7 KB |
| `OVERVIEW.OUT` | 9.7 KB |
| `PlantGro.OUT` | 45.2 KB |
| `PlantN.OUT` | 14.9 KB |
| `RunList.OUT` | 80 B |
| `SWBalSum.OUT` | 1.2 KB |
| `SoilNBalSum.OUT` | 1.5 KB |
| `SoilNi.OUT` | 45.8 KB |
| `SoilNiBal.OUT` | 2.0 KB |
| `SoilNoBal.OUT` | 1.3 KB |
| `SoilTemp.OUT` | 12.8 KB |
| `SoilWat.OUT` | 27.5 KB |
| `SoilWatBal.OUT` | 1.3 KB |
| `SoilWater.OUT` | 49.6 KB |
| `Summary.OUT` | 2.3 KB |
| `UFGA8201.MZA` | 822 B |
| `UFGA8201.MZT` | 16.1 KB |
| `UFGA8201.MZX` | 5.0 KB |
| `UFGA8201.WTH` | 17.7 KB |
| `WARNING.OUT` | 1.1 KB |
| `Weather.OUT` | 20.4 KB |
| `run_log.txt` | 284 B |

<details><summary>First lines of <code>DSSAT48.INH</code></summary>

```
*EXP.DETAILS: UFGA8201MZ NIT X IRR, GAINESVILLE 2N*3I                                

*FILES
@N  EXP.DATA    AFILE        ADIR
  1 EXP         UFGA8201.MZA                                                                                 
@N  SPECIES     SPFILE       SPDIR
  1 SPE         MZCER048.SPE ///opt/dssat/Genotype/                                                          
@N  ECOTYPE     EFILE        EDIR
  1 ECO         MZCER048.ECO ///opt/dssat/Genotype/                                                          
@N  CULTIVAR    CFILE        CDIR
  1 CUL         MZCER048.CUL ///opt/dssat/Genotype/                                                          
@N  SOIL        SFILE        SDIR
```

</details>

<details><summary>First lines of <code>DSSAT48.INP</code></summary>

```
*MODEL INPUT FILE            C     1     1     1   999     0
*FILES              
MODEL          MZCER048
FILEX          UFGA8201.MZX                                                                                 
FILEA          UFGA8201.MZA                                                                                 
FILET          UFGA8201.MZT                                                                                 
SPECIES        MZCER048.SPE ///opt/dssat/Genotype/                                                          
ECOTYPE        MZCER048.ECO ///opt/dssat/Genotype/                                                          
CULTIVAR       MZCER048.CUL ///opt/dssat/Genotype/                                                          
PESTS          MZCER048.PST ///opt/dssat/Pest/                                                              
SOILS          SOIL.SOL     ///opt/dssat/Soil/                                                              
WEATHERW       UFGA8201.WTH                                                                                 
```

</details>

<details><summary>First lines of <code>ET.OUT</code></summary>

```
*SOIL-PLANT-ATMOSPHERE MODULE OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
@YEAR DOY   DAS   SRAA  TMAXA  TMINA    REFA    EOAA    EOPA    EOSA    ETAA    EPAA    ESAA    EFAA    EMAA    EOAC    ETAC    EPAC    ESAC    EFAC    EMAC    KCAA    KBSA    KEAA
 1982 056     1  14.80  27.20  10.60 -99.000   3.545   0.000   3.545   2.727   0.000   2.727   0.000   0.000    3.54    2.73    0.00    2.73    0.00    0.00 -99.000 -99.000 -99.000 
```

</details>

<details><summary>First lines of <code>EnvSum.OUT</code></summary>

```
*Environmental Summary: DSSAT Cropping System Model Ver. 4.8.6.000      -HEAD    OCT 18, 2026; 04:44:48

!                                                                                    SEASONAL ENVIRONMENTAL DATA
!IDENTIFIERS..........................................  GHG Emissions (kg/ha) ....   Planting to Harvest ...........................................................................  Phase 1: Emergence
@   RUNNO   TRNO R# O# P# CR MODEL... EXNAME..    HDAT  N2OEM  CO2EM  CH4EM  TCEQM   NDCH  DAYLA   CO2A  TMINA  TAVGA  TMAXA  SRADA   PRCP   PETP   ETCP   ESCP   EPCP   WSGA   NSTA  NDCH1  TMIN1  TAVG
        1      1  1  0  1 MZ MZCER048 UFGA8201 1982185  0.095   337.  0.000  1281.    128   12.9  340.9   16.0   22.7   29.3   18.5  660.7  565.3  284.4   97.4  189.7   0.15   0.19     18   14.4   21.
```

</details>

<details><summary>First lines of <code>Evaluate.OUT</code></summary>

```
*EVALUATION : UFGA8201MZ NIT X IRR, GAINESVILLE 2N*3I                                 DSSAT Cropping System Model Ver. 4.8.6.000      -HEAD    OCT 18, 2026; 04:44:48

@RUN EXCODE        TN RN CR   ADAPS   ADAPM   PD1PS   PD1PM   PDFPS   PDFPM   MDAPS   MDAPM   HWAMS   HWAMM   PWAMS   PWAMM   H#AMS   H#AMM   HWUMS   HWUMM   H#UMS   H#UMM   CWAMS   CWAMM   BWAMS   BW
   1 UFGA8201MZ     1  1 MZ      76      75     -99     -99     -99     -99     128     128    2293   2929.     -99     -99     742    917.  0.3090   0.218   110.9    229.    6556   5532.    4307   35
```

</details>

<details><summary>First lines of <code>GHG.OUT</code></summary>

```
*GHG emissions output file

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
!               |---------- Daily (g/ha) ----------|------- Cumulative (kg/ha) --------|---- Cum CO2-equiv kg[CO2eq]/ha ---|
!               Soil CO2  Net CO2      N2O      CH4 Soil CO2  Net CO2      N2O      CH4  Net CO2      N2O      CH4    Total
```

</details>

<details><summary>First lines of <code>INFO.OUT</code></summary>

```
*INFO DETAIL FILE

******************************************************************************

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN               UFGA8201    1

 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN
  
```

</details>

<details><summary>First lines of <code>MgmtEvent.OUT</code></summary>

```
*MANAGEMENT OPERATIONS EVENT SUMMARY

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
!---------------------------------------------------------------------------------------------
@RUN Date........  DOY    DAS    DAP  CR  Stage         Operation       Quantities
```

</details>

<details><summary>First lines of <code>MgmtOps.OUT</code></summary>

```
*MANAGEMENT OPERATIONS DAILY OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  

@YEAR DOY   DAS   DAP  IR#C  IRRC  TL#C  TLDD DLYR3   TLBD  NAPC  NICM  R#AC RESNC RESPC
```

</details>

<details><summary>First lines of <code>Mulch.OUT</code></summary>

```
*Surface Mulch daily output file

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
@YEAR DOY   DAS    MCFD   MDEPD    MWAD    MWTD
 1982 055     0   0.000    0.00       0    0.00
```

</details>

<details><summary>First lines of <code>N2O.OUT</code></summary>

```
*N2O emissions output file

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
!              |------------------------------ Cumulative -----------------------------|------------------------------ Daily ----------------------------------|
!               N2Oemit  N2emit  NOemit   Denit  Nitrif   N2O-denit+nit      N2      NO N2Oemit  N2emit  NOemit   Denit  Nitrif   N2O-denit+nit      N2      NO   Denitrification (g[N]/ha) by soil dept
```

</details>

<details><summary>First lines of <code>OUTPUT.LST</code></summary>

```
*Output file list

@FILENAME          DESCRIPTION
ET.OUT             Daily soil-plant-atmosphere output file           
MgmtOps.OUT        Daily management operations output file           
PlantGro.OUT       Daily plant growth output file                    
PlantN.OUT         Daily plant nitrogen output file                  
SoilNi.OUT         Daily inorganic soil N output file                
SoilTemp.OUT       Daily soil temperature output file                
SoilWat.OUT        Daily soil water output file                      
Weather.OUT        Daily weather output file                         
Mulch.OUT          Daily surface mulch output file                   
```

</details>

<details><summary>First lines of <code>OVERVIEW.OUT</code></summary>

```
*SIMULATION OVERVIEW FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048


 CROP           : Maize            CULTIVAR : McCurdy 84aa     ECOTYPE :IB0001
```

</details>

<details><summary>First lines of <code>PlantGro.OUT</code></summary>

```
*GROWTH ASPECTS OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
!                                                                                                                                                                                                       
!                                                                                                                                                                                                       
```

</details>

<details><summary>First lines of <code>PlantN.OUT</code></summary>

```
*PLANT N OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
@YEAR DOY   DAS   DAP   CNAD   GNAD   VNAD   GN%D   VN%D   NUPC   LNAD   SNAD   LN%D   SN%D   RN%D   SNN0C   SNN1C
 1982 057     2     0    0.0    0.0    0.0   0.00   0.00    0.0    0.0    0.0    0.0   0.00   0.00    0.00    0.00
```

</details>

<details><summary>First lines of <code>RunList.OUT</code></summary>

```
 NREP  EXP  TRT  NYR FILEX        DESCRIPTION
    1    1    1    1 UFGA8201.MZX
```

</details>

<details><summary>First lines of <code>SWBalSum.OUT</code></summary>

```
*WATER BALANCE SUMMARY OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  

!                           |----- Initial Water Content (mm) -----|------ Final Water Content (mm) -------|-------- Water Additions (mm) ---------|--------------- Water Losses (mm) ---------------|--
```

</details>

<details><summary>First lines of <code>SoilNBalSum.OUT</code></summary>

```

*SOIL N BALANCE - CENTURY ROUTINES

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

!                              |--------------- Initial N State Variables ----------------|----------------- Final N State Variables -----------------|------------- N Additions -------------|---------
!                              |----------------- Organic ----------------------|         |------------------ Organic ----------------------|         |  Harvest   Applied                    |         
!                              | Surface      SOM1      SOM2      SOM3    Litter     Inorg|  Surface      SOM1      SOM2      SOM3    Litter     Inorg|  Residue   Residue  Fertiliz   Senesed|  Leached
@Run FILEX               TN CR     SN0Di    S1NTDi    S2NTDi    S3NTDi     LNTDi     NIADi      SN0D     S1NTD     S2NTD     S3NTD      LNTD      NIAD      HRNH     RESNC      NICM     SNNTC      NLCM
   1 UFGA8201.MZX         1 MZ      0.00      0.00   8708.00      0.00      8.90     15.38      0.00      0.00   8668.85      0.00      5.94     41.54      0.00      0.00    116.00      2.81     32.67
```

</details>

<details><summary>First lines of <code>SoilNi.OUT</code></summary>

```
*Soil Inorganic Nitrogen daily output file

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
!                                                                                                                                      NO3 (ppm) at soil dep. (cm):                                     
!                                                                                                                                       0-5    5-15   15-30   30-45   45-60   60-90  90-120 120-150 150-
```

</details>

<details><summary>First lines of <code>SoilNiBal.OUT</code></summary>

```
*SOIL INORGANIC N BALANCE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  


```

</details>

<details><summary>First lines of <code>SoilNoBal.OUT</code></summary>

```
*SOIL ORGANIC N BALANCE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  


```

</details>

<details><summary>First lines of <code>SoilTemp.OUT</code></summary>

```
*SOIL TEMPERATURE OUTPUT FILE (DAILY)

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
! TAV  =    20.9
! TAMP =    13.0
```

</details>

<details><summary>First lines of <code>SoilWat.OUT</code></summary>

```
*SOIL WATER DAILY OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
!                                                                                                                                         Soil water content (mm3/mm3) by layer (cm):
!                                                                                                                                           0-5    5-15   15-30   30-45   45-60   60-90  90-120 120-150 
```

</details>

<details><summary>First lines of <code>SoilWatBal.OUT</code></summary>

```
*WATER BALANCE OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  

!     WATER BALANCE PARAMETERS
```

</details>

<details><summary>First lines of <code>SoilWater.OUT</code></summary>

```
*SOIL WATER BY LAYER DAILY OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  

!----------------------------
```

</details>

<details><summary>First lines of <code>Summary.OUT</code></summary>

```
*SUMMARY : UFGA8201MZ NIT X IRR, GAINESVILLE 2N*3I                                 DSSAT Cropping System Model Ver. 4.8.6.000      -HEAD    OCT 18, 2026; 04:44:48

!IDENTIFIERS......................... EXPERIMENT AND TREATMENT.......... SITE INFORMATION............................................................. DATES............................................
@   RUNNO   TRNO R# O# P# CR MODEL... EXNAME.. TNAM..................... FNAM.... WSTA.... WYEAR SOIL_ID...             XLAT            LONG      ELEV    SDAT    PDAT    EDAT    ADAT    MDAT    HDAT  
        1      1  1  0  1 MZ MZCER048 UFGA8201 RAINFED LOW NITROGEN      UFGA0002 UFGA8201  1982 IBMZ910014         -82.3689          29.638        40 1982056 1982057 1982068 1982133 1982185 1982185  
```

</details>

<details><summary>First lines of <code>UFGA8201.MZA</code></summary>

```
*EXP. DATA (A): UFGA8201MZ Z N X IRRIGATION, GAINESVILLE                               

! File last edited on day 06/24/2026 at 12:18:09 PM
!
! 
! 
! Grain yield (HWAM) expressed as dry weight
@TRNO   HWAM  HWUM  H#AM  H#UM  LAIX  CWAM  BWAH    ADAT    MDAT  GN%M  CNAM  SNAM  GNAM
     1 2929. 0.218  917.  229.  2.26 5532. 3530. 1982132 1982185  1.80  69.5  37.8  31.7
     2 3130. 0.209 1494.  220.  2.84 7201. 4071. 1982132 1982185  1.80 104.8  47.8  57.0
     3 6850. 0.227 3013.  343.  3.26 14581 7729. 1982132 1982185  1.80 130.9  38.5  92.4
     4 11881 0.309 3847.  496.  4.09 22001 10120 1982132 1982185  1.60 267.7  74.8 192.9
```

</details>

<details><summary>First lines of <code>UFGA8201.MZT</code></summary>

```
*EXP. DATA (T): UFGA8201MZ N X IRRIGATION, GAINESVILLE                                 

! File last edited on day 06/24/2026 at 12:18:35 PM
!
! 
! 
! This was distributed with DSSAT V3.5, so available with no problems.
! Thesis or dissertation of Mutti.  Check whether anything is published.
! Possibly also canopy assimilation measured by Jones and published.
! Reliable data set.  Data on N, P, and K conc. also here.
! Additional data entered by P.V. Vara Prasad and K. J. Boote in 2001
@TRNO     DATE  CWAD  LAID  GWAD  LWAD  SWAD  VN%D  SLAD  FRLF  FRST  HIAD  CNAD  NUPC  LN%D  SN%D  GN%D  LP%D  SP%D  GP%D  LK%D  SK%D  GK%D  LNAD  SNAD  GNAD  LPAD  SPAD  GPAD  LKAD  SKAD  GKAD
```

</details>

<details><summary>First lines of <code>UFGA8201.MZX</code></summary>

```
*EXP.DETAILS: UFGA8201MZ NIT X IRR, GAINESVILLE 2N*3I

*GENERAL
@PEOPLE
 BENNETT,J.M. ZUR,B. HAMMOND,L.C. JONES,J.W.
@ADDRESS
 UNIVERSITY OF FLORIDA, GAINESVILLE, FL, USA
@SITE
 Irrigation Park, University of Florida

*TREATMENTS                        -------------FACTOR LEVELS------------
@N R O C TNAME.................... CU FL SA IC MP MI MF MR MC MT ME MH SM
```

</details>

<details><summary>First lines of <code>UFGA8201.WTH</code></summary>

```
*WEATHER DATA : Gainesville,Florida,USA

@ INSI      LAT     LONG  ELEV   TAV   AMP REFHT WNDHT
  UFGA   29.630  -82.370    10  20.9  13.0  2.00  3.00
@DATE  SRAD  TMAX  TMIN  RAIN               PAR 
82001   5.9  24.4  15.6  19.0              12.4 
82002   7.0  22.2  15.0   0.0              14.2 
82003   9.0  27.8  17.2   0.0              18.4 
82004   3.1  26.1  15.0   9.4               6.4 
82005  12.9  17.2   2.2   0.0              26.3 
82006  11.4  25.0   4.4   0.0              22.2 
82007   8.5  26.7  11.7   0.0              17.6 
```

</details>

<details><summary>First lines of <code>WARNING.OUT</code></summary>

```
*WARNING DETAIL FILE

******************************************************************************

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
```

</details>

<details><summary>First lines of <code>Weather.OUT</code></summary>

```
*WEATHER MODULE DAILY OUTPUT FILE

*DSSAT Cropping System Model Ver. 4.8.6.000 -HEAD  OCT 18, 2026 04:44:48

*RUN   1        : RAINFED LOW NITROGEN      MZCER048 UFGA8201    1
 MODEL          : MZCER048 - Maize
 EXPERIMENT     : UFGA8201 MZ NIT X IRR, GAINESVILLE 2N*3I
 DATA PATH      :
 TREATMENT  1   : RAINFED LOW NITROGEN      MZCER048
  
@YEAR DOY   DAS   PRED  CPRED  DAYLD   TWLD   SRAD   PARD   CLDD   TMXD   TMND   TAVD   TDYD   TDWD   TGAD   TGRD   WDSD   CO2D   VPDF    VPD  OZON7   WDATE
 1982 056     1    0.0    0.0   11.2   12.2   14.8   30.3   0.30   27.2   10.6   18.4   21.6   10.6   18.4   21.6   86.4  340.7   0.00   0.00 -99.00 1982056
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
dscsm048 C UFGA8201.MZX 1











```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `treatment` | Treatment (1-2 rainfed, 3-4 irrigated, 5-6 vegetative stress; odd = low nitrogen) | 1 | 1 to 6 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

DSSAT writes its `.OUT` files into the current directory. Which ones appear depends on the OUTPUTS line of the FileX. UFGA8201 asks for the overview, the summary, daily growth, soil water and soil nitrogen.

- `Overview.OUT` has the run header, the inputs as read, and the crop and soil results for each treatment.
- `Summary.OUT` has one row per treatment, with the planting, anthesis and maturity dates, the grain yield and the water and nitrogen totals.
- `PlantGro.OUT` has one row per day with growth stage, leaf area index, biomass and grain weight.
- `SoilWat.OUT` and `SoilNi.OUT` have the daily water and nitrogen balance by layer.
- `WARNING.OUT` lists warnings that DSSAT raised.

Dates in the files are in YYDOY form, so 82056 is day 56 of 1982. The `.MZA` and `.MZT` files that sit beside the FileX hold the measured end-of-season and time-series values for the same experiment, so you can compare simulated and observed yield.

## Pitfalls

- **Files must be where DSSAT looks.** It reads the FileX from the current directory and finds the path file through the current directory, the FileX folder or `DSSAT_HOME`.
- **The data are a separate download.** A source build alone has no experiments, weather or soil files.
- **Weather file names carry the station and year.** `UFGA8201.WTH` is station UFGA, year 82, sequence 01. A FileX names its weather station in the FIELDS section.
- **One FileX holds many treatments.** Mode `C` needs the treatment number, and mode `A` runs them all.
- **Output files are overwritten.** Run each case in its own folder.
- **The source build is the engine only.** The release notes list a DSSAT Shell and the GB2 and XB2 tools, but the CMake project builds one program, `dscsm048`.

## Further reading

- Project site and documentation: https://dssat.net/
- Source: https://github.com/DSSAT/dssat-csm-os
- Data repository: https://github.com/DSSAT/dssat-csm-data
- How to cite: https://dssat.net/how-to-cite-dssat/
- Paper: Jones JW, Hoogenboom G, Porter CH, et al. (2003). The DSSAT cropping system model. European Journal of Agronomy 18:235-265. https://doi.org/10.1016/S1161-0301(02)00107-7

---

Cite: Jones JW, Hoogenboom G, Porter CH, et al. (2003). The DSSAT cropping system model. European Journal of Agronomy 18:235-265. doi:10.1016/S1161-0301(02)00107-7

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/dssat-csm).
