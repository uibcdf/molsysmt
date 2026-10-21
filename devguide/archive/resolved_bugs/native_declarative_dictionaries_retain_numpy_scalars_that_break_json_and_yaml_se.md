---
summary: Native declarative dictionaries retain NumPy scalars that break JSON and YAML serialization
issue: uibcdf/molsysmt#394
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/molsysmt_TopologyDict/test_scalar_serialization.py
normative:
blocked_by: []
supersedes: []
---

# Native declarative dictionaries retain NumPy scalars that break JSON and YAML serialization

## What

`msm.convert` to TopologyDict/MolSysDict can retain NumPy integer scalars from
nullable native tables. `json.dumps` rejects them and PyYAML's safe writer cannot
represent them. Discovered while executing #393's corrected schema examples.

## How

Assign isotope 13 to an atom or a formal bond order to native chemical-state
bonds, then convert a Topology, MolSys or MolSysBuilder to its declarative form.
The three serializers duplicate a scalar normalizer that handles nulls but
returns a non-null `numpy.uint16`/`numpy.uint8` unchanged. No new chemistry or
schema is involved. Example error: `TypeError: Object of type uint16 is not JSON
serializable` on the `isotope` field.

Reproducer/guard: tests/form/molsysmt_TopologyDict/test_scalar_serialization.py
`tests/form/molsysmt_TopologyDict/test_scalar_serialization.py`.

## Why

The documented declarative transport fails on ordinary isotope and bond-order
values, also affecting native-to-YAML routes composed through these serializers.
The intended primitive values are already represented exactly by Python integers.

## Intended resolution

Share the existing scalar/null normalization at the declarative boundary and
convert NumPy scalars to their Python counterparts. Preserve IDs as strings,
nullable values as None and existing scientific/conversion-fidelity rules.
Keep structured quantity encoding owned by its existing codec. No new public
API, dependency, chemical field, or format version is introduced.

## Acceptance criteria

All three serializers must yield primitive values that survive actual JSON
and safe YAML transport and restore the expected isotope/order through public
conversion. Existing dictionary, YAML and conversion-fidelity tests must retain
state/observable refusals and report semantics.

## Resolution — 2026-10-21

Corrected the three Foundations dictionary pages against current writers and
readers. TopologyDict now lists real membership/endpoints and reference-chemistry
limits. MolSysDict documents its four fixed-unit structural fields, refusal of
attached analyses/preparation history and reportable chemical/mechanics losses.
StructuresDict is documented as a plain dictionary of arrays/quantities, with
no public constructor or in-memory base64/JSON representation. Broken form-API
links are replaced with existing public tools/owner references.

The course, conversion tutorial and conversion cookbook now explain these
same fidelity boundaries. The actual examples perform JSON or quantity-aware
native round trips with independent expected atom IDs, bond counts and physical
coordinates/time. The guard checks emitted record keys and concrete payload
types, not merely whether a table or example exists. All three historical
tables from source `17431bbb33ef6b8ee25df12193b4a2b45bc8df8e` fail these
real-payload checks. Complete corrected pages render with zero Sphinx diagnostics.

**Contract/parity tested:** 304 dictionary, builder, YAML, conversion-truth and
documentation cases pass with twelve workers and pytest-receptor. Six final
documentation guards pass after diagnostic refinement. These are overlapping
campaigns, not 310 distinct cases. No serialization schema was expanded.
The scalar transport defect discovered while executing the examples is resolved
independently under uibcdf/molsysmt#394. The constructor-temperature discrepancy
is retained separately in uibcdf/molsysmt#395 and is not repaired here.
