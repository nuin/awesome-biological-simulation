# dyngen

> Simulate single-cell RNA-seq data from gene regulatory network dynamics along a chosen cell trajectory (linear, bifurcating, cycle and others).

Licence: MIT · [Source code](https://github.com/dynverse/dyngen)

## What it simulates

dyngen simulates single-cell RNA-seq data from the dynamics of a gene regulatory network along a cell trajectory. You pick a backbone, which is a set of gene modules that regulate each other so that expression changes over time in a set pattern: linear, bifurcating, cyclic, converging and others. dyngen builds transcription factors for each module, samples target and housekeeping genes from a real regulatory network, and generates reaction kinetics.

It then simulates cells in two stages. A gold-standard run follows the backbone with ordinary differential equations. Stochastic simulations (Gillespie-type SSA) then produce single cells, each with pre-mRNA, mRNA and protein molecule counts. A final step samples counts the way a real experiment would, using a real count matrix as the reference for library size and expression distribution.

Key assumptions: the trajectory shape comes from the backbone you choose, regulation follows the generated kinetics, and the cell sampling mimics one snapshot or time-series experiment. Unlike a statistical simulator, the true gene network and the true position of every cell on the trajectory are known.

## When to use it

Use dyngen to benchmark trajectory-inference, RNA-velocity or GRN-inference methods, because the ground truth for the trajectory, the network and spliced versus unspliced counts is stored with the data.

- Use [SERGIO](sergio.md) when you already have a specific network and want to control each master regulator's rate per cell type.
- Use [scMultiSim](scmultisim.md) when you also need chromatin accessibility or spatial cell-cell interaction.
- Use Splatter (https://github.com/Oshlack/splatter) for fast count data with no network or trajectory model.

## Install

dyngen is on CRAN. The current release is 1.1.1 (published 2026-04-01), licensed MIT, and it needs R 4.1 or later. The README says it should work straight from CRAN:

```r
install.packages("dyngen")
```

The installation vignette recommends two settings for speed. Put them in your `.Rprofile`:

```r
options(Ncpus = 8L)  # number of cores
options(dyngen_download_cache_dir = tools::R_user_dir("dyngen", "data"))
```

dyngen downloads reference networks and real count matrices from GitHub the first time it needs them and caches them in that folder. The vignette also shows how to download all of them in advance from `https://github.com/dynverse/dyngen/archive/data_files.zip`.

## A first run

Adapted from the Getting started vignette (https://dyngen.dynverse.org/articles/getting_started.html). The code below has not been run for this guide. The vignette runs the steps one by one:

```r
library(dyngen)
set.seed(1)
backbone <- backbone_bifurcating()
config <- initialise_model(
  backbone = backbone,
  num_cells = 1000,
  num_tfs = nrow(backbone$module_info),
  num_targets = 50,
  num_hks = 50,
  verbose = FALSE,
  download_cache_dir = tools::R_user_dir("dyngen", "data"),
  simulation_params = simulation_default(
    total_time = 1000,
    census_interval = 2,
    ssa_algorithm = ssa_etl(tau = 300 / 3600),
    experiment_params = simulation_type_wild_type(num_simulations = 10)
  )
)
model <- generate_tf_network(config)
model <- generate_feature_network(model)
model <- generate_kinetics(model)
model <- generate_gold_standard(model)
model <- generate_cells(model)
model <- generate_experiment(model)
```

`generate_dataset(config, format = "list")` runs all of these in one call. The vignette also lists `"dyno"`, `"sce"`, `"seurat"` and `"anndata"` as output formats.

The recipe below runs the one-shot call with 200 cells, 30 target genes and 30 housekeeping genes. Its image caches the GitHub data files at build time because the sandbox has no network. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds dyngen in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 67.3 s. dyngen has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [dyngen-recipe.tar.gz](https://biosimhub.pages.dev/guides/dyngen/dyngen-recipe.tar.gz) (Dockerfile, run_dyngen.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf dyngen-recipe.tar.gz
   cd dyngen
   sh run.sh
   ```

![Terminal recording of the dyngen example run](https://biosimhub.pages.dev/media/dyngen/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/dyngen:1.1.1 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/dyngen:1.1.1 Rscript /opt/run_dyngen.R bifurcating 200 30 30 8 1000 42 > out/dyngen_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cell_info.csv` | 5.9 KB |
| `counts_spliced.csv` | 68.4 KB |
| `counts_unspliced.csv` | 55.4 KB |
| `dyngen_log.txt` | 29 B |
| `feature_info.csv` | 2.0 KB |
| `milestone_network.csv` | 208 B |
| `progressions.csv` | 6.4 KB |
| `summary.txt` | 69 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/dyngen/result-dark.png"><img src="https://biosimhub.pages.dev/media/dyngen/result.png" alt="Plot of the dyngen example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>cell_info.csv</code></summary>

```
cell_id,step_ix,simulation_i,sim_time
cell1,2440,5,140.083333333332
cell2,2445,5,150.083333333333
cell3,2494,5,248.000000000011
cell4,3236,6,584.08333333332
cell5,3367,6,846.000000000105
cell6,1225,3,6.08333333333333
cell7,2982,6,76
cell8,3519,7,2.08333333333333
cell9,3542,7,48.0000000000003
cell10,3366,6,844.000000000104
cell11,1954,4,316.083333333331
```

</details>

<details><summary>First lines of <code>counts_spliced.csv</code></summary>

```
,Burn1_TF1,Burn2_TF1,Burn3_TF1,Burn4_TF1,A1_TF1,A2_TF1,A3_TF1,A4_TF1,B1_TF1,B2_TF1,B3_TF1,B4_TF1,B5_TF1,B6_TF1,B7_TF1,B8_TF1,B9_TF1,B10_TF1,B11_TF1,B12_TF1,B13_TF1,B14_TF1,C1_TF1,C2_TF1,C3_TF1,C4_TF1,
cell1,40,10730,3485,2055,172,407,49,164,2415,2,6,3932,1812,0,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,7,0,0,0,0,871,2902,0,5,1613,0,0,5884,0,0,17,8713,1888,590,9,685,10242,19,0,0,3620,13,19179,184,0,1593
cell2,99,11611,8839,1055,79,121,10,1174,4516,6,5,385,40,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1307,3263,0,3,1179,0,0,5099,0,0,149,4925,2314,3386,5,680,7163,476,0,0,5229,0,14575,44,5,2683,7
cell3,77,14939,8304,2345,643,622,13,517,5331,8,11,2774,0,0,36,10,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1508,3358,0,4,2097,0,0,7104,0,0,63,8232,3059,299,0,422,18329,1962,0,0,13594,0,14955,1176,9,
cell4,43,12653,6340,924,163,1052,24,955,4470,18,0,0,1086,3658,0,1255,33,174,52,0,0,0,4971,26,14,31,0,0,0,0,0,0,0,0,0,1887,44,88,1855,3094,0,0,14,0,9301,8,393,1042,35,4230,3391,54,8,991,34282,16,6751,1
cell5,156,20944,11333,987,77,681,22,40,6793,53,0,0,161,1322,0,1276,1471,375,42,0,0,0,14820,133,25,166,0,0,0,0,0,0,0,0,0,186,456,50,571,4415,0,0,20,0,6445,13,2472,3198,95,9296,5050,484,0,3550,1547
```

</details>

<details><summary>First lines of <code>counts_unspliced.csv</code></summary>

```
,Burn1_TF1,Burn2_TF1,Burn3_TF1,Burn4_TF1,A1_TF1,A2_TF1,A3_TF1,A4_TF1,B1_TF1,B2_TF1,B3_TF1,B4_TF1,B5_TF1,B6_TF1,B7_TF1,B8_TF1,B9_TF1,B10_TF1,B11_TF1,B12_TF1,B13_TF1,B14_TF1,C1_TF1,C2_TF1,C3_TF1,C4_TF1,
cell1,48,685,950,9,60,14,8,12,131,9,4,23,93,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,607,0,0,34,0,0,213,0,0,111,664,87,9,0,19,2035,3,0,0,322,5,2009,76,0,23,235,775,752,138,172,229,14,555,77
cell2,11,951,48,43,20,11,12,6,75,4,11,4,10,0,6,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,18,527,0,0,41,0,0,199,0,0,67,963,128,5,0,40,633,5,0,0,960,3,1728,50,9,130,1356,521,1402,23,1113,312,10,107,
cell3,7,1240,277,26,64,72,12,82,44,0,20,24,10,0,13,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,11,1047,0,0,92,0,0,1435,0,0,23,153,523,13,5,73,327,23,0,0,1384,0,1076,13,4,19,1198,2638,45,29,882,143,1
cell4,55,1785,265,26,8,35,13,16,465,20,0,0,388,114,0,61,44,16,25,0,0,0,63,35,15,28,0,0,0,0,0,0,0,0,0,18,53,20,44,548,0,0,18,0,167,0,58,21,82,671,87,14,0,30,250,0,398,118,0,205,0,57,0,32,488,673,156,45
cell5,30,167,120,28,13,35,16,97,126,23,0,0,54,81,0,185,28,18,28,0,0,0,252,25,11,29,0,0,0,0,0,0,0,0,0,44,17,25,23,1285,0,0,24,0,53,0,185,26,35,48,151,41,11,25,972,0,327,1144,11,234,0,100,0,40,334,
```

</details>

<details><summary>First lines of <code>dyngen_log.txt</code></summary>

```

done 200 cells, 92 features
```

</details>

<details><summary>First lines of <code>feature_info.csv</code></summary>

```
feature_id,module_id,is_tf,is_hk
Burn1_TF1,Burn1,TRUE,FALSE
Burn2_TF1,Burn2,TRUE,FALSE
Burn3_TF1,Burn3,TRUE,FALSE
Burn4_TF1,Burn4,TRUE,FALSE
A1_TF1,A1,TRUE,FALSE
A2_TF1,A2,TRUE,FALSE
A3_TF1,A3,TRUE,FALSE
A4_TF1,A4,TRUE,FALSE
B1_TF1,B1,TRUE,FALSE
B2_TF1,B2,TRUE,FALSE
B3_TF1,B3,TRUE,FALSE
```

</details>

<details><summary>First lines of <code>milestone_network.csv</code></summary>

```
from,to,length,directed
sA,sB,1.03151862464183,TRUE
sB,sBmid,0.343839541547278,TRUE
sBmid,sC,1.03151862464183,TRUE
sBmid,sD,1.03151862464183,TRUE
sC,sEndC,1.02292263610315,TRUE
sD,sEndD,1.53868194842407,TRUE
```

</details>

<details><summary>First lines of <code>progressions.csv</code></summary>

```
cell_id,from,to,percentage
cell1,sB,sBmid,0.701739850869925
cell2,sBmid,sC,0.125658914728628
cell3,sBmid,sD,0.298774487878907
cell4,sC,sEndC,0.676277187657925
cell5,sC,sEndC,0.959534648457241
cell6,sA,sB,0.0874197514000869
cell7,sB,sBmid,0.392433029549848
cell8,sA,sB,0
cell9,sA,sB,0.765059418112282
cell10,sC,sEndC,0.955199075077659
cell11,sD,sEndD,0.207789743346448
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
backbone bifurcating
seed 42
cells 200
features 92
milestone_edges 6
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `backbone` | Trajectory backbone | bifurcating | linear, bifurcating, cycle, converging, trifurcating |
| `cells` | Cells | 200 | 20 to 1000 |
| `targets` | Target genes | 30 | 0 to 500 |
| `housekeeping` | Housekeeping genes | 30 | 0 to 500 |
| `simulations` | Simulated cell paths | 8 | 1 to 20 |
| `total_time` | Simulation time per path | 1000 | 100 to 3000 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe writes plain CSV files from the one-shot list output:

- `counts_spliced.csv` and `counts_unspliced.csv` have one row per cell and one column per feature. They hold the mRNA and pre-mRNA counts after the experiment step.
- `cell_info.csv` has one row per cell with its `cell_id` and the simulation step it was sampled from (`step_ix`).
- `progressions.csv` places each cell on the backbone: the `from` and `to` milestones and the `percentage` of the way along that edge.
- `feature_info.csv` lists each gene, its module, and whether it is a transcription factor or a housekeeping gene.
- `milestone_network.csv` is the ground-truth trajectory: the edges between milestones.
- `summary.txt` repeats the backbone, seed and sizes.

The number of features is the transcription factors that the backbone defines plus the target and housekeeping genes you asked for. Check that cells spread along every edge of the milestone network. If they do not, raise the number of simulated paths or the simulation time.

## Pitfalls

- **First use needs the internet.** Without the cached data files the model fails with "Cannot download file". Cache them first.
- **Enough simulated cells.** `floor(total_time / census_interval) * num_simulations` should be well above `num_cells`. dyngen warns when it is not and suggests a ratio above 10.
- **Seeds.** Call `set.seed()` before `initialise_model()`. The simulation seeds in `simulation_type_wild_type()` are drawn from the R generator by default.
- **Runtime scales with cells, genes and time.** The vignette shortens the run by lowering genes, simulation time and the number of paths.
- **Optional packages.** Converting to `dyno`, `Seurat`, `SingleCellExperiment` or `anndata` objects needs those packages, which are only suggested.
- **Backbone names.** `list_backbones()` shows every built-in backbone. The recipe offers five.

## Further reading

- Package site: https://dyngen.dynverse.org
- Source: https://github.com/dynverse/dyngen
- Cannoodt R, Saelens W, Deconinck L, Saeys Y (2021). Spearheading future omics analyses using dyngen, a multi-modal simulator of single cells. Nature Communications 12:3942. https://doi.org/10.1038/s41467-021-24152-2

---

Cite: Cannoodt R, Saelens W, Deconinck L, Saeys Y (2021). Spearheading future omics analyses using dyngen, a multi-modal simulator of single cells. Nature Communications 12:3942. doi:10.1038/s41467-021-24152-2

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/dyngen).
