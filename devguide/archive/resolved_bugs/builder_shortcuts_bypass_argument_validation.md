---
summary: MolSysBuilder query shortcuts bypass argument validation
issue: uibcdf/molsysmt#391
status: resolved
opened: 2026-10-21
closed: 2026-10-21
severity: medium
verification: reproduced
area: [api, argdigest]
guard: tests/native/test_native_queries.py
normative:
blocked_by: []
supersedes: []
---

# MolSysBuilder query shortcuts bypass argument validation

**Reported:** 2026-10-21, while expanding the native-query study in
uibcdf/molsysmt#128 at the maintainer's request.
**Status:** Resolved through the shared validated native query boundary.

## What

`MolSysBuilder.get()` and `MolSysBuilder.info()` replace the caller's
`skip_digestion` flag with `True` without first validating their arguments.
Their results therefore differ from the supported general query boundary:

```python
import molsysmt as msm
from molsysmt.native import MolSysBuilder

builder = MolSysBuilder()
builder.add_atom(atom_name="C", atom_type="C")
builder.get(skip_digestion="yes", n_atoms=True)  # returns 1
msm.get(builder, skip_digestion="yes", n_atoms=True)  # ArgumentError
builder.get(output_type="garbage", n_atoms=True)  # returns None
msm.get(builder, output_type="garbage", n_atoms=True)  # ArgumentError
builder.get(element="atoms", selection=0, atom_index=True)  # NotWithThisFormError
msm.get(builder, element="atoms", selection=0, atom_index=True)  # [0]
builder.info(skip_digestion="yes")  # returns a Styler
```

## How

The two shortcuts in `molsysmt/native/molsys_builder.py` have no ArgDigest
boundary and unconditionally delegate to `basic.get`/`basic.info` with
`skip_digestion=True`. This is the builder counterpart of the MolSys-only
repair in uibcdf/molsysmt#377, whose historical record is
[native shortcut validation](../archive/resolved_bugs/native_molsys_shortcuts_bypass_argument_validation.md).

Forwarding the caller's flag to the existing validated providers is a bounded
repair. A later optimized native query boundary must provide the complete
validation contract before trusted internal delegation. Neither approach needs
a duplicate attribute catalogue.

## Why

Builders are useful native inputs during incremental molecular construction.
Invalid query options must fail at the public boundary, and supported aliases
must work without requiring a conversion or a completed build. The faster
unvalidated builder shortcut is not valid evidence of an optimized equivalent
query in #128.

## What is measured and what is assumed

The commands above were executed with one declared carbon atom against source
`7ef2085d9b011b97bcb94644c0c48b14f96bdb02`, Linux/Python 3.14.7. The observed
values and exception types are reproduced. No mutation, coordinate loss or
scientific calculation failure was demonstrated.

## What was refuted

Declaring a `skip_digestion` option does not make its default effective when the
method discards it. The generic query over the same builder does normalize the
alias and reject the invalid options; absence of atom data is not the cause.

## Scope and exclusions

The existing builder `get` and `info` shortcuts only. The independent native
dispatch optimization belongs to uibcdf/molsysmt#128. This report does not
change builder construction, finalization, mutation or scientific inference.

## Acceptance criteria

- Reject invalid skip flags, output selectors, requested-attribute flags and
  unknown attribute names at the supported default boundary.
- Normalize supported element aliases and scalar atom selections.
- Preserve signatures, valid outputs and explicit trusted boolean calls.
- Add a regression test with independently expected values, and document the
  actual validation boundary in the API, User Guide and affected course.

## Provenance

2026-10-21, Linux x86_64 development checkout; Python 3.14.7. The reproduction
uses only native construction and query functions, without external files.


## Resolution — 2026-10-21

**Contract-tested.** MolSysBuilder inherits the shared native get/info boundary.
ArgDigest rejects invalid skip/output/attribute flags and unknown keywords,
normalizes supported element/attribute aliases and scalar selections, and
executes directly against the editable domains. Existing positional calls
remain valid; info additionally supports the shared keyword-only options.

`tests/native/test_native_queries.py` independently expects rejection of the
reported invalid options for every resident type, including the builder, and
checks live counts after adding an atom. The original unconditional bypass
admits these options or fails valid alias normalization and cannot satisfy
those assertions. No builder finalization is used for the queries.

The combined basic/native/interaction/connectivity selection passes 2,285 tests
with 12 workers and Pytest Receptor. Seven shared-method doctest examples pass;
new executable sections in the User Guide/Cookbook/course and changed method
API docstrings render without diagnostics. This closes boundary correctness,
not the separate remaining #128 representation/file optimization scope.
