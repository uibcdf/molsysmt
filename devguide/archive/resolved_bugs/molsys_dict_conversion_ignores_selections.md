---
summary: Preserve selections in MolSysDict to MolSys conversion
issue: uibcdf/molsysmt#410
status: resolved
opened: 2026-10-22
closed: 2026-10-22
severity: high
verification: reproduced
area: [convert, extract]
guard: tests/form/molsysmt_MolSysDict/test_selected_conversion.py
normative:
blocked_by: []
supersedes: []
---

# Selected MolSysDict reconstruction

## What

The direct MolSysDict-to-MolSys converter has no axis arguments. Public conversion
and extraction therefore ignore their atom/structure selections on that route.
The #406 synthetic removal case retains four atoms when three were requested.

## How

Add keyword-only `atom_indices` and `structure_indices`, retaining the existing
positional `skip_digestion` argument. Apply the existing dictionary extraction
tool before reconstruction; do not duplicate atom/bond/group remapping in the
converter or implement a removal-specific workaround.

## Why

The adapter is the common provider for selected conversion, extraction and
removal into MolSys. Silent selection loss changes the requested molecular
system and invalidates downstream index assumptions.

## What is measured and what is assumed

Executed on 2026-10-22 in the development environment: the #406 test
`tests/basic/test_remove_ownership.py::test_other_forms_keep_independent_out_of_place_route`
reproduced four output atoms instead of three. This uses the documented MolSysDict
0.1 schema: no saved analyses/mechanics and integer-readable structure labels.
These schema limits are not changed by the repair. No benchmark is claimed.

## What was refuted

Fixing only removal would leave conversion and extraction incorrect. Building a
complete native system and then implementing another remapping algorithm is
unnecessary because the dictionary extraction tool already owns projection.

## Scope and exclusions

The declared MolSysDict-to-MolSys edge only; no new schema fields, inference
policy, structure-label representation or file-handler route. The latter's
version-specific capability/diagnostic limitation is reported in #411.

## Acceptance criteria

Compare known atom IDs and analytic coordinate values after atom selection and
nonconsecutive/repeated structure selection through both public convert/extract.
Keep source payload unchanged, legacy positional adapter calls and removal's
selected result. Close with addressable converter guards and documentation.

## Resolution

The converter now accepts both axes as keyword-only arguments and delegates
projection to the existing dictionary extractor before building MolSys. Its
positional `item, skip_digestion` convention remains valid. Guards compare original
atom IDs, analytic coordinates and repeated/nonconsecutive structure labels
through both public conversion and extraction; the removal acceptance also passes.
The source payload remains unchanged. The complete dictionary-form group passes
in the final focused selection and the last broad run, as recorded under #406.
Its deterministic converter example and selected Foundations example execute.
No JSON schema, chemical inventory persistence or label policy is expanded.
