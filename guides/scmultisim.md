# scMultiSim

> Simulate paired single-cell RNA and ATAC counts, optionally with RNA velocity, from a cell differentiation tree and a gene regulatory network.

Licence: Artistic-2.0 · [Source code](https://github.com/ZhangLabGT/scMultiSim)

## What it simulates

scMultiSim simulates multi-modal single-cell data: gene expression (RNA counts), chromatin accessibility (ATAC counts), RNA velocity, and optionally the spatial location of cells. It takes a cell differentiation tree and, optionally, a gene regulatory network (GRN). It produces spliced and unspliced counts while accounting for the relation between the modalities.

The README says the expression of a gene is set by three factors: cell-cell interactions, the within-cell GRN and chromatin accessibility. You tune how strongly each one acts. The differentiation tree controls the cell population. Each node is a cell type and connected nodes are differentiation steps. A continuous population gives a trajectory, and a discrete population gives clusters at the tips.

Technical effects are added in a second step: a function adds sequencing noise to the true counts and another divides cells into batches with a batch effect.

Key assumptions: the tree and GRN are inputs and are not inferred, and each cell carries latent factors (CIFs) that the tree structures.

## When to use it

Use scMultiSim to benchmark methods that need ground truth across modalities: GRN inference, RNA velocity, multi-omics integration, batch correction, or cell-cell interaction analysis.

- Use [SERGIO](sergio.md) when you only need RNA with a fixed GRN and per-cell-type regulator rates.
- Use [dyngen](dyngen.md) when you want a mechanistic trajectory with pre-mRNA, mRNA and protein counts.
- Use Splatter (https://github.com/Oshlack/splatter) for RNA counts that match a real dataset's statistics, with no regulatory model.

## Install

scMultiSim is on Bioconductor under the Artistic-2.0 licence. The current Bioconductor release lists version 1.8.0, which needs R 4.4 or later:

```r
if (!require("BiocManager")) install.packages("BiocManager")
BiocManager::install("scMultiSim")
```

Bioconda carries an older build, `bioconductor-scmultisim` 1.6.0 (noarch, built for R 4.5 and Bioconductor 3.22):

```bash
conda create -n scmultisim -c conda-forge -c bioconda bioconductor-scmultisim=1.6.0
```

The recipe on this page uses the Bioconda build, so its behaviour can differ slightly from the 1.8.0 documentation.

## A first run

Adapted from the Basics vignette (https://zhanglabgt.github.io/scMultiSim/articles/basics.html). The code has not been run for this guide.

```r
library(scMultiSim)
data(GRN_params_100)

options <- list(
  rand.seed = 0,
  GRN = GRN_params_100,
  num.cells = 1000,
  num.cifs = 50,
  cif.sigma = 0.5,
  tree = Phyla5(),
  diff.cif.fraction = 0.8,
  do.velocity = TRUE
)
results <- sim_true_counts(options)
add_expr_noise(results, alpha_mean = 1e4)
divide_batches(results, nbatch = 2, effect = 1)
```

`scmultisim_help("options")` documents every option, and `run_shiny()` opens an app for exploring them. The vignette says the 100-gene network gains 10 percent unregulated genes, so the data has 110 genes.

The recipe below runs the same call with 200 cells and the 3-leaf tree and writes the matrices to CSV files. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds scMultiSim in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 43.6 s. scMultiSim has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [scmultisim-recipe.tar.gz](https://biosimhub.pages.dev/guides/scmultisim/scmultisim-recipe.tar.gz) (Dockerfile, run_scmultisim.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf scmultisim-recipe.tar.gz
   cd scmultisim
   sh run.sh
   ```

![Terminal recording of the scMultiSim example run](https://biosimhub.pages.dev/media/scmultisim/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/scmultisim:1.6.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/scmultisim:1.6.0 Rscript /opt/run_scmultisim.R phyla3 200 50 0.5 no no yes 42 > out/scmultisim_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `atac_counts.csv` | 710.1 KB |
| `cell_meta.csv` | 5.5 KB |
| `counts_observed.csv` | 82.9 KB |
| `counts_true.csv` | 62.7 KB |
| `scmultisim_log.txt` | 114 B |
| `summary.txt` | 57 B |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/scmultisim/result-dark.png"><img src="https://biosimhub.pages.dev/media/scmultisim/result.png" alt="Plot of the scMultiSim example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>atac_counts.csv</code></summary>

```
,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,V29,V30,V31,V32,V33,V34,V35,V36,V37,V38,V39,V40,V41,V42,V43,V44,V45,V46,V47,V48,V49,V50,V51,V52,
1,7.16965428850552,4.14844266982085,2.02107975796585,4.61567730673422,4.17545930684976,2.50798007918801,3.90187144463505,10.9287601341032,4.53638600730052,5.23262455955249,6.47373814390929,12.04006017
```

</details>

<details><summary>First lines of <code>cell_meta.csv</code></summary>

```
cell_id,pop,depth
cell1,4_5,0
cell2,4_5,0.0256410256410256
cell3,4_5,0.0512820512820513
cell4,4_5,0.0769230769230769
cell5,4_5,0.102564102564103
cell6,4_5,0.128205128205128
cell7,4_5,0.153846153846154
cell8,4_5,0.179487179487179
cell9,4_5,0.205128205128205
cell10,4_5,0.230769230769231
cell11,4_5,0.256410256410256
```

</details>

<details><summary>First lines of <code>counts_observed.csv</code></summary>

```
,V1,V2,V3,V4,V5,V6,V7,V8,V9,V10,V11,V12,V13,V14,V15,V16,V17,V18,V19,V20,V21,V22,V23,V24,V25,V26,V27,V28,V29,V30,V31,V32,V33,V34,V35,V36,V37,V38,V39,V40,V41,V42,V43,V44,V45,V46,V47,V48,V49,V50,V51,V52,
1,27364,9658,15756,11694,14030,20879,5778,15150,1071,8051,61,4883,10717,6566,5485,3622,7868,585,1708,7747,5609,11716,11100,3802,4330,3223,7799,9321,9250,0,9463,3591,5282,400,1329,7424,7625,7070,6683,5
2,48,334,199,325,384,704,826,217,701,350,1684,516,167,117,190,368,373,564,260,720,1290,385,270,104,167,330,220,197,41,82,288,40,114,107,82,181,6,66,164,226,68,11,152,90,75,64,132,174,282,79,158,104,13
```

</details>

<details><summary>First lines of <code>counts_true.csv</code></summary>

```
,cell1,cell2,cell3,cell4,cell5,cell6,cell7,cell8,cell9,cell10,cell11,cell12,cell13,cell14,cell15,cell16,cell17,cell18,cell19,cell20,cell21,cell22,cell23,cell24,cell25,cell26,cell27,cell28,cell29,cell3
1,320,66,122,94,106,171,49,160,6,107,1,54,154,150,136,38,120,5,23,94,82,157,125,55,53,38,107,122,146,0,141,42,81,2,14,101,134,111,77,67,112,133,119,75,12,121,86,104,127,107,74,3,137,60,28,56,117,85,53
2,3,14,9,13,18,29,35,12,29,25,73,20,16,13,23,22,32,34,27,58,110,37,21,6,14,28,17,9,5,7,20,5,9,5,7,14,1,4,6,15,8,2,13,11,4,7,13,10,14,6,18,8,12,18,5,3,5,5,1,6,4,10,9,16,13,24,6,9,16,5,4,8,4,5,21,3,7,5,
```

</details>

<details><summary>First lines of <code>scmultisim_log.txt</code></summary>

```
Time spent: 0.02 mins
Adding experimental noise...
50..100..150..200..Using atac_counts
done 110 genes, 200 cells
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
seed 42
tree phyla3
genes 110
cells 200
atac_regions 330
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `tree` | Differentiation tree | phyla3 | phyla1, phyla3, phyla5 |
| `cells` | Cells | 200 | 50 to 1000 |
| `cifs` | Cell identity factors (CIFs) | 50 | 20 to 100 |
| `cif_sigma` | CIF variance (low gives a clear trajectory) | 0.5 | 0.1 to 1 |
| `discrete` | Discrete cell populations | no | no, yes |
| `velocity` | Simulate unspliced counts and RNA velocity | no | no, yes |
| `technical_noise` | Add technical noise to the RNA counts | yes | yes, no |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

`sim_true_counts` returns an environment object. The vignette lists its fields, and the recipe writes these:

- `counts_true.csv`: the true gene-by-cell RNA counts.
- `counts_observed.csv`: the same after `add_expr_noise`, written when technical noise is on.
- `atac_counts.csv`: region-by-cell ATAC counts. A region-to-gene matrix in the object links regions to genes.
- `cell_meta.csv`: a cell type label (`pop`) and pseudotime for each cell.
- `unspliced_counts.csv` and `velocity.csv`: the unspliced counts and the ground-truth RNA velocity, written when velocity is on.
- `summary.txt`: seed, tree, and the numbers of genes, cells and ATAC regions.

The vignette checks the result with a t-SNE plot of `log2(counts + 1)` coloured by `cell_meta$pop`. A clear trajectory or well-separated clusters means the tree's effect dominates.

## Pitfalls

- **Trajectory clarity depends on `cif.sigma`.** The vignette says 0.1 gives a very clear trajectory and 1 a noisy one.
- **`diff.cif.fraction` sets the tree's weight.** A larger value gives a clearer structure. A smaller value lets the GRN and other effects dominate.
- **`num.cifs` should scale with genes.** The default is 50. The vignette advises 50 to 100 for more than 2000 genes and 20 to 40 for fewer than 1000.
- **No GRN is allowed.** Set `GRN = NA` and give `num.genes` instead.
- **Run time grows with options.** The README FAQ reports about one minute for 1000 cells, 100 genes and 50 CIFs with RNA and ATAC on an i7-12700K, about 3 minutes with RNA velocity, and about 30 minutes for 500 cells with spatial cell-cell interaction.
- **Noise functions modify the object.** `add_expr_noise` adds `counts_obs` and `divide_batches` adds `counts_with_batches` in place.
- **Version drift.** Option names in the website documentation follow the current release.

## Further reading

- Source: https://github.com/ZhangLabGT/scMultiSim
- Documentation and tutorials: https://zhanglabgt.github.io/scMultiSim/articles
- Li H, Zhang Z, Squires M, Chen X, Zhang X (2025). scMultiSim: simulation of single-cell multi-omics and spatial data guided by gene regulatory networks and cell-cell interactions. Nature Methods 22:982-993. https://doi.org/10.1038/s41592-025-02651-0

---

Cite: Li H, Zhang Z, Squires M, Chen X, Zhang X (2025). scMultiSim: simulation of single-cell multi-omics and spatial data guided by gene regulatory networks and cell-cell interactions. Nature Methods 22:982-993. doi:10.1038/s41592-025-02651-0

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/scmultisim).
