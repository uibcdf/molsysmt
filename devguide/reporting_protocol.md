# Reporting protocol

How a defect or a proposal enters the project, is worked on, and is closed.

This document is normative. It governs `pending_bugs/`, `pending_proposals/`, their
`docs/` subdirectories, and the GitHub issue board. It complements
[DOCUMENT_POLICY.md](DOCUMENT_POLICY.md), which governs what a developer document must
contain; this one governs the lifecycle around it.

## The rule

**If it deserves a document in `devguide/`, it deserves an issue.**

We have never written a pending document for a typo, a lint fix, or a rename. The
document is already the significance filter, so no second one is needed.

The two records have different jobs and must not be given the same one:

| | holds | changes |
|---|---|---|
| the document | the analysis, the measurements, the refuted paths | continuously |
| the issue | state, and the settled facts a reader outside the repository needs | at two moments only |

The issue is written when it opens and when it closes. It is not maintained in between.
If the analysis changes on the way, the document is corrected; the issue is not
rewritten, and the closing comment states the final truth.

**One theme, one issue, one or more documents.** A theme may grow a separate evidence
document, or split into two themes. Both movements are reported on the issue.

## Identity

The issue number is the stable identity of a theme. Filenames are local names and may
change; issue numbers may not.

Consequences:

- Cross-repository references use `uibcdf/<repo>#<number>`, never a path into another
  repository's `devguide/`. A path breaks silently when the other side renames or, as in
  repositories that delete rather than archive, removes the file. An issue number does
  not break; it closes.
- References between documents *within* this repository stay repository-relative
  Markdown links, as [DOCUMENT_POLICY.md](DOCUMENT_POLICY.md) requires.

## Front matter

Every document under `pending_bugs/` or `pending_proposals/` — and every document
archived from them — begins with YAML front matter:

```yaml
---
summary: Structural attribute resolution ignores the structure axis.
issue: uibcdf/molsysmt#137
status: open
opened: 2026-08-03
closed:
severity: high
verification: reproduced
area: [attribute, convert]
guard:
normative:
blocked_by: []
supersedes: []
---
```

| field | required | meaning |
|---|---|---|
| `summary` | always | One line. Feeds every generated index and the issue title. |
| `issue` | always | `uibcdf/<repo>#<number>`. |
| `status` | always | See below. |
| `opened` | always | ISO date the document was filed. |
| `closed` | when not open | ISO date the status left the open set. |
| `severity` | bugs | `critical`, `high`, `medium`, `low`. |
| `verification` | always | How the report itself was verified. See below. |
| `area` | always | One or more free tags matching repository areas. |
| `guard` | see closing | Test that fails if the defect returns. |
| `normative` | see closing | Document that absorbed the durable rules. |
| `blocked_by` | optional | Issue references this waits on. |
| `supersedes` | optional | Issue references this replaces. |

`README.md` files in those directories carry no front matter; they are indexes, not
reports.

### `status`

| value | meaning |
|---|---|
| `open` | Filed, not started. |
| `active` | Being worked on now. |
| `blocked` | Waiting on something named in `blocked_by`. |
| `partial` | Some phases done, the rest pending. |
| `resolved` | Done, with the guard or the normative document named. |
| `withdrawn` | The premise died. |
| `superseded` | Replaced by the theme named in the replacing document's `supersedes`. |

`partial` and `blocked` exist because we needed them and did not have them. Three
entries were carrying that state in prose — *"Tier 1 is resolved; Tier 2 and Tier 3
pending"*, *"Part 1 done; Part 2 pending"* — where nothing could query it and the index
had to be written by hand.

The first four are the **open set**. The last three are the **closed set**, and a
document in the closed set belongs under `archive/`.

### `verification`

How solid the report's own diagnosis is:

| value | meaning |
|---|---|
| `reproduced` | Run, and it failed as described. |
| `measured` | Numbers in the document, with the command that produces them. |
| `inspected` | Read in the source, not executed. |
| `upstream` | Confirmed to originate outside this repository. |
| `asserted` | Believed, not checked. |

`asserted` is permitted. It is the honest label for a report worth filing before it is
verified, and it makes that debt visible instead of letting a claim read as a finding.
Three claims were corrected last cycle that would have carried this label.

**This is a different axis from the evidence labels in
[DOCUMENT_POLICY.md](DOCUMENT_POLICY.md).** Those — *Implemented*, *Contract-tested*,
*Parity-tested*, *Scientifically validated*, *Benchmarked* — qualify how well a
**feature** is verified. This field qualifies how well a **report** is verified. Use both
where both apply: a report may be `verification: measured` about a surface that is only
*Implemented*.

## Filing a report we found ourselves

1. **Open the issue first**, to obtain the number.
2. **Write the document** from [`templates/report.md`](templates/report.md), with
   `issue:` filled in. One template serves both queues: the directory decides whether it
   is a defect or a proposal, and the *What / How / Why* spine is the same one the issue
   carries, expanded.
3. **Commit and push.** Until the push, the issue's `Record` line names a path that does
   not yet exist on `main`; do not leave that gap open across sessions.

The issue body at open:

```
What  — get_dihedral_quartets(with_blocks=True) raises on every real system.
How   — msm.structure.get_dihedral_quartets(molsys, with_blocks=True)
        ValueError: setting an array element with a sequence.
        A ragged collection of atom-index sets is pushed through np.array.
Why   — Public since 0.19.0. No caller can use with_blocks at all, and the
        feature is advertised in the docstring and in the User Guide.
Record — devguide/pending_bugs/dihedral_quartets_with_blocks_raises_on_ragged_blocks.md
```

For a proposal the three fields keep their names and change their content: **What** is
what is proposed, **How** is how it would be done in two lines, **Why** is the problem it
solves and the evidence behind it.

Two optional lines, bugs only, when they apply: `Affects` when the affected surface is
not obvious from *What*, and `Workaround` — that one is for whoever is hitting the defect
today.

**Telegraphic.** Reasoning belongs in the document.

## Attending a report that came from outside

The issue already exists and someone else wrote it, possibly in different terms and
possibly with the wrong diagnosis. Attending it means writing the local document and
answering once:

```
Triaged. Reproduced on 0.20.1 / Python 3.13 / Linux.

What  — <the problem as we verified it, not as it arrived>
How   — <the command we reproduced it with>
Why   — <real scope: which public surface is affected>
Record — devguide/pending_bugs/<file>.md

Analysis and progress go in that file; this issue carries the state and the
resolution.
```

Restating *What / How / Why* in our own terms is the point of the comment, not a
courtesy. The document's `verification` field then records whether we reproduced it,
only inspected it, or could not reproduce it at all.

Remove `needs-triage` when this comment goes in.

### The asymmetry

It holds in one direction only, and this must stay written down or the validator will
one day be made to enforce the other:

- **Every document in `pending_*` has an `issue`.** Always. The validator checks this.
- **Not every issue has a document.** An incoming issue awaiting triage has none, and one
  that cannot be reproduced or is declined closes with the reason and never gets one.

## Closing

An entry closes when three things exist: the change, the record, and something that
fails if the defect returns.

1. Set `status`, `closed`, and **`guard`** — the test that fails if it comes back. For a
   proposal whose outcome is a rule rather than a behaviour, set **`normative`** instead:
   the document that absorbed the durable rules, as
   [DOCUMENT_POLICY.md](DOCUMENT_POLICY.md) requires. One of the two is mandatory for
   `resolved`; neither is for `withdrawn` or `superseded`.
2. Move the document to `archive/resolved_bugs/` or `archive/resolved_proposals/`.
3. Close the issue with the three-line comment.

```
Fixed in 3f9a1c2 — fix(structure): return dihedral blocks as the list they always were

For users — blocks come back as a list, not an array. Prolines yield one block
            instead of two: the ring survives the cut.
Guard  — tests/structure/test_dihedral_quartets.py::test_ragged_blocks
Record — devguide/archive/resolved_bugs/dihedral_quartets_with_blocks_raises_on_ragged_blocks.md
```

*For users* is the line that belongs in the issue more than in the document: the
document is written for us, the issue is read by them.

For a proposal, the first line is a **Decision** — accepted, withdrawn, or superseded —
with the reason in one line. Our archive already distinguishes *completed*, *withdrawn*
and *superseded*; that distinction should be visible from outside.

Finding and fixing within one session is normal and still gets both. An issue opened and
closed the same day is the public record showing the defect was caught and corrected in
hours.

## Corrections

A claim that turns out to be false is corrected, not left standing. Where depends on the
document's state:

- **In the open set:** correct in place. The document is live.
- **Archived:** append a dated correction note. Do not edit the original claim.
  [DOCUMENT_POLICY.md](DOCUMENT_POLICY.md) makes archived documents immutable historical
  evidence, and it is right: rewriting them destroys the record of what we believed and
  when. A stale benchmark number needs no correction at all — it was true on its date. A
  claim that was **never** true does, and an appended note gives both the correction and
  the fact that we got it wrong.

```markdown
## Correction — 2026-08-09

The section above states that MolSysMT pre-renders warning messages. It never did:
the call sites always passed `reason=` as structured data. What was real is the
`smonitor>=0.11.6` floor, under which `{reason}` rendered literally.
```

This is the habit that has paid best. Keep it.

## Labels

| group | labels | who sets them |
|---|---|---|
| kind, exactly one | `bug`, `proposal`, `enhancement`, `documentation` | by hand, at open |
| state, zero or one | `in-progress`, `blocked`, `partial` | derived from `status` |
| area, zero or more | `form`, `convert`, `structure`, `docs`, `build`, `ci`, `deps` | derived from `area` |
| triage | `needs-triage` | by hand, on arrival from outside |
| severity | `scientific-integrity` | by hand, bugs only |

No state label means open and unstarted. There is no `done` label: GitHub closes issues,
and a `done` label on an open issue is a contradiction waiting to happen.

Only `scientific-integrity` is promoted to a label, because it is the one severity a
third party must see without reading anything. The rest stays in `severity`.

The milestone carries release scope: `1.0` on anything that blocks it.

Derived labels are synchronised from the front matter, never edited on the board:

```bash
python devtools/scripts/devguide_issue.py sync
```

## Indexes are generated

Each queue's `README.md` has a hand-written head — how to read the directory, what
precedence it carries, what it demands — and a generated block:

```markdown
<!-- generated: devguide_index -->
...
<!-- /generated -->
```

The head is judgement and is written. The block is data and is rendered from front
matter. [DOCUMENT_POLICY.md](DOCUMENT_POLICY.md) forbids maintaining two manually
independent authoritative lists, and a hand-written index of documents that also
describe themselves is exactly that.

Narrative about a closed entry belongs in the entry's own `## Resolution` section, which
is where someone will look for it in a year — not in the index of the directory it has
already left.

```bash
python devtools/scripts/devguide_index.py           # write
python devtools/scripts/devguide_index.py --check   # fail if stale
```

## What is checked automatically

`devtools/scripts/validate_devguide.py`, already part of the release gate, checks:

- front matter present, parseable, and carrying every required field;
- `status` and `verification` drawn from the vocabularies above;
- `issue` present and well formed on every pending document;
- `severity` present on bugs;
- `closed` set whenever the status is in the closed set, and absent when it is not;
- `resolved` naming a `guard` **that exists in the test tree**, or a `normative`
  document that exists;
- `blocked_by` and `supersedes` well formed;
- generated index blocks up to date.

It runs offline. Verifying that the issue exists and that its state agrees is a separate,
opt-in step, because it needs the network and a token:

```bash
python devtools/scripts/devguide_issue.py sync --check
```

## Scope beyond this repository

The same front matter and the same vocabularies apply to `argdigest`, `depdigest`,
`pyunitwizard`, `smonitor` and `molsysviewer`. That uniformity is what makes
`uibcdf/<repo>#<number>` a reliable reference in every direction.

One alignment is required: **archive, never delete.** A repository that deletes a closed
proposal breaks every reference into it. This one archives, and the others should.

## Security

An exploitable finding is not opened as a public issue. It goes to a private security
advisory, and the local document stays out of the pending queues until a fix is
released. The protocol above resumes at that point.
