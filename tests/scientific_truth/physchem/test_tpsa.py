"""Bounded original-fragment TPSA evidence, separate from provider parity."""

import numpy as np

import molsysmt as msm


def test_tpsa_matches_primary_ertl_fragment_sums():
    from rdkit import Chem

    # Ertl, Rohde, Selzer (2000), Table 1 (angstrom²): OH 20.23,
    # ether O 9.23, carbonyl O 17.07; doi:10.1021/jm000942e.
    source = Chem.MolFromSmiles("CCO.COC.CC(=O)O")
    result = msm.physchem.get_tpsa(source)
    assert result.shape == (3,)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"),
        [20.23, 9.23, 20.23 + 17.07],
        atol=1e-12,
        rtol=0,
    )


def test_primary_oxygen_fragment_is_retained_in_atomic_context():
    from rdkit import Chem

    molsys = Chem.MolFromSmiles("CCO")
    atomic = msm.physchem.get_tpsa(molsys, element="atom", selection=[2, 0, 2])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(atomic, to_unit="angstrom**2"),
        [20.23, 0, 20.23],
        atol=1e-12,
        rtol=0,
    )
