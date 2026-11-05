"""Keep missing ID metadata distinct from source strings spelling sentinels."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys


@pytest.mark.parametrize("native", [False, True])
@pytest.mark.parametrize(
    "element,field", [("atom", "atom_id"), ("group", "group_id"), ("chain", "chain_id")]
)
def test_nullable_ids_remain_missing_in_public_and_native_queries(
    native, element, field
):
    source = MolSys(n_atoms=7, n_groups=7, n_chains=7)
    table = getattr(source.topology, element + "s")
    table[field] = pd.array(
        [None, pd.NA, "<NA>", "None", "nan", "", "37"], dtype="string"
    )
    query = source.get if native else lambda **kwargs: msm.get(source, **kwargs)
    values = query(element=element, **{field: True})
    assert values == [None, None, "<NA>", "None", "nan", "", "37"]
    selected = query(element=element, selection=[3, 0, 6, 0], **{field: True})
    assert selected == ["None", None, "37", None]
    assert table[field].isna().tolist() == [
        True,
        True,
        False,
        False,
        False,
        False,
        False,
    ]


@pytest.mark.parametrize("missing", [None, pd.NA, np.nan])
def test_shared_normalizer_handles_scalar_and_nested_missing_ids(missing):
    from molsysmt.basic.get import _coerce_ids_to_string

    assert _coerce_ids_to_string(missing) is None
    assert _coerce_ids_to_string([[missing, "<NA>"], [7, missing]]) == [
        [None, "<NA>"],
        ["7", None],
    ]
    assert _coerce_ids_to_string(np.array([5.0, np.nan])) == ["5.0", None]
