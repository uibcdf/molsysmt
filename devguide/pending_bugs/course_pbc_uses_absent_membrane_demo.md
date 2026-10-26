---
summary: Biophysics PBC course uses an absent membrane demo.
issue: uibcdf/molsysmt#466
status: open
opened: 2026-10-26
closed:
severity: medium
verification: reproduced
area: [docs, course, pbc]
guard:
normative:
blocked_by: []
supersedes: []
---

# Biophysics PBC course uses an absent membrane demo

**Reported:** 2026-10-26, authorized by the principal maintainer after PBC addon receiving.

## What

Executing the first code cell of
`docs/content/course/Path_Biophysics/40_PBC_Geometry.ipynb` raises
`KeyError: 'popc_membrane.h5msm'` at this lookup:

```python
import molsysmt as msm
system = msm.systems['POPC membrane']['popc_membrane.h5msm']
```

The actual registry has `popc_membrane.psf` and `popc_membrane.dcd` only.

## How

The notebook assumes an unregistered bundled file. Failure precedes box
retrieval or any PBC calculation. Its new addon ownership link changes prose
only and does not repair or qualify those code cells.

## Why

The membrane example cannot be followed by readers. The same source-key
mistake was fixed in PCA module 35 under uibcdf/molsysmt#449; that guard does
not cover this PBC module. This is a distinct remaining occurrence, not a
regression in the repaired PCA notebook. It surfaced while receiving the
expert addon under uibcdf/molsysviewer#264.

## What is measured and what is assumed

Actual first code-cell execution fails on the registry lookup. The other
three PBC path modules were reviewed, not rerun through their download and
solvation workflows. No failure of native PBC geometry is inferred.

## What was refuted

The source registry confirms that the requested H5MSM key is absent. The
reported error is not a Viewer import, selection, rendering or box-unit error.

## Scope and exclusions

Use the registered bundled membrane data and preserve the biological lesson.
Do not replace the membrane scenario with a synthetic box merely to pass.

## Acceptance criteria

Correct the input, execute the real notebook cells with pytest and assert
meaningful box lengths, angles and volume with units. Preserve the separate
module-35 PCA guard and its registered-source correction.

## Provenance

Python 3.14/Linux in `molsyssuite@uibcdf_3.14`; isolated provider c7fb92a62
with prose-only PBC addon links, delivered in 9061e2149. The local source
receiving receipt records the failed course verification separately from
successful geometry and addon tests.
