---
summary: Native add rejects valid keep_ids flags during argument digestion
issue: uibcdf/molsysmt#356
status: resolved
opened: 2026-10-09
closed: 2026-10-09
severity: medium
verification: reproduced
area: [argdigest, native]
guard: tests/native/test_native_add_digestion.py::test_native_add_accepts_boolean_keep_ids
normative:
blocked_by: []
supersedes: []
---

# Native add rejects valid keep_ids flags

**Reported:** 2026-10-09 during #353/#354 stabilization.
**Status:** Resolved; native public addition recognizes its boolean argument contract.

## What

Both public native `Topology.add` and `MolSys.add` reject their documented
boolean `keep_ids` values, including the default. The form-agnostic `msm.add`
wrapper succeeds through controlled delegation, so its success did not protect
the direct native boundary.

```python
from molsysmt.native import Topology
Topology().add(Topology())
# ArgumentError: Error in argument 'keep_ids' with value 'True'.
```

Bundled alanine controls reproduce this for complete systems too: twelve valid
combinations of native class, default/True/False and full/selected atom inventory
fail before addition; eight invalid boolean controls are correctly rejected.

## How

The private `keep_ids` digester accepts callers ending in `add.add`/`merge.merge`
but omits native method owners. ArgDigest reports methods using their runtime
class's module plus method name: `molsysmt.native.topology.add` and
`molsysmt.native.molsys.add`. Accept those two existing boolean-bearing callers
while preserving rejection of non-booleans and unsupported caller contexts.
No provider ArgDigest change, validation bypass or wider generic suffix is needed.

## Why

These are decorated public native methods, not private helpers. An ordinary
caller should not need trusted-delegation flags to use their documented inputs.
The older direct native tests used `skip_digestion=True`; the public wrapper
validated first. Neither exercised the affected native boundary. New tests call
that boundary normally, and the #353 metadata test is upgraded to do so too.

## Evidence and exclusions

Before fix: `python -m pytest tests/native/test_native_add_digestion.py
--receptor=llm -n12` obtains **12 failed, 8 passed**. Failures are the valid flags;
invalid values fail as required before molecular mutation.
Linux, Python 3.14.7, ArgDigest `0.15.0+1.g5c6711e`, source `dfdb31489`, shared
development environment and preserved Rust extension. Full and selected direct
native calls, string chain IDs, source preservation and coordinate-axis alignment
are tested. No new addition mode, chemical-state alignment policy or argument
coercion is introduced. Release/publication remains paused.

## Acceptance

- Default/True/False works at both native public boundaries with digestion enabled.
- Full/nonmonotonic subsets retain the intended chain/index/atom semantics.
- Integer/string/None substitutes are rejected before target mutation.
- Existing public wrapper and topology-operation regressions remain passing.
- Native docstrings, Foundations, Toolbox, Cookbook and course agree with the contract.

## Resolution — 2026-10-09

The existing private argument digester now recognizes both native method owners.
The accepted type remains exactly `bool`; no generic caller wildcard or bypass
is introduced. Existing #353 native metadata assertions now execute with normal
digestion, and additional source-preservation controls cover both classes and
nonmonotonic selection.

`python -m pytest tests/native/test_native_add_digestion.py tests/basic/add
 tests/native/test_topology_operations.py --receptor=llm -n12`:
**115 passed**. All twenty direct native controls pass, including eight invalid
values rejected before mutation. The guard's valid default/explicit flags failed
on the original source and now assert real addition plus labels/index alignment.

`python -m pytest molsysmt/basic/add.py molsysmt/native/topology.py
 molsysmt/native/molsys.py --doctest-modules --receptor=llm -n12`:
**3 passed**. Affected public guidance documents normal native calls without
requiring trusted delegation; notebook code and outputs are unchanged.
These are bounded source results, not qualification of replacement artifacts.
