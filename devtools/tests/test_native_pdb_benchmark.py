"""Checking analytic scaling inputs against public native graph construction."""

import numpy as np
import pytest

import molsysmt as msm
from devtools.scripts.benchmark_native_pdb_connectivity import (
    _alanine_source,
    _distribution,
)


@pytest.mark.parametrize(
    "groups_per_chain,expected",
    [
        (2, [[0, 1], [1, 2], [1, 4], [2, 3], [2, 5], [5, 6], [6, 7], [6, 9], [7, 8]]),
        (1, [[0, 1], [1, 2], [1, 4], [2, 3], [5, 6], [6, 7], [6, 9], [7, 8]]),
    ],
)
def test_synthetic_expected_graph_includes_polymer_links_but_not_ter_crossings(
    groups_per_chain, expected
):
    text, generated_expected = _alanine_source(2, groups_per_chain)
    assert generated_expected == [tuple(pair) for pair in expected]
    assert text.startswith("HEADER    SYNTHETIC")
    assert "CONECT" not in text
    explicit = msm.convert(text, get_missing_bonds=False)
    assert explicit.chemical_states.get_bonds().empty
    output = msm.convert(text, get_missing_bonds=True, bond_inference_engine="MolSysMT")
    assert output.get_n_atoms() == 10
    assert (
        output.chemical_states.get_bonds()[["atom1_index", "atom2_index"]]
        .to_numpy()
        .tolist()
        == expected
    )
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="angstrom"),
        msm.pyunitwizard.get_value(explicit.structures.coordinates, to_unit="angstrom"),
    )


def test_summary_retains_observations_and_uses_inclusive_quartiles():
    values = [9, 1, 5]
    result = _distribution(values)
    assert result == dict(
        n=3, values=[9, 1, 5], minimum=1, median=5, maximum=9, interquartile_range=4
    )


@pytest.mark.parametrize(
    "groups,chain", [(0, 32), (20000, 32), (1, 0), (1, 101), (19999, 1)]
)
def test_synthetic_inputs_refuse_unbounded_or_unrepresentable_sizes(groups, chain):
    with pytest.raises(ValueError):
        _alanine_source(groups, chain)
