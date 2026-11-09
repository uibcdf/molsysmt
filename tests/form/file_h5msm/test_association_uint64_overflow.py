"""Reject out-of-range unsigned maps before a signed transport conversion."""

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import ChemicalStates, Structures, Topology
from molsysmt.native._chemical_state import _ChemicalStateStorage


def _write(path, values, axis):
    link = dict(
        axis=axis,
        source="structures",
        target="topology",
        source_name=None,
        target_name=None,
        indices=values,
    )
    if axis == "structure":
        link.update(
            source="interactions",
            target="interactions",
            source_name="a",
            target_name="b",
        )
        analyses = {
            name: msm.Interactions.from_records(
                [],
                n_atoms=2,
                n_structures=2,
                evaluated_structure_indices=[0, 1],
                method="map_fixture",
            )
            for name in ["a", "b"]
        }
        payload = dict(interactions=analyses)
    else:
        payload = dict(
            structures=Structures(
                coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), "nm")
            )
        )
        if axis == "atom":
            payload["topology"] = Topology(n_atoms=2)
        else:
            states = ChemicalStates(n_atoms=2)
            for _ in range(2):
                states._append_state(_ChemicalStateStorage(n_atoms=2))
            payload["chemical_states"] = states
            link["target"] = "chemical_states"
    return msm.h5msm.write_layers(path, **payload, associations=[link])


@pytest.mark.parametrize("invalid", [2**63, 2**64 - 1])
@pytest.mark.parametrize("axis", ["atom", "structure", "structure_state"])
def test_unsigned_out_of_range_maps_are_refused_before_file_creation(
    tmp_path, invalid, axis
):
    path = tmp_path / "invalid.h5msm"
    indices = np.array([invalid, 0], dtype=np.uint64)
    with pytest.raises(ValueError, match="indices|range|outside"):
        _write(path, indices, axis)
    assert not path.exists()
    np.testing.assert_array_equal(indices, np.array([invalid, 0], dtype=np.uint64))


@pytest.mark.parametrize(
    "indices", [np.array([1, 0], dtype=np.uint64), np.array([-1, 0], dtype=np.int64)]
)
@pytest.mark.parametrize("axis", ["atom", "structure", "structure_state"])
def test_valid_unsigned_and_signed_unknown_maps_keep_their_meaning(
    tmp_path, indices, axis
):
    path = tmp_path / "valid.h5msm"
    _write(path, indices, axis)
    layers = msm.h5msm.read_layers(path, layers="associations")
    np.testing.assert_array_equal(layers["associations"][0]["indices"], indices)
