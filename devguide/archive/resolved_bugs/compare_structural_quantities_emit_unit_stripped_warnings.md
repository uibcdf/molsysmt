---
summary: Structural compare emits UnitStrippedWarning when normalizing quantities.
issue: uibcdf/molsysmt#435
status: resolved
opened: 2026-10-23
closed: 2026-10-23
severity: low
verification: reproduced
area: [basic, units]
guard: tests/basic/compare/test_compare_structural.py::test_compare_real_structural_quantities_without_implicit_unit_stripping
normative:
blocked_by: []
supersedes: []
---

# Structural compare emits UnitStrippedWarning when normalizing quantities

**Reported:** 2026-10-23, while receiving the MolSysViewer tools comparison API.
**Status:** Resolved at the source boundary; no installed/release qualification is claimed.

## What

Native `molsysmt.basic.compare` emits `UnitStrippedWarning` while comparing structural quantities of a real molecular system with itself. The same warning reaches the MolSysViewer tools addon; it is not introduced by the wrapper.

Observed on MolSysMT source `5911dace61c667138e0596ff631dc628d9b85ac1`, Python 3.14 in `molsyssuite@uibcdf_3.14`:

```python
import warnings
import molsysmt as msm

molsys = msm.convert(
    msm.systems['pentalanine']['traj_pentalanine.h5msm'],
    structure_indices=[0, 8, 3],
)
with warnings.catch_warnings(record=True) as observed:
    warnings.simplefilter('always')
    result = msm.compare(
        molsys, molsys,
        attribute_type='structural', include_none=True,
        output_type='dictionary',
    )

print(all(result.values()))  # True
print([(type(w.message).__name__, w.lineno) for w in observed])
```

The comparison emits six `UnitStrippedWarning` entries under the `always` filter, alternating between `molsysmt/basic/compare.py:349` and `:350`. Message: “The unit of the quantity is stripped when downcasting to ndarray.” Demo loading separately emits its existing H5MSM 0.4 deprecation warning, outside this capture.

## How

`array_equal_normalized()` calls `np.asarray(a)` and `np.asarray(b)` directly. Some structural attributes arrive as physical quantities. Their implicit ndarray conversion strips the unit and warns.

`coordinates=True` alone returned True without this warning in the same exercise; the reproduction deliberately retains the full structural-attribute route. Do not infer that every coordinate comparison warns.

## Why

Ordinary valid comparisons should not warn merely because MolSysMT returned its own quantity-valued attributes. It also prevents warning-strict consumers from treating an otherwise valid comparison as an ordinary query.

The observed self-comparison and addon/native parity remain correct. This report does **not** establish an incorrect scientific result, incompatible-unit comparison, or physical data loss. Severity: low; scientific unit handling still deserves an explicit regression.

## Acceptance criteria

- Compare real structural quantities without `UnitStrippedWarning`, preserving native boolean/dictionary outputs and missing-value/shape behavior.
- Normalize quantities explicitly through the owning unit tools; test physically equivalent values under different compatible unit policies and distinct values, rather than suppressing the warning.
- Add a focused native regression using the bundled system. Do not work around it with a downstream warning filter or a second addon comparison algorithm.

## Ownership and related work

- Provider: MolSysMT basic comparison / quantities.
- Consumer: `uibcdf/molsysviewer#264`, via `uibcdf/molsysmt#421` and `view.addons.molsysmt.basic.compare`.
- Distinct from closed `uibcdf/molsysmt#433`: that report concerned physical units incorrectly accepted as positional correspondence indices; this concerns comparison of legitimate physical quantities.
- Local analysis: `devguide/pending_bugs/compare_structural_quantities_emit_unit_stripped_warnings.md`.

No scientific fix or package/release qualification is claimed by this report.

## What is measured and what is assumed

Measured: the native structural self-comparison returns an all-True dictionary;
six quantity-downcast warnings are captured under an always filter. Native/addon
parity remains intact in the current receiving cases. Coordinates-only comparison
does not emit this warning in the same fixture. No unequal-physical-system result
has been diagnosed as wrong; there is no scientific-integrity claim here.

## What was refuted

The warning does not require Viewer or its addon. It is not the positional-index
units defect from uibcdf/molsysmt#433, a topology-rebuilding comparison, or the
separate legacy H5MSM demo-loading warning. A downstream filter would conceal
provider behavior instead of receiving an explicit unit-normalization contract.

## Scope and exclusions

Receive legitimate quantity-valued structural attributes in native comparison.
Do not broaden this into topology editing, general ArgDigest normalization,
unsupported comparison rules or a new addon algorithm. Warning suppression is
not a unit-normalization fix. The distinct explicit H5MSM compression-option
finding remains outside this report.

## Provenance

Reproduced in `molsyssuite@uibcdf_3.14` with its explicitly selected Python 3.14
interpreter, provider source `5911dace61c667138e0596ff631dc628d9b85ac1` and bundled
`pentalanine/traj_pentalanine.h5msm`, structures [0, 8, 3]. The ordinary source
checkout retains unrelated autosummary modifications; this is not an installed
artifact or release qualification. The reproduction above is the command's
Python body and needs no network or live browser.

## Resolution — 2026-10-23

The normalized-array comparison checks quantities with PyUnitWizard, verifies
compatibility and extracts values explicitly, converting the second operand to
the first operand's units. It never infers units for an unlabelled array or
compares equal magnitudes in incompatible dimensions. Existing shape, missing
value and numerical-tolerance rules are retained. No warning filter is added.
The separate explicit derived-box selector defect is uibcdf/molsysmt#437.

The real pentalanine reproduction now returns the all-True structural report
without UnitStrippedWarning. Literal nm/angstrom boxes and nm/pm application
policies verify equivalent and distinct observations. A controlled adapter
response exercises retained differing units and incompatible dimensions at
the public comparison boundary. It fails for the original magnitude-only
normalizer. Query selectors retain strict boolean validation.

Qualification: 179 comparison, PBC, argument-contract and bound-predicate cases
pass in 20.62 s with 12 workers and pytest-receptor (79 existing legacy-H5MSM
warnings). The public compare doctest passes in 5.60 s (three legacy warnings).
The comparison tutorial, course module 14 and conversion cookbook execute in
14.7, 10.6 and 13.5 s respectively. Foundations unit guidance and the docstring
state the explicit-normalization behavior. These are source-level controls,
not a full scientific or installed release matrix.
