---
summary: Execute every declared conversion edge in the test suite, not only audit it statically.
issue: uibcdf/molsysmt#181
status: open
opened: 2026-08-19
closed:
verification: measured
area: [form, convert, tests]
guard:
normative:
blocked_by: []
supersedes: []
---

# Run the conversion graph, do not only describe it

**Reported:** 2026-08-19, from the post-mortem of
[`uibcdf/molsysmt#180`](https://github.com/uibcdf/molsysmt/issues/180): seven public
conversion routes were broken for eleven days with every audit green.
**Status:** open, post-1.0 by decision. The gap is measured; the cost of closing it is
not.

## What

Generate one smoke case per declared conversion edge, over a small shipped system,
asserting only that the conversion completes and returns an object of the declared form.

Not fidelity. Not shapes, units, indexing or `None` semantics — those are the subject of
[Conversion Fidelity and MolSysDict v1](conversion_fidelity_and_molsysdict_v1.md) and are
a much larger claim. This proposal asserts the weakest useful property: **the route
runs**.

## How

The graph is already discoverable. `audit_conversion_fidelity.py` builds it from each
adapter's `_convert_to` map, and the same traversal can emit parametrised cases instead
of a coverage report.

The hard parts are not the traversal:

- **Which system to use per source form.** A `file:prmtop` case needs a prmtop; an
  `openmm.Topology` case needs coordinates supplied, as
  [`uibcdf/molsysmt#180`](https://github.com/uibcdf/molsysmt/issues/180) showed. Some
  forms have no small shipped instance.
- **Soft dependencies.** Edges into `pdbfixer`, `parmed`, `MDAnalysis` and the rest must
  skip cleanly, not fail, when the dependency is absent.
- **Runtime.** `tests/form` already runs 6 772 tests in roughly 270 s on 14 workers.
  Adding up to 561 cases is not free, and some edges download or write files.

## Why

Measured on 2026-08-19:

| | |
|---|---|
| declared conversion edges | **561** |
| adapters declaring them | 92 |
| median edges per adapter | 5 |
| largest | `molsysmt_MolSys` 34, `file_pdb` 23, `string_pdb_id` 20 |
| `convert(` calls in `tests/` | 956 |
| distinct target forms named in `tests/` | 55 |

Coverage exists and is substantial. What does not exist is any statement about *which*
of the 561 edges it touches, so the answer to "is this route exercised?" is unknown
rather than yes or no.

**Both audits over this graph are static, and both say so.**
`audit_conversion_fidelity.py`: *"The compact baseline records accepted non-exhaustive
coverage debt; it is not a claim that those routes are fully verified."*
`validate_form_adapters.py`: *"This static reachability check does not prove correct
values, shapes, units, indexing, `None` semantics, conversion fidelity, decorator
correctness, or iterator output behavior."*

Neither is wrong. The gap is not a defect in either tool; it is that nothing closes it.

**What that cost.** In `e6b20c77c` (2026-08-08, 214 files, *"make a plugin's converters
lazy, and unambiguous to import"*), seven adapters acquired an import of the target
form's identity converter instead of their own. Seven public routes — `nglview.NGLWidget
-> openmm.Topology`, four out of `openmm.Topology`, two out of `string:alphafold_id` —
raised on every call. Both audits stayed green for eleven days.

A smoke case per edge would have failed on the introducing commit. It would also have
caught the two further defects found while fixing #180, neither of which needs fidelity
to detect: a `StringIO().read(text)` misuse raising `TypeError`, and an unguarded
`coordinates.shape[0]`.

## What is measured and what is assumed

Measured: every figure in the table above, by parsing the `_convert_to` dictionaries and
grepping `tests/`.

Assumed, explicitly: that most edges can be exercised from a shipped system. Not
checked — some forms may have no small instance, and that is precisely what a first
measurement pass should establish before any estimate is offered.

Not estimated: the effort. The 2026-08-19 conversation put a figure on a related idea
without measuring it and had to withdraw it; no figure is offered here.

## What was refuted

**A static check in `validate_form_adapters.py`, proposed as the guard for #180 and
withdrawn.** Two rules were tried. Flagging any absolute import of a converter that
shadows a local module produced 52 hits, most legitimate — `MDAnalysis_AtomGroup`
delegating to `MDAnalysis_Universe` is by design. Narrowing to *identity* converters
looked sharper and still flagged `file_h5msm` and `file_pdb`, whose target converters
deliberately accept a path; those routes were run and all succeed.

What separates the defect from the legitimate cases is whether the imported converter
tolerates a foreign item, which is behavioural and invisible to a static rule. That
failure is the argument for this proposal: the property in question only exists at run
time, so the check has to run.

## Scope and exclusions

In scope: one executable case per declared edge, asserting completion and returned form.

Out of scope:

- Fidelity of the converted content — [Conversion Fidelity and MolSysDict
  v1](conversion_fidelity_and_molsysdict_v1.md).
- Replacing either static audit. They answer a different question, cheaply, and should
  stay.
- Transitive routes. Only edges declared in a `_convert_to` map.

## Acceptance criteria

- Every declared edge is either exercised or explicitly listed as not exercisable, with
  the reason.
- The list may only shrink, in the idiom already used by
  `form_attribute_delivery_baseline.json` and `tier1_conversion_fidelity_baseline.json`.
- Missing soft dependencies skip; they do not fail.
- Introducing #180's defect again fails the suite.

## Provenance

MolSysMT at `bc42b2eaa`, 2026-08-19. Edge counts from the `_convert_to` dictionaries in
`molsysmt/form/*/__init__.py`; test counts from `tests/`; timing from
`pytest tests/form -n 14 --dist loadfile`.
