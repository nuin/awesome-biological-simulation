# AquaCrop

> Water-driven crop growth and yield for a season, from daily climate, soil, crop and management files, run through a project (PRM) file.

Licence: BSD-3-Clause · [Source code](https://github.com/KUL-RSDA/AquaCrop)

## What it simulates

AquaCrop is the FAO crop model for water-limited yield. It runs on a daily time step through a growing season. A soil water balance tracks rain, irrigation, runoff, drainage, evaporation and transpiration. The crop side tracks canopy cover, root depth, biomass and the harvest index, and turns water stress into biomass and yield. Salinity, fertility, temperature and weed stress can reduce growth too.

This catalog entry is the open-source Fortran code from KU Leuven, which the project says is endorsed by FAO. The repository holds version 7.3. You describe a run through a text project file (`.PRM`) that points to the input files:

- **Climate (CLI):** with temperature (Tnx or TMP), reference evapotranspiration (ETo), rain (PLU) and atmospheric CO2.
- **Calendar (CAL), crop (CRO), field management (MAN), soil profile (SOL).**
- **Optional:** irrigation management (IRR), groundwater table (GWT), initial soil water (SW0), off-season conditions (OFF) and field observations (OBS).

A project file can chain several seasons. The bundled Ottawa project has three cultivation years, and its harvests file lists several cuttings per year.

## When to use it

Use AquaCrop when the question is how water supply and irrigation change yield, and you have daily weather and soil data for a field or a grid cell.

- Use [LPJmL](lpjml.md) when you want vegetation, carbon and water at global or regional scale, with natural vegetation and crops together.
- Use a general ODE tool, such as [XPPAUT](xppaut.md), when you want to write the crop equations yourself.

The model is a field-scale tool. It has no spatial transport between fields. For a map of yields you run it once per cell, as NASA's Land Information System does when it uses AquaCrop as a crop model, which the README mentions.

## Install

There are two routes, both from the README at https://github.com/KUL-RSDA/AquaCrop.

**Prebuilt executable.** The GitHub release page for v7.3_typofix (13 February 2026) lists `aquacrop-7.3-x86_64-linux.zip`, macOS and Windows zips, a Windows GUI and the release notes. The testcase README says only x86-64 CPUs are supported for the precompiled executable.

**Build from source.** The README asks for GNU Make 3.82 or later and GNU Fortran 6.4.0 or later (or ifort 18.0.1):

```bash
git clone https://github.com/KUL-RSDA/AquaCrop.git
cd AquaCrop/src
make
```

The `bin` target builds the `aquacrop` executable and `lib` builds `libaquacrop.so`. The Makefile has `STATIC=1` for a static executable and `DEBUG=1` for a debug build. The recipe below builds the v7.3_typofix tag with `make bin STATIC=1` inside a `gcc:14.2.0` image. It runs on x86-64.

## A first run

Adapted from the testcase README in the repository, https://github.com/KUL-RSDA/AquaCrop/blob/master/testcase/README.md.

The `testcase/` folder is self-contained. Copy the executable into it and run it from there:

```bash
cd AquaCrop/testcase
cp ../src/aquacrop .
./aquacrop
```

AquaCrop reads `LIST/ListProjects.txt`, which names `Ottawa.PRM`. It reads the data files from `DATA/`, `OBS/`, `PARAM/` and `SIMUL/`, and writes results into `OUTP/`. The README says the calculation finishes in a few seconds. To check it, compare each file in `OUTP/` with the same file in `OUTP_REF/`. Apart from the first line, which holds the creation date, they should match:

```bash
diff OUTP/AllDone.OUT OUTP_REF/AllDone.OUT
```

## Run the tested example

This recipe builds AquaCrop in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 0.6 s. AquaCrop has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [aquacrop-recipe.tar.gz](https://biosimhub.pages.dev/guides/aquacrop/aquacrop-recipe.tar.gz) (Dockerfile, run.sh, example project.prm, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf aquacrop-recipe.tar.gz
   cd aquacrop
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/aquacrop:7.3 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/aquacrop:7.3 /usr/local/bin/run-aquacrop /work/in/project.prm > out/aquacrop_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `AllDone.OUT` | 9 B |
| `ListProjectsLoaded.OUT` | 602 B |
| `aquacrop_stdout.txt` | 0 B |
| `case/DATA/21May.CAL` | 639 B |
| `case/DATA/AlfOttawaGDD.CRO` | 7.8 KB |
| `case/DATA/Ottawa.CLI` | 101 B |
| `case/DATA/Ottawa.ETo` | 4.6 KB |
| `case/DATA/Ottawa.MAN` | 1.4 KB |
| `case/DATA/Ottawa.PLU` | 4.6 KB |
| `case/DATA/Ottawa.SOL` | 678 B |
| `case/DATA/Ottawa.Tnx` | 10.8 KB |
| `case/LIST/ListProjects.txt` | 12 B |
| `case/LIST/Ottawa.PRM` | 3.5 KB |
| `case/LIST/project.PRM` | 3.5 KB |
| `case/OBS/Ottawa.OBS` | 3.6 KB |
| `case/OUTP/.gitkeep` | 0 B |
| `case/OUTP/AllDone.OUT` | 9 B |
| `case/OUTP/ListProjectsLoaded.OUT` | 602 B |
| `case/OUTP/projectPRM1evaluation.OUT` | 2.3 KB |
| `case/OUTP/projectPRM2evaluation.OUT` | 2.3 KB |
| `case/OUTP/projectPRM3evaluation.OUT` | 2.3 KB |
| `case/OUTP/projectPRMday.OUT` | 783.2 KB |
| `case/OUTP/projectPRMharvests.OUT` | 2.1 KB |
| `case/OUTP/projectPRMseason.OUT` | 1.9 KB |
| `case/PARAM/Ottawa.PPn` | 2.1 KB |
| `case/PARAM/project.PPn` | 2.1 KB |
| `case/README.md` | 2.2 KB |
| `case/SIMUL/AggregationResults.SIM` | 97 B |
| `case/SIMUL/DEFAULT.CRO` | 6.7 KB |
| `case/SIMUL/DEFAULT.SOL` | 628 B |
| `case/SIMUL/DailyResults.SIM` | 349 B |
| `case/SIMUL/DailyResultsFullList.SIM` | 701 B |
| `case/SIMUL/EToData.SIM` | 4.0 KB |
| `case/SIMUL/MaunaLoa.CO2` | 1.3 KB |
| `case/SIMUL/OttawaReference.Tnx` | 570 B |
| `case/SIMUL/ParticularResults.SIM` | 131 B |
| `case/SIMUL/ParticularResultsFullList.SIM` | 613 B |
| `case/SIMUL/RainData.SIM` | 4.0 KB |
| `case/SIMUL/TCrop.SIM` | 3.6 KB |
| `case/SIMUL/TCropReference.SIM` | 7.5 KB |
| `case/SIMUL/TempData.SIM` | 7.6 KB |
| `case/SIMUL/TnxReference365Days.SIM` | 7.5 KB |
| `projectPRM1evaluation.OUT` | 2.3 KB |
| `projectPRM2evaluation.OUT` | 2.3 KB |
| `projectPRM3evaluation.OUT` | 2.3 KB |
| `projectPRMday.OUT` | 783.2 KB |
| `projectPRMharvests.OUT` | 2.1 KB |
| `projectPRMseason.OUT` | 1.9 KB |

<details><summary>First lines of <code>AllDone.OUT</code></summary>

```
All done
```

</details>

<details><summary>First lines of <code>ListProjectsLoaded.OUT</code></summary>

```
Intermediate results: None created

Daily output results:
1. - soil water balance
2. - crop development and production
3. - soil water content in the soil profile and root zone
4. - soil salinity in the soil profile and root zone
5. - soil water content at various depths of the soil profile
6. - soil salinity at various depths of the soil profile
7. - climate input parameters

Particular results:
```

</details>

<details><summary>First lines of <code>case/DATA/21May.CAL</code></summary>

```
Onset: 21 May - spring 2014 alfafla seeded in Field 13
         7.3  : AquaCrop Version (January 2026)
         0    : The onset of the growing period is fixed on a specific date
        -9    : Day-number (1 ... 366) of the Start of the time window for the onset criterion: Not applicable
        -9    : Length (days) of the time window for the onset criterion: Not applicable
       141    : Day-number (1 ... 366) for the onset of the growing period
        -9    : preset value for generation of the onset: Not applicable
        -9    : Number of successive days: Not applicable
        -9    : Number of occurrences: Not applicable
```

</details>

<details><summary>First lines of <code>case/DATA/AlfOttawaGDD.CRO</code></summary>

```
Ottawa variety - Alfalfa - Louvain-La-Neuve (Belgium) -  adjusted for Ottawa - calibrated for Soil Fertility
     7.3       : AquaCrop Version (January 2026)
     1         : File not protected
     4         : forage crop
     1         : Crop is sown in 1st year
     0         : Determination of crop cycle : by growing degree-days
     1         : Soil water depletion factors (p) are adjusted by ETo
     5.0       : Base temperature (degC) below which crop development does not progress
    30.0       : Upper temperature (degC) above which crop development no longer increases with an increase in temperature
  1920         : Total length of crop cycle in growing degree-days
     0.15      : Soil water depletion factor for canopy expansion (p-exp) - Upper threshold
     0.55      : Soil water depletion factor for canopy expansion (p-exp) - Lower threshold
```

</details>

<details><summary>First lines of <code>case/DATA/Ottawa.CLI</code></summary>

```
Ottawa, Canada
 7.3  : AquaCrop Version (January 2026)
Ottawa.Tnx
Ottawa.ETo
Ottawa.PLU
MaunaLoa.CO2
```

</details>

<details><summary>First lines of <code>case/DATA/Ottawa.ETo</code></summary>

```
Ottawa, Canada
     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)
     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)
     1  : First month of record
  2014  : First year of record (1901 if not linked to a specific year)

  Average ETo (mm/day)
=======================
0.0
0.0
0.0
0.3
```

</details>

<details><summary>First lines of <code>case/DATA/Ottawa.MAN</code></summary>

```
Ottawa, Canada
     7.3       : AquaCrop Version (January 2026)
     0         : percentage (%) of ground surface covered by mulches IN growing period
    50         : effect (%) of mulches on reduction of soil evaporation
    50         : Degree of soil fertility stress (%) - Effect is crop specific
     0.00      : height (m) of soil bunds
     0         : surface runoff NOT affected by field surface practices
     0         : N/A (surface runoff is not affected or completely prevented)
     0         : relative cover of weeds at canopy closure (%)
     0         : increase of relative cover of weeds in mid-season (+%)
   100.00      : shape factor of the CC expansion function in a weed infested field
   100         : replacement (%) by weeds of the self-thinned part of the CC - only for perennials
```

</details>

<details><summary>First lines of <code>case/DATA/Ottawa.PLU</code></summary>

```
Ottawa, Canada
     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)
     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)
     1  : First month of record
  2014  : First year of record (1901 if not linked to a specific year)

  Total Rain (mm)
=======================
0.3
0.9
0.1
1.1
```

</details>

<details><summary>First lines of <code>case/DATA/Ottawa.SOL</code></summary>

```
Ottawa, Canada - sandy loam - Field of the Canadian Food Inspection Agency (CFIA)
        7.3  : AquaCrop Version (January 2026)
       46                   : CN (Curve Number)
        7                   : Readily evaporable water from top layer (mm)
        1                   : number of soil horizons
       -9                   : variable no longer applicable
  Thickness  Sat   FC    WP     Ksat   Penetrability  Gravel  CRa       CRb           description
  ---(m)-   ----(vol %)-----  (mm/day)      (%)        (%)    -----------------------------------------
    1.50    46.0  29.0  13.0  1200.0        100         0     -0.390600  1.255639   sandy loam               
```

</details>

<details><summary>First lines of <code>case/DATA/Ottawa.Tnx</code></summary>

```
Ottawa, Canada
     1  : Daily records (1=daily, 2=10-daily and 3=monthly data)
     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)
     1  : First month of record
  2014  : First year of record (1901 if not linked to a specific year)

  Tmin (C)   TMax (C)
========================
-31.3	-21.4
-29.9	-23.4
-32.3	-24.1
-29.8	-4.2
```

</details>

<details><summary>First lines of <code>case/LIST/ListProjects.txt</code></summary>

```
project.PRM
```

</details>

<details><summary>First lines of <code>case/LIST/Ottawa.PRM</code></summary>

```
Ottawa (Canada)
      7.3  : AquaCrop Version (January 2026)
      1         : Year number of cultivation (Seeding/planting year)
  41414         : First day of simulation period - 21 May 2014      
  41577         : Last day of simulation period - 31 October 2014  
  41414         : First day of cropping period - 21 May 2014      
  41577         : Last day of cropping period - 31 October 2014  
-- 1. Climate (CLI) file
   Ottawa.CLI
   './DATA/'
   1.1 Temperature (Tnx or TMP) file
   Ottawa.Tnx
```

</details>

<details><summary>First lines of <code>case/LIST/project.PRM</code></summary>

```
Ottawa (Canada)
      7.3  : AquaCrop Version (January 2026)
      1         : Year number of cultivation (Seeding/planting year)
  41414         : First day of simulation period - 21 May 2014      
  41577         : Last day of simulation period - 31 October 2014  
  41414         : First day of cropping period - 21 May 2014      
  41577         : Last day of cropping period - 31 October 2014  
-- 1. Climate (CLI) file
   Ottawa.CLI
   './DATA/'
   1.1 Temperature (Tnx or TMP) file
   Ottawa.Tnx
```

</details>

<details><summary>First lines of <code>case/OBS/Ottawa.OBS</code></summary>

```
Ottawa, Canada
     7.3  : AquaCrop Version (January 2026)
     1.00  : depth of sampled soil profile
     1     : first day of observations
     1     : first month of observations
  2014     : first year of observations (1901 if not linked to a specific year)

   Day    Canopy cover (%)    dry Biomass (ton/ha)    Soil water content (mm)
            Mean     Std         Mean       Std           Mean      Std
=============================================================================
   144      -9.0    -9.0         0.045     -9.0           -9.0     -9.0
   160      -9.0    -9.0         0.386     -9.0           -9.0     -9.0
```

</details>

<details><summary>First lines of <code>case/OUTP/AllDone.OUT</code></summary>

```
All done
```

</details>

<details><summary>First lines of <code>case/OUTP/ListProjectsLoaded.OUT</code></summary>

```
Intermediate results: None created

Daily output results:
1. - soil water balance
2. - crop development and production
3. - soil water content in the soil profile and root zone
4. - soil salinity in the soil profile and root zone
5. - soil water content at various depths of the soil profile
6. - soil salinity at various depths of the soil profile
7. - climate input parameters

Particular results:
```

</details>

<details><summary>First lines of <code>case/OUTP/projectPRM1evaluation.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59
Evaluation of simulation results - Statistics
** Run number:1


  ASSESSMENT OF CANOPY COVER --------------------------------------
  No statistic analysis (insufficient data)
  ----------------------------------------------------------------


  ASSESSMENT OF BIOMASS PRODUCTION --------------------------------
              --------- Biomass (ton/ha) ---------
```

</details>

<details><summary>First lines of <code>case/OUTP/projectPRM2evaluation.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59
Evaluation of simulation results - Statistics
** Run number:2


  ASSESSMENT OF CANOPY COVER --------------------------------------
  No statistic analysis (insufficient data)
  ----------------------------------------------------------------


  ASSESSMENT OF BIOMASS PRODUCTION --------------------------------
              --------- Biomass (ton/ha) ---------
```

</details>

<details><summary>First lines of <code>case/OUTP/projectPRM3evaluation.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:26:00
Evaluation of simulation results - Statistics
** Run number:3


  ASSESSMENT OF CANOPY COVER --------------------------------------
  No statistic analysis (insufficient data)
  ----------------------------------------------------------------


  ASSESSMENT OF BIOMASS PRODUCTION --------------------------------
              --------- Biomass (ton/ha) ---------
```

</details>

<details><summary>First lines of <code>case/OUTP/projectPRMday.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59

   Run:   1
   Day Month  Year   DAP Stage   WC(3.05)   Rain     Irri   Surf   Infilt   RO    Drain       CR    Zgwt       Ex       E     E/Ex     Trx       Tr  Tr/Trx    ETx      ET  ET/ETx      GD       Z     S
                                      mm      mm       mm     mm     mm     mm       mm       mm      m        mm       mm     %        mm       mm    %        mm      mm       %  degC-day     m      
    21     5  2014     1     1     881.0     0.1      0.0    0.0    0.1    0.0      0.0      0.0   -9.90      3.9      3.2     82      0.4      0.4   100      4.3     3.6      84     11.4    0.30     
```

</details>

<details><summary>First lines of <code>case/OUTP/projectPRMharvests.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59
Biomass and Yield at Multiple cuttings

   Run:   1
    Nr   Day  Month Year   DAP Interval  Biomass    Sum(B)   Dry-Yield  Sum(Y) Fresh-Yield  Sum(Y)
                                 days     ton/ha    ton/ha    ton/ha    ton/ha    ton/ha    ton/ha
     0    21     5  2014                             0.000               0.000               0.000
     1    13     7  2014    54    54       4.792     4.792     4.633     4.633    23.167    23.167
     2    31     8  2014   103    49       3.074     7.865     3.074     7.707    15.368    38.535
  9999     1    11  2014                             9.171               9.012              45.062

   Run:   2
```

</details>

<details><summary>First lines of <code>case/OUTP/projectPRMseason.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59

    RunNr     Day1   Month1    Year1     Rain      ETo       GD     CO2      Irri   Infilt   Runoff    Drain   Upflow        E     E/Ex       Tr      TrW   Tr/Trx    SaltIn   SaltOut    SaltUp  SaltPr
                                           mm       mm  degC.day    ppm        mm       mm       mm       mm       mm       mm        %       mm       mm        %    ton/ha    ton/ha    ton/ha    ton/
   Tot(1)       21        5     2014    487.5    431.0   1802.6   398.82      0.0    477.7      9.8     35.3      0.0    166.1       85    276.2    276.2      100     0.000     0.000     0.000     0.0
   Tot(2)        1       11     2014    782.1    617.6   2118.6   401.02      0.0    768.9     13.2    194.5      0.0    288.7       89    348.3    348.3      100     0.000     0.000     0.000     0.0
   Tot(3)       25       10     2015    926.2    653.7   2213.1   404.41      0.0    901.2     25.0    311.8      0.0    296.8       81    351.6    351.6      100     0.000     0.000     0.000     0.0
```

</details>

<details><summary>First lines of <code>case/PARAM/Ottawa.PPn</code></summary>

```
      4         : Evaporation decline factor for stage II
      1.10      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface
      5         : Threshold for green CC below which HI can no longer increase (% cover)
     70         : Starting depth of root zone expansion curve (% of Zmin)
      5.00      : Maximum allowable root zone expansion (fixed at 5 cm/day)
     -6         : Shape factor for effect water stress on root zone expansion
     20         : Required soil water content in top soil for germination (% TAW)
      1.0       : Adjustment factor for FAO-adjustment soil water depletion (p) by ETo
      3         : Number of days after which deficient aeration is fully effective
      1.00      : Exponent of senescence factor adjusting drop in photosynthetic activity of dying crop
     12         : Decrease of p(sen) once early canopy senescence is triggered (% of p(sen))
     10         : Thickness top soil (cm) in which soil water depletion has to be determined
```

</details>

<details><summary>First lines of <code>case/PARAM/project.PPn</code></summary>

```
      4         : Evaporation decline factor for stage II
      1.10      : Ke(x) Soil evaporation coefficient for fully wet and non-shaded soil surface
      5         : Threshold for green CC below which HI can no longer increase (% cover)
     70         : Starting depth of root zone expansion curve (% of Zmin)
      5.00      : Maximum allowable root zone expansion (fixed at 5 cm/day)
     -6         : Shape factor for effect water stress on root zone expansion
     20         : Required soil water content in top soil for germination (% TAW)
      1.0       : Adjustment factor for FAO-adjustment soil water depletion (p) by ETo
      3         : Number of days after which deficient aeration is fully effective
      1.00      : Exponent of senescence factor adjusting drop in photosynthetic activity of dying crop
     12         : Decrease of p(sen) once early canopy senescence is triggered (% of p(sen))
     10         : Thickness top soil (cm) in which soil water depletion has to be determined
```

</details>

<details><summary>First lines of <code>case/README.md</code></summary>

```
# Testcase

This folder contains an AquaCrop testcase that you may use 
to verify the correct execution of the precompiled static AquaCrop 
executable on your hardware. Note that only x86_64 CPU architectures 
are supported. The reference output (./OUTP_REF) was generated with 
AquaCropV7.3.

## Running the testcase
To run the test, copy the executable to the present directory and
follow the instructions below for your operating system:

```

</details>

<details><summary>First lines of <code>case/SIMUL/AggregationResults.SIM</code></summary>

```
0 :  Time aggregation for intermediate results (0 = none ; 1 = daily; 2 = 10-daily; 3 = monthly)
```

</details>

<details><summary>First lines of <code>case/SIMUL/DEFAULT.CRO</code></summary>

```
a generic crop
     7.3       : AquaCrop Version (January 2026)
     1         : File not protected
     2         : fruit/grain producing crop
     1         : Crop is sown
     1         : Determination of crop cycle : by calendar days
     1         : Soil water depletion factors (p) are adjusted by ETo
     5.5       : Base temperature (degC) below which crop development does not progress
    30.0       : Upper temperature (degC) above which crop development no longer increases with an increase in temperature
    -9         : Total length of crop cycle in growing degree-days
     0.25      : Soil water depletion factor for canopy expansion (p-exp) - Upper threshold
     0.60      : Soil water depletion factor for canopy expansion (p-exp) - Lower threshold
```

</details>

<details><summary>First lines of <code>case/SIMUL/DEFAULT.SOL</code></summary>

```
deep loamy soil profile
        7.3                 : AquaCrop Version (January 2026)
       61                   : CN (Curve Number)
        9                   : Readily evaporable water from top layer (mm)
        1                   : number of soil horizons
       -9                   : variable no longer applicable
  Thickness  Sat   FC    WP     Ksat   Penetrability  Gravel  CRa       CRb           description
  ---(m)-   ----(vol %)-----  (mm/day)      (%)        (%)    -----------------------------------------
    4.00    50.0  30.0  10.0   500.0        100         0     -0.453600  0.837340   Loamy soil horizon
```

</details>

<details><summary>First lines of <code>case/SIMUL/DailyResults.SIM</code></summary>

```
 1 : Various parameters of the soil water balance
 2 : Crop development and production
 3 : Soil water content in the soil profile and root zone
 4 : Soil salinity in the soil profile and root zone
 5 : Soil water content at various depths of the soil profile
 6 : Soil salinity at various depths of the soil profile
 7 : Climate input parameters


```

</details>

<details><summary>First lines of <code>case/SIMUL/DailyResultsFullList.SIM</code></summary>

```
In the absence of the 'DailyResults.SIM' file in the 'SIMUL' subdirectory, no daily results will be provided.
IF daily output is required, copy one or more of the lines below in a text file 'DailyResults.SIM'.
(note that recording all daily outputs, might slow donw significantly the speed of the Plug-In program)

 1 : Various parameters of the soil water balance
 2 : Crop development and production
 3 : Soil water content in the soil profile and root zone
 4 : Soil salinity in the soil profile and root zone
 5 : Soil water content at various depths of the soil profile
 6 : Soil salinity at various depths of the soil profile
 7 : Climate input parameters
 8 : Irrigation events and intervals
```

</details>

<details><summary>First lines of <code>case/SIMUL/EToData.SIM</code></summary>

```
    0.7000
    0.7000
    0.7000
    0.5000
    0.7000
    0.6000
    0.5000
    0.6000
    0.6000
    0.6000
    0.6000
    0.6000
```

</details>

<details><summary>First lines of <code>case/SIMUL/MaunaLoa.CO2</code></summary>

```
Default atmospheric CO2 concentration from 1902 to 2099 (updated 01/01/2026)
Year     CO2 (ppm by volume)
============================
  1902  297.4
  1905  298.2
  1912  300.7
  1915  301.3
  1924  304.5
  1926  305.0
  1929  305.2
  1932  307.8
  1934  309.2
```

</details>

<details><summary>First lines of <code>case/SIMUL/OttawaReference.Tnx</code></summary>

```
Reference : Ottawa, Canada
     3  : Monthly records (1=daily, 2=10-daily and 3=monthly data)
     1  : First day of record (1, 11 or 21 for 10-day or 1 for months)
     1  : First month of record
  1901  : First year of record (1901 if not linked to a specific year)

  Tmin (C)   TMax (C) 
  =======================
    -18.74     -7.73
    -19.40     -8.05
    -12.18     -1.32
     -2.14     10.01
```

</details>

<details><summary>First lines of <code>case/SIMUL/ParticularResults.SIM</code></summary>

```
 1 : Biomass and Yield at Multiple cuttings (for herbaceous forage crops)
 2 : Evaluation of simulation results (when Field Data)

```

</details>

<details><summary>First lines of <code>case/SIMUL/ParticularResultsFullList.SIM</code></summary>

```
In the absence of the 'ParticularResults.SIM' file in the 'SIMUL' subdirectory, no (1) simulated biomass and yield at mutliple cuttings of herbaceous forage crops during the season, or (2) Evaluation 
IF this type of output is required, copy one or more of the lines below in a text file 'ParticularResults.SIM'.
(note that recording all particular outputs, might slow donw significantly the speed of the Plug-In program)

 1 : Biomass and Yield at Multiple cuttings (for herbaceous forage crops)
 2 : Evaluation of simulation results (when Field Data)

```

</details>

<details><summary>First lines of <code>case/SIMUL/RainData.SIM</code></summary>

```
    6.1000
    0.0000
    0.0000
   22.2000
    7.5000
    0.5000
    0.2000
    5.5000
    1.3000
    0.2000
    0.1000
    0.1000
```

</details>

<details><summary>First lines of <code>case/SIMUL/TCrop.SIM</code></summary>

```
    7.0000   19.8000
   -1.7000    9.4000
   -2.4000   10.0000
   -1.7000   17.1000
    1.5000   21.1000
    6.6000   24.0000
    9.6000   21.0000
    6.4000   15.5000
    1.4000    9.0000
   -0.1000    9.6000
   -1.4000   13.3000
    0.6000   17.6000
```

</details>

<details><summary>First lines of <code>case/SIMUL/TCropReference.SIM</code></summary>

```
      5.00     17.84
      5.26     18.11
      5.53     18.37
      5.79     18.63
      6.04     18.88
      6.29     19.12
      6.53     19.36
      6.77     19.59
      7.01     19.81
      7.24     20.02
      7.46     20.23
      7.68     20.43
```

</details>

<details><summary>First lines of <code>case/SIMUL/TempData.SIM</code></summary>

```
    0.5000   10.3000
   -2.7000    7.9000
   -1.0000   11.8000
    2.4000   10.8000
    5.8000   13.1000
   -1.4000    7.2000
   -3.6000    5.8000
    2.7000   13.4000
    5.2000   12.4000
    3.7000   15.5000
    3.8000   15.1000
    5.9000   18.5000
```

</details>

<details><summary>First lines of <code>case/SIMUL/TnxReference365Days.SIM</code></summary>

```
    -15.27     -5.36
    -15.61     -5.60
    -15.94     -5.82
    -16.26     -6.04
    -16.57     -6.26
    -16.87     -6.46
    -17.16     -6.66
    -17.43     -6.85
    -17.70     -7.03
    -17.95     -7.20
    -18.20     -7.37
    -18.43     -7.53
```

</details>

<details><summary>First lines of <code>projectPRM1evaluation.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59
Evaluation of simulation results - Statistics
** Run number:1


  ASSESSMENT OF CANOPY COVER --------------------------------------
  No statistic analysis (insufficient data)
  ----------------------------------------------------------------


  ASSESSMENT OF BIOMASS PRODUCTION --------------------------------
              --------- Biomass (ton/ha) ---------
```

</details>

<details><summary>First lines of <code>projectPRM2evaluation.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59
Evaluation of simulation results - Statistics
** Run number:2


  ASSESSMENT OF CANOPY COVER --------------------------------------
  No statistic analysis (insufficient data)
  ----------------------------------------------------------------


  ASSESSMENT OF BIOMASS PRODUCTION --------------------------------
              --------- Biomass (ton/ha) ---------
```

</details>

<details><summary>First lines of <code>projectPRM3evaluation.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:26:00
Evaluation of simulation results - Statistics
** Run number:3


  ASSESSMENT OF CANOPY COVER --------------------------------------
  No statistic analysis (insufficient data)
  ----------------------------------------------------------------


  ASSESSMENT OF BIOMASS PRODUCTION --------------------------------
              --------- Biomass (ton/ha) ---------
```

</details>

<details><summary>First lines of <code>projectPRMday.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59

   Run:   1
   Day Month  Year   DAP Stage   WC(3.05)   Rain     Irri   Surf   Infilt   RO    Drain       CR    Zgwt       Ex       E     E/Ex     Trx       Tr  Tr/Trx    ETx      ET  ET/ETx      GD       Z     S
                                      mm      mm       mm     mm     mm     mm       mm       mm      m        mm       mm     %        mm       mm    %        mm      mm       %  degC-day     m      
    21     5  2014     1     1     881.0     0.1      0.0    0.0    0.1    0.0      0.0      0.0   -9.90      3.9      3.2     82      0.4      0.4   100      4.3     3.6      84     11.4    0.30     
```

</details>

<details><summary>First lines of <code>projectPRMharvests.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59
Biomass and Yield at Multiple cuttings

   Run:   1
    Nr   Day  Month Year   DAP Interval  Biomass    Sum(B)   Dry-Yield  Sum(Y) Fresh-Yield  Sum(Y)
                                 days     ton/ha    ton/ha    ton/ha    ton/ha    ton/ha    ton/ha
     0    21     5  2014                             0.000               0.000               0.000
     1    13     7  2014    54    54       4.792     4.792     4.633     4.633    23.167    23.167
     2    31     8  2014   103    49       3.074     7.865     3.074     7.707    15.368    38.535
  9999     1    11  2014                             9.171               9.012              45.062

   Run:   2
```

</details>

<details><summary>First lines of <code>projectPRMseason.OUT</code></summary>

```
AquaCrop 7.3 (January 2026) - Output created on (date) : 18-10-2026   at (time) : 13:25:59

    RunNr     Day1   Month1    Year1     Rain      ETo       GD     CO2      Irri   Infilt   Runoff    Drain   Upflow        E     E/Ex       Tr      TrW   Tr/Trx    SaltIn   SaltOut    SaltUp  SaltPr
                                           mm       mm  degC.day    ppm        mm       mm       mm       mm       mm       mm        %       mm       mm        %    ton/ha    ton/ha    ton/ha    ton/
   Tot(1)       21        5     2014    487.5    431.0   1802.6   398.82      0.0    477.7      9.8     35.3      0.0    166.1       85    276.2    276.2      100     0.000     0.000     0.000     0.0
   Tot(2)        1       11     2014    782.1    617.6   2118.6   401.02      0.0    768.9     13.2    194.5      0.0    288.7       89    348.3    348.3      100     0.000     0.000     0.000     0.0
   Tot(3)       25       10     2015    926.2    653.7   2213.1   404.41      0.0    901.2     25.0    311.8      0.0    296.8       81    351.6    351.6      100     0.000     0.000     0.000     0.0
```

</details>


## Reading the output

The recipe's wrapper script copies the bundled Ottawa data into `case/`, installs the uploaded file as the only project, runs `aquacrop`, and copies the `.OUT` files up. For the project `project.PRM`, the file names start with `projectPRM`. These are the files, with column names from the repository's reference output in `testcase/OUTP_REF/`:

- `projectPRMseason.OUT` has one `Tot(n)` line per season. Columns include start date, rain, ETo, growing degree days, CO2, irrigation, runoff, drainage, evaporation, transpiration, biomass, harvest index, dry and fresh yield, water productivity and the end date. In the reference output, season 1 (21 May to 31 October 2014) shows rain of 487.5 mm, ETo of 431.0 mm, biomass of 9.258 ton/ha and dry yield of 9.109 ton/ha.
- `projectPRMday.OUT` has one row per day with the water balance (rain, infiltration, runoff, drainage, evaporation, transpiration, ET), stress percentages and canopy cover. It is the largest file (about 800 kB in the reference output).
- `projectPRMharvests.OUT` lists each cutting with its date, days after planting, interval, biomass and yield. The reference output has two cuttings in 2014, on 13 July and 31 August.
- `projectPRM1evaluation.OUT` and the files for later runs hold fit statistics against the field observations in `OBS/Ottawa.OBS`.
- `ListProjectsLoaded.OUT` says which projects loaded and which output options were on. `AllDone.OUT` holds the text "All done".

The numbers above come from the reference output in the repository, not from a run of this recipe.

## Pitfalls

- **Paths are relative to the working directory.** AquaCrop looks for `LIST/`, `DATA/` and `OUTP/` next to where you start it, and the project file lists data folders such as `./DATA/`.
- **The project name drives two file names.** The parameter file for `X.PRM` is `PARAM/X.PPn`, and output names start with `XPRM`. The recipe copies the Ottawa parameters to match.
- **The recipe takes a project file only.** Climate, soil and crop come from the bundled Ottawa set. Your own data needs the full folder layout on your machine.
- **Dates are day numbers.** The project file gives dates as serial day numbers (for example 41414 for 21 May 2014).
- **Windows line endings.** The testcase README says the files are set up for Linux and macOS. On Windows they need converting, and the forward slashes in the project file become back slashes.

## Further reading

- Repository and README: https://github.com/KUL-RSDA/AquaCrop
- Project documentation: https://ees.kuleuven.be/en/aquacrop and https://www.fao.org/aquacrop/en/
- Releases: https://github.com/KUL-RSDA/AquaCrop/releases
- Paper: Raes D, Steduto P, Hsiao TC, Fereres E (2009). AquaCrop - the FAO crop model to simulate yield response to water: II. Main algorithms and software description. Agronomy Journal 101:438-447. https://doi.org/10.2134/agronj2008.0140s

---

Cite: Raes D, Steduto P, Hsiao TC, Fereres E (2009). AquaCrop - the FAO crop model to simulate yield response to water: II. Main algorithms and software description. Agron J 101:438-447. doi:10.2134/agronj2008.0140s

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/aquacrop).
