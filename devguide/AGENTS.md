# Developer Guide Agents Guide

Rules for working inside `devguide/`. Read `../AGENTS.md` first.

## Before you write anything here

Two documents govern this directory, and they answer different questions:

- [`DOCUMENT_POLICY.md`](DOCUMENT_POLICY.md) — **what a document must contain**: its
  role, its evidence labels, its single-source rules, its link conventions.
- [`reporting_protocol.md`](reporting_protocol.md) — **how an entry lives**: how it is
  filed, tracked on the issue board, corrected, and closed.

If you are filing or closing a bug or a proposal, the second one is normative and
enforced. Do not improvise a header, a status word, or an index line.

## Filing a defect or a proposal

**One rule: if it deserves a document here, it deserves a GitHub issue.** We have never
written a pending document for a typo, so the document is already the significance
filter.

```bash
# creates the issue and scaffolds the document with its number already in place
python devtools/scripts/devguide_issue.py open --kind bug --title "..." --area form,convert --severity high
```

Then fill the document in from [`templates/report.md`](templates/report.md). One
template serves both queues; the directory decides which it is, and the
*What / How / Why* spine is the same one the issue carries, expanded.

If the report arrived from outside, the issue already exists: write the document, then
answer once on the issue restating *What / How / Why* **as you verified it**, not as it
arrived, and remove `needs-triage`.

## Closing

An entry closes when three things exist: the change, the record, and something that
fails if the defect returns.

1. Set `status`, `closed`, and `guard` — the test that fails if it comes back. For a
   proposal whose outcome is a rule rather than a behaviour, set `normative` instead:
   the document that absorbed the durable rules.
2. Move the document under `archive/`.
3. Close the issue naming the commit, the guard, and the archived record:

```bash
python devtools/scripts/devguide_issue.py close devguide/archive/resolved_bugs/<file>.md \
    --users "what changed for someone using the library" --dry-run
```

A proposal is archived, never deleted. If one of these questions returns, it returns
with a different premise and deserves a fresh document rather than a revived one.

## Things that are easy to get wrong

- **Do not hand-edit a queue index.** The block between the generated markers is
  rendered from front matter. Edit the entries, then run
  `python devtools/scripts/devguide_index.py`.
- **Do not reference another repository's `devguide/` by path.** Use
  `uibcdf/<repo>#<number>`. A sibling that deletes a closed proposal instead of
  archiving it has already left us with a broken link this way.
- **Do not edit an archived document to correct it.** Append a dated correction note.
  `DOCUMENT_POLICY.md` holds archived material immutable, and rewriting it destroys the
  record of what we believed and when. In the open set, correct in place.
- **Do not retrofit front matter into documents archived before 2026-08-09.** They
  predate the protocol and are exempt by design.
- **`verification` is not the same axis as the evidence labels** in
  `DOCUMENT_POLICY.md`. That one qualifies how well a *feature* is verified; this one
  qualifies how well a *report* is verified. `asserted` is a permitted, honest value.

## Checking your work

```bash
python devtools/scripts/validate_devguide.py        # links, schema, lifecycle, indexes
python devtools/scripts/devguide_index.py --check   # indexes only, writes nothing
python devtools/scripts/devguide_issue.py sync --check   # board agreement; needs gh
```

The first is part of the release gate and runs offline. The third needs the network and
an authenticated `gh`, so it is deliberately not gated.
