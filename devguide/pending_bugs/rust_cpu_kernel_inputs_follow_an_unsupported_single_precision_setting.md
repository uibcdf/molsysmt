---
summary: Single-precision configuration sends float32 coordinates to float64-only Rust CPU kernels.
issue: uibcdf/molsysmt#620
status: open
opened: 2026-11-06
closed:
severity: high
verification: reproduced
area: [structure]
guard:
normative:
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
Implementation remains pending; no runtime repair is claimed by this report.

## Provenance

Found while adding actual decorated-call receiving for #613. Its initial
counterexample XML retains this independent failure. A separate serial probe
isolates it from thread scheduling. The complete seven-page inventory before
filing contains 551 issues, 98 open, and no equivalent precision-setting report.
The issue is admitted under #334's included-profile correctness rule; it changes
neither the phase weights nor publication authorization.
