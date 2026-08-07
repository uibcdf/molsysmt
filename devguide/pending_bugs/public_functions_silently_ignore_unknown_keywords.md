# Public functions silently ignore unknown keyword arguments

**Reported:** 2026-08-07, found while writing the Phase 2 regression matrix of the
[atom-axis `add()` audit](../archive/resolved_proposals/atom_axis_add_semantic_audit.md). A test
asserting that `add()` honours `attribute_policy` passed — against a function that has
no such parameter.

**Status:** open. Confirmed, with a reproduction that returns a wrong answer.

**Severity:** high. This is the silent-wrong-result class: a mistyped parameter name is
accepted, the call runs with the default, and the caller receives a plausible result
with no diagnostic.

## Reproduction

`structure_indices` misspelled by one letter, on a 5,000-structure trajectory:

```python
import molsysmt as msm

molsys = msm.convert(msm.systems['pentalanine']['traj_pentalanine.h5msm'],
                     to_form='molsysmt.MolSys')

msm.get(msm.extract(molsys, selection='all', structure_indices=[0, 1, 2]), n_structures=True)
# 3

msm.get(msm.extract(molsys, selection='all', structure_indeces=[0, 1, 2]), n_structures=True)
# 5000        <- no error, no warning
```

The second call silently extracted the entire trajectory. A user who then measures a
property over what they believe are three structures gets a number computed over five
thousand.

## Scope

Sampled on 2026-08-07 against the working tree, one bogus keyword per call. Three
different behaviours, none of them correct:

| Behaviour | Functions |
| --- | --- |
| **silently ignored** | `select`, `extract`, `add`, `merge`, `copy`, `info`, `append_structures`, `concatenate_structures` |
| raw `KeyError: 'bogus'` | `get`, `contains` |
| `TypeError` naming an internal function | `convert` (`to_molsysmt_MolSys() got an unexpected keyword argument`) |

Eight of the eleven functions sampled accept anything. The sample was not exhaustive;
the acceptance test below measures the real extent.

`inspect.signature(msm.add)` reports the eight declared parameters and no `**kwargs`,
so the signature a user reads — and a linter or IDE checks against — does not describe
what the function accepts.

## Likely cause

The public decorator stack (`@signal`, `@arg_digest`) wraps the target in a wrapper
that forwards `**kwargs`. Digestion validates the arguments it knows and passes the
rest through; whether an unknown name then fails depends entirely on what the inner
implementation does with it. Functions that pass their arguments explicitly to a form
adapter drop the extras on the floor; `get` and `contains` look names up in a
dictionary and raise `KeyError`; `convert` forwards them into the converter, which
raises `TypeError`.

Nothing in the chain checks the caller's keywords against the declared signature.

## Affected public behavior

- Any misspelled parameter is silently ignored on eight of eleven sampled entry
  points, and the call proceeds with defaults.
- A caller cannot detect the mistake from the return value, because the result is
  well-formed.
- Where it does fail, the diagnostic is a raw `KeyError` or a `TypeError` naming a
  private converter, neither of which is catalogued or actionable — this contradicts
  [`error_policy.md`](../error_policy.md).
- Feature detection is impossible: passing a parameter a future version will support
  succeeds today and does nothing, which is how this defect was found.

## Acceptance tests

1. **A parametrised test over the public API surface.** For every function in
   `api_surface.md`, calling it with one keyword that is not in its signature must
   raise a catalogued MolSysMT error naming the offending keyword. The registry
   already enumerates 188 classified symbols, so the test needs no hand-written list.
2. **The typo reproduction above**, asserting that the misspelling raises rather than
   returning 5,000 structures.
3. **`inspect.signature` agrees with what is accepted**: no public function accepts a
   keyword absent from its own signature.

## Notes

The fix belongs in the decorator stack, not in each function: rejecting unknown
keywords once in `@arg_digest` covers every decorated entry point and keeps the three
current behaviours from having to be reconciled one by one. That crosses into
`argdigest`, so it needs the same upstream-or-local decision as
[`smonitor_warn_drops_structured_extra.md`](smonitor_warn_drops_structured_extra.md).

Found by the `add()` audit but independent of it: none of the audit's decisions
depend on this, and fixing it does not depend on them.
