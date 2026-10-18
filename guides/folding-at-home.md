# Folding@home

> A volunteer distributed-computing project that runs molecular dynamics of protein folding and dynamics on donated computers, through a client that fetches work from project servers.

Licence: GPL-3.0 · [Source code](https://github.com/FoldingAtHome/fah-client-bastet)

## What it simulates

Folding@home is a distributed computing project. People around the world install a client, and each computer runs a piece of a large molecular dynamics study of how proteins fold, misfold and move. The project's README links protein misfolding to diseases such as Alzheimer's, ALS, Huntington's and Parkinson's, and to many cancers. A published example of its scale is a study of the SARS-CoV-2 spike protein (Zimmerman et al., 2021) that used the network to run simulations at exascale.

The repository named in this entry is the version 8 client back end, called `fah-client` (code name bastet). It does not simulate anything by itself. It is a daemon that:

1. asks a project Assignment Server for a work unit;
2. downloads the work unit data from a Work Server;
3. downloads the science core binary for that work unit type (the cores are OpenMM-based);
4. runs the core as a subprocess;
5. uploads the results, and repeats, scaled to the CPU and GPU resources you allow.

You do not choose the system, force field or length of the run. The project's scientists choose them and send work units to the clients.

## When to use it

Use Folding@home to donate idle computer time to the project's studies. It is not a tool for running your own simulation.

Alternatives for running your own molecular dynamics:

- [OpenMM](openmm.md) is the toolkit behind the cores, scriptable from Python.
- [GROMACS](gromacs.md) is a fast command-line package for biomolecular dynamics.
- [LAMMPS](lammps.md) fits materials and coarse-grained systems.

## Install

This guide has no run recipe. The client works only by talking to Folding@home servers: it requests a work unit, downloads the core and returns results. The sandbox on this site has no network, and there is no offline mode or example work unit.

Official routes:

- **Installers.** The download page at https://foldingathome.org/start-folding/ lists the latest releases of the client software and links the v8.5 Client Users Guide. A macOS uninstaller is offered there too.
- **Web control panel.** The client is controlled from a web frontend at https://app.foldingathome.org/. The client serves a local HTTP port, and an optional link to a Folding@home account lets the frontend control it remotely.
- **From source (Debian Linux).** The README lists the prerequisites (`scons`, `git`, `npm`, `build-essential`, `fakeroot`, `libssl-dev`, `zlib1g-dev`, `libbz2-dev`, `liblz4-dev`, `libsystemd-dev`). It then builds three repositories:

```
git clone https://github.com/cauldrondevelopmentllc/cbang
git clone https://github.com/foldingathome/fah-client-bastet
git clone https://github.com/foldingathome/fah-web-client-bastet
export CBANG_HOME=$PWD/cbang
scons -C cbang
scons -C fah-client-bastet
scons -C fah-client-bastet package
sudo apt install ./fah-client-bastet/fah-client_<version>_amd64.deb
```

The latest tag is v8.5.6. An RPM build is described in `BUILDING-RPM.md`. The package starts a system service named `fah-client`. Logs go to `/var/log/fah-client` and data to `/var/lib/fah-client`. The licence is GPL-3.0.

## A first run

Adapted from the [README](https://github.com/FoldingAtHome/fah-client-bastet#readme). After installation the service starts on its own and restarts at boot:

```
systemctl status --no-pager -l fah-client
sudo systemctl stop fah-client
sudo systemctl start fah-client
```

Then open https://app.foldingathome.org/ in a browser to see the client, set how many CPU cores and which GPUs it may use, and pause or resume folding. To test the frontend locally instead, run `npm i` and `npm run dev` in `fah-web-client-bastet` and open http://localhost:3000/.

If you start `fah-client` by hand in a terminal, the data and log folders appear in the folder you ran it from.

## Reading the output

You do not read raw output. The client uploads the result of each work unit to the project. The frontend shows the work units in progress, their progress and the logs. The project reports its findings in papers, and the project site has statistics. An optional account lets you link several machines and count your contribution.

## Pitfalls

- **It needs a network.** Work is fetched and returned over the internet, so a machine on a closed network cannot fold.
- **Load on your machine.** The client uses the CPU and GPU resources you give it. Set limits in the frontend if you share the machine.
- **Older clients are removed.** The Debian package removes Folding@home clients older than version 8.
- **Not a lab tool.** There is no way to submit your own system. For that, run OpenMM or GROMACS.
- **Sudo and service.** The package runs as a system service, so installing needs administrator rights.

## Further reading

- Client source and README: https://github.com/FoldingAtHome/fah-client-bastet
- Architecture notes: https://github.com/FoldingAtHome/fah-client-bastet/blob/master/ARCHITECTURE.md
- Project site and downloads: https://foldingathome.org
- Shirts M, Pande VS (2000). Science 290:1903-1904. https://doi.org/10.1126/science.290.5498.1903
- Beberg AL et al. (2009). Folding@home: lessons from eight years of volunteer distributed computing. IPDPS. https://doi.org/10.1109/IPDPS.2009.5160922
- Zimmerman MI et al. (2021). Nature Chemistry 13:651-659. https://doi.org/10.1038/s41557-021-00707-0

---

Cite: Shirts M, Pande VS (2000). Screen savers of the world unite! Science 290:1903-1904. doi:10.1126/science.290.5498.1903

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/folding-at-home).
