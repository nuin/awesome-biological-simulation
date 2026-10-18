# Auryn

> Event-driven C++ simulator for recurrent spiking neural networks with synaptic plasticity such as STDP.

Licence: GPL-3.0-or-later · [Source code](https://github.com/fzenke/auryn)

## What it simulates

Auryn simulates recurrent spiking neural networks in C++. Neurons are integrate-and-fire units, and synapses can change with spike timing, for example through spike-timing-dependent plasticity (STDP). The simulator is event-driven: work happens when a spike is emitted or received, so quiet networks cost little.

You write a C++ program that builds neuron groups and connections, attaches monitors, and calls the run loop. Auryn ships with example programs. The best known is `sim_coba_benchmark`, the Vogels-Abbott network of conductance-based neurons that the Auryn paper used to compare speed against other simulators.

In that example the network has 3200 excitatory and 800 inhibitory neurons, connected at 2% sparseness, with a refractory period of 5 ms. Time runs in seconds. The program writes spike times to files and the elapsed wall-clock time to `elapsed.dat`.

## When to use it

Use Auryn when you need fast single-machine or MPI simulation of plastic point-neuron networks and are happy to write C++.

- Use [Rockpool](rockpool.md) when you want Python layers, gradient training, or deployment to neuromorphic chips.
- Use [CARLsim 6](carlsim6.md) when you want GPU execution of Izhikevich networks from a C++ library.
- Use [Brian2CUDA](brian2cuda.md) when you want to write models as equations in Python and run them on an NVIDIA GPU.

## Install

Auryn 0.8.4 (released 2025-03-11) builds from source. The project README gives these steps for Debian-based Linux. They need a C++ compiler, CMake and Boost with MPI support.

```bash
sudo apt-get install cmake git build-essential libboost-all-dev
git clone https://github.com/fzenke/auryn.git && cd auryn/build/release
./bootstrap.sh && make
```

To install the library for your own programs, run `sudo make install`, or `make DESTDIR=./your/dir/ install` for a local copy. The licence is GPL-3.0-or-later.

The recipe below builds the tag v0.8.4 on Ubuntu 22.04 with Open MPI. It builds and runs on biosimhub; the recorded output is listed with the recipe below.

## Run the tested example

This recipe builds Auryn in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-17 in 5.6 s. Auryn has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower.

1. Download [auryn-recipe.tar.gz](https://biosimhub.pages.dev/guides/auryn/auryn-recipe.tar.gz) (Dockerfile, run-auryn, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf auryn-recipe.tar.gz
   cd auryn
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build --platform linux/amd64 -t biosimhub/auryn:0.8.4 .
mkdir -p out && chmod a+w out
docker run --rm --platform linux/amd64 \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/auryn:0.8.4 run-auryn --simtime 5 > out/run_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `coba.0.e.ras` | 3.5 MB |
| `coba.0.i.ras` | 862.6 KB |
| `elapsed.dat` | 2 B |
| `run_log.txt` | 2.2 KB |
| `sim_coba_benchmark.0.log` | 1.3 KB |

<details><summary>First lines of <code>coba.0.e.ras</code></summary>

```
0.013800 0
0.013800 1
0.013800 2
0.013800 3
0.013800 4
0.013800 5
0.013800 6
0.013800 7
0.013800 8
0.013800 9
0.013800 10
0.013800 11
```

</details>

<details><summary>First lines of <code>coba.0.i.ras</code></summary>

```
0.013800 0
0.013800 1
0.013800 2
0.013800 3
0.013800 4
0.013800 5
0.013800 6
0.013800 7
0.013800 8
0.013800 9
0.013800 10
0.013800 11
```

</details>

<details><summary>First lines of <code>elapsed.dat</code></summary>

```
1
```

</details>

<details><summary>First lines of <code>run_log.txt</code></summary>

```
( 0) Setting up neuron groups ...
( 0) Setting up E connections ...
( 0) Setting up I connections ...
( 0) Setting up monitors ...
( 0) Simulating ...

[>                   ]   0%      t=0.0s
[>                   ]   2%      t=0.1s
[>                   ]   4%      t=0.2s
[=>                  ]   6%      t=0.3s
[=>                  ]   8%      t=0.4s
[==>                 ]  10%      t=0.5s
```

</details>

<details><summary>First lines of <code>sim_coba_benchmark.0.log</code></summary>

```
10/18/26 04:17:57:: Logger started on Rank 0
10/18/26 04:17:57:: Starting Auryn Kernel
10/18/26 04:17:57:: Auryn version 0.8.4-30beee9 ( compiled Oct 18 2026 04:15:20 )
10/18/26 04:17:57:: Git repository revision v0.8.4
10/18/26 04:17:57:: Simulation timestep is set to 1.000000e-04s  
10/18/26 04:17:57:: Auryn was compiled with MPI support.
10/18/26 04:17:57:: Not running a parallel simulation.
10/18/26 04:17:57:: Setting up neuron groups ...
10/18/26 04:17:57:: SpikingGroup (SpikingGroup.cpp): :: Size 3200
10/18/26 04:17:57:: SpikingGroup (SpikingGroup.cpp): :: Size 800
10/18/26 04:17:57:: Setting up E connections ...
10/18/26 04:17:57:: Setting up I connections ...
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--simtime` | Simulated time (s) | 5 | 0.5 to 30 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## A first run

Adapted from the [Auryn README](https://github.com/fzenke/auryn#run-a-first-network-simulation). After the build, run the benchmark from the examples directory:

```bash
cd examples
./sim_coba_benchmark --dir .
```

The README states that spiking activity goes to files with the extension `ras`. With gnuplot installed, it plots the excitatory raster like this:

```bash
echo "set xlabel 'Time [s]'; plot [1:2] 'coba.0.e.ras' with dots lc rgb 'black'" | gnuplot -p
```

The program accepts `--simtime` (model seconds), `--dir` (where files go), and `--fast`, which turns off most monitoring. The source sets the default run to 20 model seconds and the default directory to `/tmp`, so pass `--dir`.

## Reading the output

- `coba.0.e.ras` and `coba.0.i.ras` hold the spikes of the excitatory and inhibitory groups. The `0` is the MPI rank. Each line is one spike. The README plot uses the first column as time in seconds and the second as the neuron index, so a dot plot is a raster.
- `elapsed.dat` holds the wall-clock seconds of the run, written by rank 0. Compare it with the model time to get the real-time factor.
- The log file in the output directory records progress messages from the run.

In a balanced network like this one, expect irregular, asynchronous firing after a start-up transient. Check the raster for that pattern before you trust a change you make to weights or input.

## Pitfalls

- **Boost must have MPI support.** The README requires it. A Boost build without MPI fails at compile time.
- **`--fast` writes no spike files.** It exists for benchmarking. Drop it when you want a raster.
- **Output goes to `/tmp` by default.** Always set `--dir`.
- **File names carry the MPI rank.** A run on several ranks writes `coba.0...`, `coba.1...` and so on, and you merge them yourself.
- **Time units are seconds, not milliseconds.** The refractory period in the source is `5.0e-3`.
- **Auryn is a library, not a model language.** Changing the network means editing and recompiling C++.

## Further reading

- Documentation: https://www.fzenke.net/auryn/
- Source and examples: https://github.com/fzenke/auryn
- Paper: Zenke F, Gerstner W (2014). Limits to high-speed simulations of spiking neural networks using general-purpose computers. Front Neuroinform 8:76. https://doi.org/10.3389/fninf.2014.00076

---

Cite: Zenke F, Gerstner W (2014). Limits to high-speed simulations of spiking neural networks using general-purpose computers. Front Neuroinform 8:76. doi:10.3389/fninf.2014.00076

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/auryn).
