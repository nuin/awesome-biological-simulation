# L-Py

> Grow a stochastic branching tree with an L-system, and write the derived string, 3D geometry and segment counts.

Licence: CECILL-C · [Source code](https://github.com/openalea/lpy)

## What it simulates

L-Py grows plant-like structures from L-system rewriting rules. An L-system is a string of symbols and a set of rules that replace symbols, all at once, in each step. Symbols such as `F` (draw a segment), `+` (turn), `/` (roll) and `[` `]` (start and end a branch) are turtle graphics commands. After the last step, the string is read as a 3D shape. L-Py adds parameters to symbols, Python code inside rules, and random choices, so one rule set gives a family of different trees.

The example uses one growing bud, `A(length, width, steps left)`. In each step the bud lays down a segment `F`. With probability 0.7 it starts a side branch, turned 40 degrees from the axis and rolled 137.5 degrees (the golden angle) around it. The side branch is 0.75 times as long and 0.7 times as wide. The main axis continues 0.95 times as long. The run takes 8 steps.

L-Py also has a GUI editor and can drive time-varying growth with `Start`, `End` and `StartEach` hooks. The recipe uses the Python library only.

## When to use it

Use L-Py to explore how a few local rules set whole-plant form:

- How do branching angle, length ratio and branching probability change the crown?
- How many segments and branches does a rule set make after n steps?
- Which shapes can you get from a rule you can write on one page?

L-Py makes the shape, and does not model water, carbon or light. For root systems with measured parameters and an organ-level growth model, use [CPlantBox](cplantbox.md).

## Install it yourself

L-Py is distributed on the `openalea3` conda channel. The conda dry run `micromamba create -n lpy --dry-run -c openalea3 -c conda-forge openalea.lpy=3.15.4 openalea.plantgl=3.23.2 python=3.13` resolves to L-Py 3.15.4 and PlantGL 3.23.2.

```
micromamba create -n lpy -c openalea3 -c conda-forge openalea.lpy=3.15.4 openalea.plantgl=3.23.2 python=3.13
micromamba activate lpy
```

The `openalea3` channel lists builds for linux-64, osx-64, osx-arm64 and win-64. The recipe's image is linux/amd64 and installs the system graphics libraries libGL and libGLU for PlantGL. No display is needed. A minimal run:

```python
import openalea.lpy as lpy

code = """
Axiom: A(1)
derivation length: 6
production:
A(x) --> F(x)[+(30)A(x*0.8)][-(30)A(x*0.8)]
interpretation:
"""
lsys = lpy.Lsystem()
lsys.set(code)
lstring = lsys.derive()
scene = lsys.sceneInterpretation(lstring)
scene.save("t.obj")
```

In the image this gave a string of 505 modules (`F(1)[+(30)F(0.8)[+(30)F(0.64)...`), a scene of 63 shapes and an OBJ file of 89,787 bytes.

## Run the tested example

This recipe builds L-Py in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 10.9 s. L-Py has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [l-py-recipe.tar.gz](https://biosimhub.pages.dev/guides/l-py/l-py-recipe.tar.gz) (Dockerfile, run_lpy.py, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf l-py-recipe.tar.gz
   cd l-py
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/l-py:3.15.4 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/l-py:3.15.4 python /opt/run_lpy.py --steps 8 --angle 40 \
    --ratio 0.75 --branch_prob 0.7 --roll 137.5 \
    --seed 42
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `lstring.txt` | 12.1 KB |
| `run_log.txt` | 94 B |
| `stats.csv` | 92 B |
| `tree.mtl` | 175 B |
| `tree.obj` | 357.0 KB |

<details><summary>First lines of <code>lstring.txt</code></summary>

```
_(0.08)F(1.0)[+(40.0)/(137.5)_(0.055999999999999994)F(0.75)[+(40.0)/(137.5)_(0.03919999999999999)F(0.5625)[+(40.0)/(137.5)_(0.027439999999999992)F(0.421875)[+(40.0)/(137.5)_(0.019207999999999992)F(0.3
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
8 steps: 247 segments, 103 side branches, total length 90.27, bounding box 1.81 x 3.37 x 7.40
```

</details>

<details><summary>First lines of <code>stats.csv</code></summary>

```
segments,side_branches,total_length,size_x,size_y,size_z
247,103,90.274,1.809,3.368,7.395
```

</details>

<details><summary>First lines of <code>tree.mtl</code></summary>

```
newmtl Color_1
	Ka 0.2549019607843137 0.17647058823529413 0.058823529411764705
	Kd 0.7647058823529411 0.5294117647058824 0.17647058823529413
	Ks 0.0 0.0 0.0
	Tr 0.0 
	illum 2
```

</details>

<details><summary>First lines of <code>tree.obj</code></summary>

```
# File generated by PlantGL - Sun Oct 18 01:20:45 2026
v    0.080000 0.000000 0.000000
v    0.080000 0.000000 1.000000
v    0.056569 0.056569 0.000000
v    0.056569 0.056569 1.000000
v    -0.000000 0.080000 0.000000
v    -0.000000 0.080000 1.000000
v    -0.056569 0.056569 0.000000
v    -0.056569 0.056569 1.000000
v    -0.080000 -0.000000 0.000000
v    -0.080000 -0.000000 1.000000
v    -0.056569 -0.056569 0.000000
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--steps` | Derivation steps (bud generations) | 8 | 1 to 10 |
| `--angle` | Branch angle from the axis (degrees) | 40 | 5 to 90 |
| `--ratio` | Side-branch length ratio | 0.75 | 0.3 to 0.95 |
| `--branch_prob` | Probability of a side branch per step | 0.7 | 0.05 to 1 |
| `--roll` | Roll around the axis between branches (degrees) | 137.5 | 0 to 180 |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The helper `run_lpy.py` writes the rules above with your numbers, derives the string, and writes five files.

- `run_log.txt`: "8 steps: 247 segments, 103 side branches, total length 90.27, bounding box 1.81 x 3.37 x 7.40".
- `lstring.txt` (12,373 bytes) is the derived string. It starts `_(0.08)F(1.0)[+(40.0)/(137.5)_(0.056)F(0.75)[...`: set the width to 0.08, draw a segment of length 1.0, start a branch, turn 40 degrees, roll 137.5 degrees, narrow to 0.056, and draw a segment of 0.75.
- `stats.csv` repeats the counts: 247 segments (`F` symbols), 103 side branches (`[` symbols), a summed length of 90.274, and the box size on each axis.
- `tree.obj` (365,562 bytes) and `tree.mtl` hold the geometry as cylinders. Open them in Blender or MeshLab.

The box is 7.40 tall. The main axis alone gives that: its nine segments are 1, 0.95, 0.9025 and so on, summing to 7.40. The height stayed 7.40 in every 8-step run below, so only the width and depth change with the settings.

## Your own runs

Each run changes one value from the example (8 steps, 40 degrees, ratio 0.75, branch probability 0.7, roll 137.5, seed 42).

| Change | Segments | Side branches | Total length | Box (x, y, z) |
|---|---|---|---|---|
| Example | 247 | 103 | 90.27 | 1.81, 3.37, 7.40 |
| Seed 43 | 228 | 91 | 86.57 | 1.81, 3.37, 7.40 |
| 10 steps | 721 | 295 | 202.76 | 2.28, 3.99, 8.62 |
| Angle 70 | 247 | 103 | 90.27 | 2.77, 4.84, 7.40 |
| Angle 15 | 247 | 103 | 90.27 | 0.74, 1.44, 7.40 |
| Branch probability 1.0 | 511 | 255 | 167.98 | 1.81, 3.37, 7.40 |
| Branch probability 0.3 | 65 | 18 | 34.52 | 1.34, 2.89, 7.40 |
| Roll 0 | 247 | 103 | 90.27 | 0.16, 3.91, 7.40 |
| Length ratio 0.9 | 247 | 103 | 149.08 | 2.73, 4.02, 7.40 |

- **Same seed, same tree.** Two runs with seed 42 gave an identical `lstring.txt`.
- **Angle changes only the shape.** The counts and the total length are the same for 15, 40 and 70 degrees, and the box width goes from 0.74 to 2.77.
- **Branch probability changes the counts.** With probability 1.0 every bud branches. The 8-step run then has 511 segments and 255 side branches. With 10 steps it had 2047 segments and 1023 side branches.
- **No roll flattens the tree.** With roll 0 all branches lean in the same plane, and the x size fell to 0.16.

## Pitfalls

- **Counts grow fast with steps and probability.** At probability 1.0, 10 steps gave 2047 segments and a 3.2 MB OBJ file. The recipe allows at most 10 steps.
- **Random choices use Python's generator.** The helper seeds it inside the L-system's `Start` function, so one seed gives one tree.
- **Lengths are in arbitrary units.** The first segment is 1.0. Scale the OBJ in your viewer.
- **No display.** The image sets `QT_QPA_PLATFORM=offscreen`, and the runs used no display.

## Further reading

- L-Py documentation: https://lpy.readthedocs.io/
- Source: https://github.com/openalea/lpy
- PlantGL (geometry and viewer used by L-Py): https://github.com/openalea/plantgl
- Book: Prusinkiewicz P, Lindenmayer A. The Algorithmic Beauty of Plants. Springer, 1990. Free PDF at http://algorithmicbotany.org/papers/abop/abop.pdf
- Paper: Boudon F et al. (2012) L-Py: an L-system simulation framework for modeling plant architecture development based on a dynamic language. Frontiers in Plant Science 3:76. https://doi.org/10.3389/fpls.2012.00076

---

Cite: Boudon F, Pradal C, Cokelaer T, Prusinkiewicz P, Godin C (2012). L-Py: an L-system simulation framework for modeling plant architecture development based on a dynamic language. Frontiers in Plant Science 3:76. doi:10.3389/fpls.2012.00076

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/l-py).
