---
summary: Validated native bioassembly operations cannot round trip through H5MSM 0.5
issue: uibcdf/molsysmt#396
status: open
opened: 2026-10-21
closed:
severity: medium
verification: reproduced
area: [native, form, units, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Validated native bioassembly operations cannot round trip through H5MSM 0.5

**Reported:** 2026-10-21 during the native structure-copy persistence tests for
uibcdf/molsysmt#121.
**Status:** Open; the constructor/codec boundary needs a coordinated fix.

## What

A normally validated `Structures` constructor accepts one biological assembly
operation but normalizes its rotation to shape `(1, 1, 1, 3, 3)`. Public H5MSM 0.5
writing then rejects that same object because assembly rotations require shape
`(n_operations, 3, 3)`.

```python
from pathlib import Path
from tempfile import TemporaryDirectory
import numpy as np
import molsysmt as msm
from molsysmt.native import Structures

puw = msm.pyunitwizard
structures = Structures(
    coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm"),
    bioassembly={"1": {
        "chain_indices": [[0]],
        "rotations": [np.eye(3)],
        "translations": [puw.quantity([0., 0., 0.], "nm")],
    }},
)
print(np.asarray(structures.bioassembly["1"]["rotations"]).shape)
with TemporaryDirectory() as directory:
    msm.h5msm.write_layers(
        str(Path(directory) / "assembly.h5msm"), structures=structures,
    )
```

Observed output in the development environment:

```text
(1, 1, 1, 3, 3)
ValueError: Bioassembly rotations must have shape (n_operations, 3, 3).
```

## How

**Inspected:** `digest_bioassembly` delegates its operation lists to
`digest_rotations` and `digest_translations`. Their general geometry digesters
add structure/item axes to each operation. The H5MSM 0.5 assembly codec expects
a flat operation axis. General point/structure transform semantics and biological
assembly operation semantics are different contracts.

The assembly codec is in `molsysmt/form/_h5msm05_bioassembly.py`. Its existing
round-trip tests include `skip_digestion=True` fixtures, so they verify the codec
but do not guard the normally validated constructor-to-writer route. Validate
all numeric shapes and translation units at the owning assembly boundary rather
than relaxing the codec to accept arbitrary extra axes.

## Why

Users can obtain a valid-looking native object through the public constructor
that cannot be saved through the public H5MSM writer. This blocks that assembly
workflow with a clear error; no silent persisted scientific corruption was
observed. The new coordinate-block storage does not modify any assembly
normalizer or codec involved in the reproduction.

## What is measured and what is assumed

**Reproduced:** the minimal constructor/public-writer call above on Linux,
Python 3.14.7, on 2026-10-21, while #121 was based on MolSysMT
`85b8b038008de4b6ac05e6f6c3e5028935bd3f85` with native structure-storage work in
progress. The implicated digesters and H5MSM assembly codec have no changes in
that work. Existing schema-compatible metadata assigned directly to the native
field round-trips; this does not qualify public constructor validation.

**Not qualified:** all supported chain-scope and multi-operation combinations.
Translation normalization may expose an additional shape mismatch after the
rotation error is resolved and must be covered in the same boundary tests.

## What was refuted

- This is a failure of copying the assembly metadata: writing the original
  freshly constructed object fails before a copy is attempted.
- The codec's existing bypassed fixtures prove the public route: the normal
  constructor changes their operation shape.
- Silently squeezing arbitrary dimensions is an adequate contract: operation
  axes must be normalized deliberately and malformed inputs rejected.

## Scope and exclusions

Align native assembly validation and typed H5MSM 0.5 persistence. Preserve
proper-rotation checks and explicit translation units. Do not change general
structure/point transform shapes solely to repair an assembly-specific caller.
No fix, scientific algorithm, dependency floor or release decision is delivered
by this report. #121's copy tests use schema-compatible native metadata and do
not claim to resolve this constructor defect.

## Acceptance criteria

- A normally validated public constructor can write and read one/multiple
  assembly operations, including common and per-operation chain scopes.
- Translation values retain explicit length units under non-default application
  units; row/operation ordering and numerical transforms survive the round trip.
- Invalid rotations, missing/incompatible units, operation counts and chain
  scopes fail clearly before publication.
- A public constructor-to-H5MSM regression guard exercises ordinary validation;
  `skip_digestion=True` alone cannot satisfy it.
