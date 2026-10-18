# muscat (simData)

> Simulate multi-sample, multi-condition scRNA-seq counts with cluster-specific differential-state genes, anchored to a reference data set that ships with the package.

Licence: GPL-3.0-only · [Source code](https://github.com/HelenaLC/muscat)

## What it simulates

muscat is an R package for differential state analysis in single-cell RNA-seq with many samples, conditions and cell subpopulations. Its `simData` function is the simulator. It fits a negative binomial model to a real reference data set (dispersion, sample-specific means, library sizes), then samples new counts from that model with changes you choose.

You pick the number of genes, cells, subpopulations (clusters) and samples, and the share of genes in each differential distribution category: EE (equal expression), EP (equal proportions), DE (differential expression), DP (differential proportions), DM (differential modality) and DB (both). Fold changes are drawn from a gamma distribution around a mean log2 fold change you set (`lfc`). A per-cluster factor (`rel_lfc`) lets some clusters change more than others or not at all. "Type" genes (`p_type`, or a `phylo_tree`) make clusters separable.

The output is a `SingleCellExperiment` with counts, cell metadata (cluster, sample, group), and a gene table in `metadata(sim)$gene_info` that lists, for each gene and cluster, its category, log fold change and simulated means in groups A and B. The truth is therefore stored with the data.

## When to use it

Use muscat to build test data for pseudobulk or mixed-model differential state methods, where the question is "which genes change in which cell type between conditions, across biological replicates". Samples are a first-class part of the design, which matters for avoiding pseudoreplication.

- Use [Splatter](splatter.md) for a simple gamma-Poisson model of one or several cell groups, estimated from a count matrix of your own.
- Use [scDesign3](scdesign3.md) when you need gene-gene correlation, trajectories or spatial coordinates learned from a real data set.

## Install

muscat is on Bioconductor (release 3.23 lists muscat 1.26.0, which needs R 4.6):

```r
if (!requireNamespace("BiocManager", quietly = TRUE))
    install.packages("BiocManager")
BiocManager::install("muscat")
```

Bioconda carries `bioconductor-muscat` 1.24.0 (Bioconductor 3.22, R 4.5) as a noarch package. The recipe pins that:

```bash
conda create -n muscat -c conda-forge -c bioconda bioconductor-muscat=1.24.0
```

Package dependencies include edgeR, limma, scater, glmmTMB, lme4 and variancePartition. The recipe runs on linux/amd64 (emulated on Arm), since not every R dependency was checked for linux-aarch64.

## A first run

Adapted from the [muscat simulation vignette](https://github.com/HelenaLC/muscat/blob/main/vignettes/simulation.Rmd), which prepares the reference with `prepSim` and then calls `simData`:

```r
library(muscat)
data(example_sce)
ref <- prepSim(example_sce, verbose = FALSE)
sim <- simData(ref, nc = 2e3, ng = 1e3, force = TRUE,
    p_dd = diag(6)[1, ], nk = 3, ns = 3)
table(sim$sample_id, sim$cluster_id)
```

`example_sce` ships with the package, so no input file is needed. The recipe wraps the same calls in `run_muscat.R` with a seed, `p_dd = c(1 - p_de, 0, p_de, 0, 0, 0)` (so only EE and DE genes) and `force = TRUE`, which the package requires when the gene count differs from the reference.

## Run the tested example

This recipe builds muscat (simData) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 20.1 s. muscat (simData) has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [muscat-recipe.tar.gz](https://biosimhub.pages.dev/guides/muscat/muscat-recipe.tar.gz) (Dockerfile, run_muscat.R, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf muscat-recipe.tar.gz
   cd muscat
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/muscat:1.24.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/muscat:1.24.0 Rscript /opt/run_muscat.R --cells 1000 --genes 500 \
    --clusters 3 --samples 3 --p-de 0.1 --lfc 2 \
    --seed 42 > out/muscat_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `cells.csv` | 36.1 KB |
| `counts_sparse.csv` | 4.2 MB |
| `gene_info.csv` | 136.1 KB |
| `muscat_log.txt` | 462 B |

<details><summary>First lines of <code>cells.csv</code></summary>

```
"","cluster_id","sample_id","group_id"
"cell1","cluster1","sample1.B","B"
"cell2","cluster3","sample3.B","B"
"cell3","cluster1","sample3.B","B"
"cell4","cluster1","sample2.A","A"
"cell5","cluster2","sample2.A","A"
"cell6","cluster3","sample2.B","B"
"cell7","cluster1","sample1.A","A"
"cell8","cluster1","sample2.B","B"
"cell9","cluster2","sample2.A","A"
"cell10","cluster3","sample1.A","A"
"cell11","cluster3","sample2.A","A"
```

</details>

<details><summary>First lines of <code>counts_sparse.csv</code></summary>

```
"gene","cell","count"
"gene4","cell1",1
"gene8","cell1",45
"gene9","cell1",6
"gene10","cell1",2
"gene13","cell1",8
"gene16","cell1",2
"gene17","cell1",9
"gene19","cell1",1
"gene22","cell1",1
"gene23","cell1",1
"gene26","cell1",51
```

</details>

<details><summary>First lines of <code>gene_info.csv</code></summary>

```
"gene","cluster_id","category","logFC","sim_gene","sim_disp","sim_mean.A","sim_mean.B"
"gene1","cluster1","ee",NA,"PSMB1",0.441916018356905,0.750780792763995,0.859112842278173
"gene1","cluster2","ee",NA,"PSMB1",0.441916018356905,0.773252783795242,0.890384865886171
"gene1","cluster3","ee",NA,"PSMB1",0.441916018356905,0.784744184015088,0.851609183919217
"gene2","cluster1","ee",NA,"PNRC1",1.00356917496754,0.728495742130542,0.833612225620766
"gene2","cluster2","ee",NA,"PNRC1",1.00356917496754,0.750300708295419,0.86395601739834
"gene2","cluster3","ee",NA,"PNRC1",1.00356917496754,0.761451015032032,0.826331294598573
"gene3","cluster1","ee",NA,"ATP5J",0.138206533040691,0.497834750137586,0.56966857876183
"gene3","cluster2","ee",NA,"ATP5J",0.138206533040691,0.512735688131682,0.590404724663845
"gene3","cluster3","de",2.8604917647384,"ATP5J",0.138206533040691,0.508051356416957,3.99755762530673
"gene4","cluster1","ee",NA,"BSG",0.595223444717179,0.289918975065095,0.331752113398622
"gene4","cluster2","ee",NA,"BSG",0.595223444717179,0.298596683219383,0.34382801240939
```

</details>

<details><summary>First lines of <code>muscat_log.txt</code></summary>

```
genes=500 cells=1000 clusters=3 samples=3 seed=42
cells per sample and cluster:
           
            cluster1 cluster2 cluster3
  sample1.A       58       47       67
  sample2.A       55       66       64
  sample3.A       49       54       45
  sample1.B       61       66       51
  sample2.B       50       57       54
  sample3.B       51       57       48
gene categories (gene x cluster):

```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--cells` | Cells | 1000 | 100 to 5000 |
| `--genes` | Genes | 500 | 50 to 2000 |
| `--clusters` | Cell subpopulations | 3 | 1 to 6 |
| `--samples` | Samples per condition | 3 | 1 to 6 |
| `--p-de` | Fraction of differentially expressed genes | 0.1 | 0 to 1 |
| `--lfc` | Mean log2 fold change of DE genes | 2 | 0 to 6 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe writes three CSV files and a text log.

- `counts_sparse.csv` has columns gene, cell and count, one row per non-zero count. Rebuild the matrix with a sparse-matrix reader.
- `cells.csv` lists each cell with `cluster_id`, `sample_id` and `group_id` (A or B).
- `gene_info.csv` has one row per gene and cluster: `category`, `logFC`, `sim_gene`, `sim_disp` and `sim_mean.A` and `sim_mean.B`. The vignette notes that `logFC` approximates `log2(sim_mean.B / sim_mean.A)` only for DE genes, because other categories use mixtures.
- `muscat_log.txt` prints the cell counts per sample and cluster and the count of each gene category.

Check the category table against your setting. With `p_de = 0.1`, about 10% of gene-cluster rows should be DE and the rest EE. The example in the `simData` help page makes the same check with the comment "should be ~10% DE".

## Pitfalls

- **Gene and sample counts need `force = TRUE`.** The docs say the library sizes only make sense when the simulated gene count matches the reference. Smaller gene sets are meant for testing.
- **Only one reference condition is used.** `prepSim` keeps samples from a single group (the first, unless `group_keep` is set). Differences between conditions come from the simulation, not from the reference.
- **`ns` counts samples per group** when two groups are simulated. The docs define it per group for `dd = TRUE`.
- **Unpaired designs draw reference samples at random.** Set `paired = TRUE` to reuse the same set in both groups.
- **Phylogeny overrides `nk`.** With `phylo_tree`, the number of clusters comes from the tree.
- **The model is not zero-inflated.** The vignette describes a plain negative binomial, aimed at droplet data.
- **Version drift.** Docs on GitHub track the newest release. Check `?simData` in your installed version.

## Further reading

- Simulation vignette: https://github.com/HelenaLC/muscat/blob/main/vignettes/simulation.Rmd
- Bioconductor page: https://bioconductor.org/packages/muscat
- Source: https://github.com/HelenaLC/muscat
- Paper: Crowell HL et al. (2020). muscat detects subpopulation-specific state transitions from multi-sample multi-condition single-cell transcriptomics data. Nature Communications 11:6077. https://doi.org/10.1038/s41467-020-19894-4

---

Cite: Crowell HL, Soneson C, Germain P-L, et al. (2020). muscat detects subpopulation-specific state transitions from multi-sample multi-condition single-cell transcriptomics data. Nature Communications 11:6077. doi:10.1038/s41467-020-19894-4

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/muscat).
