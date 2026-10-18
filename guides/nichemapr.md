# NicheMapR

> Compute hourly microclimate for a site on land, then the body temperature and activity hours of a lizard-like ectotherm living in it.

Licence: GPL-3.0 · [Source code](https://github.com/mrke/NicheMapR)

## What it simulates

NicheMapR is an R package that computes the physical environment an animal lives in, then the animal's heat and water budget inside it. It has two linked parts.

- **The microclimate model** turns monthly climate averages for a site into hourly air temperature, humidity, wind, solar radiation and soil temperature at 10 depths, with and without shade. It solves the heat balance of the ground surface and soil column.
- **The ectotherm model** takes those hourly conditions and a body description (mass, shape, solar absorptivity, preferred and critical temperatures). It solves the body's heat balance each hour. The animal basks, forages, moves into shade or retreats down a burrow, and the model records its body temperature and activity.

The assumptions are one representative day per month (12 days, 24 hours each), a single animal, and no population dynamics. The climate comes from the 10-minute-resolution global monthly climatology (1961-1990) that ships with NicheMapR.

## When to use it

Use NicheMapR to ask how much of the day an ectotherm can be active at a site, how that changes with shade, body size or climate, and when it must shelter from cold or heat. Typical uses are lizard activity windows, species range limits and warming scenarios.

- It computes physiology for one individual in a given habitat. For allele or genotype change in a population, use [SLiM](slim.md) or [msprime](msprime.md).
- It needs a land location. For cells with no climate data (open ocean) the package substitutes dummy values.

## Install it yourself

NicheMapR is not on conda-forge or CRAN. It installs from GitHub, and its Fortran code needs a compiler:

```r
install.packages("remotes")
remotes::install_github("mrke/NicheMapR")
library(NicheMapR)
get.global.climate(folder = "~/globalclimate")   # one-off download, about 0.5 GB unpacked
```

The recipe's image builds version 3.3.3 from a pinned commit and stores the climate data as a 53 MB compressed NetCDF, so the container needs no download. The image is 1.38 GB. The minimal script below gives the example's default result:

```r
library(NicheMapR)
micro <- micro_global(loc = c(146.77, -19.29))   # Townsville, Australia
ecto <- ectotherm()                               # a 40 g lizard
e <- as.data.frame(ecto$environ)
sum(e$ACT == 2)                                   # foraging hours in the 12 days
```

In the image this printed 131 foraging hours and body temperatures from 13.3 to 37.1 C.

## Run the tested example

This recipe builds NicheMapR in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 2.5 s.

1. Download [nichemapr-recipe.tar.gz](https://biosimhub.pages.dev/guides/nichemapr/nichemapr-recipe.tar.gz) (Dockerfile, run_nichemapr.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf nichemapr-recipe.tar.gz
   cd nichemapr
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/nichemapr:3.3.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/nichemapr:3.3.3 Rscript /opt/run_nichemapr.R --lon 146.77 \
    --lat -19.29 --minshade 0 --maxshade 90 --mass 40 \
    --shape 3 --alpha 0.85 --tfmin 24 --tfmax 34 \
    --tpref 30 --ctmax 40 --burrow 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `ectotherm.csv` | 8.4 KB |
| `microclimate.csv` | 28.6 KB |
| `run_log.txt` | 101 B |
| `summary.csv` | 621 B |

<details><summary>First lines of <code>ectotherm.csv</code></summary>

```
"month","hour","body_temp_c","activity","shade_pct","depth_node"
1,0,29.8522146973352,0,0,-2.5
1,1,28.9298534705246,0,0,-2.5
1,2,28.1741615235161,0,0,-2.5
1,3,27.5516971378765,0,0,-2.5
1,4,27.0350708652352,0,0,-2.5
1,5,26.606142573199,0,0,-2.5
1,6,28.1366870514989,2,0,0
1,7,29.7721859970471,2,36,0
1,8,29.8214722653149,2,60,0
1,9,29.9225579078425,2,75,0
1,10,29.8554379771667,2,87,0
```

</details>

<details><summary>First lines of <code>microclimate.csv</code></summary>

```
"month","hour","air_c","soil_surface_c","soil_10cm_c","rh_pct","wind_ms","solar_wm2"
1,0,25.1565124411079,26.0217648302632,32.7838181231495,64.9723722920631,0.257140339827472,0
1,1,24.9270697905333,25.5834951531422,31.9807279830436,68.0536708707649,0.208670121281348,0
1,2,24.7491167059876,25.2427071338368,31.259647903045,71.0508715050331,0.160199902735224,0
1,3,24.603557664714,24.9614899696886,30.6157427531892,74.0102602509018,0.111729684189101,0
1,4,24.498627065568,24.7313112249373,30.0423817248854,76.8681557727726,0.0493241924003397,0
1,5,24.366623544352,24.5178213507038,29.5325670804588,80.6585688550223,0.0338305075421418,0.0411261224923811
1,6,24.6219215995008,25.1123433706331,29.0803997957837,79.7550932157694,0.101815321054037,36.5661552448859
1,7,26.3009116032558,28.1428934312034,28.7029343518719,72.149979792487,0.16626799772618,177.121992599901
1,8,28.9682505146123,33.2434649164503,28.5682975663115,62.119490763022,0.230506304488212,329.507846311977
1,9,31.8513465229594,38.6600892899413,28.8572412869764,53.5834110181949,0.291881113463966,467.109201362688
1,10,34.5408184851894,43.5722398531402,29.6422984165345,46.7048697233624,0.350927122152227,574.928227558886
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: site 146.77,-19.29, 288 hours simulated, foraging 131 h, basking 5 h, body temp 13.3 to 37.1 C
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
"month","mean_air_c","min_air_c","max_air_c","mean_body_c","min_body_c","max_body_c","forage_hours","bask_hours"
1,29.67,24.37,38.35,30.48,26.61,36.24,13,0
2,29.19,24.31,37.36,30.26,26.47,37.13,13,0
3,28.05,23.04,36.53,29.41,23.27,36.36,12,1
4,25.5,20.38,34.74,27.94,22.09,35.03,11,0
5,22.54,17.37,32.02,25.53,18.83,30.71,10,1
6,19.16,13.27,29.76,21.88,14.44,29.9,7,1
7,18.37,12.06,29.65,21.19,13.28,29.98,7,1
8,20.08,13.46,31.63,23.12,14.79,29.99,9,0
9,22.83,16.09,34.48,25.86,17.64,33.74,11,0
10,26.1,19.42,37.04,27.52,21.21,34.25,12,1
11,28.47,22.27,38.49,29.37,24.35,37,13,0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--lon` | Longitude (degrees east) | 146.77 | -180 to 180 |
| `--lat` | Latitude (degrees north) | -19.29 | -60 to 80 |
| `--minshade` | Minimum shade (%) | 0 | 0 to 100 |
| `--maxshade` | Maximum shade (%) | 90 | 1 to 100 |
| `--mass` | Animal wet mass (g) | 40 | 1 to 5000 |
| `--shape` | Body shape (0 plate, 1 cylinder, 2 ellipsoid, 3 lizard, 4 frog) | 3 | 0, 1, 2, 3, 4 |
| `--alpha` | Solar absorptivity | 0.85 | 0.1 to 1 |
| `--tfmin` | Minimum foraging body temperature (C) | 24 | 5 to 40 |
| `--tfmax` | Maximum foraging body temperature (C) | 34 | 10 to 45 |
| `--tpref` | Preferred body temperature (C) | 30 | 10 to 45 |
| `--ctmax` | Critical thermal maximum (C) | 40 | 20 to 50 |
| `--burrow` | Can shelter in a burrow | 1 | 0, 1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_nichemapr.R` runs `micro_global` and `ectotherm`, then writes four files. The run took 2.5 s.

- `run_log.txt` (101 bytes) has one line: "done: site 146.77,-19.29, 288 hours simulated, foraging 131 h, basking 5 h, body temp 13.3 to 37.1 C". The 288 hours are 12 days of 24 hours, so "131 h" is the sum over the 12 representative days.
- `microclimate.csv` (29,273 bytes) has one row per hour with air temperature at the animal's height, soil surface and 10 cm temperatures, relative humidity, wind speed and solar radiation.
- `ectotherm.csv` (8,610 bytes) has the body temperature, an activity code (0 inactive, 1 basking, 2 foraging), the shade chosen in percent and the depth in cm (negative values are below ground).
- `summary.csv` (621 bytes) has one row per month.

The summary follows the Townsville seasons. January has a mean air temperature of 29.67 C (24.37 to 38.35 C) and 13 foraging hours. July has a mean of 18.37 C (12.06 to 29.65 C) and 7 foraging hours.

The hourly file shows how the model schedules a July day. The lizard sits at 2.5 cm depth overnight and its body cools to 13.3 C at 07:00. It emerges at 10:00 and holds a body temperature of 29.6 to 30.0 C from 10:00 to 15:00 by moving between 12 and 51 percent shade (the preferred temperature is 30 C). Body temperature is 28.2 C at 16:00, the animal basks at 17:00 (21.7 C) and it is underground again at 18:00. The tight band around 30 C is the signal that the animal is thermoregulating, not following air temperature.

## Your own runs

Each run changes one thing from the example and ran in the recipe's image in about 2.5 s.

- **A cold site.** `--lon -89.4557 --lat 43.1379` (Madison, Wisconsin) gave 46 foraging hours in the 12 days against 131, and body temperatures from 6.1 to 30.5 C. From November to March the animal never forages. Its body temperature sits at 7.34 C, the soil temperature of the deepest retreat node. July has 13 foraging hours.
- **Less shade.** `--maxshade 10` gave 78 foraging hours against 131 and a maximum body temperature of 37.4 C. January dropped from 13 to 5 foraging hours. With little shade the animal exceeds its 34 C foraging ceiling for much of the day and retreats.
- **A smaller animal.** `--mass 5` gave 129 foraging hours and 7 basking hours. The total changed by only 2 hours at this site, so body mass matters little for activity time here.

## Pitfalls

- **Hours are for 12 representative days.** Multiply a monthly value by the days in the month for a monthly total. The model does not simulate weather variation within a month.
- **Minimum shade must be below maximum shade.** The recipe rejects equal or reversed values with a clear message, and the R function stops with an error for the same reason.
- **Body temperature in a burrow is the soil temperature.** The constant 7.34 C at Madison is a soil value, not a thermoregulated one. Check `depth_node` before reading a flat line as a preference.
- **The climate is a 1961-1990 average.** It is a baseline, and it has no extremes beyond the monthly diurnal range.
- **Parameter changes interact.** In the recipe, `--tfmin` also sets the basking and retreat-exit temperatures, which are 6.5 C lower (17.5 C at the default 24 C).

## Further reading

- Source and install instructions: https://github.com/mrke/NicheMapR
- Package tutorials: https://mrke.github.io/NicheMapR/inst/doc/index.html
- Kearney MR, Porter WP (2017). NicheMapR: an R package for biophysical modelling: the microclimate model. Ecography 40:664-674. https://doi.org/10.1111/ecog.02360
- Kearney MR, Porter WP (2020). NicheMapR: an R package for biophysical modelling: the ectotherm and Dynamic Energy Budget models. Ecography 43:85-96. https://doi.org/10.1111/ecog.04680

---

Cite: Kearney MR, Porter WP (2017). NicheMapR: an R package for biophysical modelling: the microclimate model. Ecography 40:664-674. doi:10.1111/ecog.02360; Kearney MR, Porter WP (2020). NicheMapR: an R package for biophysical modelling: the ectotherm and Dynamic Energy Budget models. Ecography 43:85-96. doi:10.1111/ecog.04680

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/nichemapr).
