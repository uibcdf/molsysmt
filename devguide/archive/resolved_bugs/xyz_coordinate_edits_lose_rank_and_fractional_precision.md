---
summary: XYZ coordinate edits lose supported ranks and fractional precision.
issue: uibcdf/molsysmt#638
status: resolved
opened: 2026-11-07
closed: 2026-11-07
severity: high
verification: reproduced
area: [structure, form, coordinates, units]
guard: tests/structure/test_xyz_edit_representation.py
normative: devguide/forms_and_conversions.md
blocked_by: []
supersedes: []
---

# XYZ coordinate edit representation

## What

Public rotation silently truncates fractional results in accepted integer XYZ
storage. Accepted rank-two floating coordinate quantities fail at publication
because the setter indexes three axes. These are separate from #633's corrected
borrowed-storage mutation; both inspected sources remain unchanged after that fix.

## How

A public 45-degree z rotation of `[[[1, 0, 0]]] nm` with integer dtype returns
`[[[0, 0, 0]]] nm` rather than `[sqrt(0.5), sqrt(0.5), 0] nm`. The output remains
int64 and incorrectly loses the point's radius. A floating `(2, 3)` quantity is
recognized as XYZ but raises `IndexError` when the three-index setter publishes
the result. The source-alias correction does not fix arithmetic/storage dtype or
the source rank. Both controls and source-preservation assertions are retained.

`XYZ.is_form` accepts length quantities of rank one, two and three; coordinate
normalization accepts integer dtypes. Canonical-rank floating/native guards alone
therefore do not cover these other accepted inputs.

## Why

A proper rotation must preserve geometry regardless of an accepted input's
storage representation. A physically fractional result cannot be silently
rounded through integer assignment. The normalized calculation shape and the
target's original shape must have a deliberate publication contract.

## Acceptance and ownership

Review geometry and the XYZ adapter together, reusing existing unit, conversion,
copy and coordinate-publication tools. Compute in floating storage, support the
declared ranks and return a correct independent result. For in-place storage
that cannot represent the result, use a supported unit-owner mutation or reject
before any write with an explicit public contract; do not silently truncate.
Preserve units, quantity-library/form policy, atom/structure maps, readonly and
failure behavior, and normal floating/native cases. Guard independent/in-place
modes, ranks, integer/floating storage and fractional rotations/translations.

This is included-operation data integrity admitted under #334. It remains due
before final geometry qualification; it adds no method, dependency, placeholder
API or progress weight. #602's matrix constructor and #633's 58 canonical-rank
ownership guards retain their narrower verified scopes.

## Owner correction and first receiving — 2026-11-07

The original 156-case public guard has 135 failures and 21 passes on public
PyUnitWizard 0.28.1, exact Viewer 25061d9e9 and existing development Python 3.14.
It confirms rank-one/two assignment, fractional arithmetic/storage and mismatched
quantity-owner assignment under a different application unit policy. The latter
belongs to the same coordinate-publication boundary, not a new detector/method.

Rotation and translation now share private, focused coordinate-edit preparation.
Selected integer magnitudes compute in owned float64; independent integer XYZ
targets also promote to float64 before publication. Floating dtype, original
rank, unit and quantity library remain intact. Complementary native-inventory/
XYZ compositions use the same target preparation. Ordinary public `copy()` still
preserves integer dtype and exact storage; it does not become a transform.

The XYZ setter validates destination-compatible units, safe integer storage and
selected-shape broadcasting before assignment. It publishes through the original
quantity owner at its original rank. Floating or narrowing writes to integer XYZ
raise the existing structured `StructuralInconsistencyError` before any write;
a caller must use floating storage or an independent transform. This deliberate
refusal includes mathematically integral floating results and avoids a hidden
rounding convention. No PyUnitWizard private storage or process policy is changed.

First receiving passes 214 cases without failures/errors/skips: the 156 new
representation/publication cases and all 58 prior ownership guards. An expanded
profile adds a second application policy, composite sources and explicit basic
copy controls; broader geometry/addon/documentation receiving is in progress.
The new tests use signed analytic rotation/translation oracles and unchanged
unselected/source checks. They do not derive expected geometry from the new
publication helper. Original failed outcomes remain retained.

Docstrings, Toolbox, Cookbook, all four Module 46 paths and the maintained form
contract describe promotion and the in-place limit. No public signature, Rust
kernel, dependency floor or scientific profile changes. Source delivery, final
expanded receiving and issue closeout remain due; #636 and #635 keep their
separate acceptance boundaries.

## Expanded receiving and retained preparation errors

The broad geometry/XYZ/addon/documentation campaign has 7,977 passes and two
failures (zero skips/errors; native exit one). Both failures occur in the new
composite fixture before the operation: it mistakenly uses the removed top-level
`molsysmt.MolSys` instead of the maintained `molsysmt.native.MolSys`. Only that
fixture import/construction is corrected. No runtime or expected-geometry
assertion changes after this broad campaign.

The complete expanded representation/ownership selection and public transform
doctests then pass **269 cases** without omissions on actual public ArgDigest
0.14.0 and PyUnitWizard 0.28.1. This includes both composite operations. Do not
relabel the original 7,979-case campaign as an all-pass run or add overlapping
counts. Its unaffected passes and the separately corrected receiving are retained.

The six-notebook execution first fails before kernel startup because the sandbox
forbids Jupyter's local sockets (`PermissionError`). All original per-notebook
logs are copied to that failed campaign. An identical retry uses the existing
interpreter with local sockets permitted, not a new environment or installed
packages. Notebook/code and candidate/graphical acceptance remain separate.

## Resolution — 2026-11-07

The coordinate-owner correction and its guards are complete. All six affected
notebooks execute successfully on the corrected source after granting Jupyter
local sockets; 107 registered scientific cases across 68 nodes pass with an
explicitly dirty, release-ineligible certificate. All fourteen fast source gates
pass. HTML compilation exits zero with the six retained title-underline warnings.
Whole-tree Ruff lint and formatting checks pass.

The [portable receiving receipt](../../../devtools/data/xyz_coordinate_representation_receiving_638_20261107.json)
retains all nine campaigns, source/provider/backend identities, original failures
and separately successful controls. Its 269-case minimum-provider receiving
covers the corrected fixtures; the broad 7,977-pass/two-fixture-failure attempt
is not rewritten as a zero-failure campaign. This resolves accepted XYZ rank,
precision and quantity-owner publication without promoting stability or adding
a method/dependency. Source delivery and board verification are recorded
separately in the release ledger; #636 and newer-host #635 remain open.
