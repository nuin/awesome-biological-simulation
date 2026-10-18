#!/usr/bin/env python3
"""Copy the biosimhub guides into guides/ as GitHub Markdown.

    python3 scripts/import_guides.py ~/Projects/biosimhub

Reads <biosimhub>/guides/<id>.md and <biosimhub>/src/lib/generated/guides.json
(run `node scripts/sync.mjs` there first). Each guide gets a header with the
licence, source and citation, and, for tools with a container recipe, the tested
example: the download link, run.sh, the expected output files and the parameters.
Links between guides become relative links. Writes guides/README.md as an index.
"""
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SITE = "https://biosimhub.pages.dev"


def size(n):
    for unit in ("B", "KB", "MB", "GB"):
        if n < 1024 or unit == "GB":
            return f"{n:.0f} {unit}" if unit == "B" else f"{n:.1f} {unit}"
        n /= 1024


def cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def example(s):
    out = ["## Run the tested example", ""]
    line = f"This recipe builds {s['title']} in a container and runs the example below. It needs [Docker](https://docs.docker.com/get-docker/) and nothing else."
    if s.get("expected"):
        line += f" It last ran on {s['expected']['captured']} in {s['expected']['seconds']} s."
    else:
        line += " It follows the project's documentation and has not been run yet."
    if s.get("emulated"):
        line += f" {s['title']} has no ARM build, so on Apple silicon Docker runs the x86 image under emulation, which is slower."
    files = ", ".join(s["files"])
    if s["examples"]:
        files += ", example " + ", ".join(e["name"] for e in s["examples"])
    out += [line, "",
            f"1. Download [{s['id']}-recipe.tar.gz]({SITE}{s['archive']}) ({files}, run.sh).",
            "2. Unpack it and run the script:", "",
            "   ```sh", f"   tar -xzf {s['id']}-recipe.tar.gz", f"   cd {s['id']}", "   sh run.sh", "   ```", ""]
    if s.get("run"):
        out += ["<details><summary>What run.sh does</summary>", "", "```sh", s["run"], "```", "",
                "Inputs are read from `in/` and results land in `out/`. Change the values after each option to run your own case; the parameter table lists them.",
                "", "</details>", ""]
    e = s.get("expected")
    if e:
        out += ["### Expected output", "", "| File | Size |", "|---|---:|"]
        out += [f"| `{cell(f['file'])}` | {size(f['bytes'])} |" for f in e["files"]]
        out += [""]
        for f in e["files"]:
            if f.get("head"):
                out += [f"<details><summary>First lines of <code>{f['file']}</code></summary>", "", "```",
                        f["head"], "```", "", "</details>", ""]
    if s["params"]:
        out += ["### Parameters", "", "| Option | Meaning | Example value | Range |", "|---|---|---|---|"]
        for p in s["params"]:
            if p["type"] == "enum":
                rng = ", ".join(p["choices"])
            elif p.get("min") is not None or p.get("max") is not None:
                rng = f"{p.get('min') if p.get('min') is not None else ''} to {p.get('max') if p.get('max') is not None else ''}"
            else:
                rng = p["type"]
            meaning = p["label"] + (f" ({p['help']})" if p.get("help") else "")
            default = p["default"] if p.get("default") is not None else "not set"
            out.append(f"| `{cell(p.get('option') or p['name'])}` | {cell(meaning)} | {cell(default)} | {cell(rng)} |")
        out += ["", "Ranges are the limits used for the example recipe; the program itself may accept more.", ""]
    return "\n".join(out)


def convert(g, body):
    body = re.sub(r"^---\n.*?\n---\n?", "", body, flags=re.S)
    body = re.sub(r"\]\(/guide/([a-z0-9-]+)\)", r"](\1.md)", body)
    body = re.sub(r"\]\(/(?!/)", f"]({SITE}/", body)
    head = [f"# {g['title']}", "", f"> {g['summary']}", ""]
    meta = []
    if g.get("license"):
        meta.append(f"Licence: {g['license']}")
    if g.get("source"):
        meta.append(f"[Source code]({g['source']})")
    if meta:
        head += [" · ".join(meta), ""]
    if g.get("plugin"):
        p = g["plugin"]
        head += [f"**[Run {p['title']} in your browser]({SITE}{p['href']})**: {p['summary']} "
                 f"Nothing to install; the first visit downloads about {round(p['download_kb'] / 1024)} MB.", ""]
    ex = example(g["server"]) if g.get("server") else ""
    if "<!-- example -->" in body:
        body = body.replace("<!-- example -->", ex, 1)
    elif ex:
        body = body.rstrip() + "\n\n" + ex
    tail = ["", "---", ""]
    if g.get("citation"):
        tail += [f"Cite: {g['citation']}", ""]
    tail += [f"This guide is also on [biosimhub]({SITE}/guide/{g['id']}).", ""]
    return "\n".join(head) + "\n" + body.lstrip("\n").rstrip() + "\n" + "\n".join(tail)


def main():
    hub = Path(sys.argv[1]).expanduser()
    guides = json.loads((hub / "src/lib/generated/guides.json").read_text())
    dest = ROOT / "guides"
    shutil.rmtree(dest, ignore_errors=True)
    dest.mkdir()
    for g in guides:
        src = hub / "guides" / f"{g['id']}.md"
        (dest / f"{g['id']}.md").write_text(convert(g, src.read_text()))
    index = ["# Guides", "",
             f"Written guides for {len(guides)} simulators, from [biosimhub]({SITE}). "
             "Most include a container recipe whose example has been run, with its expected output.", ""]
    for g in sorted(guides, key=lambda g: g["title"].lower()):
        index.append(f"- [{g['title']}]({g['id']}.md) - {g['summary'].rstrip('.')}.")
    (dest / "README.md").write_text("\n".join(index) + "\n")
    print(f"guides/: {len(guides)} guides")


if __name__ == "__main__":
    main()
