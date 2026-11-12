---
summary: One-letter sequence copying exposes the standard-library function instead of its adapter
issue: uibcdf/molsysmt#731
status: active
opened: 2026-11-12
closed:
severity: medium
verification: reproduced
area: [form]
guard: tests/form/string_amino_acids_1/test_copy.py
normative:
blocked_by: []
supersedes: []
---

# One-letter sequence copy adapter

## What

The copy module imports the standard-library copy function and accidentally
names its decorated wrapper extract. The form exports the standard function.
Ordinary msm.copy and the one-argument adapter call preserve the sequence;
explicit skip_digestion=True/False raises TypeError. The distinction matters: the
probe does not establish a failure of the ordinary public default.

## How

The bounded probe on cd6f26523 records both successful defaults and the trusted-
argument TypeError. The combined defect baseline has eight failures/two passes:
four copy failures and four separate AlphaFold export failures under #732.
Renaming the wrapper to copy and aliasing the standard helper supplies the
existing adapter boundary rather than changing string representation.

## Why

The exported adapter must accept its documented common validation argument.
Strings are immutable; an equal result need not have a distinct identity. The
fix preserves content and prefixes and uses the established ArgDigest decorator.
No new public API, sequence interpretation or atomic construction is added.

## Acceptance and evidence

Validated/trusted calls and ordinary public calls must preserve bare/prefixed
values. The corrected combined cohort passes thirteen cases, including both
changed docstrings and the existing three-letter copy guard. Documentation
source/HTML, common gates and closeout remain due before closure.

## Provenance

Linux/Python 3.14.7; the frozen controlled provider composition and native
4ffb82e4 remain. One CPU, 1.5 GiB, no own swap and a 6.5-GiB host reserve.
Original probe failures and source hashes remain in the receiving cache.
