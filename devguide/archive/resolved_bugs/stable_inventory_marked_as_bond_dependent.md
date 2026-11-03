---
summary: Bond-requirement metadata marks stable inventory as connectivity-dependent.
issue: uibcdf/molsysmt#534
status: resolved
opened: 2026-11-03
closed: 2026-11-03
severity: medium
verification: reproduced
area: [attribute, basic]
guard: tests/attribute/test_bond_requirements.py
normative:
blocked_by: []
supersedes: []
---

# Stable inventory and bond-requirement metadata disagree

**Reported:** MolSysViewer's provider-owned metadata facade under
uibcdf/molsysviewer#264 and uibcdf/molsysmt#421.
**Status:** correction, local combined qualification and hosted native/addon
receiving completed; overall candidate qualification remains separate.

## What

On source 27c6bd3c0b4adfc1b7c3b635b9f30bcf6ffa0cab, pure Topology reads
`molecule_index`, `molecule_id` and `entity_index` from atoms, and `atom_index`
from molecules. The public `bonds_are_required_to_get_attribute` helper returns
True for all four, despite the absence of a chemical facade and the stable
inventory classification.

## How

`molsysmt/attribute/bonds_are_required_to_get_attribute.py` lists stable molecule,
entity and some chain attributes alongside chemical fields. Its source-element
list also treats every molecule/entity query as bond-dependent. The helper is
used in planning and foreign-form selection; actual failures in each consumer
have not been established by this metadata reproduction.

## Why

Provider metadata must distinguish stored stable membership from state-local
components/connectivity. A consumer must not infer a chemical prerequisite or
restore Topology chemical storage to compensate for an inaccurate declaration.

## Acceptance and boundaries

Review the distinction between reading stored fields and constructing missing
inventory in a foreign conversion. Cover all stable element axes with independent
expected requirements, plus bonds/components and the source-element axis.
Exercise pure Topology, absent chemistry and zero-state chemistry and affected
get/selection planning. Preserve genuine graph prerequisites. Do not change a
static list without checking the callers' inference contract or equate stable
molecules with chemical components.

## Correction and contract qualification — 2026-11-03

Only state-local component and bond fields/source elements retain the bond
prerequisite. Stable molecule/entity fields, chain type and stored molecule-type
counts no longer request graph reconstruction. The public signature and ArgDigest
boundary stay unchanged; a new docstring explicitly distinguishes stored-data
queries from missing-inventory reconstruction in a foreign conversion.

The independent 320-case matrix covers stable and graph attributes across all
stable source axes, projections from bond/component axes, and real public get/
selection calls on pure Topology, chemistry-absent MolSys and zero-state MolSys.
On the original metadata it produces **109 failures / 211 passes**, exit 1;
after correction all **320 pass**, exit 0. An initial fixture used the unavailable
root `msm.Topology` export; it was corrected to the established native import
before recording the accepted red run. That fixture error is not a product defect.

Four real PDB-text planning tests additionally observe the public get and
selection routes: stable molecule queries request no missing bonds, while bond/
component queries still request their graph. Together with existing attribute
and pipe tests they pass **345 cases**, exit 0, 13.85 s, 21 warnings. An initial
observer patched the basic alias instead of the root converter actually used
by get's planner; its two harness failures are retained, not claimed as product
regressions. Both corrected routing controls execute genuine conversions.

The combined attribute, public get/select, native-domain and ArgDigest selection
passes **1,320 tests**, zero skips/failures, exit 0, 63.67 s, with 32 disclosed
warnings. Both involved public docstrings pass doctests. Foundation, Toolbox,
Cookbook and course module 8 explain the stable/graph distinction. Only narrative
cells change: all notebook code, outputs and execution counts are preserved.
Raw/receptor receipts remain in ignored `.pytest_cache/stabilization-534-535/`.

Final combined receiving, including the completed alias-bootstrap repair, passes
**3,866 tests**, zero skips/failures, exit 0, 203.04 s, with 745 visible warnings.
Canonical receptor evidence is complete and agrees with JUnit. All 14 fast gates,
Ruff lint/format and signature stability against the preceding source pass.
The new attribute and four real planning controls are included in both aligned
routine smoke commands. This does not claim a complete matrix or installed pair.

Published source **13f72af2c9630bf768e03b59e2c973d5c6def4f4** retains these
corrections and controls. [Routine CI 41694657220](https://github.com/uibcdf/molsysmt/actions/runs/41694657220)
is cancelled while its scientific job still has no executed steps, after the
later #503 checkpoint supersedes it. Five administrative workflows pass on that
source; they do not supply the missing scientific execution. No cancelled or
queued result is counted as successful receiving.

Current source **839709e4adeb754adbb5a9eea0a5eb2fa21d795c** retains this exact
metadata repair and guards and adds only #503's detached CIP bibliography.
[Routine CI 41698204284](https://github.com/uibcdf/molsysmt/actions/runs/41698204284)
completes successfully: **4,530 native passes / 16 optional skips** and
**2,449 addon passes / four optional skips**, both exit 0. All new attribute
and public planning guards execute. The skips are unavailable Ackredit (14
native/four addon), unyt (one native) and astropy (one native). The tiers retain
590 and 1,539 warnings. Conda's inventory records Python 3.14.10, NumPy 2.5.4
and Pandas 3.1.0; the bound Viewer is ca7ebea60d530a7a0c65cb4d0ccea7b4288f3352.
GH Run Receptor's final watch exits 0 and agrees with native job 126134233921.

All five applicable source workflows pass: routine smoke 41698204284, devguide
41698204237, Ruff 41698204479, suite policy 41698205147 and publication governance
41698205100. This closes the scoped native ownership defect; it does not qualify
a full matrix, release or installed pair. PR #538 and its new reports remain
separate, unintegrated work.

## Provenance

2026-11-03, Linux, existing Python 3.14.7 development environment. Public native
queries on the bundled pentalanine H5MSM source reproduce all four cases; its
legacy-format warning is expected. No Viewer or consumer-side normalizer is used.
