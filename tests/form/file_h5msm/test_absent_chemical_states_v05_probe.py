"""Probe native H5MSM 0.5 combinations without a chemical-state layer."""

import pickle

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    read_no_chemical_states_molsys_file,
    write_modular_file,
    write_no_chemical_states_molsys_file,
)
from molsysmt.native import MolSys, Structures, Topology


def _topology():
    topology = Topology(n_atoms=3)
    topology._clear_chemical_states()
    return topology


def _structures():
    return Structures(coordinates=msm.pyunitwizard.quantity(np.zeros((2, 3, 3)), "nm"))


def _link(indices):
    return {
        "axis": "atom",
        "source": "structures",
        "target": "topology",
        "source_name": None,
        "target_name": None,
        "indices": indices,
    }


def _analysis():
    return msm.Interactions.from_records(
        [
            {
                "structure_index": 1,
                "interaction_type": "hbond",
                "participants": [
                    {"role": "donor", "atom_indices": [0]},
                    {"role": "hydrogen", "atom_indices": [1]},
                    {"role": "acceptor", "atom_indices": [2]},
                ],
                "measurements": {"distance": 0.20},
            }
        ],
        n_atoms=3,
        n_structures=2,
        evaluated_structure_indices=[0, 1],
        method="candidate",
        measure_units={"distance": "nm"},
    )


@pytest.mark.parametrize(
    "has_topology,has_structures",
    [
        (True, False),
        (False, True),
        (True, True),
    ],
)
def test_absent_chemistry_roundtrip_preserves_domain_presence(
    tmp_path, has_topology, has_structures
):
    system = MolSys._from_partial_domains(
        topology=_topology() if has_topology else None,
        structures=_structures() if has_structures else None,
    )
    filename = tmp_path / "without_chemistry.h5msm"
    write_no_chemical_states_molsys_file(filename, system)
    with h5py.File(filename, "r") as file:
        assert "chemical_states" not in file
        assert ("topology" in file) == has_topology
        assert ("structures" in file) == has_structures

    restored = read_no_chemical_states_molsys_file(filename)
    assert restored.chemical_states is None
    assert (restored.topology is not None) == has_topology
    assert (restored.structures is not None) == has_structures
    assert restored.get_n_atoms() == 3
    assert msm.get(restored, n_chemical_states=True) is None
    assert not msm.has_attribute(restored, "n_bonds", include_none=True)
    assert not msm.has_attribute(restored, "n_components", include_none=True)
    with pytest.raises(ValueError, match="no chemical-states domain"):
        msm.convert(restored, to_form="molsysmt.ChemicalStates")
    with pytest.raises(ValueError, match="no chemical-states domain"):
        msm.convert(restored, to_form="molsysmt.ChemicalStatesDict")

    for clone in (restored.copy(), pickle.loads(pickle.dumps(restored))):
        assert clone.chemical_states is None
        assert (clone.topology is not None) == has_topology
        assert (clone.structures is not None) == has_structures

    if has_topology and has_structures:
        modern_filename = tmp_path / "modern.h5msm"
        msm.convert(restored, to_form="file:h5msm", output_filename=modern_filename)
        assert msm.h5msm.read(modern_filename).chemical_states is None
        with pytest.raises(
            ValueError, match="requires topology, chemical states, and structures"
        ):
            msm.convert(restored, to_form="molsysmt.MolSysDict")


def test_frame_only_structures_keep_an_unknown_atom_count(tmp_path):
    frames = Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
    system = MolSys._from_partial_domains(structures=frames)
    assert system.get_n_atoms() is None
    filename = tmp_path / "time_only.h5msm"
    write_no_chemical_states_molsys_file(filename, system)

    restored = read_no_chemical_states_molsys_file(filename)
    assert restored.topology is None
    assert restored.chemical_states is None
    assert restored.get_n_atoms() is None
    assert not msm.has_attribute(restored, "n_atoms", include_none=True)
    assert msm.get(restored, n_structures=True) == 2
    selected = restored.extract(structure_indices=[1, 0, 1])
    assert selected.topology is None
    assert selected.get_n_atoms() is None
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(selected.structures.time, to_unit="ps"),
        [1.0, 0.0, 1.0],
    )
    with pytest.raises(ValueError, match="declared atom-index domain"):
        restored.extract(atom_indices=[0])


@pytest.mark.parametrize("has_topology", [False, True])
def test_public_05_roundtrip_of_structures_and_interactions_without_chemistry(
    tmp_path, has_topology
):
    system = MolSys._from_partial_domains(
        topology=_topology() if has_topology else None,
        structures=_structures(),
        interactions={"candidate": _analysis()},
    )
    filename = str(tmp_path / "structure_interactions.h5msm")
    msm.h5msm.write(system, filename)

    with h5py.File(filename, "r") as file:
        assert "chemical_states" not in file
        assert "interactions" in file
        assert ("topology" in file) == has_topology
    restored = msm.h5msm.read(filename)
    assert (restored.topology is not None) == has_topology
    assert restored.chemical_states is None
    assert restored.structures.coordinates.shape == (2, 3, 3)
    observed = restored.interactions["candidate"]
    assert observed.query(structure_indices=[0]).n_interactions == 0
    assert observed.query(structure_indices=[1], atom_indices=[0]).n_interactions == 1
    assert observed.measure_units == {"distance": "nm"}
    assert observed.measurements["distance"].tolist() == [0.20]
    assert restored.copy().interactions["candidate"].n_interactions == 1

    if not has_topology:
        selected = restored.extract(atom_indices=[2, 0, 1], structure_indices=[1, 0, 1])
        assert selected.topology is None
        assert selected.structures.coordinates.shape == (3, 3, 3)
        selected_analysis = selected.interactions["candidate"]
        assert selected_analysis.n_interactions == 2
        np.testing.assert_array_equal(selected_analysis.atom_source_indices, [2, 0, 1])
        np.testing.assert_array_equal(
            selected_analysis.structure_source_indices, [1, 0, 1]
        )
        assert selected_analysis.query(structure_indices=[0]).n_interactions == 1
        assert selected_analysis.query(structure_indices=[2]).n_interactions == 1
        dropped = restored.extract(atom_indices=[2, 0])
        assert dropped.interactions["candidate"].n_interactions == 0
        assert dropped.interactions["candidate"].query(structure_indices=[0]).to_dict()[
            "evaluated_structure_indices"
        ].tolist() == [0]

    converted_filename = tmp_path / "converted_structure_interactions.h5msm"
    msm.convert(system, to_form="file:h5msm", output_filename=converted_filename)
    converted = msm.convert(converted_filename, to_form="molsysmt.MolSys")
    assert converted.chemical_states is None
    assert (
        converted.interactions["candidate"]
        .query(structure_indices=[1], atom_indices=[0])
        .n_interactions
        == 1
    )


def test_reader_rejects_unlinked_interaction_axes_without_chemistry(tmp_path):
    filename = tmp_path / "unlinked_interactions.h5msm"
    write_modular_file(
        filename,
        structures=_structures(),
        interactions={"candidate": _analysis()},
    )
    with pytest.raises(ValueError, match="declared identity links"):
        msm.h5msm.read(str(filename))


@pytest.mark.parametrize("indices", [None, [1, 0, 2]])
def test_reader_rejects_undeclared_or_reordered_shared_atom_axis(tmp_path, indices):
    filename = tmp_path / "unrepresentable.h5msm"
    write_modular_file(
        filename,
        topology=_topology(),
        structures=_structures(),
        associations=None if indices is None else [_link(indices)],
    )
    with pytest.raises(ValueError, match="declared identity links"):
        read_no_chemical_states_molsys_file(filename)


def test_absent_chemistry_does_not_accept_a_topology_with_hidden_states():
    with pytest.raises(ValueError, match="must have no states"):
        MolSys._from_partial_domains(topology=Topology(n_atoms=3))
