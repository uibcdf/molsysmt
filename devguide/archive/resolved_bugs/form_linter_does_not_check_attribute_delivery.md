# Bug: the form adapter linter does not check that declared attributes are deliverable

> Archived resolution record. This document describes the defect and rollout
> plan as originally diagnosed; current behavior is defined by the validator and
> its committed baseline.

**Status:** resolved 2026-07-13
**Severity:** medium — it is the safety net that should have caught the two bugs above
**Implementation:** `devtools/scripts/validate_form_adapters.py`
**Baseline:** `devtools/data/form_attribute_delivery_baseline.json`
**CI enforcement:** `.github/workflows/ci-smoke.yaml`

## Symptom

The conformance linter reports **92/92 PASS**, and did so while `file:inpcrd`
declared 12 attributes and implemented zero getters. It still passes today for
every form listed in
[`form_attributes_declared_without_getters.md`](../../pending_bugs/form_attributes_declared_without_getters.md),
including `parmed.Structure` (51 attributes declared, 2 getters) and `rdkit.Mol`
(74 declared, none reachable).

## Root cause

The linter is purely structural. It verifies that an adapter **has** the pieces of
the contract:

- the variables `form_name`, `form_type`, `bonds_are_explicit`,
  `bonds_can_be_computed`, and the three `piped_*` attributes;
- the callables `is_form` and `has_attribute`;
- that `attributes` is a dict and `_convert_to` is a dict;
- that a declared `StructuresIterator` implements `__enter__`/`__exit__`.

It never cross-checks the **promise** (`attributes.py` — what the form says it can
give) against the **delivery** (the getters that exist, or those reachable through
the form's pipes). A form that declares every attribute in the catalog and
implements nothing passes green.

## Proposed check

For each attribute declared `True` in a form's `attributes.py`, require that it be
*reachable*:

- the form implements `get_<attribute>_from_<element>` for at least one `element`
  in that attribute's `get_from` list in the attribute catalog
  (`molsysmt/attribute/attributes.py`); **or**
- the form's relevant pipe (`piped_topological_attribute`,
  `piped_structural_attribute`, or `piped_any_attribute`, followed transitively)
  leads to a form that does.

Attributes whose catalog entry has an empty `get_from` are derived and exempt.

Run against the current tree this check flags roughly 70 of the 92 forms, so it
cannot be turned into a hard gate on day one. Suggested rollout:

1. land the check in report-only mode and record the current inventory as a
   baseline;
2. fix the Tier 1 and Tier 2 forms (see the companion bug document);
3. flip it to a hard failure once those are clean, so the ratchet only tightens.

## Why this matters more than the individual fixes

Each of the other three bugs in this directory is a hole that this linter was
supposed to make impossible. `file:inpcrd` shipped with both getter modules left
as untouched scaffolding, and every gate in the repository — the linter, the test
suite, the support-tier notebook — reported green. The scaffolding tool
(`devtools/scripts/scaffold_form.py`) generates exactly those empty modules, so
the failure mode is the default outcome of the intended workflow: scaffold a form,
declare its attributes, forget to fill the getters, pass CI.

## Related

- [`get_single_attribute_bypasses_piping.md`](get_single_attribute_bypasses_piping.md)
- [`form_attributes_declared_without_getters.md`](../../pending_bugs/form_attributes_declared_without_getters.md)
- [`is_a_molecular_system_swallows_missing_getters.md`](is_a_molecular_system_swallows_missing_getters.md)
- `devguide/form_adapter_implementation.md` documents the adapter contract the
  linter is meant to enforce.
