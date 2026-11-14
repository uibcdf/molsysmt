---
summary: Conversion keyword registry omits output_filename for four writable file forms
issue: uibcdf/molsysmt#748
status: resolved
opened: 2026-11-13
closed: 2026-11-13
severity: medium
verification: reproduced
area: [convert, form, argdigest]
guard: tests/test_argument_contract.py::test_the_converter_table_still_matches_the_converters
normative:
blocked_by: []
supersedes: []
---

# Conversion keyword registry has four missing destination arguments

**Reported:** 2026-11-13, contextual complete-source audit for #713.
**Status:** Resolved in `a049a45f9`; the four canonical destination keywords are restored.

## What

The maintained converter table differs from the converters for `file:crd`,
`file:inpcrd`, `file:prmtop` and `file:h5`. Every difference is the missing
`output_filename` keyword; there are no stale keywords or unreadable signatures
in the measured derivation.

```bash
python -m pytest --receptor=llm -n0 tests/test_argument_contract.py::test_the_converter_table_still_matches_the_converters
```

This guard fails both in the complete source session and the isolated cohort.

## How

The written `molsysmt._private.argdigest.domain.converter_arguments` table is
the admissible keyword union used at the generic conversion boundary. The
four targets' current signatures declare `output_filename`; the committed
table does not. `devtools/scripts/generate_converter_arguments.py` derives all
96 targets and reports those exact four missing names, with 92 targets equal.
Regenerate and review the table rather than computing a replacement at runtime.

## Why

A drifted table can refuse a converter-supported explicit destination keyword
before the converter runs. The observed evidence establishes the registry
disagreement; it does not claim every filename-as-`to_form` route is broken or
that existing files are corrupted.

## What is measured and what is assumed

The complete run and isolated two-failure cohort use unchanged inputs. A
separate fresh derivation identifies the four differences above. The
[context receipt](../../../devtools/data/complete_context_import_receiving_713_20261113.json)
retains those outcomes and limits. No wrong molecular calculation is observed.

## What was refuted

The disagreement does not depend on xdist or cross-test mutation: it recurs
in an isolated invocation. All converter signatures are readable; ignoring
unreadable adapters or weakening the comparison would not repair this defect.

## Scope and exclusions

Restore the reviewed written contract, exercise the affected public keyword
paths, and retain typo rejection. Do not add a runtime-derived domain or
silently make every converter keyword universally admissible.

## Acceptance criteria

The named guard passes after regeneration, the four relevant public conversion
routes admit their destination keywords when required inputs are available,
and unsupported keyword rejection remains tested. The original complete
failed session remains failed; focused receiving has its own source identity.

## Provenance

Clean `dec10b9d55be137a7fe3978bbdf6f031e99bbdcb`, Linux/Python 3.14.7,
the unchanged native/client/support composition in the context receipt.
The isolated checks use 1 CPU/1.5 GiB, zero own swap and a 6.5-GiB host reserve,
with no OOM or resource stop.

## Resolution and receiving — 2026-11-13

Implementation `a049a45f9` regenerates the written domain with the maintained
generator. The reviewed diff adds exactly `output_filename` to the four targets
reported above. No converter implementation, runtime-derived domain, dependency
floor or broad keyword bypass changes.

The original equality guard passes. Four new public-call controls, which all
failed with UnknownArgumentError before the correction, now copy independent
whole-file outputs to the requested destination even with `copy_if_all=False`.
The original source bytes remain unchanged when the result is edited. Misspelled
`output_filenam` is still rejected without modifying the destination. These
opaque byte-copy tests receive keyword delivery and file independence; they do
not certify molecular decoding of arbitrary payloads.

The joint selected receiving passes 331 cases with zero omissions. It retains
all affected solvation, public argument, whole-file/copy, specific OpenMM
copy/extraction and addon paths plus the solvate doctest. The generator's check,
fifteen fast gates and full Ruff checks pass. The
[receiving receipt](../../../devtools/data/source_axis_converter_receiving_747_748_20261113.json)
records exact committed-source bytes, provider/native identities and bounded
resource measurements. It preserves the nine-failure/one-pass negative cohort
and the separate 1,615-case attempt interrupted at its operational wall ceiling.
Neither is relabelled as passed; complete-source/nightly and final qualification
remain separately required.
