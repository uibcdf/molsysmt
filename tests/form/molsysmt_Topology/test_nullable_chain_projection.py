"""Atom-level chain labels preserve missing memberships and nullable indices."""

import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import MolSys, Topology


@pytest.mark.parametrize("selection", ["all", [3, 1, 0]])
@pytest.mark.parametrize("native", [False, True])
def test_atom_chain_queries_use_declared_nullable_membership(selection, native):
    topology = Topology(n_atoms=4, n_chains=2)
    topology.atoms["chain_index"] = pd.array([1, None, 0, 1], dtype="Int64")
    msm.set(topology, element="chain", chain_id=[7, "B"])
    msm.set(topology, element="chain", chain_name=["left", "right"])
    msm.set(topology, element="chain", chain_type=["protein", "peptide"])
    source = MolSys._from_partial_domains(topology=topology) if native else topology
    expected = [
        [1, None, 0, 1],
        ["B", None, "7", "B"],
        ["right", None, "left", "right"],
        ["peptide", None, "protein", "peptide"],
    ]
    if isinstance(selection, list):
        expected = [[column[i] for i in selection] for column in expected]
    assert (
        msm.get(
            source,
            element="atom",
            selection=selection,
            chain_index=True,
            chain_id=True,
            chain_name=True,
            chain_type=True,
        )
        == expected
    )
    assert topology.atoms["chain_index"].tolist() == [1, pd.NA, 0, 1]
