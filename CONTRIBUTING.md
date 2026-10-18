# Contributing

Entries live in `data/simulators.json`. `README.md` is generated from it, so edit the data file and run:

```sh
python3 scripts/build_readme.py
```

Commit both files in the same pull request.

## What belongs here

- Software that simulates a biological system: molecules, cells, tissues, organs, organisms, populations, epidemics or ecosystems.
- Released code or a downloadable program. A paper without code does not qualify.
- One entry per tool. A tool that spans two fields goes in the one its users most often come from.

## Fields

| Field | Content |
|---|---|
| `name` | The tool's own name and capitalisation. |
| `url` | Repository or home page. |
| `what_it_simulates` | One sentence, starting with a capital letter, on what the tool models. No marketing words. |
| `domain` | One of the section keys in `scripts/build_readme.py`. |
| `language`, `license` | As stated by the project; licence as an SPDX identifier where possible. |
| `maintenance` | `active`, `maintained`, `dormant` (no activity for a year or more), `abandoned` or `unknown`. |
| `archived` | `true` for a read-only repository. |
| `stars` | GitHub stars when added; refreshed occasionally. |
| `pmid_or_doi` | The paper to cite: a DOI (`10.…`) or a PubMed ID. |
| `guide` | A biosimhub guide id, or `null`. |

## Corrections

A wrong licence, a dead link or a project that changed status: open an issue or a pull request with the source that shows the change.
