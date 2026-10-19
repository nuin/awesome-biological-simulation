# oxDNA

> Coarse-grained simulation of DNA and RNA at nucleotide resolution by Monte Carlo or molecular dynamics.

Licence: GPL-3.0-only · [Source code](https://github.com/lorenzo-rovigatti/oxDNA)

## What it simulates

oxDNA simulates DNA and RNA with a coarse-grained model. Each nucleotide is one rigid body with interaction sites for the backbone, the stacking and the hydrogen bonds. The model reproduces helix structure, melting, hairpin formation and the mechanics of nanostructures at a cost far below all-atom simulation.

The README describes the code as an extensible simulation and analysis framework. It supports DNA, RNA, Lennard-Jones and patchy-particle simulations, with molecular dynamics and several Monte Carlo schemes, on CPU cores and on NVIDIA GPUs. The force field is chosen with `interaction_type` (`DNA`, `DNA2`, `RNA`, `RNA2`, `NA`, `LJ` and others). The functional forms of oxDNA1, oxDNA2, oxRNA and oxNA are given in the original papers linked from the README.

A run needs three files: an input file with the settings, a topology file that lists the strands and bases, and a configuration file with the starting positions and orientations. Lengths and energies are in reduced units. The temperature `T` can be given in kelvin by appending `K`, for example `T = 334 K`.

## When to use it

Use oxDNA for questions at the scale of tens to thousands of nucleotides: hairpin and duplex melting, DNA origami and other nanostructures, strand displacement, supercoiling, persistence length.

- [LAMMPS](lammps.md) includes an oxDNA pair style. The README states that the LAMMPS version is a separate code and not linked to this repository.
- [GROMACS](gromacs.md) and [OpenMM](openmm.md) run all-atom nucleic acids, at much higher cost per nanosecond.
- [OpenMD](openmd.md) and [GOMC](gomc.md) cover other molecular models and do not include this nucleotide model.

oxDNA runs on one CPU core or one GPU. The README FAQ says it cannot spread one simulation over several cores or GPUs. The Python bindings (`oxpy`) can drive parallel schemes such as replica exchange.

## Install

oxDNA is built from source with CMake. The current release is v3.7.0. The install page requires CMake and a C++14 compiler.

```
git clone --branch v3.7.0 https://github.com/lorenzo-rovigatti/oxDNA.git
cd oxDNA
mkdir build && cd build
cmake ..
make -j4
```

This places `oxDNA`, `DNAnalysis` and `confGenerator` in `build/bin`. Useful CMake switches from the install page: `-DCUDA=ON` for GPUs, `-DMPI=ON`, `-DPython=ON` for `oxpy` and the analysis tools, and `-DNATIVE_COMPILATION=OFF` to build without `-march=native` when the binary runs on another machine. The analysis package `oxDNA_analysis_tools` is on PyPI (version 2.0.5 at the time of writing).

## A first run

Adapted from the HAIRPIN example in the repository (https://github.com/lorenzo-rovigatti/oxDNA/tree/v3.7.0/examples/HAIRPIN). Its `run.sh` says it simulates "an 18-base hairpin (6-base stem + 6-base loop) at 334 K". The main settings in its `input` file are `sim_type = VMMC`, `backend = CPU`, `T = 334 K`, `dt = 0.003`, a log-free `energy_file = energy.dat`, and a second output that writes the hydrogen-bond energy (`hb_energy.dat`) every 10,000 steps.

```
build/bin/oxDNA input
```

The file sets `steps = 100000000`, which is long. Override any key on the command line, for example `oxDNA input steps=1000000 seed=42`. The usage page states that key=value pairs after the input file replace the file's values.

The container recipe below uses the same files with `steps` set to 200,000 and a ten-point energy log. On one emulated x86 CPU, 1,000,000 steps took 175 s and 200,000 steps took 97 s, so most of the time is start-up; raise `steps` for a longer run. The recipe has been run on biosimhub; its recorded output files are listed with the recipe below.

## Run the tested example

This recipe builds oxDNA in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-18 in 97.4 s. oxDNA has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [oxdna-recipe.tar.gz](https://biosimhub.pages.dev/guides/oxdna/oxdna-recipe.tar.gz) (Dockerfile, run_oxdna.sh, example input.txt, topology.top, configuration.conf, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf oxdna-recipe.tar.gz
   cd oxdna
   sh run.sh
   ```

![Terminal recording of the oxDNA example run](https://biosimhub.pages.dev/media/oxdna/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/oxdna:3.7.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/oxdna:3.7.0 sh /opt/run_oxdna.sh /work/in/input.txt /work/in/topology.top /work/in/configuration.conf 200000 334 42 > out/oxdna_stdout.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `energy.dat` | 539 B |
| `hb_energy.dat` | 504 B |
| `last_conf.dat` | 3.1 KB |
| `log.dat` | 1.7 KB |
| `oxdna_stdout.txt` | 0 B |
| `trajectory.dat` | 3.1 KB |

<details><summary>First lines of <code>energy.dat</code></summary>

```
           0  -0.365026   0.000  0.000  0.000   
       20000  -0.626089   0.381  0.610  0.000   
       40000  -0.471730   0.394  0.607  0.000   
       60000  -0.567868   0.401  0.606  0.000   
       80000  -0.741088   0.403  0.605  0.000   
      100000  -0.641312   0.408  0.603  0.000   
      120000  -0.593502   0.415  0.603  0.000   
      140000  -0.457542   0.411  0.603  0.000   
      160000  -0.665045   0.410  0.603  0.000   
      180000  -0.263318   0.407  0.603  0.000   
      200000  -0.435150   0.403  0.605  0.000   
```

</details>

<details><summary>First lines of <code>hb_energy.dat</code></summary>

```
           0   0.000000
       10000  -0.000000
       20000   0.000000
       30000   0.000000
       40000   0.000000
       50000   0.000000
       60000   0.000000
       70000   0.000000
       80000   0.000000
       90000   0.000000
      100000   0.000000
      110000   0.000000
```

</details>

<details><summary>First lines of <code>last_conf.dat</code></summary>

```
t = 200000
b = 50 50 50
E = -0.435149750680664 -0.435149750680664 0
-110.617347239102 263.563460547507 36.8566664228409 -0.285544739976203 0.698904042800712 0.655741824522992 -0.778958545898624 -0.567849708303249 0.266026864341586 0 0 0 0 0 0
-109.658640976048 263.033223331694 35.9026610005209 0.643784982591007 -0.153938201994067 -0.749562489827987 0.575551963620948 -0.548104144370581 0.606895200257725 0 0 0 0 0 0
-110.139142555032 263.48691479481 35.6563681692904 -0.845819948080883 -0.440829944923029 -0.300428985098994 -0.398039436723074 0.896454044133585 -0.194768461434902 0 0 0 0 0 0
-110.348740070827 263.800270707294 35.2778983781858 -0.798351477950813 -0.223391407075653 0.559223744934452 -0.39322009970183 0.896719888519179 -0.203153623459276 0 0 0 0 0 0
-110.387496162685 264.385440392074 34.3011363799039 0.215461041692681 0.952886312437583 -0.213504602015531 0.41140989547694 0.109710025444195 0.904823523246764 0 0 0 0 0 0
-110.022891138531 264.40414954495 34.2700503047221 -0.697885588230905 0.107242520861732 -0.708134695844529 -0.661587998817869 0.28218314248962 0.694747431743976 0 0 0 0 0 0
-109.009364332046 264.225213233785 34.2802699233066 0.683444468165956 -0.3692702877579
```

</details>

<details><summary>First lines of <code>log.dat</code></summary>

```
INFO: seeding the RNG with 42
INFO: Initializing backend 
INFO: Simulation type: VMMC
INFO: The generator will try to take into account bonded interactions by choosing distances between bonded neighbours no larger than 2.000000
INFO: Converting temperature from Kelvin (334.000000 K) to simulation units (0.111333)
INFO: Temperature change detected (new temperature: 60.85 C, 334.00 K), re-initialising the DNA interaction
INFO: pid: 1
INFO: (Cells.cpp) N_cells_side: 4, 4, 4; rcut=1.58377, IS_MC: 1
INFO: N: 18, N molecules: 1
WARNING: maxclust < 0, setting it to N = 18
INFO: Not attempting to preserve topology; max_move_size = 21.6325
INFO: RELEASE: v3.7.0
```

</details>

<details><summary>First lines of <code>trajectory.dat</code></summary>

```
t = 200000
b = 50 50 50
E = -0.435149750680664 -0.435149750680664 0
-110.617347239102 263.563460547507 36.8566664228409 -0.285544739976203 0.698904042800712 0.655741824522992 -0.778958545898624 -0.567849708303249 0.266026864341586 0 0 0 0 0 0
-109.658640976048 263.033223331694 35.9026610005209 0.643784982591007 -0.153938201994067 -0.749562489827987 0.575551963620948 -0.548104144370581 0.606895200257725 0 0 0 0 0 0
-110.139142555032 263.48691479481 35.6563681692904 -0.845819948080883 -0.440829944923029 -0.300428985098994 -0.398039436723074 0.896454044133585 -0.194768461434902 0 0 0 0 0 0
-110.348740070827 263.800270707294 35.2778983781858 -0.798351477950813 -0.223391407075653 0.559223744934452 -0.39322009970183 0.896719888519179 -0.203153623459276 0 0 0 0 0 0
-110.387496162685 264.385440392074 34.3011363799039 0.215461041692681 0.952886312437583 -0.213504602015531 0.41140989547694 0.109710025444195 0.904823523246764 0 0 0 0 0 0
-110.022891138531 264.40414954495 34.2700503047221 -0.697885588230905 0.107242520861732 -0.708134695844529 -0.661587998817869 0.28218314248962 0.694747431743976 0 0 0 0 0 0
-109.009364332046 264.225213233785 34.2802699233066 0.683444468165956 -0.3692702877579
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `steps` | Simulation steps | 200000 | 1000 to 20000000 |
| `temperature` | Temperature (K) | 334 | 250 to 400 |
| `seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `energy.dat`: one row per `print_energy_every` steps, with the time and the energy terms in reduced units. A hairpin that stays folded has a low and steady potential energy per nucleotide.
- `hb_energy.dat`: the step number and the hydrogen-bond energy from the `data_output_1` block of the example. A closed stem gives a clearly negative value, and an open hairpin gives values near zero. A trace that jumps between the two levels shows folding and unfolding events.
- `trajectory.dat` and `last_conf.dat`: configurations in the same text format as the starting file (`t`, `b` for the box, `E` for energies, then one line per nucleotide with position and orientation vectors). Open them with oxView or `oxDNA_analysis_tools`.
- `log.dat`: the run log.

The example HAIRPIN folder ships notes and histograms (`DOCS/`) from the original 2012 run. Compare the shape of your hydrogen-bond distribution against them before trusting longer runs.

## Pitfalls

- **Units are reduced.** A time step of 0.003 is not a picosecond count. Convert with the conversion constants in the documentation before quoting times.
- **One input, many overrides.** Command-line overrides are convenient, and they also hide settings. Keep the final values in the input file for reproducibility.
- **Seed repeats only the same build.** The `seed` key reproduces a run for the same binary and options.
- **Initial configurations can be overstretched.** The `confGenerator` warning in the docs says its random insertion makes circular strands very unlikely to work. Relax generated configurations first, as the `RELAX_INITIAL_CONFIGURATION` example shows.
- **Native compilation is not portable.** A binary built with `-march=native` can fail on another CPU.

## Further reading

- Repository: https://github.com/lorenzo-rovigatti/oxDNA
- Documentation: https://lorenzo-rovigatti.github.io/oxDNA/
- Install page: https://lorenzo-rovigatti.github.io/oxDNA/install.html
- Paper: Poppleton E et al. (2023) oxDNA: coarse-grained simulations of nucleic acids made simple. J Open Source Softw 8(81):4693. https://doi.org/10.21105/joss.04693
- Model paper: Ouldridge TE, Louis AA, Doye JPK (2011) Structural, mechanical, and thermodynamic properties of a coarse-grained DNA model. J Chem Phys 134:085101. https://doi.org/10.1063/1.3552946

---

Cite: Poppleton E, et al. (2023). oxDNA: coarse-grained simulations of nucleic acids made simple. J Open Source Softw 8(81):4693. doi:10.21105/joss.04693

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/oxdna).
