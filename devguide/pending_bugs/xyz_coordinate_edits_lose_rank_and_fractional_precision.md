---
summary: XYZ coordinate edits lose supported ranks and fractional precision.
issue: uibcdf/molsysmt#638
status: open
opened: 2026-11-07
closed:
severity: high
verification: reproduced
area: [structure, form, coordinates, units]
guard:
normative:
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
