# scDesign3

> Learn a copula model of single-cell data along a pseudotime trajectory and simulate a new count matrix, using the example data that ships with the package.

Licence: MIT · [Source code](https://github.com/SONGDONGYUAN1994/scDesign3)

## What it simulates

scDesign3 is an R package that learns a statistical model of a single-cell data set and then simulates a new one. It handles gene expression, chromatin accessibility, protein, methylation and spatial data, using cell states of three kinds: discrete cell types, continuous trajectories (pseudotime) and spatial coordinates.

The model has two parts. For each gene, a generalised additive model fits the marginal distribution (negative binomial, Poisson, zero-inflated versions, or Gaussian) as a smooth function of the cell covariates. A copula then ties the genes together, so the simulated genes keep the correlation seen in the reference. The default copula is Gaussian, and a vine copula is an option that the README warns is slow above about 1000 features.

The function `scdesign3()` returns a list. `new_count` is the synthetic count matrix. `new_covariate` holds new cell covariates when you ask for a different cell count. `model_aic` and `model_bic` score the marginal models, the copula and the total, which lets you compare model choices. Fitted models are returned only when `return_model = TRUE`.

Because the simulation starts from real data, scDesign3 is used to make realistic positive and negative controls: data that look like a reference but have a known structure.

## When to use it

Use scDesign3 when the benchmark data must look like a particular real data set, including gene correlation, a trajectory or tissue layout, and you want a goodness-of-fit score for the model.

- Use [Splatter](splatter.md) for a quick count matrix from a gamma-Poisson model with groups, batches or paths, and no reference data needed.
- Use [muscat](muscat.md) for multi-sample, multi-condition designs with known cluster-specific differential state genes.

The README notes that run time is quadratic in the number of features used in the copula. Cut the gene count to speed a run up.

## Install

scDesign3 is on Bioconductor. Release 3.23 lists scDesign3 1.10.0 (MIT licence, R 4.3 or later is listed under Depends).

```r
if (!require("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("scDesign3")
```

The GitHub README still shows `devtools::install_github("SONGDONGYUAN1994/scDesign3")` and says Bioconductor submission was in progress, so it is older than the Bioconductor listing.

Bioconda carries `bioconductor-scdesign3` 1.8.0 (Bioconductor 3.22, R 4.5). The recipe pins it:

```bash
conda create -n scdesign3 -c conda-forge -c bioconda bioconductor-scdesign3=1.8.0
```

Two dependencies, `r-coop` and `r-umap`, had no linux-aarch64 build in the Anaconda listing, so the recipe uses linux/amd64 (emulated on Arm). The README advises about 1 GB of memory per core when you set `n_cores`.

## A first run

Adapted from the [scDesign3 quickstart vignette](https://github.com/SONGDONGYUAN1994/scDesign3/blob/main/vignettes/scDesign3.Rmd), which models a pancreas data set with one pseudotime trajectory. The vignette keeps only the top 100 genes "to save computational time":

```r
library(scDesign3)
library(SingleCellExperiment)
data("example_count", package = "scDesign3")
data("pseudotime", package = "scDesign3")
example_sce <- SingleCellExperiment(
  assays = list(counts = example_count, logcounts = log1p(example_count)),
  colData = DataFrame(pseudotime = pseudotime))
set.seed(123)
example_simu <- scdesign3(
  sce = example_sce, assay_use = "counts", celltype = NULL,
  pseudotime = "pseudotime", mu_formula = "s(pseudotime, k = 10, bs = 'cr')",
  sigma_formula = "1", family_use = "nb", n_cores = 2,
  usebam = FALSE, corr_formula = "1", copula = "gaussian", DT = TRUE)
```

The data ship inside the package, so there is no input file. The recipe keeps the first 50 genes by default, runs on one core and writes the result to files.

## Run the tested example

This recipe builds scDesign3 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 19 s. scDesign3 has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [scdesign3-recipe.tar.gz](https://biosimhub.pages.dev/guides/scdesign3/scdesign3-recipe.tar.gz) (Dockerfile, run_scdesign3.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf scdesign3-recipe.tar.gz
   cd scdesign3
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/scdesign3:1.8.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/scdesign3:1.8.0 Rscript /opt/run_scdesign3.R --genes 50 --k 10 \
    --family nb --seed 42 > out/scdesign3_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `pseudotime.csv` | 75.5 KB |
| `scdesign3_log.txt` | 336 B |
| `simulated_counts_sparse.csv` | 1.8 MB |

<details><summary>First lines of <code>pseudotime.csv</code></summary>

```
"cell","pseudotime"
"AAACCTGAGAGGGATA",0.677236481670882
"AAACCTGGTAAGTGGC",0.431568681533416
"AAACGGGCAAAGAATC",0.749373139424365
"AAACGGGGTACAGTTC",0.92544064992522
"AAACGGGGTGAAATCA",0.38034515145602
"AAACGGGTCAAACAAG",0.256324605282185
"AAACGGGTCAGCTCTC",0.0293945637976826
"AAACGGGTCCGCGCAA",0.688434320994249
"AAACGGGTCGCATGGC",0.839083814470048
"AAAGATGAGAGTACCG",0.638239817030204
"AAAGATGAGTCATGCT",0.915115334313608
```

</details>

<details><summary>First lines of <code>scdesign3_log.txt</code></summary>

```
reference: 50 genes x 2087 cells
simulated: 50 genes x 2087 cells, family=nb, k=10, seed=42
zero fraction, reference 0.386, simulated 0.368
AIC/BIC (marginals, copula, total):
aic.marginal   aic.copula    aic.total 
  429443.491    -4200.243   425243.248 
bic.marginal   bic.copula    bic.total 
  432226.470     2713.024   434939.493 
```

</details>

<details><summary>First lines of <code>simulated_counts_sparse.csv</code></summary>

```
"gene","cell","count"
"Pyy","AAACCTGAGAGGGATA",115
"Iapp","AAACCTGAGAGGGATA",3
"Chgb","AAACCTGAGAGGGATA",37
"Rbp4","AAACCTGAGAGGGATA",15
"Spp1","AAACCTGAGAGGGATA",1
"Chga","AAACCTGAGAGGGATA",5
"Cck","AAACCTGAGAGGGATA",11
"Nnat","AAACCTGAGAGGGATA",1
"Neurog3","AAACCTGAGAGGGATA",1
"Tmsb4x","AAACCTGAGAGGGATA",8
"Xist","AAACCTGAGAGGGATA",6
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--genes` | Genes to model (Run time grows with the square of the gene count.) | 50 | 10 to 200 |
| `--k` | Spline basis size for the mean | 10 | 4 to 20 |
| `--family` | Marginal distribution | nb | nb, poisson, zinb, zip |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `simulated_counts_sparse.csv` has one row per non-zero count (gene, cell, count). The cells are the reference cells, in the same order, because the run does not change the cell number.
- `pseudotime.csv` lists the pseudotime of each cell, which is the covariate the model was fitted on.
- `scdesign3_log.txt` prints the reference and simulated dimensions, the fraction of zeros in each, and the AIC and BIC vectors.

The vignette checks the result with `dim(example_simu$new_count)`, which matches the input, and with a UMAP comparison from `plot_reduceddim()`. Do the same on your data. The simulated zero fraction should be near the reference, and a UMAP coloured by pseudotime should show the same trajectory shape.

## Pitfalls

- **Cost grows with the square of the gene count.** Start with 50 to 100 genes, as the vignette does.
- **`sigma_formula` costs time.** The vignette comment says letting dispersion vary along pseudotime "will significantly increase the computational cost".
- **`DT = TRUE` suits discrete families.** The distributional transformation makes counts continuous. For Gaussian data it should be off.
- **Match the covariates to the question.** Cell types, pseudotime and spatial coordinates enter the formulas through the `colData` columns you name.
- **Parallel code is built for Unix.** The README says parallel computing is mainly for UNIX operating systems. Balance `n_cores` against memory.
- **Same seed, same input.** Call `set.seed` before `scdesign3`, as the recipe does.

## Further reading

- Quickstart vignette: https://github.com/SONGDONGYUAN1994/scDesign3/blob/main/vignettes/scDesign3.Rmd
- Tutorials site: https://songdongyuan1994.github.io/scDesign3/docs/index.html
- Bioconductor page: https://bioconductor.org/packages/scDesign3
- Paper: Song D, Wang Q, Yan G, et al. (2024). scDesign3 generates realistic in silico data for multimodal single-cell and spatial omics. Nature Biotechnology 42:247-252. https://doi.org/10.1038/s41587-023-01772-1

---

Cite: Song D, Wang Q, Yan G, et al. (2024). scDesign3 generates realistic in silico data for multimodal single-cell and spatial omics. Nature Biotechnology 42:247-252. doi:10.1038/s41587-023-01772-1

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/scdesign3).
