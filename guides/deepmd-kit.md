# DeePMD-kit

> Train a small deep neural network potential (se_e2_a) on labelled water frames and test its energy and force errors on held-out frames.

Licence: LGPL-3.0-or-later · [Source code](https://github.com/deepmodeling/deepmd-kit)

## What it simulates

DeePMD-kit trains a neural-network potential from reference data. You give it atomic coordinates, boxes, and the energies and forces that a quantum calculation produced for each frame. It learns a function that returns energy and forces from the atomic positions alone. The trained model can then drive molecular dynamics in LAMMPS, i-PI or ASE at a small fraction of the cost of the quantum method.

The recipe trains the "se_e2_a" model. A descriptor turns each atom's neighbours inside a cutoff radius into a rotation-invariant feature, an embedding network processes those features, and a fitting network sums per-atom energies into the total. Forces come from the derivative of the energy, so energy and force are consistent. The recipe uses the PyTorch backend (`dp --pt`).

Units are eV for energy and eV per angstrom for force. The data is 80 frames of 64 water molecules (192 atoms: 64 O, 128 H) from DeePMD-kit's own water example. The recipe trains on the first 64 frames and tests on the last 16.

## When to use it

Use DeePMD-kit when you have quantum-mechanical reference frames (DFT or similar) and want a fast potential for the same system.

- Use [CP2K](cp2k.md) or [NWChem](nwchem.md) to produce the reference energies and forces.
- Use [LAMMPS](lammps.md) to run molecular dynamics with a trained model.
- Use [OpenMM](openmm.md) when a classical force field is enough and no training data exists.

## Install it yourself

The recipe image installs the conda-forge build of 3.1.3 (CPU, Python 3.12, MPICH), which carries both the TensorFlow 2.18 and PyTorch 2.6.0 backends. The image is 750 MB.

```
micromamba create -n dp -c conda-forge "deepmd-kit=3.1.3=cpu_py312*mpich*"
micromamba run -n dp dp --pt train input.json
micromamba run -n dp dp --pt freeze -o model.pth
micromamba run -n dp dp --pt test -m model.pth -s test -n 16
```

The helper `run_dp.py` takes one `.npz` file with `coord`, `force`, `energy`, `box` and `atype`, writes the train and test systems in DeePMD's `set.000/*.npy` layout, writes `input.json` from the form values, and runs the three commands.

## Run the tested example

This recipe builds DeePMD-kit in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 53.9 s.

1. Download [deepmd-kit-recipe.tar.gz](https://biosimhub.pages.dev/guides/deepmd-kit/deepmd-kit-recipe.tar.gz) (Dockerfile, run_dp.py, example data.npz, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf deepmd-kit-recipe.tar.gz
   cd deepmd-kit
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/deepmd-kit:3.1.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/deepmd-kit:3.1.3 python /opt/run_dp.py --data /work/in/data.npz \
    --steps 300 --rcut 6 --embedding small --fitting small \
    --start_lr 0.01 --test_frames 16 --seed 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `checkpoint` | 17 B |
| `dp_commands.log` | 9.8 KB |
| `input.json` | 862 B |
| `input_v2_compat.json` | 1.3 KB |
| `lcurve.out` | 807 B |
| `model.ckpt-300.pt` | 1.3 MB |
| `model.ckpt.pt` | 1.3 MB |
| `model.pth` | 573.7 KB |
| `out.json` | 3.5 KB |
| `result.json` | 178 B |
| `run_log.txt` | 153 B |
| `test/set.000/box.npy` | 704 B |
| `test/set.000/coord.npy` | 36.1 KB |
| `test/set.000/energy.npy` | 192 B |
| `test/set.000/force.npy` | 36.1 KB |
| `test/type.raw` | 384 B |
| `test/type_map.raw` | 4 B |
| `train/set.000/box.npy` | 2.4 KB |
| `train/set.000/coord.npy` | 144.1 KB |
| `train/set.000/energy.npy` | 384 B |
| `train/set.000/force.npy` | 144.1 KB |
| `train/type.raw` | 384 B |
| `train/type_map.raw` | 4 B |

<details><summary>First lines of <code>checkpoint</code></summary>

```
model.ckpt-300.pt
```

</details>

<details><summary>First lines of <code>dp_commands.log</code></summary>

```
$ dp --pt train input.json
To get the best performance, it is recommended to adjust the number of threads by setting the environment variables OMP_NUM_THREADS, DP_INTRA_OP_PARALLELISM_THREADS, and DP_INTER_OP_PARALLELISM_THREAD
[2026-10-18 01:58:51,449] DEEPMD INFO    DeePMD version: 3.1.3
[2026-10-18 01:58:51,449] DEEPMD INFO    Configuration path: input.json
[2026-10-18 01:58:51,449] DEEPMD INFO     _____               _____   __  __  _____           _     _  _   
[2026-10-18 01:58:51,449] DEEPMD INFO    |  __ \             |  __ \ |  \/  ||  __ \         | |   (_)| |  
[2026-10-18 01:58:51,449] DEEPMD INFO    | |  | |  ___   ___ | |__) || \  / || |  | | ______ | | __ _ | |_ 
[2026-10-18 01:58:51,449] DEEPMD INFO    | |  | | / _ \ / _ \|  ___/ | |\/| || |  | ||______|| |/ /| || __|
[2026-10-18 01:58:51,449] DEEPMD INFO    | |__| ||  __/|  __/| |     | |  | || |__| |        |   < | || |_ 
[2026-10-18 01:58:51,449] DEEPMD INFO    |_____/  \___| \___||_|     |_|  |_||_____/         |_|\_\|_| \__|
[2026-10-18 01:58:51,449] DEEPMD INFO    Please read and cite:
[2026-10-18 01:58:51,449] DEEPMD INFO    Wang, Zhang, Han and E, Comput.Phys.Comm. 228, 178-184 (2018)
```

</details>

<details><summary>First lines of <code>input.json</code></summary>

```
{
 "model": {
  "type_map": [
   "O",
   "H"
  ],
  "descriptor": {
   "type": "se_e2_a",
   "sel": [
    46,
    92
   ],
```

</details>

<details><summary>First lines of <code>input_v2_compat.json</code></summary>

```
{
    "model": {
        "type_map": [
            "O",
            "H"
        ],
        "descriptor": {
            "type": "se_e2_a",
            "sel": [
                46,
                92
            ],
```

</details>

<details><summary>First lines of <code>lcurve.out</code></summary>

```
# step       rmse_trn    rmse_e_trn    rmse_f_trn   lr      
# If there is no available reference data, rmse_*_{val,trn} will print nan
      1      2.68e+01      1.21e+00      8.44e-01    1.0e-02
     30      2.21e+01      4.68e-02      6.98e-01    1.0e-02
     60      1.13e+01      1.86e-02      5.67e-01    4.0e-03
     90      5.35e+00      1.25e-02      4.24e-01    1.6e-03
    120      2.71e+00      8.71e-03      3.38e-01    6.3e-04
    150      2.09e+00      8.27e-03      4.08e-01    2.5e-04
    180      1.20e+00      9.58e-03      3.60e-01    1.0e-04
    210      8.95e-01      5.02e-03      4.00e-01    4.0e-05
    240      6.13e-01      4.02e-03      3.80e-01    1.6e-05
    270      4.86e-01      1.14e-02      3.60e-01    6.3e-06
```

</details>

<details><summary>First lines of <code>out.json</code></summary>

```
{
    "model": {
        "type_map": [
            "O",
            "H"
        ],
        "descriptor": {
            "type": "se_e2_a",
            "sel": [
                46,
                92
            ],
```

</details>

<details><summary>First lines of <code>result.json</code></summary>

```
{
 "train_frames": 64,
 "test_frames": 16,
 "atoms": 192,
 "steps": 300,
 "energy_rmse_ev": 1.329363,
 "energy_rmse_per_atom_ev": 0.006923764,
 "force_rmse_ev_per_a": 0.3727904
}
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: train_frames=64, test_frames=16, atoms=192, steps=300, energy_rmse_ev=1.329363, energy_rmse_per_atom_ev=0.006923764, force_rmse_ev_per_a=0.3727904
```

</details>

<details><summary>First lines of <code>test/type.raw</code></summary>

```
0
0
0
0
0
0
0
0
0
0
0
0
```

</details>

<details><summary>First lines of <code>test/type_map.raw</code></summary>

```
O
H
```

</details>

<details><summary>First lines of <code>train/type.raw</code></summary>

```
0
0
0
0
0
0
0
0
0
0
0
0
```

</details>

<details><summary>First lines of <code>train/type_map.raw</code></summary>

```
O
H
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--steps` | Training steps | 300 | 10 to 5000 |
| `--rcut` | Descriptor cutoff (A) | 6 | 3 to 6 |
| `--embedding` | Embedding network size | small | small, medium |
| `--fitting` | Fitting network size | small | small, medium, large |
| `--start_lr` | Starting learning rate | 0.01 | 1e-05 to 0.02 |
| `--test_frames` | Held-out test frames | 16 | 2 to 40 |
| `--seed` | Seed | 1 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The run trains for 300 steps (batch size 1), freezes the model and tests it. It took 53.9 s.

- `run_log.txt` has one line: "done: train_frames=64, test_frames=16, atoms=192, steps=300, energy_rmse_ev=1.329363, energy_rmse_per_atom_ev=0.006923764, force_rmse_ev_per_a=0.3727904".
- `lcurve.out` has one row per 30 steps with the training RMSE of energy per atom and force, and the learning rate. The force RMSE falls from 0.844 eV/A at step 1 to 0.360 eV/A at step 270, while the learning rate decays from 1e-2 to 6.3e-6.
- `model.pth` is the frozen model (587,460 bytes). `model.ckpt.pt` is the checkpoint (1,408,384 bytes).
- `input.json` is the training input, `result.json` repeats the test numbers, and `dp_commands.log` has the output of the three `dp` commands.
- `train/` and `test/` hold the data as DeePMD reads it.

Judge the result against two baselines computed from the same data. Predicting zero force on the 16 test frames gives an RMSE of 0.813 eV/A, so the force RMSE of 0.373 eV/A removes 54 % of it. Predicting the mean training energy gives a total-energy RMSE of 0.638 eV on the test frames. The trained model scores 1.329 eV, which is worse. Energy needs more steps than force at this scale, so this model is a demonstration of the workflow, not a usable potential.

## Your own runs

Each run changes one value from the example (300 steps, learning rate 0.01, seed 1). Test errors are force RMSE in eV/A and total-energy RMSE in eV.

- **Another seed.** `--seed 2` gave 0.718 eV/A and 0.606 eV, in 62 s. A force RMSE almost twice the example's shows that 300 steps are not enough to make training reliable.
- **More steps.** `--steps 1000` gave 0.219 eV/A and 0.813 eV, in 109 s. Force error fell by 41 %, and the energy error improved too.
- **Larger networks.** `--embedding medium --fitting medium` gave 0.356 eV/A and 0.989 eV, in 99 s. The larger model took twice as long and was not clearly better at 300 steps.
- **Shorter cutoff.** `--rcut 4` gave 0.291 eV/A and 1.489 eV, in 47 s. The force error was lower than the 6 A run, and the energy error was higher.
- **Lower learning rate.** `--start_lr 0.001` gave 0.787 eV/A and 0.601 eV. With this rate and 300 steps the model had learned almost nothing (the zero-force baseline is 0.813).

## Pitfalls

- **The training RMSE can mislead.** The `rmse_trn` column of `lcurve.out` is a loss weighted by energy and force prefactors that change during training. Read the `rmse_e_trn` and `rmse_f_trn` columns, and test on held-out frames.
- **Neighbour counts.** The recipe uses `sel = [46, 92]` for 6 A in liquid water. A denser system or a longer cutoff needs larger values, and the number of entries must match the number of atom types.
- **Single system only.** The helper expects the atom order and types in `atype` to be [O, H] and the same in every frame.
- **Runs are seed-sensitive at this length.** Report several seeds before drawing conclusions from small differences.
- **Time.** About 0.08 s per step on one CPU (1000 steps took 109 s against 54 s for 300), plus roughly 30 s for start-up, freezing and testing.

## Further reading

- Documentation: https://docs.deepmodeling.com/projects/deepmd/
- Water example data and inputs: https://github.com/deepmodeling/deepmd-kit/tree/master/examples/water
- Source: https://github.com/deepmodeling/deepmd-kit
- Paper: Wang H et al. (2018) DeePMD-kit: A deep learning package for many-body potential energy representation and molecular dynamics. Comput Phys Commun 228:178-184. https://doi.org/10.1016/j.cpc.2018.03.016

---

Cite: Wang H, Zhang L, Han J, E W (2018). DeePMD-kit: A deep learning package for many-body potential energy representation and molecular dynamics. Comput Phys Commun 228:178-184. doi:10.1016/j.cpc.2018.03.016

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/deepmd-kit).
