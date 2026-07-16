# Scalability and Heavy-Trajectory Contract

MolSysMT contains an internal chunked-execution framework for trajectories that
should not be loaded into memory at once. This document describes the current
contract, not the complete pre-1.0 design history, which is archived under
`archive/assessments/`.

## Current public scope

The public heavy path is currently integrated into these structure operations:

- `molsysmt.structure.get_center`;
- `molsysmt.structure.get_rmsd`;
- `molsysmt.structure.get_distances`.

Eligibility is narrower than the full eager API. It depends on the operation,
selection shape, comparison mode, output, and whether the input form advertises
the required attributes in `_heavy_support`. Unsupported combinations must use
the eager path or fail explicitly; they must not be described as generally
out-of-core capable.

## Decision policy

`molsysmt._private.execution.memory_policy` estimates the coordinate footprint
from atom and structure counts. `heavy_mode` controls the decision:

- `"auto"`: select heavy execution when the estimated footprint exceeds the
  configured RAM budget;
- `"force"`: request heavy execution;
- `"off"`: use eager execution.

`max_ram_usage`, `chunk_size`, `chunk_memory_fraction`, and
`memory_pressure_threshold` configure the policy. The footprint is an estimate,
not a complete peak-memory proof; reducers and outputs may dominate memory use.

## Chunk contract

`ChunkedExecutor` obtains chunks from a form-specific `StructuresIterator` and
builds dictionaries with these keys:

- `coordinates`: read-only `float64` values in nm;
- `box`: read-only `float64` values in nm, or `None`;
- `time`: read-only `float64` values in ps, or `None`;
- `structure_indices`: read-only structure identifiers or `None`.

Reducers must copy an array before mutating it. Scientific logic belongs in the
reducer; the executor owns iteration, policy, and orchestration.

## Reducer protocol

Every reducer implements `initialize(metadata)`, `consume(chunk)`, and
`finalize()`. The following hooks are optional and must be assessed per reducer:

- `estimate_output_shape(metadata)` for disk-backed output allocation;
- `checkpoint()` and `restore(state)` for resumability;
- `merge(other)` for combining independently accumulated state.

The presence of these methods on the base class does not guarantee support.
Their defaults return no checkpoint or raise `NotImplementedError`. In
particular, the distance reducer cannot restore or merge disk-backed state
across process invocations.

The executor is sequential. `merge()` provides a reducer protocol that a future
parallel orchestrator may use; it does not make `ChunkedExecutor` itself a
parallel trajectory engine.

## Persistent results

`PersistentResultHandle` is a NumPy-memmap-backed array-like result. A temporary
backing file is deleted by `cleanup()`; a caller-provided path remains under
caller control. Disk-backed delivery is operation- and size-dependent. It is not
a general return type for every heavy operation.

Callers receiving a handle must manage its lifecycle explicitly and avoid
calling `to_memory()` unless the complete output fits in RAM.

## Failure integrity

Scientific exceptions must not be converted into silent data loss.
`ChunkedExecutor` is fail-fast: exceptions raised by an iterator, chunk
normalization, or `Reducer.consume()` propagate to the caller. The executor does
not return finalized partial results after such a failure. Corrupt-input
recovery is not currently part of the heavy-execution contract; adding it would
require an explicit policy, exact frame provenance, and alignment tests.

Checkpoint files use Python pickle and are trusted local artifacts, not safe
interchange files. Never restore a checkpoint from an untrusted source.

## Evidence required for a heavy-capability claim

For each operation/form combination, tests must cover:

1. eager versus chunked numerical parity, units, shape, and ordering;
2. non-contiguous `structure_indices` and atom selections;
3. first, final, and partial chunks;
4. relevant PBC behavior;
5. unsupported combinations and explicit failures;
6. cleanup and disk-budget behavior for persistent results;
7. checkpoint/restore or merge only when the reducer implements them;
8. propagation of scientific exceptions without partial-success results.

Framework tests with synthetic reducers demonstrate the protocol but do not
certify every public reducer or input form.

## Extension rule

New heavy operations should reuse `ChunkedExecutor` and `Reducer`, declare the
required form attributes, and add operation-level parity tests. Do not expose a
public `heavy_mode` parameter before the complete eligible and ineligible API
surface is defined and tested.
