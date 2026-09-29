"""Keep chemical donor-hydrogen membership when atom indices interleave."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


def _interleaved_pairs_system():
    builder = msm.MolSysBuilder()
    for name, kind in (("N1", "N"), ("H2", "H"), ("N2", "N"), ("H1", "H"), ("O", "O")):
        builder.add_atom(atom_name=name, atom_type=kind)
    builder.add_group([0, 1, 2, 3, 4], group_name="ALA")
    builder.add_bond(0, 3)
    builder.add_bond(2, 1)
    builder.set_coordinates(puw.quantity([
        [0, 0, 0], [0.7, 0, 0], [0.8, 0, 0], [0.1, 0, 0], [0.3, 0, 0],
    ], "nanometers"))
    return builder.build()


def test_donor_hydrogen_pairs_keep_declared_covalent_membership():
    pairs = msm.interactions.hbonds.get_donor_atoms(_interleaved_pairs_system())
    assert pairs.dtype.kind == "i"
    np.testing.assert_array_equal(pairs, [[0, 3], [2, 1]])


@pytest.mark.parametrize("method_name", ["get_buch_hbonds", "get_luzard_chandler_hbonds"])
def test_hbond_triples_keep_the_hydrogen_of_their_donor(method_name):
    method = getattr(msm.interactions.hbonds, method_name)
    triples, *_ = method(_interleaved_pairs_system(), pbc=False)
    np.testing.assert_array_equal(triples[0], [[0, 3, 4]])


def test_buch_analysis_queries_the_actual_covalent_hydrogen():
    result = msm.interactions.hbonds.get_buch_hbonds(
        _interleaved_pairs_system(), pbc=False, output_type="molsysmt.Interactions",
    )
    assert result.query(atom_indices=[3]).n_interactions == 1
    assert result.query(atom_indices=[1]).n_interactions == 0
    assert result.relation(0)["participants"][1]["atom_indices"].tolist() == [3]
