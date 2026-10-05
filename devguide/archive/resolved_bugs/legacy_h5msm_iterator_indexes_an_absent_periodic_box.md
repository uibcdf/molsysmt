---
summary: Legacy H5MSM iterator indexes an absent periodic box
issue: uibcdf/molsysmt#330
status: resolved
opened: 2026-10-05
closed: 2026-10-05
severity: medium
verification: reproduced
area: [form, basic]
guard: tests/form/file_h5msm/test_structures_v05_probe.py::test_legacy_structural_iterator_returns_none_for_an_absent_box
normative:
blocked_by: []
supersedes: []
---

# Legacy H5MSM iterator indexes an absent periodic box

**Reported:** 2026-10-05, while qualifying uibcdf/molsysmt#304 peptide reports.
**Status:** Corrected and contract-tested; published resolution is recorded at closure.

## What

A legacy 0.4 file can contain coordinates without a box. Its native structures
iterator, requested with coordinates and box, indexes the zero-length box
instead of returning absent evidence:

```python
from molsysmt.form.file_h5msm.iterators import StructuresIterator
with StructuresIterator(filename, structure_indices=[0],
                        coordinates=True, box=True,
                        output_type='dictionary') as iterator:
    result = next(iterator)
# OSError: selection + offset not within extent for file dataspace
```

The regression fixture creates this file with the legacy writer from a native
MolSys carrying coordinates and no box. The public peptide report reaches that
supported iterator and fails before it can use Cartesian geometry.

## How

`form.molsysmt_H5MSMFileHandler.iterators.StructuresIterator.__next__` indexes
`f['box'][indices, :, :]` even if that dataset is empty. Initialization correctly
omits its unit from the populated fields, but the read does not use that evidence.
The equivalent time/id branches already protect absent datasets.

## Why

Supported legacy nonperiodic systems fail on a combined structural query. The
failure is independent of peptide chemistry and affects the general adapter.
Correct absence must not be replaced with an invented box or guessed unit.

## What is measured and what is assumed

**Reproduced:** both legacy filenames and caller-owned handlers fail in the
peptide guard on the box indexing line. No source data are changed. This is a
read failure, not a corrupt file or unsupported coordinate unit.
No throughput or whole-trajectory memory result is claimed.

## What was refuted

The coordinates and selected structure are present. Changing the scientific
PBC policy cannot repair an adapter that unconditionally indexes an absent box.

## Scope and exclusions

Return None for an empty legacy box series while preserving coordinate rows,
units and caller-owned handler lifetime. The related #304 adapter extension
also delegates alternate-location requests to their existing getter; unsupported
legacy label evidence remains explicit in the peptide report. No schema changes.

## Acceptance criteria

The named general adapter guard reads coordinates and None for the absent box.
Public peptide controls pass for both legacy paths and leave caller handles open.
Retain legacy deprecation diagnostics and physical-unit validation.

## Provenance

Linux x86_64, 2026-10-05, Python 3.14.7, h5py 3.16.0, NumPy 2.4.6 and released
ArgDigest 0.13.0 source overlay. Source base c2f16cbc2 plus #304 work. These are
editable-source controls, not installed-release qualification.

## Resolution

The adapter returns None before indexing an empty box dataset or constructing a
quantity. The guard creates an actual 0.4 file and asserts that coordinates are
read unchanged and no box is invented. Public peptide guards cover file and
caller-owned handler paths, preserving the handle after the read.

The affected combined selection passed **147 tests in 32.68 s**, with 28 legacy
H5MSM deprecations and two existing pandas setter FutureWarnings retained. The
run includes the new report doctest, previous template/peptide guards and the
full `test_structures_v05_probe.py` module. This is focused source qualification,
not the full matrix. The command and environment are recorded in the #304 report.
