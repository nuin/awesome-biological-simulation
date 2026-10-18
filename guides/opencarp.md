# openCARP (single-cell bench)

> Run a single-cell cardiac ionic model with periodic stimuli using openCARP's bench tool and return the transmembrane voltage and ionic current traces.

Licence: LicenseRef-openCARP-Academic-Public-License · [Source code](https://opencarp.org/)

## What it simulates

openCARP is a cardiac electrophysiology simulator for tissue and organ models. Its `bench` tool is the single-cell part. It integrates one cell's ionic model, a set of ordinary differential equations for the membrane voltage, ion channel currents and ion concentrations. A stimulus current is injected at set times, and `bench` writes the voltage and chosen currents over time.

You pick an ionic model with `--imp`, such as `tenTusscherPanfilov` (a human ventricular cell) or `OHara`. You set the stimulus (strength, duration, count, spacing) and the run length. Units are ms, mV and uA/cm^2.

The example paces one cell twice, 500 ms apart, with a 1 ms stimulus of 30 uA/cm^2, for 1000 ms. The key assumption is that the cell is isolated. There is no coupling to neighbors, so the output shows the cell's own action potential (AP) response to the pacing.

## When to use it

Use `bench` for single-cell questions:

- How long is the action potential for a given model and pacing rate?
- What stimulus strength triggers an action potential?
- How do models differ in their currents, for example ICaL or IKr?

[PyLEMS](pylems.md) runs models written in LEMS and [XPPAUT](xppaut.md) runs general ODE systems. Use openCARP when you want a curated cardiac ionic model (the recipe lists 16 models for `--imp`: tenTusscherPanfilov, LuoRudy91, LuoRudy94, Courtemanche, Grandi, OHara, Tomek, Fabbri, MitchellSchaeffer, AlievPanfilov, HodgkinHuxley, Fox, Shannon, Nygren, Maleckar and Skibsbye). Tissue and organ simulations need the full openCARP, which this guide does not cover.

## Install it yourself

The conda-forge package is `opencarp`. A dry run `micromamba create -n t --dry-run -c conda-forge -c bioconda opencarp=19.0.0` resolves opencarp 19.0.0 on linux-aarch64. The package license is the openCARP Academic Public License.

```
conda create -n opencarp -c conda-forge opencarp=19.0.0
conda activate opencarp
```

The minimal command is the tool's own, with no helper script:

```
bench --imp tenTusscherPanfilov --stim-curr 30 --stim-dur 1 --duration 1000 \
      --numstim 2 --bcl 500 --dt 0.01 --dt-out 1 --fout=bench_vm
```

`bench --list-imps` lists models. `bench --imp tenTusscherPanfilov --imp-info` prints that model's tunable parameters and state variables. `bench --help` shows all options. The ones used here: `--stim-curr` (default 60), `--stim-dur` (default 1 ms), `--numstim` (default 1), `--bcl` (default 1000 ms), `--dt` (default 0.01 ms), `--dt-out` (default 1 ms), `--fout` and `--duration`.

## Run the tested example

This recipe builds openCARP (single-cell bench) in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else. It last ran on 2026-10-12 in 0.8 s.

1. Download [opencarp-recipe.tar.gz](https://biosimhub.pages.dev/guides/opencarp/opencarp-recipe.tar.gz) (Dockerfile, run.sh).
2. Unpack it and run the script:

   ```sh
   tar -xzf opencarp-recipe.tar.gz
   cd opencarp
   sh run.sh
   ```

<details><summary>What run.sh does</summary>

```sh
docker build -t biosimhub/opencarp:19.0.0 .
mkdir -p out && chmod a+w out
docker run --rm \
  --user "$(id -u):$(id -g)" -e HOME=/tmp \
  -v "$PWD/in:/work/in:ro" -v "$PWD/out:/work/out" -w /work/out \
  biosimhub/opencarp:19.0.0 bench --imp tenTusscherPanfilov --stim-curr 30 \
    --stim-dur 1 --duration 1000 --numstim 2 --bcl 500 \
    --dt 0.01 --dt-out 1 --fout=bench_vm > out/bench_log.txt
```

Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.

</details>

### Expected output

| File | Size |
|---|---:|
| `Trace_0.dat` | 256.4 KB |
| `bench_log.txt` | 273 B |
| `bench_vm.txt` | 43.0 KB |
| `tenTusscherPanfilov_trace_header.txt` | 83 B |

<details><summary>First lines of <code>Trace_0.dat</code></summary>

```
0.0000000000	1.299999979229	0.000070000619	0.000069999256	-0.003450196379	0.116749639327	0.000000002832	-0.000000000001	-0.000003715271	-0.172870754261	0.179392686024	-0.132160126636	-0.047497654914	0
1.0000000000	1.299997690453	0.000070062520	0.000069925152	-0.003454258102	0.193418872375	0.000000308204	-0.000000008067	-0.000004624438	-0.171711822904	0.180392786951	-0.131967933942	-0.047399400455	0
2.0000000000	1.299995032083	0.000070283537	0.000069876344	-0.038842005877	1.540812848632	0.000029373296	0.000000145413	-8.051484950423	-0.091627973384	0.255154035745	-0.114739843106	-0.038957196641	0.
3.0000000000	1.299992249736	0.000092358769	0.000069899080	-3.697634419850	0.000610844468	0.208333186196	0.000033995591	-7.571675317035	0.111584012725	0.331938805313	-0.057772888459	-0.011040975858	0.0
4.0000000000	1.299989851755	0.000262691607	0.000069987115	-7.333799029466	0.001299940416	0.569296137131	0.000185458077	-0.000242627217	0.094525493943	0.330094772968	-0.062603850314	-0.013412439598	0.0
5.0000000000	1.299987897092	0.001741588299	0.000070076051	-9.349260460360	0.002335254676	0.510098510053	0.000367118125	-0.000000047918	0.081669015201	0.328438301834	-0.066378249141	-0.01526644965
```

</details>

<details><summary>First lines of <code>bench_log.txt</code></summary>

```




All done!


setup time          0.000347 s
initialization time 0.018839 s
main loop time      0.052516 s
total ode time      0.018574 s

```

</details>

<details><summary>First lines of <code>bench_vm.txt</code></summary>

```
     0.000 -8.62000000e+01 -4.47465931e-02 
     1.000 -8.61604097e+01 -3.48607207e-02 
     2.000 -5.68083015e+01 -5.14133397e+00 
     3.000 +3.94378711e+01 -4.83168724e+00 
     4.000 +3.13859499e+01 +8.99019495e+00 
     5.000 +2.49430252e+01 +3.96319193e+00 
     6.000 +2.27585524e+01 +8.69204537e-01 
     7.000 +2.25934851e+01 -3.03122710e-01 
     8.000 +2.30855337e+01 -5.98332891e-01 
     9.000 +2.37088680e+01 -6.31750050e-01 
    10.000 +2.43406292e+01 -6.33967339e-01 
    11.000 +2.49846906e+01 -6.57762827e-01 
```

</details>

<details><summary>First lines of <code>tenTusscherPanfilov_trace_header.txt</code></summary>

```
sv->CaSR
sv->CaSS
sv->Cai
ICaL
IK1
IKr
IKs
INa
INaCa
INaK
IbCa
IbNa
```

</details>

### Parameters

| Option | Meaning | Example value | Range |
|---|---|---|---|
| `--imp` | Ionic cell model | tenTusscherPanfilov | tenTusscherPanfilov, LuoRudy91, LuoRudy94, Courtemanche, Grandi, OHara, Tomek, Fabbri, MitchellSchaeffer, AlievPanfilov, HodgkinHuxley, Fox, Shannon, Nygren, Maleckar, Skibsbye |
| `--stim-curr` | Stimulus current (uA/cm2) | 30 | 0 to 500 |
| `--stim-dur` | Stimulus duration (ms) | 1 | 0.1 to 20 |
| `--duration` | Simulated duration (ms) | 1000 | 10 to 20000 |
| `--numstim` | Number of stimuli | 2 | 1 to 100 |
| `--bcl` | Basic cycle length (ms) | 500 | 50 to 5000 |
| `--dt` | Integration time step (ms) | 0.01 | 0.001 to 0.1 |
| `--dt-out` | Output interval (ms) | 1 | 0.1 to 100 |

Ranges are the limits used for the example recipe; the program itself may accept more.


## Reading the output

The command writes three kinds of file, plus the log on standard output.

- `bench_vm.txt` (44044 bytes) has 1001 lines at 1 ms steps. The first column is time and the second is the voltage. It starts at 0 ms with -86.2 mV. At 3 ms the voltage is +39.4 mV, the peak of the first action potential. A third column follows, which the bench help does not name.
- `Trace_0.dat` (262588 bytes) is tab-separated with 1001 rows and 17 columns. Column 1 is time. The other 16 are listed in `tenTusscherPanfilov_trace_header.txt`: `sv->CaSR`, `sv->CaSS`, `sv->Cai`, `ICaL`, `IK1`, `IKr`, `IKs`, `INa`, `INaCa`, `INaK`, `IbCa`, `IbNa`, `IpCa`, `IpK`, `Ito` and `V`.
- `bench_log.txt` (273 bytes) holds the timing. The main loop took 0.0525 s for 1000 ms of cell time.

In `Trace_0.dat`, row 3 (t = 2 ms) has INa at -8.05 uA/cm^2, and the voltage is -56.8 mV, on the way up to the +39.4 mV peak.

## Your own runs

Copy the docker run line from the recipe and change values. The reference run keeps the voltage above -20 mV for 275 ms after the first stimulus and 518 ms over both.

1. **Another model.** Set `--imp OHara`. The resting voltage was -87.0 mV, against -86.2. The first action potential stayed above -20 mV for 244 ms and the peak was +39.4 mV (39.37 against 39.44 for tenTusscherPanfilov). The run had the same number of files, with a different trace header.
2. **Weaker stimulus.** Set `--stim-curr 5`. No action potential fired. The voltage never rose above -81.5 mV, and it was 0 ms above -20 mV. A 5 uA/cm^2 pulse moved the cell about 5 mV.
3. **Faster pacing.** Set `--bcl 300` and `--numstim 3`. The first beat stayed above -20 mV for 275 ms. At 300 ms the voltage was still -58.2 mV. The second stimulus at 301 ms raised it only to -33.3 mV, and no action potential followed. The third stimulus at 601 ms fired a full action potential of 259 ms above -20 mV.

## Pitfalls

- **Subthreshold stimuli give no error.** The weak run completed with a flat trace. Check the peak voltage in `bench_vm.txt`.
- **Units.** Current is in uA/cm^2 (the same as pA/pF), time in ms and voltage in mV. Do not paste current values from papers in other units.
- **`--duration` and `--numstim`.** The last stimulus must fit inside the duration. With 2 stimuli and 500 ms spacing, 1000 ms covers both beats.
- **Fast pacing skips beats.** At a 300 ms cycle the second stimulus found the cell not yet recovered. Count the beats that fired, because the stimuli sent overcount them.
- **Start state.** Beat one starts from the model's default initial state, so early beats may differ from later ones.

## Further reading

- openCARP site: https://opencarp.org/
- Basic bench example: https://opencarp.org/documentation/examples/01_ep_single_cell/01_basic_bench
- User manual: https://opencarp.org/documentation/user-manual
- Plank G, Loewe A, Neic A, et al. (2021). The openCARP simulation environment for cardiac electrophysiology. Comput Methods Programs Biomed 208:106223. https://doi.org/10.1016/j.cmpb.2021.106223

---

Cite: Plank G, Loewe A, Neic A, et al. (2021). The openCARP simulation environment for cardiac electrophysiology. Comput Methods Programs Biomed 208:106223. doi:10.1016/j.cmpb.2021.106223

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/opencarp).
