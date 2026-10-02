"""Exercise general chemical matching without truncated graphs or matches."""

import numpy as np
import pandas as pd
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt._private.smonitor import (
    ArgumentError,
    StructuralInconsistencyError,
    UnsupportedHeavyOperationError,
)


@pytest.mark.parametrize("fractional", [False, True])
def test_read_only_bond_arrays_preserve_source_chemistry(monkeypatch, fractional):
    source = msm.convert(
        Chem.MolFromSmiles("c1ccccc1.[NH4+].CCO"), to_form="molsysmt.MolSys"
    )
    state = source.chemical_states._states[
        source.chemical_states.reference_chemical_state_index
    ]
    if fractional:
        orders = state.bonds.reindex(columns=["bond_order", "fractional_bond_order"])
        state.bonds["fractional_bond_order"] = (
            orders["bond_order"]
            .astype(float)
            .fillna(orders["fractional_bond_order"].astype(float))
        )
        state.bonds["bond_order"] = np.nan
    original_atoms = state.atom_attributes.copy(deep=True)
    original_bonds = state.bonds.copy(deep=True)
    to_numpy = pd.Series.to_numpy

    def read_only(series, *args, **kwargs):
        array = to_numpy(series, *args, **kwargs)
        if not kwargs.get("copy", False):
            array = array.view()
            array.setflags(write=False)
        return array

    monkeypatch.setattr(pd.Series, "to_numpy", read_only)
    result = msm.topology.get_substructure_matches(
        source, ["[a;r6]1:[a;r6]:[a;r6]:[a;r6]:[a;r6]:[a;r6]:1", "[N+]"]
    )
    assert result["matches"][0].tolist() == [[0, 1, 2, 3, 4, 5]]
    assert result["matches"][1].tolist() == [[6]]
    pd.testing.assert_frame_equal(state.atom_attributes, original_atoms)
    pd.testing.assert_frame_equal(state.bonds, original_bonds)


@pytest.mark.parametrize("native", [False, True])
def test_query_order_resonance_and_empty_shapes(native):
    source = Chem.MolFromSmiles("CCO.NC(=[NH2+])N")
    if native:
        source = msm.convert(source, to_form="molsysmt.Topology")
    result = msm.topology.get_substructure_matches(source, ["[O]", "[C]=[N+]", "[F]"])
    assert result["matches"][0].tolist() == [[2]]
    assert result["matches"][1].tolist() == [[4, 5]]
    assert result["matches"][2].shape == (0, 1)
    assert all(matrix.dtype == np.int64 for matrix in result["matches"])
    assert result["source_atom_indices"].tolist() == list(range(7))
    assert result["software"]["molsysmt"] == msm.__version__


def test_match_limit_is_applied_before_selection_without_silent_truncation():
    with pytest.raises(UnsupportedHeavyOperationError):
        msm.topology.get_substructure_matches(
            "smiles:CCCC", "[C]", selection=[0], max_matches=2
        )
    result = msm.topology.get_substructure_matches(
        "smiles:CCCC", "[C][C]", selection=[0, 1], max_matches=3
    )
    assert result["matches"][0].tolist() == [[0, 1]]


@pytest.mark.parametrize("patterns", ["", [], "[INVALID", 1])
def test_invalid_queries_fail(patterns):
    with pytest.raises(ArgumentError):
        msm.topology.get_substructure_matches("smiles:CCO", patterns)


def test_missing_charge_or_aromaticity_is_not_inferred():
    source = msm.convert("smiles:CCO", to_form="molsysmt.Topology")
    source._reference_chemical_state.atom_attributes.loc[0, "formal_charge"] = None
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_substructure_matches(source, "[O]")


def test_missing_covalent_order_is_not_filled_with_a_single_bond():
    source = msm.convert("smiles:CCO", to_form="molsysmt.Topology")
    source._reference_chemical_state.bonds.loc[0, "bond_order"] = None
    source._reference_chemical_state.bonds.loc[0, "fractional_bond_order"] = None
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_substructure_matches(source, "[C]")


def test_unrepresentable_fractional_order_is_not_an_unspecified_bond():
    source = msm.convert("smiles:CCO", to_form="molsysmt.Topology")
    source._reference_chemical_state.bonds.loc[0, "bond_order"] = None
    source._reference_chemical_state.bonds.loc[0, "fractional_bond_order"] = 1.2
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_substructure_matches(source, "[C]")
