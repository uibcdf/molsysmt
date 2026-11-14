---
summary: Selection expression evaluation wraps resource failures as argument errors.
issue: uibcdf/molsysmt#756
status: open
opened: 2026-11-14
closed:
severity: medium
verification: inspected
area: [basic, selection]
guard:
normative:
blocked_by: []
supersedes: []
---

# Selection mistakes resource exhaustion for invalid input

**Reported:** 2026-11-14 by BindingMT during its fixed native selection-snapshot work.
**Status:** admitted after #754; owner reproduction and correction pending.

## What

BindingMT reports that public `msm.select` wraps injected `MemoryError` and
`OSError(errno.ENOMEM)` in `ArgumentError`. The original resource exception
remains its cause, but its type and identity no longer reach the consumer.
`KeyboardInterrupt` and `SystemExit` already propagate unchanged. The exact
consumer source/native identity and synthetic reproducer are in #756; this
owner record does not relabel that upstream run as local execution.

## How

Inspection confirms the shared expression-evaluation try/except in
`molsysmt/basic/select.py` preserves ArgumentError/CatalogException and wraps
other Exception instances. Preserve the original object with a bare raise
for MemoryError and only the ENOMEM case of OSError. Keep ordinary parser
exceptions, their causes and provider/catalog argument diagnostics intact.
Exercise the real public boundary with normal digestion, all applicable
syntax dispatches and any affected direct inventory/bond evaluation paths.
Private backend injection is test instrumentation, never a consumer workaround.

## Why

Capacity failure is not evidence of invalid selection input. Client error
handling and shared-resource disposition need the real exception identity;
consumers should not unwrap causes or add competing selectors.

## What is measured and what is assumed

The handler is locally inspected. Synthetic reproduction is upstream-reported
and will be repeated by the owner with one atom. No real memory exhaustion,
large allocation, native build, installation or held client campaign is needed.

## Scope and exclusions

Correct exception propagation and its public diagnostics/guards. Do not change
selection syntax, numerical results, units, ordering, chemistry or provider
floors. Preserve the separate client receiving and final-pair requirements.

## Acceptance criteria

- Real public calls preserve the same MemoryError and OS ENOMEM objects.
- Other OSError/parser failures retain ArgumentError and their original cause.
- Catalog/provider argument errors and process-control exceptions still propagate.
- Focused tests use synthetic failures without allocation pressure; applicable
  documentation and local quality checks pass.
