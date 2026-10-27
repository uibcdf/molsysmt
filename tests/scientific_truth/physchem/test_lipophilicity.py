"""Bounded primary atomic-sum controls, independent of provider parity."""

import numpy as np

import molsysmt as msm


def test_wildman_crippen_primary_atomic_sums():
    from rdkit import Chem

    # Wildman and Crippen (1999), Table 1, doi:10.1021/ci990307l:
    # C1=0.1441, C18=0.1581, H1=0.1230. Methane, ethane, benzene.
    # These sums validate only these atom types, not prediction accuracy.
    molsys = Chem.MolFromSmiles("C.CC.c1ccccc1")
    result = msm.physchem.get_lipophilicity(molsys)
    assert result.shape == (3,)
    np.testing.assert_allclose(
        result,
        [0.1441 + 4 * 0.1230, 2 * 0.1441 + 6 * 0.1230, 6 * (0.1581 + 0.1230)],
        atol=1e-12,
        rtol=0,
    )


def test_primary_methane_atomic_values_and_nonindexed_hydrogen_attribution():
    from rdkit import Chem

    indexed = Chem.AddHs(Chem.MolFromSmiles("C"))
    atomic = msm.physchem.get_lipophilicity(indexed, element="atom")
    np.testing.assert_allclose(
        atomic, [0.1441, 0.1230, 0.1230, 0.1230, 0.1230], atol=1e-12, rtol=0
    )
    folded = msm.physchem.get_lipophilicity(Chem.MolFromSmiles("C"), element="atom")
    np.testing.assert_allclose(folded, [0.1441 + 4 * 0.1230], atol=1e-12, rtol=0)
