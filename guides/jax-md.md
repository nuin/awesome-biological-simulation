# JAX MD

> Differentiable molecular dynamics in JAX, run as a fixed Lennard-Jones fluid simulation (NVT Langevin or NVE) with a thermodynamic log and trajectory.

Licence: Apache-2.0 · [Source code](https://github.com/jax-md/jax-md)

## What it simulates

JAX MD is a molecular dynamics library written in JAX. Simulations are Python functions that turn one state into the next, so they compile with XLA and can run on CPU, GPU or TPU. They are also differentiable: you can take derivatives of an outcome with respect to a parameter.

The recipe runs one fixed system: a Lennard-Jones fluid of identical particles in a periodic cubic box, in reduced units (sigma = epsilon = mass = 1). You choose the particle count, number density, temperature, ensemble (NVT Langevin or NVE), time step, step count, report interval and seed. Output is a thermodynamic CSV and the positions of every reported frame.

The key assumption is classical dynamics on a pair potential. The helper sums over all particle pairs, with no neighbour list.

## When to use it

- Teaching and quick tests of liquid behaviour: temperature relaxation, equipartition, energy conservation.
- Research code that needs gradients through a simulation, or custom potentials, such as neural network potentials, written in Python.

Alternatives: [LAMMPS](lammps.md) runs the same Lennard-Jones fluid with a neighbour list and scales to far more atoms. [OpenMM](openmm.md) and [GROMACS](gromacs.md) fit real biomolecular force fields.

## Install it yourself

JAX MD 0.2.29 from conda-forge. A dry run resolved `jax-md 0.2.29` with `jax 0.10.2` and a CPU `jaxlib 0.10.2` (354 MB in total):

```
conda install -c conda-forge jax-md=0.2.29
```

The project README also gives `python -m pip install jax-md --upgrade`. For a GPU, follow the JAX GPU instructions. The jax-md install alone does not enable it.

A minimal script (the same calls as the helper, 1000 steps):

```python
import numpy as np, jax.numpy as jnp
from jax import random, lax
from jax_md import energy, simulate, space

n, density = 256, 0.8
box = (n / density) ** (1 / 3)
displacement, shift = space.periodic(box)
energy_fn = energy.lennard_jones_pair(displacement, sigma=1.0, epsilon=1.0)
init, apply = simulate.nvt_langevin(energy_fn, shift, 0.005, kT=1.0, gamma=1.0)

side = 7  # 7**3 = 343 grid sites, first 256 used
grid = np.stack(np.meshgrid(*[np.arange(side)] * 3, indexing="ij"), -1).reshape(-1, 3)[:n]
R = jnp.asarray((grid + 0.5) * (box / side))

key = random.PRNGKey(42)
state = init(key, R, mass=1.0)
state = lax.fori_loop(0, 1000, lambda _, s: apply(s), state)
print("PE per particle:", float(energy_fn(state.position)) / n)
```

This prints `-4.89067793039538`, the same value as step 1000 in the example's `thermo.csv`. The recipe's image sets `JAX_ENABLE_X64=1` and `JAX_PLATFORMS=cpu`.

## Run the tested example

This recipe builds JAX MD in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 12.3 s.

1. Download [jax-md-recipe.tar.gz](https://biosimhub.pages.dev/guides/jax-md/jax-md-recipe.tar.gz) (Dockerfile, run_lj.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf jax-md-recipe.tar.gz
   cd jax-md
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/jax-md:0.2.29 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/jax-md:0.2.29 python /opt/driver/run_lj.py --particles 256 \
    --density 0.8 --temperature 1 --ensemble nvt \
    --dt 0.005 --steps 5000 --report-every 100 \
    --seed 42 > out/jaxmd_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `jaxmd_stdout.txt` | 43 B |
| `thermo.csv` | 3.1 KB |
| `trajectory.npz` | 287.8 KB |

<details><summary>First lines of <code>jaxmd_stdout.txt</code></summary>

```
done: 256 particles, box 6.840, 5000 steps
```

</details>

<details><summary>First lines of <code>thermo.csv</code></summary>

```
step,potential_energy,kinetic_energy,temperature
0,-1.6424193161613774,1.583344863963279,1.055563242642186
100,-4.262105603879149,2.9777984913557414,1.9851989942371608
200,-4.632197700480043,2.284483472128754,1.5229889814191695
300,-4.840928712783134,1.8229576597924182,1.2153051065282787
400,-4.903961137004881,1.6419917445127203,1.0946611630084802
500,-4.915091932834674,1.5689922379344838,1.0459948252896558
600,-4.990471000686762,1.3975286672181009,0.9316857781454005
700,-4.942926965034976,1.38776870438913,0.92517913625942
800,-5.037475569161884,1.4077550223075361,0.9385033482050241
900,-4.910052124831772,1.3933176062582102,0.9288784041721402
1000,-4.89067793039538,1.3344172575782296,0.889611505052153
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--particles` | Particles | 256 | 8 to 2000 |
| `--density` | Number density (reduced units) | 0.8 | 0.05 to 1.2 |
| `--temperature` | Temperature kT (reduced units) | 1 | 0.1 to 5 |
| `--ensemble` | Ensemble | nvt | nvt, nve |
| `--dt` | Time step (reduced units) | 0.005 | 0.0005 to 0.01 |
| `--steps` | MD steps | 5000 | 100 to 100000 |
| `--report-every` | Report interval (steps) | 100 | 10 to 10000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example is 256 particles at density 0.8, so the box side is (256 / 0.8)^(1/3) = 6.840. It runs NVT Langevin at kT = 1 with friction 1, dt 0.005, 5000 steps, reporting every 100 steps. The recipe's helper starts the particles on a 7 x 7 x 7 grid (the first 256 sites) and draws velocities from the seed.

`thermo.csv` (3224 bytes) has 51 rows (step 0 to 5000). Energies are per particle. Temperature is 2 x kinetic energy / (3 N).

- Step 0: potential energy -1.642, temperature 1.056. The grid sits far from the liquid's equilibrium.
- Step 100: potential energy -4.262, temperature 1.985. Falling potential energy heats the fluid.
- Step 500: -4.915 and 1.046. Step 1000: -4.891 and 0.890.
- Step 5000: -4.981 and 0.980. The mean temperature over the second half of the run is 0.975, so the Langevin thermostat holds kT = 1.

`trajectory.npz` (294677 bytes) holds `positions` with shape (51, 256, 3) and the scalar `box` (6.840). `jaxmd_stdout.txt` reads `done: 256 particles, box 6.840, 5000 steps`. The run took 12.3 s.

## Your own runs

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out "$@"; }
dr biosimhub/jax-md:0.2.29 python /opt/driver/run_lj.py --ensemble nve --steps 5000
```

1. NVE (`--ensemble nve`), other values at default. Total energy per particle stayed at -0.128 (step 0) and -0.126 (step 5000). The temperature rose from 1.009 to 2.546 (mean 2.466 over the second half), because the grid start sits above the equilibrium potential energy and NVE turns that into heat.
2. A dilute hot gas: `--temperature 2.0 --density 0.3`. The box grew to 9.485. The mean temperature over the second half was 2.046, and the potential energy rose from -1.934 to -1.642.
3. The same seed twice. The 1000-step script above reproduced the example's step-1000 value to all printed digits.

## Pitfalls

- A random start overlaps particles. A uniform random start of the same 256 particles gave a potential energy of 1.7e14 per particle after 200 steps. Start from a lattice, as the helper does.
- The recipe's image sets `JAX_ENABLE_X64=1`. Set it in a native run too if you want to reproduce the example's digits.
- NVE does not hold the temperature you pass. The value only sets the initial momenta.
- Everything is in reduced units. Map to argon (or another fluid) with your own sigma, epsilon and mass.
- All-pairs energy grows with N squared, and the recipe limits runs to 2000 particles.
- The recipe's helper wraps each report block in `jit`, so the 12 s wall time for 5000 steps includes compile time.

## Further reading

- JAX MD reference and examples: https://jax-md.readthedocs.io
- Source and install notes: https://github.com/jax-md/jax-md
- Schoenholz SS, Cubuk ED (2021) J Stat Mech 2021:124016. https://doi.org/10.1088/1742-5468/ac3ae9

---

Cite: Schoenholz SS, Cubuk ED (2021). JAX, M.D. A framework for differentiable physics. J Stat Mech 2021:124016. doi:10.1088/1742-5468/ac3ae9

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/jax-md).
