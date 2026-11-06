---
summary: Reconcile canonical H5MSM string storage with chemical-inventory append checks.
issue: uibcdf/molsysmt#616
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: medium
verification: reproduced
area: [form, native]
guard: tests/native/test_recovered_inventory_append.py
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

The [format contract](../../h5msm_format.md) declares canonical extension storage
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

## Native-owner receiving — 2026-11-06

The owner independently reproduces the original 3,818-atom TcTIM continuation
failure on main `4a80c22941090257d8ef78df09c944831413ee31`. This report is received
from PR #543 head `8ab2f5474b2e04c68d31ef2854a238984b645fc8`; its original
consumer evidence above is preserved.

The correction is a shared private native table comparator. It retains the
fast typed-equality path, exact axes/columns, numerical/Boolean typing and all
inventory/state metadata checks. On a storage-only mismatch it compares actual
string/missing values through temporary nullable-string columns, without
rewriting source/target tables. Stable and chemical inventory comparisons use
the same owner helper. This does not coerce numeric/Boolean data into label
text, turn missing values into literal strings, or accept absent optional fields.
Only mismatched string columns need temporary arrays; no coordinates are copied
for comparison. This allocation statement is source-inspected, not a benchmark.

The maintained native regression covers native/dictionary/H5MSM targets, both
public mutation modes, object/nullable/`str` backings, two states, optional atom
fields, null labels and explicit/unknown structure associations. It preserves
named occurrence indices, original observations and evaluated-empty coverage;
new structures remain unevaluated. The original TcTIM case also exercises the
direct native append path. Negative controls retain changes in bonds,
assignments, component memberships/labels, missing/optional values, completeness,
state/reference order and atom correspondence. Numeric/Boolean-to-string label
coercion is independently refused.

The first new test-authoring attempt incorrectly reads occurrence indices as an
attribute instead of the public query dictionary. It records six authoring
failures and the real TcTIM rejection. After correcting that assertion, five
positive persistence cases fail with the original inventory exception, while
16 native/negative controls pass. These original JUnit files are retained.
The first corrected-runtime selection passes 75 native/association/atomicity
cases. A broader native/composition/H5MSM/interaction selection then passes
2,735 cases with zero failures/errors/skips; warning categories are retained.
Final expanded string-backing/docstring and integrated receiving follows below.

This receiving uses Linux/Python 3.14.7 in the existing development environment,
published Pytest Receptor 1.2.1 and 12 workers. No dependency/environment or
compiled backend is changed. This does not qualify an installed Viewer pair,
other platforms, a release candidate or a complete scientific session. The
owning progress packet is [here](../../pre_1_0_robustness_audit_20261106.md).

## Resolution checkpoint — 2026-11-06

Implemented in `19d6d55c1663bf3c6c7adfb9433fc775326292b5`. The final joint native,
composition, H5MSM and named-interaction selection passes **2,748 cases**, with
zero failures/errors/skips and 746 retained warnings. The expanded string/append
and module-doctest selection passes **40 cases** separately; scopes overlap and
are not summed. All-code Ruff checks/formatting, dependency validation and the
156-notebook course structure check pass. Tutorial/course edits preserve every
code cell, output, ID and metadata; affected public docstrings, tools, cookbook
and native-domain guidance describe the contract.

The [portable phase-one receipt](../../../devtools/data/pre_1_0_robustness_phase1_receiving_20261106.json)
retains original failed/authoring attempts, exact test summaries/digests, source
identity/hashes, versions and limits. Source delivery is verified on origin
before board closure. A source closeout does not qualify another platform, an
installed Viewer pair or a release artifact. PR #543's remaining graphical/session
receiving and other linked defects retain their own scope.
