"""Probe H5MSM 0.5 native topology and chemistry without structures."""

import pickle

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    read_topology_chemistry_molsys_file,
    write_modular_file,
    write_topology_chemistry_molsys_file,
)
from molsysmt.native import MolSys, Topology


def _domains():
    topology = Topology(n_atoms=3)
    topology.add_bonds([[0, 1]])
    states = msm.convert(topology, to_form="molsysmt.ChemicalStates")
    return topology, states


def test_topology_and_chemistry_roundtrip_without_structures(tmp_path):
    topology, states = _domains()
    system = MolSys._from_partial_domains(topology=topology, chemical_states=states)
    filename = tmp_path / "topology_chemistry.h5msm"
    write_topology_chemistry_molsys_file(filename, system)
    with h5py.File(filename, "r") as file:
        assert set(file) == {"topology", "chemical_states", "associations"}
        assert "bonds" not in file["topology"]

    restored = read_topology_chemistry_molsys_file(filename)
    assert restored.structures is None
    assert restored.topology.n_atoms == 3
    assert restored.chemical_states is restored.topology._chemical_states_domain
    assert len(restored.chemical_states.get_bonds()) == 1
    assert msm.get(restored, n_atoms=True) == 3
    assert msm.get(restored, n_structures=True) is None

    for clone in (restored.copy(), pickle.loads(pickle.dumps(restored))):
        assert clone.structures is None
        assert clone.chemical_states is clone.topology._chemical_states_domain
        assert len(clone.chemical_states.get_bonds()) == 1


@pytest.mark.parametrize(
    "route", ["native", "extract", "convert", "file_extract", "file_convert"]
)
def test_real_topology_chemistry_atom_selection_without_coordinates(tmp_path, route):
    source = msm.convert(
        msm.systems["pentalanine"]["traj_pentalanine.h5msm"],
        to_form="molsysmt.MolSys",
        selection=list(range(10)),
        structure_indices=[0, 8, 3],
    )
    filename = str(tmp_path / "topology_chemistry.h5msm")
    msm.h5msm.write_layers(
        filename,
        topology=source.topology,
        chemical_states=source.chemical_states,
        associations=[
            {
                "axis": "atom",
                "source": "chemical_states",
                "target": "topology",
                "source_name": None,
                "target_name": None,
                "indices": "identity",
            }
        ],
    )
    partial = msm.convert(filename, to_form="molsysmt.MolSys")
    selected = [4, 0, 1]
    if route == "native":
        extracted = partial.extract(atom_indices=selected)
    elif route in {"extract", "file_extract"}:
        extracted = msm.extract(
            filename if route.startswith("file_") else partial,
            selection=selected,
            to_form="molsysmt.MolSys" if route == "file_extract" else None,
        )
        if route == "file_extract":
            extracted = msm.convert(extracted, to_form="molsysmt.MolSys")
    else:
        extracted = msm.convert(
            filename if route.startswith("file_") else partial,
            to_form="molsysmt.MolSys",
            selection=selected,
        )
    assert extracted.structures is None
    assert msm.get(extracted, n_structures=True) is None
    assert extracted.topology.atoms["atom_id"].tolist() == (
        source.topology.atoms.iloc[[0, 1, 4]]["atom_id"].tolist()
    )
    assert extracted.chemical_states is extracted.topology._chemical_states_domain
    assert extracted.chemical_states.n_atoms == 3
    source_bonds = source.chemical_states.get_bonds()
    old_to_new = {0: 0, 1: 1, 4: 2}
    expected = [
        [old_to_new[int(a)], old_to_new[int(b)]]
        for a, b in source_bonds[["atom1_index", "atom2_index"]].itertuples(
            index=False, name=None
        )
        if int(a) in old_to_new and int(b) in old_to_new
    ]
    assert expected, (
        "The real selection must retain bonds to exercise endpoint remapping."
    )
    np.testing.assert_array_equal(
        extracted.chemical_states.get_bonds()[
            ["atom1_index", "atom2_index"]
        ].to_numpy(),
        np.asarray(expected, dtype=np.int64).reshape(-1, 2),
    )
    assert partial.structures is None
    assert partial.get_n_atoms() == 10
    output = str(tmp_path / f"selected_{route}.h5msm")
    msm.convert(extracted, to_form="file:h5msm", output_filename=output)
    restored = msm.h5msm.read(output)
    assert restored.structures is None
    assert restored.chemical_states is restored.topology._chemical_states_domain
    assert (
        restored.topology.atoms["atom_id"].tolist()
        == extracted.topology.atoms["atom_id"].tolist()
    )


@pytest.mark.parametrize("selection", [[0], []])
def test_topology_chemistry_rejects_an_undeclared_structure_axis(selection):
    topology, states = _domains()
    system = MolSys._from_partial_domains(topology=topology, chemical_states=states)
    with pytest.raises(ValueError, match="declared structure-index domain"):
        system.extract(atom_indices=[0], structure_indices=selection)
    assert system.structures is None
    assert system.get_n_atoms() == 3


def test_topology_only_selection_does_not_invent_chemistry_or_structures():
    topology = Topology(n_atoms=3)
    topology.atoms["atom_id"] = ["0", "1", "2"]
    topology._clear_chemical_states()
    system = MolSys._from_partial_domains(topology=topology)
    selected = system.extract(atom_indices=[2, 0])
    assert selected.get_n_atoms() == 2
    assert selected.chemical_states is None
    assert selected.structures is None
    assert selected.topology.atoms["atom_id"].tolist() == ["0", "2"]
    assert system.get_n_atoms() == 3


def test_topology_chemistry_selection_preserves_multiple_states_and_metadata():
    topology, states = _domains()
    states._states[0].state_id = "reference-id"
    states.append_state()
    states._states[1].state_id = "alternate-id"
    states._states[1].provenance_index = 7
    states._states[1].atom_attributes["formal_charge"] = [0, 1, -1]
    states._set_reference_index(1)
    system = MolSys._from_partial_domains(topology=topology, chemical_states=states)
    selected = system.extract(atom_indices=[2, 1])
    assert selected.structures is None
    assert selected.chemical_states is selected.topology._chemical_states_domain
    assert selected.chemical_states.n_chemical_states == 2
    assert selected.chemical_states.reference_chemical_state_index == 1
    assert [state.state_id for state in selected.chemical_states._states] == [
        "reference-id",
        "alternate-id",
    ]
    assert selected.chemical_states._states[1].provenance_index == 7
    assert selected.chemical_states._states[1].atom_attributes[
        "formal_charge"
    ].tolist() == [1, -1]
    assert selected.chemical_states.get_bonds(chemical_state=0).empty
    selected.chemical_states._states[1].atom_attributes.at[0, "formal_charge"] = 0
    assert states._states[1].atom_attributes["formal_charge"].tolist() == [0, 1, -1]


def test_structure_axis_from_interactions_is_selectable_without_coordinates():
    topology, states = _domains()
    analysis = msm.Interactions.from_records(
        [
            {
                "structure_index": index,
                "interaction_type": "disulfide_candidate",
                "participants": [
                    {"role": "sulfur", "atom_indices": [0]},
                    {"role": "sulfur", "atom_indices": [2]},
                ],
                "measurements": {"distance": distance},
            }
            for index, distance in [(1, 0.21), (3, 0.22)]
        ],
        n_atoms=3,
        n_structures=4,
        evaluated_structure_indices=[0, 1, 2, 3],
        method="declared_candidate",
        measure_units={"distance": "nm"},
    )
    system = MolSys._from_partial_domains(
        topology=topology, chemical_states=states, interactions={"candidate": analysis}
    )
    selected = system.extract(atom_indices=[2, 0], structure_indices=[3, 1, 3])
    assert selected.structures is None
    observed = selected.interactions["candidate"]
    assert observed.n_interactions == 3
    np.testing.assert_array_equal(observed.atom_source_indices, [0, 2])
    np.testing.assert_array_equal(observed.structure_source_indices, [3, 1, 3])
    assert observed.query(structure_indices=[0]).n_interactions == 1
    assert observed.query(structure_indices=[1]).n_interactions == 1
    assert observed.query(structure_indices=[2]).n_interactions == 1
    assert observed.measure_units == {"distance": "nm"}
    assert system.interactions["candidate"].n_interactions == 2


@pytest.mark.parametrize("indices", [None, [1, 0, 2]])
def test_reader_requires_one_identity_atom_link(tmp_path, indices):
    topology, states = _domains()
    filename = tmp_path / "unrepresentable.h5msm"
    associations = (
        None
        if indices is None
        else [
            {
                "axis": "atom",
                "source": "chemical_states",
                "target": "topology",
                "source_name": None,
                "target_name": None,
                "indices": indices,
            }
        ]
    )
    write_modular_file(
        filename,
        topology=topology,
        chemical_states=states,
        associations=associations,
    )
    with pytest.raises(ValueError, match="declared identity atom-axis link"):
        read_topology_chemistry_molsys_file(filename)
