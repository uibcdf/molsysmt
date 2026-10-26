---
summary: flip rejects its default and distorts geometry for nonunit plane normals.
issue: uibcdf/molsysmt#460
status: resolved
opened: 2026-10-25
closed: 2026-10-25
severity: high
verification: reproduced
area: [structure, digestion]
guard: tests/structure/flip/test_reflection_contract.py
normative:
blocked_by: []
supersedes: []
---

# Reflection default and normal scaling

## What

The declared `vector=None` default rejects before the intended z-normal fallback.
A normal `[2, 0, 0]` changes distances rather than describing the same reflection
as `[1, 0, 0]`. The zero vector silently returns unchanged coordinates.

## How

```python
import molsysmt as msm
from molsysmt.native import Structures
puw = msm.pyunitwizard
molsys = Structures(coordinates=puw.quantity([[[1, 2, 3], [4, 5, 6]]], 'nm'))
msm.structure.flip(molsys)  # ArgumentError instead of the intended z reflection
msm.structure.flip(molsys, vector=[2, 0, 0])  # x becomes -7, -28 instead of -1, -4
```

The Rust kernel evaluates `r - 2 dot(r-p, n) n`, which assumes a unit normal.
Generic vector digestion accepts nonunit vectors without normalization and
refuses None, making the Python default fallback unreachable. The measured pair
distance changes from 5.196152422706632 to 21.42428528562855 nm for `[2, 0, 0]`.

## Why

A plane is unchanged by any finite nonzero scaling of its normal. Reflection
must preserve distances and be its own inverse. These native defects were
independently disclosed during uibcdf/molsysmt#421 receiving but had no separate
owning report; the addon must reuse the repaired provider, not supply a second
reflection algorithm.

## Scope and acceptance

Keep the signature and Rust kernel. Define the existing None default as
`[0, 0, 1]`; normalize finite nonzero normals without modifying input arrays.
Validate a single finite length-bearing plane point before coordinate writes.
Keep generic vector semantics unchanged for other callers. Reuse the existing
private scale-safe vector helper and compiled reflection kernel.

Independent analytical, isometry and double-reflection tests must cover native
MolSys/Structures, selected and repeated atoms/structures, unit policies,
in-place/independent outputs, boxes and scoped interaction invalidation. Invalid
normal/point rejection preserves coordinates and analysis identity/coverage.
Bound-addon receiving and documentation must reflect the same scientific owner.
No new method, backend, form or release capability is added.

## Provenance

Reproduced without Viewer on `7b1604ec36f67efc80fa5f159f2469f9b58325c4`,
Linux/Python 3.14.7, existing development interpreter, 2026-10-25.


## Resolution — 2026-10-25

A flip-specific branch in vector digestion maps None to [0, 0, 1] and uses the
existing private scale-safe unit-vector normalizer. It refuses zero, nonfinite,
complex or unit-bearing normals while preserving caller arrays. Other vector
callers retain their existing values and None refusal; no global vector policy
is changed. No additional Rust routine is needed: the existing compiled kernel
already implements reflection correctly for a unit normal.

One finite real length-bearing plane point applies to all selected structures.
Point stacks previously lost all but their first row; they now reject before
writes. General point digestion reuses the existing quantity-string parser so
unparseable input raises the catalogued argument error, and rejects complex
points before a float cast could discard their imaginary part. The reflection
boundary also refuses a nonfinite result before coordinate publication.

The function's signature, form-agnostic basic getters/setters, physical unit
policy, selected atom/structure axes, independent output and native None return
remain intact. Boxes and stored chemistry are unchanged. Native coordinate
setters invalidate only edited-structure interaction coverage; invalid plane
inputs preserve coordinates, box and analysis identity/coverage. Reflection
reverses handedness, which is now explicit in the docs and course.

## Validation

The initial 79-case independent reflection selection produced 71 failures and
eight passes on the original source. This includes scaled-normal, default and
invalid-plane admission checks, not 71 distinct defects. Independent
Householder plane matrices, pair distances, fixed plane points, inverse
reflection and signed tetrahedral volume protect the repaired scientific intent.
Native MolSys and coordinate-only Structures, repeated/nonconsecutive axes,
input arrays, nm/angstrom/pm policies and real bound-view synchronization are
covered. The generic-vector guard checks that the policy stays caller-specific.

The focused selection initially passes 592 cases in 20.87 seconds. Two updated
notebooks execute successfully: the POPC reflection tutorial (11.7 seconds) and
Common Core Module 16 (15.7 seconds). Existing static unit-normal POPC views
remain valid and are embedded through the maintained notebook protocol. The
Cookbook includes an independent x=3 nm selected-population reflection/inverse;
its code and the course's tagged reflection cell are executed by documentation
guards. The public reflection doctest passes in 7.76 seconds.

A first draft used strings containing nan/inf to reach the finite-point guard;
the configured literal parser refuses those strings before geometry. The shared
point parser now translates that refusal consistently, and separate real
quantities exercise nonfinite/complex point admission directly. No provider
parser capability or third-party scientific equivalence is assumed.

The local broad command is:

```bash
MPLBACKEND=Agg python -m pytest tests/structure tests/pbc \
  tests/scientific_truth/structure tests/_private/argdigest \
  tests/build/remove_overlapping_molecules \
  tests/documentation/test_move_away_examples.py \
  tests/molsysviewer_molsysmt/test_structure_transform_tools.py \
  tests/molsysviewer_molsysmt/test_structure_move_away_tools.py \
  -m 'not network' --receptor=llm -n 12
```

An initial broad checkpoint passes 2,368 cases in 47.94 seconds; the final run
also includes direct complex-point refusal. Warnings retain legacy H5MSM,
deliberately unavailable GPU fallback, deliberate tiny-memory-budget pressure,
an existing invalid-rotation determinant and one structural attribute drop.
No actual GPU or full supported-platform qualification is claimed.

The working tree also contains independent principal-axis addon receiving.
That work is preserved and excluded from this repair's commit. Source regression
observations do not replace exact committed-head CI or clean installed-package
qualification. Public dependency floors, synchronized guides, release refs,
packages and publication authorization remain unchanged.


## Final local verification — 2026-10-25

The final broad run passes **2,369 tests in 47.80 seconds**, without failures
or omissions, with the same 644 warning categories described above. Ruff lint
and formatting, all 251 public docstring checks and all fourteen fast release
gates pass. Sphinx HTML builds successfully; the existing warning debt remains
uibcdf/molsysmt#144, including the course's mandated heading hierarchy and old
tutorial admonition formatting. No warning-free build is claimed. The native
reflection guard is included in the bounded smoke tier.
