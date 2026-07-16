# Heavy Executor Fail-Fast Resolution

**Status:** resolved 2026-07-13

## Original defect

`ChunkedExecutor._execute_heavy()` wrapped chunk normalization and every
`reducer.consume()` call in `except Exception`. It emitted
`CorruptFrameSkippedWarning` and continued with the next chunk.

An algorithm error, unit error, shape defect, out-of-memory condition, or bug in
one reducer was therefore treated as corrupt input. The returned result could
omit an entire chunk while appearing successful. With multiple reducers,
earlier reducers could already have consumed the chunk before a later reducer
failed, leaving their states inconsistent.

## Resolution

Heavy execution is now fail-fast. Exceptions from iteration, chunk
normalization, and reducer consumption propagate to the caller. Reducers are
not finalized after those failures, so the executor cannot return a
partial-success result.

Implicit corrupt-frame skipping and `CorruptFrameSkippedWarning` were removed.
Any future recovery mode requires an explicit policy, exact frame provenance,
output masks or indices, and alignment tests.

## Evidence

Focused tests verify that reducer and normalization exceptions propagate and
that no reducer is finalized. The maintained contract is in
`devguide/SCALABILITY.md`.
