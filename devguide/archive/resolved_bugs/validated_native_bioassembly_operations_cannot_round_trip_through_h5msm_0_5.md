---
summary: Validated native bioassembly operations cannot round trip through H5MSM 0.5
issue: uibcdf/molsysmt#396
status: resolved
opened: 2026-10-21
closed: 2026-10-22
severity: medium
verification: reproduced
area: [native, form, units, tests]
guard: tests/form/file_h5msm/test_validated_bioassembly.py
normative:
blocked_by: []
supersedes: []
---

# Validated native bioassembly operations cannot round trip through H5MSM 0.5

**Reported:** 2026-10-21 during the native structure-copy persistence tests for
uibcdf/molsysmt#121.
**Status:** Resolved on 2026-10-22; the reproduction below describes the original defect.

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

**Initial unqualified scope:** common/per-operation scopes and multi-operation
translations were not yet qualified at opening. The resolution below supplies
those tests; this historical reproduction is not current behavior.

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
The initial #121 copy tests use schema-compatible native metadata and do not
resolve this constructor defect. The separate repair below changes neither a
scientific algorithm, a dependency floor nor a release decision.

## Acceptance criteria

- A normally validated public constructor can write and read one/multiple
  assembly operations, including common and per-operation chain scopes.
- Translation values retain explicit length units under non-default application
  units; row/operation ordering and numerical transforms survive the round trip.
- Invalid rotations, missing/incompatible units, operation counts and chain
  scopes fail clearly before publication.
- A public constructor-to-H5MSM regression guard exercises ordinary validation;
  `skip_digestion=True` alone cannot satisfy it.

## Resolution — 2026-10-22

**Implemented:** assembly digesters now preserve exactly one operation axis,
reusing the existing proper-rotation validator. Translation vectors retain
explicit length units, including mixed input units and nondefault output policy.
Common chain indices and per-operation chain scopes retain their distinct
meaning. Counts, malformed axes, nonfinite matrices/vectors and invalid chain
indices fail at validation. New containers prevent partial mutation of caller
metadata and make repeated normal construction idempotent.

Extraction uses the chain sequence length rather than an ambiguous NumPy truth
value. The builder recognizes flat common sets separately from repeated
per-operation sets, including a single common chain. Its preexisting limit on
heterogeneous per-operation sets remains explicit. General rotation/translation
coordinate axes and the H5MSM storage schema are unchanged. Trusted codec input
that deliberately bypasses validation retains its existing storage checks.

**Contract-tested:** the new public regression module covers one/multiple/zero
operations, empty chain scopes, both scope encodings, matrix/list translation
inputs, input nonmutation, repeated construction, malformed operations and
public H5MSM round trips. The initial 23-case counterfactual produced 17 failures
and six passes against the original implementation. The final guard also
includes common-single-chain and explicit unsupported-builder cases.

**Analytically checked:** direct dictionaries, named assemblies and reloaded
H5MSM assemblies produce the expected identity and quarter-turn-plus-translation
coordinates for selected chain sets. This verifies geometry independently of
another codec's output.

**Validation:** Linux/Python 3.14.7 in the existing development environment;
12 workers and `pytest-receptor`. The first integrated H5MSM/copy/geometry/build
campaign passed 841 tests with 614 expected legacy deprecation warnings. A
separate PDB/BCIF/native-parser campaign passed 481 tests with one expected
cross-chain covalent-bond warning. Eleven docstring examples and the new
self-contained assembly-persistence recipe execute successfully. Notebook code
cells and their saved outputs are unchanged; their prose was updated, without
claiming a new complete course/notebook execution. The final focused rerun passes 34 tests, including all 27 new public guards and
the bundled-system assembly builder. All fourteen fast gates, full-package Ruff,
docstring fidelity, public API drift, dependency and developer-guide checks pass.
The full installed/platform release matrix is not claimed.

The independent builder defect that ignores nondefault structure indices is
tracked as uibcdf/molsysmt#401; the analytical assembly checks here deliberately
use structure 0. It does not invalidate this operation-shape/persistence repair.
