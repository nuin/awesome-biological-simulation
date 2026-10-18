# openmmtools

> Parallel-tempering replica exchange of alanine dipeptide on the OpenMM CPU platform, with the replica paths and the mean potential energy at each temperature.

Licence: MIT · [Source code](https://github.com/choderalab/openmmtools)

## What it simulates

openmmtools is a Python library of samplers and move sets built on OpenMM. It adds what plain OpenMM leaves out: replica exchange, alchemical free-energy states, Monte Carlo moves and a system-and-state toolkit. Each sampler runs on any OpenMM platform (CPU, CUDA, OpenCL).

The recipe uses one part: parallel-tempering replica exchange. The helper script builds N copies of a small molecule at temperatures spaced geometrically between a lowest and a highest value. Each copy runs Langevin dynamics for a block of steps. Then the sampler proposes swaps of temperature between copies and accepts them with the Metropolis rule. A copy that heats up crosses barriers more easily, and a copy that cools down returns to the target ensemble.

The test systems are alanine dipeptide (22 atoms) in implicit solvent (GBSA) or in vacuum. They come from `openmmtools.testsystems`. The assumptions are a fixed-charge force field, rigid bonds to hydrogen and a Langevin thermostat with a collision rate of 1 per ps.

## When to use it

- Learning how replica exchange behaves: swap rates, temperature spacing and how a replica moves across the ladder.
- Prototyping a multistate or alchemical sampler in Python before moving it to a GPU.
- Generating test data for tools that read OpenMM NetCDF output.

Use [OpenMM](openmm.md) for plain molecular dynamics of a structure you upload. Use [GROMACS](gromacs.md) for large solvated systems and production runs. This recipe has no upload: the system is a built-in test molecule, so it demonstrates the sampler and does not model your protein.

## Install it yourself

The conda command below resolves for openmmtools 0.26.0 on conda-forge. It brought OpenMM 8.6.1 in the 0.26.0 image.

```
micromamba create -n omt -c conda-forge openmmtools=0.26.0
micromamba activate omt
```

A minimal replica-exchange run, without the recipe's helper script:

```python
from openmm import unit
from openmmtools import mcmc, states, testsystems
from openmmtools.multistate import ReplicaExchangeSampler, MultiStateReporter

test = testsystems.AlanineDipeptideImplicit()
temps = [300, 400, 500, 600]
thermo = [states.ThermodynamicState(test.system, temperature=t * unit.kelvin) for t in temps]
sampler_states = [states.SamplerState(test.positions) for _ in temps]
move = mcmc.LangevinDynamicsMove(timestep=2 * unit.femtosecond, n_steps=250, reassign_velocities=True)
sampler = ReplicaExchangeSampler(mcmc_moves=move, number_of_iterations=10)
sampler.create(thermo, sampler_states, MultiStateReporter("remd.nc"))
sampler.run()
```

## Run the tested example

This recipe builds openmmtools in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 24.2 s.

1. Download [openmmtools-recipe.tar.gz](https://biosimhub.pages.dev/guides/openmmtools/openmmtools-recipe.tar.gz) (Dockerfile, run_remd.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf openmmtools-recipe.tar.gz
   cd openmmtools
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/openmmtools:0.26.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/openmmtools:0.26.0 python /opt/driver/run_remd.py --system alanine-dipeptide-implicit \
    --replicas 6 --tmin 300 --tmax 600 --iterations 20 \
    --steps-per-iteration 250 --timestep-fs 2 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `energy_by_temperature.csv` | 241 B |
| `remd.nc` | 78.9 KB |
| `replica_states.csv` | 411 B |
| `run_log.txt` | 1.3 KB |
| `summary.json` | 321 B |

<details><summary>First lines of <code>energy_by_temperature.csv</code></summary>

```
state,temperature_K,samples,mean_potential_kJ_mol,std_potential_kJ_mol
0,300.0,20,-110.932,14.944
1,344.61,20,-104.287,14.969
2,395.85,20,-101.127,17.983
3,454.71,20,-98.282,15.164
4,522.33,20,-78.212,27.165
5,600.0,20,-58.603,26.161
```

</details>

<details><summary>First lines of <code>replica_states.csv</code></summary>

```
iteration,replica0_state,replica1_state,replica2_state,replica3_state,replica4_state,replica5_state
0,0,1,2,3,4,5
1,1,2,3,4,0,5
2,3,1,5,2,0,4
3,2,0,5,3,1,4
4,2,1,5,3,0,4
5,2,0,5,3,1,4
6,5,1,4,2,3,0
7,5,0,4,1,2,3
8,5,4,3,2,0,1
9,5,2,4,0,1,3
10,4,3,5,1,2,0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
Please cite the following:

        Friedrichs MS, Eastman P, Vaidyanathan V, Houston M, LeGrand S, Beberg AL, Ensign DL, Bruns CM, and Pande VS. Accelerating molecular dynamic simulations on graphics processing unit. J. Comput.
        Eastman P and Pande VS. OpenMM: A hardware-independent framework for molecular simulations. Comput. Sci. Eng. 12:34, 2010. DOI: 10.1109/MCSE.2010.27
        Eastman P and Pande VS. Efficient nonbonded interactions for molecular dynamics on a graphics processing unit. J. Comput. Chem. 31:1268, 2010. DOI: 10.1002/jcc.21413
        Eastman P and Pande VS. Constant constraint matrix approximation: A robust, parallelizable constraint method for molecular simulations. J. Chem. Theor. Comput. 6:434, 2010. DOI: 10.1021/ct9004
        Chodera JD and Shirts MR. Replica exchange and expanded ensemble simulations as Gibbs multistate: Simple improvements for enhanced mixing. J. Chem. Phys., 135:194110, 2011. DOI:10.1063/1.36606
        
{"system": "alanine-dipeptide-implicit", "temperatures_K": [300.0, 344.61, 395.85, 454.71, 522.33, 600.0], "iterations": 20, "steps_per_iteration": 250, "md_steps_per_replica": 5000, "fraction_of_repl
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "system": "alanine-dipeptide-implicit",
 "temperatures_K": [
  300.0,
  344.61,
  395.85,
  454.71,
  522.33,
  600.0
 ],
 "iterations": 20,
 "steps_per_iteration": 250,
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--system` | Test system | alanine-dipeptide-implicit | alanine-dipeptide-implicit, alanine-dipeptide-vacuum |
| `--replicas` | Replicas (temperature states) | 6 | 2 to 12 |
| `--tmin` | Lowest temperature (K) | 300 | 200 to 600 |
| `--tmax` | Highest temperature (K) | 600 | 250 to 1000 |
| `--iterations` | Exchange iterations | 20 | 1 to 300 |
| `--steps-per-iteration` | MD steps per iteration | 250 | 10 to 2000 |
| `--timestep-fs` | Time step (fs) | 2 | 0.5 to 2.5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper script `run_remd.py` runs 6 replicas from 300 to 600 K (300, 344.61, 395.85, 454.71, 522.33 and 600 K). It does 20 iterations of 250 Langevin steps at 2 fs, so each replica covers 5,000 steps (10 ps). After every iteration the sampler proposes swaps. Five files come back.

- `run_log.txt` has the openmmtools citation list and a one-line JSON summary.
- `summary.json` holds the ladder, the step counts, the fraction of replicas that changed state per iteration, the number of end-to-end traversals and the wall time.
- `replica_states.csv` has 21 rows (the starting state plus 20 iterations). Each column is a replica and each value is the temperature index it occupies. Row 0 is `0,1,2,3,4,5`. Row 1 is `1,2,3,4,0,5`: replica 0 moved to state 1, replica 4 to state 0, and replica 5 stayed at 600 K.
- `energy_by_temperature.csv` has one row per temperature: sample count (20 each), mean potential energy and its standard deviation, in kJ/mol.
- `remd.nc` (80,769 bytes) is the NetCDF file openmmtools writes. Analyse it with `openmmtools.multistate.MultiStateReporter` or pymbar.

Check the energy table against physics. Mean potential energy should rise with temperature. In the captured run it went from -110.9 kJ/mol at 300 K to -104.3, -101.1, -98.3 and -78.2 at 522 K and to -58.6 at 600 K. The standard deviation grew from 14.9 to 26.2 kJ/mol over the same range, as expected for a wider conformational spread. The ladder is not perfectly smooth. With 20 samples per state, the mean at one temperature can sit a few kJ/mol off the trend.

## Your own runs

Each run below changes one thing from the default (6 replicas, 300 to 600 K, 20 iterations of 250 steps, implicit solvent). Each used the recipe's image.

- **Default repeated.** The fraction of replicas that changed state per iteration was 0.693 and the replicas made 8 end-to-end traversals. Mean potential energy ran from -117.2 kJ/mol at 300 K to -53.5 at 600 K.
- **Two replicas.** `--replicas 2` (300 and 600 K only) gave a state-change fraction of 0.158. Mean energies were -111.8 kJ/mol at 300 K and -71.0 at 600 K. Only 2 temperatures means each replica has one neighbour, so it moves less often than on the 6-rung ladder.
- **Vacuum.** `--system alanine-dipeptide-vacuum` gave a state-change fraction of 0.675. Mean energies rose from -67.3 kJ/mol at 300 K to -0.8 at 600 K, a 66 kJ/mol rise against 64 kJ/mol in implicit solvent for that repeat of the default.
- **Twelve replicas, narrower ladder.** `--replicas 12 --tmax 450 --iterations 10` gave a state-change fraction of 0.963. Neighbouring temperatures are 11 to 17 K apart, so nearly every replica moved at each iteration.

## Pitfalls

- **The seed does not make a run repeatable.** The seed fixes the swap proposals and the starting velocities. Runs with 6 replicas still differed between repeats, from the first iteration on. The default run was repeated several times and the energy tables never matched exactly. Report averages over several runs.
- **A short run is a demonstration.** 20 iterations give 20 samples per temperature. Convergence of free energies needs thousands of iterations.
- **Temperature spacing sets the swap rate.** Replica exchange needs neighbouring energy distributions to overlap. The ladder is geometric, so adding replicas or lowering the top temperature raises the rate of swaps.
- **Only a built-in test molecule runs.** Uploading a structure needs the OpenMM force-field setup shown in the [OpenMM guide](openmm.md), then a `ThermodynamicState` built from that system.
- **No GPU.** The recipe runs on the CPU platform with one thread. A 22-atom system gains nothing from a GPU.

## Further reading

- openmmtools documentation: https://openmmtools.readthedocs.io
- Multistate samplers (replica exchange, SAMS): https://openmmtools.readthedocs.io/en/stable/multistate.html
- Source: https://github.com/choderalab/openmmtools
- Paper: Chodera JD, Shirts MR (2011) Replica exchange and expanded ensemble simulations as Gibbs sampling: Simple improvements for enhanced mixing. J Chem Phys 135:194110. https://doi.org/10.1063/1.3660669

---

Cite: Chodera JD, Shirts MR (2011). Replica exchange and expanded ensemble simulations as Gibbs sampling: Simple improvements for enhanced mixing. J Chem Phys 135:194110. doi:10.1063/1.3660669

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openmmtools).
