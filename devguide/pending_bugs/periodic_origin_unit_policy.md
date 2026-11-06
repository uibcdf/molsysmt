---
summary: Near-zero periodic origins are snapped using application-dependent units.
issue: uibcdf/molsysmt#608
status: open
opened: 2026-11-06
closed:
severity: high
verification: reproduced
area: [pbc, units, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# Near-zero periodic origins and application units

## What

The native atomwise primary wrapping path replaces a near-zero origin using
`np.isclose(..., atol=1e-4)` on standardized numeric values. The physical
threshold changes with the application's length standard, so the same molecular
system and explicit quantity can produce different primary-cell images.

## How

Native ed09f6453, Python 3.14, no Viewer: a selected atom at [0,0,0] nm in a
3/4/5-nm orthogonal cell, with explicit origin [1e-5,0,0] nm and compact=False,
returns [0,0,0] nm under nm/angstrom standards and [3,0,0] nm under pm.
The primary cell starts at x=1e-5 nm, so x=0 is outside that requested cell.
The latter image is consistent with the origin. Reproduction retained in
`/tmp/msv-periodic-origin-policy-probe-20261106.log`.

## Why and acceptance

Preserve explicit reference points without an application-unit-dependent
replacement. Qualify exact zero, small positive/negative origins, boundary atoms,
input quantity units, nm/angstrom/pm policies, grouping, structure scope and
independent/in-place effects. Review related centered/MIC branches without
assuming they share the same failure. Do not mask image differences by a loose
coordinate tolerance or add a consumer-side origin formula/standard override.

This finding keeps general reference-point and periodic release qualification
pending under #421 / PR #543 and uibcdf/molsysviewer#264. The prepared GUI's
passing lattice cases cover their explicit tested origins, not this failed
boundary case. Native correction and exact consumer receiving remain required;
no scientific workaround is implemented in the addon.
