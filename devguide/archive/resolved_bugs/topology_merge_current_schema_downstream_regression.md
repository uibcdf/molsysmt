# Resolved Bug: topology merge assumed the retired flat atom schema

**Status:** resolved, contract-tested, and downstream-tested 2026-07-16
**Severity:** high — two MolSysViewer merge workflows failed through MolSysMT
**Location:** `molsysmt/form/molsysmt_Topology/merge.py`

## Symptom and downstream impact

Merging current native topologies raised:

```text
IndexError: single positional indexer is out-of-bounds
```

The visible downstream failures were:

- `molsysviewer/tests/test_tools_basic_merge.py::test_tools_basic_merge_merges_scene_state_and_resolves_tag_collisions`;
- `molsysviewer/tests/test_tools_basic.py::test_tools_basic_merge_returns_new_view_from_multiple_views`.

The defect belonged to MolSysMT. Marking the consumer tests as expected failures
would only have been appropriate if the dependency could not be stabilized
promptly.

## Root cause

`molsysmt_Topology.merge` still offset atom hierarchy fields by positional
columns 3, 4, and 5. That assumed the retired flat atom table containing
`group_index`, `component_index`, and `chain_index` in those positions.

The current stable atom schema has five named columns:

```text
atom_id, atom_name, atom_type, group_index, chain_index
```

Component membership is atom-aligned chemical-state information and no longer
occupies an atom-table column. Accessing positional column 5 therefore failed,
while treating column 4 as component membership would also have corrupted chain
indices.

## Resolution

Merge now offsets named hierarchy columns before concatenation and handles
state-local component membership through the chemical-state API. It also
preserves:

- group, chain, molecule, and entity indices;
- component tables and atom-to-component membership;
- atom chemical-state attributes;
- normalized bond fields and every atom-reference field;
- conservative connectivity and component completeness metadata.

Inputs with multiple chemical states are rejected until an explicit state
alignment policy exists, preventing silent reference-state collapse.

## Evidence

At diagnosis, the MolSysMT merge suite gained a regression asserting the exact
then-current five-column atom schema, state-local component offsets, chain
offsets, formal-charge retention, and rich bond-reference remapping. The
subsequent additive `isotope` field makes the current schema six columns; the
same regression now locks that schema without changing the named-column merge
contract. All 15 focused MolSysMT merge tests passed when the incident closed.

Both previously failing MolSysViewer tests pass directly against the corrected
MolSysMT working tree. No downstream `xfail` is required.
