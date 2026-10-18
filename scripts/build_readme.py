#!/usr/bin/env python3
"""Write README.md from data/simulators.json.

    python3 scripts/build_readme.py

Edit the data file, not the README: the README is regenerated from it.
"""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
GUIDES = "https://biosimhub.pages.dev/guide/"

# Section order and titles, with one sentence on what each section covers.
SECTIONS = [
    ("popgen", "Population genetics", "Coalescent and forward-time simulators of genomes in populations."),
    ("phylo-seqevo", "Phylogenetics and sequence evolution", "Trees, sequence evolution along them, and species-level processes."),
    ("ngs-reads", "Sequencing reads and data", "Simulated sequencing reads, variants and single-cell or bulk expression data."),
    ("molecular", "Molecular simulation", "Molecular dynamics, docking, free energy and coarse-grained models."),
    ("systems-bio", "Systems biology", "Biochemical networks, metabolism and rule-based models."),
    ("grn-synbio", "Gene regulation and synthetic biology", "Gene regulatory networks and engineered genetic circuits."),
    ("cell-tissue", "Cells and tissues", "Cell-based, vertex and continuum models of cells and tissues."),
    ("physiology-organ", "Physiology and organs", "Cardiac, musculoskeletal, pharmacokinetic, crop and whole-body models."),
    ("neuroscience", "Neuroscience", "Neurons, networks and brain-scale models."),
    ("epidemiology", "Epidemiology", "Compartmental, network and agent-based disease transmission."),
    ("ecology-abm", "Ecology and agent-based models", "Populations, communities, vegetation and general agent-based frameworks."),
]

STATUS = {"dormant": "dormant", "abandoned": "abandoned", "unknown": "status unknown"}


def anchor(title):
    return re.sub(r"[^a-z0-9 -]", "", title.lower()).replace(" ", "-")


def paper_link(ref):
    """The first DOI in the field, else the first PubMed ID; parentheses are escaped for Markdown."""
    ref = ref or ""
    doi = re.search(r"10\.\d{4,9}/\S+", ref)
    if doi:
        return "https://doi.org/" + doi.group(0).rstrip(".;,").replace("(", "%28").replace(")", "%29")
    pmid = re.search(r"\b\d{6,9}\b", ref)
    return f"https://pubmed.ncbi.nlm.nih.gov/{pmid.group(0)}/" if pmid else None


def entry(t):
    name = t["name"].replace("[", "(").replace("]", ")")
    head = f"[{name}]({t['url']})" if t.get("url") else name
    desc = (t.get("what_it_simulates") or "").strip().rstrip(".") + "."
    meta = []
    if t.get("language"):
        meta.append(f"`{t['language']}`")
    lic = (t.get("license") or "").strip()
    if lic and lic.lower() not in ("none-found", "none declared"):
        meta.append(lic)
    if t.get("stars"):
        meta.append(f"★ {t['stars']:,}")
    if t.get("archived"):
        meta.append("archived")
    elif t.get("maintenance") in STATUS:
        meta.append(STATUS[t["maintenance"]])
    paper = paper_link(t.get("pmid_or_doi"))
    if paper:
        meta.append(f"[paper]({paper})")
    if t.get("guide"):
        meta.append(f"[guide]({GUIDES}{t['guide']})")
    return f"- {head} - {desc}" + (" " + " · ".join(meta) + "." if meta else "")


def main():
    data = json.loads((ROOT / "data/simulators.json").read_text())
    by = {}
    for t in data:
        by.setdefault(t["domain"], []).append(t)
    unknown = set(by) - {k for k, _, _ in SECTIONS}
    if unknown:
        raise SystemExit(f"domains without a section: {sorted(unknown)}")

    guides = sum(1 for t in data if t.get("guide"))
    out = [
        "# Awesome Biological Simulation [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)",
        "",
        "> Software that simulates living systems, from molecules to ecosystems.",
        "",
        f"{len(data)} simulators in {len(SECTIONS)} fields. Each entry gives what the tool simulates, its language, "
        "licence, GitHub stars, maintenance status and, where known, the paper to cite. "
        f"{guides} entries link to a written guide on [biosimhub](https://biosimhub.pages.dev), "
        "most of them with a container recipe whose example has been run.",
        "",
        "Status: entries are maintained unless marked *dormant* (no activity for a year or more), "
        "*abandoned* (stated as unmaintained, or no activity for several years), *archived* (read-only repository) "
        "or *status unknown* (no public repository to check).",
        "",
        "## Contents",
        "",
    ]
    for key, title, _ in SECTIONS:
        out.append(f"- [{title}](#{anchor(title)})")
    out += ["", ""]
    for key, title, blurb in SECTIONS:
        items = sorted(by.get(key, []), key=lambda t: t["name"].lower())
        out += [f"## {title}", "", f"{blurb} {len(items)} entries.", ""]
        out += [entry(t) for t in items]
        out += [""]
    out += [
        "## Contributing",
        "",
        "Additions and corrections are welcome. Read the [contribution guidelines](CONTRIBUTING.md) first.",
        "",
    ]
    (ROOT / "README.md").write_text("\n".join(out))
    print(f"README.md: {len(data)} entries, {guides} with guides")


if __name__ == "__main__":
    main()
