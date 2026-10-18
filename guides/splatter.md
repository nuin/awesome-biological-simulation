# Splatter

> Simulate scRNA-seq count matrices with the Splat gamma-Poisson model, with optional cell groups, differential expression and dropout.

Licence: GPL-3.0-only · [Source code](https://github.com/Oshlack/splatter)

## What it simulates

Splatter is an R package that simulates single-cell RNA-seq counts. Its own model is called Splat, a gamma-Poisson model. Mean expression of each gene comes from a gamma distribution. The biological coefficient of variation (BCV) sets a mean-variance trend. Counts are then drawn from a Poisson distribution. Each cell gets an expected library size from a log-normal distribution.

Options layered on top:

- **Expression outliers:** genes whose mean lies outside the gamma distribution.
- **Dropout:** random zeros whose chance falls as mean expression rises.
- **Groups:** cell types that differ in a share of genes (`de.prob`, `group.prob`).
- **Paths:** a continuous change from one cell type to another, with each cell at a random step.
- **Batches:** a technical effect on all genes, set through the number of cells per batch (`batchCells`).

Parameters live in a `SplatParams` object. You can set them by hand with `setParam`, or estimate them from a count matrix with `splatEstimate`. The package also wraps other published simulators behind the same interface (`listSims()` lists them; the vignette names the Simple and Lun 2 simulations), plus `splatPop` for population-scale data with eQTL effects.

The output is a `SingleCellExperiment`. Besides `counts`, it holds the intermediate matrices (`BaseCellMeans`, `BCV`, `CellMeans`, `TrueCounts`, `Dropout`), cell columns (`Cell`, `Batch`, `Group`, `ExpLibSize`) and gene columns (`BaseGeneMean`, `OutlierFactor`, `GeneMean`, `DEFac<Group>`).

## When to use it

Use Splatter for a fast, simple count matrix with a known number of groups, batches or a trajectory, for example to test a clustering, normalisation or batch-correction method.

- Use [muscat](muscat.md) when you need several biological samples per condition and cluster-specific differential state genes.
- Use [scDesign3](scdesign3.md) when the synthetic data should copy gene-gene correlation, a real trajectory or spatial layout from a reference.

Splat does not model gene-gene correlation. Genes are independent given the cell means.

## Install

Splatter is on Bioconductor. Release 3.23 lists Splatter 1.36.0 and needs R 4.6.

```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("splatter")
```

Bioconda carries `bioconductor-splatter` 1.34.0 (Bioconductor 3.22, R 4.5) as a noarch package, which the recipe pins:

```bash
conda create -n splatter -c conda-forge -c bioconda bioconductor-splatter=1.34.0
```

The package depends on scater, scuttle, edgeR and other Bioconductor packages. The recipe targets linux/amd64 (emulated on Arm), because the whole dependency tree was not checked for linux-aarch64. The GitHub repository is GPL-3.0.

## A first run

Adapted from the [Splatter vignette](https://github.com/Oshlack/splatter/blob/master/vignettes/splatter.Rmd). The vignette's quick start estimates parameters from a mock data set and simulates from them:

```r
library(splatter)
library(scater)
set.seed(1)
sce <- mockSCE()
params <- splatEstimate(sce)
sim <- splatSimulate(params)
```

The vignette's group example uses `splatSimulate(group.prob = c(0.5, 0.5), method = "groups")`. The recipe skips the estimate step and sets the parameters directly: 2000 genes, 300 cells in one batch, two equal groups, a 10% chance that a gene is differentially expressed, no dropout and a seed.

## Run the tested example

This recipe builds Splatter in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 11.9 s. Splatter has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [splatter-recipe.tar.gz](https://biosimhub.pages.dev/guides/splatter/splatter-recipe.tar.gz) (Dockerfile, run_splatter.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf splatter-recipe.tar.gz
   cd splatter
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/splatter:1.34.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/splatter:1.34.0 Rscript /opt/run_splatter.R --genes 2000 --cells 300 \
    --groups 2 --de-prob 0.1 --dropout none --seed 42 > out/splatter_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cells.csv` | 13.1 KB |
| `counts_sparse.csv` | 10.2 MB |
| `genes.csv` | 107.6 KB |
| `splatter_log.txt` | 117 B |

<details><summary>First lines of <code>cells.csv</code></summary>

```
"Cell","Batch","Group","ExpLibSize"
"Cell1","Batch1","Group1",59388.7625604673
"Cell2","Batch1","Group1",43900.9410709975
"Cell3","Batch1","Group2",75616.8113534845
"Cell4","Batch1","Group1",56685.3375756827
"Cell5","Batch1","Group1",54525.8911636491
"Cell6","Batch1","Group1",46739.7161165872
"Cell7","Batch1","Group1",59781.2648031468
"Cell8","Batch1","Group2",51018.4986419519
"Cell9","Batch1","Group1",53814.6779887676
"Cell10","Batch1","Group1",77461.4017325744
"Cell11","Batch1","Group2",57808.7152376132
```

</details>

<details><summary>First lines of <code>counts_sparse.csv</code></summary>

```
"gene","cell","count"
"Gene2","Cell1",14
"Gene3","Cell1",121
"Gene4","Cell1",48
"Gene5","Cell1",2
"Gene6","Cell1",24
"Gene7","Cell1",12
"Gene8","Cell1",5
"Gene9","Cell1",18
"Gene11","Cell1",4
"Gene13","Cell1",13
"Gene15","Cell1",5
```

</details>

<details><summary>First lines of <code>genes.csv</code></summary>

```
"Gene","BaseGeneMean","OutlierFactor","GeneMean","DEFacGroup1","DEFacGroup2"
"Gene1",0.0937860988361447,1,0.0937860988361447,1,1
"Gene2",1.01323282704636,1,1.01323282704636,1,1
"Gene3",1.67292839427455,21.9245851590685,22.9334183530245,1,1
"Gene4",7.43693422438815,1,7.43693422438815,1,1
"Gene5",0.353867871826092,1,0.353867871826092,1,1
"Gene6",4.14323952985981,1,4.14323952985981,1,1
"Gene7",0.872688054199918,1,0.872688054199918,1,1
"Gene8",1.21837578079792,1,1.21837578079792,1,1
"Gene9",3.02926726009219,1,3.02926726009219,1,1
"Gene10",0.00484216527118392,1,0.00484216527118392,1,1
"Gene11",0.436344458097965,1,0.436344458097965,1,1
```

</details>

<details><summary>First lines of <code>splatter_log.txt</code></summary>

```
genes=2000 cells=300 groups=2 seed=42
fraction of zero counts: 0.211
cells per group:

Group1 Group2 
   149    151 
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--genes` | Genes | 2000 | 100 to 10000 |
| `--cells` | Cells | 300 | 20 to 3000 |
| `--groups` | Cell groups | 2 | 1 to 6 |
| `--de-prob` | Probability a gene is differentially expressed | 0.1 | 0 to 1 |
| `--dropout` | Dropout type | none | none, experiment |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `counts_sparse.csv` has one row per non-zero count (gene, cell, count).
- `cells.csv` has `Cell`, `Batch`, `Group` and `ExpLibSize`. The group column shows which cells belong to which type.
- `genes.csv` has `BaseGeneMean`, `OutlierFactor`, `GeneMean` and one `DEFac` and `GeneMean` column per group. A `DEFac` of 1 means the gene is not differentially expressed.
- `splatter_log.txt` reports the sizes, the share of zero counts and the cells per group.

Sanity checks: cells per group should be close to equal at `group.prob` of 0.5 each, and about 10% of genes should have a `DEFac` different from 1 in a group. The vignette says two groups at 0.5 each give "around 50" cells per group in its default example. A higher dropout setting raises the share of zeros.

## Pitfalls

- **Cell count is set through batches.** The parameter docs say `nCells` cannot be set directly. It is the sum of `batchCells`, which the recipe sets to one batch.
- **Size grows with genes times cells.** The recipe holds a dense matrix before it writes sparse triplets, so its limits are 10,000 genes and 3,000 cells.
- **Group probabilities must sum to 1.** The recipe divides evenly between groups.
- **Seeds are a parameter.** `seed` is part of the parameter object. Pass it to `splatSimulate` as the recipe does.
- **Dropout is off in the recipe by default.** Turn it on with `dropout.type = "experiment"` to see zeros that depend on mean expression.
- **Estimation starts from counts.** The vignette checks that the matrix is an integer count matrix before calling `splatEstimate`.
- **Version drift.** GitHub tracks the newest development version. Check `?splatSimulate` in your installed version.

## Further reading

- Vignette: https://github.com/Oshlack/splatter/blob/master/vignettes/splatter.Rmd
- Splat parameters: https://github.com/Oshlack/splatter/blob/master/vignettes/splat_params.Rmd
- Bioconductor page: https://bioconductor.org/packages/splatter
- Paper: Zappia L, Phipson B, Oshlack A (2017). Splatter: simulation of single-cell RNA sequencing data. Genome Biology 18:174. https://doi.org/10.1186/s13059-017-1305-0

---

Cite: Zappia L, Phipson B, Oshlack A (2017). Splatter: simulation of single-cell RNA sequencing data. Genome Biology 18:174. doi:10.1186/s13059-017-1305-0

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/splatter).
