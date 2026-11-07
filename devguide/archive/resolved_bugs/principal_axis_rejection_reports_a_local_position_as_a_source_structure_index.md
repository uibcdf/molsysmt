---
summary: Principal-axis rejection reports a local position as a source structure index
issue: uibcdf/molsysmt#640
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: low
verification: measured
area: [diagnostics, structure]
guard: tests/structure/align_principal_axes/test_rejection_indices.py::test_degenerate_moments_name_source_index_and_selected_position
normative:
blocked_by: []
supersedes: []
---

# Principal-axis rejection reports a local position as a source structure index

## What

`structure.align_principal_axes` labels a local position in the selected structure array as a molecular structure number. With requested structures `[2, 0]` and degenerate moments only in source structure 0, the error says that structure 1 is degenerate. Structure 1 was not evaluated.

## How

Owner Geometry/principal-axis receiving uses bundled pentalanine, three structures, moving atoms 0–7 and `structure_indices=[2, 0]`. Set only source structure 0's selected atoms collinear. Native validation rejects before writes, but its reason says `structure 1 has degenerate principal moments`. The loop enumerates the returned moments rather than reporting the source axis or explicitly naming a local selection position.

## Why

A user may inspect or repair the wrong structure. Numerical rejection, molecular coordinates, revision and coverage remain correct; this is an index-space diagnostic defect. The GUI must preserve the native reason rather than translate it. Report the actual source structure index, or explicitly label the selected-array position and its mapping. Cover nonconsecutive/reordered, repeated and all-structure native scopes. Preserve all-structure rejection before coordinate publication.

Related consumer: uibcdf/molsysviewer#315, provider work uibcdf/molsysmt#421.

## Evidence and acceptance

Observed on the native source retained in owner `aadefc11d`, during the new principal-axis GUI guard. The directed run's degenerate case and final combined 5,569-case run preserve coordinates/revisions; they expose the misleading native reason. Source location: `molsysmt/structure/align_principal_axes.py`, the loop over `moments`. No detector, eigensolver or GUI workaround is requested. A new regression should independently put the defective geometry in source structure 0, request `[2,0]`, and check that the reason identifies the correct index space.

## Resolution — 2026-11-07

The degeneracy loop now distinguishes the selected-array position from the
molecular system's structure index. It maps the already validated requested
indices only on rejection, and includes both spaces in the native reason:
`structure_index 0 (selection position 1)` for requested `[2, 0]`. The `all`
case uses its canonical position. Structure IDs remain labels. No extra
coordinate read, trajectory-sized index array or geometry computation is added.
ArgDigest/public getter validation still rejects negative/out-of-range indices;
no Python-negative-index convention is introduced.

The guard executes native `Structures` and `MolSys`, inertia and geometric
moments, independent/in-place requests and reordered, repeated, scalar and `all`
scopes against explicit anisotropic/collinear coordinates. All 48 cases inspect
the structured error reason and prove unchanged coordinates/IDs; MolSys also
retains the existing analysis's evaluated coverage. Two further tests preserve
invalid-index rejection. The bound Geometry consumer checks the exact native
source/selection mapping without a message translation.

The [combined receiving receipt](../../../devtools/data/native_structure_diagnostics_receiving_640_641_20261107.json)
retains the exact baseline, commands, source fingerprints and failed authoring
attempts. The final original-source fixture has **60 failing diagnostic cases
and two passing invalid-index controls**. Corrected receiving passes **701
integrated cases** (including all 62 new cases), one function doctest and two
actual Jupyter scenarios: principal axes (eight steps) and shared rejected-error
lifetime (five steps). The Python panel guard checks the new index-specific
reason; the browser scenarios receive geometry and shared error propagation,
not a separate new browser index-error oracle. Registered source/configuration
inputs remain unchanged within each campaign. Page-error fingerprints match
plain-Jupyter controls; the original #615 observation is not causally resolved.
HTML compilation passes with six retained title-underline warnings.

Initial test fixtures incorrectly assumed root native-class aliases, constructor
keywords and a missing required interaction method; one initially proposed
negative-index case conflicted with the supported index contract. Those attempts
are retained separately from the corrected original-source reproduction. Runtime
APIs, numerical criteria and assertions were not relaxed to accommodate them.

Native moments, tensors, CPU/Rust backend, physical units and all-structure
preflight remain unchanged. No new dependency, scientific algorithm or attribution
event. Public source/issue closeout and clean exact-source scientific execution
retain separate delivery evidence under #334. Installed/platform/human/final-
candidate acceptance remains independently pending.
