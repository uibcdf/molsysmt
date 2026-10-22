---
summary: ViewerJSON native decoding rejects string chain IDs
issue: uibcdf/molsysmt#397
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [form, native, attribute, tests]
guard: tests/form/molsysmt_ViewerJSON/test_label_identity.py
normative:
blocked_by: []
supersedes: []
---

# ViewerJSON native decoding rejects string chain IDs

**Reported:** 2026-10-21 during admitted-payload copying probes for #121.
**Status:** Resolved; IDs are string labels and optional index columns carry identity.

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

## Resolution — 2026-10-21

**Implemented:** all native ID assignments use pandas string storage. The decoder
also transfers element symbols, obtains group names from each group's actual
first atom, compacts entity rows, and aligns group-to-synthetic-molecule-to-entity
membership. Components use the existing native connectivity rebuild tool, with
local string IDs; the decoder does not duplicate a connectivity algorithm.

The native exporter now supplies optional per-atom group_index, chain_index and
entity_index columns. The reader validates them, compacts represented elements in
source positional order, and rejects contradictory labels/group metadata with the
existing SMonitor FormatError. These are additive graphics-schema fields, not a
new H5MSM schema or new public function. Legacy label-only payloads still decode:
chain/entity labels define identity and group labels define identity within a
chain. They cannot distinguish repeated identities sharing those labels. The
reader cannot authenticate missing identity; callers needing distinct elements
must supply their positional columns. Unknown membership remains nullable and an
empty payload creates no phantom hierarchy.

The graphics projection omits complete component/molecule metadata. Components
are reconstructed from stored bonds; one synthetic molecule per represented group
supplies a coherent entity association. This is a documented projection policy,
not a claim of a lossless full native round trip. H5MSM remains the full-domain
persistence route. Geometry collection, charge persistence, dependency floors and
scientific calculations are unchanged. No new Ackredit attribution boundary or
external engine integration is involved.

**Contract-tested:** the initial 16-case identity module failed against the old
reader (string parsing, missing explicit axes and rejection diagnostics). The
final 22-case module covers the exact reported builder, alphabetic/leading-zero
labels, numeric legacy labels, duplicate labels including within one chain,
nonconsecutive axes and reordered atoms, invalid index types/ranges/lengths,
conflicting metadata, empty hierarchy and cross-group covalent connectivity.
The combined native Topology/MolSys/Structures/ViewerJSON form scope and remaining
copy-protocol regressions obtained **1,859 passed**, no omissions, in 17.85 s with
`python -m pytest --receptor=llm -n 12` on Linux/Python 3.14.7. Six expected legacy
H5MSM deprecation warnings were retained. Three doctest items across the reader,
exporter and wrapper passed. Source tests do not qualify installed MolSysViewer,
its renderer or other operating systems. The independent extraction defect found
during review is tracked in uibcdf/molsysmt#399.

The 14 fast repository gates, package Ruff checks, focused formatting checks,
public docstring fidelity (247 functions) and course structure validation also
passed. The obsolete course-local validator was invoked during inspection and
reported its already documented historical template mismatch; the maintained
`devtools/scripts/validate_course.py` is the passing gate. Documentation changes
are narrative-only in the existing notebooks; their executable cells/outputs
were preserved. No full Sphinx build or notebook reexecution is claimed here.
