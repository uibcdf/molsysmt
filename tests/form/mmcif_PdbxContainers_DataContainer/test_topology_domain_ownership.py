"""Retaining native ownership after declared entry-CIF construction."""

import numpy as np
import pytest

import molsysmt as msm

from .test_connectivity_policy import _as_file, _declared_source


@pytest.mark.parametrize("form", ["container", "cif", "bcif"])
def test_entry_conversion_keeps_components_outside_topology_and_allows_permutation(
    tmp_path, form
):
    container = _declared_source()
    item = container if form == "container" else _as_file(container, tmp_path, form)
    source = msm.convert(item, to_form="molsysmt.MolSys", get_missing_bonds=False)
    before_atoms = source.topology.atoms.copy(deep=True)
    coordinates = msm.pyunitwizard.get_value(
        source.structures.coordinates, to_unit="nm"
    ).copy()
    assert "_components_dirty" not in vars(source.topology)
    assert msm.get(source, n_components=True) == 1
    result = msm.permute_atoms(source, atom_indices=[1, 0])
    assert (
        result.topology.atoms.atom_name.tolist()
        == before_atoms.atom_name.tolist()[::-1]
    )
    assert source.topology.atoms.equals(before_atoms)
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(result.structures.coordinates, to_unit="nm"),
        coordinates[:, ::-1],
    )
    assert msm.get(result, n_bonds=True) == 1
    assert msm.get(result, n_components=True) == 1
