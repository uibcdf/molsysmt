---
summary: Public signature guard treats local private helpers as public API
issue: uibcdf/molsysmt#315
status: resolved
opened: 2026-10-04
closed: 2026-10-04
severity: medium
verification: reproduced
area: [api, tests]
guard: devtools/tests/test_validate_public_api_stability.py
normative:
blocked_by: []
supersedes: []
---

# Public signature guard treats local private helpers as public API

**Reported:** 2026-10-04 during reusable chemistry-digest factoring for uibcdf/molsysmt#222.
**Status:** Resolved; public signatures remain protected and private implementation scope is excluded.

## What

`python devtools/scripts/validate_public_api_stability.py` reported that public
function `table` was removed from `_private/partial_charges.py`, although it was
a local closure inside `_digest` and never exposed to callers.

## How

The signature extractor walked every AST function with a non-underscore name,
without considering its lexical parents or the private source module. Class
methods also shared unqualified names, allowing collisions between classes.

## Why

A legitimate private refactor failed a public compatibility gate. A waiver or
unused replacement helper would satisfy the gate without preserving a real
user contract. Other module functions, methods and conditional public definitions
still need protection against actual parameter loss or default changes.

## What is measured and what is assumed

**Reproduced:** The unchanged scientific digest was moved to a shared private
helper; the guard failed on the unexposed closure, not on an exported signature.
**Contract-tested:** Tests cover local/private exclusion, class qualification,
module-level conditional definitions and real public function/method parameter
removal. Numerical/scientific validation is not a claim of this tooling fix.

## What was refuted

No public `table` export or API removal exists. Preserving a dead helper or adding
a broad waiver was rejected; both would hide the scope defect.

## Scope and exclusions

The existing AST signature guard is corrected, without changing its signature
comparison semantics or release policy. It does not become a full export resolver;
the separate API stability registry still owns declared public exports.

## Acceptance criteria

Private refactors pass; actual public parameter removals fail. The guard tests
assert both outcomes, so ignoring all changes cannot pass.

## Resolution

Track nonlocal public definitions, qualify class methods, exclude private modules
and local closures/classes, and preserve conditional module definitions. Local
Ruff and the unchanged public-signature comparison pass. Focused execution is
recorded alongside the final checkpoint; no full platform matrix is claimed.


## Local checkpoint

On 2026-10-04, `python -m pytest --receptor=llm
devtools/tests/test_validate_public_api_stability.py
tests/basic/test_set_mechanical_atom_types.py tests/basic/test_set_partial_charge.py`
passed 28 cases in 4.39 seconds. Python 3.13.14 is the bounded development
runtime (uibcdf/molsysmt#237), using the released ArgDigest 0.13 source snapshot
at `9880fa7b990fd0987ff0de715b665eb9e11c11b2`. These focused controls do not
establish a full platform matrix or release qualification.
