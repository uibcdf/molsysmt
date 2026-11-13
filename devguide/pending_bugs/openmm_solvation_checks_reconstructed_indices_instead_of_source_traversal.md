---
summary: OpenMM solvation checks reconstructed indices instead of source traversal
issue: uibcdf/molsysmt#747
status: open
opened: 2026-11-13
closed:
severity: medium
verification: reproduced
area: [build, form]
guard: tests/build/solvate/test_source_identifiers.py::test_noncanonical_provider_indices_are_rejected_before_solvent
normative:
blocked_by: []
supersedes: []
---

# Solvation validates a reconstructed provider axis

**Reported:** 2026-11-13, during the contextual complete-source audit for #713.
**Status:** open; current-source failure independently reproduced.

## What

An OpenMM Modeller whose first atom index is changed to 9 reaches
`Modeller.addSolvent` instead of being rejected for noncanonical traversal.
The existing public regression deliberately makes solvent construction fail
if it is reached. Both the complete source session and the isolated check fail:

```bash
python -m pytest --receptor=llm -n0 tests/build/solvate/test_source_identifiers.py::test_noncanonical_provider_indices_are_rejected_before_solvent
```

## How

`build.solvate` converts the source to an independent `openmm.Modeller` before
`build._solvation_ids.capture` checks traversal. The copy route reconstructs
the topology with dense indices. The helper validates that reconstructed
modeller, rather than the original provider topology on which source getters
and positional correspondence depend. Inspection therefore explains the
observed bypass; validate the original relevant axis before reconstructing it.

## Why

Solvation promises positional source correspondence and explicitly rejects
traversal/index disagreement. Silently normalizing malformed input before
that check defeats the promised refusal and can hide an ambiguous source axis.
No incorrect result for a valid canonical input is demonstrated by this test.

## What is measured and what is assumed

The isolated two-failure cohort reproduces this assertion with unchanged source
and providers. The source/copy validation order is distinct from any claim
about the unobserved cause of #713. See the
[context receipt](../../devtools/data/complete_context_import_receiving_713_20261113.json).

## What was refuted

This failure does not require xdist or other tests: the isolated regression
also fails. The helper already checks dense traversal, so adding a second
check of the reconstructed copy would not repair the owning boundary.

## Scope and exclusions

Restore validation of the actual provider source used for correspondence;
preserve independent copies, nullable/string IDs, units and valid-source
solvation. Do not redesign solvation or implicitly reorder source coordinates.

## Acceptance criteria

Reject malformed original atom/group traversal before solvent construction;
the named regression must pass. Exercise valid IDs and provider-copy paths,
including source immutability, to ensure the rejection does not break supported
canonical inputs. Keep the original failed full session failed.

## Provenance

Clean `dec10b9d55be137a7fe3978bbdf6f031e99bbdcb`, Linux/Python 3.14.7,
unchanged native ABI3 `4ffb82e4`, frozen client/support composition documented
in the context receipt. Full execution: three workers/3 CPUs/6 GiB; isolated
receiving: sequential, 1 CPU/1.5 GiB. Both retain a 6.5-GiB host reserve and
zero own swap. No resource stop or own OOM occurs.
