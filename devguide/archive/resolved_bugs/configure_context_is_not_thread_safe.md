# Configuration Context Was Not Thread-Safe

**Status:** resolved 2026-07-18

## Original problem

`molsysmt.configure.configure_context` and `with_configure_overrides` described
their behavior as thread-safe while mutating shared module attributes without
coordination. Overlapping contexts could observe and restore each other's
values. Unknown configuration names were also created as module attributes and
were not removed on exit.

## Decision

MolSysMT configuration remains explicitly process-global for 1.0. Context-local
overrides were rejected for this release because kernels, execution policies,
and public code read module attributes directly. Retrofitting `contextvars`
would require a broad accessor or module-proxy migration and still would not by
itself settle Numba runtime behavior.

Configuration context writers are now serialized for their full lifetime with
a reentrant lock. Nested contexts in one thread remain supported. This prevents
snapshot and restoration races but deliberately does not promise isolation:
code running concurrently outside the context can observe temporary values.
Direct module assignments remain process-global and do not acquire the context
lock.

## Resolution

- synchronize overlapping contexts with a module-private `RLock`;
- restore values and release the lock after normal or exceptional exits;
- synchronize the `gpu_mode` and `use_gpu` compatibility aliases;
- reject absent, private, or callable configuration names;
- bypass the context entirely when a decorated call has no effective overrides;
- replace thread-safety claims with the process-global serialization contract;
- cover nested contexts, exceptions, invalid keys, aliases, and deterministic
  overlap between two threads.

## Separate follow-up boundary

Concurrent lazy Numba compilation and Numba thread masking remain an independent
operational audit. Configuration serialization is not evidence for either
behavior.
