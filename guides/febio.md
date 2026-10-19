# FEBio

> Compress a block of elastic material with nonlinear implicit finite elements and return nodal displacements and axial stress per element.

Licence: MIT · [Source code](https://github.com/febiosoftware/FEBio)

## What it simulates

FEBio is a nonlinear implicit finite element solver for biomechanics. You describe a body as a mesh of elements with a material law, then add constraints and loads. FEBio finds the displacements, strains and stresses that balance the loads. It handles large deformation, so a soft tissue can be squeezed by a third of its height and the answer still holds.

The solid mechanics module covers elastic, hyperelastic, viscoelastic and fibre-reinforced materials. Other modules add biphasic and multiphasic transport (fluid and solutes moving through cartilage), fluid flow and fluid-structure interaction. Contact, rigid bodies, prescribed motion and pressure loads are built in.

A model is one XML file with the extension `.feb`. It holds the control settings, materials, mesh, boundary conditions, load curves and the outputs you want. FEBio Studio is the graphical front end that builds these files, and the solver also runs from the command line.

## When to use it

Use FEBio when the question is about stress and strain in soft tissue, cartilage, bone or a device, and the deformation is too large for linear theory.

- Use [openCARP](opencarp.md) when the question is the electrical activation of the heart, not its mechanics.
- Use [OpenSim](opensim.md) when you want whole-body musculoskeletal dynamics from motion data.
- Use [bioptim](bioptim.md) when you want to predict a movement as an optimal control problem.

## Install

The README says pre-compiled executables for Windows, macOS and Linux come with the FEBio Studio installer at https://febio.org/downloads/. The source is MIT licensed. The latest release is v4.13 (2026-08-04).

To build from source on Linux, follow `BUILD.md` in the repository. It needs CMake and a C++17 compiler. Intel MKL is optional. Without MKL, FEBio falls back to its skyline linear solver, which is slower and uses more memory than Pardiso. This build leaves the other optional libraries (HYPRE, MMG, levmar, NLopt, FFTW) off:

```
git clone --depth 1 --branch v4.13 https://github.com/febiosoftware/FEBio
cd FEBio
cmake . -B cmbuild -DCMAKE_BUILD_TYPE=Release -DSET_DEVCOMMIT=OFF \
  -DUSE_MKL=OFF -DUSE_FFTW=OFF -DUSE_HYPRE=OFF -DUSE_LEVMAR=OFF \
  -DUSE_MMG=OFF -DUSE_NLOPT=OFF -DUSE_ZLIB=ON
cmake --build cmbuild -j4
```

The executable is `cmbuild/bin/febio4`, with its shared libraries in `cmbuild/lib`. The project's own Linux CI script uses the same `cmbuild` folder and turns the optional libraries on.

## A first run

Adapted from the FEBio README and the command-line parser in [`FEBio/FEBioApp.cpp`](https://github.com/febiosoftware/FEBio/blob/v4.13/FEBio/FEBioApp.cpp):

```
febio4 -i model.feb -o febio.log -p model.xplt -noconfig -silent
```

`-i` names the input file (a missing extension becomes `.feb`), `-o` the log file, `-p` the plot file, `-noconfig` skips the configuration file and `-silent` keeps the screen quiet. `febio4 -info` prints the version.

The recipe's helper script writes `model.feb` itself. It builds a box of 10 mm edges from hex8 elements, fixes the bottom face in z, and fixes the x=0 and y=0 faces in x and y so that a quarter of the block stands for the whole. It then pushes the top face down in a set number of load steps. Units are mm, MPa and s.

## Run the tested example

This recipe builds FEBio in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 1 s. FEBio has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [febio-recipe.tar.gz](https://biosimhub.pages.dev/guides/febio/febio-recipe.tar.gz) (Dockerfile, run_febio.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf febio-recipe.tar.gz
   cd febio
   sh run.sh
   ```

![Terminal recording of the FEBio example run](https://biosimhub.pages.dev/media/febio/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/febio:4.13 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/febio:4.13 python3 /opt/run_febio.py --nx 4 --ny 4 --nz 4 \
    --material neo-Hookean --youngs 10 --poisson 0.3 \
    --compression 0.3 --steps 10 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `displacement.csv` | 48.8 KB |
| `febio.log` | 27.4 KB |
| `model.feb` | 9.4 KB |
| `model.xplt` | 43.8 KB |
| `run_log.txt` | 122 B |
| `stress_sz.csv` | 12.0 KB |

<details><summary>First lines of <code>displacement.csv</code></summary>

```
*Step  = 0
*Time  = 0
*Data  = ux;uy;uz
1,0,0,0
2,0,0,0
3,0,0,0
4,0,0,0
5,0,0,0
6,0,0,0
7,0,0,0
8,0,0,0
9,0,0,0
```

</details>

<details><summary>First lines of <code>febio.log</code></summary>

```
===========================================================================
         ________    _________   _______       __     _________            
        |        |\ |        |\ |       \\    |  |\  /         \\          
        |    ____|| |    ____|| |    __  ||   |__|| |    ___    ||         
        |   |\___\| |   |\___\| |   |\_| ||    \_\| |   //  \   ||         
        |   ||__    |   ||__    |   ||_| ||   |  |\ |  ||    |  ||         
        |       |\  |       |\  |         \\  |  || |  ||    |  ||         
        |    ___||  |    ___||  |    ___   || |  || |  ||    |  ||         
        |   |\__\|  |   |\__\|  |   |\__|  || |  || |  ||    |  ||         
        |   ||      |   ||___   |   ||__|  || |  || |   \\__/   ||         
        |   ||      |        |\ |          || |  || |           ||         
        |___||      |________|| |_________//  |__||  \_________//          
```

</details>

<details><summary>First lines of <code>model.feb</code></summary>

```
<?xml version="1.0" encoding="UTF-8"?>
<febio_spec version="4.0">
	<Module type="solid"/>
	<Control>
		<analysis>STATIC</analysis>
		<time_steps>10</time_steps>
		<step_size>0.1</step_size>
		<solver type="solid">
			<symmetric_stiffness>symmetric</symmetric_stiffness>
			<max_refs>15</max_refs>
			<qn_method type="BFGS"/>
		</solver>
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
model.feb: 125 nodes, 64 hex8 elements, neo-Hookean, E=10 MPa, v=0.3, compression=0.3
Starting without configuration file
```

</details>

<details><summary>First lines of <code>stress_sz.csv</code></summary>

```
*Step  = 0
*Time  = 0
*Data  = sz
1,0
2,0
3,0
4,0
5,0
6,0
7,0
8,0
9,0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--nx` | Elements along x | 4 | 1 to 20 |
| `--ny` | Elements along y | 4 | 1 to 20 |
| `--nz` | Elements along z | 4 | 1 to 20 |
| `--material` | Material model | neo-Hookean | neo-Hookean, isotropic elastic |
| `--youngs` | Young's modulus (MPa) | 10 | 0.01 to 100000 |
| `--poisson` | Poisson's ratio | 0.3 | 0 to 0.45 |
| `--compression` | Nominal compressive strain on the top face | 0.3 | 0.01 to 0.6 |
| `--steps` | Load steps | 10 | 1 to 100 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

- `febio.log` records each time step, the Newton iterations it needed and the final status. A normal run ends with a "N O R M A L   T E R M I N A T I O N" banner, and a failed run ends with "E R R O R   T E R M I N A T I O N".
- `model.xplt` is the binary plot file. Open it in FEBio Studio to see the deformed mesh coloured by displacement or stress.
- `displacement.csv` lists node ids with `ux`, `uy` and `uz` for each stored step. The top nodes should end at `uz` equal to minus the nominal strain times 10 mm.
- `stress_sz.csv` lists the axial Cauchy stress per element. Compression gives negative values.

Because the platens are frictionless, the stress is nearly uniform, which makes the output easy to check. At small strain, the stress is about the Young's modulus times the strain. At 30 percent strain the neo-Hookean and isotropic elastic laws give different stresses. The difference comes from the material law, not from the mesh.

## Pitfalls

- **Elements can invert.** A large compression of a coarse mesh gives a negative Jacobian and an error termination. Use more load steps or a finer mesh.
- **Poisson's ratio near 0.5 locks hex8 elements.** The recipe caps it at 0.45. Use an uncoupled (nearly incompressible) material formulation for rubber-like tissue.
- **The solver changes without MKL.** The skyline solver solves the same equations as Pardiso but takes longer and more memory on big meshes.
- **Format versions differ.** The helper writes `febio_spec` version 4.0. Other spec versions use different tags for some features, so check an older file before you reuse it.
- **Units are not checked.** FEBio uses whatever consistent set you choose.
- **Use a log file.** With `-silent` there is no screen output, so read `febio.log` to see why a run stopped.

## Further reading

- Source and build guide: https://github.com/febiosoftware/FEBio
- Documentation: https://help.febio.org/
- Forums: https://forums.febio.org/
- Paper: Maas SA, Ellis BJ, Ateshian GA, Weiss JA (2012). FEBio: Finite Elements for Biomechanics. Journal of Biomechanical Engineering 134(1):011005. https://doi.org/10.1115/1.4005694

---

Cite: Maas SA, Ellis BJ, Ateshian GA, Weiss JA (2012). FEBio, finite elements for biomechanics. Journal of Biomechanical Engineering 134(1):011005. doi:10.1115/1.4005694

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/febio).
