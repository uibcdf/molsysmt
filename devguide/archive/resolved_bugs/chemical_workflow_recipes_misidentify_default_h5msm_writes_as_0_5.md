---
summary: Chemical-workflow recipes misidentify default H5MSM writes as 0.5
issue: uibcdf/molsysmt#772
status: resolved
opened: 2026-11-17
closed: 2026-11-17
severity: low
verification: reproduced
area: [docs]
guard: tests/documentation/test_chemical_workflow_recipes.py
normative:
blocked_by: []
supersedes: []
---

# Default and explicit compatibility writes in chemical recipes

**Reported:** 2026-11-17, #334 B1 literal-example receiving.
**Status:** resolved; examples and actual persisted headers received.

## What

The export-order and metadata Cookbook examples use the default public H5MSM
writer while stating that their actual file is 0.5. The metadata example even
prints that assertion after reading the new file. Native file headers are 1.0.
Public writing works; the explanation confuses default output and compatibility.

The first literal-recipe cohort passes six cases and fails the two format-profile
checks. The guard reads actual completed HDF5 root headers before the recipes
retire their temporary files; it does not infer format from a filename, printout
or conversion keyword.

## How

Explain the default 1.0 path accurately and retain the locally protected 0.5
round trip as a separate, explicitly requested compatibility example. Read both
files through the public API and assert the same molecular correspondence,
string labels and squared-length B factors. Preserve other examples, anchors, warnings and the 0.5 mechanics limitation.
The prepared-PDBQT recipe also gains an actual default-1.0 parameter round trip;
its read-versus-write MODEL scope is clarified. No runtime writer changes.

## Why

Readers should know which schema they wrote and distinguish current persistence
from an explicit older projection. This corrects bounded instructional accuracy,
not chemical interpretation or a format regression.

## Evidence and acceptance

`tests/documentation/test_chemical_workflow_recipes.py` executes the source
fences/cells. Independent assertions preserve reverse/inverse coordinate axes,
`['101', '00101']` labels and repeated/empty structure B-factor queries; the
completed files must actually cover default 1.0 and explicit 0.5. Notebook
execution, strict HTML and final checks follow the correction. Source evidence
uses Linux/Python 3.14.7 and the existing received support composition, under
bounded resources. It is not installed-client or release-pair qualification.

A single observed terminal-reconstruction attribute-drop warning belongs to the
unrelated successful recipe control and is retained, not suppressed to pass.

## Resolution — 2026-11-17

The export-order and metadata recipes now identify the default as H5MSM 1.0
and execute a separate explicit 0.5 compatibility round trip. The prepared-PDBQT
recipe shows default persistence of supplied parameter columns while keeping
partial chemistry and the external torsion tree explicit. Its MODEL reader and
single-structure writer limits no longer appear contradictory.

The original literal cohort records six passes and two failures; corrected and
final examples pass all eight cases, including nm/ps and pm/fs prepared inputs.
The metadata notebook executes its four code cells with string-ID and squared-unit
assertions. The guard reads actual file headers before temporary retirement;
changing a printed version alone cannot satisfy it. Expected molecular values,
source maps, units and source bytes remain independently asserted.

Strict full/incremental HTML, final local article/link/asset receiving and offline
static reader views pass. The existing template control's attribute-drop warning
remains visible. No runtime format writer, preparation method, source chemistry
or final release gate is changed.

[Supplemental receiving](../../../devtools/data/supplemental_pre1_work_334_20261117.json)
retains original failures, source/execution/rendering identities and limits.
