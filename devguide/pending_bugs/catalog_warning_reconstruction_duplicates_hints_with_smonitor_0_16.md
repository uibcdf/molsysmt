---
summary: Catalog warning reconstruction duplicates hints with SMonitor 0.16
issue: uibcdf/molsysmt#236
status: blocked
opened: 2026-09-22
closed:
severity: medium
verification: measured
area: [tests, diagnostics]
guard:
normative:
blocked_by: [uibcdf/smonitor#21]
supersedes: []
---

# Catalog warning reconstruction duplicates hints with SMonitor 0.16

**Reported:** 2026-09-22, after the Ruff migration while reviewing 15 failures in
the private SMonitor integration tests.
**Status:** Blocked on `uibcdf/smonitor#21`, which owns the catalog-warning rebuild
behavior. The local tests already guard the visible text.

## What

With SMonitor `0.16.0+4.gec50e9e`, rebuilding a MolSysMT catalog warning from its
`args` appends the catalog hint again. The existing private suite gives 15 failures:
14 parametrizations of
`tests/_private/smonitor/test_xdist_warning_reconstruction.py::test_catalog_warnings_are_not_re_rendered`
and one
`tests/_private/smonitor/test_warnings.py::test_structural_attribute_drop_warning_preserves_reconstructed_message`.

```bash
$ pytest --receptor=llm -n 12 tests/_private
# 15 failed, 788 passed
$ python -c 'from molsysmt._private.smonitor.warnings import StructuralAttributeDropWarning; w=StructuralAttributeDropWarning(attributes=["time"]); r=type(w)(*w.args); print(str(w)==str(r))'
False
```

The latter command is the same args-only reconstruction operation used by warning
transport. The original `StructuralAttributeDropWarning` contains the
`attribute_policy='strict'` hint once; the rebuilt one contains it twice.

## How

`molsysmt/_private/smonitor/warnings.py:21` forwards both `catalog=CATALOG` and
`meta=META` on every call to `MolSysMTCatalogWarning.__init__`, including a rebuild
whose `message` is already rendered. SMonitor's
`smonitor/integrations/diagnostic.py:169` currently treats the text as authoritative
only when `message` is present **and** `extra`, `meta`, and `catalog` are all absent.
MolSysMT's wrapper therefore misses that branch, resolves the warning code again,
and appends the hint again. SMonitor's integration guide itself documents the
wrapper pattern that supplies a catalog. The provider-side defect is
`uibcdf/smonitor#21`.

`pyproject.toml` permits `smonitor>=0.13.0`, so this development version lies within
MolSysMT's declared version range. The controlled hard-dependency file pins an older
SMonitor commit; whether the defect appears with that controlled pin was not measured
in this report.

## Why

Warning text is user-facing diagnostic information and should survive pytest-xdist
or another args-only rebuild unchanged. Duplicate hints reduce its clarity and fail
an existing integration guard across 15 test cases. The defect affects warning
presentation; no change to molecular results was observed.

## What is measured and what is assumed

**Measured:** `pytest --receptor=llm -n 12 tests/_private` returned 15 failures and
788 passes on 2026-09-22. Fourteen failures are the parametrized round-trip guard;
the fifteenth is the direct `StructuralAttributeDropWarning` guard.

**Measured:** a direct `type(w)(*w.args)` rebuild of
`StructuralAttributeDropWarning(attributes=["time"])` duplicates its hint. The
comparison prints `False`.

**Inspected:** MolSysMT always supplies `catalog` and `meta`, and SMonitor's
args-only predicate requires both to be absent. The declared dependency floor is
`smonitor>=0.13.0`.

**Unmeasured:** the behavior under every released SMonitor version in the supported
range, including the controlled hard-dependency pin. A fix must be tested against
the version selected for release.

## What was refuted

The earlier MolSysMT defects `uibcdf/molsysmt#158` and `uibcdf/molsysmt#161`
corrected constructor argument order and extended class coverage. The failing
classes now accept the rendered message first, so their previous field-ordering
problem does not explain this duplication. The current failure depends on the
SMonitor rebuild predicate and MolSysMT's documented wrapper pattern.

## Scope and exclusions

This report tracks MolSysMT's compatibility with the supported SMonitor version
range and its warning round-trip guard. The provider behavior is tracked in
`uibcdf/smonitor#21`. It does not propose changing molecular computations or
weakening the existing warning assertions.

## Acceptance criteria

- The xdist round-trip and direct reconstruction tests pass with the corrected
  SMonitor integration using Pytest Receptor and 12 workers.
- The selected SMonitor release or dependency constraint is verified against the
  declared supported range and the controlled release environment.
- The MolSysMT warning guard remains able to detect a second appended hint.

## Dependencies and risks

Blocked by `uibcdf/smonitor#21`. A consumer-side workaround, if chosen before a
provider release, must preserve catalog resolution for new warnings and exact text
for args-only rebuilds.

## Provenance

2026-09-22; Linux 7.0.0-28-generic x86_64; Python 3.13.14; pytest 9.1.1;
pytest-xdist 3.8.0; SMonitor 0.16.0+4.gec50e9e; MolSysMT commit `b82019dac`.
