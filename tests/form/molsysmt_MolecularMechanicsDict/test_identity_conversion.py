"""Identity adapters validate their registered form and preserve copy policy."""

import numpy as np
import pytest

from molsysmt._private.smonitor import ArgumentError
from molsysmt.form.molsysmt_MolecularMechanicsDict.to_molsysmt_MolecularMechanicsDict import (
    to_molsysmt_MolecularMechanicsDict,
)
from molsysmt.native import Topology


@pytest.mark.parametrize("copy_if_all", [True, False])
def test_identity_conversion_preserves_values_and_copy_policy(copy_if_all):
    source = {"forcefield": ["amber14-all.xml"], "partial_charge": [0.1, -0.1]}
    result = to_molsysmt_MolecularMechanicsDict(source, copy_if_all=copy_if_all)
    assert (result is source) is (not copy_if_all)
    assert result["forcefield"] == ["amber14-all.xml"]
    np.testing.assert_array_equal(result["partial_charge"], [0.1, -0.1])
    if copy_if_all:
        result["forcefield"].append("amber14/tip3p.xml")
        assert source["forcefield"] == ["amber14-all.xml"]


def test_identity_conversion_rejects_foreign_native_form():
    with pytest.raises(ArgumentError):
        to_molsysmt_MolecularMechanicsDict(Topology())
