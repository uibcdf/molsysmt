import pytest
import numpy as np
import numba as nb

from molsysmt.lib.make_numba_signature import make_numba_signature
from molsysmt.lib.series import (
    serie_to_chunks,
    chunks_to_serie,
    serialized_lists,
    occurrence_order,
    occurrence_order_sorted_serie,
)


def test_make_numba_signature_handles_optional_and_tuple_output():
    sig = make_numba_signature(arguments=[nb.float64[:], [nb.int64[:], None]], output=(nb.int64, nb.float64))
    assert not isinstance(sig, list)

    single = make_numba_signature(arguments=[nb.float64[:]], output=None)
    assert not isinstance(single, list)


def test_make_numba_signature_rejects_invalid_optional_defaults():
    from molsysmt._private.smonitor import InternalAlgorithmError

    with pytest.raises(InternalAlgorithmError):
        make_numba_signature(arguments=[[None]], output=None)

    with pytest.raises(InternalAlgorithmError):
        make_numba_signature(arguments=[[None, 0]], output=None)


def test_series_helpers_and_serialized_lists():
    serie = np.array([1, 2, 3, 7, 8, 10], dtype=np.int64)
    starts, sizes = serie_to_chunks(serie)
    assert np.array_equal(starts, np.array([1, 7, 10], dtype=np.int64))
    assert np.array_equal(sizes, np.array([3, 2, 1], dtype=np.int64))
    rebuilt = chunks_to_serie(starts, sizes)
    assert np.array_equal(rebuilt, serie)

    sl_list = serialized_lists([[3, 4], [10], [2, 9, 1]])
    assert sl_list.n_indices == 3
    assert sl_list.n_values == 6
    assert np.array_equal(sl_list.indices, np.array([0, 1, 2], dtype=np.int64))

    sl_dict = serialized_lists({8: [3, 4, 6], 2: [1], 6: [2, 9]})
    assert np.array_equal(sl_dict.indices, np.array([2, 6, 8], dtype=np.int64))
    assert sl_dict.starts.shape[0] == 4

    occ = occurrence_order(np.array([5, 2, 5, 9, 2], dtype=np.int64))
    assert np.array_equal(occ, np.array([0, 1, 0, 2, 1], dtype=np.int64))

    occ_sorted = occurrence_order_sorted_serie(np.array([1, 1, 2, 2, 2, 4], dtype=np.int64))
    assert np.array_equal(occ_sorted, np.array([0, 0, 1, 1, 1, 2], dtype=np.int64))
