# R simulators (webR)

> R 4.6 in the browser: stochastic SIR epidemics with SimInf or adaptivetau, and random trees with ape.

Licence: GPL-3.0 (webR binaries; R itself GPL-2 | GPL-3); packages: SimInf GPL-3, adaptivetau GPL-3.0-or-later, ape GPL-2 | GPL-3 · [Source code](https://github.com/r-wasm/webr)

**[Run R simulators (webR) in your browser](https://biosimhub.pages.dev/run/webr/index.html)**: R 4.6 in the browser: stochastic SIR epidemics with SimInf or adaptivetau, and random trees with ape. Nothing to install; the first visit downloads about 22 MB.

[![The R simulators (webR) plugin after its default run](https://biosimhub.pages.dev/media/webr/plugin-light.png)](https://biosimhub.pages.dev/run/webr/index.html)

## What it simulates

webR is R compiled to WebAssembly, so R packages run inside your browser tab. The page uses it for three models.

- **SIR with SimInf.** A stochastic epidemic in one well-mixed population. SimInf runs it as an exact Gillespie simulation of infection (S to I) and recovery (I to R) events.
- **SIR with adaptivetau.** The same process written as two transitions with rates beta x S x I / N and gamma x I, run by adaptive tau-leaping. The output is event times, which the page samples on whole days.
- **Random tree with ape.** `rcoal(n)` draws a coalescent tree, in which tips join in random pairs backwards in time. `rtree(n)` draws a random topology with random branch lengths.

Both SIR models use frequency-dependent transmission. With the same parameters they simulate the same process, so you can compare them. Counts are whole individuals, and every run starts from `set.seed(seed)`.

## When to use it

- You work in R and want to try a stochastic epidemic model or a random tree before you write a script.
- You want to compare an exact method (SimInf) with an approximate one (adaptivetau) on the same SIR model.
- You need a quick random tree in Newick format, for example for a teaching example.

[epydemix](epydemix.md) on biosimhub fits when you want 5, 50 and 95 percent bands over many runs and a Python workflow. [GillesPy2](gillespy2.md) fits for general reaction networks. [msprime](msprime.md) fits when you need real population-genetic coalescent simulations with recombination and demography. The `rcoal` tree here is a simple coalescent shape. It does not model a specific population.

## Run it in your browser

R starts once per visit. Each package installs on the first run of a model that needs it and is kept for the rest of the visit.

Controls:

- **Model.** SIR, SimInf (default), SIR, adaptivetau or Random tree, ape. The link parameter `?model=siminf|adaptivetau|ape` preselects one.
- **SIR fields.** Population N (default 1000, up to 1,000,000), Initially infected (10), Transmission rate beta per day (0.3), Recovery rate gamma per day (0.1) and Days (120, up to 2000).
- **Tree fields.** Tree (`rcoal` or `rtree`) and Tips (12, from 2 to 300).
- **Seed.** Default 42. Each run calls `set.seed(seed)` first.
- **Run.** Errors such as 0 initially infected appear in the status line in plain words.

Readouts for SIR: a chart of Susceptible, Infected and Recovered per day, and a table with R0 = beta / gamma, the peak infected and its day, the recovered count and percentage at the end, and the number still infected. The adaptivetau page also shows the number of simulation steps. For trees: an SVG drawing with a scale bar and the Newick string.

Measured in headless Chromium, starting R downloads 12.7 MB and takes 1.4 to 2.1 s, or 5.6 s on a cold first fetch. SimInf adds 9.5 MB and 2.5 to 2.8 s. adaptivetau adds 1.4 MB. ape adds 8.3 MB. A run itself takes 0.01 to 0.06 s. The default first visit transfers about 22.7 MB.

Limits: three models only, WebAssembly-built packages only, and possible memory caps on phones. The webR repository has SimInf 10.1.0, while CRAN has 11.1.0. Two packages do not work: phangorn installs but fails to load, and deSolve has no WebAssembly build. R graphics to SVG draws no text in webR, so the page draws trees itself.

## Install it yourself

Native R has all of this. Install R from https://cran.r-project.org/, then:

```r
install.packages(c("SimInf", "adaptivetau", "ape"))
```

Package pages: SimInf (CRAN version 11.1.0), adaptivetau (2.3-2) and ape (5.8-1). In a conda-forge test, `r-ape` resolved and ran under R 4.5.3. A conda-forge install of `r-siminf` and `r-adaptivetau` did not resolve, so use CRAN for those two. A CRAN source install of adaptivetau inside a bare conda environment failed to build. The cause is probably a missing build dependency.

To run webR yourself, the npm package is `webr` (version 0.6.0). Packages install with `webr::install("Matrix")` from R code inside webR, as the webR documentation shows.

Minimal commands in R, the same as the page runs:

```r
library(adaptivetau)
set.seed(42)
trans <- list(c(S = -1, I = +1), c(I = -1, R = +1))
rates <- function(x, p, t) c(p$beta * x[["S"]] * x[["I"]] / p$N, p$gamma * x[["I"]])
out <- ssa.adaptivetau(c(S = 990, I = 10, R = 0), trans, rates,
                       list(beta = 0.3, gamma = 0.1, N = 1000), tf = 120)

library(ape)
set.seed(42)
tr <- rcoal(12)
write.tree(tr)
```

For SimInf, the page runs `SIR(u0 = data.frame(S = 990L, I = 10L, R = 0L), tspan = 0:120, beta = 0.3, gamma = 0.1)`, then `run()` and `trajectory()`.

## Reading the output

With the defaults, R0 = 0.3 / 0.1 = 3. A population of 1000 with 10 infected has a large outbreak in most seeds, and the chart shows infected rising, peaking and falling as susceptibles run out. The table reports the peak and the recovered percentage. For R0 = 3 the deterministic final size is about 94 percent, and a stochastic run can fall below it when the first infections recover before they spread.

For the tree model with `rcoal`, run seed 42 with 12 tips. In native R 4.5.3 with ape 5.8.1 the tree has total height 1.953, and sister tips have equal branch lengths, which makes it ultrametric. The same seed with `rtree(12)` gives a tree of height 3.513 whose tips are at different depths. The Newick starts `((t10:0.3695...`. The page may print a different tree if its R version draws differently, so compare Newick strings rather than assuming they match.

## Your own runs

Try these in the page, and change one value at a time.

- **Same model, two seeds.** Run SimInf at seed 42 and seed 7. Compare the peak day and the recovered percentage.
- **SimInf against adaptivetau.** Use the same parameters and seed. The two methods draw random numbers differently, so paths differ. Compare the summary table rather than single curves.
- **Lower beta.** Set beta to 0.15, so R0 = 1.5. Compare the peak size and day with the default run.
- **Bigger population.** Set N to 10,000 and initially infected to 100. A run with N = 100,000 over 200 days takes 0.02 s with adaptivetau.
- **Tree.** Switch to ape and compare `rcoal` with `rtree` at 12 and 100 tips.

## Pitfalls

- **First run is slow.** The first run of each model downloads its package. Later runs are instant.
- **Seeds are per run.** Each run sets the seed first. The same seed and parameters repeat the same output.
- **Rates are per day.** beta and gamma are per day, and the chart x axis is in days. Rescale if your rates are per week.
- **Package versions differ.** The page has SimInf 10.1.0, and CRAN has 11.1.0. Results can differ between versions.

## Further reading

- webR documentation: https://docs.r-wasm.org/webr/latest/
- Installing packages in webR: https://docs.r-wasm.org/webr/latest/packages.html
- webR source: https://github.com/r-wasm/webr
- SimInf: https://cran.r-project.org/package=SimInf, paper: Widgren S et al. (2019), J Stat Softw 91(12), https://doi.org/10.18637/jss.v091.i12
- adaptivetau: https://cran.r-project.org/package=adaptivetau
- ape: https://cran.r-project.org/package=ape

---

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/webr).
