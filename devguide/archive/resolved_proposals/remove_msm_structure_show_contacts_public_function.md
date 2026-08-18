---
summary: Remove msm.structure.show_contacts public function
issue: uibcdf/molsysmt#168
status: resolved
opened: 2026-08-17
closed: 2026-08-18
verification: reproduced
area: [structure]
guard:
normative: devguide/api_stability_registry.md
blocked_by: []
supersedes: []
---

# Remove `msm.structure.show_contacts` public function

**Reported:** 2026-08-17 during documentation audit and tool surface standardization.
**Status:** resolved 2026-08-18 in `e7f2e8ce9`.

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

## Resolution — 2026-08-18

Removed in `e7f2e8ce9`. The registry drops from 190 to 189 symbols.

Removed with the function: `argument/style.py`, which validated one value against
the single caller `molsysmt.structure.show_contacts.show_contacts` and would have
raised for every input once that caller was gone, and `argument/show.py`, which had
no other user. `show_contacts` also left the `threshold` digester's caller list and
the API reference autosummary.

Two things this proposal got wrong, recorded because they cost time:

**It named a file that does not exist.** Step 2 asks to clean
`molsysmt/api_structure.py`; there is no such path in the repository.

**It missed the course.** The proposal scopes the removal to the code and one User
Guide page, but Module 32, "Visualizing Interaction Matrices", is built on
`show_contacts` in all four Paths, with six call sites. `course_manifest.yml` pins
each module's id, display number and title, so the modules could not be deleted —
they were rewritten onto `get_contacts` + Matplotlib, reproducing what
`show_contacts` did internally (`get_contacts`, then `imshow(origin='lower',
interpolation='nearest')`).

Two pre-existing errors in that module were corrected while rewriting it: the
Enzyme and Alzheimer challenges instructed the reader to pass `element='group'`, an
argument `show_contacts` never had and `get_contacts` does not have either, and the
Alzheimer text claimed the function was built on Matplotlib when its default
backend was Plotly.

**How this is guarded.** `devtools/scripts/validate_api_stability.py` rejects any
public export missing from `devtools/data/public_api_stability.json`, so
reintroducing `show_contacts` fails the release gate with `Unclassified public
export` until someone classifies it deliberately. That mechanism was observed
firing on the same day for `molecular_mechanics.get_degrees_of_freedom`, which
reached `main` unclassified and turned the fast gate red at 12/13.

Verified: `validate_course.py` passes (156 notebooks, toctrees, manifest and
labels), fast gates 13/13, full suite 9980 passed / 11 skipped.
