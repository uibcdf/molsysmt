---
summary: Structural inconsistency hints assume comparisons and retain obsolete axis terminology
issue: uibcdf/molsysmt#641
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: low
verification: measured
area: [diagnostics]
guard: tests/cross_repo/test_smonitor_contracts.py::test_structural_inconsistency_keeps_reason_and_conditional_hints
normative:
blocked_by: []
supersedes: []
---

# Structural inconsistency hints assume comparisons and retain obsolete axis terminology

## What

The shared `MSM-ERR-STRUCT-003` hint assumes every structural inconsistency is an atom/count comparison or merge. It also uses generic `residues` and `frames` where MolSysMT uses `groups` and `structures`.

## How

Run `structure.align_principal_axes` with a nonorthonormal target basis or a left-handed basis on bundled pentalanine. The precise native reason is correct, but the user hint instructs the user to ensure atoms, residues or frames match between systems being compared or merged. This single-system target-basis validation is neither a comparison nor a merge. The agent hint similarly asks for atom/frame count matching.

## Why

The generic advice misdirects correction of a legitimate scientific rejection and conflicts with the public vocabulary. Update the shared owning catalogue, keeping the structured reason authoritative and using conditional, broadly applicable advice. Cover both a single-system basis rejection and a real correspondence/count rejection. Preserve the error code, exception type, reason and diagnostic propagation; do not add per-consumer message rewrites.

## Evidence and acceptance

Reproduced during owner principal-axis source receiving; the exact native reasons remain `Target axes must be orthonormal` and `Target axes must form a right-handed basis`. Owning source: `molsysmt/_private/smonitor/catalog.py`, `MSM-ERR-STRUCT-003` user/agent hints. This is a MolSysMT catalogue defect, not a SMonitor rendering defect. Numerical results and rejection atomicity are unaffected.

## Resolution — 2026-11-07

The owning `MSM-ERR-STRUCT-003` templates now direct users to the reported
reason, geometry, dimensions and index correspondence. Advice about selected
atoms, groups and structures is explicitly conditional on comparing or merging
systems. Developer/QA guidance stays general. All four audiences retain the
native reason; QA no longer suppresses it, and agent rendering carries it in
the main message. The code, exception class and structured reason remain intact.
No SMonitor provider modification or consumer-side message rewrite is needed.

The guard triggers real nonorthonormal and left-handed target-basis rejections,
and a real composite with incompatible two-/three-structure axes, under user,
developer, QA and agent profiles. Its twelve cases check the exact native code
and reason, geometry/dimension advice, conditional comparison guidance and the
MolSysMT groups/structures vocabulary. Each test restores the application profile
and catalogue. The developer guide also corrects its stale warning-entry lookup
to the actual nested catalogue and documents native reason propagation.

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
