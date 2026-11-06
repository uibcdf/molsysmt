---
summary: Reconcile canonical H5MSM string storage with chemical-inventory append checks.
issue: uibcdf/molsysmt#616
status: open
opened: 2026-11-06
closed:
severity: medium
verification: reproduced
area: [h5msm, native, molsysviewer]
guard:
normative:
blocked_by: []
supersedes: []
---

# H5MSM component string storage and continued append

## What

A TcTIM source with water/ions removed appends to its fresh copy, but cannot
append to its H5MSM-recovered counterpart. The rejected target remains at one
structure in this reproduction. No partial write or lost coordinate is claimed.

```python
import molsysmt as msm

source = msm.convert(msm.systems['TcTIM']['1tcd.bcif.gz'], to_form='molsysmt.MolSys')
msm.remove(source, selection="group_type=='water' or group_type=='ion'", in_place=True)
msm.h5msm.write(source, '/tmp/tctim-append-receiving.h5msm')
restored = msm.h5msm.read('/tmp/tctim-append-receiving.h5msm')
msm.append_structures(source.copy(), source)  # one -> two structures
msm.append_structures(restored, source)      # StructuralInconsistencyError
```

## How

Independently reproduced without Viewer on native ed09f6453; current remote
main was fetched and resolves to that same source. Receiving uses contribution
8f8c442e, Python 3.14 and the recorded explicit PyUnitWizard source. The retained
3,818-atom systems have the same state/reference count, ID, completeness,
component evidence, provenance, memberships and 3,890-row normalized bond table.
Source `components.component_name` / `component_type` use object storage; the
reader restores nullable string storage. `_inventory_equals()` uses strict
DataFrame equality and rejects that representation difference before append.

The [format contract](../h5msm_format.md) declares canonical extension storage
on read. Its relation to inventory equality needs the native owner's decision.
This is distinct from #325's stringification of numeric/Boolean columns and
#520's partial publication before validating state/analysis associations.
The full seven-page board inventory (547 issues, 611 items including PRs) was
reviewed before opening this report.

## Why

The complete-session target under #421 / uibcdf/molsysviewer#264 must allow
continued work after persistence. An in-memory-versus-disk string backend must
not masquerade as a chemical difference. The addon cannot bypass native
alignment or rewrite chemistry tables to obtain acceptance.

## Acceptance and current boundary

The owner should qualify fresh/canonical targets, equivalent labels/nulls and
all state metadata/optional columns while retaining rejection for genuinely
different bonds, assignments, completeness, state order/reference or atom
correspondence. Preserve source/target data and explicit associations on both
acceptance and rejection. Publish a deliberate stricter limitation if that is
the intended contract. No native repair is included in this contribution.

The consumer's separate save/recover guards compare all scientific values,
nulls, membership and structural fields, allowing only the documented nullable
string representation. Those guards do not claim that subsequent source
structure append passes; this issue retains that continuation requirement.

## Consumer guard follow-up — 2026-11-06

Smoke 42239788034 on b18d5d823 passes 6,042 native cases/23 optional skips but
fails one new consumer session comparison (4,772 other addon passes, four
optional skips). CI uses pandas 3.1.1; its source component names have
`StringDtype(na_value=nan)` rather than the local object backing. The reader
returns `StringDtype(na_value=pd.NA)`. The consumer helper had admitted only
object-to-string normalization, so that stricter-than-format test rejects a
storage-only difference. A local NaN-string fixture reproduces the failure.

The test-only follow-up compares text values and exact null masks before
canonicalizing both string backings in temporary comparison copies. It adds
real TcTIM cases for object, nullable string and, where exposed by pandas,
NaN-backed string storage. Negative controls must still reject changed chemical
labels and null masks under each collected backing. All ten local session/
comparison cases pass; hosted recovery remains a new-source gate. No native
chemical data, append alignment check or scientific algorithm is changed, so
this does not resolve #616.
