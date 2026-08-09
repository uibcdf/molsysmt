---
summary: One line, present tense. Becomes the issue title.
issue: uibcdf/molsysmt#000
status: open
opened: 2026-01-01
closed:
severity: medium
verification: asserted
area: []
guard:
normative:
blocked_by: []
supersedes: []
---

# <Title: the defect, or what is proposed — not the fix>

**Reported:** <date, and how it surfaced — a suite run, a downstream request, an audit,
a defect that turned out to be a design question.>
**Status:** <one line agreeing with the `status` field.>

<!--
One template for both queues. The directory decides which this is:

  pending_bugs/       a defect. `severity` is required.
  pending_proposals/  work not yet part of the contract. Remove `severity`.

The three sections below are the same spine the issue carries, expanded. Delete this
comment and any section that genuinely does not apply, but do not delete a section
because it is hard to fill: an empty "What was refuted" and a missing one say different
things.
-->

## What

**Bug:** the behaviour that is wrong, with the command that produces it pasted, not
paraphrased.

**Proposal:** what is proposed, in a paragraph. If it does not fit in a paragraph, it is
more than one proposal.

```bash
$ python -c "..."
```

## How

**Bug:** where it goes wrong, with `file.py:line`. If the cause is not yet known, say so
— an unfinished diagnosis is a fact, and `verification: asserted` records it honestly.

**Proposal:** the design, in enough detail to be argued with.

## Why

**Bug:** who or what breaks, and how far it reaches. This is what justifies the
`severity`.

**Proposal:** the problem it solves, with the evidence behind it. One driven by a
measurement carries the measurement; one driven by a judgement says so plainly.

## What is measured and what is assumed

Separate them, explicitly. Mark every estimate as an estimate, on its own line. A number
without the command that produced it is an assumption wearing a number's clothes.

## What was refuted

Hypotheses tried and eliminated, and why — for a proposal, the alternatives considered
and why they lost. This is the section that saves the next session, and the one most
often skipped.

## Scope and exclusions

What this covers, and what looks covered but is not. Exclusions are load-bearing: they
are what stops a report growing into a program.

## Acceptance criteria

What must be true to close this, in terms that can be checked.

It ends in one of two places, and reaching `resolved` requires one of them:

- a test that fails if this returns — the `guard` field. A confirmed defect does not
  close without one;
- or, when the outcome is a rule rather than a behaviour, the normative document that
  absorbs it — the `normative` field, as [DOCUMENT_POLICY.md](../DOCUMENT_POLICY.md)
  requires.

## Dependencies and risks

*(Optional.)* What this waits on, and what resolving it could break. Anything that is
another tracked theme goes in `blocked_by` as an issue reference, not only in prose.

## Provenance

*(Required whenever this document carries a measurement.)* Host, Python version, relevant
dependency versions, date.
