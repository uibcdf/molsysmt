# Warning counts under parallel test execution

**Role:** operational.
**Evidence:** benchmarked — measurements below, with the commands that produced
them, on this development host on 2026-08-16.

The number of warnings this suite reports is **not reproducible between runs
under `-n 12`**. It is reproducible in serial, and reproducible under
`--dist loadfile`. Anything that compares two warning reports — a baseline, a
"no new warnings" gate, a diff between branches — has to account for that or it
will fail intermittently for reasons unrelated to the change under review.

This is not a defect in pytest-xdist, in pytest, or in molsysmt. It is what a
per-process cache does when the process count changes.

## Measurement

`tests/form/mdtraj_Topology/`, counting occurrences of OpenMM's *"Unlikely unit
cell vectors detected in PDB file"*, recorded per test through a
`pytest_warning_recorded` hook:

| configuration | runs | occurrences | reproducible |
|---|---:|---|---|
| serial | 3 | 2, 2, 2 | yes |
| `-n 12 --dist loadfile` | 3 | 4, 4, 4 | yes |
| `-n 12` (default `--dist load`) | 4 | 30, 32, 34, 40 | **no** |
| `-n 12 -W always` | 3 | 32, 34, 40 | **no** |

Across the whole suite the same effect shows up smaller: the aggregate moved
between 129 and 130 across six runs, and the *set* of tests reported as emitting
the warning changed between runs while its size stayed at seven.

## Why

The PDB behind those tests is read once per process and cached. The first test
in a worker to need it pays the read and emits the warning; every later test in
that same worker hits the cache and emits nothing.

So the count is roughly *how many workers touched that path*, and **which** tests
pay for it depends on how `--dist load` hands work out — which depends on timing.
Twelve workers, twelve cold caches; one process, one.

`-W always` does not help, and measuring that is what rules out the obvious wrong
explanation: the deduplication is not Python's `__warningregistry__` — pytest
already resets warning filters per test — it is the cache. Turning warning
filters up changes nothing because nothing was being filtered.

`--dist loadfile` fixes it by making the distribution deterministic: every test in
a file goes to the same worker, so each cache warms in the same order every run.
The count it produces (4) is not the serial count (2), and does not need to be —
a baseline needs to be *stable*, not minimal.

## Consequences

- **Do not gate on warning counts under the default `-n 12`.** Use
  `--dist loadfile` for such a gate, or run it serially.
- **A diff of two warning reports across runs is not evidence of a change.** Both
  the totals and the emitting test names move on their own.
- The same reasoning applies to any other per-process cache in the suite, not
  just this one. The symptom to recognise is a count that scales with the worker
  count rather than with the number of tests.

This matters beyond housekeeping: `uibcdf/smonitor`'s pytest-bridge proposal
plans warning baselines and a *"newly introduced warning fingerprint"* policy.
Such a gate is only meaningful under a deterministic distribution.

## Reproducing

```bash
# varies between runs
pytest -n 12 -q tests/form/mdtraj_Topology/

# stable
pytest -n 12 --dist loadfile -q tests/form/mdtraj_Topology/
pytest -q tests/form/mdtraj_Topology/
```

To attribute warnings to tests, register a plugin exposing
`pytest_warning_recorded(warning_message, when, nodeid, location)` and append
`nodeid` with the message text; under xdist the hook fires on the workers, so the
file has to be opened per write with `O_APPEND`.
