# Bug Report: `msm.compare()` emits `UserWarning` on array shape mismatches

**Status:** Pending fix in `molsysmt/basic/compare.py`.
**Severity:** Low-Medium (produces intrusive Python warnings in user notebooks when auditing non-identical systems).

## What We Hit

When executing a comparison between a full system and an extracted sub-system (such as full T4 Lysozyme vs a protein-only sub-system), auditing array attributes like `coordinates` or `velocities` with `output_type='dictionary'` emits an unexpected `UserWarning`:

```python
import molsysmt as msm
from molsysmt import systems

lysozyme = msm.convert(systems['T4 lysozyme L99A']['181l.bcif.gz'], to_form='molsysmt.MolSys')
protein_only = msm.extract(lysozyme, selection='molecule_type == "protein"')

report = msm.compare(lysozyme, protein_only, coordinates=True, box=True, n_groups=True, output_type='dictionary')
```

**Emitted Warning:**
```text
UserWarning: Shape mismatch for 'coordinates': (1, 1441, 3) vs (1, 1289, 3). Returning False.
```

## Why This Happens

In `molsysmt/basic/compare.py` (around line 567), array attribute shape checks explicitly invoke `warn()` when array dimensions differ:

```python
if dict_A[attribute].shape != dict_B[attribute].shape:
    warn(f"Shape mismatch for '{attribute}': {dict_A[attribute].shape} vs {dict_B[attribute].shape}. Returning False.")
    return False
```

Comparing systems with different numbers of atoms or frames is a standard use case for `msm.compare()`. Returning `False` in the comparison result (or in the `output_type='dictionary'` report) is the expected functional output of a comparison test, not an exceptional or erroneous state that warrants a `UserWarning`.

## Proposed Solution for Developers

1. **Quiet Boolean Reporting:** Remove the `warn(...)` call during shape mismatch evaluation in `molsysmt/basic/compare.py`. When array shapes differ, `compare` should directly assign or return `False` for that attribute.
2. **Optional Diagnostic Logging:** If diagnostic details about shape mismatches are needed for debugging, route them through `smonitor` at `DEBUG` level or behind an explicit `verbose=True` argument rather than emitting standard `UserWarning` alerts.
