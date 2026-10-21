---
summary: Native dictionary guides describe fields outside their implemented 0.1 schemas
issue: uibcdf/molsysmt#393
status: open
opened: 2026-10-21
closed:
severity: medium
verification: inspected
area: [docs, form]
guard:
normative:
blocked_by: []
supersedes: []
---

# Native dictionary guides describe fields outside their implemented 0.1 schemas

## What

The Foundations pages for TopologyDict and MolSysDict describe a broader or
incorrect schema compared with their actual 0.1 serializers/converters.
Discovered while updating the independent #128 stored-atom query documentation.
This is a documentation finding, not a proposed serialization expansion.

## How

Compare the declarative schema tables in
`docs/content/user/foundations/native_world/classes/molsysmt_TopologyDict.md`
and `molsysmt_MolSysDict.md` in that directory with:

- `molsysmt/form/molsysmt_Topology/to_molsysmt_TopologyDict.py`;
- `molsysmt/form/molsysmt_TopologyDict/to_molsysmt_Topology.py`;
- `molsysmt/form/molsysmt_MolSys/to_molsysmt_MolSysDict.py`;
- `molsysmt/form/molsysmt_MolSysDict/_builder.py`.

**Inspected:** TopologyDict's table advertises components and atom-level
`group_index`/`chain_index`, while the serializer writes group `atom_indices`
and chain `group_indices`. Molecule/entity membership uses `group_indices` and
`molecule_indices`, rather than the advertised parent fields. Bond endpoint
keys are `atom_index_1`/`atom_index_2`, not `atom1_index`/`atom2_index`.
MolSysDict's 0.1 nested structures are not the general StructuresDict contract;
its reader handles coordinates, box, time and structure_id. The complete-domain
and lossless-JSON wording needs review against the admitted conversion-fidelity
limits, including chemical states, interactions and other observables.

## Why

Users following these tables can write records whose fields are ignored or
missing on reconstruction, or assume lossless persistence of unsupported
native domains. The stable 0.1 contract must be documented as implemented.

## Intended resolution

Correct the schema tables, examples and fidelity limits without changing the
format. Link each page to actual supported conversions. Verify examples and
schema keys against representative serializer output, retaining unsupported
state/observable refusal tests. Check neighboring dictionary pages for the
same concrete discrepancy; do not expand the review to unrelated formats.

No schema change is authorized by this report. The #128 query implementation
remains separately tracked in its own record.
