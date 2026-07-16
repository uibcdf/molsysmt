# Atom-Type Inference Uses `print` and a Broad Exception

**Status:** resolved 2026-07-13

**Severity:** medium — diagnostics and developer traceability

## Evidence

`molsysmt/element/atom/get_atom_type_from_atom_name.py` catches `Exception` around
a dictionary lookup, prints directly to standard output, and returns `"UNK"`.

## Why this is a defect

- A missing mapping should catch `KeyError`, not unrelated programming errors.
- Direct printing bypasses the SMonitor diagnostic catalog and profile controls.
- Library output can pollute notebooks, command pipelines, and batch workflows.
- Returning `"UNK"` may be a valid compatibility policy, but it must be paired
  with a structured, testable diagnostic.

## Proposed correction

1. Catch `KeyError` only.
2. Emit a catalogued recoverable warning with the unrecognized atom name.
3. Preserve the current `"UNK"` return unless the public compatibility policy is
   deliberately changed.
4. Add tests for the known-name path, unknown-name path, diagnostic payload, and
   propagation of unexpected exceptions.

## Acceptance criteria

- No direct `print` occurs.
- Unknown names return the documented fallback and emit the catalogued signal.
- Unrelated internal errors are not swallowed.

## Resolution

The lookup now catches `KeyError` only. Unknown names return `"UNK"` and emit
the catalogued `UnknownAtomNameWarning`; unexpected mapping failures propagate.
Regression tests also prove that no text is printed to standard output.
