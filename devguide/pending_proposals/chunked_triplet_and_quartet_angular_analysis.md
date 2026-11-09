---
summary: Bound native triplet and quartet angular analysis with chunked execution
issue: uibcdf/molsysmt#667
status: open
opened: 2026-11-09
closed:
verification: inspected
area: [structure, performance]
guard:
normative:
blocked_by: []
supersedes: []
---

# Chunked native angular observations

**Scope:** Post-1.0 follow-up, not another pre-1.0 acceptance exit.

## What

get_angles and the explicit-quartet get_dihedral_angles path currently gather
all requested participating coordinates and return a complete resident array.
The source-inspected limitation is explicit in native/GUI documentation. A
fifty-row frontend page does not bound that native calculation. No unsafe
large-system stress run or measured universal failure is claimed.

## How

Reuse ChunkedExecutor and existing Rust kernels at the native scientific owner.
Keep structure order/repetitions, global tuple indices, roles, row-vector boxes,
native undefined observations and application-owned angle units. Admit resource
and work requirements before expensive materialization. Receive empty axes,
chunk boundaries and persistent-output lifetime as in other geometry APIs.
Do not add a GUI-local scientific implementation, competing result store,
placeholder public API, new detector or format.

## Why

The immediate related consumer is MolSysViewer's #421 explicit angular tasks;
Python clients also benefit from general native tools. Current eager behavior
is documented and retained. This extension belongs in reusable native geometry
and its general execution machinery, rather than a special viewer pipeline.

## Acceptance criteria

Compare analytic and native-path results across ordinary/trusted calls,
nondefault units, nonconsecutive/repeated structures, tuple order/repetition,
zero/undefined observations, PBC and chunk boundaries. Measure input delivery,
numeric work, output/RSS and cleanup under enforced conservative resource
limits. Keep caller/object overhead and installed/platform claims separate.
Large-scale performance claims require their own evidence. There is no
commitment to a new dependency, schema or pre-1.0 scope expansion.
