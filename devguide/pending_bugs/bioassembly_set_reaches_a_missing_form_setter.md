---
summary: Setting readable bioassembly metadata reaches a missing form setter.
issue: uibcdf/molsysmt#697
status: active
opened: 2026-11-10
closed:
severity: medium
verification: reproduced
area: [basic, set, native]
guard: tests/basic/test_bioassembly_assignment_contract.py
normative:
blocked_by: []
supersedes: []
---

# Unavailable editing routes need a typed refusal

## What / How / Why

The Structures and MolSys adapters expose bioassembly metadata for reading, but
neither declares a setter. Basic set incorrectly treats read availability as
write availability and reaches an internal AttributeError. The protected
baseline fails 24 public calls across inferred/explicit system elements,
standalone/attached domains, complete/selected structure scopes, and None,
empty or named replacements. Two constructor/getter unit controls pass.

## Contract and correction

Keep the supported constructor route. This stabilization correction does not
add an editing API or reinterpret system-level assembly operations as a
structure-aligned series. Basic set checks that the requested adapter setter
exists and is callable, then raises the existing SMonitor
NotWithThisFormError when it does not. Both element-dispatch branches share the
same small private resolver. Argument digestion still validates incoming
operations and units; the attribute registry still truthfully declares reading.

Refusal preserves coordinates, existing assembly metadata and named-analysis
coverage. None and an empty dictionary cannot manufacture a missing route.
The existing sequential contract for multiple attributes is unchanged: this
does not promise rollback of another attribute already assigned in that call.

## Receiving

Require public typed-refusal and source-preservation controls, constructor/getter
nm/pm equivalence, neighboring basic/form/native consumers, public docstrings,
the relevant tutorial/course explanation, and offline governance gates.
The original AttributeError baseline remains failed evidence. This supplemental
repair adds no milestone weight and supplies no installed or release acceptance.
