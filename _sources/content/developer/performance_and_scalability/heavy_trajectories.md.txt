# Heavy trajectory infrastructure

This page describes the internal architecture for out-of-core (chunked) trajectory processing.
Read it if you want to:

- add heavy-mode support to a new form,
- implement a new analysis function that supports the heavy path,
- write a custom `Reducer`, or
- understand the execution flow for debugging.

The canonical design document is `devguide/SCALABILITY.md`.

---

## Architecture overview

The heavy path is built around three components:

```
ChunkedExecutor
  │
  ├── form.StructuresIterator  ← reads the trajectory in chunks
  │
  └── Reducer(s)               ← accumulate partial results per chunk
```

`ChunkedExecutor` owns the orchestration loop. It does not contain any scientific logic. It:

1. estimates the memory footprint and decides eager vs. heavy;
2. validates that the form supports the requested attributes in heavy mode;
3. initialises each reducer (possibly creating a `PersistentResultHandle` for large outputs);
4. iterates chunks from the form's `StructuresIterator`;
5. feeds each chunk to all reducers;
6. saves checkpoints at configurable intervals;
7. emits SMonitor telemetry at each step.

Chunk processing is fail-fast. Exceptions from the iterator, chunk
normalization, or a reducer propagate to the caller, and the executor does not
finalize or return partial results. There is no implicit corrupt-frame skipping
policy.

---

## The `Reducer` ABC

Every heavy-mode analysis function defines a private `Reducer` subclass.
The base class is `molsysmt._private.execution.Reducer`.

### Mandatory interface

```python
from molsysmt._private.execution import Reducer

class MyReducer(Reducer):

    def initialize(self, metadata: dict) -> None:
        """Called once before the chunk loop. Reset all accumulation state here."""

    def consume(self, chunk: dict) -> None:
        """Called once per chunk. chunk is read-only. Copy before mutating."""

    def finalize(self):
        """Called once after all chunks. Return the final result."""
```

### `metadata` keys (passed to `initialize`)

| Key | Type | Description |
|---|---|---|
| `n_atoms` | int | atoms selected (after atom_indices filtering) |
| `n_structures` | int | frames to be processed by this executor |
| `n_structures_total` | int | total frames in the source system |
| `n_chunks` | int | number of chunks that will be delivered |
| `operation` | str | name of the calling operation |
| `form` | str | form name string |
| `atom_indices` | array or 'all' | atom selection |
| `structure_indices` | array or None | frame selection |
| `output_handle` | PersistentResultHandle or absent | present only when `estimate_output_shape` returned a shape |

### `chunk` keys (passed to `consume`)

| Key | Type | Description |
|---|---|---|
| `coordinates` | np.ndarray float64, nm | shape `(n_chunk, n_atoms, 3)`, **read-only** |
| `box` | np.ndarray float64, nm or `None` | shape `(n_chunk, 3, 3)` |
| `time` | np.ndarray float64, ps or `None` | shape `(n_chunk,)` |
| `structure_indices` | np.ndarray int or `None` | global frame indices |

### Optional extensions

Override these to enable additional features:

```python
def estimate_output_shape(self, metadata: dict):
    """
    Return the shape (tuple) of the final output array.
    ChunkedExecutor will call check_disk_budget(), create a PersistentResultHandle,
    and pass it as metadata['output_handle'] to initialize().
    Return None (default) to always accumulate in RAM.
    """
    return None

def checkpoint(self) -> dict | None:
    """
    Return a serializable state dict (will be pickled by ChunkedExecutor).
    Return None (default) if checkpointing is not supported.
    """
    return None

def restore(self, state: dict) -> None:
    """
    Restore accumulated state from a checkpoint dict.
    Called before the chunk loop when restore_from is set.
    initialize() is NOT called when restoring — state comes from here.
    Raises NotImplementedError by default.
    """
    raise NotImplementedError(...)

def merge(self, other: Reducer) -> None:
    """
    Merge another reducer's partial state into self (earlier frames first).
    Used for parallel reduction: run N executors on N trajectory segments,
    then merge in temporal order.
    Raises NotImplementedError by default.
    """
    raise NotImplementedError(...)
```

### Minimal example

```python
import numpy as np
from molsysmt._private.execution import Reducer

class MeanCoordinatesReducer(Reducer):
    """Computes the per-atom mean position over all frames."""

    def initialize(self, metadata):
        self._sum = np.zeros((metadata['n_atoms'], 3), dtype=np.float64)
        self._count = 0

    def consume(self, chunk):
        coords = np.array(chunk['coordinates'], dtype=np.float64)  # writable copy
        self._sum += coords.sum(axis=0)
        self._count += coords.shape[0]

    def finalize(self):
        return self._sum / self._count

    def checkpoint(self):
        return {'sum': self._sum.tolist(), 'count': self._count}

    def restore(self, state):
        self._sum = np.array(state['sum'], dtype=np.float64)
        self._count = state['count']

    def merge(self, other):
        self._sum += other._sum
        self._count += other._count
```

---

## `ChunkedExecutor` usage

```python
from molsysmt._private.execution import ChunkedExecutor

executor = ChunkedExecutor(
    molecular_system=molsys,
    form='molsysmt.H5MSMFileHandler',
    operation='my_operation',
    reducer=my_reducer,            # single reducer → execute() returns one result
    # reducers=[r1, r2],           # multiple reducers → execute() returns list
    atom_indices=atom_indices,
    structure_indices=None,        # None means 'all'
    chunk_size=500,
    heavy_mode='force',            # 'auto' | 'force' | 'off'
    attributes=['coordinates'],    # attributes to request per chunk (see below)
    # -- checkpoint / resume --
    checkpoint_interval=10,        # save checkpoint every 10 chunks (0 = disabled)
    checkpoint_path='/tmp/ckpts/', # directory or file path
    restore_from=None,             # path to a .pkl checkpoint to resume from
    # -- user-controlled output path --
    output_path=None,              # if set, PersistentResultHandle writes here (not deleted on cleanup)
)
result = executor.execute()
```

### The `attributes` parameter

`attributes` controls which data fields are requested from the `StructuresIterator` per chunk.
The default is `['coordinates']`. Add `'box'` when the operation needs periodic boundary
conditions (PBC), and `'time'` when the reducer needs timestamps:

```python
# Distances with PBC: need box vectors per chunk
executor = ChunkedExecutor(..., attributes=['coordinates', 'box'])

# Custom reducer that also needs frame timestamps
executor = ChunkedExecutor(..., attributes=['coordinates', 'time'])
```

`execute()` validates that every requested attribute appears as `True` in the form's
`_heavy_support` dict before starting. If any attribute is unsupported,
`UnsupportedHeavyOperationError` is raised immediately.

### Multi-reducer (read-once, analyze-many)

Pass `reducers=[r1, r2, ...]` to run multiple analyses in a single trajectory pass.
`execute()` returns a list of results in the same order:

```python
executor = ChunkedExecutor(
    ...,
    reducers=[center_reducer, rmsd_reducer],
)
center_result, rmsd_result = executor.execute()
```

### Checkpoint / resume

```python
# First run — save a checkpoint every 20 chunks
executor = ChunkedExecutor(
    ...,
    checkpoint_interval=20,
    checkpoint_path='/tmp/run1/',
)
result = executor.execute()

# If interrupted, resume from the last checkpoint
import os, glob
last_ckpt = sorted(glob.glob('/tmp/run1/*.pkl'))[-1]

executor2 = ChunkedExecutor(
    ...,
    restore_from=last_ckpt,
)
result = executor2.execute()
```

The reducer's `restore()` is called before the chunk loop. `initialize()` is skipped.
The executor automatically computes which frames were already processed and skips them.

### User-controlled output path

When `output_path` is set, the `PersistentResultHandle` created for a large-output reducer writes
to that path instead of a system temporary file. The file is **not** deleted by `cleanup()`,
giving the caller full lifecycle control:

```python
executor = ChunkedExecutor(
    ...,
    output_path='/scratch/distances.dat',
)
result = executor.execute()
# result is a PersistentResultHandle backed by /scratch/distances.dat
# The file persists after result.cleanup() or when the handle goes out of scope.
```

This is forwarded directly to `PersistentResultHandle(shape, path=output_path)`.

### Parallel reduction via `merge()`

```python
# Process two halves independently
r1 = MyReducer()
ChunkedExecutor(..., reducer=r1, structure_indices=list(range(0, 2500))).execute()

r2 = MyReducer()
ChunkedExecutor(..., reducer=r2, structure_indices=list(range(2500, 5000))).execute()

# Merge in temporal order (earlier frames first)
r1.merge(r2)
result = r1.finalize()
```

---

## Adding heavy support to a form

Two things are required:

### 1. Declare `_heavy_support`

In the form's `__init__.py`, add a module-level dict listing every attribute the form's
`StructuresIterator` can deliver in a chunk:

```python
_heavy_support = {
    'coordinates': True,
    'box': True,     # set True only if the iterator can yield box vectors per chunk
    # 'time': True,  # add if time is available
}
```

`ChunkedExecutor.execute()` reads this dict before starting. If a requested attribute is not
listed as `True`, it raises `UnsupportedHeavyOperationError`.

`box` support matters for PBC-aware operations (e.g. `get_distances(pbc=True)`). All current
heavy-mode forms (`file:h5msm`, `molsysmt.H5MSMFileHandler`, `file:xtc`) declare both
`'coordinates'` and `'box'` as `True`.

### 2. Implement `StructuresIterator`

The form module must export a `StructuresIterator` class that is a context manager and a
Python iterator. Minimum signature:

```python
class StructuresIterator:
    def __init__(self, molecular_system, atom_indices='all',
                 structure_indices=None, chunk=1,
                 output_type='dictionary', skip_digestion=True,
                 coordinates=True, box=False, time=False, **kwargs):
        ...

    def __iter__(self):
        return self

    def __next__(self) -> dict:
        """
        Return one chunk as a dict with keys:
          'coordinates', 'box', 'time', 'structure_id'
        where 'coordinates' is a puw quantity (nm) and 'box' is nm.
        Raise StopIteration when exhausted.
        """
        ...

    def __enter__(self):
        return self

    def __exit__(self, *args):
        # Close resources owned by this iterator.
        # Do NOT close a molecular system passed in from outside.
        ...
```

`ChunkedExecutor` calls `_build_chunk()` on the raw dict returned by `__next__()` to
strip units and produce a canonical float64 chunk.

---

## SMonitor event codes

| Code | Name | Trigger |
|---|---|---|
| `MSM-INFO-HVY-001` | `HeavyPathSelected` | heavy mode activated |
| `MSM-INFO-HVY-002` | `EagerPathAccepted` | footprint within budget |
| `MSM-INFO-HVY-003` | `ChunkProcessed` | after each successful chunk |
| `MSM-WARN-HVY-001` | `SlowChunkIOWarning` | chunk I/O > 5 s |
| `MSM-WARN-HVY-003` | `MemoryPressureWarning` | RSS > `memory_pressure_threshold × max_ram_usage` |
| `MSM-ERROR-HVY-001` | `UnsupportedHeavyOperationError` | form/attribute not supported |
| `MSM-ERROR-HVY-002` | `HeavyOutputFailureError` | disk budget exceeded |

All codes are registered in `molsysmt/_private/smonitor/catalog.py`.

**ETA computation.** The `eta_s` field in `ChunkProcessed` is computed via an exponential moving
average (EMA, α = 0.3) of per-chunk elapsed times, so it adapts continuously as I/O speed changes
over the run rather than relying only on the first-chunk measurement.

**Memory pressure.** `MemoryPressureWarning` is emitted after each chunk when
`psutil.Process().memory_info().rss > molsysmt.configure.memory_pressure_threshold × max_ram_usage`.
The check is silently skipped if `psutil` is not installed. Threshold is configurable:
`molsysmt.configure.memory_pressure_threshold` (default `0.80`).

---

## Relevant source files

| File | Role |
|---|---|
| `molsysmt/_private/execution/chunked_executor.py` | Orchestration loop |
| `molsysmt/_private/execution/reducer.py` | `Reducer` ABC |
| `molsysmt/_private/execution/memory_policy.py` | Footprint estimate, decide_mode, check_disk_budget |
| `molsysmt/_private/execution/persistent_result.py` | `PersistentResultHandle` |
| `molsysmt/structure/get_center.py` | `_CenterReducer` |
| `molsysmt/structure/get_rmsd.py` | `_RMSDReducer` |
| `molsysmt/structure/get_distances.py` | `_DistancesReducer` |
| `molsysmt/form/molsysmt_H5MSMFileHandler/iterators.py` | Reference `StructuresIterator` (H5MSM handler) |
| `molsysmt/form/file_h5msm/iterators.py` | File-path iterator (delegates to handler, owns lifecycle) |
| `molsysmt/form/file_xtc/iterators.py` | XTC iterator (delegates to `mdtraj.XTCTrajectoryFile`) |
| `tests/heavy/` | All heavy-mode tests |
