"""Join native table columns with their declared nullable dtypes."""

import pandas as pd


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
