# Reporting bugs and proposals

How work enters MolSysMT, is tracked, and is closed.

```{note}
The canonical source is [`devguide/reporting_protocol.md`](https://github.com/uibcdf/molsysmt/blob/main/devguide/reporting_protocol.md)
in the repository. This page explains the same process for readers who are not working
inside a checkout; where the two differ, the repository wins.
```

## If you are using MolSysMT

**[Open an issue](https://github.com/uibcdf/molsysmt/issues/new/choose).** That is the
front door, whether you have a patch or only a symptom. Templates for a bug report and
for a proposal are offered when you create one.

A useful report answers three questions:

- **What** goes wrong, or what you would like to exist.
- **How** to see it — the shortest snippet that reproduces it, pasted rather than
  described, with the traceback if there is one.
- **Why** it matters: which call, which workflow, and what you did instead.

Include your MolSysMT version, your Python version, and your platform. If a molecular
file is involved, a small one that shows the problem is worth more than a large one that
also does.

Usage questions belong in
[Discussions](https://github.com/uibcdf/molsysmt/discussions). An exploitable problem
belongs in a
[private security advisory](https://github.com/uibcdf/molsysmt/security/advisories/new),
not in a public issue.

## What happens to your report

We triage by reproducing it. When we do, we answer on the issue restating the problem
**as we verified it** — an incoming diagnosis is sometimes right and sometimes not, and
saying which is part of the answer — and we link the working record under `devguide/`.

From then on the two records have different jobs:

| | holds | changes |
|---|---|---|
| the document in `devguide/` | the analysis, the measurements, the paths that were tried and refuted | continuously |
| the issue | state, and the settled facts a reader outside the repository needs | at two moments only |

The issue is written when it opens and when it closes, and is not maintained in between.
If the analysis changes on the way, the document is corrected; the issue is not
rewritten, and the closing comment states the final truth.

Not every issue becomes a document. One that cannot be reproduced, or that is declined,
closes with the reason.

## How it closes

An entry closes when three things exist: the change, the record, and something that
fails if the defect returns. The closing comment names all three:

```text
Fixed in 3f9a1c2 — fix(structure): return dihedral blocks as the list they always were

For users — blocks come back as a list, not an array. Prolines yield one block
            instead of two: the ring survives the cut.
Guard  — tests/structure/test_dihedral_quartets.py::test_ragged_blocks
Record — devguide/archive/resolved_bugs/dihedral_quartets_with_blocks_raises_on_ragged_blocks.md
```

The **Guard** line is the one that makes "closed" mean something: a confirmed defect
does not close without a test that fails if it comes back. For a proposal whose outcome
is a rule rather than a behaviour, that line instead names the normative document that
absorbed the rule.

A report is archived, never deleted. If one of these questions returns, it returns with
a different premise and deserves a fresh document rather than a revived one.

## If you are working inside the repository

Maintainers and automated agents follow a stricter version of the same process, because
the queues under `devguide/` are validated:

- **If it deserves a document, it deserves an issue.** One theme, one issue, one or more
  documents. We do not write documents for typos, so the document is already the
  significance filter.
- Every entry carries front matter — summary, issue, status, dates, severity, how the
  report itself was verified, area — which the release gate checks and from which the
  queue indexes are generated.
- Cross-repository references use `uibcdf/<repo>#<number>`, never a path into another
  repository's developer guide. A path breaks silently when the other side renames or
  removes the file; an issue number does not break, it closes.
- Corrections to an archived document are appended as dated notes rather than edited in
  place, so the record of what was believed, and when, survives.

The commands:

```bash
python devtools/scripts/devguide_issue.py open --kind bug --title "..." --area form
python devtools/scripts/devguide_index.py            # regenerate the queue indexes
python devtools/scripts/validate_devguide.py         # schema, lifecycle, indexes, links
```

Full rules in
[`devguide/AGENTS.md`](https://github.com/uibcdf/molsysmt/blob/main/devguide/AGENTS.md)
and
[`devguide/reporting_protocol.md`](https://github.com/uibcdf/molsysmt/blob/main/devguide/reporting_protocol.md).
