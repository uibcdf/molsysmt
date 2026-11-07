---
summary: Structural inconsistency hints assume comparisons and retain obsolete axis terminology
issue: uibcdf/molsysmt#641
status: open
opened: 2026-11-07
closed:
severity: low
verification: reproduced
area: [diagnostics]
guard:
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
