---
summary: Single-precision configuration sends float32 coordinates to float64-only Rust CPU kernels.
issue: uibcdf/molsysmt#620
status: resolved
opened: 2026-11-06
closed: 2026-11-06
severity: high
verification: reproduced
area: [structure]
guard: tests/structure/test_native_precision_policy.py
normative: devguide/performance_and_jit.md
blocked_by: []
supersedes: []
---

# CPU precision request and kernel input mismatch

## What

With `configure.context(precision='single')`, public distances fail with
`TypeError: 'ndarray' object is not an instance of 'ndarray'` while processing
coordinates. Shared geometry extraction prepares float32, but the bundled Rust
CPU kernels require float64. The same finite two-atom system succeeds under
the default double policy. This also reproduces serially, independently of #613.

## How

```python
import molsysmt as msm
from molsysmt.native import Structures

molsys = Structures(coordinates=msm.pyunitwizard.quantity(
    [[[0.0, 0.0, 0.0], [1.0, 0.0, 0.0]]], 'nm'))
with msm.configure.context(precision='single'):
    msm.structure.get_distances(molsys, pbc=False, parallel=False)
```

The failure occurs on public source `16ecaae01c4b670ef3a38ce595362b83e172cc69`
with the phase-two extension built from the delivered Rust source. Linux/Python
3.14.7, existing development environment. Integer/float input controls both pass
under double precision; the global precision policy causes the mismatch.
`molsysmt/lib/structure/_kernel_inputs.py` selects float32 in both extraction
and alignment helpers. The actual kernel signature accepts float64 only.

## Why and acceptance

Define the existing CPU precision boundary and enforce it before an opaque
native conversion error. Preserve physical values, units, source independence,
and eager/chunked semantics across affected consumers. Either implement an
already supported precision contract faithfully or reject the unsupported
request clearly; do not silently pretend float64 execution is single precision.
This does not require a new float32/GPU backend for 1.0.

Add a maintained public regression for the reproduced setting and supported
double controls. Record the diagnostic/compatibility decision, complete the
affected documentation lifecycle and qualify the shared helper's consumers.
At initial reporting, no runtime repair had been made.

## Provenance

Found while adding actual decorated-call receiving for #613. Its initial
counterexample XML retains this independent failure. A separate serial probe
isolates it from thread scheduling. The complete seven-page inventory before
filing contains 551 issues, 98 open, and no equivalent precision-setting report.
The issue is admitted under #334's included-profile correctness rule; it changes
neither the phase weights nor publication authorization.

## Maintainer decision and correction — 2026-11-06

The maintainer selects preserving already implemented single-coordinate outputs
and diagnosing effective float64 native computation, rather than rejecting that
publication capability. The shared preparation boundary now retains float64
working values instead of quantizing before the CPU binding. The canonical
chunked route makes the same effective-precision declaration. An internal dtype
resolver reuses the existing precision digester and a typed SMonitor diagnostic,
`MSM-WARN-PRECISION-001`, with requested/effective/backend fields. It neither
introduces another kernel nor changes configuration behind the caller's back.

Fitting/alignment retain final single-coordinate quantization. Native storage
remains float64; a plain quantity output can retain float32 magnitudes. These
are separately documented policies, not a claim that all output forms use the
same dtype or that native RAM is halved. The User Guide's old float32-default
and absolute sub-picometer assertions are corrected against actual native and
CPU contracts. Input units and the chosen application unit standard remain
owned by PyUnitWizard.

Original directed receiving has 21 failures and two passing controls: eager
distances hit the dtype error; heavy distances and existing fit outputs omit an
effective-precision diagnostic. The first corrected diagnostic/serialization/
configuration profile passes 297 cases. Expanded public receiving passes 39
cases, covering independent non-float32-representable distance truth, units,
eager/chunked paths, two-input alignment, shared-consumer parity, SASA, torsion
editing, supported fitted outputs, no-extra-dtype-copy controls and warning-as-
error atomicity. Parity is not independent scientific validation; final broader
receiving, documentation, exact source publication and closeout remain pending.

The maintainer also renews the #334 development route: working commits carry
`[skip ci]`, direct pushes are batched, and remote CI is reserved for deliberately
agreed qualification checkpoints. This is recorded in root AGENTS.md; it waives
no exact-candidate release gate. Existing CI is observed without dispatching a
replacement merely to inspect it.

## Final local receiving — 2026-11-06

Implementation `cb07e54af2a9be545b36d3fe8c64de34e0a0b132` preserves the
maintainer-selected compatibility behavior. Joint receiving with the #524
renderer declaration passes 4,592 cases without failures, errors or skips.
The affected documentation/public-doctest profile passes 599 cases. Registered
scientific execution passes 97 cases across 64 nodes without omissions. These
profiles overlap and do not qualify every operation under every precision
setting. The directed guard distinguishes independent numerical truth from
shared-consumer parity.

The [receiving receipt](../../../devtools/data/native_precision_receiving_620_20261106.json)
binds all 21 implementation/test/documentation files, exact backend, native
process exits, commands, original counterexamples, retained warnings and
documentation preservation. The seven changed notebooks retain their code,
outputs, cell IDs and metadata. Four human autosummary edits and the native
extension remain unchanged. An initial fast-gate run correctly rejects a stale
generated report index; the owning generator repairs it before final lifecycle
validation. No diagnostic is suppressed.

Final lifecycle receiving passes all fourteen fast gates, including developer-
guide integrity, and the generated queue-index check. These are local source
checks rather than the full matrix or installed-candidate qualification.

The scientific certificate correctly identifies pre-commit dirty development
source and is not release-eligible. No environment or backend is replaced and
no new remote workflow is dispatched. Public delivery and issue closure follow
independent source retrieval. Remaining #524 work still prevents phase-three
credit; accepted overall plan progress remains 40%.
