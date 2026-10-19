# PyBoolNet

> Find the steady states and attractor candidates of a Boolean network, then run seeded random walks under synchronous, asynchronous or mixed updating.

Licence: LGPL (PyPI classifier; the repository has no LICENSE file) · [Source code](https://github.com/hklarner/pyboolnet)

## What it simulates

PyBoolNet analyses Boolean networks. Each node of the network is ON or OFF, and a logical rule sets its next value from the nodes that regulate it. Gene regulatory and signalling models are often written this way, because a rule such as "E2F is on when Rb is off" needs no rate constants.

You give it a network in `.bnet` format, one rule per line. It returns the attractors, which are the states or cycles the network can settle into, and it can walk the network step by step. Three update schemes decide which nodes change at each step. Synchronous updating changes all nodes at once. Asynchronous updating changes one random node at a time. Mixed updating changes a random subset.

## When to use it

Use PyBoolNet to ask which stable behaviors a regulatory network allows, which inputs lead to which, and what a node knockout or a fixed input does.

- Use [GillesPy2](gillespy2.md) or [COPASI](copasi.md) when you have reaction rates and need amounts over time.
- Use [XPPAUT](xppaut.md) when the model is a set of differential equations and you want bifurcations.
- PyBoolNet also does model checking with CTL and LTL queries and builds state-transition graphs. The biosimhub recipe covers attractors and random walks only.

## Install it yourself

```
pip install pyboolnet==3.0.16
```

The package bundles Linux x86-64 binaries for gringo, clasp, NuSMV-a, espresso and BNetToPrime. This is why the biosimhub image runs as linux/amd64. The NuSMV-a binary links `libreadline.so.6` and `libxml2`, and Debian 12 ships only `libreadline.so.8`. The recipe installs `libxml2` and `libreadline8` with apt, then links `libreadline.so.6` to the version 8 library. Without the link, attractor checks stop with NuSMV return code 127.

A minimal run with the Python API, on the network of the example:

```python
from pyboolnet.file_exchange import bnet2primes
from pyboolnet.trap_spaces import compute_steady_states

primes = bnet2primes(open("network.bnet").read())
print(len(compute_steady_states(primes)))
```

In the 3.0.16 image this printed 7.

## Run the tested example

This recipe builds PyBoolNet in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 7.7 s. PyBoolNet has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [pyboolnet-recipe.tar.gz](https://biosimhub.pages.dev/guides/pyboolnet/pyboolnet-recipe.tar.gz) (Dockerfile, run_pyboolnet.py, example network.bnet, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf pyboolnet-recipe.tar.gz
   cd pyboolnet
   sh run.sh
   ```

![Terminal recording of the PyBoolNet example run](https://biosimhub.pages.dev/media/pyboolnet/run.gif)

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/pyboolnet:3.0.16 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/pyboolnet:3.0.16 python /opt/run_pyboolnet.py --network /work/in/network.bnet \
    --update asynchronous --walks 200 --length 100 \
    --seed 42 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `attractors.txt` | 616 B |
| `run_log.txt` | 265 B |
| `summary.json` | 949 B |
| `trajectory.csv` | 2.2 KB |
| `walks.csv` | 6.8 KB |

<picture><source media="(prefers-color-scheme: dark)" srcset="https://biosimhub.pages.dev/media/pyboolnet/result-dark.png"><img src="https://biosimhub.pages.dev/media/pyboolnet/result.png" alt="Plot of the PyBoolNet example output" width="760"></picture>

Drawn from the example's output files.

<details><summary>First lines of <code>attractors.txt</code></summary>

```
update: asynchronous
complete: yes
steady states: 7
  000000100
  100010110
  000000110
  100110110
  000100110
  110110000
  010100000
attractors (one per minimal trap space): 10
  0: 000000100  steady  free nodes: 0
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
network: 9 nodes, inputs ['DNA_damage', 'GF'], clamped {}, update asynchronous, seed 42
steady states 7, attractors 10 (3 cyclic), complete yes
walks ending in: {'0': 6, '1': 13, '2': 11, '3': 49, '4': 29, '5': 6, '6': 10, '7': 20, '8': 25, '9': 31}
done in 6.31 s
```

</details>

<details><summary>First lines of <code>summary.json</code></summary>

```
{
 "nodes": 9,
 "inputs": [
  "DNA_damage",
  "GF"
 ],
 "clamped": {},
 "update": "asynchronous",
 "seed": 42,
 "walks": 200,
 "walk_length": 100,
 "steady_states": 7,
```

</details>

<details><summary>First lines of <code>trajectory.csv</code></summary>

```
step,CycD,CycE,DNA_damage,E2F,GF,Mdm2,Rb,p27,p53
0,0,0,1,0,0,0,0,0,1
1,0,0,1,0,0,1,0,0,1
2,0,0,1,0,0,1,1,0,1
3,0,0,1,0,0,1,1,0,0
4,0,0,1,0,0,0,1,0,0
5,0,0,1,0,0,0,1,0,1
6,0,0,1,0,0,0,1,1,1
7,0,0,1,0,0,1,1,1,1
8,0,0,1,0,0,1,1,1,0
9,0,0,1,0,0,0,1,1,0
10,0,0,1,0,0,0,1,1,1
```

</details>

<details><summary>First lines of <code>walks.csv</code></summary>

```
walk,end_state,trap_space,CycD,CycE,DNA_damage,E2F,GF,Mdm2,Rb,p27,p53
0,001001111,3,0,0,1,0,0,1,1,1,1
1,000000110,1,0,0,0,0,0,0,1,1,0
2,110110000,8,1,1,0,1,1,0,0,0,0
3,000100110,2,0,0,0,1,0,0,1,1,0
4,111110000,9,1,1,1,1,1,0,0,0,0
5,000000100,0,0,0,0,0,0,0,1,0,0
6,101010111,7,1,0,1,0,1,0,1,1,1
7,111110001,9,1,1,1,1,1,0,0,0,1
8,110110000,8,1,1,0,1,1,0,0,0,0
9,110110000,8,1,1,0,1,1,0,0,0,0
10,000000110,1,0,0,0,0,0,0,1,1,0
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--update` | Update scheme | asynchronous | asynchronous, synchronous, mixed |
| `--walks` | Random walks | 200 | 1 to 5000 |
| `--length` | Steps per walk | 100 | 1 to 2000 |
| `--clamp` | Fixed nodes (e.g. GF=1,DNA_damage=0) | not set | text |
| `--seed` | Seed | 42 | 1 to 2147483647 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The example network has 9 nodes and is not a published model. Two nodes are inputs (growth factor GF and DNA_damage). The others are CycD, CycE, Rb, E2F, p27, p53 and Mdm2. The p53 and Mdm2 pair forms a negative feedback loop: p53 turns Mdm2 on and Mdm2 turns p53 off.

- `run_log.txt` says: 9 nodes, 7 steady states, 10 attractors of which 3 are cyclic, and the attractor set is complete. The 200 walks ended in all 10 attractors.
- `attractors.txt` lists each attractor as a string of 0, 1 and `-` in the node order CycD CycE DNA_damage E2F GF Mdm2 Rb p27 p53. A `-` marks a node that keeps changing inside the attractor. Attractor 3 is `00100-11-`: DNA_damage on, GF off, and Mdm2 and p53 oscillating. It is cyclic, with 2 free nodes.
- `walks.csv` has one row per walk: the end state, the attractor index and every node value. The 200 random start states ended mostly in attractor 3 (49 walks), 9 (31 walks) and 4 (29 walks).
- `trajectory.csv` follows walk 0 for 100 steps. DNA_damage stays 1. By step 10, Rb and p27 are on and stay on. From then on only p53 and Mdm2 change, in a four-step loop: (p53, Mdm2) = (1,0), (1,1), (0,1), (0,0), then back.
- `summary.json` repeats the counts with the seed.

Attractors by input setting, from the 10 above: 4 with GF off and no damage (all steady), 1 cyclic with GF off and damage, 3 steady with GF on and no damage, and 2 cyclic with GF on and damage. A cell with GF on and no damage can sit in attractor 8 (`110110000`: CycD, CycE and E2F on, Rb off), the state that commits to division.

## Your own runs

Each run used the recipe's image, one CPU and seed 42 unless noted.

- **Fix the inputs.** `--clamp GF=1,DNA_damage=0` gave 3 attractors, all steady, and no cycles. The 200 walks ended in `100010110` (41), `100110110` (45) and `110110000` (114). So 57 percent of walks reached the division-committed state.
- **Add damage.** `--clamp GF=1,DNA_damage=1 --walks 500 --length 200` gave 0 steady states and 2 cyclic attractors, `10101-11-` (236 walks) and `11111-00-` (264 walks). With damage, p53 and Mdm2 never settle.
- **Synchronous updating.** `--update synchronous` listed the same 10 attractors. The 200 walks ended in 9 of them, and none ended in attractor 0 (all off except Rb).
- **Another seed.** `--seed 43` gave the same 10 attractors, with walk counts such as 42 in attractor 3 (against 49). The attractor set is fixed by the network, and only the walk tallies depend on the seed.

## Pitfalls

- **Inputs are free by default.** A node with no regulators is an input, and the attractor list covers every input setting. Use `--clamp NAME=0,NAME=1` to fix inputs or knock out a node. A name that is not in the network stops the run with a message.
- **Walk counts are not basin sizes.** The walks start at random states, and asynchronous steps are random, so the counts depend on the seed and the walk length. A length of 100 was long enough for this network. Check yours by doubling it.
- **Cyclic attractors show as trap spaces.** An attractor with `-` entries is a set of states, and the recipe does not list them one by one.
- **Graphviz is absent.** The log starts with "Executable dot not found" lines. Drawing state-transition graphs needs Graphviz, which the image leaves out.
- **Emulation.** The image runs as linux/amd64, so on an ARM host the 9-node example takes about 7 s.

## Further reading

- Source: https://github.com/hklarner/pyboolnet
- Documentation: https://pyboolnet.readthedocs.io
- Paper: Klarner H, Streck A, Siebert H (2017) PyBoolNet: a python package for the generation, analysis and visualization of boolean networks. Bioinformatics 33(5):770-772. https://doi.org/10.1093/bioinformatics/btw682

---

Cite: Klarner H, Streck A, Siebert H (2017). PyBoolNet: a python package for the generation, analysis and visualization of boolean networks. Bioinformatics 33(5):770-772. doi:10.1093/bioinformatics/btw682

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/pyboolnet).
