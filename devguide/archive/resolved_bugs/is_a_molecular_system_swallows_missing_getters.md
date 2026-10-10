# Resolved Bug: `is_a_molecular_system` accepted failed verification

**Status:** resolved and contract-tested 2026-07-13
**Originally diagnosed:** 2026-07-12
**Severity:** high — silently accepts an invalid molecular system
**Location:** `molsysmt/basic/is_a_molecular_system.py:79-100`

## Symptom

A topology file and a coordinates file belonging to **different** molecular
systems were accepted as one valid molecular system. No error, no warning.

```python
import molsysmt as msm
# pentalanine.prmtop declares 5207 atoms; the inpcrd below declares 3
msm.basic.is_a_molecular_system([prmtop_of_system_A, inpcrd_of_system_B])
# True    (before file:inpcrd got its getters)
```

## Root cause

Two independent defects compound each other.

**The predicate bypasses the pipes.** It reaches into the form module directly:

```python
n_atoms = _dict_modules[form_in].get_n_atoms_from_system(item)
```

This is not `msm.get()`. Whatever a form routes through
`piped_topological_attribute` is invisible here, so the form must own the direct
getter or the probe cannot work at all.

**Every failure is swallowed.** The call sits inside a blanket
`except Exception: ... pass`. When `file:inpcrd` had no getters, the resulting
`AttributeError` was discarded, the inpcrd contributed nothing to `set_n_atoms`,
the set collapsed to `{n_atoms(prmtop)}`, its length was 1, and the predicate
returned `True`.

So an incomplete adapter did not degrade into "cannot verify". It degraded into
"verified fine". The failure mode defaults to yes.

## The deeper problem: one boolean answers two questions

`is_a_molecular_system` conflates two questions that need separate answers:

- **Classification** — are these items one system split across complementary
  parts (topology + coordinates), or several distinct systems?
- **Validation** — given that they are meant to be one system, are they
  consistent?

Because a single boolean carries both, `False` means both "these are two different
systems" (`['1CRN', '2LAO']`) and "this is one broken system"
(prmtop of A + inpcrd of B) — two completely different user errors that deserve
completely different messages. And `True` additionally absorbs "could not check".

Downstream, `digest_molecular_system` can only raise a generic `ArgumentError`
telling the user to "check the API for the expected argument format", because the
predicate did not tell it what was actually wrong.

## Proposed fix

**Split the two questions.**

*Classification* can be answered from the form registry alone — statically, with
no file reads and no network. Each form declares what it provides, so:

> at most one item may carry a topology; if two or more do, they are distinct
> systems, not complementary parts of one.

Check it against the real cases: `[prmtop, inpcrd]` → one topology → one system.
`[pdb, xtc]` → one topology → one system. `[Topology, Structures]` → one system.
`['1CRN', '2LAO']` → two topologies → two systems. `['1CRN', '1CRN']` → two
topologies → two systems (today this pair is silently collapsed into a single
327-atom system).

Note this also removes the network cost: today the predicate downloads from RCSB
just to count atoms on a `string:pdb_id`, and `convert` then resolves the same
form again. Under the rule above, the two-pdb-id case is decided without touching
the network at all.

*Validation* by atom count then runs **only** on the branch already classified as
one system — which is exactly the branch where the count is cheap to obtain, from
local file headers. It must **fail loudly when it cannot verify** rather than
`pass`: an incomplete adapter has to surface as an error, never as a valid system.

## Related

- The missing getter that triggered this is fixed; see
  `molsysmt/form/file_inpcrd/get_topological_attributes.py`.
- Other forms are still in the same state:
  [`form_attributes_declared_without_getters.md`](form_attributes_declared_without_getters.md).
- Because the predicate bypasses pipes, adding a pipe to a form is **not** enough
  to make it usable here. Any form that may appear in a multi-item molecular
  system needs `get_n_atoms_from_system` of its own.

## Resolution

Classification and validation now produce a private structured assessment.
Classification uses form capabilities and identifies two or more
topology-providing items as separate systems before reading molecular data.
Candidate complementary items are validated through the public `get()` delivery
path, including registered pipes and derivations.

Validation has explicit `valid`, `invalid`, and `unverified` states. The public
boolean predicate returns `True` only for a proven valid single system. Argument
digestion preserves the distinction: mismatched atom counts raise
`StructuralInconsistencyError`, while a failed consistency probe raises the
catalog-backed `MolecularSystemVerificationError` (`MSM-ERR-SYS-004`).

Regression tests cover static classification without atom-count reads,
inconsistent complementary forms, failed probes, unsupported strings, public
digestion, and the original PRMTOP/INPCRD cases.
