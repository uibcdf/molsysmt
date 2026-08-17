---
summary: Remove msm.structure.show_contacts public function
issue: uibcdf/molsysmt#168
status: open
opened: 2026-08-17
closed:
verification: asserted
area: [structure]
guard:
normative:
blocked_by: []
supersedes: []
---

# Remove `msm.structure.show_contacts` public function

**Reported:** 2026-08-17 during documentation audit and tool surface standardization.
**Status:** open

## What

The public function `molsysmt.structure.show_contacts` is redundant with `molsysmt.structure.get_contacts` and standard plotting / visualization workflows. MolSysMT cleanly separates data querying and computation (`get_*`) from visualization rendering. Having a specialized graphical shortcut `show_contacts` on the core structural calculation surface bloats the API and duplicates functionality readily provided by `get_contacts` together with standard plotting libraries (`matplotlib`, `seaborn`) or contact viewers.

## How

1. Deprecate and remove `molsysmt.structure.show_contacts` from `molsysmt/structure/show_contacts.py` and `molsysmt/structure/__init__.py`.
2. Remove references from `molsysmt/api_structure.py` and API autosummary tables.
3. Remove user documentation unit `docs/content/user/tools/structure/show_contacts.ipynb`.

## Why

MolSysMT architectural invariants prioritize orthogonal, composable tools:
- `molsysmt.structure.get_contacts` provides full mathematical contact queries across all supported forms, selections, thresholds, and output formats (`matrix`, `pairs`, etc.).
- Plotting contact maps belongs to user scripting (e.g. `plt.imshow(contacts)`) or dedicated visualization wrappers, keeping `molsysmt.structure` strictly focused on structural computation.

## What is measured and what is assumed

- **Measured:** `get_contacts.ipynb` already includes complete 2D heatmap demonstrations with `matplotlib.pyplot.imshow`.
- **Assumed:** Removing `show_contacts` simplifies the public API surface without loss of scientific functionality.

## What was refuted

- Retaining `show_contacts` as an alias or convenience function was considered, but keeping graphical rendering wrappers mixed with numerical structural calculators creates architectural inconsistency across the `tools/structure` subportal.

## Scope and exclusions

- **Covers:** Deprecation and eventual removal of `msm.structure.show_contacts` and its user guide tutorial page.
- **Excludes:** `molsysmt.structure.get_contacts`, which remains the canonical, fully supported contact computation engine.

## Acceptance criteria

- `show_contacts.ipynb` removed from documentation toctrees and file system.
- `msm.structure.show_contacts` deprecated/removed in codebase.
- API validation and release gate pass cleanly.
