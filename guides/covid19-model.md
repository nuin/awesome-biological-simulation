# covid19-model simulator

> Simulate a stochastic, site-based epidemic with household transmission, testing and smart contact tracing on a bundled Swiss or German region.

Licence: MIT · [Source code](https://github.com/covid19-model/simulator)

## What it simulates

The covid19-model simulator follows every person in a small region through households and visits to public sites such as shops, schools, offices, social venues and bus stops. People visit sites according to a mobility trace. An infected person exposes the people at the same site and in the same household, and infection events are drawn in continuous time. The number of secondary cases per person comes out overdispersed, because a few visits to crowded sites cause most infections.

On top of that it models testing and contact tracing: symptomatic people get tested, positives isolate, and their traced contacts are tested and isolated. The authors fitted it to German and Swiss case counts and used it to ask what tracing and testing achieve.

Inputs are a region (a bundled mobility file), the transmission rates at sites and in households, the starting number of exposed people, and the tracing policy. Output is the infection history of everyone, which the recipe reduces to daily counts and a summary row.

## When to use it

- You want to see how a tracing app or household isolation changes attack rate in a town-sized population.
- You want an overdispersed, site-based epidemic that a compartmental model cannot give.
- You want a working example of the published code in a container.

Use [epydemix](epydemix.md) for age-structured compartmental epidemics, and [odin](odin.md) for epidemics defined by your own equations. This simulator carries no real case data in the recipe.

## Install it yourself

The upstream repository (MIT) lists its dependencies in `requirements.txt`: numba 0.48.0, numpy 1.22.0, pandas 1.0.3, torch 2.2.0, botorch 0.2.1 and others. Torch and botorch serve only the parameter calibration.

The recipe skips calibration. It runs Python 3.10.15 with numpy 1.23.5, pandas 1.5.3, scipy 1.10.1, numba 0.57.1, networkx 2.8.8, interlap 0.2.7, joblib 1.2.0, sympy 1.12, matplotlib 3.7.3 and pathos 0.3.1, on the repository at commit 4ab126a. Four downsampled regions ship in the image: Tubingen, Kaiserslautern and Bern at 1 in 10, Locarno at 1 in 2. The helper script `run_c19.py` follows the repository's `sim-baseline.py`, and runs the repeats one after another so that the seed fixes the result.

## Run the tested example

This recipe builds covid19-model simulator in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 30.3 s.

1. Download [covid19-model-recipe.tar.gz](https://biosimhub.pages.dev/guides/covid19-model/covid19-model-recipe.tar.gz) (Dockerfile, run_c19.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf covid19-model-recipe.tar.gz
   cd covid19-model
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/covid19-model:4ab126a .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/covid19-model:4ab126a python /opt/c19/run_c19.py --region tubingen \
    --days 60 --repeats 1 --seed-exposed 20 --beta-site 0.02 \
    --beta-household 0.02 --tracing household \
    --compliance 0 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `daily.csv` | 729 B |
| `run_log.txt` | 148 B |
| `summary.csv` | 198 B |

<details><summary>First lines of <code>daily.csv</code></summary>

```
repeat,day,new_infections,new_symptomatic,new_positive_tests
0,0,20,0,0
0,1,2,0,0
0,2,7,0,0
0,3,11,3,0
0,4,2,4,3
0,5,3,1,7
0,6,3,3,9
0,7,5,3,2
0,8,3,1,3
0,9,6,1,1
0,10,5,2,4
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
repeat 0: 381 of 9054 infected, peak 17 per day on day 34
done: tubingen, 9054 people, 148 sites, 60 days, 1 repeats; mean attack rate 4.21 percent
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
repeat,people,sites,ever_infected,attack_rate_pct,peak_new_infections_per_day,peak_day,tested_positive,dead,hospitalised,site_exposures,household_exposures
0,9054,148,381,4.21,17,34,304,1,8,161,197
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--region` | Region (downsampled 1 in 10 | tubingen | tubingen, kaiserslautern, bern, locarno |
| `--days` | Simulated days | 60 | 10 to 120 |
| `--repeats` | Repeats (one mobility trace each) | 1 | 1 to 5 |
| `--seed-exposed` | Individuals exposed on day 0 | 20 | 1 to 200 |
| `--beta-site` | Transmission rate at sites | 0.02 | 0 to 0.1 |
| `--beta-household` | Transmission rate in households | 0.02 | 0 to 0.1 |
| `--tracing` | Contact tracing (household traces and isolates household members; app traces every contact of app users) | household | household, app |
| `--compliance` | Share of people using the tracing app (needs app tracing) | 0 | 0 to 1 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is the Tubingen region (9054 people, 148 sites), 60 days, 1 repeat, 20 people exposed on day 0, transmission rate 0.02 at sites and in households, household-only tracing, seed 42. It takes about 30 s.

- `run_log.txt` says "381 of 9054 infected, peak 17 per day on day 34". That is a 4.21 percent attack rate.
- `summary.csv` has one row per repeat. Of the 381 infected, 304 tested positive, 8 were hospitalised and 1 died. There were 161 site exposures and 197 household exposures.
- `daily.csv` has one row per repeat and day with new infections, new symptomatic cases and new positive tests. Day 0 shows 20 new infections, the seeded people.

The counts agree with each other. The 20 seeds, 161 site exposures and 197 household exposures give 378. The remaining 3 are background exposures, which the helper sets to 5/7 per 100,000 people per day, or 3.9 expected over 60 days in this population.

The default rates of 0.02 are not fitted values. The upstream authors calibrated each region against real cases, and the recipe does not load those values. Treat results as behaviour of the model, not as a forecast.

## Your own runs

Each run changes one setting from the example (Tubingen, 60 days, 1 repeat). The attack rate is the share of 9054 people infected.

- **App tracing.** `--tracing app` traces every contact of app users instead of household members only. With no app users (`--compliance 0`) it gave 381 infected, the same as household tracing. With half the people on the app, 172 infected (1.90 percent). With everyone, 97 (1.07 percent).
- **Higher transmission.** Both rates at 0.03 gave 1500 infected (16.57 percent), a peak of 72 per day on day 59, 1041 positive tests and 2 deaths. The epidemic was still growing at day 60.
- **Another region.** `--region bern` gave 6377 of 13377 people infected (47.67 percent) with a peak of 256 per day on day 30 and 17 deaths. Bern's trace has 225 sites. The same rates spread much further than in Tubingen.
- **Another seed.** `--seed 43` gave 201 infected (2.22 percent) with a peak of 9 per day on day 59, against 381 for seed 42. Report several seeds or use `--repeats`.

## Pitfalls

- **Rates do not transfer between regions.** The same 0.02 gave 4.21 percent in Tubingen and 47.67 percent in Bern, because each region has its own mobility trace. Pick rates per region.
- **Run time follows epidemic size.** The 60-day example took about 30 s. A larger epidemic takes longer because every infection triggers contact and tracing events.
- **Day 0 is not a peak.** The seeded exposures all land on day 0, so the summary reports the peak from day 1.
- **Tracing needs compliance in app mode.** In household mode `--compliance` changes nothing, because household members are traced without the app.
- **Repeats run in sequence.** Each repeat adds roughly the single-run time.

## Further reading

- Source and README: https://github.com/covid19-model/simulator
- Preprint: https://arxiv.org/abs/2004.07641
- Paper: Lorch L et al. (2022) Quantifying the effects of contact tracing, testing, and containment measures in the presence of infection hotspots. ACM Transactions on Spatial Algorithms and Systems 8(4). https://doi.org/10.1145/3530774

---

Cite: Lorch L, Kremer H, Trouleau W, Tsirtsis S, Szanto A, Schoelkopf B, Gomez-Rodriguez M (2022). Quantifying the effects of contact tracing, testing, and containment measures in the presence of infection hotspots. ACM Trans Spatial Algorithms Syst 8(4). doi:10.1145/3530774

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/covid19-model).
