---
summary: Evaluate a native AminoAcidSequence value object
issue: uibcdf/molsysmt#242
status: open
opened: 2026-09-24
closed:
verification: inspected
area: [form, convert]
guard:
normative:
blocked_by: []
supersedes: []
---

# Evaluate a native AminoAcidSequence value object

**Reported:** 2026-09-24, during the review of optional Biopython use in core
sequence conversions.
**Status:** Open design question; no class is approved for implementation yet.

## What

Decide whether MolSysMT needs one immutable `AminoAcidSequence` value object
with explicit one-letter and three-letter constructors and views. This is a
future API decision, not a prerequisite for removing an avoidable Biopython
dependency from the current string-form converter.

## How

If a use case justifies the object, specify its canonical internal
representation, validation, treatment of ambiguity and nonstandard residues,
terminal cappings, selection and indexing, equality, serialization, and its
place in the form catalogue. Candidate entry points are
`from_one_letter()` and `from_three_letter()` rather than separate
`AminoAcids1` and `AminoAcids3` classes. Compare the resulting API with the
existing `string:amino_acids_1` and `string:amino_acids_3` forms and their
explicit prefixes before adding a new public form.

## Why

An explicit value object could make short or ambiguous strings unambiguous
and permit sequence-level metadata. Encoding length alone does not create
two different molecular entities, however. The existing string forms already
distinguish one-letter and three-letter notation, and the current dependency
problem is confined to a converter. Adding classes without a distinct
user-facing contract would multiply adapters, tests, and documentation.

## What is measured and what is assumed

Inspected on 2026-09-24: the catalogue declares separate string forms under
`molsysmt/form/string_amino_acids_1/` and
`molsysmt/form/string_amino_acids_3/`; `molsysmt/native/__init__.py` has no
amino-acid sequence class. No usage study has established demand for a new
object. Improved explicitness and metadata support are design hypotheses.

## What was refuted

Two native classes, one per code length, are not needed merely to replace
`Bio.SeqUtils.seq3`: the string converter can use MolSysMT's own code table.
The opposite conclusion, that a typed sequence can never help, is also not
established; ambiguity and metadata remain valid reasons to revisit it.

## Scope and exclusions

This issue evaluates a future type and its form contract. It does not request
implementation now, change string-form precedence, eliminate Biopython
interoperability, or promise a release version. Core dependency reduction is
tracked separately in `uibcdf/molsysmt#243`.

## Acceptance criteria

- Record a concrete user need and compare it with existing string forms and
  explicit prefixes.
- Choose one value object, another design, or no new class; state the reasons.
- If accepted, define behavior for ambiguous codes, caps, indexing, and
  conversion before implementation, with API/User Guide/course coverage and
  an addressable behavioral test.
- If the outcome is a durable rule without a class, name the normative
  document that records it when closing this proposal.
