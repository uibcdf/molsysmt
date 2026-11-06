"""Checking source-index label correspondences independently of chemical states."""

import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import ArgumentError, StructuralInconsistencyError
from molsysmt.native import MolSys, Topology


def topology(names=("C1", "O1", "N1"), elements=("C", "O", "N")):
    result = Topology(n_atoms=len(names), n_groups=1 if names else 0)
    result.atoms["atom_name"] = list(names)
    result.atoms["atom_type"] = list(elements)
    result.atoms["atom_id"] = [str(100 + index) for index in range(len(names))]
    return result


@pytest.mark.parametrize(
    "form", ["topology", "system", "topology_dict", "system_dict", "h5msm"]
)
def test_exact_names_match_source_indices_in_supported_forms(form, tmp_path):
    source = topology()
    if form != "topology":
        source = MolSys._from_partial_domains(topology=source)
    if form.endswith("_dict"):
        source = msm.convert(
            source,
            to_form="molsysmt.TopologyDict"
            if form == "topology_dict"
            else "molsysmt.MolSysDict",
        )
    elif form == "h5msm":
        source = msm.convert(source, to_form=str(tmp_path / "names.h5msm"))
    reference = topology(("N1", "C1", "O1"), ("N", "C", "O"))
    result = msm.topology.get_atom_name_correspondence(
        source, reference_molecular_system=reference
    )
    np.testing.assert_array_equal(result, [[0, 1], [1, 2], [2, 0]])
    assert result.dtype == np.int64
    assert reference.atoms.atom_id.tolist() == ["100", "101", "102"]


def test_nonconsecutive_selection_retains_both_full_source_axes():
    source = topology(("unused", "N1", "C1", "O1"), ("H", "N", "C", "O"))
    reference = topology(("C1", "outside", "N1", "O1"), ("C", "H", "N", "O"))
    result = msm.topology.get_atom_name_correspondence(
        source,
        selection=[3, 1],
        reference_molecular_system=reference,
        reference_selection=[2, 3],
    )
    np.testing.assert_array_equal(result, [[3, 3], [1, 2]])
    result[0, 0] = -1
    assert source.atoms.atom_name.tolist() == ["unused", "N1", "C1", "O1"]


@pytest.mark.parametrize(
    "names,elements",
    [
        (("C1", "C1", "N1"), ("C", "O", "N")),
        (("C1", "O1", "other"), ("C", "O", "N")),
        (("C1", "O1", "N1"), ("C", "O", "S")),
        (("C1", None, "N1"), ("C", "O", "N")),
    ],
)
def test_ambiguity_and_incompatible_labels_are_refused(names, elements):
    with pytest.raises(StructuralInconsistencyError):
        msm.topology.get_atom_name_correspondence(
            topology(), reference_molecular_system=topology(names, elements)
        )


@pytest.mark.parametrize("selection", [[0, 0], [True, 1], [0.0], [[0]], [-1]])
def test_invalid_or_repeated_positional_indices_are_not_coerced(selection):
    with pytest.raises((ArgumentError, StructuralInconsistencyError)):
        msm.topology.get_atom_name_correspondence(topology(), selection=selection)


def test_empty_correspondence_has_defined_shape_and_types():
    result = msm.topology.get_atom_name_correspondence(topology(), selection=[])
    assert result.shape == (0, 2)
    assert result.dtype == np.int64


def test_coordinate_and_chemical_domains_are_not_required_or_read(monkeypatch):
    source = topology()
    original_get = msm.basic.get

    def only_inventory(*args, **kwargs):
        assert set(key for key, value in kwargs.items() if value is True) == {
            "atom_name",
            "atom_type",
        }
        return original_get(*args, **kwargs)

    monkeypatch.setattr(msm.basic, "get", only_inventory)
    before = source.atoms.copy(deep=True)
    result = msm.topology.get_atom_name_correspondence(source)
    pd.testing.assert_frame_equal(source.atoms, before)
    np.testing.assert_array_equal(result, [[0, 0], [1, 1], [2, 2]])
