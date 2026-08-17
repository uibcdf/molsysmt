---
summary: devguide_issue.py cannot label an issue whose area tags are not already labels on the board.
issue: uibcdf/molsysmt#159
status: open
opened: 2026-08-16
closed:
severity: medium
verification: reproduced
area: [build, docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# Bug: an unknown area tag blocks the whole label synchronisation

**Reported:** 2026-08-16, filing `uibcdf/molsysmt#158` under
[reporting_protocol.md](../reporting_protocol.md). The report's `area:` named
`diagnostics`, which other entries already use and the board does not have, and
the synchronisation step failed.
**Status:** open, cause identified, not started. The *taxonomy* half is gone — every area
tag now has a label — but that was fixed on the board, not here: the all-or-nothing call
is unchanged and unguarded, so the defect returns with the next new area tag. See
*Re-measured*.

## What

`devguide_issue.py sync` fails outright for any report whose `area:` contains a tag
that is not a label on the board. Nothing is applied for that issue — not the area
labels that *do* exist, and not the state label.

```bash
$ python devtools/scripts/devguide_issue.py sync
devguide/pending_bugs/xdist_re_renders_catalog_warnings_on_the_controller.md: uibcdf/molsysmt#158 is missing labels ['diagnostics']
gh issue edit 158 --add-label blocked --add-label tests --add-label diagnostics failed: failed to update https://github.com/uibcdf/molsysmt/issues/158: 'diagnostics' not found
failed to update 1 issue
```

`sync --check` shows the reach:

```bash
$ python devtools/scripts/devguide_issue.py sync --check
... #158 is missing labels ['diagnostics']
... #155 is missing labels ['argdigest', 'performance', 'units']
... #152 is missing labels ['diagnostics', 'digestion', 'form']
... #153 is missing labels ['dependencies', 'digestion']
... #148 is missing labels ['api', 'docs', 'selection']
... #149 is missing labels ['convert', 'form', 'performance']
... #150 is missing labels ['api', 'docs']
... #157 is missing labels ['api', 'argdigest', 'dependencies']

8 entr(ies) drifted.
```

Note `#152`, `#149` and `#150`: they are also missing `form`, `convert` and `docs`,
which *do* exist. Those are collateral — the call that would have applied them is the
one the unknown label rejects.

A single run separates cause from coincidence. `#159` carries `area: [build, docs]`,
both of which exist, and it synchronises; `#158` fails in the same run:

```bash
$ python devtools/scripts/devguide_issue.py sync
... #159 is missing labels ['docs']
  synchronised labels on #159
gh issue edit 158 --add-label diagnostics failed: ... 'diagnostics' not found
failed to update 1 issue
```

### `open` is affected too, and worse

Observed 2026-08-17 while filing `#161`. The defect is not confined to `sync`:
`open` refuses to create the issue at all when `--area` names an unknown tag, so
neither the issue nor its scaffolded document exists afterwards.

```bash
$ python devtools/scripts/devguide_issue.py open --kind proposal \
    --title "Extend the catalog-warning round-trip guard to every warning class" \
    --area diagnostics,tests
gh issue create --title ... --label proposal,diagnostics,tests failed: could not add label: 'diagnostics' not found
```

`sync` leaves an issue with stale labels; `open` leaves nothing, and the filer
has to pick an area tag that already exists on the board rather than the one
that is accurate. `#161` was filed as `area: [tests]` for that reason alone —
`diagnostics` is the second tag it should carry. That is how the drift grows:
the workaround for an unlabelled area is to stop recording the area.

## How

`devtools/scripts/devguide_issue.py:198-207` builds a single `gh issue edit` per
issue and appends every wanted label to it:

```python
add = sorted(wanted - present)
call = ["issue", "edit", str(number)]
for label in add:
    call += ["--add-label", label]
_gh(*call)
```

`gh` validates labels against the repository and rejects the command if any one of
them is unknown, so the operation is all-or-nothing.

`command_open` shares the shape at `:84` and `:101-103`, passing
`",".join(labels)` to `gh issue create`. There the consequence is worse: the issue
is never created, and the protocol's first step — *"Open the issue first, to obtain
the number"* — cannot complete for a report in a new area. This half is by
inspection; no throwaway issue was created to confirm it.

## Why

The script exists to keep the board agreeing with the queues, and the failure is
silent in the direction that matters. `blocked`, `partial` and `in-progress` are
*derived* from `status`, so while an area tag is unknown the board keeps saying a
theme is open and unstarted when the document says it is blocked. A reader outside
the repository sees only the board.

It also produces drift that running the tool cannot clear: `sync --check` returns 1
for eight entries, and `sync` fixes none of them. A check that cannot go green stops
being read.

Severity is `medium`, not higher: no library behaviour is affected, and the labels
can be applied by hand.

## What is measured and what is assumed

Measured, on this checkout at `ca60317da`:

- 8 entries drift, from the `sync --check` output above.
- Board labels absent but used in `area:`: `api`, `argdigest`, `diagnostics`,
  `digestion`, `performance`, `selection`, `units`. Obtained by comparing
  `gh label list` against the `area:` values across `pending_bugs/`,
  `pending_proposals/` and `archive/`.
- The board has `deps`; three documents write `dependencies`. That one is a naming
  mismatch, not a missing label, and creating a `dependencies` label would leave two
  names for one area.

Assumed:

- That `command_open` fails the same way. The mechanism is the same `gh` label
  validation, but it was not executed.

### Re-measured — 2026-08-17

The measurements above were true on their date and are left standing. On this checkout at
`615da28fd` the picture is different:

- The seven labels are on the board: `api`, `argdigest`, `diagnostics`, `digestion`,
  `performance`, `selection`, `units`. Someone created them between 2026-08-16 and today.
- **Zero** of the 16 area tags in use across `pending_bugs/`, `pending_proposals/` and
  `archive/` lack a label. The `deps`/`dependencies` mismatch no longer appears either.
- `sync --check` reports **1** entry drifted, down from 8.

That one entry is worth its own line, because it is not the same defect and it did not
exist when this was filed:

```
devguide/archive/withdrawn_bugs/boundary_digestion_on_internal_predicates.md:
uibcdf/molsysmt#147 is missing labels ['digestion', 'form', 'performance']
```

`#147` is **closed**, withdrawn on 2026-08-13. It became visible to `sync` only because
`615da28fd` added `archive/withdrawn_bugs` to the archive tuple in `devguide_reports.py`,
which had been outside every check. So this row is a blind spot surfacing, not a
regression — but it raises a question this report did not ask: **should `sync` write
labels to closed issues at all?** While it does, `sync --check` cannot return 0 unless
every archived report's issue is labelled to match front matter nobody will revisit, and
the first acceptance criterion below is unreachable for a reason unrelated to the defect.

What has **not** changed is the defect itself. `devguide_issue.py:198-207` still builds one
`gh issue edit` per issue and appends every wanted label to it, so the next area tag that
is not yet a label reproduces the original failure exactly — for `sync`, and worse for
`open`. The board was brought into line by hand; the tool that was supposed to keep it
there was not touched.

## What was refuted

*The report's `area:` was wrong.* First reading, and it is not: `diagnostics` is
already used by `#152`, and `argdigest`, `performance`, `units`, `digestion`,
`selection` and `api` are used by five more. The tags are consistent with the queue;
the board is what is behind.

*It arrived with `#158`.* No — six of the eight drifted entries predate it, three of
them already archived.

## Scope and exclusions

Covers the labelling path of `devguide_issue.py`, both `sync` and `open`.

Excluded: which labels the board *should* have. That is a decision about the label
taxonomy, and resolving it — whether by creating the seven missing labels, by
reconciling `deps`/`dependencies`, or by narrowing what `area:` may contain — is a
question for whoever owns the board, not something this report settles.

Also excluded: `devguide_index.py` and `devguide_reports.py`, which both pass.

## Acceptance criteria

- `python devtools/scripts/devguide_issue.py sync --check` returns 0 on a clean
  checkout.
- An unknown area tag no longer prevents the labels that exist — in particular the
  state label — from being applied. Whether the tool creates the missing label,
  applies what it can and reports the rest, or refuses earlier with a clear message,
  is open; any of the three satisfies this.
- A test covering an area tag with no matching label names the `guard` field.

## Dependencies and risks

None tracked. The risk in the obvious fix — having the tool create labels it does
not find — is that a typo in `area:` silently becomes a label, which is how a
taxonomy stops being one.

## Provenance

Host: this development checkout, molsysmt at `ca60317da`. Python 3.13.14,
`gh` against `uibcdf/molsysmt`. 2026-08-16.
