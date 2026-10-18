# Artistoo

> Cellular Potts model of cells and tissues: cell sorting by differential adhesion, or a single migrating cell (Act model).

Licence: MIT · [Source code](https://github.com/ingewortel/artistoo)

**[Run Artistoo in your browser](https://biosimhub.pages.dev/run/artistoo/index.html)**: Cellular Potts model of cells and tissues: cell sorting by differential adhesion, or a single migrating cell (Act model). Nothing to install; the first visit downloads about 0 MB.

## What it simulates

Artistoo simulates cells on a pixel grid with the Cellular Potts Model (CPM). Each cell is a set of pixels. The model makes copy attempts, where a pixel tries to take the label of a neighbor. Energy constraints decide how likely each attempt is. The constraints here are adhesion between neighbors, a volume constraint and, for the Act model, perimeter and activity constraints. The page counts time in Monte Carlo steps (MCS).

The browser page runs two models with Artistoo 1.2.0:

- **Cell sorting.** Two cell types start as a randomly mixed disc. Adhesion energy J is set for same-type contacts, different-type contacts and contacts with the medium.
- **Migrating cell (Act model).** One cell with volume, perimeter and activity constraints crawls across the grid. The cell reinforces recently protruded pixels. This follows Niculescu et al. (2015).

The temperature T sets how strongly the model listens to the energy constraints, as the Artistoo manual puts it.

## When to use it

Use it to ask what cell-cell adhesion, size and motility rules produce:

- Does a difference in adhesion strength sort two cell types?
- How fast does sorting happen at a given temperature?
- Does a stronger activity constraint make a cell travel farther?

[PyAFV](pyafv.md) and [tyssue](tyssue.md) on biosimhub model tissue as polygons (active Voronoi cells and a vertex model). They fit confluent epithelia, where cell shape is a polygon with a preferred area and perimeter. Artistoo fits when cells deform freely, round up, crawl or sit among a medium.

## Run it in your browser

Press **Run** with the defaults. The lattice draws live and the chart updates as it goes. The page needs no install. The run happens in your browser.

Controls:

- **Model** picks sorting or Act. Choosing one resets grid size, target volume and MCS to that model's defaults.
- **Grid size** is pixels per side (40 to 300). The grid wraps around at the edges.
- **Cells of type A / B** (sorting only) set the cell counts. 40 + 40 cells of 100 pixels is the default.
- **Target volume** is the pixel count each cell tries to keep.
- **J same type, J different type, J with medium** (sorting only) are adhesion energies. Defaults 10, 40 and 20. Sorting needs J different type to be higher than J same type.
- **Act strength** and **Act memory** (Act only) are LAMBDA_ACT (default 200) and MAX_ACT (default 80).
- **Temperature T** defaults to 20.
- **Monte Carlo steps** defaults to 3000 for sorting and 1000 for Act.
- **Seed** must be 1 or more. Seed 0 would make Artistoo pick a random seed, so the page refuses it.

Readouts:

- For sorting, the chart is the **heterotypic fraction**. It is the share of cell-cell boundary (4-neighbor pixel pairs) that joins an A cell to a B cell. Random mixing of equal numbers gives about 0.5. A lower value means more sorting.
- For Act, the chart is the net displacement of the cell centroid from its start, in pixels, unwrapped across the periodic edge.
- The **Grid hash** is an FNV-1a hash of the final lattice. The same parameters and seed give the same hash.

Limits: the browser build runs on the main thread, so the grid stops at 300 and runs stop at 20000 MCS. The page rejects setups where the cells do not fit, which is when the cell disc is wider than 90% of the grid. Constants not in the form are fixed. The volume constraint LAMBDA_V is 50 and the Act model's perimeter constraint LAMBDA_P is 2. With reduced motion set in the OS, only the final state is drawn.



## Install it yourself

Artistoo is not on npm. The Artistoo manual says to clone the repository (`git clone https://github.com/ingewortel/artistoo.git`) and use the files in `build/`. The page here vendors version 1.2.0 of `build/artistoo.js` unchanged.

In a web page, load it and build a model:

```html
<script src="artistoo.js"></script>
<script>
  const C = new CPM.CPM([60, 60], {
    torus: [true, true], seed: 1, T: 20,
    J: [[0, 20], [20, 100]], V: [0, 200], LAMBDA_V: [0, 50]
  });
  const id = C.makeNewCellID(1);
  for (let x = 25; x < 35; x++) for (let y = 25; y < 35; y++) C.setpix([x, y], id);
  for (let i = 0; i < 200; i++) C.timeStep();
  console.log(C.time, C.getVolume(id));
</script>
```

Run against the 1.2.0 build in Node, this code grew the 100-pixel square to 200 pixels (its target volume) after 200 MCS. For Node scripts, the manual says to load `build/artistoo-cjs.js` with `require`, then create `new CPM.Simulation(config)` and call `sim.run()`.

## Reading the output

The example is the default sorting run. Seed 1 gives a heterotypic fraction of 0.497 at the start and 0.225 after 3000 MCS. A drop from about 0.5 to 0.23 means that A and B cells now touch their own type most of the time. The Act default moves the cell 87.3 pixels in 1000 MCS.

The page's own code draws the lattice and measures sorting. Artistoo supplies the grid, the model (`CPM.CPM`), constraints (`getConstraint`) and the seeded random generator.

## Your own runs

Runs of the page's functions in Node used the same seed and defaults. Each line changes one input.

1. **No adhesion preference.** Set J different type to 10, equal to J same. The fraction stayed at 0.497 to 0.499. With equal energies the types stayed mixed.
2. **Hotter.** Set T to 60. The final fraction after 3000 MCS was 0.128, against 0.225 at T = 20. Sorting went further in the same time.
3. **Another seed.** Seed 2 started at 0.512 and ended at 0.193. Single runs vary, so use several seeds.
4. **Act strength.** In the Act model, LAMBDA_ACT of 0 moved the cell 1.9 pixels, 200 moved it 87.3 and 400 moved it 117.8.

## Pitfalls

- **Seed 0.** It picks a random seed, so the run cannot be reproduced. Use 1 or more.
- **One seed, one answer.** Sorting at seed 1 and seed 2 ended at 0.225 and 0.193. Run several seeds before you compare two parameter sets.
- **J values and T work together.** Sorting needs J different above J same. The T = 60 run sorted further than T = 20 with the same J, so change one at a time.
- **Cells that do not fit.** 80 cells of 100 pixels need a disc of about 101 pixels across. In a 120 grid, that passes the 90% check by a small margin.
- **No physical units.** Volume is in pixels, distance in pixels and time in MCS. Calibrate before you compare with an experiment.

## Further reading

- Artistoo site and examples: https://artistoo.net/
- Manual, first simulation: https://artistoo.net/manual/your-first-simulation.html
- Manual, getting started: https://artistoo.net/manual/getting-started.html
- Source: https://github.com/ingewortel/artistoo
- Wortel IMN, Textor J (2021). Artistoo, a library to build, share, and explore simulations of cells and tissues in the web browser. eLife 10:e61288. https://elifesciences.org/articles/61288
- Niculescu I, Textor J, de Boer RJ (2015). Crawling and gliding: a computational model for shape-driven cell migration. PLoS Comput Biol 11:e1004280. https://doi.org/10.1371/journal.pcbi.1004280

---

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/artistoo).
