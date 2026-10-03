---
summary: Optional attribution diagnostic failures interrupt recognition
issue: uibcdf/molsysmt#295
status: resolved
opened: 2026-10-03
closed: 2026-10-03
severity: medium
verification: measured
area: [diagnostics, physchem]
guard: tests/physchem/test_get_cip_stereochemistry.py
normative:
blocked_by: []
supersedes: []
---

# Optional attribution diagnostic failures interrupt recognition

**Reported:** uibcdf/pharmacophoremt#19; original provider report #295.
**Status:** Resolved. The warning-promotion path was fixed in #305; this correction
also protects diagnostic import, construction and emission on the original report.

## What

Optional Ackredit failures must preserve scientific recognition under strict
warning filters. The original filter-promotion path is already guarded by
`tests/test_ackredit.py` after `174f2bfec`. Diagnostic import, construction and
emission must also remain outside the scientific exception boundary.

## How

`_ackredit._failed` imported and constructed its diagnostic before its protective
handler and only isolated promotion of the same warning instance. A constructor
or emitter failure escaped and replaced the completed result. Move import,
construction and emission into the isolated diagnostic boundary. Preserve the
ordinary catalog event and its exact warning promotion; if that path fails,
emit a fallback log with the signal code, caller, operation and both errors as
required by `SMONITOR_GUIDE.md` section 3.4. Do not silently discard diagnostics,
change warning filters, or catch exceptions from the science body.

## Why

PharmacophoreMT reported recognition failure when optional attribution failed.
The provider boundary is reusable across preparation, recognition and interaction
calculations. Consumers must not patch it privately or lose completed science
because an auxiliary attribution diagnostic failed.

## What is measured and what is assumed

**Reproduced:** A real Ackredit session with controlled `register_item` failure
under `warnings.simplefilter('error')` preserves the alanine S label on existing
main `3e1eea3cd`. Diagnostic constructor and emitter fault injection each replace
that label with `RuntimeError`. The initial selection passed one case and failed
two in 3.93 seconds; it deselected 19 unrelated cases. This confirms the #305
filter correction and the remaining boundary failure separately.

The control uses actual RDKit CIP labeling with independently known L-alanine S
configuration, retains detached references and requires source binary identity.
Catalog events are inspected with SMonitor MemoryHandler; fallback records must
retain the original provider and diagnostic failures. This is controlled failure
evidence, not a claim that Ackredit currently fails registration in normal use.

## What was refuted

- #295 is fully represented by the already resolved #305: warning promotion is
  covered, but import/construction/emission failures were still exposed.
- A scientific exception should be caught at this boundary: the science body
  remains outside attribution-specific exception handling.

## Scope and exclusions

Shared optional attribution boundary and original consumer failure contract.
Preserve current catalog behavior and ordinary warnings. No change to Ackredit,
PharmacophoreMT, chemistry algorithms, dependency floors or host warning policy.

## Acceptance criteria

- Real Ackredit failure under warnings-as-errors preserves known recognition,
  detached references and source immutability, without credits for failed tracking.
- Diagnostic import, constructor and emitter failures retain a structured fallback
  log instead of replacing recognition or its original scientific exception.
- The ordinary catalog event remains visible; unrelated scientific warnings and
  actual scientific failures propagate unchanged.

## Provenance

Linux x86_64, Python 3.13.14 under uibcdf/molsysmt#237, released ArgDigest 0.13.0
snapshot `9880fa7b990fd0987ff0de715b665eb9e11c11b2`, 2026-10-03.
Ackredit checkout `30369ac4ddc2ca4af60c37568489132aace72263` has nine existing dirty
entries and is three commits behind origin; its editable reported version is
`0.5.0+34.g115a152.dirty`. PharmacophoreMT has 175 existing dirty entries and is ten
commits behind origin. Both worktrees are preserved; this does not freeze a clean
published component pair.
Command: `env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest
--receptor=llm tests/physchem/test_get_cip_stereochemistry.py -k real_ackredit_failure`.

## Resolution — 2026-10-03

The shared failure handler now protects its entire diagnostic path. Promotion of
the same catalog warning retains its existing SMonitor event without a duplicate.
Import/construction/emission failures use a fallback log with signal code, caller,
operation, provider error and diagnostic error. Provider exceptions that cannot
format still retain their exception type. This fallback is specifically permitted
by `SMONITOR_GUIDE.md` section 3.4; no scientific criteria or warning filters change.

The public guard invokes real Ackredit registration inside a session and requires
the known alanine S label, original source bytes, detached scientific reference and
no claimed credits after controlled failure. Ordinary warning promotion requires
an actual SMonitor event; diagnostic failures require the fallback log's contextual
fields. `tests/test_ackredit.py` additionally requires original scientific exception
identity during failed cleanup and propagation of unrelated scientific warnings.

The final selection passed **104 tests in 39.04 seconds**, including the public
CIP doctest, shared boundary, recognition, native template preparation, pinned EST
controls and interaction attribution:

```bash
env PYTHONPATH=/tmp/molsysmt-readiness-argdigest-013 python -m pytest --receptor=llm \
  tests/test_ackredit.py tests/physchem/test_get_cip_stereochemistry.py \
  tests/physchem/test_chemical_template.py tests/physchem/test_chemical_template_est.py \
  tests/interactions/test_scientific_attribution.py \
  --doctest-modules molsysmt/physchem/get_cip_stereochemistry.py
```

Its two existing pandas FutureWarnings come from the chemical-state H5MSM reader.
Ruff, public signature/docstring checks, developer-guide and canonical course gates
pass. Public docstrings, Foundations, Toolbox, Cookbook and course Module 12 state
the behavior. Notebook code and outputs are preserved. This is local provider
evidence with the preserved editable Ackredit checkout, not certification of the
complete PharmacophoreMT workflow or a clean published package pair.
