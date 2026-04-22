# Proposal: Normalize data types in `msm.info()` for clean reporting

## Status
Pending

## Purpose
Ensure that the visual output of `info()` is clean and free of Python/NumPy technical boilerplate like `np.int64()`.

## Motivation
In the current implementation, some hierarchical attributes (like lists of indices) contain NumPy types. When Pandas renders these in a Styler or DataFrame, it often prints the full type representation (e.g., `[np.int64(1), np.int64(2)]`). This is visually distracting and provides no value to the user, who only cares about the numerical value.

## Recommendation
Update `molsysmt/basic/info.py` to recursively convert all NumPy scalars and arrays into standard Python types (`int`, `float`, `list`, `str`) before populating the final DataFrame. This will ensure that the "Human-readable" goal of `info()` is fully met.
