# simglucose

> Type 1 diabetes glucose-insulin simulator (UVA/Padova model) with 30 virtual patients, a CGM sensor, an insulin pump and a basal-bolus controller.

Licence: MIT · [Source code](https://github.com/jxx123/simglucose)

## What it simulates

simglucose is a Python implementation of the 2008 version of the UVA/Padova type 1 diabetes simulator, which the README calls FDA-approved. It models the glucose-insulin system of a virtual patient, with meals, subcutaneous insulin delivery and a continuous glucose monitor (CGM). It ships with 30 virtual patients: 10 adolescents, 10 adults and 10 children.

A simulation links four parts: the patient model, a CGM sensor (Dexcom, GuardianRT or Navigator), an insulin pump (Cozmo or Insulet), and a meal scenario, either random or a list of (time, carbohydrate) pairs. A controller reads the sensor and returns basal and bolus insulin. The package supplies a basal-bolus controller, and you can write your own. The same system is also exposed as a Gym and Gymnasium environment for reinforcement learning, where the default reward at each step is the drop in a risk index.

## When to use it

Use simglucose to test an insulin-dosing controller (PID, model predictive, reinforcement learning) against virtual patients, or to see how meals and sensor noise move blood glucose over days. It is a research tool and says so itself.

Alternatives:

- [COPASI](copasi.md) solves ODE models that you write yourself, including glucose-insulin models.
- [XPPAUT](xppaut.md) explores ODE systems with phase planes and bifurcation analysis.
- [openCARP](opencarp.md) simulates cardiac electrophysiology, another physiological system.

## Install

simglucose 0.2.11 is on PyPI (checked on the PyPI JSON API) as a pure Python wheel. The README asks for Python 3.9 or newer and installs with pip:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install simglucose==0.2.11
python -c "import simglucose; print(simglucose.__file__)"
```

The wheel pins `gym==0.9.4` and `gymnasium~=0.29.1`, and needs `numpy`, `scipy`, `pandas`, `matplotlib` and `pathos`. The licence is MIT. The recipe installs the package in a Python 3.10 image with no display. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## A first run

Adapted from the "Advanced Usage" section of the [README](https://github.com/jxx123/simglucose). It builds the parts, runs one simulated day with the basal-bolus controller and prints the result table:

```python
from datetime import datetime, timedelta
from simglucose.simulation.env import T1DSimEnv
from simglucose.controller.basal_bolus_ctrller import BBController
from simglucose.sensor.cgm import CGMSensor
from simglucose.actuator.pump import InsulinPump
from simglucose.patient.t1dpatient import T1DPatient
from simglucose.simulation.scenario_gen import RandomScenario
from simglucose.simulation.sim_engine import SimObj, sim

start_time = datetime(2018, 1, 1)
patient = T1DPatient.withName("adolescent#001")
sensor = CGMSensor.withName("Dexcom", seed=1)
pump = InsulinPump.withName("Insulet")
scenario = RandomScenario(start_time=start_time, seed=1)
env = T1DSimEnv(patient, sensor, pump, scenario)
results = sim(SimObj(env, BBController(), timedelta(days=1), animate=False, path="."))
print(results)
```

`sim` also writes `<patient name>.csv` into `path`. The recipe fixes the start time and the seed, so one seed gives one run. Its other choice for meals is the README's custom list: 45 g at 7:00, 70 g at 12:00, 15 g at 16:00, 80 g at 18:00 and 10 g at 23:00.

## Run the tested example

This recipe builds simglucose in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 4.6 s.

1. Download [simglucose-recipe.tar.gz](https://biosimhub.pages.dev/guides/simglucose/simglucose-recipe.tar.gz) (Dockerfile, run_simglucose.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf simglucose-recipe.tar.gz
   cd simglucose
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/simglucose:0.2.11 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/simglucose:0.2.11 python /opt/run_simglucose.py --patient 'adolescent#001' \
    --days 1 --sensor Dexcom --pump Insulet --meals random \
    --seed 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `adolescent#001.csv` | 58.3 KB |
| `results.csv` | 58.3 KB |
| `run_log.txt` | 302 B |

<details><summary>First lines of <code>adolescent#001.csv</code></summary>

```
Time,BG,CGM,CHO,insulin,LBGI,HBGI,Risk
2018-01-01 00:00:00,149.02,165.7939493687905,0.0,0.013933333333333336,0.0,2.7552758979034984,2.7552758979034984
2018-01-01 00:03:00,149.01999999999933,161.58202232204695,0.0,0.013933333333333336,0.0,2.7552758979034135,2.7552758979034135
2018-01-01 00:06:00,149.0200000002988,159.23937324662245,0.0,0.013933333333333336,0.0,2.755275897942923,2.755275897942923
2018-01-01 00:09:00,149.02000000371407,157.47270951030134,0.0,0.013933333333333336,0.0,2.755275898393481,2.755275898393481
2018-01-01 00:12:00,149.02000002022487,156.10895023557381,0.0,0.013933333333333336,0.0,2.755275900571683,2.755275900571683
2018-01-01 00:15:00,149.02000007188917,154.97501455537628,0.0,0.013933333333333336,0.0,2.75527590738754,2.75527590738754
2018-01-01 00:18:00,149.02000019652166,153.89782161722897,0.0,0.013933333333333336,0.0,2.755275923829774,2.755275923829774
2018-01-01 00:21:00,149.0200004498227,152.70429058588806,0.0,0.013933333333333336,0.0,2.7552759572467305,2.7552759572467305
2018-01-01 00:24:00,149.02000090609062,151.22134064452328,0.0,0.013933333333333336,0.0,2.7552760174402433,2.7552760174402433
2018-01-01 00:27:00,149.02000165778895,149.3112895614478,0.0,0.
```

</details>

<details><summary>First lines of <code>results.csv</code></summary>

```
Time,BG,CGM,CHO,insulin,LBGI,HBGI,Risk
2018-01-01 00:00:00,149.02,165.7939493687905,0.0,0.013933333333333336,0.0,2.7552758979034984,2.7552758979034984
2018-01-01 00:03:00,149.01999999999933,161.58202232204695,0.0,0.013933333333333336,0.0,2.7552758979034135,2.7552758979034135
2018-01-01 00:06:00,149.0200000002988,159.23937324662245,0.0,0.013933333333333336,0.0,2.755275897942923,2.755275897942923
2018-01-01 00:09:00,149.02000000371407,157.47270951030134,0.0,0.013933333333333336,0.0,2.755275898393481,2.755275898393481
2018-01-01 00:12:00,149.02000002022487,156.10895023557381,0.0,0.013933333333333336,0.0,2.755275900571683,2.755275900571683
2018-01-01 00:15:00,149.02000007188917,154.97501455537628,0.0,0.013933333333333336,0.0,2.75527590738754,2.75527590738754
2018-01-01 00:18:00,149.02000019652166,153.89782161722897,0.0,0.013933333333333336,0.0,2.755275923829774,2.755275923829774
2018-01-01 00:21:00,149.0200004498227,152.70429058588806,0.0,0.013933333333333336,0.0,2.7552759572467305,2.7552759572467305
2018-01-01 00:24:00,149.02000090609062,151.22134064452328,0.0,0.013933333333333336,0.0,2.7552760174402433,2.7552760174402433
2018-01-01 00:27:00,149.02000165778895,149.3112895614478,0.0,0.
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Process ID: 1
Simulation starts ...
Simulation Completed!
patient=adolescent#001 days=1 sensor=Dexcom pump=Insulet meals=random seed=1
rows=481 (one per sample time)
BG mean=126.8 min=86.1 max=160.6 mg/dL
time in range 70-180 = 100.0 %
time below 70 = 0.0 %, above 180 = 0.0 %
mean LBGI=0.30 HBGI=1.43
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--patient` | Virtual patient | adolescent#001 | adolescent#001, adolescent#002, adolescent#003, adolescent#004, adolescent#005, adolescent#006, adolescent#007, adolescent#008, adolescent#009, adolescent#010, adult#001, adult#002, adult#003, adult#004, adult#005, adult#006, adult#007, adult#008, adult#009, adult#010, child#001, child#002, child#003, child#004, child#005, child#006, child#007, child#008, child#009, child#010 |
| `--days` | Days | 1 | 1 to 14 |
| `--sensor` | CGM sensor | Dexcom | Dexcom, GuardianRT, Navigator |
| `--pump` | Insulin pump | Insulet | Cozmo, Insulet |
| `--meals` | Meal scenario | random | random, custom |
| `--seed` | Seed | 1 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The result table has a time index and these columns, from the source:

- `BG`: true blood glucose, in mg/dL.
- `CGM`: the sensor reading, with noise.
- `CHO`: carbohydrate eaten at that step.
- `insulin`: insulin delivered.
- `LBGI`, `HBGI`: low and high blood glucose indices.
- `Risk`: the combined risk index.

The recipe writes it as `results.csv` and prints a summary: mean, minimum and maximum glucose, the share of time between 70 and 180 mg/dL, below 70 and above 180, and the mean LBGI and HBGI. The patient file named after the virtual patient holds the same table.

Plot BG against CHO and insulin to see how each meal moves glucose and how the controller responds. The CGM value is built from the subcutaneous glucose of the patient model plus sensor noise.

## Pitfalls

- **The meal list is in hours.** In a custom scenario a plain number is read as hours after the start time. A timedelta or datetime is also accepted.
- **Random scenarios draw new meals each day.** Set the seed in both `RandomScenario` and `CGMSensor` to repeat a run.
- **Gymnasium observations are arrays.** Since the August 2023 update the Gymnasium environment returns a numpy array. The older Gym one returns a namedtuple with a CGM field.
- **Animation and parallel runs clash on macOS.** The README says most Matplotlib backends there are not thread-safe, so do not set both `animate` and `parallel`.
- **The `gym` pin is old.** `gym==0.9.4` is a very old release. Install into a fresh virtual environment.
- **Virtual patients are not people.** The README describes the simulator as for research use only.

## Further reading

- Project: https://github.com/jxx123/simglucose
- Patient parameter definitions: https://github.com/jxx123/simglucose/blob/master/definitions_of_vpatient_parameters.md
- Examples folder: https://github.com/jxx123/simglucose/tree/master/examples
- Man CD, Micheletto F, Lv D, Breton M, Kovatchev B, Cobelli C (2014). The UVA/PADOVA type 1 diabetes simulator: new features. J Diabetes Sci Technol 8:26-34. https://doi.org/10.1177/1932296813514502

---

Cite: Xie J (2018). Simglucose v0.2.1. https://github.com/jxx123/simglucose. Model: Man CD, Micheletto F, Lv D, Breton M, Kovatchev B, Cobelli C (2014). The UVA/PADOVA type 1 diabetes simulator: new features. J Diabetes Sci Technol 8:26-34. doi:10.1177/1932296813514502

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/simglucose).
