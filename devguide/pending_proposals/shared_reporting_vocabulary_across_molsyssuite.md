---
summary: A reporting vocabulary every MolSysSuite tool can adopt unchanged.
issue: uibcdf/molsysmt#156
status: open
opened: 2026-08-17
closed:
verification: measured
area: [docs]
guard:
normative:
blocked_by: []
supersedes: []
---

# A reporting vocabulary every MolSysSuite tool can adopt unchanged

**Reported:** 2026-08-14 as `uibcdf/molsysmt#156`, from MolSysViewer, after it adopted
this repository's reporting protocol. Attended here on 2026-08-17.
**Status:** open. The ownership question the issue asks is decided (see *Decision*); the
work that follows from it has not started.

## What

Extract the domain-free part of [`reporting_protocol.md`](../reporting_protocol.md) — the
required front-matter fields and the accepted values of `status` and `verification` — into
a small declarative file, so that a MolSysSuite tool can adopt it whole and have
`uibcdf/<repo>#<number>` mean the same thing from its first day. Each repository keeps its
own validator, index generator and board sync written against that data.

The proposal carries an exclusion that is doing real work: the evidence labels of
[`DOCUMENT_POLICY.md`](../DOCUMENT_POLICY.md) — *Implemented*, *Contract-tested*,
*Parity-tested*, *Scientifically validated*, *Benchmarked* — must **not** enter the shared
set. Not as an exemption for MolSysViewer, but because they cannot be universal: two of the
five are questions only a library with equivalent forms and an independent oracle can ask.
The test the issue proposes for anything else offered to the shared set is the same one:
*if a new MolSysSuite tool could not use it on its first day, it does not belong there*.

The distinction behind it is worth keeping in these words: **a report is a report in any
repository; a capability belongs to the domain.**

## Decision

The vocabulary evolves in two phases, and we are in the first:

1. **Phase 1 — developed from MolSysMT.** This repository owns and develops the
   vocabulary. The siblings adopt it from here.
2. **Phase 2 — exported and agreed.** It moves to a consensus repository that issues it,
   with its own rules written there.

For MolSysViewer this answers what it asked in order to size its investment: the source
of the vocabulary **is** destined to move, so a copy made today is temporary in its
origin, not in its content. What it should not do is adapt the shared fields and values to
its own queues — those are the part that must stay identical across phases.

The issue's own concrete question was about the **tooling**, and it is not settled by this
decision. The issue already argues against sharing it — validators, index generators and
board sync depend on each repository's queue shapes and label set — and records that a
shared package was considered and rejected there, because it would put a new dependency in
five release gates with no clear owner. Phase 2 is where that argument gets written down as
a rule rather than left as a preference.

## How

The vocabularies already live in exactly one place in this repository, as module constants
in `devtools/scripts/devguide_reports.py`: `REQUIRED_FIELDS`, `KNOWN_FIELDS`,
`OPEN_STATUSES`, `CLOSED_STATUSES`, `VERIFICATIONS`, `SEVERITIES`. That module's docstring
already states the reason — the schema is described once and shared by
`validate_devguide.py`, `devguide_index.py` and `devguide_issue.py`.

So Phase 1 is small: move those constants into data under `devtools/data/`, beside
`devguide_migration_baseline.json`, have `devguide_reports.py` read them, and make
[`reporting_protocol.md`](../reporting_protocol.md) §*Scope beyond this repository* name
that file as the source instead of describing the vocabulary in prose twice.

One constraint the parser imposes: `devguide_reports.py` accepts a deliberately restricted
YAML subset and runs on a bare interpreter in `ci-devguide.yaml`, with no PyYAML available.
The vocabulary file must therefore be JSON, like the migration baseline, or stay inside the
same restricted subset.

## Why

[`reporting_protocol.md`](../reporting_protocol.md) §*Scope beyond this repository* already
declares that the same front matter and the same vocabularies apply to `argdigest`,
`depdigest`, `pyunitwizard`, `smonitor` and `molsysviewer`, and that this uniformity is
what makes `uibcdf/<repo>#<number>` a reliable reference in every direction. That claim
holds only while the vocabularies mean the same thing everywhere, and today they are prose
in two repositories with nothing keeping them equal. A third adopter copies from whichever
happens to be open.

The evidence that they travel is not an argument, it is an adoption: the vocabulary was
taken into a *viewer* without adapting a word, and fits its queues.

## What is measured and what is assumed

Measured on 2026-08-17, on the local checkouts, with:

```bash
python - <<'PY'
import re, pathlib
root = pathlib.Path('/home/diego/repos@uibcdf/molsysviewer/devguide')
n, fields = 0, set()
for d in ('pending_bugs', 'pending_proposals'):
    for p in (root / d).rglob('*.md'):
        if p.name == 'README.md':
            continue
        text = p.read_text(encoding='utf-8')
        if not text.startswith('---'):
            continue
        n += 1
        fields |= set(re.findall(r'^([a-z_]+):', text[3:text.find('\n---', 3)], re.M))
print(n, sorted(fields))
PY
```

- MolSysViewer carries `devguide/reporting_protocol.md`, adopted 2026-08-14.
- **29** of its pending documents carry front matter. The issue reported 28 three days
  earlier; the queue grew by one. Neither number is a contract.
- The field set in use there is exactly the twelve this repository declares: `summary`,
  `issue`, `status`, `opened`, `closed`, `severity`, `verification`, `area`, `guard`,
  `normative`, `blocked_by`, `supersedes`.
- The `status` values in use (`open`, `blocked`, `partial`) and the `verification` values
  (`inspected`, `measured`, `reproduced`) are subsets of the vocabularies here.
- The divergence the issue describes is real and visible:
  `molsysviewer/devguide/capability_audit.md` classifies capabilities with
  `browser-observed` beside `contract-tested`.
- No sync mechanism exists on the MolSysViewer side for the root integration guides: no
  reference to `ARGDIGEST_GUIDE.md` or `SMONITOR_GUIDE.md` under its `devtools/` or
  `.github/`. Today those guides are copied by hand.

Assumed:

- That the two `reporting_protocol.md` documents state identical vocabularies *in prose*
  today. This is not established. A table-shape comparison written against this
  repository's formatting matched nothing in the sibling's file, which measures the
  regular expression rather than the documents. What is established is the field set
  actually in use, above — which is the stronger evidence anyway, because it is what the
  documents are for.

## What was refuted

- *That MolSysViewer is asking for an exemption.* It is not. The three divergences it
  lists — single-theme reports only in the queues, a flat archive, and open/close written
  by hand rather than by script — are recorded as local shapes, and it argues that none of
  them should be inherited by a future tool.
- *That the evidence labels are a candidate for the shared set.* Its own adoption refutes
  it: applying them to a viewer's capability audit, `Parity-tested` and *Scientifically
  validated* could not be earned, and two labels meaningless in a library without an
  interface had to be added.
- *That this is a large change here.* The vocabularies are already centralized in one
  module; the work is moving constants into data with a single consumer. The cost of the
  proposal is not the refactor, it is the ownership.

## Scope and exclusions

Covers the shared vocabulary and how it is distributed, in both phases.

Excluded:

- the tooling, per *Decision* above;
- the evidence labels of `DOCUMENT_POLICY.md`, permanently;
- this repository's own label taxonomy, and the `deps`/`dependencies` mismatch, which
  belong to [`devguide_issue_sync_fails_on_unknown_area_labels.md`](../pending_bugs/devguide_issue_sync_fails_on_unknown_area_labels.md);
- the choice of consensus repository for Phase 2, which is not a MolSysMT decision.

## Acceptance criteria

The outcome is a rule rather than a behaviour, so this closes on `normative`, not `guard`.

Phase 1:

- the required fields and the `status` / `verification` vocabularies exist as data,
  consumed by `devguide_reports.py`, with no second prose copy in this repository;
- `reporting_protocol.md` §*Scope beyond this repository* names that file as the source
  and states that MolSysMT owns it during Phase 1;
- the file loads on a bare interpreter, as `ci-devguide.yaml` requires;
- `validate_devguide.py` and `devguide_index.py --check` stay green.

Phase 2 is a separate document. It closes when the vocabulary is issued from the consensus
repository with its rules written there, and this repository consumes it like any other
adopter.

## Dependencies and risks

Not blocked.

The risk is the one the phases exist to manage: a vocabulary owned here and adopted
outward makes this repository responsible for a schema that five repositories validate
against, so a value added for a local need silently becomes an ecosystem change. During
Phase 1 the control is the issue's own test — if a new tool could not use it on day one,
it does not belong in the shared set. Phase 2 replaces that self-restraint with written
rules and a neutral owner, which is why it exists.

## Provenance

Host: this development checkout. `molsysmt` at `b5266dbf0`, `molsysviewer` at `c91a608d`.
Python 3.13.14. 2026-08-17.
