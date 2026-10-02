"""Probe explicit cross-layer axis associations in H5MSM 0.5."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import read_modular_file, write_modular_file
from molsysmt.native import Structures, Topology


def _link(axis, source, target, indices, *, source_name=None, target_name=None):
    return {
        "axis": axis,
        "source": source,
        "target": target,
        "source_name": source_name,
        "target_name": target_name,
        "indices": indices,
    }


def _domains():
    topology = Topology(n_atoms=3)
    topology.add_bonds([[0, 1]])
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm")
    )
    interactions = msm.Interactions.from_records(
        [],
        n_atoms=3,
        n_structures=2,
        evaluated_structure_indices=[0, 1],
        method="candidate",
    )
    return topology, structures, interactions


def test_identity_and_reordered_links_are_explicit_and_compact(tmp_path):
    topology, structures, interactions = _domains()
    filename = tmp_path / "linked.h5msm"
    links = [
        _link("atom", "chemical_states", "topology", "identity"),
        _link("atom", "structures", "topology", [2, 0, 1]),
        _link("atom", "interactions", "topology", "identity", source_name="hbonds"),
        _link(
            "structure", "interactions", "structures", "identity", source_name="hbonds"
        ),
        _link("structure_state", "structures", "chemical_states", [0, 0]),
    ]
    write_modular_file(
        filename,
        topology=topology,
        chemical_states=msm.convert(topology, to_form="molsysmt.ChemicalStates"),
        structures=structures,
        interactions={"hbonds": interactions},
        associations=links,
    )
    with h5py.File(filename, "r") as file:
        assert set(file) == {
            "topology",
            "chemical_states",
            "structures",
            "interactions",
            "associations",
        }
        assert file["associations/0"].attrs["mapping"] == "identity"
        assert "indices" not in file["associations/0"]
        assert file["associations/1/indices"][:].tolist() == [2, 0, 1]

    restored = read_modular_file(filename)
    assert len(restored["associations"]) == 5
    np.testing.assert_array_equal(restored["associations"][1]["indices"], [2, 0, 1])
    assert restored["associations"][0]["indices"] == "identity"
    np.testing.assert_array_equal(restored["associations"][4]["indices"], [0, 0])
    assert restored["chemical_states"].n_chemical_states == 1
    assert restored["interactions"]["hbonds"].n_structures == 2


def test_equal_cardinality_does_not_imply_an_association(tmp_path):
    topology, structures, _ = _domains()
    filename = tmp_path / "unlinked.h5msm"
    write_modular_file(filename, topology=topology, structures=structures)
    assert read_modular_file(filename)["associations"] is None

    empty_filename = tmp_path / "explicitly_empty_links.h5msm"
    write_modular_file(
        empty_filename, topology=topology, structures=structures, associations=[]
    )
    assert read_modular_file(empty_filename)["associations"] == []


def test_invalid_link_fails_before_file_creation_and_tampering_is_rejected(tmp_path):
    topology, structures, _ = _domains()
    filename = tmp_path / "invalid.h5msm"
    with pytest.raises(ValueError, match="outside the target axis"):
        write_modular_file(
            filename,
            topology=topology,
            structures=structures,
            associations=[_link("atom", "structures", "topology", [0, 1, 3])],
        )
    assert not filename.exists()
    with pytest.raises(ValueError, match="cannot map distinct atoms"):
        write_modular_file(
            filename,
            topology=topology,
            structures=structures,
            associations=[_link("atom", "structures", "topology", [0, 0, 1])],
        )
    assert not filename.exists()

    write_modular_file(
        filename,
        topology=topology,
        structures=structures,
        associations=[_link("atom", "structures", "topology", [2, 0, 1])],
    )
    with h5py.File(filename, "r+") as file:
        file["associations/0/indices"][2] = 9
    with pytest.raises(ValueError, match="outside the target axis"):
        read_modular_file(filename)


def test_contradictory_direct_and_indirect_atom_maps_are_rejected(tmp_path):
    topology, structures, _ = _domains()
    filename = tmp_path / "contradictory.h5msm"
    with pytest.raises(ValueError, match="Direct and composed axis links disagree"):
        write_modular_file(
            filename,
            topology=topology,
            chemical_states=msm.convert(topology, to_form="molsysmt.ChemicalStates"),
            structures=structures,
            associations=[
                _link("atom", "structures", "chemical_states", "identity"),
                _link("atom", "chemical_states", "topology", "identity"),
                _link("atom", "structures", "topology", [2, 0, 1]),
            ],
        )
    assert not filename.exists()


@pytest.mark.parametrize(
    ("has_topology", "has_states", "has_structures"),
    [
        (True, False, False),
        (False, True, False),
        (False, False, True),
        (True, True, False),
        (True, False, True),
        (False, True, True),
        (True, True, True),
    ],
)
def test_every_nonempty_primary_domain_combination_roundtrips(
    tmp_path, has_topology, has_states, has_structures
):
    topology, structures, _ = _domains()
    filename = tmp_path / "combination.h5msm"
    write_modular_file(
        filename,
        topology=topology if has_topology else None,
        chemical_states=(
            msm.convert(topology, to_form="molsysmt.ChemicalStates")
            if has_states
            else None
        ),
        structures=structures if has_structures else None,
    )
    restored = read_modular_file(filename)
    assert (restored["topology"] is not None) == has_topology
    assert (restored["chemical_states"] is not None) == has_states
    assert (restored["structures"] is not None) == has_structures
    assert restored["interactions"] is None
    assert restored["associations"] is None
