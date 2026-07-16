# Resolved Bug: `merge` collapsed per-system indices

**Status:** resolved and contract-tested 2026-07-13
**Originally diagnosed:** 2026-07-12
**Severity:** medium — the documented calling convention raises a raw third-party error
**Location:** `molsysmt/basic/merge.py:114-132`, together with
`molsysmt/_private/arg_digestion/argument/structure_indices.py:35`

## Symptom

`merge` documents `structure_indices` as *"0-based indices of the structures to include
from each system. A single value applies to all systems; otherwise provide a list matching
`molecular_systems`."* Providing exactly that list crashes:

```python
import molsysmt as msm
a = msm.systems['T4 lysozyme L99A']['181l.pdb']    # 1 structure
b = msm.systems['Trp-Cage']['1l2y.h5msm']          # 38 structures

msm.merge([a, b], structure_indices=[0, 0], to_form='molsysmt.MolSys')
# TypeError: Indexing elements must be in increasing order      <- raw h5py error

msm.merge([a, b], structure_indices=[[0], [0]], to_form='molsysmt.MolSys')   # works
msm.merge([a, b], structure_indices=0, to_form='molsysmt.MolSys')            # works
```

`selections` has the same defect when given per-system index collections:

```python
msm.merge([a, b], selections=[[0, 1, 2], [0, 1, 2]], structure_indices=0)
# TypeError: Only 1D arrays allowed for fancy indexing          <- raw numpy error
```

Both errors come from third-party libraries, not from MolSysMT.

## Root cause

The two arguments are overloaded: the same list can mean *"one value per system"* or *"one
collection of indices, applied to every system"*. `merge` disambiguates by type:

```python
# molsysmt/basic/merge.py:124
if not isinstance(structure_indices, (list, tuple)):
    structure_indices = [structure_indices for ii in range(n_molecular_systems)]
elif len(structure_indices) != n_molecular_systems:
    raise ArgumentLengthError(...)
```

But by the time the body runs, `@arg_digest` has already normalised the argument, and
`digest_structure_indices` turns any flat sequence of integers into an **ndarray**:

| passed | after digestion | `isinstance(..., (list, tuple))` |
|---|---|---|
| `0` | `array([0])` | False → broadcast to every system ✓ |
| `[0, 0]` | `array([0, 0])` | **False → broadcast to every system** ✗ |
| `[[0], [0]]` | `[array([0]), array([0])]` | True → one per system ✓ |

So `[0, 0]` — the documented per-system form — is read as *"structures 0 and 0, for every
system"*. Each system is then asked for a duplicated index, and h5py rejects it.

The type test cannot work: after digestion, a per-system list of integers and a single
multi-index array are indistinguishable. `merge` is trying to recover an intent that the
digester has already erased.

## Proposed fix

The ambiguity is in the API, so the fix has to be there too. Options, in order of preference:

1. **Keep the type test but make it survive digestion.** Have `digest_structure_indices`
   preserve the outer list when it has one element per system — that is, digest `merge`'s
   `structure_indices` with a dedicated per-system digester (the repository already has
   `structure_indices_A` / `structure_indices_B` / `structure_indices_2` variants for
   argument-specific behaviour) rather than the general one that flattens.
2. **Reject the ambiguous form.** If `structure_indices` is a flat sequence of integers whose
   length happens to equal `n_molecular_systems`, raise `ArgumentError` naming both readings
   and asking for `[[0], [0]]` or a scalar. Safe, but pushes the ambiguity onto the user.

Whichever is chosen, the failure must surface as a MolSysMT exception. A raw h5py or numpy
`TypeError` leaking from a documented calling convention is the part that must not survive.

## Also to check

At diagnosis, the docstring of `merge` promised
the `[0, 0]` form that does not work, and does not mention the `[[0], [0]]` form that does.

## Resolution

The `selections` and `structure_indices` digesters are now caller-aware for
`merge()` and `concatenate_structures()`. They use `molecular_systems` to
normalize the arguments into exactly one entry per input system before the
public function body runs.

The public contract is now unambiguous:

- a list or tuple contains one scalar or collection per system;
- a scalar, string, NumPy array, range, or `'all'` is broadcast to all systems;
- a per-system length mismatch raises `ArgumentLengthError` during digestion.

Regression tests cover flat per-system structure indices, nested per-system atom
collections, scalar broadcasts, NumPy collection broadcasts, mismatch errors,
and the equivalent `concatenate_structures()` behavior. The API docstrings, User
Guide merge tutorial, and Common Core course module record the same rules.
