# OpenMM

> Molecular dynamics of a solvated structure with the AMBER or CHARMM force fields; upload a PDB, get a minimised, equilibrated trajectory back.

Licence: MIT · [Source code](https://github.com/openmm/openmm)

## What it simulates

OpenMM runs classical molecular dynamics from Python. You give it a structure, a force field and an integrator. It minimises the energy, then integrates Newton's equations with a Langevin thermostat. Atoms interact through the AMBER or CHARMM force fields, and PME handles long-range electrostatics in periodic boxes.

The recipe wraps this in one helper script. Input is a PDB file with hydrogens and, for a periodic run, a `CRYST1` box line. Output is a final PDB, a DCD trajectory and a CSV log of energies.

The key assumption is a fixed-charge force field with rigid bonds to hydrogen. Bonds do not break, and the PDB must already contain every hydrogen.

## When to use it

- Short runs of a solvated structure when you want Python control of every step.
- Custom forces and integrators, and GPU speed in a native install.
- Checking a structure with two force fields.

Alternatives: [GROMACS](gromacs.md) is faster for long runs of large biomolecular systems once you have a `.tpr`. [LAMMPS](lammps.md) handles non-biomolecular systems and custom pair potentials.

## Install it yourself

OpenMM 8.6.1 from conda-forge. A dry run resolved `openmm 8.6.1` (Python 3.14 build, 270 MB in total):

```
conda install -c conda-forge openmm=8.6.1
python -m openmm.testInstallation
```

The second command lists the platforms OpenMM can use. The minimal Python script follows the steps in the OpenMM user guide, and the helper makes the same calls:

```python
import openmm as mm, openmm.app as app, openmm.unit as u
pdb = app.PDBFile("water.pdb")
ff = app.ForceField("amber14-all.xml", "amber14/tip3p.xml")
system = ff.createSystem(pdb.topology, nonbondedMethod=app.PME,
                         nonbondedCutoff=0.9*u.nanometer, constraints=app.HBonds)
integ = mm.LangevinMiddleIntegrator(300*u.kelvin, 1/u.picosecond, 2*u.femtosecond)
sim = app.Simulation(pdb.topology, system, integ)
sim.context.setPositions(pdb.positions)
sim.minimizeEnergy()
sim.reporters.append(app.DCDReporter("traj.dcd", 500))
sim.step(5000)
```

## Run the tested example

This recipe builds OpenMM in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 11.3 s.

1. Download [openmm-recipe.tar.gz](https://biosimhub.pages.dev/guides/openmm/openmm-recipe.tar.gz) (Dockerfile, run_md.py, example structure.pdb, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf openmm-recipe.tar.gz
   cd openmm
   sh run.sh
   ```

![Terminal recording of the OpenMM example run](https://biosimhub.pages.dev/media/openmm/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/openmm:8.6.1 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/openmm:8.6.1 python /opt/driver/run_md.py /work/in/structure.pdb \
    --forcefield amber14-tip3p --steps 5000 --temperature 300 \
    --timestep-fs 2 --report-every 500 --seed 42 > out/openmm_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `final.pdb` | 61.4 KB |
| `md_log.csv` | 955 B |
| `openmm_stdout.txt` | 489 B |
| `trajectory.dcd` | 91.8 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/openmm/result-dark.png"><img src="https://biosimhub.pages.dev/media/openmm/result.png" alt="Plot of the OpenMM example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>final.pdb</code></summary>

```
REMARK   1 CREATED WITH OPENMM 8.6.1, 2026-10-12
CRYST1   20.000   20.000   20.000  90.00  90.00  90.00 P 1           1 
HETATM    1  O   HOH A   1      11.753   8.405   7.214  1.00  0.00           O  
HETATM    2  H1  HOH A   1      11.505   7.807   7.920  1.00  0.00           H  
HETATM    3  H2  HOH A   1      12.661   8.178   7.015  1.00  0.00           H  
HETATM    4  O   HOH A   2       1.727   1.207   1.429  1.00  0.00           O  
HETATM    5  H1  HOH A   2       2.542   1.383   1.899  1.00  0.00           H  
HETATM    6  H2  HOH A   2       1.638   0.255   1.450  1.00  0.00           H  
HETATM    7  O   HOH A   3      14.074  13.317   0.533  1.00  0.00           O  
HETATM    8  H1  HOH A   3      14.244  14.239   0.727  1.00  0.00           H  
HETATM    9  H2  HOH A   3      14.818  13.044  -0.004  1.00  0.00           H  
HETATM   10  O   HOH A   4       6.710   7.118   5.173  1.00  0.00           O  
```

</details>

<details><summary>First lines of <code>md_log.csv</code></summary>

```
#"Step","Time (ps)","Potential Energy (kJ/mole)","Kinetic Energy (kJ/mole)","Temperature (K)","Speed (ns/day)"
500,1.0000000000000007,-10515.12035973148,1642.151334225499,255.67043146130163,0
1000,2.0000000000000013,-10476.164531064793,1962.4468244030877,305.5379951030141,96.8
1500,2.999999999999891,-10241.54106016235,1898.3302388748054,295.555532010736,92.7
2000,3.999999999999781,-10380.22235329227,1925.1373706818306,299.7291978675278,91
2500,4.999999999999671,-10444.947285962864,1883.5838870049377,293.25963755419525,89.9
3000,5.999999999999561,-10472.36811978893,1892.5847797329627,294.66100786602243,90.3
3500,6.999999999999451,-10440.918843103214,1889.8987596526474,294.24281503657056,89.7
4000,7.999999999999341,-10485.432008100315,1971.1240193236374,306.88896813635944,90
4500,8.999999999999675,-10275.797583175465,1876.9043008523117,292.2196769622378,90.7
5000,10.000000000000009,-10238.216245246693,2013.5761958732892,313.4984480720439,91.6
```

</details>

<details><summary>First lines of <code>openmm_stdout.txt</code></summary>

```
#"Step","Potential Energy (kJ/mole)","Temperature (K)"
500,-10515.12035973148,255.67043146130163
1000,-10476.164531064793,305.5379951030141
1500,-10241.54106016235,295.555532010736
2000,-10380.22235329227,299.7291978675278
2500,-10444.947285962864,293.25963755419525
3000,-10472.36811978893,294.66100786602243
3500,-10440.918843103214,294.24281503657056
4000,-10485.432008100315,306.88896813635944
4500,-10275.797583175465,292.2196769622378
5000,-10238.216245246693,313.4984480720439
done
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--forcefield` | Force field and water model | amber14-tip3p | amber14-tip3p, amber14-tip3pfb, charmm36-tip3p |
| `--steps` | MD steps | 5000 | 1 to 200000 |
| `--temperature` | Temperature (K) | 300 | 1 to 1000 |
| `--timestep-fs` | Time step (fs) | 2 | 0.5 to 4 |
| `--report-every` | Report interval (steps) | 500 | 1 to 100000 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper `run_md.py` reads the PDB, builds the system (PME with a 0.9 nm cutoff if the PDB has a box, no cutoff if it does not), constrains bonds to hydrogen, and uses a Langevin middle integrator with friction 1/ps. It runs on the CPU platform with two threads. It minimises for at most 200 iterations, assigns velocities at the target temperature using the seed, then runs. It writes a DCD frame and a CSV row every `report_every` steps.

The example box is 20 A on a side (`CRYST1 20.000`) with 774 atoms, which is 258 water molecules. At 2 fs per step, 5000 steps is 10 ps.

- `md_log.csv` (955 bytes) has 10 rows, at steps 500 to 5000. Columns: step, time in ps, potential energy and kinetic energy in kJ/mole, temperature in K, speed in ns/day.
- At 1 ps the potential energy is -10515 kJ/mole and the temperature 255.7 K. At 10 ps they are -10238 kJ/mole and 313.5 K. Frames in between sit between 292 and 307 K.
- `trajectory.dcd` (93956 bytes) holds 10 frames. `final.pdb` (62846 bytes) holds the last coordinates, wrapped into the box.
- `openmm_stdout.txt` repeats step, potential energy and temperature every 500 steps and ends with `done`.

The temperature of 774 atoms fluctuates by about 10 K from frame to frame. Judge the average over many frames.

## Your own runs

```
dr() { docker run --rm --user "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out "$@"; }
dr biosimhub/openmm:8.6.1 python /opt/driver/run_md.py /work/in/structure.pdb --forcefield charmm36-tip3p --steps 5000
```

Each run below used 5000 steps and was averaged over its last five frames.

1. Default (amber14-tip3p, 300 K, seed 42): mean 301.4 K, potential energy -10353.9 kJ/mole.
2. `--forcefield charmm36-tip3p`: 299.4 K and -10373.7 kJ/mole.
3. `--temperature 350`: 348.7 K and -9735.2 kJ/mole. The potential energy rose by 619 kJ/mole.
4. `--seed 7`: 298.9 K and -10309.3 kJ/mole.

The seed alone moved the potential energy by 45 kJ/mole, which is more than the 20 kJ/mole gap between the two force fields. Compare force fields only over longer runs with several seeds.

## Pitfalls

- OpenMM needs a structure with hydrogens. Add every hydrogen before you upload.
- Without a `CRYST1` line the helper runs with no cutoff and no periodic box. A bulk liquid needs the periodic box, so put it in `CRYST1`.
- Energies are in kJ/mole and the box is in nm inside OpenMM. PDB files use angstroms.
- The first frame is not at equilibrium. The default log reads 255.7 K at 1 ps. Discard early frames.
- Time step above 2 fs needs the bond-to-hydrogen constraints that the helper turns on. Check that the energy stays stable at larger steps.

## Further reading

- OpenMM user guide, running simulations: https://docs.openmm.org/latest/userguide/application/02_running_sims.html
- Getting started and installation: https://docs.openmm.org/latest/userguide/application/01_getting_started.html
- Cookbook: https://openmm.github.io/openmm-cookbook/latest/index.html
- Source: https://github.com/openmm/openmm
- Eastman P et al. (2017) PLoS Comput Biol 13:e1005659. https://doi.org/10.1371/journal.pcbi.1005659

---

Cite: Eastman P et al. (2017). OpenMM 7: Rapid development of high performance algorithms for molecular dynamics. PLoS Comput Biol 13:e1005659. doi:10.1371/journal.pcbi.1005659

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openmm).
