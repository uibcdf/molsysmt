---
summary: Feature results share mutable reference metadata across calculations.
issue: uibcdf/molsysmt#490
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [physchem, metadata, attribution]
guard:
normative:
blocked_by: []
supersedes: []
---

# Shared result references contaminate later method metadata

**Reported:** 2026-10-26 during final expert addon feature-reader receiving.
**Status:** open; numeric recognition succeeds, mutable result metadata aliases
shared declarations.

## What

The plain `method_reference` dictionaries returned by hydrophobic and halogen site readers share mutable global ProLIF metadata. Editing a completed result changes reference metadata in later calculations, including the other reader. Numeric recognition results need not change for their provenance to become contaminated.

## How

```python
import molsysmt as msm
from rdkit import Chem

first = msm.physchem.get_hydrophobic_sites(Chem.MolFromSmiles('CCC'))
assert first['method_reference']['version'] == '2.2.2'
first['method_reference']['version'] = 'user-edited'
second = msm.physchem.get_halogen_bond_sites(Chem.MolFromSmiles('CCl.C=O'))
assert second['method_reference'] is first['method_reference']
print(second['method_reference']['version'])  # user-edited, expected original 2.2.2
```

Run in a fresh short-lived process: this intentionally mutates the returned dictionary. Both readers assign `method_reference=PROLIF_REFERENCE`; `_private/interaction_attribution.py` creates detached bibliography items but returns this original reference object inside the result. Reproduced without Viewer at source 02671792f3b90de654b467683a8d394118dc4ccb (and its documentation-only successor), Linux/Python 3.14.7, RDKit 2025.9.5. No source file or primary molecular-system edit is necessary.

## Why

The expert addon under #421 / uibcdf/molsysviewer#264 must retain native scientific results and provenance without introducing consumer-specific repairs. Completed reports must not become a route to changing global method declarations or unrelated future calculations. This is independent of the reference-selection repair in #488.

## Acceptance criteria

Return independently owned result-level reference metadata while preserving existing plain-dictionary fields, values, roles and serialization. Add native pytest guards that mutate `method_reference` in one result and confirm an earlier result, a later same-reader result and a different-reader result retain canonical values. Check positive and evaluated-empty recognition outputs and distinguish `method_reference` from already detached attribution items. Audit other consumers of the shared constant where applicable; do not presume every detector has the same alias without a reproduction. Keep numeric results, source axes, units and scientific parameters unchanged. Detach the small metadata at its owning boundary; avoid copying entire systems, trajectories or large occurrence buffers.

Record: `devguide/pending_bugs/shared_method_reference_metadata.md`. This report does not introduce a Viewer workaround or promise broader scientific/model validation.


## What is measured and what is assumed

The hydrophobic and halogen dictionaries share the same Python reference object;
mutating the version in one result propagates to both later readers in a fresh
process. Recognition populations are not changed by this reproduction. Other
feature/detector families may have independent ownership behavior and need an
actual audit rather than a blanket conclusion.

## What was refuted

No Viewer object, scene, managed edit, primary mutation or selection conversion
participates. The detached attribution item list is a distinct object from the
aliased method_reference declaration; copying that bibliography alone does not
remove this route to changing later provenance.

## Scope and exclusions

The fix belongs at the provider's small metadata ownership boundary. No wrapper
copy, selector change, new scientific model or whole-system copying. The
scientific algorithm, units, source indices and primary remain unchanged.

## Provenance

Linux/Python 3.14.7, RDKit 2025.9.5, native source 02671792f and documentation-only
successor 87d7b9d09. Short-lived isolated process; the intentional mutation does
not persist in the user's Python session or alter source files. Original
ProLIF version 2.2.2 becomes user-edited metadata in both subsequent calls.
