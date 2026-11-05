---
summary: Water-box clipping uses transposed fractional coordinates and omits lower bounds.
issue: uibcdf/molsysmt#564
status: resolved
opened: 2026-11-05
closed: 2026-11-05
severity: high
verification: reproduced
area: [build, pbc, units]
guard: tests/build/make_water_box/test_cell_membership.py
normative:
blocked_by: []
supersedes: []
---

# Preserving water membership in a requested periodic cell

## What

`build.make_water_box` advertises triclinic support but clips oxygen coordinates
using the column-vector transform for a row-vector box and checks only the upper
fractional bounds. Valid input therefore produces out-of-cell oxygen sites.

## How

The supplied box rows are `[[2,0,0], [.7,1.8,0], [.3,.2,1.7]]` nm. On main
27ccb1b6d640b7e2087a86dea06f6e666dc73fe1 the reported 266 waters include 111
outside that cell. The orthogonal `2*eye(3)` control has 268 waters and no outside
sites. Hydrogen sites outside the cell are not the defect: complete O-H-H groups
must remain intact.

For row vectors, `r = f @ B` and `f = r @ inverse(B)`. The old implementation
uses `inverse(B) @ r.T`, and its clipping predicate is only `< 1`. Tests use an
independent linear solve and literal Cartesian points for known fractional
locations, including negative fractional positions with non-negative Cartesian
coordinates, the included origin and all three excluded upper faces.

## Why

Incorrect clipping changes solvent population and geometry. MolSysMT owns the
repair; the expert-addon contribution in #543 and uibcdf/molsysviewer#264 must
not implement a client coordinate workaround.

## Contract and implementation plan

- Admit one finite, nonsingular, length-bearing row-vector box. Reuse existing
  ArgDigest quantity normalization and shared PBC validation before reference
  loading; do not silently choose the first of multiple supplied structures.
- Retain complete reference waters precisely when `0 <= f < 1` on every oxygen
  fractional axis. Do not wrap or distort individual atoms; H may cross a face.
- Preserve template geometry, deterministic tile order, native string labels,
  two O-H bonds per water, and typed `(1, 0, 3)` coordinates if no water fits.
  Keep native coordinates and boxes in canonical nm under a nondefault
  presentation policy without changing that application policy.
- Honor existing `form` through public conversion; it is currently ignored.
  Default native output avoids a redundant copy.
- Describe the bundled SPC-MODEL reference accurately. This operation populates
  inventory/connectivity and coordinates, not charges or a particular force-field
  parameterization. Clipping does not guarantee exact density, equilibration or
  absence of clashes.

The clipping expression is feature-specific linear algebra. Existing PBC
validation, quantity normalization and conversion remain reusable tools; no
speculative public coordinate-conversion package or compiled kernel is needed.
The reference is the existing bundled file; no new third-party scientific method
or attribution-provider boundary is introduced.

## Tests and limitations

Public controls cover positive/negative tilts, a rotated cell, orthogonal
control, literal half-open boundaries, whole-water geometry, bond/group
inventory, equivalent nm/angstrom/pm inputs, canonical storage under an angstrom
policy, invalid/multiple/empty cells, output independence, empty populations
and requested output form.

The first 21-case draft exits 1 with 14 failures and seven passes. Five failures
are test assumptions corrected before implementation: root `msm.Structures` is
not the constructor route used here; native stored units stay nm under an
angstrom presentation policy (three cases); native public arrays are read-only
and must be edited through setters. Corrected controls use the public native
constructor, preserve application policy and use a box setter. The failed draft
is retained, not counted as 14 production defects.

No minimization, water force field, ion-count policy, general packing algorithm,
H5MSM schema, new detector or optional-engine fallback is added.

## Provenance

2026-11-05, existing shared Linux/Python 3.14.7 development environment, NumPy
2.4.6 and Pandas 2.3.3. Pytest Receptor 1.2.1 uses its verified published payload.
Baseline JUnit: `.pytest_cache/water-box-564-before.xml`; corrected baseline:
`.pytest_cache/water-box-564-baseline-corrected.xml`. Source/guard hashes and
final receiving belong in the closing receipt.

## Implementation and observations

The corrected row-vector mask keeps **207 waters with zero out-of-cell oxygen
sites**, while the 2 nm orthogonal control stays at **268**. A scalar oracle
enumerates a deliberately wider source lattice and solves the reported lower-
triangular box analytically; it checks the complete oxygen multiset, including
duplicates, rather than only output bounds. Independent template-vector checks
protect whole-water geometry, and the literal fixture requires three retained
waters with their exact O-H-H coordinates and six bonds.

Wrapping would move invalid candidates rather than implement clipping. Filtering
only the previous output would remove invalid sites but lose valid candidates
that the transposed transform had already excluded. The complete lattice oracle
guards both failure modes. No packing/thermodynamic validation follows from these
geometric controls.

Existing ArgDigest normalization and shared `validate_box_array` check the input
before reference reading. The reference-loader helper remains private to this
factory; analytic tests patch that helper rather than a shared form adapter, so
lazy registry imports cannot retain a test double. Public SMonitor tracing and
catalog errors are used. Optional output conversions retain their existing lazy
DepDigest boundaries. Default output has no new optional dependency.

The intermediate corrected baseline still had one test rank error: direct native
box assignment requires `(1,3,3)`. After correcting the fixture, the unchanged
runtime exits 1 with **10 failures and 11 passes**. The implementation first passes
all 21 controls. Adding the complete-lattice oracle and absent-box guard gives
**23 published-floor passes** and **773 affected passes** across water construction,
PBC and ArgDigest. The published provider payloads are the same four verified
floors used for #568; only the SMonitor pytest entry point is disabled in that
floor run under #524, with runtime diagnostics active.

The native doctest passes, and the complete updated tutorial executes eight code
cells in **7.4 s**. The other edited course/Cookbook material changes prose only;
its executable payload and outputs are preserved. A stale sentence in the touched
Structures page contradicted its own public-setter notification description; the
sentence now agrees with the implemented #285 owner-invalidation boundary.


## Final receiving

All **773 affected controls**, **23 published-floor controls**, **586
documentation/owner-notification controls**, and the native doctest pass. The
complete tutorial executes eight code cells in 7.4 s. The other three edited
notebooks retain identical executable cells, outputs and metadata. Ruff lint
and formatting, dependency/docstring/API-signature checks and course validation
pass. The source signature and dependency floors do not change; no Rust rebuild
is performed. These selections overlap and are not a full installed/platform
or thermodynamic validation matrix.

The [receiving receipt](../../../devtools/data/water_box_receiving_564_20261105.json)
records the failed baseline drafts, corrected baseline, final counts, unit and
geometry conventions, exact source/test identities and remaining limits.

Queue review observes no newer open issue than #576, and PR #543 at
ac1f6dbad9ce3b29751dfd0a33e5df596e5dbae0. The prior 27ccb1b6d smoke run
42114952994 is in progress, not certified successful. Next native triage is
#575's ignored explicit ion counts and #574's label handling; #576 and #572
remain separately owned capability proposals.
