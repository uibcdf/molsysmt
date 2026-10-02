"""Probe the independent numeric structures layer proposed for H5MSM 0.5."""

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt.form._h5msm05_modular import (
    append_modular_structures,
    read_modular_file,
    read_topology_free_molsys_file,
    write_modular_file,
)
from molsysmt.form._h5msm05_structures import (
    append_independent_structures,
    read_independent_structures,
    write_independent_structures,
)
from molsysmt.native import Structures, Topology


def test_structures_only_roundtrip_and_nonconsecutive_selection(tmp_path):
    source = Structures(
        constant_time_step=True,
        time_step=msm.pyunitwizard.quantity(1.0, "ps"),
        structure_id=[10, 11, 12],
        time=msm.pyunitwizard.quantity([0.0, 1.0, 2.0], "ps"),
        coordinates=msm.pyunitwizard.quantity(
            np.arange(36).reshape(3, 4, 3), "angstrom"
        ),
        velocities=msm.pyunitwizard.quantity(np.ones((3, 4, 3)), "nm/ps"),
        box=msm.pyunitwizard.quantity(np.ones((3, 3, 3)), "nm"),
        b_factor=msm.pyunitwizard.quantity(np.ones((3, 4)), "nm**2"),
        occupancy=np.full((3, 4), 0.75),
        temperature=msm.pyunitwizard.quantity([290.0, 300.0, 310.0], "K"),
        potential_energy=msm.pyunitwizard.quantity([-1.0, -2.0, -3.0], "kJ/mol"),
        kinetic_energy=msm.pyunitwizard.quantity([0.1, 0.2, 0.3], "kJ/mol"),
        skip_digestion=True,
    )
    filename = tmp_path / "structures_only.h5msm"
    with h5py.File(filename, "w") as file:
        file.attrs["type"] = "h5msm"
        file.attrs["version"] = "0.5"
        write_independent_structures(file, source, block_size=1)
        assert set(file) == {"structures"}
        assert file["structures"].attrs["n_atoms"] == 4

    with h5py.File(filename, "r") as file:
        observed = read_independent_structures(
            file, structure_indices=[2, 0, 2], atom_indices=[3, 1]
        )
    assert observed.n_structures == 3
    assert observed.n_atoms == 2
    assert observed.structure_id.tolist() == [12, 10, 12]
    assert observed.constant_time_step is False
    assert observed.time_step is None
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed.coordinates, to_unit="nm"),
        msm.pyunitwizard.get_value(source.coordinates, to_unit="nm")[[2, 0, 2]][
            :, [3, 1]
        ],
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed.temperature, to_unit="K"),
        [310.0, 290.0, 310.0],
    )
    assert observed.velocities.shape == (3, 2, 3)
    assert observed.b_factor.shape == (3, 2)
    np.testing.assert_allclose(observed.occupancy, 0.75)
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed.potential_energy), [-3.0, -1.0, -3.0]
    )
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(observed.kinetic_energy), [0.3, 0.1, 0.3]
    )


def test_time_only_layer_has_unknown_atom_domain(tmp_path):
    filename = tmp_path / "time_only.h5msm"
    source = Structures(time=msm.pyunitwizard.quantity([0.0, 2.0], "ps"))
    with h5py.File(filename, "w") as file:
        write_independent_structures(file, source)
        assert file["structures"].attrs["n_atoms"] == -1
        observed = read_independent_structures(file)
        with pytest.raises(ValueError, match="unknown atom domain"):
            read_independent_structures(file, atom_indices=[0])
    assert observed.n_structures == 2
    assert observed.coordinates is None
    np.testing.assert_allclose(msm.pyunitwizard.get_value(observed.time), [0.0, 2.0])


def test_alternate_locations_roundtrip_sparse_sites_and_selected_axes(tmp_path):
    puw = msm.pyunitwizard
    source = Structures(
        coordinates=puw.quantity(np.zeros((3, 3, 3)), "nm"),
        alternate_location=[
            {
                2: {
                    "location_id": np.array(["A", "B"]),
                    "atom_id": np.array(["7", "8"], dtype=object),
                    "occupancy": np.array([0.6, 0.4]),
                    "b_factor": puw.quantity([10.0, 20.0], "angstrom**2"),
                    "coordinates": puw.quantity(
                        [[1.0, 2.0, 3.0], [4.0, 5.0, 6.0]], "angstrom"
                    ),
                }
            },
            {},
            {
                0: {
                    "location_id": ["C"],
                    "atom_id": [9],
                    "occupancy": None,
                    "b_factor": None,
                    "coordinates": None,
                }
            },
        ],
        skip_digestion=True,
    )
    filename = tmp_path / "alternates.h5msm"
    write_modular_file(filename, structures=source)

    with h5py.File(filename, "r") as file:
        group = file["structures/alternate_location"]
        np.testing.assert_array_equal(group["frame_offsets"][:], [0, 1, 1, 2])
        np.testing.assert_array_equal(group["site_offsets"][:], [0, 2, 3])
        assert group["coordinates"].shape == (3, 3)
        assert group["coordinates"].attrs["unit"] == "nm"
        assert group["b_factor"].attrs["unit"] == "nm**2"
        selected = read_independent_structures(
            file, structure_indices=[2, 0, 2], atom_indices=[2, 0]
        )
    assert [list(frame) for frame in selected.alternate_location] == [[1], [0], [1]]
    assert selected.alternate_location[0][1]["atom_id"].tolist() == [9]
    assert selected.alternate_location[0][1]["occupancy"] is None
    first = selected.alternate_location[1][0]
    assert first["location_id"].tolist() == ["A", "B"]
    assert first["atom_id"].tolist() == ["7", "8"]
    np.testing.assert_allclose(first["occupancy"], [0.6, 0.4])
    np.testing.assert_allclose(
        puw.get_value(first["coordinates"], to_unit="nm"),
        [[0.1, 0.2, 0.3], [0.4, 0.5, 0.6]],
    )
    np.testing.assert_allclose(
        puw.get_value(first["b_factor"], to_unit="nm**2"), [0.1, 0.2]
    )

    incoming = Structures(
        coordinates=puw.quantity(np.zeros((1, 3, 3)), "nm"),
        alternate_location=[source.alternate_location[0]],
        skip_digestion=True,
    )
    msm.h5msm.append_structures(str(filename), incoming)
    observed = read_modular_file(filename, layers="structures")["structures"]
    assert observed.n_structures == 4
    assert observed.alternate_location[3][2]["location_id"].tolist() == ["A", "B"]
    with h5py.File(filename, "r") as file:
        np.testing.assert_array_equal(
            file["structures/alternate_location/frame_offsets"][:], [0, 1, 1, 2, 3]
        )
        np.testing.assert_array_equal(
            file["structures/alternate_location/site_offsets"][:], [0, 2, 3, 5]
        )
    missing_alternates = Structures(coordinates=puw.quantity(np.zeros((1, 3, 3)), "nm"))
    with pytest.raises(ValueError, match="matching alternate_location presence"):
        msm.h5msm.append_structures(str(filename), missing_alternates)
    assert (
        read_modular_file(filename, layers="structures")["structures"].n_structures == 4
    )
    with h5py.File(filename, "r+") as file:
        file["structures/alternate_location/coordinates"].attrs["unit"] = "angstrom"
    with pytest.raises(ValueError, match="unsupported unit"):
        read_modular_file(filename, layers="structures")
    with pytest.raises(ValueError, match="unsupported unit"):
        msm.h5msm.append_structures(str(filename), incoming)
    with h5py.File(filename, "r") as file:
        assert file["structures"].attrs["n_structures"] == 4
        assert file["structures/coordinates"].shape[0] == 4


def test_empty_alternate_locations_remain_present_and_bad_offsets_fail(tmp_path):
    puw = msm.pyunitwizard
    source = Structures(
        coordinates=puw.quantity(np.zeros((2, 1, 3)), "nm"),
        alternate_location=[{}, {}],
        skip_digestion=True,
    )
    filename = tmp_path / "empty_alternates.h5msm"
    write_modular_file(filename, structures=source)
    observed = read_modular_file(filename, layers="structures")["structures"]
    assert observed.alternate_location == [{}, {}]
    with h5py.File(filename, "r+") as file:
        file["structures/alternate_location/frame_offsets"][1] = 1
    with pytest.raises(ValueError, match="offsets are inconsistent"):
        read_modular_file(filename, layers="structures")


def test_bioassembly_roundtrip_preserves_chain_scopes_and_translation_units(tmp_path):
    puw = msm.pyunitwizard
    source = Structures(
        coordinates=puw.quantity(np.zeros((1, 3, 3)), "nm"),
        bioassembly={
            "common": {
                "chain_indices": [0, 2],
                "rotations": [np.eye(3), np.eye(3)],
                "translations": [
                    puw.quantity([10.0, 0.0, 0.0], "angstrom"),
                    puw.quantity([0.0, 20.0, 0.0], "angstrom"),
                ],
            },
            "per_operation": {
                "chain_indices": [[0], [1, 2]],
                "rotations": np.stack([np.eye(3), -np.eye(3)]),
                "translations": puw.quantity([[0.0, 0.0, 0.0], [1.0, 2.0, 3.0]], "nm"),
            },
        },
        skip_digestion=True,
    )
    filename = tmp_path / "assemblies.h5msm"
    write_modular_file(filename, structures=source)

    with h5py.File(filename, "r") as file:
        collection = file["structures/bioassembly"]
        assert collection.attrs["schema_version"] == 1
        assert all(
            child["translations"].attrs["unit"] == "nm" for child in collection.values()
        )
    observed = read_modular_file(filename, layers="structures")[
        "structures"
    ].bioassembly
    assert observed["common"]["chain_indices"] == [0, 2]
    assert observed["per_operation"]["chain_indices"] == [[0], [1, 2]]
    np.testing.assert_allclose(
        puw.get_value(observed["common"]["translations"], to_unit="nm"),
        [[1.0, 0.0, 0.0], [0.0, 2.0, 0.0]],
    )
    np.testing.assert_allclose(observed["per_operation"]["rotations"][1], -np.eye(3))

    appended = Structures(
        coordinates=puw.quantity(np.ones((1, 3, 3)), "nm"),
        bioassembly=source.bioassembly,
        skip_digestion=True,
    )
    append_modular_structures(filename, appended)
    assert (
        read_modular_file(filename, layers="structures")["structures"].n_structures == 2
    )
    with h5py.File(filename, "r") as file:
        with pytest.raises(ValueError, match="cannot remap bioassembly chain indices"):
            read_independent_structures(file, atom_indices=[1, 0])

    incompatible = Structures(
        coordinates=puw.quantity(np.ones((1, 3, 3)), "nm"),
        bioassembly={"different": source.bioassembly["common"]},
        skip_digestion=True,
    )
    with pytest.raises(ValueError, match="bioassembly metadata differ"):
        append_modular_structures(filename, incompatible)
    assert (
        read_modular_file(filename, layers="structures")["structures"].n_structures == 2
    )

    subset_filename = tmp_path / "assembly_subset.h5msm"
    with pytest.raises(
        ValueError, match="cannot write an atom selection with bioassembly"
    ):
        msm.convert(
            source,
            to_form="file:h5msm",
            selection=[0, 1],
            output_filename=str(subset_filename),
        )
    assert not subset_filename.exists()

    with h5py.File(filename, "r+") as file:
        file["structures/bioassembly/0/translations"].attrs["unit"] = "angstrom"
    with pytest.raises(ValueError, match="Bioassembly operation data"):
        read_modular_file(filename, layers="structures")


def test_absent_empty_and_unsupported_structures_are_explicit(tmp_path):
    filename = tmp_path / "empty.h5msm"
    with h5py.File(filename, "w") as file:
        assert read_independent_structures(file) is None
        with pytest.raises(
            ValueError, match="Alternate locations require a known atom axis"
        ):
            write_independent_structures(
                file, Structures(alternate_location=[{0: {}}], skip_digestion=True)
            )
        assert "structures" not in file
        with pytest.raises(ValueError, match="structure_id.*cannot be stored"):
            write_independent_structures(
                file, Structures(structure_id=[1.5], skip_digestion=True)
            )
        assert "structures" not in file
        write_independent_structures(file, Structures())
        assert read_independent_structures(file).n_structures == 0
        with pytest.raises(ValueError, match="already exists"):
            write_independent_structures(file, Structures())


def test_invalid_stored_axis_is_rejected(tmp_path):
    filename = tmp_path / "bad_axis.h5msm"
    with h5py.File(filename, "w") as file:
        write_independent_structures(
            file, Structures(time=msm.pyunitwizard.quantity([0.0, 1.0], "ps"))
        )
        file["structures"].attrs["n_structures"] = 3
        with pytest.raises(ValueError, match="invalid shape"):
            read_independent_structures(file)


def _trajectory_part(ids, times, n_atoms=2):
    count = len(ids)
    return Structures(
        structure_id=np.asarray(ids, dtype=np.int64),
        time=msm.pyunitwizard.quantity(times, "ps"),
        coordinates=msm.pyunitwizard.quantity(
            np.arange(count * n_atoms * 3).reshape(count, n_atoms, 3), "nm"
        ),
        box=msm.pyunitwizard.quantity(np.tile(np.eye(3), (count, 1, 1)), "nm"),
        constant_time_step=True,
        time_step=msm.pyunitwizard.quantity(1.0, "ps"),
        constant_id_step=True,
        id_step=1,
        constant_box=True,
        skip_digestion=True,
    )


def test_structures_only_append_preserves_axes_and_metadata(tmp_path):
    filename = tmp_path / "append.h5msm"
    write_modular_file(filename, structures=_trajectory_part([10, 11], [0.0, 1.0]))
    append_modular_structures(
        filename, _trajectory_part([12, 13, 14], [2.0, 3.0, 4.0]), block_size=1
    )

    full = read_modular_file(filename, layers="structures")["structures"]
    assert full.n_structures == 5
    assert full.structure_id.tolist() == [10, 11, 12, 13, 14]
    assert full.constant_time_step and full.constant_id_step and full.constant_box
    assert msm.pyunitwizard.get_value(full.time_step, to_unit="ps") == 1.0
    assert full.id_step == 1
    with h5py.File(filename, "r") as file:
        assert set(file) == {"structures"}
        assert file["structures/coordinates"].maxshape == (None, 2, 3)
        selected = read_independent_structures(
            file, structure_indices=[4, 0, 4], atom_indices=[1]
        )
    assert selected.structure_id.tolist() == [14, 10, 14]
    assert selected.coordinates.shape == (3, 1, 3)


def test_string_structure_ids_roundtrip_and_append_without_numeric_step(tmp_path):
    puw = msm.pyunitwizard
    filename = tmp_path / "string_ids.h5msm"
    first = Structures(
        structure_id=np.asarray(["model-a"]),
        coordinates=puw.quantity(np.zeros((1, 2, 3)), "nm"),
        skip_digestion=True,
    )
    second = Structures(
        structure_id=np.asarray(["model-b"], dtype=object),
        coordinates=puw.quantity(np.ones((1, 2, 3)), "nm"),
        skip_digestion=True,
    )
    write_modular_file(filename, structures=first)
    append_modular_structures(filename, second)

    with h5py.File(filename, "r") as file:
        assert file["structures/structure_id"].attrs["value_kind"] == "string"
    observed = read_modular_file(filename, layers="structures")["structures"]
    assert observed.structure_id.tolist() == ["model-a", "model-b"]
    assert observed.constant_id_step is False


def test_append_rejects_incompatible_payload_before_resizing(tmp_path):
    filename = tmp_path / "append_reject.h5msm"
    write_modular_file(filename, structures=_trajectory_part([10, 11], [0.0, 1.0]))
    missing_box = Structures(
        structure_id=[12],
        time=msm.pyunitwizard.quantity([2.0], "ps"),
        coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm"),
        skip_digestion=True,
    )
    for invalid, pattern in (
        (_trajectory_part([12], [2.0], n_atoms=3), "incompatible atom axis"),
        (missing_box, "same series"),
    ):
        with pytest.raises(ValueError, match=pattern):
            append_modular_structures(filename, invalid)
    with h5py.File(filename, "r+") as file:
        file["structures/box"].attrs["unit"] = "angstrom"
        with pytest.raises(ValueError, match="cannot be appended"):
            append_independent_structures(file, _trajectory_part([12], [2.0]))
        assert file["structures"].attrs["n_structures"] == 2
        assert all(item.shape[0] == 2 for item in file["structures"].values())


def test_append_clears_discontinuous_metadata_and_rejects_other_layers(tmp_path):
    filename = tmp_path / "append_discontinuous.h5msm"
    write_modular_file(filename, structures=_trajectory_part([10, 11], [0.0, 1.0]))
    append_modular_structures(filename, _trajectory_part([20], [9.0]))
    with h5py.File(filename, "r") as file:
        group = file["structures"]
        assert not group.attrs["constant_time_step"]
        assert not group.attrs["constant_id_step"]
        assert "time_step_ps" not in group.attrs
        assert "id_step" not in group.attrs

    other = tmp_path / "not_structures_only.h5msm"
    write_modular_file(
        other,
        topology=Topology(n_atoms=2),
        structures=_trajectory_part([10], [0.0]),
    )
    with pytest.raises(ValueError, match="topology-free"):
        append_modular_structures(other, _trajectory_part([11], [1.0]))


def test_append_to_zero_frame_and_unknown_atom_axis(tmp_path):
    filename = tmp_path / "empty_coordinates.h5msm"
    write_modular_file(filename, structures=_trajectory_part([], []))
    append_modular_structures(filename, _trajectory_part([7], [0.0]))
    observed = read_modular_file(filename, layers="structures")["structures"]
    assert observed.structure_id.tolist() == [7]
    assert observed.coordinates.shape == (1, 2, 3)

    time_only = tmp_path / "time_only_append.h5msm"
    write_modular_file(
        time_only,
        structures=Structures(time=msm.pyunitwizard.quantity([0.0], "ps")),
    )
    append_modular_structures(
        time_only,
        Structures(time=msm.pyunitwizard.quantity([2.0, 4.0], "ps")),
    )
    result = read_modular_file(time_only, layers="structures")["structures"]
    assert result.n_structures == 3
    assert result.coordinates is None
    with h5py.File(time_only, "r") as file:
        assert file["structures"].attrs["n_atoms"] == -1


def test_topology_free_append_keeps_atom_link_and_extends_state_map(tmp_path):
    states = msm.convert(Topology(n_atoms=2), to_form="molsysmt.ChemicalStates")
    atom_link = {
        "axis": "atom",
        "source": "structures",
        "target": "chemical_states",
        "source_name": None,
        "target_name": None,
        "indices": "identity",
    }
    filename = tmp_path / "chemistry_and_structures.h5msm"
    write_modular_file(
        filename,
        chemical_states=states,
        structures=_trajectory_part([10, 11], [0.0, 1.0]),
        associations=[atom_link],
    )
    append_modular_structures(filename, _trajectory_part([12], [2.0]))
    payload = read_modular_file(filename)
    assert payload["structures"].structure_id.tolist() == [10, 11, 12]
    assert payload["chemical_states"].n_atoms == 2
    assert payload["associations"][0]["indices"] == "identity"

    linked = tmp_path / "frame_linked.h5msm"
    write_modular_file(
        linked,
        chemical_states=states,
        structures=_trajectory_part([10, 11], [0.0, 1.0]),
        associations=[
            atom_link,
            {
                "axis": "structure_state",
                "source": "structures",
                "target": "chemical_states",
                "source_name": None,
                "target_name": None,
                "indices": [0, 0],
            },
        ],
    )
    with pytest.raises(ValueError, match="structure_state_indices are required"):
        append_modular_structures(linked, _trajectory_part([12], [2.0]))
    with pytest.raises(ValueError, match="outside the state axis"):
        append_modular_structures(
            linked, _trajectory_part([12], [2.0]), structure_state_indices=[1]
        )
    with h5py.File(linked, "r") as file:
        assert file["structures"].attrs["n_structures"] == 2
        assert file["associations/1/indices"].shape == (2,)
    append_modular_structures(
        linked,
        _trajectory_part([12, 13], [2.0, 3.0]),
        structure_state_indices=[-1, 0],
    )
    mapped = read_modular_file(linked)
    assert mapped["structures"].structure_id.tolist() == [10, 11, 12, 13]
    np.testing.assert_array_equal(mapped["associations"][1]["indices"], [0, 0, -1, 0])
    native = read_topology_free_molsys_file(linked)
    assert native._structure_chemical_state_indices.tolist()[:2] == [0, 0]
    assert native._structure_chemical_state_indices.isna().tolist() == [
        False,
        False,
        True,
        False,
    ]
    assert native._structure_chemical_state_indices[3] == 0


def test_append_converts_identity_state_map_when_new_frame_reuses_a_state(tmp_path):
    states = msm.ChemicalStates(n_atoms=2)
    states.append_state()
    states.append_state()
    filename = tmp_path / "identity_state_map.h5msm"
    link = {
        "axis": "structure_state",
        "source": "structures",
        "target": "chemical_states",
        "source_name": None,
        "target_name": None,
        "indices": "identity",
    }
    write_modular_file(
        filename,
        chemical_states=states,
        structures=_trajectory_part([10, 11], [0.0, 1.0]),
        associations=[link],
    )
    append_modular_structures(
        filename, _trajectory_part([12], [2.0]), structure_state_indices=[1]
    )
    with h5py.File(filename, "r") as file:
        assert file["associations/0"].attrs["mapping"] == "explicit"
        assert file["associations/0/indices"].maxshape == (None,)
    append_modular_structures(
        filename, _trajectory_part([13], [3.0]), structure_state_indices=[-1]
    )
    mapping = read_modular_file(filename, layers="associations")["associations"]
    np.testing.assert_array_equal(mapping[0]["indices"], [0, 1, 1, -1])
