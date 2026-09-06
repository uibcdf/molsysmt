---
summary: puw.parse.parse lets pint's UndefinedUnitError escape the length digesters
issue: uibcdf/molsysmt#203
status: resolved
opened: 2026-09-06
closed: 2026-09-06
severity: medium
verification: reproduced
area: [argdigest, units]
guard: tests/_private/argdigest/test_digester_contract.py::test_a_string_that_is_not_a_quantity_is_refused_as_an_argument
normative:
blocked_by: []
supersedes: []
---

# The same bad input arrived as two different exceptions

**Reported:** 2026-09-06 from `uibcdf/molsysviewer`, while synchronising that project's
copies of these digesters with ours. Offered rather than reported as breakage: nothing
downstream depended on the behaviour, and the viewer had already contained it on its side.
**Status:** resolved.

## What

A string that does not parse as a quantity left the digester as the unit registry's own
exception instead of as `ArgumentError`.

```python
>>> digest_threshold("hola", caller="molsysmt.structure.get_contacts.get_contacts")
pint.errors.UndefinedUnitError
>>> digest_threshold(3, caller="molsysmt.structure.get_contacts.get_contacts")
molsysmt._private.smonitor.exceptions.ArgumentError
```

So the same class of bad input reached the caller as two different exception types
depending on whether it was written as a string or as a bare number, and the one that
escaped named pint rather than the argument. It carried no `caller`, no argument name,
and none of the catalogue's documentation links.

## How

The string branch was unguarded:

```python
if isinstance(threshold, str):
    threshold = puw.parse.parse(threshold)
```

`coordinates.py` already did the right thing — its whole body sits inside a `try` that
re-raises as `ArgumentError` — so the fix is that shape, factored into
`argument/_quantity_parsing.py` and used by every digester that parses a quantity string.
The `cause` parameter of `ArgumentError`, present since the exception was written and
until now unused, carries the parser's own type and message into the structured record.

## Why

An argument error is the one class of failure a user is guaranteed to meet, and the
boundary exists so that it names the argument, the caller and the remedy. An exception
from a transitive dependency does none of that, and it makes the failure look like a
library defect rather than a typo. The inconsistency is the sharper half: a caller writing
`except ArgumentError` caught the bare number and missed the string.

## What is measured and what is assumed

**Measured:** the report named five files. The same unguarded pattern was present in
**twenty**, all of `argument/`'s quantity digesters except `coordinates.py`. All twenty
raised `UndefinedUnitError` for `'definitely-not-a-unit'` before the change and
`ArgumentError` after it.

```bash
grep -rln "puw.parse.parse" molsysmt/_private/argdigest/argument/*.py | wc -l
21   # the twentieth-first is coordinates.py, already guarded
```

Fixing only the five named would have left fifteen instances of the same defect, and no
gate over the class could have been written, so the fix covers the family.

**Measured, found while there:** two digesters raised `AttributeError` rather than
`ArgumentError` when called without a caller — `switch_distance`, whose
`caller.startswith` had no `None` guard although its neighbour `cutoff_distance` did, and
`value`, whose every branch dispatches on the caller. Both now refuse at the boundary.

**Not measured:** whether other digesters mishandle `caller=None`. The two above were
found by the sweep this guard performs, which passes `caller=None` deliberately; a
digester outside the quantity-parsing family is not covered by it.

## What was refuted

**That the parse failure should be allowed to propagate for diagnosis.** It reads as
better information and is not: the parser's message names the token it could not resolve
but not the argument it came from, and the digester knows both. `cause=` keeps the
parser's own type and message in the structured record, so nothing is lost.

## Scope and exclusions

Covered: every digester under `molsysmt/_private/argdigest/argument/` that parses a
quantity string, and the two caller-dispatch crashes found by the sweep.

Not covered: the drift the report also mentions, `molsysmt.thirds.` versus
`molsysmt.third_party.` in the viewer's copy of `threshold.py`. That one ran the other
way and was fixed on their side; ours already names `molsysmt.third_party`.

## Acceptance criteria

- Every quantity-parsing digester refuses an unparseable string with `ArgumentError`.
  The guard discovers the set from the source, so a digester that starts parsing strings
  is covered the day it is written. Confirmed to report all twenty against the previous
  code.

## Provenance

Linux, Python 3.13.14, `pint` through `pyunitwizard`, `molsysmt` at working tree
`c40f46559`, 2026-09-06.
