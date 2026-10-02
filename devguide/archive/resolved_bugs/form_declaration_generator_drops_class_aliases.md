---
summary: Form declaration generator drops registered class aliases
issue: uibcdf/molsysmt#294
status: resolved
opened: 2026-10-02
closed: 2026-10-02
severity: medium
verification: reproduced
area: [form, devtools]
guard: devtools/tests/test_generate_form_declarations.py::test_regeneration_preserves_viewer_class_recognition
normative:
blocked_by: []
supersedes: []
---

# Form declaration generator drops registered class aliases

**Reported:** 2026-10-02 during native SDF form registration.
**Status:** Resolved; the generator retains adapter-owned aliases, and runtime
recognition through regenerated metadata is regression-tested.

## What

`generate_form_declarations.py --check` reports semantic drift for the viewer
adapter. Its `declaration()` result lacks `item_class_keys`, so `--write` would
erase the registered `IframeMarkup` alias. Four native declarations also differ
in JSON formatting only; their parsed values are identical.

## How

The generator derives only one primary class key from the form name. The viewer
adapter now owns explicit string class-key aliases, and the generic generator
retains that metadata without importing optional viewer classes. Generated
declarations are refreshed through the normal command.

## Why

Registering a new form must not undo existing class recognition. The affected
consumer is MolSysViewer. This is a tooling defect rather than an SDF scientific
limitation, and it has its own owning issue.

## Evidence and regression

The previous generated result was compared with parsed shipped JSON and lacked
the alias. `devtools/tests/test_generate_form_declarations.py` writes the real
generated declaration into an isolated catalogue and verifies runtime recognition
of both `MolSysView` and `IframeMarkup`. Omitting the aliases again makes the
second lookup fail. No production catalogue is changed by the test.

**Contract-tested:** The generator regression and existing viewer extraction
tests pass (4 tests). `generate_form_declarations.py --check` confirms that all
94 declarations match their modules after regeneration.

## Scope

Explicit adapter-owned alias metadata and its generation/recognition regression.
No scientific data or viewer rendering behavior changes.
