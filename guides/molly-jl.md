# Molly.jl

> Molecular dynamics of a Lennard-Jones gas in Julia with an Andersen thermostat, returning an XYZ trajectory, an energy log and the radial distribution function.

Licence: MIT · [Source code](https://github.com/JuliaMolSim/Molly.jl)

## What it simulates

Molly.jl is a molecular dynamics package written in Julia. It integrates Newton's equations for atoms with pairwise potentials (Lennard-Jones, Coulomb), bonded terms, thermostats and barostats. It handles protein force fields, and it supports automatic differentiation through simulations, which is used to fit force fields.

The recipe runs the simplest case. A gas of argon-like Lennard-Jones atoms is placed at random in a cubic periodic box, given random velocities at the target temperature and integrated with velocity Verlet. An Andersen thermostat keeps the temperature near the target by resampling velocities at random.

The key assumptions are one atom type, a Lennard-Jones potential cut off at the smaller of 1.2 nm and half the box, and a constant-volume box. Units are real: nm, ps, K and kJ/mol, with sigma 0.34 nm, epsilon 0.998 kJ/mol and mass 39.948 g/mol as defaults.

## When to use it

- You write or extend simulation code in Julia and want a native MD package.
- You want to differentiate through a simulation, for example to fit force-field parameters to data.
- You want a small, scriptable MD example to adapt.

For all-atom proteins with a mature toolchain, use [GROMACS](gromacs.md) or [OpenMM](openmm.md). For input-script MD with many potentials, use [LAMMPS](lammps.md). This recipe uses the CPU and one thread. Molly.jl also runs on GPUs through Julia packages, which the recipe does not use.

## Install it yourself

Pinned to Molly 0.23.3 on Julia 1.11.3. The recipe fixes all 1030 lines of dependency versions in a `Manifest.toml`. With Julia installed:

```
julia -e 'using Pkg; Pkg.add(name="Molly", version="0.23.3")'
julia -e 'using Molly; println(pkgversion(Molly))'
```

The first install downloads and compiles the dependencies and took about 2 minutes in the container build. The recipe's image is 2.04 GB on disk because it holds the compiled packages. The first `using Molly` in a new session is the slow step, so the image precompiles at build time.

A minimal script, close to the one in the Molly documentation:

```julia
using Molly
atoms = [Atom(mass=39.948u"g/mol", σ=0.34u"nm", ϵ=0.998u"kJ * mol^-1") for _ in 1:100]
boundary = CubicBoundary(3.0u"nm")
coords = place_atoms(100, boundary; min_dist=0.3u"nm")
sys = System(atoms=atoms, coords=coords, boundary=boundary,
    velocities=[random_velocity(39.948u"g/mol", 120.0u"K") for _ in 1:100],
    pairwise_inters=(LennardJones(),),
    energy_units=u"kJ * mol^-1", force_units=u"kJ * mol^-1 * nm^-1")
simulate!(sys, VelocityVerlet(dt=0.002u"ps", coupling=AndersenThermostat(120.0u"K", 1.0u"ps")), 1000)
```

The recipe's script `run_molly.jl` adds loggers, the cutoff, the output files and the radial distribution function.

## Run the tested example

This recipe builds Molly.jl in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 8.5 s.

1. Download [molly-jl-recipe.tar.gz](https://biosimhub.pages.dev/guides/molly-jl/molly-jl-recipe.tar.gz) (Dockerfile, Manifest.toml, Project.toml, run_molly.jl, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf molly-jl-recipe.tar.gz
   cd molly-jl
   sh run.sh
   ```

![Terminal recording of the Molly.jl example run](https://biosimhub.pages.dev/media/molly-jl/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/molly-jl:0.23.3 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/molly-jl:0.23.3 julia /opt/run_molly.jl --n-atoms 100 --box 3 \
    --temperature 120 --steps 5000 --dt 0.002 \
    --sigma 0.34 --epsilon 0.998 --coupling 1 \
    --seed 42 > out/molly_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `log.csv` | 3.9 KB |
| `molly_log.txt` | 212 B |
| `rdf.csv` | 1.1 KB |
| `trajectory.xyz` | 261.3 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/molly-jl/result-dark.png"><img src="https://biosimhub.pages.dev/media/molly-jl/result.png" alt="Plot of the Molly.jl example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>log.csv</code></summary>

```
step,time_ps,temperature_K,potential_kJ_mol,kinetic_kJ_mol
0,0.0000,109.326,-54.3821,134.9842
50,0.1000,126.364,-82.1097,156.0210
100,0.2000,132.127,-87.5755,163.1374
150,0.3000,122.994,-82.3202,151.8602
200,0.4000,130.235,-83.7506,160.8011
250,0.5000,131.209,-81.8998,162.0040
300,0.6000,128.259,-82.7186,158.3612
350,0.7000,119.778,-82.2766,147.8894
400,0.8000,125.219,-85.1153,154.6080
450,0.9000,115.324,-83.0572,142.3899
500,1.0000,118.028,-92.8774,145.7287
```

</details>

<details><summary>First lines of <code>molly_log.txt</code></summary>

```
Molly 0.23.3, Julia 1.11.3, 100 atoms, box 3.0 nm, 5000 steps
mean temperature 116.5 K (target 120.0), second half
g(r) first peak 2.61 at r = 0.384 nm
mean potential -124.787 kJ/mol, mean kinetic 143.838 kJ/mol
```

</details>

<details><summary>First lines of <code>rdf.csv</code></summary>

```
r_nm,g_r
0.0094,0.0000
0.0281,0.0000
0.0469,0.0000
0.0656,0.0000
0.0844,0.0000
0.1031,0.0000
0.1219,0.0000
0.1406,0.0000
0.1594,0.0000
0.1781,0.0000
0.1969,0.0000
```

</details>

<details><summary>First lines of <code>trajectory.xyz</code></summary>

```
100
Lattice="30.0 0 0 0 30.0 0 0 0 30.0"
Ar 18.8804 13.5102 14.3222
Ar 21.0939 20.2004 4.9768
Ar 18.4043 20.0502 13.7109
Ar 8.9810 19.8343 19.1829
Ar 10.2794 8.0361 15.4761
Ar 2.7007 8.1797 5.7469
Ar 12.7077 14.5411 2.4173
Ar 15.4605 5.8953 18.0154
Ar 11.9312 9.4779 13.0238
Ar 25.7602 9.5890 16.9100
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--n-atoms` | Number of atoms | 100 | 10 to 300 |
| `--box` | Cubic box edge (nm) | 3 | 2 to 10 |
| `--temperature` | Thermostat temperature (K) | 120 | 20 to 500 |
| `--steps` | MD steps | 5000 | 500 to 50000 |
| `--dt` | Time step (ps) | 0.002 | 0.0005 to 0.005 |
| `--sigma` | Lennard-Jones sigma (nm) | 0.34 | 0.2 to 0.5 |
| `--epsilon` | Lennard-Jones epsilon (kJ/mol) | 0.998 | 0.1 to 3 |
| `--coupling` | Andersen thermostat coupling time (ps) | 1 | 0.1 to 10 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example places 100 atoms in a 3 nm box and runs 5,000 steps of 0.002 ps (10 ps) at 120 K. The capture took 8.5 s on one CPU, most of it Julia start-up and compiling the first call.

- `molly_log.txt` has the summary for the second half of the run. Mean temperature is 116.5 K against a target of 120.0. Mean potential energy is -124.787 kJ/mol and mean kinetic energy is 143.838 kJ/mol. The first g(r) peak is 2.61 at r = 0.384 nm.
- `log.csv` has 101 rows, one per 50 steps, with temperature, potential and kinetic energy. Temperature in the second half ranges from 104.8 to 138.1 K, a wide spread for 100 atoms.
- `trajectory.xyz` has 101 frames of 100 atoms in Angstrom, with the box in the comment line (30.0 A).
- `rdf.csv` has 80 bins out to half the box, 1.5 nm.

Check the numbers. For 100 atoms, 3/2 N kB T at 120 K is 149.6 kJ/mol, and the kinetic energy of 143.8 kJ/mol matches a temperature of 116.5 K. The g(r) peak at 0.384 nm sits at 1.13 sigma, where the Lennard-Jones minimum (2^(1/6) sigma = 0.382 nm) is. The potential energy of -1.25 kJ/mol per atom shows that the atoms cluster: the density is 3.7 atoms/nm^3, and argon at 120 K is below its critical temperature (about 150 K).

## Your own runs

Each run below changes values from the example (seed 42, 100 atoms, 3 nm, 120 K, 5000 steps).

- **Hot gas.** `--temperature 300` gave a mean temperature of 293.3 K, a potential energy of -86.9 kJ/mol and a first peak of 1.53 at 0.366 nm. Faster atoms clump less, so the peak falls from 2.61 to 1.53.
- **Dilute gas.** `--box 6` gave -14.2 kJ/mol and a peak of 2.21 at 0.394 nm. The density is 8 times lower, so the potential energy is about 9 times weaker.
- **Dense system.** `--n-atoms 200 --box 2.5 --temperature 100 --steps 10000` gave a mean temperature of 100.6 K, a potential energy of -739.6 kJ/mol (-3.70 per atom) and a peak of 2.38 at 0.383 nm.
- **Another seed.** `--seed 43` gave a mean temperature of 118.2 K, a potential energy of -123.2 kJ/mol and a first peak of 2.35. The peak height moved from 2.61 to 2.35 with only 100 atoms, so report averages over several seeds.

## Pitfalls

- **Start-up time.** Julia compiles the first call of each function. The 8.5 s run spends most of its time before the first step. A longer run costs little more per step.
- **Density limit.** The helper stops when the reduced density n sigma^3 / V is above 0.7. For 300 atoms in a 2 nm box it printed "reduced density 1.47 is above 0.7". Random placement fails in a box that full.
- **Fluctuations are large.** 100 atoms give temperature samples from 104.8 to 138.1 K in the second half. Use more atoms or longer runs for averages.
- **Thermostat.** The Andersen thermostat randomises velocities, so it destroys dynamical properties such as diffusion. Use it for equilibrium averages.
- **Units.** Molly attaches units to quantities such as lengths, masses and energies. The recipe's script strips them with `ustrip` before writing files.

## Further reading

- Documentation: https://juliamolsim.github.io/Molly.jl/stable/
- Source: https://github.com/JuliaMolSim/Molly.jl
- Paper: Greener JG (2024) Differentiable simulation to develop molecular dynamics force fields for disordered proteins. Chem Sci 15:4897-4909. https://doi.org/10.1039/D3SC05230C

---

Cite: Greener JG (2024). Differentiable simulation to develop molecular dynamics force fields for disordered proteins. Chem Sci 15:4897-4909. doi:10.1039/D3SC05230C

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/molly-jl).
