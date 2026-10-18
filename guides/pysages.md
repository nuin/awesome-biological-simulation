# PySAGES

> Estimate the free energy along the distance of a Lennard-Jones dimer with adaptive biasing force or metadynamics, and compare it with the exact curve.

Licence: GPL-3.0-or-later (MIT for most files; abf.py is GPL-3.0-or-later) · [Source code](https://github.com/SSAGESLabs/PySAGES)

## What it simulates

PySAGES is a Python library of advanced-sampling methods for molecular dynamics: adaptive biasing force (ABF), metadynamics, umbrella integration, string methods and others. It does not run the dynamics. It attaches to an MD engine (OpenMM, HOOMD-blue, LAMMPS, ASE or JAX MD), reads positions and forces at each step, adds a bias along collective variables you choose and returns a free-energy estimate. The methods are written in JAX, so they can use a GPU when the engine does.

The recipe runs the smallest system where the answer is known: two particles with a Lennard-Jones interaction (epsilon = 1 eV, sigma = 1 A, 40 amu each) in a periodic 8 A box, driven by ASE's Langevin dynamics. The collective variable is the distance r between them. For two particles the exact free energy along r is A(r) = V(r) - 2 kT ln r, where the second term comes from the r-squared volume element. The helper writes the PySAGES curve next to this exact curve.

You choose the method (ABF or metadynamics), kT, friction, time step, step count, number of bins, the upper end of the distance grid and the seed.

## When to use it

Use PySAGES when you want to compute a free-energy profile or surface along collective variables, and your engine is one of the supported ones.

- Use [OpenMM](openmm.md), [LAMMPS](lammps.md) or [GROMACS](gromacs.md) alone for unbiased dynamics.
- Use [OpenPathSampling](openpathsampling.md) when you want the transition paths themselves and not a free-energy profile.
- Use [JAX MD](jax-md.md) for differentiable, custom-potential MD without enhanced sampling.

## Install it yourself

PySAGES 0.5.1 is on conda-forge, with ASE 3.29.0 for the engine. The recipe's image resolved them with Python 3.14.8, JAX 0.10.2 (CPU jaxlib), NumPy 2.5.4 and numba 0.68.0, and came to 1.97 GB:

```
micromamba create -n pysages -c conda-forge pysages=0.5.1 ase=3.29.0
```

Other engines are separate installs. A minimal script with the calls the helper makes, for 10,000 ABF steps:

```python
import numpy as np
import pysages
from ase import Atoms
from ase.calculators.lj import LennardJones
from ase.md import Langevin
from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from pysages.colvars import Distance
from pysages.grids import Grid
from pysages.methods import ABF, CVRestraints

KB = 8.617333262e-5

def generate_simulation(**kwargs):
    atoms = Atoms("Ar2", positions=[[0, 0, 0], [1.12, 0, 0]], cell=[8, 8, 8], pbc=True)
    atoms.set_masses([40.0, 40.0])
    atoms.calc = LennardJones(epsilon=1.0, sigma=1.0, rc=3.0)
    rng = np.random.default_rng(42)
    MaxwellBoltzmannDistribution(atoms, temperature_K=0.3 / KB, rng=rng)
    return Langevin(atoms, 0.01, temperature_K=0.3 / KB, friction=0.1, rng=rng, logfile=None)

walls = CVRestraints(lower=np.array([0.9]), upper=np.array([3.0]),
                     kl=np.array([50.0]), ku=np.array([50.0]))
method = ABF([Distance([0, 1])], Grid(lower=0.95, upper=3.0, shape=40), restraints=walls)
result = pysages.run(method, generate_simulation, 10000)
analysis = pysages.analyze(result)
fe, mesh = (np.asarray(analysis[k]).reshape(-1) for k in ("free_energy", "mesh"))
print("minimum at r = %.3f, range %.2f" % (mesh[fe.argmin()], fe.max() - fe.min()))
```

This printed `minimum at r = 1.129, range 0.63`. With 30,000 steps the range was 1.20. `pysages.run` takes a function that builds the simulation, and PySAGES wraps whatever it returns.

## Run the tested example

This recipe builds PySAGES in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 35.6 s.

1. Download [pysages-recipe.tar.gz](https://biosimhub.pages.dev/guides/pysages/pysages-recipe.tar.gz) (Dockerfile, run_dimer.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pysages-recipe.tar.gz
   cd pysages
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/pysages:0.5.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pysages:0.5.1 python /opt/run_dimer.py --method abf --kt 0.3 \
    --friction 0.1 --dt 0.01 --steps 30000 --bins 40 \
    --upper 3 --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `fes.csv` | 1.1 KB |
| `run_log.txt` | 263 B |
| `summary.json` | 284 B |

<details><summary>First lines of <code>fes.csv</code></summary>

```
r,free_energy_pysages,free_energy_exact,visits
0.9756,1.1983,1.8267,178
1.0269,0.4638,0.5539,510
1.0781,0.1144,0.1014,1042
1.1294,0.0000,0.0000,1777
1.1806,0.0062,0.0404,1448
1.2319,0.0607,0.1295,1864
1.2831,0.1319,0.2267,1070
1.3344,0.2172,0.3156,762
1.3856,0.3162,0.3907,686
1.4369,0.4042,0.4513,734
1.4881,0.4466,0.4988,754
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
{"method": "abf", "kT": 0.3, "friction": 0.1, "dt": 0.01, "steps": 30000, "bins": 40, "grid": [0.95, 3.0], "seed": 42, "minimum_r_pysages": 1.1294, "minimum_r_exact": 1.1294, "rmse_vs_exact_1.0_to_2.5
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "method": "abf",
 "kT": 0.3,
 "friction": 0.1,
 "dt": 0.01,
 "steps": 30000,
 "bins": 40,
 "grid": [
  0.95,
  3.0
 ],
 "seed": 42,
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--method` | Sampling method | abf | abf, metad |
| `--kt` | Temperature kT (eV) | 0.3 | 0.2 to 1 |
| `--friction` | Langevin friction (1/ASE time) | 0.1 | 0.01 to 2 |
| `--dt` | Time step (ASE time units) | 0.01 | 0.002 to 0.02 |
| `--steps` | MD steps | 30000 | 1000 to 100000 |
| `--bins` | Bins along the distance | 40 | 10 to 100 |
| `--upper` | Upper end of the distance grid (A) | 3 | 2 to 3.5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is ABF at kT = 0.3 eV (the well is 3.3 kT deep), friction 0.1, time step 0.01, 30,000 steps, 40 bins from 0.95 to 3.0 A, seed 42. It took 35.6 s.

- `summary.json` (284 bytes): the free-energy minimum is at r = 1.1294 A, the same bin as the exact curve. The RMS difference from the exact curve over 1.0 to 2.5 A is 0.163 eV (after setting each curve's minimum to zero).
- `fes.csv` (1114 bytes) has 40 rows: r, the PySAGES free energy, the exact free energy and the number of visits to the bin. The bin at 1.1294 A is zero in both columns and has 1777 visits. The repulsive wall at 0.9756 A is 1.198 eV in PySAGES and 1.827 eV in the exact curve, with only 178 visits.
- The barrier between the bound state and the open state peaks at 0.493 eV near 1.80 A in PySAGES. The exact peak is 0.605 eV at 1.85 A. At 3.0 A the exact curve is 0.412 eV and PySAGES gives 0.114 eV, so the open state is too low by about 0.3 eV.
- The visit counts run from 178 to 3062 per bin. ABF pushes the dimer across the whole grid, so no bin stays empty.
- `run_log.txt` repeats the summary line.

The shape is right, with the well, barrier and plateau in the correct places. The 0.3 eV offset at large r is sampling error from one 30,000-step trajectory.

## Your own runs

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/out:/work/out" -w /work/out "$@"; }
dr biosimhub/pysages:0.5.1 python /opt/run_dimer.py --method metad --kt 0.3 --friction 0.1 --dt 0.01 --steps 30000 --bins 40 --upper 3.0 --seed 42
```

1. Metadynamics (`--method metad`): minimum at 1.1294 A, RMS difference 0.298 eV, highest value 1.668 eV, 28.3 s. Hills of height 0.05 eV and width 0.05 A are added every 50 steps. The metadynamics curve is further from the exact one than ABF at the same step count.
2. Another seed (7) with ABF: RMS difference 0.173 eV and highest value 1.023 eV. The minimum is again at 1.1294 A.
3. kT = 0.6 with ABF: RMS difference 0.124 eV. The minimum moves to 2.9744 A, and the exact curve also has its minimum there, since the well is only 1.7 kT deep and the volume term wins.
4. The same seed twice gave identical `fes.csv` files.

## Pitfalls

- Keep the collective variable inside the grid. Without the restraint walls, the dimer left the 0.95 to 3.0 A grid. The 10,000-step and 30,000-step runs of the minimal script then both printed `minimum at r = 2.974, range 0.52`.
- Time steps matter for ABF. At dt = 0.02, friction 0.1 and 30,000 steps the minimum landed at 2.9744 A and the RMS difference rose to 0.228 eV. At dt = 0.01 it was 0.163 eV and the minimum was at 1.1294 A. A test with 1 amu particles at dt = 0.005 and friction 1 also put the minimum at 2.9744 A, so the recipe uses 40 amu particles.
- Near 2 kT well depth the bound and open states are equally likely, so the minimum can sit at either end. The recipe limits kT to 0.2 to 1.0 eV.
- The helper's "exact" curve ignores the periodic box and uses a 3 A cutoff, so it is a reference and not a convergence criterion.
- Each ABF bin needs many visits. Raise `--steps` or reduce `--bins` if the curve is noisy.

## Further reading

- PySAGES documentation and examples: https://github.com/SSAGESLabs/PySAGES
- ASE documentation: https://ase-lib.org
- Zubieta Rico P et al. (2024) npj Comput Mater 10:35. https://doi.org/10.1038/s41524-023-01189-z

---

Cite: Zubieta Rico P, Schneider L, Perez-Lemus GR, et al. (2024). PySAGES: flexible, advanced sampling methods accelerated with GPUs. npj Comput Mater 10:35. doi:10.1038/s41524-023-01189-z

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pysages).
