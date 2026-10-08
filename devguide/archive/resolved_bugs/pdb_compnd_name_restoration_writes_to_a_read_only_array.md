---
summary: PDB molecule-name restoration writes to a read-only Pandas array
issue: uibcdf/molsysmt#349
status: resolved
opened: 2026-10-07
closed: 2026-10-07
severity: medium
verification: reproduced
area: [form, convert]
guard: tests/form/molsysmt_PDBFileHandler/test_to_molsysmt_native.py::test_compnd_names_preserve_topology_with_copy_on_write
normative:
blocked_by: []
supersedes: []
---

# PDB COMPND name restoration writes to a read-only array

**Reported:** DockingMT under uibcdf/molsysmt#349, related to
uibcdf/dockingmt#42 and uibcdf/dockingmt#30.
**Status:** Resolved; public file and handler conversions preserve COMPND names
with both object-backed and inferred-string columns.

## What

Public conversion of the bundled 181L PDB raises
`ValueError: assignment destination is read-only` under Copy-on-Write:

```python
import pandas as pd
import molsysmt as msm

with pd.option_context('future.infer_string', False, 'mode.copy_on_write', True):
    msm.convert(msm.systems['T4 lysozyme L99A']['181l.pdb'],
                to_form='molsysmt.MolSys')
```

Pandas 3 always enables Copy-on-Write; only the `future.infer_string` option
is needed for the consumer's original reproduction.

## How

`_apply_compnd_names` in
`molsysmt/form/molsysmt_PDBFileHandler/to_molsysmt_MolSys.py` obtains
`molecule_name` through `to_numpy(dtype=object)` and modifies that array before
assigning it back to the column. An object-backed column can expose a protected
view. Requesting `copy=True` provides the independently writable buffer the
operation needs. The read-only `molecule_type` array requires no copy.

## Why

Both public file and handler routes fail before returning a system. Default
string inference passing did not cover applications choosing object strings.
This is a current-profile correctness repair admitted by the frozen 1.0 scope,
not an expansion of chemical preparation.

## What is measured and what is assumed

Before the fix, the four-case public regression yielded two failures and two
passes with Pandas 2.3.3. Both object-string routes failed at the reported
assignment. After the fix, the following selection passed 46 cases with
Pandas 2.3.3 and the same 46 with Pandas 3.0.6:

```bash
python -m pytest --receptor=llm -n 12 \
  tests/form/molsysmt_PDBFileHandler/test_to_molsysmt_native.py \
  tests/form/file_pdb/test_connectivity_policy.py
```

The Pandas 3 run retained twelve deprecation warnings about explicitly setting
the now-always-enabled Copy-on-Write option. Counts from the two environments
are separate compatibility observations, not 92 unique tests. The guard
asserts the literal COMPND name, atom/group/bond/entity counts, atom indices'
associated IDs, unchanged coordinates, input COMPND records and handler liveness.
It fails without the buffer copy; it does not merely inspect source spelling.

## What was refuted

Default string inference does not establish object-column compatibility. No
global Pandas option change, disabled Copy-on-Write or backend substitution is
needed. The failure is also reproducible with Pandas 2's Copy-on-Write enabled.

## Scope and exclusions

The repair changes one private buffer allocation and preserves public defaults,
chemical criteria, index spaces and units. It adds no public API. The complete
source/installed matrices for a future 1.0 candidate remain owned by #334; the
published 0.23.0 files do not contain this later repair.

## Acceptance criteria

The named public regression must restore `T4 LYSOZYME` under both string
inference modes and both input routes, preserving topology and input data.
Adjacent connectivity-policy cases must remain green on Pandas 2 and 3.

## Provenance

Linux x86_64, Python 3.14.7, NumPy 2.4.6, 2026-10-07. Development environment:
`molsyssuite@uibcdf_3.14`, Pandas 2.3.3. Existing retained compatibility
environment: `molsysmt-stabilization-py314-20261006`, Pandas 3.0.6; no new
environment was created. Both imported this checkout's editable source and
retained the existing native extension. JUnit outcomes and hashes are retained
in the [bounded closure receipt](../../../devtools/data/pre_1_0_issue_reconciliation_20261007.json).
