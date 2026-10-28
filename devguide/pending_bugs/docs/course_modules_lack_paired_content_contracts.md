---
summary: Course modules lack paired content-protection contracts.
issue: uibcdf/molsysmt#512
status: open
opened: 2026-10-27
closed:
severity: low
verification: measured
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Course modules lack paired content-protection contracts

**Reported:** 2026-10-27 while inspecting course instructions for the heading
normalization under uibcdf/molsysmt#144.
**Status:** pre-existing, nonblocking authoring debt; schedule after 1.0.

## What

The course guide requires each module to have a paired, module-specific
content-protection contract. Only 38 of 156 manifested modules have one under
either accepted filename convention. The other 118 inherit general guidance
but lack their specific frozen-content rules.

## How

Run from the repository root:

```python
from collections import Counter
from pathlib import Path
import yaml

course = Path("docs/content/course")
modules = yaml.safe_load((course / "course_manifest.yml").read_text())
missing = []
for module in modules:
    path = course / module["path"]
    contracts = [path.with_suffix(".AGENTS.md"), path.with_name(path.name + ".AGENTS.md")]
    if not any(contract.is_file() for contract in contracts):
        missing.append(module["path"])
print(len(modules), len(modules) - len(missing), len(missing))
print(dict(Counter(path.split("/")[0] for path in missing)))
```

Observed output: `156 38 118`. Missing contracts by path:

| Path | Missing |
| --- | ---: |
| Alzheimer | 29 |
| Enzyme | 29 |
| Antiviral | 30 |
| Biophysics | 30 |
| Common Core | 0 |

## Why

Future editorial work needs to know which scientific scenarios, index/unit
semantics, source ownership, examples, results and stable references must
survive. Generic formatting instructions cannot supply those decisions.
This finding does not demonstrate incorrect calculations or invalidate the
existing course content. The heading-only work preserves all original code,
outputs and other notebook payloads independently.

## What is measured and what is assumed

The manifest population, filenames and file existence are inspected directly
on source 8965569998ad20674924e2e6e3d81b3159ae89ff. The heading normalization
creates or removes no course modules or companion contracts. This is not an
assessment that each existing contract is pedagogically complete.

## What was refuted

- A generic or empty template for each missing filename would satisfy a
  presence check without providing its required protection.
- Copying another path's biological constraints could give incorrect guidance.
- Reformatting headings does not require redesigning the scientific lessons.

## Scope and exclusions

Review modules in bounded groups and write substantive contracts for their
actual content. Preserve existing notebooks and scientific scope. This work
does not add examples, certify old calculations, re-execute the course or
block the documentation-warning repairs under uibcdf/molsysmt#144.

## Acceptance criteria

- All manifested modules have an addressable paired contract.
- Reviewed contracts name actual module-specific invariants and useful
  protection decisions; a file containing boilerplate alone does not qualify.
- Existing valid contracts retain their protection rules.
- A maintained guard checks coverage, with explicit content review alongside
  the mechanical check. Record that guard and the review evidence at closure.

## Provenance

Linux, Python 3.14 development environment, 2026-10-27; filesystem/manifest
inspection only. No molecular calculations or external services are involved.
