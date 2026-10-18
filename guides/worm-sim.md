# worm-sim

> A browser demo in which a simulated C. elegans connectome steers a crawling worm toward food you drop on the page.

Licence: MIT · [Source code](https://github.com/heyseth/worm-sim)

## What it simulates

worm-sim is a web page. It runs a model of the C. elegans nervous system in JavaScript and uses the output to move a drawn worm. C. elegans is a roundworm with a fully mapped connectome, the wiring diagram of its neurons. The page loads that map (`connectome.js`) and updates neuron activity each animation frame.

The README states the setup. Hunger neurons are stimulated continuously. If the worm nears food, food-sensing neurons are stimulated. If its nose reaches the edge of the window, nose-touch neurons fire and the worm backs away. If its tail then bumps the edge, tail-touch neurons send it forward again.

The worm is a chain of linked body nodes. Neuron output goes to dorsal and ventral muscle activation in 24 muscle rows from head to tail. According to the README, nothing injects a bending wave into the muscles: it arises from head motor neurons (SMD and RMD, swinging about 0.6 times a second) and from proprioception in the B-type motor neurons. Command interneurons choose the direction (AVB and PVC for forward, AVA, AVD and AVE for backward). Reversals start at random about once or twice a minute and end in an omega turn. The body is overdamped, with drag 30 times higher sideways than lengthwise, and the README says that difference is what turns the bending wave into motion at about 0.2 body lengths a second.

## When to use it

Use worm-sim to show students how a connectome can drive behaviour, or to watch a sensory-to-motor loop without installing anything.

- Use [PyNN](pynn.md) or NEST when you need a quantitative network model you can parameterise and record.
- Use OpenWorm's tools for a full biophysical C. elegans model (a separate, much larger project).
- Use [RatInABox](ratinabox.md) for synthetic data from an exploring animal.

worm-sim is a demonstration, not a research simulator. It has no parameter forms, no data export and no published validation.

## Install

Nothing to install. The README sends you to the live page: https://heyseth.github.io/worm-sim/. The author's site, https://sethm.me/worm-sim/, serves the same app. Both responded when checked.

To run it offline, clone https://github.com/heyseth/worm-sim and open `index.html`, which loads `js/connectome.js`, `js/constants.js` and `js/main.js` and a stylesheet from `css/`. The repository has no build step. The page fetches one web font from Google Fonts, so it falls back to a default font offline. If your browser blocks scripts from local files, serve the folder with any static file server. The licence is MIT (Copyright 2017 Seth Miller).

## A first run

Open the page and watch. The README describes the controls:

1. The worm crawls on its own.
2. Click or tap anywhere to drop food. The worm follows the scent and leaves faint tracks in the agar.
3. Use the corner panel to watch the connectome. Each dot is a neuron, laid out on a spiral with the most connected neurons in the middle. A dot flashes when its neuron fires. Hover or tap a dot to see the neuron's name.
4. The toolbar at the bottom recenters the worm, clears food, hides the connectome panel and links to the source.

The page follows your device's light or dark theme.

Adapted from the [worm-sim README](https://github.com/heyseth/worm-sim#usage).

## Reading the output

There is no file output. What you read is on screen:

- **Neuron dots.** Flashes show which neurons fire. Command neurons for forward motion (AVB, PVC) and backward motion (AVA, AVD, AVE) take turns, and the active group silences the other.
- **Muscle bars.** Two rows of bars below the panel show dorsal and ventral muscle activation from head to tail. A bending wave moves along them: head to tail for forward crawling, tail to head for backward.
- **Worm path.** Tracks in the agar show where the worm went. Drop food and compare the track before and after.
- **Reversals.** A nose touch at the window edge makes a reversal almost certain, the README says. Long reversals end in a deep ventral bend of the head, the omega turn.

The only numbers the README gives are the 0.6 times a second head rhythm and the 0.2 body lengths a second speed above.

## Pitfalls

- **It is a toy model.** The README describes a simplified body and a connectome with simple rules. Do not read the activity as a measured C. elegans recording.
- **The window is the arena.** The edges of the browser window act as walls, so a resized window changes the behaviour.
- **No seed.** There is no control for repeating a run. Reversals are random.
- **Frame rate matters.** Neuron activity updates per animation frame, so a busy browser tab may slow the worm.
- **No data export.** To keep a result, take a screenshot or screen recording.

## Further reading

- Live demo: https://heyseth.github.io/worm-sim/
- Source and README: https://github.com/heyseth/worm-sim
- The GoPiGo Connectome project the connectome code comes from: https://github.com/Connectome/GoPiGo
- Boyle JH, Berri S, Cohen N (2012). Gait Modulation in C. elegans: An Integrated Neuromechanical Model. Frontiers in Computational Neuroscience 6. https://doi.org/10.3389/fncom.2012.00010 (cited by the README for the proprioception mechanism)

---

Cite: Miller S (2017). worm-sim: simulate the C. elegans worm brain in your browser. https://github.com/heyseth/worm-sim

This guide is also on [biosimhub](https://biosimhub.pages.dev/guide/worm-sim).
