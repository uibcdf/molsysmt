---
summary: Return ProtOr radii, assigned types and provenance from one evaluation
issue: uibcdf/molsysmt#728
status: open
opened: 2026-11-12
closed:
verification: asserted
area: [physchem]
guard:
normative:
blocked_by: []
supersedes: []
---

# Receiving ProtOr radii and typing together

**Reported:** OpenCASTp consumer request, uibcdf/opencastp#13.
**Status:** source-reviewed proposal; no numerical defect or measured speedup.

## What

Offer an explicit public request returning the selected ProtOr radius quantity,
assigned types and typing provenance from the same evaluation. Preserve the
ordinary radius-only return contract. The consumer currently composes two
supported public operations; that composition remains supported while this
proposal is evaluated.

## How

At source `bdcd326ae`, `get_protor_vdw_radius` in
`molsysmt/physchem/atoms/protor.py` already obtains both types and provenance
from `get_protor_atom_type`, then returns only radii. Requesting the public
atom types separately repeats that selection and typing work. Inspect an
optional return flag on the existing owning operation versus a dedicated
combined public operation before selecting its name/signature. Share the
existing typing calculation; do not add a process-global molecular cache or
make the consumer read private tables.

## Why

OpenCASTp needs aligned radii, types and provenance for reproducible molecular
preparation. Returning existing intermediate results can avoid duplicate work
while keeping scientific ownership in MolSysMT. This is a source-supported
opportunity, not an established performance result or a new radius model.

## Scope and work order

Admit a bounded API/compatibility study into the pre-1.0 polishing queue after
the active native-form documentation increment. It is not a correctness blocker
for 1.0. Retain selection, syntax, units, fallback and typing semantics; do not
expand this request into new chemistry or alter #470/#471 selector contracts.
A public change needs ArgDigest validation, applicable attribution, documentation
and course review, focused guards and a consumer handoff before completion.

## Acceptance criteria

- Match separate public radii/types/provenance calls for ordinary, empty,
  repeated/reordered and explicit/string selections with declared syntax.
- Preserve protein rules and aliases, implicit-H/connectivity behavior,
  fallback evidence, rejection cases, source nonmutation and nondefault
  PyUnitWizard units. Keep selected rows aligned across every returned field.
- Prove one typing evaluation for a combined request and compare against known
  independent typing/radius examples, not only implementation self-parity.
- Measure representative complete molecular preparation and retained memory
  under bounded resources before advertising a saving; array-only consumer
  benchmarks do not measure this dependency path.
- Deliver the supported API/version to OpenCASTp; its numerical array core
  remains independent of molecular preparation.

## Measured and unverified

The provider call/discard path is inspected in source. No timing, memory gain,
combined implementation, consumer acceptance or scientific-model change is
claimed. API naming and combined-result shape remain to be reviewed.
