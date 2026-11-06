"""Join native table columns with their declared nullable dtypes."""

import pandas as pd


def equivalent(left, right):
    """Compare ordered declarations across equivalent nullable string storage.

    Numeric/boolean fields retain their typed equality. Only actual string or
    missing values can cross an object/nullable-string storage boundary; this
    never turns a number into a label or a missing value into literal text.
    Inputs are read without modifying or canonicalizing their stored columns.
    """
    if left.equals(right):
        return True
    if not left.index.equals(right.index):
        return False
    if isinstance(left, pd.DataFrame) and isinstance(right, pd.DataFrame):
        if not left.columns.equals(right.columns):
            return False
        columns = ((left[name], right[name]) for name in left.columns)
    elif isinstance(left, pd.Series) and isinstance(right, pd.Series):
        columns = ((left, right),)
    else:
        return False
    for first, second in columns:
        if first.equals(second):
            continue
        if any(
            pd.api.types.infer_dtype(values, skipna=True)
            not in {"string", "unicode", "empty"}
            for values in (first, second)
        ):
            return False
        if not first.astype("string").equals(second.astype("string")):
            return False
    return True


def concatenate(left, right):
    """Join each column with nullable promotion, avoiding all-NA table inference."""
    result = pd.DataFrame(index=range(len(left) + len(right)))
    for name in dict.fromkeys([*left.columns, *right.columns]):
        dtype = left[name].dtype if name in left else right[name].dtype
        first = (
            left[name]
            if name in left
            else pd.Series(pd.NA, index=left.index, dtype=dtype)
        )
        second = (
            right[name]
            if name in right
            else pd.Series(pd.NA, index=right.index, dtype=dtype)
        )
        if not len(second):
            result[name] = first.reset_index(drop=True).copy(deep=True)
        elif not len(first):
            result[name] = second.reset_index(drop=True).copy(deep=True)
        else:
            result[name] = pd.concat([first, second], ignore_index=True)
    return result
