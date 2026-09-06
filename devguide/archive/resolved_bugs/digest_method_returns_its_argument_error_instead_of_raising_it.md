---
summary: digest_method returns its ArgumentError instead of raising it, so the guard is inert
issue: uibcdf/molsysmt#209
status: resolved
opened: 2026-09-06
closed: 2026-09-06
severity: low
verification: reproduced
area: [argdigest, molecular_mechanics]
guard: tests/_private/argdigest/test_digester_contract.py::test_no_digester_returns_the_error_it_should_raise
normative:
blocked_by: []
supersedes: []
---

# A digester that cannot refuse anything

**Reported:** 2026-09-06, reading `molsysmt/_private/argdigest/argument/method.py` while
auditing the digester family. Both of its eleven lines were wrong, in different ways.
**Status:** resolved.

## What

`digest_method` refused nothing. Its terminal statement built an `ArgumentError` and
**returned** it, so the error object became the digested value of the argument and was
handed to the function body as if the user had passed it.

```python
>>> from molsysmt._private.argdigest.argument.method import digest_method
>>> out = digest_method('L-BFGS')
>>> type(out).__name__, isinstance(out, BaseException)
('ArgumentError', True)
```

`potential_energy_minimization` carries `@arg_digest()` and declares `method='L-BFGS'`.
Its own default digested into an error object stating that the default is invalid.

The second path was dead. The one whitelisted caller was
`molsysmt.structure.align.align`, which is not in the tree: `molsysmt/structure/` holds
`align_principal_axes.py` and `least_rmsd_align.py`, and no `align.py`. So the
fall-through was the only path the digester had.

## How

`molsysmt/_private/argdigest/argument/method.py:11`, `return` where every one of the
other 390 modules in that directory writes `raise`.

The fix makes the digester refuse by raising, and replaces the unreachable caller
whitelist with the value contract that is actually implemented. `method` reaches exactly
one surface, and OpenMM's `LocalEnergyMinimizer` implements one algorithm, so `'L-BFGS'`
— case-insensitively, normalized like `engine` and `to_form` — is the only value the
minimization can honour.

## Why

Nothing observable was wrong for a user, and that is why the severity is `low` rather
than higher: the body of `potential_energy_minimization` never reads `method`, so no
call returned a wrong answer. `potential_energy_minimization` is classified
`outside-contract` in `devtools/data/public_api_stability.json`.

What was missing is the guard. Every other digester refuses a bad value by raising; this
one could not refuse anything, and a misspelled algorithm name was accepted in silence.
The day the argument is read, or a second callable declares one by that name, the failure
would not be an `ArgumentError` at the boundary — it would surface far from the digester
that existed to prevent it.

## What is measured and what is assumed

**Measured:** the reproduction above, run on the working tree at `ebfc72ace`.

**Measured:** an AST scan of `molsysmt/_private/argdigest/` reports `method.py:11` as the
only `return` of an exception constructor in the tree. The defect was isolated, not a
family.

**Measured:** an AST scan for a `method` parameter over `molsysmt/**/*.py` finds two
functions — `potential_energy_minimization` and the `NotImplementedMethodError`
constructor, which is not digested. So one surface, not several.

**Inspected:** `LocalEnergyMinimizer.minimize` takes no algorithm selector. That L-BFGS
is OpenMM's only local minimizer is upstream documentation, not a MolSysMT measurement.

## What was refuted

**That the argument should simply be removed.** It is declared, documented and ignored,
which is the deeper defect, and deleting it would end the question. It was not done here:
removing a public argument is an API decision, `potential_energy_minimization` is a
documented surface with a User Guide page and four course notebooks, and this report is
about a guard that does not guard. Restoring the guard is complete on its own terms, and
narrowing the accepted set to the single implemented value is what makes the argument
honest in the meantime.

**That the caller whitelist should be repaired rather than dropped.** There is no caller
to repair it to. Keying on a caller buys nothing when the argument reaches one function,
and `platform` and `engine` — its two neighbours in the same signature — are both
caller-agnostic.

## Scope and exclusions

Covered: the digester, and the parameter block of `potential_energy_minimization`, whose
six descriptions were the generated `Argument <name>.` placeholder and whose `platform`
entry advertised `'Reference'` and `'OpenCL'`, both of which `digest_platform` refuses.

Not covered: that `method` is accepted and never read. It stays declared, now with a
docstring that says what it does and does not do.

## Acceptance criteria

- A returned exception anywhere under `molsysmt/_private/argdigest/` fails the suite.
- `digest_method` returns `'L-BFGS'` for the implemented algorithm and raises
  `ArgumentError` for anything else.
- The default that `potential_energy_minimization` declares survives its own digester.

Both behavioural guards and the structural one were confirmed to fail against the
previous `method.py` before being committed.

## Provenance

Linux, Python 3.13.14, `molsysmt` at working tree `ebfc72ace`, 2026-09-06.
