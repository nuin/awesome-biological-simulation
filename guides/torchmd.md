# TorchMD

> Run a short Langevin molecular dynamics simulation of a water box with TorchMD (CHARMM-style force field written in PyTorch) and log potential, kinetic and total energy and temperature.

Licence: MIT · [Source code](https://github.com/torchmd/torchmd)

## What it simulates

TorchMD is a molecular dynamics engine written in PyTorch. It reads a CHARMM-style topology and force field, computes forces with PyTorch tensors, and integrates Newton's equations with a Langevin thermostat. Because forces come from tensors, a neural-network potential can be added as an extra force term and trained through the same code.

The recipe runs the classical force field only. The system is 97 flexible water molecules (291 atoms) in a periodic box of 16.919 x 16.633 x 16.639 A. The force terms are Lennard-Jones, bonds, angles and electrostatics. Time runs in femtoseconds, energies are in kcal/mol, and temperature is in kelvin.

The key assumptions are a fixed-charge water model with flexible bonds, a cutoff (7.3 A by default) on non-bonded forces, a thermostat but no barostat, and a single replica on one CPU.

## When to use it

Use TorchMD to learn how a PyTorch MD loop is built, to prototype a force term that you want to differentiate or train, or to run small classical systems in a Python workflow.

- Use [OpenMM](openmm.md) or [GROMACS](gromacs.md) for production-scale classical runs with constraints, barostats and long-range electrostatics (PME).
- Use [LAMMPS](lammps.md) for coarse-grained or materials systems with many potential styles.
- Use [JAX MD](jax-md.md) for another differentiable engine, built on JAX.

## Install it yourself

The recipe image uses Python 3.12, with PyTorch 2.14.1 (CPU build) from conda-forge, then TorchMD 1.1.2 and moleculekit 1.17.16 from PyPI:

```
micromamba create -n tmd -c conda-forge python=3.12 pip "pytorch=*=cpu_*" "numpy<2" scipy pandas networkx pyyaml tqdm "parmed>=4.3"
micromamba run -n tmd pip install --no-deps torchmd==1.1.2 moleculekit==1.17.16
micromamba run -n tmd python -m torchmd.run --conf conf.yaml
```

The recipe's helper `run_torchmd.py` writes `conf.yaml` from the form values, runs `torchmd.run` and summarises the log.

## Run the tested example

This recipe builds TorchMD in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 12.2 s.

1. Download [torchmd-recipe.tar.gz](https://biosimhub.pages.dev/guides/torchmd/torchmd-recipe.tar.gz) (Dockerfile, run_torchmd.py, example psf.psf, pdb.pdb, forcefield.yaml, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf torchmd-recipe.tar.gz
   cd torchmd
   sh run.sh
   ```

![Terminal recording of the TorchMD example run](https://biosimhub.pages.dev/media/torchmd/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/torchmd:1.1.2 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/torchmd:1.1.2 python /opt/run_torchmd.py --psf /work/in/psf.psf \
    --pdb /work/in/pdb.pdb --forcefield /work/in/forcefield.yaml \
    --steps 3000 --timestep 1 --temperature 300 \
    --gamma 5 --cutoff 7.3 --output_period 50 \
    --minimize 200 --electrostatics reaction_field \
    --seed 1 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `conf.yaml` | 376 B |
| `input.yaml` | 529 B |
| `monitor_0.csv` | 5.5 KB |
| `output_0.npy` | 204.7 KB |
| `output_0.xyz` | 528.0 KB |
| `run_log.txt` | 138 B |
| `summary.json` | 211 B |
| `torchmd_stdout.log` | 10.1 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/torchmd/result-dark.png"><img src="https://biosimhub.pages.dev/media/torchmd/result.png" alt="Plot of the TorchMD example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>conf.yaml</code></summary>

```
cutoff: 7.3
device: cpu
forcefield: /work/in/forcefield.yaml
forceterms:
- lj
- bonds
- angles
- electrostatics
langevin_gamma: 5.0
langevin_temperature: 300.0
log_dir: .
minimize: 200
```

</details>

<details><summary>First lines of <code>input.yaml</code></summary>

```
coordinates: null
cutoff: 7.3
device: cpu
exclusions: !!python/tuple
- bonds
- angles
- 1-4
extended_system: null
external: null
forcefield: /work/in/forcefield.yaml
forceterms:
- lj
```

</details>

<details><summary>First lines of <code>monitor_0.csv</code></summary>

```
iter,ns,epot,ekin,etot,T,t
50,4.9999999999999996e-05,-924.463623046875,168.93613,-755.5274963378906,194.7595,1.1506152153015137
100,9.999999999999999e-05,-882.7234497070312,182.64673,-700.0767211914062,210.5659,1.296283483505249
150,0.00015000000000000001,-877.8861694335938,217.2321,-660.6540679931641,250.43796,1.4243557453155518
200,0.00019999999999999998,-870.8844604492188,228.43481,-642.4496459960938,263.3531,1.5548160076141357
250,0.00025,-843.6937866210938,213.55743,-630.1363525390625,246.20158,1.697197437286377
300,0.00030000000000000003,-849.1795654296875,251.21404,-597.9655303955078,289.61432,1.831477165222168
350,0.00035,-829.1224365234375,251.93787,-577.1845703125,290.4488,1.966764211654663
400,0.00039999999999999996,-825.6843872070312,262.65265,-563.03173828125,302.80142,2.098721504211426
450,0.00045,-802.4154052734375,235.80234,-566.6130676269531,271.8468,2.2368385791778564
500,0.0005,-820.283447265625,257.58325,-562.7001953125,296.95712,2.365467071533203
550,0.00055,-822.9822998046875,244.93225,-578.050048828125,282.3723,2.4999282360076904
```

</details>

<details><summary>First lines of <code>output_0.xyz</code></summary>

```
291

O 2.9689982 9.307691 8.8363495
H 2.469931 9.279162 9.6753025
H 2.2162526 9.211491 8.187135
O 9.887557 7.903574 5.190201
H 10.147486 8.427113 5.9761696
H 9.17763 8.4842005 4.817603
O 2.1312795 6.389791 2.5930839
H 2.2307339 5.50318 2.2333703
H 1.6462227 6.8904886 1.8815567
O 10.769096 7.559794 2.5272758
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
done: frames=60, first_epot_kcal=-924.5, last_epot_kcal=-853.2, mean_T_second_half_K=304.5, etot_first_kcal=-755.5, etot_last_kcal=-595.8
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "frames": 60,
 "first_epot_kcal": -924.463623046875,
 "last_epot_kcal": -853.2349853515625,
 "mean_T_second_half_K": 304.543208,
 "etot_first_kcal": -755.5274963378906,
 "etot_last_kcal": -595.7771606445312
}
```

</details>

<details><summary>First lines of <code>torchmd_stdout.log</code></summary>

```
Force terms:  ['lj', 'bonds', 'angles', 'electrostatics']
Writing logs to  ./monitor_0.csv
Iter  Epot            fmax    
   0   -573.125549    96.655581
   1   -231.158386    264.608543
   2   -647.831787    28.852937
   3   -661.574951    23.733004
   4   -703.865479    42.562560
   5   -723.458618    43.324530
   6   -737.584412    31.861450
   7   -759.782532    62.646566
   8   -768.139160    24.972595
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--steps` | MD steps | 3000 | 50 to 20000 |
| `--timestep` | Time step (fs) | 1 | 0.1 to 4 |
| `--temperature` | Temperature (K) | 300 | 10 to 1000 |
| `--gamma` | Langevin friction (1/ps) | 5 | 0.01 to 50 |
| `--cutoff` | Non-bonded cutoff (A) | 7.3 | 3 to 8 |
| `--output_period` | Log every N steps | 50 | 10 to 1000 |
| `--minimize` | Minimisation steps before MD (0 = none) | 200 | 0 to 500 |
| `--electrostatics` | Electrostatics beyond the cutoff | reaction_field | reaction_field, cutoff |
| `--seed` | Seed | 1 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The run simulates 3000 steps of 1 fs (3 ps) after 200 minimisation steps, and logs every 50 steps. It took 12.2 s including start-up.

- `run_log.txt` has one line: "done: frames=60, first_epot_kcal=-924.5, last_epot_kcal=-853.2, mean_T_second_half_K=304.5, etot_first_kcal=-755.5, etot_last_kcal=-595.8".
- `monitor_0.csv` has 60 rows with the step, time in ns, potential energy, kinetic energy, total energy, temperature and wall time. At step 50 the temperature is 194.8 K and the potential energy is -924.5 kcal/mol. At step 500 the temperature is 297.0 K.
- `output_0.xyz` is the trajectory: 60 frames of 291 atoms (540,643 bytes). `output_0.npy` holds the same coordinates as an array.
- `conf.yaml` is the TorchMD configuration the helper wrote, and `summary.json` repeats the run-log numbers.

Check the temperature. The thermostat targets 300 K and the mean over the second half of the run (1.5 to 3 ps) is 304.5 K. With 291 atoms the instantaneous temperature fluctuates by about 5 %, so 304.5 K agrees with the target. The total energy rises from -755.5 to -595.8 kcal/mol because the thermostat adds heat while the minimised system warms from 195 K to 300 K. It is not conserved in a Langevin run.

## Your own runs

Each run changes one value from the example (seed 1). Results are mean temperature over the second half, and the last potential energy.

- **Another seed.** `--seed 2` gave 304.3 K and -821.3 kcal/mol, against 304.5 K and -853.2. Different initial velocities and thermostat noise change the energy by about 30 kcal/mol (4 %). The same seed reproduced the example exactly.
- **Hotter target.** `--temperature 350` gave a mean of 346.2 K.
- **No minimisation.** `--minimize 0` started at -618.5 kcal/mol (the first logged value) against -924.5 with minimisation, and ended at -828.1 kcal/mol with a mean of 293.7 K. The system relaxes in either case, and the minimised start wastes less of the run.
- **Plain cutoff electrostatics.** `--electrostatics cutoff` started at -414.7 kcal/mol and ended at -833.7 kcal/mol. Truncating the Coulomb force at 7.3 A gives a noisy first stretch. The default reaction-field setting started from -924.5.
- **Weak thermostat.** `--gamma 0.1` gave a mean of only 213.7 K. With friction 0.1 per ps the system needs about 10 ps to reach the target, so the 3 ps run ends cold.
- **Time step 2 fs.** `--timestep 2` gave 299.7 K, with 6 ps simulated in the same 3000 steps.

## Pitfalls

- **Force-term names must be lower case.** TorchMD's own example configuration writes `LJ`, `Bonds`, `Angles` and `Electrostatics`. With those capitals the Lennard-Jones coefficients are not built and the run stops with "'Parameters' object has no attribute 'A'". The helper writes `lj`, `bonds`, `angles`, `electrostatics`.
- **The box needs a CRYST1 line.** TorchMD reads the periodic box from the PDB. The topology (PSF) and PDB must list the same atoms in the same order.
- **Steps must be a multiple of the output period.** Otherwise TorchMD raises "Steps must be multiple of output-period".
- **The example box is dilute.** 97 waters in 4,682 cubic A is about 0.62 g/cm3. There is no barostat, so the density stays there and properties such as pressure are not water at ambient conditions.
- **Cutoff and box size.** The cutoff must stay below half the box edge (8.3 A here). The recipe limits it to 8 A.
- **Short runs.** 3 ps is a demonstration of the code path. It is too short for equilibrium properties.

## Further reading

- TorchMD repository and tutorial notebook: https://github.com/torchmd/torchmd
- Force-field format: the YAML in the repository's `tests/water` folder, the same file as the recipe's example.
- Source: https://github.com/torchmd/torchmd
- Paper: Doerr S et al. (2021) TorchMD: A deep learning framework for molecular simulations. J Chem Theory Comput 17:2355-2363. https://doi.org/10.1021/acs.jctc.0c01343

---

Cite: Doerr S, Majewski M, Perez A, Kramer A, Clementi C, Noe F, Giorgino T, De Fabritiis G (2021). TorchMD: A deep learning framework for molecular simulations. J Chem Theory Comput 17:2355-2363. doi:10.1021/acs.jctc.0c01343

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/torchmd).
