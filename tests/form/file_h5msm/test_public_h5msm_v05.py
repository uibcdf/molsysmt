"""Check the explicit public H5MSM 0.5 API and legacy migration."""

import pickle
from importlib.resources import files
from pathlib import Path

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import LegacyH5MSMWarning
from molsysmt.native import ChemicalStates, MolSys, Structures


def test_public_05_read_write_and_layer_selection(tmp_path):
    source = MolSys(n_atoms=2)
    source.topology.add_bonds([[0, 1]])
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), "nm")
    )
    filename = str(tmp_path / "public05.h5msm")
    assert msm.h5msm.write(source, filename) == filename
    restored = msm.h5msm.read(filename)
    assert restored.chemical_states is restored.topology._chemical_states_domain
    assert len(restored.chemical_states.get_bonds()) == 1
    assert restored.structures.coordinates.shape == (2, 2, 3)
    layers = msm.h5msm.read_layers(filename, layers=["chemical_states", "interactions"])
    assert set(layers) == {"chemical_states", "interactions"}
    assert layers["chemical_states"].n_atoms == 2
    assert layers["interactions"] is None


@pytest.mark.parametrize("has_atom_coordinates", [False, True])
def test_public_05_reads_a_structures_only_file_as_molsys(
    tmp_path, has_atom_coordinates
):
    source = (
        Structures(coordinates=msm.pyunitwizard.quantity(
            np.arange(18, dtype=float).reshape(2, 3, 3), "nm"
        ))
        if has_atom_coordinates else
        Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
    )
    filename = str(tmp_path / "structures_only.h5msm")
    msm.h5msm.write_layers(filename, structures=source)

    with h5py.File(filename, "r") as file:
        assert set(file) == {"structures"}
    direct_structures = msm.convert(filename, to_form="molsysmt.Structures")
    assert direct_structures.n_structures == 2
    for restored in (
        msm.h5msm.read(filename),
        msm.convert(filename, to_form="molsysmt.MolSys"),
    ):
        assert restored.topology is None
        assert restored.chemical_states is None
        assert not restored.interactions
        assert restored.structures.n_structures == 2
        assert restored.get_n_atoms() == (3 if has_atom_coordinates else None)
        if has_atom_coordinates:
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(restored.structures.coordinates,
                                             to_unit="nm"),
                np.arange(18, dtype=float).reshape(2, 3, 3),
            )
        else:
            assert restored.structures.coordinates is None
            np.testing.assert_array_equal(
                msm.pyunitwizard.get_value(restored.structures.time, to_unit="ps"),
                [0.0, 1.0],
            )


def test_public_05_writers_reject_mechanics_without_creating_a_file(tmp_path):
    source = MolSys(n_atoms=2)
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    source.molecular_mechanics.forcefield = "example"
    direct = tmp_path / "mechanics_write.h5msm"
    converted = tmp_path / "mechanics_convert.h5msm"

    with pytest.raises(ValueError, match="molecular mechanics"):
        msm.h5msm.write(source, str(direct))
    with pytest.raises(ValueError, match="molecular mechanics"):
        msm.convert(source, to_form="file:h5msm", output_filename=converted)
    assert not direct.exists()
    assert not converted.exists()


def test_public_convert_writes_05_and_roundtrips_native_queries(tmp_path):
    source = MolSys(n_atoms=2)
    source.topology.add_bonds([[0, 1]])
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((2, 2, 3)), "nm")
    )
    filename = tmp_path / "converted.h5msm"

    assert msm.convert(source, to_form="file:h5msm", output_filename=filename) == str(filename)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
    assert msm.get(filename, n_atoms=True) == 2
    assert msm.has_attribute(filename, "coordinates")
    assert msm.select(filename, selection="atom_index==1") == [1]
    restored = msm.convert(filename, to_form="molsysmt.MolSys")
    assert restored.structures.coordinates.shape == (2, 2, 3)
    assert len(restored.chemical_states.get_bonds()) == 1


def test_public_convert_structures_subset_writes_05(tmp_path):
    coordinates = np.arange(36, dtype=float).reshape(3, 4, 3)
    source = Structures(coordinates=msm.pyunitwizard.quantity(coordinates, "nm"))
    filename = tmp_path / "subset.h5msm"

    msm.convert(
        source, to_form=filename, selection=[1, 3],
        structure_indices=[2, 0, 2],
    )
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
    restored = msm.convert(filename, to_form="molsysmt.Structures")
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored.coordinates, to_unit="nm"),
        coordinates[[2, 0, 2]][:, [1, 3], :],
    )


def test_public_convert_preserves_pdb_alternate_locations_in_05(tmp_path):
    source_pdb = str(files("molsysmt.data.pdb").joinpath("1bnf.pdb"))
    source = msm.convert(
        source_pdb, to_form="molsysmt.MolSys", selection=[479, 480],
        get_missing_bonds=False,
    )
    filename = tmp_path / "pdb_alternates.h5msm"
    msm.convert(source, to_form="file:h5msm", output_filename=filename)
    restored = msm.convert(filename, to_form="molsysmt.MolSys")

    assert restored.topology.n_atoms == 2
    original = source.structures.alternate_location[0][1]
    alternate = restored.structures.alternate_location[0][1]
    assert alternate["location_id"].tolist() == ["A", "B"]
    assert alternate["atom_id"].tolist() == original["atom_id"].tolist()
    np.testing.assert_allclose(alternate["occupancy"], original["occupancy"])
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(alternate["coordinates"], to_unit="nm"),
        msm.pyunitwizard.get_value(original["coordinates"], to_unit="nm"),
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(alternate["b_factor"], to_unit="nm**2"),
        msm.pyunitwizard.get_value(original["b_factor"], to_unit="nm**2"),
    )


def test_public_queries_resolve_a_nonreference_state_in_05(tmp_path):
    source = MolSys(n_atoms=2)
    source.topology._append_chemical_state(state_id="second")
    source.topology._set_chemical_state_atom_attribute(
        "formal_charge", [1, -1], state_index=1
    )
    filename = tmp_path / "states.h5msm"
    msm.convert(source, to_form="file:h5msm", output_filename=filename)

    assert msm.get(
        filename, element="atom", chemical_state=1, formal_charge=True
    ) == [1, -1]


def test_public_convert_writes_a_state_only_05_file(tmp_path):
    states = ChemicalStates(n_atoms=2)
    filename = tmp_path / "states_only.h5msm"

    msm.convert(states, to_form="file:h5msm", output_filename=filename)
    with h5py.File(filename, "r") as file:
        assert file.attrs["version"] == "0.5"
        assert set(file) == {"chemical_states"}
    restored = msm.convert(filename, to_form="molsysmt.ChemicalStates")
    assert restored.n_atoms == 2


def test_public_convert_preserves_attached_interactions(tmp_path):
    source = MolSys(n_atoms=2)
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    source.interactions = {
        "candidate": msm.Interactions.from_records(
            [], n_atoms=2, n_structures=1,
            evaluated_structure_indices=[0], method="candidate",
        )
    }
    filename = tmp_path / "with_interactions.h5msm"

    msm.convert(source, to_form="file:h5msm", output_filename=filename)
    restored = msm.convert(filename)
    assert restored.interactions["candidate"].n_interactions == 0
    assert restored.interactions["candidate"].evaluated_structure_indices.tolist() == [0]


def test_public_05_layers_support_interaction_only_payload(tmp_path):
    interactions = msm.Interactions.from_records(
        [], n_atoms=3, n_structures=2,
        evaluated_structure_indices=[0, 1], method="candidate",
    )
    filename = str(tmp_path / "interaction_only.h5msm")
    msm.h5msm.write_layers(filename, interactions={"candidate": interactions})
    payload = msm.h5msm.read_layers(filename, layers="interactions")
    assert payload["interactions"]["candidate"].n_interactions == 0
    assert payload["interactions"]["candidate"].n_structures == 2
    for restored in (msm.h5msm.read(filename),
                     msm.convert(filename, to_form="molsysmt.MolSys")):
        assert restored.topology is None
        assert restored.chemical_states is None
        assert restored.structures is None
        assert restored.get_n_atoms() == 3
        assert msm.get(restored, n_structures=True) == 2
        selected = restored.extract(atom_indices=[2, 0], structure_indices=[1, 0, 1])
        assert selected.get_n_atoms() == 2
        assert selected.interactions["candidate"].n_structures == 3
        assert selected.interactions["candidate"].evaluated_structure_indices.tolist() == [0, 1, 2]
        roundtrip = tmp_path / "interaction_only_molsys.h5msm"
        if not roundtrip.exists():
            msm.h5msm.write(restored, str(roundtrip))
        assert msm.h5msm.read(str(roundtrip)).interactions["candidate"].n_atoms == 3

    empty_filename = str(tmp_path / "present_empty_interactions.h5msm")
    msm.h5msm.write_layers(empty_filename, interactions={})
    assert msm.h5msm.read_layers(
        empty_filename, layers="interactions"
    )["interactions"] == {}
    with pytest.raises(ValueError, match="read_layers"):
        msm.h5msm.read(empty_filename)


def test_interaction_only_molsys_extracts_nonconsecutive_frames_and_atoms(tmp_path):
    analysis = msm.Interactions.from_records(
        [{
            "structure_index": 3,
            "interaction_type": "hbond",
            "participants": [
                {"role": "donor", "atom_indices": [0]},
                {"role": "hydrogen", "atom_indices": [1]},
                {"role": "acceptor", "atom_indices": [2]},
            ],
        }],
        n_atoms=3, n_structures=5,
        evaluated_structure_indices=[0, 3], method="candidate",
    )
    filename = str(tmp_path / "observed_interaction_only.h5msm")
    msm.h5msm.write_layers(filename, interactions={"hbonds": analysis})
    restored = msm.h5msm.read(filename)
    selected = restored.extract(atom_indices=[2, 0, 1], structure_indices=[3, 0, 3])
    result = selected.interactions["hbonds"]
    assert result.n_atoms == 3
    assert result.n_structures == 3
    assert result.query(structure_indices=[0, 2]).n_interactions == 2
    assert result.query(structure_indices=[1]).n_interactions == 0
    np.testing.assert_array_equal(result.atom_source_indices, [2, 0, 1])
    np.testing.assert_array_equal(result.structure_source_indices, [3, 0, 3])
    through_api = msm.extract(restored, selection=[2, 0, 1], structure_indices=[3, 0])
    assert through_api.interactions["hbonds"].query(
        structure_indices=[0]
    ).n_interactions == 1
    for clone in (restored.copy(), pickle.loads(pickle.dumps(restored))):
        assert clone.topology is None
        assert clone.structures is None
        assert clone.interactions["hbonds"].n_interactions == 1


def test_interaction_only_identity_links_are_representable(tmp_path):
    analysis = msm.Interactions.from_records(
        [], n_atoms=2, n_structures=3,
        evaluated_structure_indices=[0, 2], method="candidate",
    )
    links = [
        {
            "axis": axis, "source": "interactions", "target": "interactions",
            "source_name": "first", "target_name": "second", "indices": "identity",
        }
        for axis in ("atom", "structure")
    ]
    filename = str(tmp_path / "linked_interactions.h5msm")
    msm.h5msm.write_layers(
        filename, interactions={"first": analysis, "second": analysis},
        associations=links,
    )
    restored = msm.h5msm.read(filename)
    assert set(restored.interactions) == {"first", "second"}
    assert restored.get_n_atoms() == 2
    assert msm.get(restored, n_structures=True) == 3


def test_public_04_to_05_migration_keeps_source_unchanged(tmp_path):
    source = MolSys(n_atoms=2)
    source.structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
    )
    legacy = str(tmp_path / "old.h5msm")
    modern = str(tmp_path / "new.h5msm")
    from molsysmt.form.molsysmt_MolSys.to_file_h5msm import to_file_h5msm

    to_file_h5msm(source, output_filename=legacy)
    with pytest.warns(LegacyH5MSMWarning, match="migrate_to_05"):
        assert msm.h5msm.read(legacy).get_n_atoms() == 2
    with pytest.warns(LegacyH5MSMWarning, match="migrate_to_05"):
        msm.h5msm.migrate_to_05(legacy, modern)
    with h5py.File(legacy, "r") as file:
        assert file.attrs["version"] == "0.4"
    with h5py.File(modern, "r") as file:
        assert file.attrs["version"] == "0.5"
    assert msm.h5msm.read(modern).get_n_atoms() == 2


def test_public_03_reader_warns_and_migrates_with_the_same_helper(tmp_path):
    legacy = Path(__file__).parent / "data" / "alanine_dipeptide_v03.h5msm"
    with pytest.warns(LegacyH5MSMWarning, match="migrate_to_05"):
        observed = msm.h5msm.read(str(legacy))
    assert observed.get_n_atoms() == 22

    modern = str(tmp_path / "migrated03.h5msm")
    with pytest.warns(LegacyH5MSMWarning, match="migrate_to_05"):
        msm.h5msm.migrate_to_05(str(legacy), modern)
    with h5py.File(modern, "r") as file:
        assert file.attrs["migrated_from_version"] == "0.3"
    assert msm.h5msm.read(modern).get_n_atoms() == 22


def test_public_layer_writer_rejects_unencoded_fields_before_creating_file(tmp_path):
    filename = str(tmp_path / "unsupported.h5msm")
    structures = Structures(
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 1, 3)), "nm"),
        alternate_location=[{0: {
            "location_id": ["A"], "occupancy": [1.0],
            "b_factor": msm.pyunitwizard.quantity([1.0], "nm**2"),
            "atom_id": ["1"], "coordinates": [[0.0, 0.0, 0.0]],
        }}],
        skip_digestion=True,
    )
    with pytest.raises(ValueError, match="Alternate-location coordinates must carry units"):
        msm.h5msm.write_layers(filename, structures=structures)
    assert not (tmp_path / "unsupported.h5msm").exists()
