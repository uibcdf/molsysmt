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


@pytest.mark.parametrize(
    "n_structures,n_states,indices",
    [(1, 2, [0]), (2, 3, [0, 1]), (2, 2, [0, 1]), (2, 3, [2, 0]), (3, 2, [1, 0, None])],
)
def test_public_unequal_structure_state_populations_roundtrip(
    tmp_path, n_structures, n_states, indices
):
    """Preserve actual state maps, reference and geometry through the public file path."""
    from molsysmt.native import MolSys

    molsys = MolSys(n_atoms=3)
    molsys.topology.atoms["atom_type"] = ["C", "N", "O"]
    molsys.topology.atoms["atom_id"] = ["a", "b", "c"]
    for _ in range(n_states - 1):
        molsys.chemical_states.append_state()
    for state_index in range(n_states):
        molsys.chemical_states._states[state_index].set_atom_attribute(
            "formal_charge", [state_index, -state_index, 0]
        )
    molsys.chemical_states._set_reference_index(n_states - 1)
    xyz = np.arange(n_structures * 9, dtype=float).reshape(n_structures, 3, 3) / 100
    molsys.structures = Structures(coordinates=msm.pyunitwizard.quantity(xyz, "nm"))
    msm.set(molsys, structure_chemical_state_index=indices)
    source_mapping = msm.get(molsys, structure_chemical_state_index=True)
    filename = tmp_path / "states.h5msm"
    msm.convert(molsys, to_form=filename)
    with h5py.File(filename, "r") as file:
        link = next(
            child
            for child in file["associations"].values()
            if child.attrs["axis"] == "structure_state"
        )
        if n_structures == n_states and indices == list(range(n_structures)):
            assert link.attrs["mapping"] == "identity"
            assert "indices" not in link
        else:
            assert link.attrs["mapping"] == "explicit"
            np.testing.assert_array_equal(
                link["indices"][:], [-1 if i is None else i for i in indices]
            )
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert restored.chemical_states.n_chemical_states == n_states
    assert restored.chemical_states.reference_chemical_state_index == n_states - 1
    assert msm.get(restored, structure_chemical_state_index=True) == source_mapping
    assert msm.get(molsys, structure_chemical_state_index=True) == source_mapping
    assert restored.topology.atoms.atom_id.tolist() == ["a", "b", "c"]
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.structures.coordinates, to_unit="nm"), xyz
    )
    layers = msm.h5msm.read_layers(filename)
    assert layers["chemical_states"].n_chemical_states == n_states
    for structure_index, state_index in enumerate(indices):
        report = msm.physchem.get_chemical_readiness(
            filename,
            selection=[0],
            structure_indices=[structure_index],
            chemical_state="structure",
        )
        if state_index is None:
            assert report["chemical_state_status"] == "unassociated"
        else:
            assert report["chemical_state_index"] == state_index
            assert report["fields"]["formal_charge"]["values"].tolist() == [state_index]
    reference = msm.physchem.get_chemical_readiness(
        filename, selection=[0], structure_indices=[0]
    )
    assert reference["chemical_state_index"] == n_states - 1
    assert reference["fields"]["formal_charge"]["values"].tolist() == [n_states - 1]


@pytest.mark.parametrize(
    "axis,source,target,source_axis,target_axis",
    [
        ("atom", "structures", "topology", "atom", "atom"),
        ("structure", "interactions", "structures", "structure", "structure"),
        ("structure_state", "structures", "chemical_states", "structure", "state"),
    ],
)
@pytest.mark.parametrize(
    "source_size,target_size", [(0, 0), (0, 2), (1, 2), (2, 3), (2, 2)]
)
def test_prefix_maps_are_idempotent_without_inventing_identity(
    axis, source, target, source_axis, target_axis, source_size, target_size
):
    """The shared codec must not turn an explicit prefix into a full-domain identity."""
    from molsysmt.form._h5msm05_associations import normalize_associations

    name = "analysis" if source == "interactions" else None
    sizes = {
        (source, name, source_axis): source_size,
        (target, None, target_axis): target_size,
    }
    values = np.arange(source_size, dtype=np.int32)
    links = [_link(axis, source, target, values, source_name=name)]
    normalized = normalize_associations(links, sizes)
    repeated = normalize_associations(normalized, sizes)
    if source_size == target_size:
        assert normalized[0]["indices"] == repeated[0]["indices"] == "identity"
    else:
        np.testing.assert_array_equal(normalized[0]["indices"], values)
        np.testing.assert_array_equal(repeated[0]["indices"], values)
        assert normalized[0]["indices"].dtype == np.int64
    np.testing.assert_array_equal(values, np.arange(source_size, dtype=np.int32))


@pytest.mark.parametrize(
    "indices,message",
    [
        ("identity", "equal cardinalities"),
        ([0], "source axis length"),
        ([0, 3], "outside the target axis"),
        ([-2, 0], "outside the target axis"),
        ([0, 0], "cannot map distinct atoms"),
    ],
)
def test_prefix_fix_keeps_invalid_associations_atomic(tmp_path, indices, message):
    filename = tmp_path / "existing.h5msm"
    filename.write_bytes(b"unchanged destination")
    with pytest.raises(ValueError, match=message):
        msm.h5msm.write_layers(
            filename,
            topology=Topology(n_atoms=3),
            structures=Structures(
                coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
            ),
            associations=[_link("atom", "structures", "topology", indices)],
        )
    assert filename.read_bytes() == b"unchanged destination"


@pytest.mark.parametrize("axis", ["atom", "structure"])
def test_independent_prefix_layer_roundtrip_keeps_reader_strict(tmp_path, axis):
    """Write actual partial layers, then reject a forged full-domain identity."""
    filename = tmp_path / "prefix.h5msm"
    if axis == "atom":
        associations = [_link("atom", "structures", "topology", [0])]
        domains = dict(
            topology=Topology(n_atoms=2),
            structures=Structures(
                coordinates=msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), "nm")
            ),
        )
    else:
        associations = [
            _link(
                "structure", "interactions", "structures", [0], source_name="analysis"
            )
        ]
        domains = dict(
            structures=Structures(
                coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), "nm")
            ),
            interactions={
                "analysis": msm.Interactions.from_records(
                    [],
                    n_atoms=2,
                    n_structures=1,
                    evaluated_structure_indices=[0],
                    method="test.prefix",
                )
            },
        )
    msm.h5msm.write_layers(filename, associations=associations, **domains)
    restored = msm.h5msm.read_layers(filename)
    np.testing.assert_array_equal(restored["associations"][0]["indices"], [0])
    with h5py.File(filename, "r+") as file:
        link = file["associations/0"]
        assert link.attrs["mapping"] == "explicit"
        del link["indices"]
        link.attrs["mapping"] = "identity"
    with pytest.raises(ValueError, match="equal cardinalities"):
        msm.h5msm.read_layers(filename)
