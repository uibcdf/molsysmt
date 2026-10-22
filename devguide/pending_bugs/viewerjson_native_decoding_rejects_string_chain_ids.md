---
summary: ViewerJSON native decoding rejects string chain IDs
issue: uibcdf/molsysmt#397
status: open
opened: 2026-10-21
closed:
severity: medium
verification: reproduced
area: [form, native, attribute, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# ViewerJSON native decoding rejects string chain IDs

**Reported:** 2026-10-21 during admitted-payload copying probes for #121.
**Status:** Open; reproduced before any copy, with the decoder unchanged.

## What

A native system with chain ID `A` can be projected to ViewerJSON, but converting
that unchanged payload back to MolSys raises `ValueError` instead of preserving
the label and assigning local positional indices.

```python
import molsysmt as msm
builder = msm.MolSysBuilder()
builder.add_atom(atom_name="C", atom_type="C")
builder.add_group([0], group_name="LIG", group_id="10")
builder.add_chain(group_indices=[0], chain_id="A")
builder.set_coordinates(msm.pyunitwizard.quantity([[[0., 0., 0.]]], "nm"))
molsys = builder.build()
payload = msm.convert(molsys, to_form="molsysmt.ViewerJSON")
assert payload.data["atoms"]["chain_id"] == ["A"]
msm.convert(payload, to_form="molsysmt.MolSys")
# ValueError: invalid literal for int() with base 10: np.str_('A')
```

## How

`molsysmt/form/molsysmt_ViewerJSON/to_molsysmt_MolSys.py` builds positional
membership separately, then casts the unique chain labels to pandas `Int64`
when assigning `topo.chains["chain_id"]`. Other ID assignments also use numeric
storage and need an invariant audit; those other paths are inspected findings,
not independently qualified failure cases in this report.

## Why

Element IDs are string labels in native MolSysMT. Ordinary alphabetic chain
labels must not be parsed as indices. A generated payload cannot currently
complete its advertised native read route in this common case.

## What is measured and what is assumed

**Reproduced:** the exact one-atom example above in the existing Linux/Python
3.14.7 development environment. The copy hooks are not invoked. No timing,
scale estimate or client-installed qualification is claimed.

## What was refuted

Copying did not introduce the defect: decoding the original generated payload
fails. Coordinates and chain membership are declared, so this is not missing
geometry or an unresolved chain domain.

## Scope and exclusions

Fix native label normalization without treating labels as positions or silently
merging ambiguous source identities. Copying a ViewerJSON wrapper, JSON bond
serialization and its visual rendering are separate operations. No codec fix
is included in #121's resident-copy changes.

## Acceptance criteria

Add a guard for a generated payload containing alphabetic chain labels. Native
read must preserve string element IDs and positional membership. Include
nonconsecutive numeric-looking labels and explicitly define any duplicate-label
limitation; do not repair this by globally casting IDs to integers.

## Provenance

Observed 2026-10-21, Linux, Python 3.14.7, development environment. Decoder code
is unchanged from `e83d854b2`; the repro does not use resident-copy helpers.
