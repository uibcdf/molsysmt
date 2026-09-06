---
summary: n_nucleotides is the one attribute of 118 with no digester, so it accepts anything
issue: uibcdf/molsysmt#208
status: resolved
opened: 2026-09-06
closed: 2026-09-06
severity: medium
verification: reproduced
area: [argdigest, attribute]
guard: tests/_private/argdigest/test_digester_contract.py::test_every_attribute_has_a_digester
normative:
blocked_by: []
supersedes: []
---

# One attribute of 118 was never validated

**Reported:** 2026-09-06, from `uibcdf/molsysviewer`, where the missing digester was
warning on every legitimate call in the viewer's own suite.
**Status:** resolved.

## What

`n_nucleotides` had no module in `molsysmt/_private/argdigest/argument/`, so nothing
validated it. It accepted any type and answered 0.

```python
>>> msm.get(molsys, element='system', n_nucleotides=True)               # 0, with a warning
>>> msm.get(molsys, element='system', n_nucleotides="no soy booleano")  # 0, silently
```

Its siblings refuse that. `n_peptides`, `n_dnas` and `n_rnas` accept a `bool` from
`molsysmt.basic.get.get`, a `bool` or an `int` from `contains` and `is_composed_of`, and
raise `ArgumentError` otherwise.

Every legitimate call also emitted `DigestNotDigestedWarning: No digester for
n_nucleotides`.

## How

The digester dispatch resolves an argument to the module of its own name under
`molsysmt/_private/argdigest/argument/`. With no module there, ArgDigest warns and skips
validation rather than failing, which is the correct behaviour for a partially declared
package and the reason the gap stayed invisible.

The fix adds `n_nucleotides.py`, identical in contract to `n_peptides.py` — the same
three callers, the same accepted types — because the attribute is used in exactly the
same way. `contains` and `is_composed_of` were confirmed to accept it before the
whitelist was written, and `molsysmt.native.topology.Topology.__init__` was confirmed not
to take it.

## Why

An attribute that is not validated is not merely unguarded: a string reaches the
attribute machinery and is answered with 0, which reads as *this system has no
nucleotides* rather than as *that is not a valid request*. The value is plausible and the
question was never asked.

The gap is now closed structurally rather than by one module: the guard fails if any
attribute in `molsysmt.attribute.attributes` has no digester, so the next omission is
caught when it is written and not by a downstream project's warning count.

## What is measured and what is assumed

**Measured:** 118 attributes in `molsysmt.attribute.attributes`, 117 with a digester
module, one without.

```bash
python -c "
import pathlib
from molsysmt.attribute import attributes
mods = {p.stem for p in pathlib.Path('molsysmt/_private/argdigest/argument').glob('*.py')}
print(len(attributes), sorted(a for a in attributes if a not in mods))"
118 ['n_nucleotides']
```

**Measured:** both calls above, before and after. The string is now refused with
`ArgumentError`, and the warning count for a legitimate call drops from one to zero.

**Reported upstream, not measured here:** three of the seventy-one warnings in
MolSysViewer's suite came from this attribute.

## What was refuted

**That this was a decision rather than an omission.** The attribute is fully served
everywhere else — it appears in `molsysmt/basic/get.py` among the composition counts, and
the forms implement its getters at every element level. Nothing in the tree treats
`n_nucleotides` as special; only the digester was absent.

## Scope and exclusions

Covered: the missing digester, and a structural guard over the whole attribute
catalogue.

Not covered: whether each of the 117 existing digesters accepts the right values. The
guard checks that a digester exists and is callable, which is what can be established
structurally; what a given digester refuses stays with its behavioural test.

## Acceptance criteria

- An attribute without a digester module fails the suite. Confirmed to fail with
  `n_nucleotides.py` removed.
- `msm.get(molsys, n_nucleotides="...")` raises `ArgumentError`.
- A legitimate `n_nucleotides` call emits no warning.

## Provenance

Linux, Python 3.13.14, `molsysmt` at working tree `8064a87fa`, 2026-09-06.
