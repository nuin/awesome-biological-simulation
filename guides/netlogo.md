# NetLogo Web

> Agent-based models from the NetLogo Models Library, run by NetLogo Web (Tortoise) embedded from netlogoweb.org, with a seeded run and population chart.

Licence: GPL-2.0-or-later (engine); models CC BY-NC-SA 3.0 · [Source code](https://github.com/NetLogo/Tortoise)

**[Run NetLogo Web in your browser](https://biosimhub.pages.dev/run/netlogo/index.html)**: Agent-based models from the NetLogo Models Library, run by NetLogo Web (Tortoise) embedded from netlogoweb.org, with a seeded run and population chart. Nothing to install; the first visit downloads about 1 MB.

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/netlogo/plugin-dark.png"><img src="https://biosimhub.pages.dev/media/netlogo/plugin-light.png" alt="NetLogo Web running in the browser" width="760"></picture>

## What it simulates

NetLogo simulates agents that follow simple rules on a grid. Each agent (a turtle) has its own state, and the grid cells (patches) have state too. Population patterns come out of the rules. No equations are solved. You press `setup` to build the world and `go` to advance one tick at a time.

The page runs two models from the NetLogo Models Library, both CC BY-NC-SA 3.0.

- **Wolf Sheep Predation** (Wilensky, 1997). Wolves eat sheep, sheep eat grass and grass regrows. The `sheep-wolves-grass` version is generally stable and resembles Lotka-Volterra oscillations. The `sheep-wolves` version, with unlimited grass, tends to be unstable and often ends in extinction.
- **Virus** (Wilensky, 1998). A virus spreads through 150 people who move at random, age, reproduce, recover and gain immunity. One tick is one week.

The key assumptions are the model's own rules: random movement, local contact, and fixed per-tick probabilities such as `sheep-reproduce` at 4 percent. Randomness comes from one seeded generator, so a seed fixes the whole run.

## When to use it

- You ask how local rules (who meets whom) produce population cycles, outbreaks or extinctions.
- You want to see individuals as well as totals, for example how a virus moves through a crowd.
- You teach agent-based modelling and want ready-made models you can change with sliders.

[epydemix](epydemix.md) fits when you want a well-mixed epidemic with percentile bands over many runs. [GillesPy2](gillespy2.md) fits when the predator-prey model is a set of reactions with counts. NetLogo fits when space and individual differences matter.

## Run it in your browser

The page embeds NetLogo Web (the Tortoise engine and the Galapagos interface) from netlogoweb.org. It loads the model file from the NetLogo Models Library on GitHub, pinned to one commit (`a83b6f18cd5d7bc2323d8d86497243b791be04ea`), so the model text does not change under you. The engine itself is not pinned: netlogoweb.org serves its current build.

Controls:

- **Model.** Wolf Sheep Predation or Virus. The sliders below change with the model.
- **Wolf Sheep sliders.** `model-version`, `initial-number-sheep` (default 100), `initial-number-wolves` (50), `sheep-gain-from-food` (4), `wolf-gain-from-food` (20), `sheep-reproduce` (4 percent), `wolf-reproduce` (5 percent) and `grass-regrowth-time` (30).
- **Virus sliders.** `number-people` (150), `infectiousness` (65 percent), `chance-recover` (75 percent) and `duration` (20 weeks).
- **Seed, Ticks, Sample every.** Defaults are seed 42, 500 ticks and every 5 ticks for Wolf Sheep, and 200 ticks and every 4 for Virus.
- **Run and Stop.** Run sends `random-seed`, your slider values and `setup` to the model. Then it calls `go` in blocks and reads the counts after each block.

Readouts:

- **Chart.** Wolf Sheep plots Sheep, Wolves and Grass / 4 (grass version only). Virus plots Sick, Immune, Healthy and Total.
- **Final table.** The counts at the last tick.
- **NetLogo view.** The model's own world, monitors and plot, live in a frame. You can use its buttons too, but pressing its `go` while a run is in progress mixes the two.

Reported timings: 500 ticks of Wolf Sheep in about 2.7 s, 200 weeks of Virus in about 1 s, and 2 to 4 s to load the engine and model. The same seed gave the same counts across browser contexts. If `go` stops itself, as Wolf Sheep does when the wolves die out and sheep are abundant, the run ends early and says so.

Limits: the page needs network access to netlogoweb.org and raw.githubusercontent.com. Only two models are offered.

## Install it yourself

NetLogo desktop is free. Download it from https://www.netlogo.org/ (the documentation lists version 7.0.4 on its download page). The model files are in the library at https://github.com/NetLogo/models.

To run without the interface, the BehaviorSpace documentation gives:

```
./NetLogo_Console --headless --model "Wolf Sheep Predation.nlogox" --experiment "<name>" --table -
```

`--experiment` names an experiment saved in the model, and `--table -` writes a table of results to standard output. Use `--setup-file <path>` to read experiments from an XML file. In the experiment setup commands, `random-seed 473 setup` fixes the seed. `random-seed (474 + behaviorspace-run-number) setup` gives each repetition its own seed.

## Reading the output

Run Wolf Sheep with the defaults: 100 sheep, 50 wolves, the grass version, seed 42, 500 ticks, sampled every 5. The chart plots Sheep, Wolves and Grass / 4 against tick. The model documentation says this version resembles Lotka-Volterra oscillations, so look for sheep and wolf curves that rise and fall out of step. "Grass / 4" is the model's own scaling, which puts the grass count on the same axis as the animals. Read the exact counts from the final table.

For Virus, the defaults are 150 people, 65 percent infectiousness, 75 percent chance of recovery and 20 weeks duration. The Virus documentation says an initial outbreak usually spreads fast because nobody is immune, then declines. It also notes that a virus that infects almost everyone can die out, because the survivors are immune.

The status line reports each load step with elapsed seconds, then the final tick count. Compare the table with the monitors in the NetLogo view. They report the same values.

## Your own runs

Change one slider and keep the seed.

- **Wolf Sheep, no wolves.** Set `initial-number-wolves` to 0 in the grass version. The model documentation says this gives a stable sheep-and-grass system.
- **Wolf Sheep, `sheep-wolves` version.** The documentation says extinction is common. Run a few seeds to see how often it happens.
- **Virus, Ebola-like.** Short `duration`, high `infectiousness` and a very low `chance-recover`, as the model documentation suggests. See whether the virus persists.
- **Virus, HIV-like.** Long `duration`, very low `chance-recover` and low `infectiousness`.

Change the seed too, and compare. A single seed is one sample of a random process.

## Pitfalls

- **Slider ranges.** The page rejects values outside the model's slider range, for example `sheep-reproduce` above 20.
- **Seeds fix one run.** Report several seeds before you claim a pattern.
- **The frame's own buttons.** Do not press `go` in the frame while the page is running. The next Run resets the sliders it uses, so it starts clean.
- **Units.** Virus ticks are weeks. Wolf Sheep ticks have no unit. Grass is shown divided by 4.
- **Licence.** The models are NonCommercial. Reuse beyond teaching and research needs a licence from the authors.

## Further reading

- NetLogo documentation: https://docs.netlogo.org/
- Programming guide: https://docs.netlogo.org/programming
- BehaviorSpace (headless runs): https://docs.netlogo.org/behaviorspace
- NetLogo Web: https://www.netlogoweb.org/
- Tortoise engine: https://github.com/NetLogo/Tortoise
- Wolf Sheep Predation: https://ccl.northwestern.edu/netlogo/models/WolfSheepPredation
- Virus: https://ccl.northwestern.edu/netlogo/models/Virus
- Citation: Wilensky U (1999). NetLogo. Center for Connected Learning and Computer-Based Modeling, Northwestern University, Evanston, IL. http://ccl.northwestern.edu/netlogo/

---

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/netlogo).
