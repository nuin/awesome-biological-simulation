# GOMC

> Monte Carlo simulation of fluids in the Gibbs ensemble, for phase equilibria and densities of coexisting phases.

Licence: MIT · [Source code](https://github.com/GOMC-WSU/GOMC)

## What it simulates

GOMC is a Monte Carlo engine for molecular systems. It does not integrate equations of motion. It proposes random moves, accepts or rejects them by the Metropolis rule, and samples the chosen statistical ensemble. The repository's README describes it as a parallel code for large systems that runs on CPUs, with or without OpenMP, and on NVIDIA GPUs.

Four ensembles are built as separate executables: NVT (fixed volume), NPT (fixed pressure), GEMC (Gibbs ensemble, two boxes that exchange volume and molecules) and GCMC (grand canonical, fixed chemical potential). Moves include displacement, rotation, volume change, molecule swap and configurational-bias moves for chain molecules.

Typical results are densities, vapour-liquid coexistence, vapour pressures, adsorption isotherms and chemical potentials.

## When to use it

Use GOMC when the question is about equilibrium properties of fluids and the path in time does not matter. Gibbs ensemble runs give coexistence curves in one simulation. GCMC runs give uptake in a pore at a set chemical potential.

- [LAMMPS](lammps.md) and [GROMACS](gromacs.md) are molecular dynamics codes. Use them for dynamics, diffusion and viscosity.
- [Faunus](faunus.md) is another Monte Carlo code, aimed at coarse-grained electrolytes and macromolecules.
- [OpenMM](openmm.md) fits GPU molecular dynamics driven from Python.

## Install

GOMC is built from source. The README names the current release as 2.80 (December 2025) and requires CMake 3.18 or newer.

```
git clone --branch v2.80 https://github.com/GOMC-WSU/GOMC.git
cd GOMC
chmod u+x metamake.sh
./metamake.sh
```

The executables land in `bin/`. With no arguments, `metamake.sh` builds all CPU ensembles, and the GPU ones if CUDA is found. To build only some, name them: `./metamake.sh NVT GEMC`. The accepted names are `CPU`, `GPU`, `NVT`, `NPT`, `GCMC`, `GEMC` and the `GPU_` variants. A run takes the input file as the argument, optionally with `+pN` for N OpenMP threads, for example `./GOMC_CPU_GEMC +p4 in.conf`.

## A first run

GOMC reads one `in.conf` file that points to a force-field parameter file, and a PDB and PSF pair per box. The repository's test inputs include a two-box argon and krypton system in `test/input/Systems/AR_KR`. Its `SingleRun/in.conf` (https://github.com/GOMC-WSU/GOMC/blob/v2.80/test/input/Systems/AR_KR/SingleRun/in.conf) sets, among other lines:

- `PRNG INTSEED` and `Random_Seed 123`, so the run is repeatable.
- `ParaTypeEXOTIC on` with a Vrabec noble-gas parameter file, and `Potential VDW` with `Rcut 10` and long-range corrections on.
- `GEMC NVT` and `Temperature 143.15`.
- `RunSteps 3000`, `EqSteps 500`, `DisFreq 0.87`, `RotFreq 0.129`, `SwapFreq 0.001`.
- Two boxes, 34 and 65 angstrom on a side.
- `OutputName SingleRun`, with energy, pressure, molecule number, volume and density output on.

The full parameter reference is the user manual (https://gomc-wsu.github.io/Manual/). More ready inputs are in the GOMC Examples repository (https://github.com/GOMC-WSU/GOMC_Examples).

The container recipe below runs these AR_KR inputs, with the run length, temperature and seed taken from the form. It builds only the NVT and Gibbs-ensemble CPU executables. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds GOMC in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 0.6 s. GOMC has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [gomc-recipe.tar.gz](https://biosimhub.pages.dev/guides/gomc/gomc-recipe.tar.gz) (Dockerfile, run_gomc.sh, example conf.conf, params.inp, box0.pdb, box0psf.psf, box1.pdb, box1psf.psf, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf gomc-recipe.tar.gz
   cd gomc
   sh run.sh
   ```

![Terminal recording of the GOMC example run](https://biosimhub.pages.dev/media/gomc/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/gomc:2.80 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/gomc:2.80 sh /opt/run_gomc.sh 3000 143.15 123 /work/in/conf.conf /work/in/params.inp /work/in/box0.pdb /work/in/box0psf.psf /work/in/box1.pdb /work/in/box1psf.psf > out/gomc_console.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `SingleRun_BOX_0.pdb` | 18.3 KB |
| `SingleRun_BOX_0_restart.coor` | 4 B |
| `SingleRun_BOX_0_restart.coor.BAK` | 4 B |
| `SingleRun_BOX_0_restart.pdb` | 144 B |
| `SingleRun_BOX_0_restart.psf` | 337 B |
| `SingleRun_BOX_0_restart.xsc` | 97 B |
| `SingleRun_BOX_0_restart.xsc.BAK` | 97 B |
| `SingleRun_BOX_1.pdb` | 18.3 KB |
| `SingleRun_BOX_1_restart.coor` | 148 B |
| `SingleRun_BOX_1_restart.coor.BAK` | 148 B |
| `SingleRun_BOX_1_restart.pdb` | 606 B |
| `SingleRun_BOX_1_restart.psf` | 763 B |
| `SingleRun_BOX_1_restart.xsc` | 103 B |
| `SingleRun_BOX_1_restart.xsc.BAK` | 103 B |
| `SingleRun_merged.psf` | 782 B |
| `gomc_console.txt` | 10.1 KB |
| `run.conf` | 3.9 KB |

<details><summary>First lines of <code>SingleRun_BOX_0.pdb</code></summary>

```
REMARK     GOMC         1                                       1    
CRYST1   34.000   34.000   34.000  90.00  90.00  90.00 P 1        1  
ATOM      1 AR   AR  l   1       8.340  31.348  31.671  0.00 0.000          
ATOM      2 KR   KR  m   2      13.326  21.201  26.910  0.00 0.000          
ATOM      3 AR   AR  n   3      16.939   3.262   5.923  0.00 0.000          
ATOM      4 AR   AR  o   4       0.000   0.000   0.000  1.00 0.000          
ATOM      5 KR   KR  p   5       0.000   0.000   0.000  1.00 0.000          
ATOM      6 AR   AR  q   6       0.000   0.000   0.000  1.00 0.000          
END
REMARK     GOMC         2                                     100    
CRYST1   34.000   34.000   34.000  90.00  90.00  90.00 P 1        1  
ATOM      1 AR   AR  l   1       8.340  31.348  31.671  0.00 0.000          
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_0_restart.pdb</code></summary>

```
REMARK     GOMC     0.000   0.00000     500.000              2999    
CRYST1   34.000   34.000   34.000  90.00  90.00  90.00 P 1        1  
END
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_0_restart.psf</code></summary>

```
PSF

       2 !NTITLE 
 REMARKS Restart PSF produced by GOMC
 REMARKS Contains Geometry data for molecules in Box 0

       0 !NATOM 

       0 !NBOND: bonds 


       0 !NTHETA: angles 
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_0_restart.xsc</code></summary>

```
#$LABELS step a_x a_y a_z b_x b_y b_z c_x c_y c_z o_x o_y o_z
3000 34 0 0 0 34 0 0 0 34 17 17 17
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_0_restart.xsc.BAK</code></summary>

```
#$LABELS step a_x a_y a_z b_x b_y b_z c_x c_y c_z o_x o_y o_z
2000 34 0 0 0 34 0 0 0 34 17 17 17
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_1.pdb</code></summary>

```
REMARK     GOMC         1                                       1    
CRYST1   65.000   65.000   65.000  90.00  90.00  90.00 P 1        1  
ATOM      1 AR   AR  l   1       0.000   0.000   0.000  0.00 0.000          
ATOM      2 KR   KR  m   2       0.000   0.000   0.000  0.00 0.000          
ATOM      3 AR   AR  n   3       0.000   0.000   0.000  0.00 0.000          
ATOM      4 AR   AR  o   4      16.323  61.619  62.256  1.00 0.000          
ATOM      5 KR   KR  p   5      26.139  44.297  52.883  1.00 0.000          
ATOM      6 AR   AR  q   6      30.844   0.499   9.084  1.00 0.000          
END
REMARK     GOMC         2                                     100    
CRYST1   65.000   65.000   65.000  90.00  90.00  90.00 P 1        1  
ATOM      1 AR   AR  l   1       0.000   0.000   0.000  0.00 0.000          
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_1_restart.pdb</code></summary>

```
REMARK     GOMC    32.500   0.78540     500.000              2999    
CRYST1   65.000   65.000   65.000  90.00  90.00  90.00 P 1        1  
ATOM      1 AR   AR  l   1      38.104  37.230  53.704 1.000 0.000          
ATOM      2 AR   AR  n   2      19.053  47.139   7.603 1.000 0.000          
ATOM      3 AR   AR  q   3      53.038  11.141  60.597 1.000 0.000          
ATOM      4 AR   AR  o   4      55.731   2.867  28.568 1.000 0.000          
ATOM      5 KR   KR  m   5      20.394  63.399  59.766 1.000 0.000          
ATOM      6 KR   KR  p   6      16.016  50.911  59.336 1.000 0.000          
END
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_1_restart.psf</code></summary>

```
PSF

       2 !NTITLE 
 REMARKS Restart PSF produced by GOMC
 REMARKS Contains Geometry data for molecules in Box 1

       6 !NATOM 
       1 A    1    AR   AR   AR     0.000000       39.9480           0
       2 C    2    AR   AR   AR     0.000000       39.9480           0
       3 F    3    AR   AR   AR     0.000000       39.9480           0
       4 D    4    AR   AR   AR     0.000000       39.9480           0
       5 B    5    KR   KR   KR     0.000000       83.7980           0
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_1_restart.xsc</code></summary>

```
#$LABELS step a_x a_y a_z b_x b_y b_z c_x c_y c_z o_x o_y o_z
3000 65 0 0 0 65 0 0 0 65 32.5 32.5 32.5
```

</details>

<details><summary>First lines of <code>SingleRun_BOX_1_restart.xsc.BAK</code></summary>

```
#$LABELS step a_x a_y a_z b_x b_y b_z c_x c_y c_z o_x o_y o_z
2000 65 0 0 0 65 0 0 0 65 32.5 32.5 32.5
```

</details>

<details><summary>First lines of <code>SingleRun_merged.psf</code></summary>

```
PSF

       2 !NTITLE 
 REMARKS Combined PSF produced by GOMC
 REMARKS Contains Geometry data for molecules in ALL boxes in the system

       6 !NATOM 
       1 A    1    AR   AR   AR     0.000000       39.9480           0
       2 B    2    KR   KR   KR     0.000000       83.7980           0
       3 C    3    AR   AR   AR     0.000000       39.9480           0
       4 D    4    AR   AR   AR     0.000000       39.9480           0
       5 E    5    KR   KR   KR     0.000000       83.7980           0
```

</details>

<details><summary>First lines of <code>gomc_console.txt</code></summary>

```
Info: GOMC Version 2.80
Info: Start Time: Sun Oct 18 04:51:11 2026
Info: Host Name: 1f5be9b8c012
CPU information:
Info: Total number of CPU cores: 16
Info: Total number of CPU cores available: 16
Info: Model name: VirtualApple @ 2.50GHz
Info: System name: Linux
Info: Release: 7.0.12-linuxkit
Info: Version: #1 SMP PREEMPT Thu Aug 27 14:02:21 UTC 2026
Info: Kernel Architecture: x86_64
Info: Total Ram: 7833.5MB
```

</details>

<details><summary>First lines of <code>run.conf</code></summary>

```
########################
## Init File v2.0
## 
## IMPROVEMENTS
## - Compacts inputs into one line
## - Suggestion: edit inline with (insert key)
##
## To-Do 
## (make editor + XML version)
########################

############################################################################
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `run_steps` | Production steps | 3000 | 100 to 200000 |
| `temperature` | Temperature (K) | 143.15 | 50 to 400 |
| `seed` | Seed | 123 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

Output names start with the `OutputName` value plus the run number and letter. A run writes a console log, block or statistics files for the quantities switched on (energy, pressure, molecule counts, volume, density), and, where enabled, coordinate PDB/PSF files and a restart file. The `*Freq` lines set how often each is written.

Check a Gibbs run in this order. Volumes and molecule counts of the two boxes should drift during equilibration, then fluctuate around steady values. Compare the densities of the two boxes against known coexistence data for the fluid. Look at the move acceptance rates printed in the console. The manual describes how `AdjSteps` tunes the step sizes during equilibration.

## Pitfalls

- **Equilibration is part of the run.** Discard everything before `EqSteps` ends. Averages that include it are biased.
- **Chemical potentials are in the file's own units.** The sample uses values like `-968` for `ChemPot`. Take them from the manual or a paper that uses the same force field.
- **The force field type must match the file.** `ParaTypeCHARMM` and `ParaTypeEXOTIC` select different parameter formats. A mismatch stops the run.
- **Cell size must exceed twice the cutoff.** Box vectors smaller than that make the cutoff meaningless.
- **GPU builds need CUDA at build time.** Without it only the CPU executables exist.
- **Seeds repeat results only for the same build.** Thread counts and compilers can change the random stream.

## Further reading

- Repository: https://github.com/GOMC-WSU/GOMC
- User manual: https://gomc-wsu.github.io/Manual/
- Project site: https://gomc-wsu.org/
- Examples: https://github.com/GOMC-WSU/GOMC_Examples
- Paper: Nejahi Y et al. (2019) GOMC: GPU Optimized Monte Carlo for the simulation of phase equilibria and physical properties of complex fluids. SoftwareX 9:20-27. https://doi.org/10.1016/j.softx.2018.11.005

---

Cite: Nejahi Y, et al. (2019). GOMC: GPU Optimized Monte Carlo for the simulation of phase equilibria and physical properties of complex fluids. SoftwareX 9:20-27. doi:10.1016/j.softx.2018.11.005

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/gomc).
