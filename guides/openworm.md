# OpenWorm

> An integrated simulation of the nematode C. elegans that couples a neuron-level nervous system model (c302) to a 3D body-physics model (Sibernetic), distributed as a Docker stack.

Licence: MIT · [Source code](https://github.com/openworm/OpenWorm)

## What it simulates

OpenWorm aims to build a bottom-up computational model of the roundworm *Caenorhabditis elegans*, an animal with about a thousand cells. The goal is for behaviour such as crawling to emerge from simulated cells built from experimental data.

The `openworm/OpenWorm` repository is the entry point that ties the parts together. The README names two main components:

- **c302**, the nervous system model, run on your computer.
- **Sibernetic**, a 3D body model, run in parallel and driven by the output of the nervous system model.

The run then produces graphs of nervous system and body activity and a movie of the body model. The README shows example graphs of muscle activity and neuron activity and an animation of a crawling worm.

## When to use it

Use OpenWorm to see an integrated whole-organism simulation, for teaching, or as a starting point for work on *C. elegans* modelling. It is not a general neuron simulator. Its components target one animal.

- Use [NEURON](neuron.md) to build and test your own detailed cell models.
- Use [NEST](nest.md) for generic spiking network experiments.
- Use [Brian 2](brian2.md) to prototype neuron and synapse equations quickly.

## Install

OpenWorm has no pip or conda package. The README gives a Docker route:

1. Install Docker. The README asks for at least 60 GB of free disk space and at least 2 GB of RAM.
2. Clone the repository.
3. Optionally run `./build.sh` (`build.cmd` on Windows) to build the image locally. If you skip it, the first run downloads the latest released image from Docker Hub (`openworm/openworm`).

```
git clone http://github.com/openworm/openworm
cd openworm
```

The release in the repository `VERSION` file and on GitHub is 0.9.8 (March 2026). The licence is MIT.

There is no hosted recipe for this tool. The stack needs Docker with tens of gigabytes of images and runs several programs together, which does not fit a small single-command sandbox.

## A first run

Adapted from the [README quickstart](https://github.com/openworm/OpenWorm#running).

```
./run.sh
```

On Windows use `run.cmd`. Docker must be running. The README says about 5 to 10 minutes of output will appear on screen as the steps run. When it ends, run `./stop.sh` to remove the container, then inspect the `output` directory. To change the simulated duration, pass `-d` followed by milliseconds. The default is 15 ms; the README gives 5000 for the full movie (5 seconds).

For a shell inside the container before the simulation starts, use `./run-shell-only.sh`.

## Reading the output

- **Duration.** The default run is deliberately short. The README warns that it gives only a partial version of the example output.
- **Graphs.** Plots of nervous system activity (neurons) and muscle activity come from the c302 run.
- **Movie.** The body-model output is a movie of the simulated worm.
- **Raw data.** Sibernetic writes `worm_motion_log.txt` in a time-stamped folder under `/home/ow/sibernetic/simulations/` inside the container. Copy it out with `docker cp openworm:/home/ow/sibernetic/simulations/<folder>/worm_motion_log.txt .` after you exit the container but before you run `stop.sh`. `stop.sh` deletes the container and its data.

## Pitfalls

- **Disk space.** Plan for 60 GB.
- **`stop.sh` deletes data.** Copy out anything you need first.
- **Short default.** At 15 ms the output covers only a fraction of a second of worm time.
- **Not a validated organism model.** The README states the aim of building the first comprehensive model. Treat results as demonstrations.
- **Docker needed.** The README documents no other install.

## Further reading

- Project site: https://openworm.org
- Documentation: http://docs.openworm.org
- Source: https://github.com/openworm/OpenWorm
- Components: https://github.com/openworm/c302 and https://github.com/openworm/sibernetic
- Paper: Sarma GP, et al. (2018). OpenWorm: overview and recent advances in integrative biological simulation of Caenorhabditis elegans. Phil Trans R Soc B 373:20170382. https://doi.org/10.1098/rstb.2017.0382

---

Cite: Sarma GP, Lee CW, Portegys T, et al. (2018). OpenWorm: overview and recent advances in integrative biological simulation of Caenorhabditis elegans. Phil Trans R Soc B 373:20170382. doi:10.1098/rstb.2017.0382

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/openworm).
