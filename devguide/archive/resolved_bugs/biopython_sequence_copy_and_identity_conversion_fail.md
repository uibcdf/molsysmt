---
summary: Biopython sequence copy and identity conversion fail.
issue: uibcdf/molsysmt#360
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [form, basic, convert]
guard: tests/form/biopython_Seq/test_copy_and_identity_conversion.py::test_sequence_copy_and_identity_conversion_are_independent
normative:
blocked_by: []
supersedes: []
---

# Biopython sequence copy and identity conversion fail

**Reported:** 2026-10-09, after the real-input recognition repair under #359.
**Status:** Resolved for existing full-copy, extraction and identity-conversion routes.

## What

```python
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord
import molsysmt as msm

msm.copy(Seq("AGX"))
# AttributeError: 'Seq' object has no attribute 'copy'
msm.copy(SeqRecord(Seq("AGX")))
# AttributeError: adapter has no copy operation
msm.convert(Seq("AGX"), to_form="biopython.Seq")
msm.convert(SeqRecord(Seq("AGX")), to_form="biopython.SeqRecord")
# TypeError: extract() got an unexpected keyword argument 'group_indices'
```

## How

The Seq copy adapter and both all-selection extract branches call `item.copy()`.
Neither external object provides that method. SeqRecord has no registered copy
adapter. Both identity converters pass `group_indices` to existing extractors
whose established parameter name is `atom_indices`.

## Why

The public copy contract promises an independent object. These registered routes
cannot perform even a full copy or conversion, irrespective of annotation content.
Changing only the keyword does not repair the subsequent invalid copy call.

## What is measured and what is assumed

All four public failures were reproduced in the shared Python 3.14 development
environment. Standard-library `deepcopy` creates a distinct Seq object; guards
also require detached nested record annotations and features, rather than
assuming a shallow object copy suffices. The original regression module failed
all 13 cases before repair, exposing three failure mechanisms: invalid copy
method, missing copy registration and mismatched delegation keyword.

```bash
python -m pytest tests/form/biopython_Seq/test_copy_and_identity_conversion.py \
  molsysmt/form/biopython_Seq/copy.py \
  molsysmt/form/biopython_SeqRecord/copy.py \
  --doctest-modules --receptor=llm -n12
```

After repair, the expanded command passes 15 public facade cases and two
docstring examples. The two additional facade cases check full public extraction
and explicit source reuse. This is contract evidence, not a performance benchmark.

## What was refuted

A new sequence class or chemical reconstruction is unnecessary. The external
objects already retain their sequence and metadata. Selecting arbitrary SeqRecord
positions is a separate annotation/feature-remapping contract and must remain an
explicit unsupported operation in this bounded repair.

## Scope and exclusions

Repair copy, full identity conversion and the already implemented Seq subset
route. Preserve `copy_if_all=False` object reuse. No new SeqRecord subset semantics,
editing operation, hard dependency, or release-candidate qualification is added.

## Acceptance criteria

Public copy and identity conversion return independent objects with unchanged
content and metadata; mutations to nested copied record metadata do not affect
the source. Empty, undefined and absent sequence content remain distinguishable.
Explicit source reuse and ordered/repeated Seq subsets work. Unsupported record
subsets fail clearly without changing the source.

## Provenance

Linux, Python 3.14.7, shared `molsyssuite@uibcdf_3.14` development environment,
Biopython 1.87, 2026-10-09. The release-publication pause and frozen artifact identities remain.

## Resolution

Both full extraction routes delegate to their public digested copy adapter.
Those adapters use standard-library `deepcopy`, and SeqRecord registers its copy
operation for the public facade. Identity conversion maps group-position
selection to the existing extractor parameter, preserving its public signature.
No new record subset algorithm is introduced.

The guard's four cases exercise real Seq and SeqRecord objects through both
public operations. They assert exact source content, object independence, labels
and independently mutable nested annotations, per-position annotations and
feature qualifiers. A stub returning the input, shallow metadata copy or
sequence-only record reconstruction cannot satisfy those assertions. Companion
guards cover source reuse, empty/undefined/absent content, ordered/repeated Seq
subsets, explicit record-subset rejection and full extraction. Foundations, both
form Toolbox pages, the conversion Cookbook and Common Core Module 8 describe
the supported boundary.
