"""Exercise attributed profiles through scoped periodic and persisted analyses."""

import numpy as np
import pytest
from rdkit import Chem

import molsysmt as msm
from molsysmt import pyunitwizard as puw


@pytest.mark.parametrize("method", ["prolif", "molstar_geometry", "mdtraj_geometry"])
def test_attributed_periodic_scopes_units_and_named_nan_measure_roundtrip(method, tmp_path):
    angles = np.arange(6) * np.pi / 3
    ring = np.column_stack((.14 * np.cos(angles), .14 * np.sin(angles), np.zeros(6)))
    xyz = np.array([np.concatenate((ring, ring + [2, 0, .35])),
                    np.concatenate((ring, ring + [2, 1, 0]))])
    molsys = msm.convert(Chem.MolFromSmiles("c1ccccc1.c1ccccc1"), to_form="molsysmt.MolSys")
    box = np.eye(3) * 2
    molsys.structures.append(coordinates=puw.quantity(xyz * 10, "angstrom"),
                             box=puw.quantity(np.repeat(box[None] * 10, 2, axis=0), "angstrom"))
    with puw.context(standard_units=["angstrom", "degrees", "ps", "e"]):
        result = msm.interactions.pi_pi.get_pi_pi_interactions(
            molsys, method=method, selection=list(range(6)), selection_mode="incident",
            structure_indices=[1, 0, 1])
    assert result.occurrence_structures.tolist() == [0]
    assert result.evaluated_structure_indices.tolist() == [0, 1]
    assert result.query(atom_indices=[0], mode="incident").n_interactions == 1
    assert result.query(atom_indices=list(range(6)), mode="internal").n_interactions == 0
    assert result.measure_units["distance"] == "nm"
    assert result.measure_units["plane_angle"] == "radians"
    np.testing.assert_allclose(result.measurements["distance"], .35, atol=1e-12)
    assert result.image_vectors.tolist() == [[0, 0, 0], [-1, 0, 0]]
    assert np.isnan(result.measurements["intersection_distance"]).all()
    molsys.interactions = {method: result}
    path = str(tmp_path / "analysis.h5msm")
    msm.convert(molsys, to_form=path)
    restored = msm.convert(path, to_form="molsysmt.MolSys").interactions[method]
    assert restored.parameters == result.parameters
    assert restored.software == result.software
    assert restored.to_dict()["occurrence_indices"].tolist() == result.to_dict()["occurrence_indices"].tolist()
    np.testing.assert_array_equal(restored.image_vectors, result.image_vectors)
    assert np.isnan(restored.measurements["intersection_distance"]).all()


@pytest.mark.parametrize(("method", "arguments"), [
    ("prolif", {"offset_threshold": ".1 nm"}),
    ("prolif", {"angle_threshold": "20 degrees"}),
    ("mdtraj_geometry", {"planarity_threshold": ".01 nm"}),
    ("molstar_geometry", {"planarity_threshold": ".01 nm"}),
])
def test_profiles_reject_mixing_custom_criteria(method, arguments):
    molsys = Chem.MolFromSmiles("c1ccccc1.c1ccccc1")
    with pytest.raises(msm.ArgumentError):
        msm.interactions.pi_pi.get_pi_pi_interactions(molsys, method=method, **arguments)
