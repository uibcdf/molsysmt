---
summary: Extend the catalog-warning round-trip guard to every warning class
issue: uibcdf/molsysmt#161
status: resolved
opened: 2026-08-17
closed: 2026-08-19
verification: reproduced
area: [diagnostics, tests]
guard: tests/_private/smonitor/test_xdist_warning_reconstruction.py
normative:
blocked_by: []
supersedes: []
---

# One warning class is guarded against re-rendering; ten are not

**Reported:** 2026-08-17, auditing what `uibcdf/molsysmt#158` left behind after
the fix landed in `smonitor 0.13.0`.
**Status:** open, not started. The defect it guards against is fixed; what is
missing is the guard's reach.

## What

`tests/_private/smonitor/test_xdist_warning_reconstruction.py` asserts that a
catalog warning crossing from an xdist worker to the controller is not rendered
twice. It exercises `UnknownAtomNameWarning` and nothing else.

`molsysmt/_private/smonitor/warnings.py` declares eleven catalog warning classes
with their own `__init__`:

```bash
$ awk '/^class /{c=$2} /def __init__/{print c}' molsysmt/_private/smonitor/warnings.py
MolSysMTCatalogWarning(CatalogWarning):      # base
CrossChainCovalentBondsWarning
NotDigestedArgumentWarning
MolecularSystemMismatchWarning
StructuralAttributeOffAxisWarning
StructuralAttributeDropWarning
IncompatibleBoxWarning
BioassemblyIdentifierCollisionWarning
SlowChunkIOWarning
MemoryPressureWarning
UnknownAtomNameWarning
GpuNotAvailableWarning
```

Plus `SelectionWarning` and `DownloadWarning`, which inherit their constructor
and would regress if the base ever transformed its message again.

The proposal is to parametrise the guard over every concrete subclass, and to
make the parametrisation *discover* classes rather than list them.

## How

Discovery, not enumeration, is the whole point. A test that hardcodes eleven
names has the same hole as a test that hardcodes one: the twelfth class is not
covered, and nobody notices.

The design, in two parts:

1. **Discover** every concrete subclass of `MolSysMTCatalogWarning` by walking
   `__subclasses__()` recursively. This is what makes the guard self-extending.
2. **Require** each discovered class to appear in a registry of sample field
   values inside the test module, and fail when one is missing. Building with
   the constructor defaults alone would pass trivially — every field defaults to
   `None` — and would not exercise a template that needs a real value.

Each entry then goes through the existing `_round_trip` helper and asserts what
the current test asserts for one class: the rendered sentence appears once, and
the field value survives.

The failure a new class must produce is "you added `FooWarning`, add its sample
values here", not silence.

## Why

The shape a catalog warning class must take is not enforced by anything. A class
written the old way — a domain field first, positionally — does not raise, does
not fail import, and does not fail any test. It simply stops surviving
`type(w)(*w.args)`, which is how `pickle`, `copy.deepcopy`, `warnings.warn(text,
category)` and pytest-xdist all rebuild a warning. The user sees the template
applied to its own output:

```
Atom name 'Atom name 'Ar' is not recognized.' is not recognized.
```

That is `#158`, and it reached users before it reached the suite.

There are 377 uncommitted files in the working tree as this is filed. Whatever
warning classes that work adds are outside the guard's reach today.

## What is measured and what is assumed

Measured: eleven classes declare `__init__`, one is exercised by the guard, and
the eleven were reshaped to the message-first form during the `#158` fix.

Assumed, and worth stating plainly: that the current eleven are all correct. The
audit that reshaped them was a bulk edit followed by a review, not a
per-class round-trip assertion — the assertion is what this proposal adds. It is
possible the parametrised guard fails on its first run. That would be a result,
not a setback.

Estimate: half an hour, discovery and registry included.

## What was refuted

**Enumerating the eleven class names in `@pytest.mark.parametrize`.** Simpler,
and it leaves exactly the hole that motivates this. Rejected.

**Enforcing the shape in the base class instead of in a test.** A
`__init_subclass__` on `MolSysMTCatalogWarning` could inspect the signature and
reject a subclass whose first parameter is not `message`. It fails at import,
which is earlier and louder than a test. It was rejected for now on two counts:
it belongs in SMonitor's base rather than in MolSysMT's, since every consumer
has the same exposure; and a signature check does not catch a class whose
`__init__` transforms the message even with the right parameter order. A
round-trip assertion catches both. The enforcement idea is recorded in
`smonitor/devguide/pending_proposals/hint_ownership_on_catalog_instances.md`,
where the question of what the base classes own is being decided for 1.0.

## Scope and exclusions

Covers the catalog warning classes in `molsysmt/_private/smonitor/warnings.py`.

Does **not** cover catalog *exceptions*, which have the same exposure through the
same rebuild protocol and no guard at all. That is deliberate — it is a second
piece of work, and bundling it would delay this one — but it should not be
forgotten.

Does not cover the residue documented upstream: a hint whose template
interpolates a field cannot be re-rendered from `args` alone, because the field
is not there. No class shape fixes that; it waits on
`pytest-dev/pytest-xdist#1372`.

## Acceptance criteria

- Every concrete subclass of `MolSysMTCatalogWarning` is exercised, and adding a
  new subclass without registering sample values fails the suite.
- Each class round-trips with its rendered sentence appearing exactly once and
  its field values intact.
- The `guard` field names the resulting test.

## Dependencies and risks

Requires `smonitor >= 0.13.0`, already the floor in `pyproject.toml`. Note that
`devtools/requirements/controlled_hard_dependencies.txt` installs with
`--no-deps`, so the pinned revision there is what CI actually gets; it was
refreshed on 2026-08-16 from a revision predating `0.12.0`.

Risk: none to runtime. The change is test-only.

## Provenance

Counts taken on 2026-08-17 from `molsysmt/_private/smonitor/warnings.py` at
`d0e90f423`, with `smonitor 0.13.0`.

## Resolution — 2026-08-19

The guard covers every warning class and is self-extending. One test became 19.

### Discovery is by module, not by base class

The proposal said to walk `MolSysMTCatalogWarning.__subclasses__()`. That was the
wrong root, on two counts found while implementing it. `__subclasses__()` only sees
classes that have been imported, and it excludes `MolSysMTDeprecationWarning`, which
inherits `DeprecationWarning` deliberately so Python's own tooling treats it as a
deprecation. The invariant is not which base a class hangs off but whether its own
`__init__` renders a template — that is what `cls(*args)` can double. Discovery now
walks every `Warning` subclass defined in `molsysmt/_private/smonitor/warnings.py`,
which is the single file that defines them.

### The registry, as proposed

Each discovered class must appear in `SAMPLES` with field values and a fragment that
must appear in the rendered sentence or in `extra`. Building from the defaults would
render nothing, so the fragment is what proves the sample exercised the constructor.
Two tests keep the registry honest in both directions: a class with no sample fails,
and a sample for a class that no longer exists fails.

The fragment is looked for in the sentence *or* in `extra` because the classes split
into two kinds. `UnknownAtomNameWarning` interpolates its field into the sentence;
`MolecularSystemMismatchWarning` renders a fixed sentence and carries `caller` and
`count` as structured payload. Both consumed the field; only one shows it.

### One check the proposal did not ask for

Every declared `catalog_key` must exist in the catalog. A class pointing at a missing
key fails quietly: `_catalog_entry` returns nothing, `code` stays `None`, and the
warning still raises with whatever text the caller passed. Verified by mutation —
pointing `GpuNotAvailableWarning` at `NoSuchKey` fails the test with the dangling
pair named.

### What was refuted

*The eleven current classes might be wrong, and the parametrised guard might fail on
its first run.* The proposal said so and said it would be a result rather than a
setback. They are all correct: the run was green on the first parametrised pass.

*The structured payload is lost on the round trip because of how the classes are
shaped.* It is lost, but the cause is xdist's protocol, not the classes.
`xdist.remote.serialize_warning_message` transfers `message_str`, the class name and
`args`, never `__dict__`, and the controller rebuilds with `cls(*args)`. `pickle` and
`copy.deepcopy` preserve the payload in full because they restore `__dict__`.

An earlier revision of this work was about to assert that loss as expected
behaviour, and to file it upstream as an SMonitor defect. Both would have been
wrong. SMonitor's design is well suited to the constraint: putting the un-hinted
message in `args` and making `__init__` idempotent over it is precisely what makes
the text cross intact, and its own source says so. Nothing to change upstream. What
is written now is the consequence for callers: code on the controller must branch on
the text, not on `extra`.

### Four catalog keys with no class

`AmbiguousStructureWarning`, `MultiContainerWarning`, `SupportTier2Warning` and
`MolSysMTDeprecationWarning` appear in the catalog without a catalog-warning class.
None is a gap: the first two are emitted by passing the catalog entry to `warn()`
directly, the third is emitted by SMonitor's tier registry, and the fourth is a
`pass` with no template to double. Checked rather than assumed.

Full suite: 10 118 passed, 11 skipped.
