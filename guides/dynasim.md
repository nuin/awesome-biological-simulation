# DynaSim

> MATLAB and GNU Octave toolbox that builds, simulates and explores ODE-based neural models and networks from text equations.

Licence: MIT · [Source code](https://github.com/DynaSim/DynaSim)

## What it simulates

DynaSim is a toolbox for writing, solving and analysing systems of ordinary differential equations, built for neural models. You write equations as text strings. DynaSim turns them into a MATLAB solver function, integrates them, and returns a data structure with the state variables, the time vector and a copy of the model.

Models are organised into populations (nodes) and connections between them. Reusable pieces, called mechanisms, define ion channels or synapses once and attach them to many populations. Predefined populations, such as Izhikevich or Hodgkin-Huxley cells, shorten the setup. The same equations work for any ODE system, and the getting-started tutorial begins with the Lorenz attractor.

DynaSim also runs sets of simulations over parameter ranges, saves results, and has a graphical interface started with the command `dynasim`.

## When to use it

Use DynaSim if you work in MATLAB (or Octave) and want to define neural network models as equations, then sweep parameters on a cluster or on a desktop.

- Use [PyRates](pyrates.md) for a Python tool that generates code for population models.
- Use [Brian2CUDA](brian2cuda.md) or Brian 2 when you want Python and equation-based neuron models with GPU options.
- Use [Rockpool](rockpool.md) when the goal is a trained spiking network.

## Install

There is no recipe for this tool. It runs in MATLAB, which needs a paid licence, or in GNU Octave. The repository states support for both, but a container run of the Octave path has not been checked here.

DynaSim has no package-manager release. The latest GitHub release is v1.1 (2022-02-02), and the licence is MIT. The README gives two steps:

1. Download the repository as a zip file, or clone it:

   ```bash
   git clone https://github.com/DynaSim/DynaSim.git
   ```

2. Add it to the MATLAB or Octave path, in `startup.m` or at the command window:

   ```matlab
   addpath(genpath('YOUR/PATH/TO/DynaSim'))
   ```

Full instructions are on the [installation wiki page](https://github.com/DynaSim/DynaSim/wiki/Installation).

## A first run

Adapted from the [Getting Started tutorial](https://github.com/DynaSim/DynaSim/wiki/DynaSim-Getting-Started-Tutorial). The tutorial first sets an output folder with `dsGetConfig('demos_path')`, then simulates the Lorenz system:

```matlab
eqns={
  's=10; r=27; b=2.666'
  'dx/dt = s*(y-x);       x(0)=1'
  'dy/dt = r*x - y - x*z; y(0)=2'
  'dz/dt = -b*z + x*y;    z(0)=.5'
};
data = dsSimulate(eqns, 'tspan',[0 100], 'solver','rk4');
figure; plot(data.pop1_x, data.pop1_z);
```

`tspan` is in milliseconds, and `solver` defaults to `rk4`. Other fixed-step choices are `euler` and `rk2`, and any built-in MATLAB solver such as `ode45` works.

The next tutorial section simulates an Izhikevich neuron with a current step between 200 and 800 ms, then builds a PING (pyramidal-interneuron gamma) network from populations.

## Reading the output

- `data` is a structure. Variables are prefixed with the population name, which defaults to `pop1`, so the Lorenz state appears as `data.pop1_x`, `data.pop1_y` and `data.pop1_z`.
- The time vector and a copy of the model that was simulated sit in the same structure.
- Quantities marked with `monitor` in the equations, such as `monitor I`, are recorded and returned too.
- DynaSim writes the generated solver into a `solve` folder. The path is in `data.simulator_options.solve_file`, and you can open or rerun it.
- The Lorenz plot of `z` against `x` should show the butterfly shape. The tutorial shows an image of it.

## Pitfalls

- **Units are milliseconds.** Time constants and `tspan` use ms.
- **Generated files accumulate.** Each simulation writes a solver file. Set the output folder with the config command first.
- **Population names prefix variables.** Rename populations before comparing models, or the field names differ.
- **Octave is a second path.** The README names it, but test your model there before relying on it.
- **The last release is from 2022.** Check open issues for your MATLAB version.

## Further reading

- Documentation: https://dynasim.github.io/docs
- Function reference: https://dynasim.github.io/docs/function_reference
- Source: https://github.com/DynaSim/DynaSim
- Sherfey JS, et al. (2018). DynaSim: a MATLAB toolbox for neural modeling and simulation. Front Neuroinform 12:10. https://doi.org/10.3389/fninf.2018.00010

---

Cite: Sherfey JS, Soplata AE, Ardid S, Roberts EA, Stanley DA, Pittman-Polletta BR, Kopell NJ (2018). DynaSim: a MATLAB toolbox for neural modeling and simulation. Front Neuroinform 12:10. doi:10.3389/fninf.2018.00010

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/dynasim).
