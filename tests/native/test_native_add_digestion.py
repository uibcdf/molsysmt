"""Validating native addition without bypassing its public argument boundary."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError


@pytest.mark.parametrize("form", ["topology", "molsys"])
@pytest.mark.parametrize("keep_ids", ["default", True, False])
@pytest.mark.parametrize("atom_indices", ["all", [1, 0]])
def test_native_add_accepts_boolean_keep_ids(
    alanine_molsys, form, keep_ids, atom_indices
):
    msm.set(alanine_molsys, element="chain", chain_id=["A"])
    target = alanine_molsys if form == "molsys" else alanine_molsys.topology
    source = target.copy()
    original = source.topology if form == "molsys" else source
    source_chains = original.chains.copy(deep=True)
    n_atoms = original.n_atoms
    options = {"atom_indices": atom_indices}
    if keep_ids != "default":
        options["keep_ids"] = keep_ids

    target.add(source, **options)

    topology = target.topology if form == "molsys" else target
    added_count = n_atoms if atom_indices == "all" else 2
    assert topology.n_atoms == n_atoms + added_count
    expected_ids = ["0", "1"] if keep_ids is False else ["A", "A"]
    assert topology.chains["chain_id"].tolist() == expected_ids
    assert topology.atoms["chain_index"].iloc[n_atoms:].tolist() == [1] * added_count
    assert original.n_atoms == n_atoms
    pd.testing.assert_frame_equal(original.chains, source_chains)
    if form == "molsys":
        assert target.structures.coordinates.shape[1] == n_atoms + added_count


@pytest.mark.parametrize("form", ["topology", "molsys"])
@pytest.mark.parametrize("keep_ids", [0, 1, "True", None])
def test_native_add_rejects_invalid_keep_ids_before_mutation(
    alanine_molsys, form, keep_ids
):
    target = alanine_molsys if form == "molsys" else alanine_molsys.topology
    source = target.copy()
    topology = target.topology if form == "molsys" else target
    original_atoms = topology.atoms.copy(deep=True)
    original_chains = topology.chains.copy(deep=True)

    with pytest.raises(ArgumentError, match="keep_ids"):
        target.add(source, keep_ids=keep_ids)

    pd.testing.assert_frame_equal(topology.atoms, original_atoms)
    pd.testing.assert_frame_equal(topology.chains, original_chains)
