# Public functions silently ignore unknown keyword arguments

**Reported:** 2026-08-07, found while writing the Phase 2 regression matrix of the
[atom-axis `add()` audit](../archive/resolved_proposals/atom_axis_add_semantic_audit.md). A test
asserting that `add()` honours `attribute_policy` passed — against a function that has
no such parameter.

**Status:** resolved on 2026-08-07 and archived. Fixed upstream in ArgDigest 0.10.0 by
adding the axis this report turned out to be a symptom of — the function argument
contract — and declared in MolSysMT by pointing at its own attribute catalogue. The
reproduction below now raises `UnknownArgumentError` naming the keyword and suggesting
`structure_indices`. Guarded by `tests/test_argument_contract.py`.

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

## Confirmed cause

`argdigest/core/utils.py:18-21`, in `bind_arguments`:

```python
if not var_keyword_name:
    # Filter kwargs to only include valid parameters
    valid_params = set(sig.parameters.keys())
    kwargs = {k: v for k, v in kwargs.items() if k in valid_params}
```

When the decorated function does **not** declare `**kwargs`, argdigest actively
discards every keyword outside its signature. This is one deliberate line, not an
accident of forwarding, and it is the whole explanation for the silent cases.

It also explains why some functions do fail: they declare `**kwargs`, so
`var_keyword_name` is set, the filter is skipped, and the unknown name reaches the body.
What happens then is whatever that body happens to do — which is not a designed
behaviour either.

## Scope

Measured on 2026-08-07 against the working tree, one bogus keyword per call, over the
26 public callables of the `molsysmt` namespace.

**19 have a closed signature** — `add`, `append_structures`,
`are_multiple_molecular_systems`, `concatenate_structures`, `copy`, `extract`,
`get_attributes`, `get_form`, `has_attribute`, `info`, `is_a_molecular_system`, `merge`,
`remove`, `select`, `view`, `where_is_attribute` and others. Every one of them silently
discards an unknown keyword, through the filter above.

**7 declare `**kwargs`** because they must, and among those the behaviour is
inconsistent:

| Function | Unknown keyword |
| --- | --- |
| `compare`, `get_label`, `is_composed_of` | silently accepted |
| `get`, `set`, `contains` | raw `KeyError: 'bogus_attr'` |
| `convert` | `TypeError` naming a private converter |

So a typo is silent in 22 of 26 entry points, and produces an uncatalogued error in the
remaining four. No public function reports it properly.

`inspect.signature(msm.add)` reports eight declared parameters and no `**kwargs`, so the
signature a user reads — and a linter or IDE checks against — does not describe what the
function accepts.

## Why `**kwargs` is not the problem

The seven open signatures are open on purpose. `get`, `set`, `contains`, `compare` and
`is_composed_of` take attribute names as boolean keywords — `msm.get(molsys,
n_atoms=True)` — and there are **118 attributes**. Declaring them as parameters is not
an option and never will be.

The mistake is treating "not in the signature" as the definition of a valid keyword.
Every one of these functions has a well-defined domain of acceptable keywords; the
domain simply comes from different places:

| Kind | Domain of valid keywords | Functions |
| --- | --- | --- |
| closed | its own signature | the 19 above |
| attribute-taking | its signature **plus the attribute catalogue** | `get`, `set`, `contains`, `compare`, `is_composed_of`, `get_label` |
| delegating | its signature plus the parameters of the resolved target | `convert` |

The fix is to give each function a domain and enforce it, not to forbid `**kwargs`.

For the attribute-taking group the machinery already exists and is unused for this:
`molsysmt.attribute.attributes` enumerates the 118 names, `is_attribute()` is the
predicate, and `digest_attribute` already raises a proper catalogued `ArgumentError` for
a bad attribute name. Today that digester validates a singular `attribute=` argument;
nothing validates the attribute names arriving through `**kwargs`.

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

1. **A parametrised test over the public API surface.** Every public callable, called
   with one keyword outside its declared domain, must raise a catalogued MolSysMT error
   naming the offending keyword. The domain is the signature for closed functions and
   the signature plus the attribute catalogue for the attribute-taking ones, so the test
   needs no hand-written list of valid names.
2. **The typo reproduction above**, asserting that the misspelling raises rather than
   returning 5,000 structures.
3. **A legitimate open keyword still works**: `msm.get(molsys, n_atoms=True)` and the
   other 117 attributes must keep passing through untouched. A fix that closes the hole
   by narrowing `**kwargs` to the signature would break the library.
4. **No public function raises a bare `KeyError` or a `TypeError` naming a private
   module** for a keyword mistake.

## Open questions before implementing

- **What does the argdigest filter optimise?** It is one deliberate line with a comment,
  so it was written for a reason — plausibly to let an internal caller pass one shared
  dictionary to several functions without each rejecting the keys meant for the others.
  That use has to be found before the line is changed; if it exists, the filter must
  become opt-in rather than disappear.
- **Upstream or local?** Enforcing the closed-signature domain belongs in `argdigest`
  and would fix 19 functions at once, but it is another repository — the same
  upstream-or-local decision as
  [`smonitor_warn_drops_structured_extra.md`](smonitor_warn_drops_structured_extra.md).
  The attribute-catalogue domain is MolSysMT's own and can be enforced here regardless.
- **Where does the attribute check live?** Validating `**kwargs` against the catalogue
  inside each of the six functions duplicates the rule six times. A shared digestion
  rule — "these keywords are attribute names" — declared once per function would keep a
  single source of truth, in the spirit of the existing `digest_attribute`.
- **Is a near-miss suggestion worth it?** `structure_indeces` is one edit away from
  `structure_indices`, and the error can say so. It costs little and turns the most
  common instance of this defect into a self-explaining message.

## Notes

Found by the `add()` audit but independent of it: none of the audit's decisions depend
on this, and fixing it does not depend on them.


---

## Resolution

The fix was not "reject unknown keywords". Two findings from the design work changed
its shape, and both are worth keeping.

**`**kwargs` is not the problem.** Six public functions take the 118 attribute names as
boolean keywords and can never declare them as parameters. Treating "not in the
signature" as the definition of a valid keyword would have broken `msm.get`. Each
function has a domain of acceptable keywords; the domain simply comes from different
places — the signature for a closed function, the attribute catalogue for the open ones,
and, for `convert`, the parameters of a converter resolved at call time.

**The mechanism already half-existed and was unreachable.** MolSysMT declares
`STRICTNESS = "warn"` and 395 argument digesters, one per valid argument name, so its
universe of names was already declared. For the seven functions with `**kwargs` the
policy fired correctly. For the other nineteen it could not: `bind_arguments` discarded
the keyword before the policy layer ran. The defect was a binding step making a policy
decision, not a missing feature.

Two claims in the original triage were wrong and are corrected here. `msm.contains(molsys)`
returning `True` with no criterion is **not** a defect: the function implements an
explicit branch for that case, checking `n_atoms` and returning `False` for an empty
selection. `is_composed_of` does the same. No `requires_any_of` rule was declared for
either. Reading the bodies before declaring the contract is what caught it.

One real defect was found the same way: **`get_label` declares `**kwargs` and never
reads it**, so anything passed through it was discarded twice over. Its contract holds
it to its own signature.

`molsysmt.basic.convert` keeps the permissive default. Its domain depends on the
converter resolved from `to_form`, which a keyword-only membership test cannot express;
the gap is recorded in ArgDigest's 0.10.0 release notes and pinned by
`test_every_open_signature_declares_its_domain`.

Evidence: ~8300 MolSysMT tests with the policy set to `error`, the fast release gate at
12/12, and 1296 MolSysViewer tests with nothing declared on its side. No call in either
consumer had to change, which is the expected shape of a defect that only ever reached
users.
