# PCSE (Python Crop Simulation Environment)

> Simulate daily crop growth, phenology and nitrogen uptake of spring wheat with the LINTUL3 model in PCSE, driven by a weather file and a nitrogen schedule.

Licence: EUPL-1.1 · [Source code](https://github.com/ajwdewit/pcse)

## What it simulates

PCSE is a Python framework for crop simulation models developed in Wageningen. It ships the WOFOST models (versions 7.2, 7.3 and 8.1, as potential production, water-limited and nitrogen-limited variants), the LINTUL3 crop model, the LINGRA grassland model and a few others. Each model advances in daily steps. It reads daily weather, crop and soil parameters and farm management, and it returns state variables such as development stage, leaf area index, biomass and soil water.

PCSE separates parameters, rate variables and state variables. At each day it computes the rates, then integrates the states. Inputs and outputs live outside the models, so you can read from files, databases or web services and write to anything pandas can export.

The recipe runs LINTUL3 on spring wheat, using the example data that ships inside the package. The crop file there sets LUE (light-use efficiency) to 2.18, a temperature sum of 800 degree-days from emergence to anthesis and 1030 degree-days from anthesis to maturity.

## When to use it

Use PCSE to run WOFOST or LINTUL for a field or grid cell, to test a change to one process module, or to script many seasons from Python.

- Use [AquaCrop-OSPy](aquacrop-ospy.md) when you want a water-driven model that needs only a few crop parameters.
- Use [DSSAT-CSM](dssat-csm.md) when you need cultivar coefficients for a specific crop and detailed soil organic matter dynamics.
- Use [APSIM Next Generation](apsim-next-generation.md) when you need rotations, grazing or a graphical model editor.

## Install

```
pip install pcse==6.0.13
```

PyPI lists pcse 6.0.13 as the current release. It is a pure-Python wheel of about 0.9 MB for Python 3.9 or later. The dependencies are pydispatcher, PyYAML, openpyxl, requests, pandas, dotmap and the modified `traitlets-pcse==5.0.0.dev`. The package is licensed EUPL-1.1.

The first `import pcse` creates a `.pcse` folder in your home directory and a user settings file there. The install documentation also describes a conda route that starts from Miniconda.

## A first run

Adapted from the [PCSE getting-started page](https://pcse.readthedocs.io/en/stable/quickstart.html) and the LINTUL3 test that ships in the wheel (`pcse/tests/test_lintul3.py`). The page builds a run from five parts: crop, soil and site parameters, management in YAML, and a weather provider. The sketch below uses the files from the wheel and a Wageningen 1997 weather file in CABO format.

```python
import os, yaml, pcse
from pcse.engine import Engine
from pcse.base import ParameterProvider
from pcse.input import PCSEFileReader, CABOWeatherDataProvider

data = os.path.join(os.path.dirname(pcse.__file__), "tests", "test_data")
agro = yaml.safe_load(open(os.path.join(data, "lintul3_springwheat.agro")))["AgroManagement"]
soil = PCSEFileReader(os.path.join(data, "lintul3_springwheat.soil"))
site = PCSEFileReader(os.path.join(data, "lintul3_springwheat.site"))
crop = PCSEFileReader(os.path.join(data, "lintul3_springwheat.crop"))
weather = CABOWeatherDataProvider("NL1", data, ETmodel="P")

model = Engine(ParameterProvider(sitedata=site, soildata=soil, cropdata=crop),
               weather, agromanagement=agro, config="Lintul3.conf")
model.run_till_terminate()
output = model.get_output()
```

## Run the tested example

This recipe builds PCSE (Python Crop Simulation Environment) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.9 s.

1. Download [pcse-recipe.tar.gz](https://biosimhub.pages.dev/guides/pcse/pcse-recipe.tar.gz) (Dockerfile, run_pcse.py, example weather.997, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pcse-recipe.tar.gz
   cd pcse
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pcse:6.0.13 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pcse:6.0.13 python /opt/run_pcse.py --weather /work/in/weather.997 \
    --n1 10 --n2 5 --recovery 0.7 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `daily.csv` | 43.1 KB |
| `run_log.txt` | 172 B |

<details><summary>First lines of <code>daily.csv</code></summary>

```
day,DVS,TGROWTH,LAI,NUPTT,TRAN,TIRRIG,TNSOIL,TRAIN,TRANRF,TRUNOF,TAGBM,TTRAN,WC,WLVD,WLVG,WRT,WSO,WST
1997-01-01,,,,,,0.0,,0.0,,0.0,,0.0,0.0,,,,,
1997-01-02,,,,,,0.0,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-03,,,,,,0.0,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-04,,,,,,0.03731987891279966,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-05,,,,,,0.14982391426812997,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-06,,,,,,0.1616826507153597,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-07,,,,,,0.1616826507153597,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-08,,,,,,0.1616826507153597,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-09,,,,,,0.1616826507153597,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-10,,,,,,0.16380353781662182,,0.0,,0.0,,0.0,0.4,,,,,
1997-01-11,,,,,,0.19480777007874517,,0.0,,0.0,,0.0,0.4,,,,,
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Building PCSE demo database at: /tmp/.pcse/pcse.db ... OK
pcse=6.0.13 model=Lintul3 days=225 n1=10.0 n2=5.0
last day 1997-08-13: DVS=2.000 LAI=0.595 TAGBM=1627.3 WSO=812.9
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--n1` | First nitrogen application | 10 | 0 to 50 |
| `--n2` | Second nitrogen application | 5 | 0 to 50 |
| `--recovery` | Fraction of applied nitrogen the crop can take up | 0.7 | 0 to 1 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`get_output()` returns a list with one dictionary per day. The keys are the variables named in the configuration file `Lintul3.conf`: DVS, TGROWTH, LAI, NUPTT, TRAN, TIRRIG, TNSOIL, TRAIN, TRANRF, TRUNOF, TAGBM, TTRAN, WC, WLVD, WLVG, WRT, WSO and WST. The recipe writes them to `daily.csv` with a `day` column, and it prints the last row in `run_log.txt`.

- **DVS** is the development stage. In the Wageningen models 0 is emergence, 1 is anthesis and 2 is maturity.
- **LAI** is the leaf area index.
- **WLVG, WLVD, WST, WRT, WSO** are green leaf, dead leaf, stem, root and storage-organ (grain) weights. **TAGBM** is total above-ground biomass.
- **NUPTT** is cumulative nitrogen uptake and **TNSOIL** is soil mineral nitrogen.
- **TRANRF** is the transpiration reduction factor. A value of 1 means no water stress.
- **TRAIN**, **TIRRIG**, **TRUNOF** and **TTRAN** are cumulative rain, irrigation, runoff and transpiration.

The agromanagement file applies nitrogen on 10 April (10 g N per square metre) and 5 May (5), each with a recovery fraction of 0.7. The recipe lets you change those amounts. More nitrogen should raise NUPTT and, until another limit binds, WSO.

## Pitfalls

- **Weather files are matched by name.** `CABOWeatherDataProvider("NL1", dir)` loads every file named `NL1.yyy`, where the last three digits give the year. The recipe accepts only the 1997 file, because the management file starts on 1 January 1997.
- **WOFOST crop parameters download on first use.** `YAMLCropDataProvider` pulls YAML files from the `WOFOST_crop_parameters` GitHub repository unless you pass `fpath`. A machine without network needs a local copy.
- **NASA POWER weather needs network access.** `NASAPowerWeatherDataProvider` calls the NASA POWER web service, and the getting-started page notes that the first call can take around 30 seconds.
- **The demo shortcut needs a database file.** `pcse.start_wofost()` reads `pcse.db` from the user's `.pcse` folder. The SQL dump of that demo database ships in `pcse/tests/test_data/pcse_dump.sql`.
- **Pick the model that matches the data you have.** Water-limited and nitrogen-limited configurations need soil and site parameters the potential-production ones do not.
- **Configuration names are file names.** `config="Lintul3.conf"` selects a file from `pcse/conf`. A typo fails at load time.

## Further reading

- Documentation: https://pcse.readthedocs.io/
- Notebooks: https://github.com/ajwdewit/pcse_notebooks
- Source: https://github.com/ajwdewit/pcse
- PyPI: https://pypi.org/project/pcse/
- Paper: de Wit A, Boogaard H, Fumagalli D, et al. (2019). 25 years of the WOFOST cropping systems model. Agricultural Systems 168:154-167. https://doi.org/10.1016/j.agsy.2018.06.018

---

Cite: de Wit A, Boogaard H, Fumagalli D, et al. (2019). 25 years of the WOFOST cropping systems model. Agricultural Systems 168:154-167. doi:10.1016/j.agsy.2018.06.018

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pcse).
