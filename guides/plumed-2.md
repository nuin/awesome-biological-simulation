# PLUMED 2

> Metadynamics on a model energy landscape with PLUMED's built-in Langevin engine, returning the collective-variable trace, the deposited hills and the reconstructed free-energy profile.

Licence: LGPL-3.0-or-later · [Source code](https://github.com/plumed/plumed2)

## What it simulates

PLUMED 2 is a library that adds enhanced sampling and free-energy methods to a molecular dynamics engine. It reads collective variables (CVs) such as a distance, an angle or a dihedral from the running simulation. It then adds a bias to the forces, for example with metadynamics, umbrella sampling or a harmonic restraint. Engines such as GROMACS, LAMMPS and OpenMM link to it.

Metadynamics adds small Gaussian "hills" along a CV at regular intervals. The hills fill the free-energy wells the system sits in, so it crosses barriers it would otherwise cross rarely. When the wells are filled, the sum of the hills is the negative of the free-energy surface. The well-tempered variant shrinks the hills as they accumulate, so the bias converges.

The recipe does not need a molecular system. PLUMED ships a small Langevin engine, `plumed pesmd`, that moves a particle on an energy landscape you define in the PLUMED input. The default example is a 1D double well, U(x) = 2(x^2 - 1)^2, with minima at x = -1 and x = +1 and a barrier of 2.0 at x = 0, all in reduced units with kB = 1.

## When to use it

- You want to learn how metadynamics settings (hill height, width, pace, bias factor) behave on a landscape where the true answer is known.
- You want to test a PLUMED input file for syntax and CV definitions before using it with a real engine.
- You want a free-energy profile along one CV and plan to run the same input in GROMACS, LAMMPS or another patched engine.

For an actual protein or fluid, run PLUMED through the MD engine: [GROMACS](gromacs.md), [LAMMPS](lammps.md) or [OpenMM](openmm.md). This recipe does not link PLUMED to those engines. It uses pesmd only.

## Install it yourself

Pinned to 2.10.1 (conda-forge, serial build; `nompi*` selects it over the MPI builds):

```
micromamba create -n plumed -c conda-forge "plumed=2.10.1=nompi*"
micromamba activate plumed
plumed info --version
```

`plumed info --version` printed `2.10` in the 2.10.1 image. A pesmd run needs two files: an engine input and a PLUMED input. The engine input used by the recipe's helper `run_plumed.py` is:

```
nstep 100000
tstep 0.005
temperature 0.5
friction 1.0
dimension 1
ipos -1.0
idum 42
periodic false
plumed plumed.dat
```

Run it with `plumed pesmd < pesmd.in`, then `plumed sum_hills --hills HILLS --mintozero --outfile fes.dat`.

## Run the tested example

This recipe builds PLUMED 2 in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1.2 s.

1. Download [plumed-2-recipe.tar.gz](https://biosimhub.pages.dev/guides/plumed-2/plumed-2-recipe.tar.gz) (Dockerfile, run_plumed.py, example plumed_input.dat, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf plumed-2-recipe.tar.gz
   cd plumed-2
   sh run.sh
   ```

![Terminal recording of the PLUMED 2 example run](https://biosimhub.pages.dev/media/plumed-2/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/plumed-2:2.10.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/plumed-2:2.10.1 python /opt/run_plumed.py /work/in/plumed_input.dat \
    --nstep 100000 --temperature 0.5 --friction 1 \
    --tstep 0.005 --dimension 1 --ipos -1 --seed 42 > out/plumed_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `COLVAR` | 38.4 KB |
| `HILLS` | 56.7 KB |
| `fes.dat` | 5.3 KB |
| `pesmd.in` | 132 B |
| `plumed_log.txt` | 194 B |
| `plumed_stdout.txt` | 8.0 KB |

<details><summary>First lines of <code>COLVAR</code></summary>

```
#! FIELDS time d1.x ff metad.bias
 0.000000 -1.000000 0.000000 0.000000
 0.500000 -0.951122 0.018190 0.000000
 1.000000 -1.295391 0.919471 0.000000
 1.500000 -0.668470 0.611945 0.000000
 2.000000 -0.949888 0.019095 0.000189
 2.500000 -1.246597 0.613841 0.269369
 3.000000 -0.504340 1.111961 0.000000
 3.500000 -0.229260 1.795285 0.006256
 4.000000 -0.075754 1.977111 0.000000
 4.500000 0.409344 1.385905 0.000000
 5.000000 1.254187 0.656621 0.000000
```

</details>

<details><summary>First lines of <code>HILLS</code></summary>

```
#! FIELDS time d1.x sigma_d1.x height biasf
#! SET multivariate false
#! SET kerneltype stretched-gaussian
                      1      -1.29539101590225                    0.1                   0.36                      6
                      2    -0.9498884904174316                    0.1     0.3599728478507486                      6
                      3    -0.5043401044532269                    0.1                   0.36                      6
                      4   -0.07575428118505016                    0.1                   0.36                      6
                      5      1.254186507538214                    0.1                   0.36                      6
                      6     0.5771081013532712                    0.1                   0.36                      6
                      7      1.065625596498456                    0.1     0.3528400842344649                      6
                      8      0.871058681592343                    0.1     0.3532629567363325                      6
                      9     0.9460685046650467                    0.1     0.3107635843554553                      6
```

</details>

<details><summary>First lines of <code>fes.dat</code></summary>

```
#! FIELDS d1.x file.free der_d1.x
#! SET min_d1.x -1.94346
#! SET max_d1.x 2.02676
#! SET nbins_d1.x  114
#! SET periodic_d1.x false
   -1.943460000    6.391084026   -0.000000000
   -1.908325310    6.388774604   -0.122602147
   -1.873190619    6.381180479   -0.341268939
   -1.838055929    6.361717957   -0.815947217
   -1.802921239    6.318856337   -1.714071966
   -1.767786549    6.233652974   -3.238884173
   -1.732651858    6.084462788   -5.340531001
```

</details>

<details><summary>First lines of <code>pesmd.in</code></summary>

```
nstep 100000
tstep 0.005
temperature 0.5
friction 1.0
dimension 1
ipos -1.0
idum 42
periodic false
plumed /work/in/plumed_input.dat
```

</details>

<details><summary>First lines of <code>plumed_log.txt</code></summary>

```
pesmd done: 100000 steps, 1001 COLVAR rows, x from -1.59 to 1.67, 64 crossings of x = 0
500 hills deposited
fes.dat: 114 points, minimum 0.00 at -1.07, maximum 6.39 at -1.94
fes at x = 0: 2.235
```

</details>

<details><summary>First lines of <code>plumed_stdout.txt</code></summary>

```
PLUMED: PLUMED is starting
PLUMED: Version: 2.10.1 (git: Unknown) compiled on Aug  1 2026 at 06:14:51
PLUMED: Please cite these papers when using PLUMED [1][2]
PLUMED: For further information see the PLUMED web page at http://www.plumed.org
PLUMED: Root: /opt/conda/lib/plumed
PLUMED: LibraryPath: /opt/conda/bin/../lib/libplumedKernel.so
PLUMED: For installed feature, see /opt/conda/lib/plumed/src/config/config.txt
PLUMED: Molecular dynamics engine: pesmd
PLUMED: Precision of reals: 8
PLUMED: Running over 1 node
PLUMED: Number of threads: 1
PLUMED: Cache line size: 512
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--nstep` | MD steps | 100000 | 1000 to 500000 |
| `--temperature` | Temperature kT (reduced units; keep equal to TEMP in a well-tempered METAD) | 0.5 | 0.05 to 5 |
| `--friction` | Langevin friction | 1 | 0.01 to 10 |
| `--tstep` | Time step (reduced units) | 0.005 | 0.001 to 0.01 |
| `--dimension` | Dimensions of the landscape | 1 | 1 to 3 |
| `--ipos` | Starting position along x | -1 | -5 to 5 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example runs 100,000 steps of dt 0.005 at kT 0.5 with a well-tempered metadynamics bias of height 0.3, width 0.1, bias factor 6 and a hill every 200 steps. The run took 1.2 s on one CPU.

- `plumed_log.txt` has the summary. 1001 CV samples ranged from x = -1.59 to 1.67. The particle crossed x = 0 64 times between samples, so it moved between both wells. 500 hills were deposited.
- `COLVAR` has one row per 100 steps with time, x, the potential ff and the metadynamics bias. The first row is x = -1.0 with potential 0, which is the starting position.
- `HILLS` has one row per hill: time, centre, width, height and bias factor. The first hill has height 0.36. Well-tempered metadynamics shrinks later hills as the bias grows.
- `fes.dat` is the free-energy profile from `plumed sum_hills`, with 114 points between x = -1.94 and 2.03, shifted so its minimum is 0. The minimum is at x = -1.07.

Compare with the exact answer. The profile gave 0.08 at x = -1, 0.19 at x = +1 and 2.23 at x = 0. The exact landscape gives 0, 0 and 2.0. The barrier from the left minimum is 2.23 - 0.08 = 2.15, about 8 percent above 2.0. The ends of the profile (6.39 at x = -1.94) lie in the walls and are less converged.

## Your own runs

Each run below changes one value from the example (seed 42, kT 0.5, 100,000 steps).

- **No bias.** The same landscape without the METAD line crossed x = 0 twice in 100,000 steps, against 64 with the bias. The barrier is 4 kT, so the unbiased particle rarely leaves a well. x ranged from -1.56 to 1.24.
- **Another seed.** `--seed 43` gave 48 crossings. The profile gave 0.40 at x = -1, 0.12 at x = +1 and 2.21 at x = 0. Single runs differ by a few tenths of an energy unit.
- **Fewer steps.** `--nstep 20000` deposited 100 hills and gave 12 crossings. The profile at x = 0 was 2.34 and at x = +1 it was 0.81, against 0 in the exact answer. A shorter run is less converged.
- **Colder engine.** `--temperature 0.25` with the PLUMED input unchanged gave 45 crossings and 2.40 at x = 0. The input still had TEMP=0.5, so the bias factor used a different kT than the dynamics.

## Pitfalls

- **Two atoms.** pesmd has two atoms, and the CV is the distance between them. The example uses `DISTANCE ATOMS=1,2 COMPONENTS` and then `d1.x`. `POSITION ATOM=1` stays at 0 and the particle never moves in the CV.
- **Use `UNITS NATURAL`.** Without it PLUMED treats energies as kJ/mol and TEMP in a well-tempered METAD as kelvin. With kT 0.5 it printed `KbT 0.004157` instead of 0.5.
- **TEMP must equal the engine temperature.** The `temperature` parameter does not edit the PLUMED input.
- **`periodic false` is required.** pesmd stops with an assertion if the engine input has no `periodic` line.
- **Warnings are filtered.** PLUMED prints "Box : input requested but this quantity has not been set" on every step because pesmd passes no box. The helper drops these lines from `plumed_stdout.txt`.
- **Reduced units.** Heights and widths mean nothing in kJ/mol or nm until you map them to a real system.

## Further reading

- PLUMED documentation: https://www.plumed.org/doc
- Metadynamics action (METAD): https://www.plumed.org/doc-v2.10/user-doc/html/_m_e_t_a_d.html
- `plumed sum_hills`: https://www.plumed.org/doc-v2.10/user-doc/html/sum_hills.html
- `plumed pesmd`: https://www.plumed.org/doc-v2.10/user-doc/html/pesmd.html
- Source: https://github.com/plumed/plumed2
- Paper: Tribello GA, Bonomi M, Branduardi D, Camilloni C, Bussi G (2014) PLUMED 2: New feathers for an old bird. Comput Phys Commun 185:604-613. https://doi.org/10.1016/j.cpc.2013.09.018

---

Cite: Tribello GA, Bonomi M, Branduardi D, Camilloni C, Bussi G (2014). PLUMED 2: New feathers for an old bird. Comput Phys Commun 185:604-613. doi:10.1016/j.cpc.2013.09.018

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/plumed-2).
