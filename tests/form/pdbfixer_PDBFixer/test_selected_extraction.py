"""Keep selected PDBFixer inventory and coordinates aligned."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("route", ["extract", "convert"])
@pytest.mark.parametrize("length", ["nm", "pm"])
def test_selected_pdbfixer_extraction_aligns_inventory_and_geometry(
    builder_pdb_molsys, route, length
):
    puw.configure.set_standard_units(
        [length, "ps", "K", "mole", "dalton", "e", "kJ/mol", "radians"]
    )
    source = msm.convert(builder_pdb_molsys, to_form="pdbfixer.PDBFixer")
    names = [atom.name for atom in source.topology.atoms()]
    before = puw.get_value(
        msm.get(source, element="atom", coordinates=True), to_unit="nm"
    ).copy()
    if route == "extract":
        result = msm.extract(source, selection=[3, 1], structure_indices=[0])
    else:
        result = msm.convert(
            source, to_form="pdbfixer.PDBFixer", selection=[3, 1], structure_indices=[0]
        )
    assert result is not source
    assert [atom.name for atom in result.topology.atoms()] == [names[1], names[3]]
    actual = puw.get_value(
        msm.get(result, element="atom", coordinates=True), to_unit="nm"
    )
    assert actual.shape == (1, 2, 3)
    np.testing.assert_allclose(actual, before[:, [1, 3]], atol=1e-4)
    assert [atom.name for atom in source.topology.atoms()] == names
    np.testing.assert_array_equal(
        puw.get_value(msm.get(source, element="atom", coordinates=True), to_unit="nm"),
        before,
    )
