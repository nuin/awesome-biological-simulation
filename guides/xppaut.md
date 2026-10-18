# XPPAUT

> Integrate a user-supplied system of ODEs or difference equations in XPPAUT batch mode and return the time series as a table.

Licence: GPL-2.0-only · [Source code](https://sites.pitt.edu/~phase/bard/bardware/xpp/xpp.html)

## What it simulates

XPPAUT integrates systems of ordinary differential equations (ODEs) and difference equations. You write the equations, parameters and initial values in a short text file with the extension `.ode`. XPPAUT solves them in time and can also do phase planes, nullclines and bifurcation diagrams through AUTO in its interactive interface.

The example is the Lorenz system, three coupled equations for x, y and z with parameters sigma = 10, r = 28 and b = 2.6667. It starts at (1, 1, 1). For these parameters the solution is chaotic, so it is a standard test of an integrator.

The key assumptions are that the model is deterministic and that time advances with the chosen numerical method and step. XPPAUT has no noise terms unless you write them into the equations.

Input is the `.ode` file plus optional overrides for parameters and options. In batch mode the output is a plain-text table with time in the first column and one column per variable.

## When to use it

- You study a small dynamical system, for example an excitable cell, a gene circuit or a predator-prey pair, and want its time course.
- You want to see how the result changes with one parameter, for example r in the Lorenz system, without editing the file.
- You teach dynamical systems and want a tool the SIAM guide by Ermentrout describes step by step.

For random events with small copy numbers, [GillesPy2](gillespy2.md) on biosimhub fits better. For models in the LEMS or NeuroML2 formats, [PyLEMS](pylems.md) fits. [COPASI](copasi.md) fits when the model is a biochemical network in SBML.

## Install it yourself

Pinned to 8.0 (the current release on the XPPAUT site, dated November 2023). The conda-forge package is `xppaut`:

```
micromamba create -n xpp -c conda-forge xppaut=8.0
micromamba activate xpp
```

The XPPAUT site also lists a Linux tarball, a Windows install, and Mac installs for Apple Silicon. The package has no ARM build, so the recipe's image runs with `--platform linux/amd64`.

The command line, as printed by `xppaut -help` in the 8.0 container, includes:

- `-silent`: batch run without the interface; dump solutions to a file.
- `-outfile <filename>`: where to write the output (default `output.dat`).
- `-quiet <1|0>`: print nothing to the console.
- `-with <string>`: set anything that is in an internal set, such as `total`, `dt` or a parameter, in quotes.
- `-runnow`: run immediately on start-up (implied by `-silent`).

Minimal run:

```
xppaut lorenz.ode -silent -quiet 1 -outfile out.dat -with "total=20,dt=0.01"
```

## Run the tested example

This recipe builds XPPAUT in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.2 s. XPPAUT has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [xppaut-recipe.tar.gz](https://biosimhub.pages.dev/guides/xppaut/xppaut-recipe.tar.gz) (Dockerfile, example model.ode, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf xppaut-recipe.tar.gz
   cd xppaut
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/xppaut:8.0 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/xppaut:8.0 xppaut /work/in/model.ode -silent -quiet 1 \
    -outfile xppaut_output.dat -with total=20,dt=0.01
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `xppaut_output.dat` | 78.2 KB |

<details><summary>First lines of <code>xppaut_output.dat</code></summary>

```
0 1 1 1 
0.0099999998 1.0125672 1.2599179 0.98489064 
0.02 1.0488237 1.5239972 0.9731136 
0.029999999 1.1072088 1.7983099 0.96515799 
0.039999999 1.1868681 2.0885401 0.96173596 
0.050000001 1.287557 2.4001546 0.96380454 
0.059999999 1.4095707 2.7385457 0.97260636 
0.07 1.5536901 3.109154 0.98972905 
0.079999998 1.7211465 3.5175695 1.0171841 
0.090000004 1.9135963 3.9696152 1.0575092 
0.1 2.1331067 4.4714108 1.113896 
0.11 2.3821464 5.0294151 1.1903505 
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `total=…,dt={dt}` | Total integration time | 20 | 0.001 to 100000 |
| `total={total},dt=…` | Time step | 0.01 | 1e-05 to 10 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The model file is five lines of model plus options:

```
dx/dt=sigma*(y-x)
dy/dt=r*x-y-x*z
dz/dt=x*y-b*z
par sigma=10,r=28,b=2.6667
init x=1,y=1,z=1
@ total=20,dt=0.01,xp=t,yp=x,xlo=0,xhi=20,ylo=-25,yhi=25,maxstor=10000
done
```

`par` sets parameters, `init` sets initial values, the `@` line sets options (`total` is the time to integrate, `dt` the step), and `done` ends the file. The XPPAUT documentation says: do not put spaces around `=` in `par` lines.

The example runs the command above with no helper script. It writes only `xppaut_output.dat` (80,045 bytes, 2,001 lines).

Columns are time, x, y and z. The first line is `0 1 1 1`, the initial state. The second line is `0.0099999998 1.0125672 1.2599179 0.98489064`, one step later. The time column shows single-precision rounding, so 0.01 prints as 0.0099999998. The last line is at t = 20: x = 13.079, y = 12.919, z = 33.209.

Over the run, x ranges from -17.29 to 19.56. The solution swings between the two lobes of the attractor.

## Your own runs

Same image and command; only `-with` changed.

**Longer run** (`total=100,dt=0.01`). The file has 10,001 lines and x at t = 100 is 5.26. With `total=200` the file has 20,001 lines, so the `maxstor=10000` option in the file did not truncate the output.

**Different parameter** (`total=20,dt=0.01,r=0.5`). Parameters can be set through `-with`. For r below 1 the origin is stable, and the run decays: at t = 20, x = 4.3e-05, y = 4.1e-05, z = 1.0e-09.

**Larger step** (`total=20,dt=0.1`). The file has 201 lines. The end value of x is -4.449, against 13.079 with dt = 0.01. The Lorenz system is chaotic, so small integration errors grow, and the late part of a run depends on the step.

**Another integrator.** Adding `meth=euler` to the `-with` string changed x at t = 20 from 13.079 to 9.515. The XPPAUT numerics page lists the methods (Euler, Runge-Kutta, Dormand-Prince, CVODE and others). It does not say which is the default, so set the method yourself when you compare runs.

## Pitfalls

- **Chaos hides errors.** Two valid integrators or steps can give different values at t = 20. Compare early times, or check that the long-run statistics agree instead of single end values.
- **Spaces in `par` lines.** XPPAUT's documentation says never to put spaces around `=`. Write `par a=1,b=2`.
- **Always `-silent` in scripts.** The flag runs XPPAUT as a batch job without the interface.
- **Time column precision.** The time values are single precision. Do not use them as exact grid points.
- **Platform.** The recipe's image needs `--platform linux/amd64`, because the package has no ARM build.

## Further reading

- XPPAUT home page and downloads: https://sites.pitt.edu/~phase/bard/bardware/xpp/xpp.html
- Writing ODE files: https://sites.pitt.edu/~phase/bard/bardware/xpp/help/xppodes.html
- Numerics options: https://sites.pitt.edu/~phase/bard/bardware/xpp/help/xppnumerics.html
- Tutorial: http://sites.pitt.edu/~phase/bard/bardware/tut/start.html
- Book: Ermentrout B (2002). Simulating, Analyzing, and Animating Dynamical Systems: A Guide to XPPAUT for Researchers and Students. SIAM.

---

Cite: Ermentrout B (2002). Simulating, Analyzing, and Animating Dynamical Systems: A Guide to XPPAUT for Researchers and Students. SIAM.

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/xppaut).
