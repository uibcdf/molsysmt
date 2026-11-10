"""Do not describe regenerated positions as lost structural observations."""

import warnings

import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralAttributeOffAxisWarning
from molsysmt.native import Structures


@pytest.mark.parametrize("reverse", [False, True])
@pytest.mark.parametrize("stable_form", ["molsys", "topology"])
def test_complementary_single_structure_has_no_derived_index_loss_warning(
    reverse, stable_form
):
    pytest.importorskip("rdkit")
    source = msm.convert("smiles:CO", to_form="molsysmt.MolSys")
    assert msm.get(source, n_atoms=True) == 2
    assert msm.get(source, n_structures=True) in (0, None)
    stable = source if stable_form == "molsys" else source.topology
    coordinates = msm.pyunitwizard.quantity(
        np.array([[[0, 0, 0], [0.14, 0, 0]]], dtype=float), "nm"
    )
    structures = Structures()
    structures.coordinates = coordinates
    items = [stable, structures]
    if reverse:
        items.reverse()
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        output = msm.convert(items, to_form="molsysmt.MolSys", selection="all")
    assert not [
        item
        for item in caught
        if issubclass(item.category, StructuralAttributeOffAxisWarning)
    ], [str(item.message) for item in caught]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(output.structures.coordinates, to_unit="nm"),
        [[[0, 0, 0], [0.14, 0, 0]]],
    )
    np.testing.assert_array_equal(
        msm.get(output.topology, element="atom", atom_index=True), [0, 1]
    )
    np.testing.assert_array_equal(
        msm.get(output.topology, element="atom", atom_name=True),
        np.asarray(msm.get(source, element="atom", atom_name=True)),
    )
    assert msm.get(source, n_structures=True) in (0, None)


def test_real_off_axis_series_still_warns_without_index_noise(monkeypatch):
    from molsysmt._private import structure_axis
    from molsysmt.basic.convert import _prune_structural_attributes_off_the_axis

    monkeypatch.setattr(structure_axis, "structure_axis", lambda *a, **kw: (2, [1, 2]))
    attributes = [
        {"time", "atom_index", "structure_index", "coordinates"},
        {"coordinates"},
    ]
    with pytest.warns(StructuralAttributeOffAxisWarning) as caught:
        _prune_structural_attributes_off_the_axis(
            [object(), object()], ["molsysmt.MolSys"] * 2, attributes
        )
    messages = " ".join(str(item.message) for item in caught)
    assert (
        "time" in messages
        and "atom_index" not in messages
        and "structure_index" not in messages
    )
    assert "time" not in attributes[0]
    assert "coordinates" in attributes[1]
