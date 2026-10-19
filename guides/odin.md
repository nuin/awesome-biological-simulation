# odin

> Compile an ODE or discrete-time stochastic compartmental model written in the odin language and write its trajectories and summary.

Licence: MIT · [Source code](https://github.com/mrc-ide/odin)

## What it simulates

odin is a domain-specific language for compartmental models. You write the equations in R syntax, such as `deriv(S) <- -beta * S * I / N`. odin generates C code from them and solves the system. Continuous-time models go to the deSolve solvers (LSODA by default). Discrete-time models step forward in whole time units and may draw random numbers, so one file can describe a deterministic ODE or a stochastic binomial-chain epidemic.

The inputs are the model file and its `user()` parameters. The output is a table with one row per time point and one column per state variable. odin has no built-in epidemic model. Whatever you write is what runs.

## When to use it

- You want a transparent SIR, SEIR or age-structured model whose equations sit in the file as written.
- You need the same model as an ODE and as a stochastic discrete-time chain, to see how much noise matters.
- You call the model many times, for example in a fit, and the C code pays off over plain R.

Use [epydemix](epydemix.md) for epidemics with age groups and contact matrices that are already built in. Use [GillesPy2](gillespy2.md) for exact stochastic simulation of reaction networks. odin fits when the equations are your own.

## Install it yourself

odin is on CRAN under the MIT licence. The recipe pins odin 1.2.7 on R 4.2.2 (Debian 12), with ring 1.0.8, cinterpolate 1.0.2 and dde 1.0.7 installed from CRAN source. The odin README describes the compile-to-C design. A C compiler (gcc and make) must be present when the model runs.

```r
install.packages("odin")   # also needs gcc and make on the machine
gen <- odin::odin_("sir.R")
mod <- gen$new(beta = 0.25)
y <- mod$run(seq(0, 100, length.out = 101))
```

`odin_()` takes a file path in a variable. `odin()` quotes its argument, so `odin::odin(path)` stops with "Every line must contain an assignment".

Discrete-time models also need the dde package. Without it the run stops with "there is no package called 'dde'".

## Run the tested example

This recipe builds odin in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 1.4 s.

1. Download [odin-recipe.tar.gz](https://biosimhub.pages.dev/guides/odin/odin-recipe.tar.gz) (Dockerfile, run_odin.R, example model.r, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf odin-recipe.tar.gz
   cd odin
   sh run.sh
   ```

![Terminal recording of the odin example run](https://biosimhub.pages.dev/media/odin/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/odin:1.2.7 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/odin:1.2.7 Rscript /opt/run_odin.R /work/in/model.r --tmax 100 \
    --points 101 --replicates 5 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `run_log.txt` | 125 B |
| `summary.csv` | 141 B |
| `trajectory.csv` | 5.5 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/odin/result-dark.png"><img src="https://biosimhub.pages.dev/media/odin/result.png" alt="Plot of the odin example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>run_log.txt</code></summary>

```
odin 1.2.7 (c target), model model.r, continuous time, 0 user parameters set
done: 101 rows, 1 replicate(s), variables S,I,R
```

</details>

<details><summary>First lines of <code>summary.csv</code></summary>

```
replicate,S_final,S_max,S_t_at_max,I_final,I_max,I_t_at_max,R_final,R_max,R_t_at_max
1,19.6492,990,0,0.431741,405.459,19,979.919,979.919,100
```

</details>

<details><summary>First lines of <code>trajectory.csv</code></summary>

```
replicate,t,S,I,R
1,0,990,10,0
1,1,985.403660164034,13.4329451313097,1.16339470465573
1,2,979.269514187754,18.0059741105152,2.72451170173114
1,3,971.11851086425,24.067379846489,4.8141092892605
1,4,960.349648915049,32.0484713875394,7.60187969741187
1,5,946.229654000418,42.4654304451722,11.3049155544091
1,6,927.89828000975,55.9060086781597,16.19571131209
1,7,904.402542510851,72.9898557018307,22.6076017873183
1,8,874.775527793149,94.2900628047566,30.9344094020939
1,9,838.173799340228,120.206344379063,41.6198562807085
1,10,794.074214582674,150.793812930216,55.1319724871096
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--tmax` | Simulated time | 100 | 1 to 100000 |
| `--points` | Output time points | 101 | 2 to 5000 |
| `--replicates` | Replicates (discrete-time models only) | 5 | 1 to 100 |
| `--seed` | Seed | 42 | 1 to 2147483647 |
| `--set` | Override user parameter beta (optional) | not set | 0 to 1000 |
| `--set` | Override user parameter gamma (optional) | not set | 0 to 1000 |
| `--set` | Override user parameter I0 (optional) | not set | 0 to 1000000 |
| `--set` | Override user parameter N (optional) | not set | 1 to 100000000 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example model, `model.r` in the recipe, is a deterministic SIR with N 1000, 10 infected at the start, beta 0.4 and gamma 0.1 per day. The helper script `run_odin.R` compiles it, runs it for 100 days at 101 points and writes three files.

- `run_log.txt` says "odin 1.2.7 (c target), model model.r, continuous time". The C target means odin compiled and loaded the C code.
- `trajectory.csv` has 101 rows with columns replicate, t, S, I, R. It starts at S 990, I 10, R 0.
- `summary.csv` has one row per replicate with the final value, the maximum, and the time of the maximum of each variable.

Check the numbers against theory. R0 = beta / gamma = 4. The peak of I is 405.459 at day 19. The closed form for a large outbreak gives about 403, so the solver agrees. The final R is 979.919 and S is 19.6492. The final-size equation s = exp(-4 (1 - s)) gives s = 0.0197, so 19.7 people stay susceptible. The S and R "max" and "t at max" columns are only the start or end values, since S falls and R rises.

## Your own runs

The stochastic variant uses `update()` with a binomial draw per day: `n_SI <- rbinom(S, p_SI)`. Save it over `in/model.r` of the recipe, or upload it as the model. Each run below used seed 42.

- **Stochastic, 5 replicates.** Peak I was 455, 435, 438, 416 and 420, on days 20 to 25. Final R was 978 to 989. The ODE gave 405 on day 19 and 980, so the chain peaks a little later and a little higher than the ODE.
- **Lower transmission.** `--set beta=0.25` (R0 2.5) gave a peak of 237.5 on day 33 and a final R of 888.5.
- **Below threshold.** `--set beta=0.08` (R0 0.8) gave no outbreak. I never rose above its start of 10, and final R was 40.5.
- **One seed case, stochastic.** `--set I0=1` with 5 replicates gave three outbreaks (peaks 418, 457 and 429, final R 978, 978 and 983). Two replicates died out at once, with peaks of 2 and 1 and final R of 2 and 1. A deterministic model cannot show this.

## Pitfalls

- **/tmp without exec rights.** The job sandbox mounts /tmp so that programs cannot load code from it. odin then cannot load the C it compiles and falls back to the slower R target, with the same results. The helper script restarts R with its temporary folder in the working directory so the C target works.
- **Image size.** The image is about 959 MB because the compiler stays in it.
- **Overrides only for named parameters.** The helper script passes `--set` values for beta, gamma, I0 and N. A model that declares other `user()` names needs its own defaults in the file.
- **Random numbers come from R.** Stochastic models use R's generator, so `--seed` fixes all replicates together. Replicates differ because they continue one stream.
- **Time unit.** Discrete models step in whole units. Rates must be converted to per-step probabilities, as the file does with `1 - exp(-beta * I / N)`.

## Further reading

- odin guide: https://mrc-ide.github.io/odin/articles/guide.html
- Functions available in models: https://mrc-ide.github.io/odin/articles/functions.html
- Source: https://github.com/mrc-ide/odin
- Paper: FitzJohn RG et al. (2021) Reproducible parallel inference and simulation of stochastic state space models using odin, dust, and mcstate. Wellcome Open Research 5:288. https://doi.org/10.12688/wellcomeopenres.16466.2

---

Cite: FitzJohn RG, et al. (2021). Reproducible parallel inference and simulation of stochastic state space models using odin, dust, and mcstate. Wellcome Open Res 5:288. doi:10.12688/wellcomeopenres.16466.2

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/odin).
