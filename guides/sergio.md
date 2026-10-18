# SERGIO

> Simulate single-cell expression from a gene regulatory network, with stochastic transcription, one expression state per cell type, and optional technical noise.

Licence: GPL-3.0-only · [Source code](https://github.com/PayamDiba/SERGIO)

## What it simulates

SERGIO (Single-cell ExpRession of Genes In silicO) simulates single-cell gene expression from a gene regulatory network (GRN) that you supply. It models the stochastic nature of transcription and the linear and non-linear influence of several transcription factors on a gene.

The network has two kinds of genes. Master regulators have no regulators of their own. You give each one a basal production rate in every cell type. All other genes are targets: their production depends on their regulators through Hill functions, with an interaction strength K per regulator (positive activates, negative represses). SERGIO integrates expression over time steps with a noise term and samples cells from the steady state of each cell type.

There are two modes. Steady-state mode gives one expression state per cell type. Differentiation mode moves cells between cell types along a graph you supply and returns spliced and unspliced counts. Optional technical noise then adds outlier genes, library-size variation and dropouts, and converts the result to UMI counts.

Key assumptions: the GRN is given and fixed, interactions follow Hill kinetics, and cell types are defined only by master-regulator rates. There is no cell cycle and there are no spatial effects.

## When to use it

Use SERGIO to make single-cell data with a known regulatory ground truth, for example to test GRN-inference methods or imputation and clustering tools.

- Use [dyngen](dyngen.md) when you want the network built for you around a chosen cell trajectory, including bifurcations and cycles.
- Use [scMultiSim](scmultisim.md) when you also need chromatin accessibility, RNA velocity or cell-cell interactions.
- Use Splatter (https://github.com/Oshlack/splatter) when you only need realistic count distributions and no regulatory network.

## Install

SERGIO has no PyPI or conda package from its authors. The PyPI name `sergio` belongs to an unrelated project. The README says to clone the repository. The current release is v1.0.0 (July 2020, commit `bb84519`).

```bash
git clone https://github.com/PayamDiba/SERGIO
```

Dependencies are numpy, scipy and networkx. The code calls `np.int` and `np.float`, which numpy 1.24 removed, so use numpy 1.23.5 or older, for example with Python 3.10:

```bash
conda create -n sergio -c conda-forge python=3.10 numpy=1.23.5 scipy=1.10.1 networkx=2.8.8
conda activate sergio
export PYTHONPATH=$PWD/SERGIO   # the cloned repository, so `import SERGIO` works
```

## A first run

Adapted from the repository README (https://github.com/PayamDiba/SERGIO#readme) and its notebook `run_sergio.ipynb`. The commands below have not been run for this guide.

```python
import numpy as np
from SERGIO.sergio import sergio

sim = sergio(number_genes=100, number_bins=9, number_sc=300,
             noise_params=1, decays=0.8, sampling_state=15, noise_type='dpd')
sim.build_graph(input_file_taregts='data_sets/De-noised_100G_9T_300cPerT_4_DS1/Interaction_cID_4.txt',
                input_file_regs='data_sets/De-noised_100G_9T_300cPerT_4_DS1/Regs_cID_4.txt',
                shared_coop_state=2)
sim.simulate()
expr = sim.getExpressions()                    # cell types x genes x cells
expr_clean = np.concatenate(expr, axis=1)      # genes x cells
```

The README states that the demo steady-state simulation takes about 150 seconds and the differentiation demo about 120 seconds on a normal desktop. Technical noise is added with `outlier_effect`, `lib_size_effect`, `dropout_indicator` and `convert_to_UMIcounts`, in that order in the notebook.

The recipe below runs a 10-gene network with 3 cell types and 50 cells each. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds SERGIO in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.7 s.

1. Download [sergio-recipe.tar.gz](https://biosimhub.pages.dev/guides/sergio/sergio-recipe.tar.gz) (Dockerfile, run_sergio.py, example grn.csv, regulators.csv, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf sergio-recipe.tar.gz
   cd sergio
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/sergio:1.0.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/sergio:1.0.0 python /opt/run_sergio.py --grn /work/in/grn.csv \
    --regs /work/in/regulators.csv --genes 10 \
    --cell-types 3 --cells 50 --noise 1 --decay 0.8 \
    --hill 2 --sampling-state 15 --technical-noise yes \
    --seed 42 > out/sergio_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `counts_noisy.csv` | 12.5 KB |
| `expression_clean.csv` | 12.2 KB |
| `sergio_log.txt` | 500 B |
| `summary.txt` | 94 B |

<details><summary>First lines of <code>counts_noisy.csv</code></summary>

```
gene,type0_cell0,type0_cell1,type0_cell2,type0_cell3,type0_cell4,type0_cell5,type0_cell6,type0_cell7,type0_cell8,type0_cell9,type0_cell10,type0_cell11,type0_cell12,type0_cell13,type0_cell14,type0_cell
gene0,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.0000,0.000
```

</details>

<details><summary>First lines of <code>expression_clean.csv</code></summary>

```
gene,type0_cell0,type0_cell1,type0_cell2,type0_cell3,type0_cell4,type0_cell5,type0_cell6,type0_cell7,type0_cell8,type0_cell9,type0_cell10,type0_cell11,type0_cell12,type0_cell13,type0_cell14,type0_cell
gene0,0.8066,0.2765,0.9462,0.5018,0.1800,0.5190,0.2369,0.0815,0.4789,0.7020,0.0784,1.3158,0.6105,1.1504,0.2098,1.0310,1.4817,0.5907,1.7557,1.1361,1.5154,0.5168,0.0000,0.2775,0.1986,1.6488,0.0000,0.605
```

</details>

<details><summary>First lines of <code>sergio_log.txt</code></summary>

```
Start simulating new level
There are 2 genes to simulate in this layer
Done with current level
Start simulating new level
There are 2 genes to simulate in this layer
Done with current level
Start simulating new level
There are 3 genes to simulate in this layer
Done with current level
Start simulating new level
There are 2 genes to simulate in this layer
Done with current level
```

</details>

<details><summary>First lines of <code>summary.txt</code></summary>

```
seed	42
genes	10
cell_types	3
cells_per_type	50
clean_mean	1.8765
counts_zero_fraction	0.8060
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--genes` | Genes in the network | 10 | 3 to 200 |
| `--cell-types` | Cell types (columns in the regulator file minus one) | 3 | 1 to 12 |
| `--cells` | Cells per cell type | 50 | 10 to 300 |
| `--noise` | Noise amplitude (q) | 1 | 0.01 to 5 |
| `--decay` | Decay rate | 0.8 | 0.1 to 5 |
| `--hill` | Hill coefficient shared by all interactions | 2 | 1 to 4 |
| `--sampling-state` | Steady-state sampling length | 15 | 1 to 30 |
| `--technical-noise` | Add outliers | yes | yes, no |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The recipe writes `expression_clean.csv`, a genes-by-cells matrix. Rows are `gene0` to `gene9`. Columns are named `type<T>_cell<C>`, and cells of one type sit next to each other. Values are continuous expression levels from the simulation. If technical noise is on, `counts_noisy.csv` has the same layout with integer UMI counts after outliers, library-size scaling and dropouts.

`summary.txt` lists the seed, sizes, the mean clean expression and, with noise on, the fraction of zero counts. Compare cell types: genes downstream of a master regulator should follow that regulator's rate in each type, and a repressed target should be low where its repressor is high.

## Pitfalls

- **Gene IDs start at 0.** Every gene must appear once, either as a master regulator in the regulator file or as a target row in the interaction file. A count mismatch stops the run with "Inconsistent number of genes".
- **No gene may sit outside the network.** The source notes that a node with no incoming or outgoing edge causes an error.
- **Column counts must agree.** The regulator file needs one rate column per cell type, and `number_bins` must match.
- **A shared Hill coefficient overrides the file.** With `shared_coop_state` above 0, the Hill columns in the interaction file are ignored.
- **There is no seed argument.** SERGIO uses numpy's global generator. The recipe's script seeds it before each random step. Seed it yourself in your own scripts.
- **Run time grows with network size.** Genes, cell types, cells per type and `sampling_state` all multiply the cost.
- **Differentiation mode needs a bifurcation matrix.** The recipe covers steady-state mode only.

## Further reading

- Repository and README: https://github.com/PayamDiba/SERGIO
- Dibaeinia P, Sinha S (2020). SERGIO: a single-cell expression simulator guided by gene regulatory networks. Cell Systems 11:252-271. https://doi.org/10.1016/j.cels.2020.08.003

---

Cite: Dibaeinia P, Sinha S (2020). SERGIO: a single-cell expression simulator guided by gene regulatory networks. Cell Systems 11:252-271. doi:10.1016/j.cels.2020.08.003

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/sergio).
