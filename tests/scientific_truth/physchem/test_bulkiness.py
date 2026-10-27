"""Bounded reference cases, not geometric validation of the original descriptor."""

import numpy as np

import molsysmt as msm


def test_bulkiness_reference_areas_match_curated_amino_acids():
    # AAindex1 ZIMJ680102 / official ProtScale values; area convention:
    # Proust et al. (2019), doi:10.3389/fmicb.2019.00906, Table 1.
    # The synthetic group labels test reference lookup, not actual amino-acid chemistry.
    builder = msm.MolSysBuilder()
    for name in ["ALA", "GLY", "TRP"]:
        index = builder.add_atom(atom_name="CA", atom_type="C")
        builder.add_group([index], group_name=name)
    molsys = builder.build()
    result = msm.physchem.get_bulkiness(molsys)
    assert result.shape == (3,)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="angstrom**2"),
        [11.5, 3.4, 21.67],
        rtol=0,
        atol=1e-12,
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(result, to_unit="nm**2"),
        [0.115, 0.034, 0.2167],
        rtol=0,
        atol=1e-12,
    )
