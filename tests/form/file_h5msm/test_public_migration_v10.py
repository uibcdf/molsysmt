"""Verify the complete-file 1.0 migration through public conversion."""

import json

import h5py
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt.native import ChemicalStates, MolecularMechanics, Structures
from tests.form.file_h5msm.test_public_mechanics_v06 import _mechanical


@pytest.mark.parametrize("source_version", ["0.5", "0.6"])
def test_migrate_independent_layers_without_composing_a_molsys(
    tmp_path, source_version
):
    source = tmp_path / "source.h5msm"
    target = tmp_path / "target.h5msm"
    coordinates = np.arange(18, dtype=float).reshape(3, 2, 3)
    states = ChemicalStates(n_atoms=2)
    states.append_state()
    states.append_state()
    links = [
        dict(
            axis="atom",
            source="structures",
            target="chemical_states",
            source_name=None,
            target_name=None,
            indices="identity",
        ),
        dict(
            axis="structure_state",
            source="structures",
            target="chemical_states",
            source_name=None,
            target_name=None,
            indices=[1, -1, 0],
        ),
    ]
    options = {}
    if source_version == "0.6":
        # This layer intentionally has no declared correspondence to the other atom axes.
        options = dict(molecular_mechanics=MolecularMechanics(), mechanics_n_atoms=7)
    msm.h5msm.write_layers(
        source,
        structures=Structures(coordinates=msm.pyunitwizard.quantity(coordinates, "nm")),
        chemical_states=states,
        interactions={},
        associations=links,
        format_version=source_version,
        **options,
    )
    with h5py.File(source, "r") as file:
        original_metadata = dict(file.attrs)
    original = source.read_bytes()

    assert msm.convert(source, to_form=target, format_version="1.0") == target
    assert source.read_bytes() == original
    with h5py.File(target, "r") as file:
        assert file.attrs["version"] == "1.0"
        assert json.loads(file.attrs["migration_source"]) == original_metadata
    restored = msm.h5msm.read_layers(target)
    assert restored["topology"] is None
    assert restored["interactions"] == {}
    assert restored["chemical_states"].n_chemical_states == states.n_chemical_states
    np.testing.assert_array_equal(
        msm.pyunitwizard.get_value(restored["structures"].coordinates, to_unit="nm"),
        coordinates,
    )
    assert restored["associations"][0]["indices"] == "identity"
    np.testing.assert_array_equal(restored["associations"][1]["indices"], [1, -1, 0])
    assert (restored["molecular_mechanics"] is not None) == (source_version == "0.6")
    assert msm.h5msm.read_axis_sizes(target) == msm.h5msm.read_axis_sizes(source)

    destination = target.read_bytes()
    with pytest.raises(FileExistsError):
        msm.convert(source, to_form=target, format_version="1.0")
    assert source.read_bytes() == original
    assert target.read_bytes() == destination


def test_migration_rejects_unknown_root_metadata_before_creating_output(tmp_path):
    source = tmp_path / "source.h5msm"
    target = tmp_path / "target.h5msm"
    msm.h5msm.write_layers(source, interactions={}, format_version="0.5")
    with h5py.File(source, "r+") as file:
        file.attrs["unrepresented"] = "retain me"
    original = source.read_bytes()
    with pytest.raises(ValueError, match="Unsupported H5MSM migration source metadata"):
        msm.convert(source, to_form=target, format_version="1.0")
    assert source.read_bytes() == original
    assert not target.exists()


def test_migrate_named_observations_and_typed_mechanics(tmp_path):
    molsys = _mechanical()
    molsys.molecular_mechanics.atoms_ff["partial_charge"] = pd.array(
        [0.25, None], dtype="Float32"
    )
    molsys.interactions = {
        "pair": msm.Interactions.from_records(
            [
                {
                    "structure_index": 0,
                    "interaction_type": "synthetic",
                    "participants": [
                        {"role": "first", "atom_indices": [0]},
                        {"role": "second", "atom_indices": [1]},
                    ],
                    "measurements": {"distance": 1.5},
                }
            ],
            n_atoms=2,
            n_structures=1,
            evaluated_structure_indices=[0],
            method="migration_guard",
            measure_units={"distance": "angstrom"},
            software={"original": "1"},
        )
    }
    source = tmp_path / "stored_06.h5msm"
    target = tmp_path / "stored_10.h5msm"
    msm.h5msm.write(molsys, source, format_version="0.6")
    msm.convert(
        source, to_form="file:h5msm", output_filename=target, format_version="1.0"
    )
    original, restored = (msm.h5msm.read(path) for path in (source, target))
    before, after = original.molecular_mechanics, restored.molecular_mechanics
    pd.testing.assert_frame_equal(after.atoms_ff, before.atoms_ff)
    assert after.partial_charge_assignment == before.partial_charge_assignment
    observation = restored.interactions["pair"]
    assert observation.software == {"original": "1"}
    assert observation.measure_units == {"distance": "angstrom"}
    occurrences = observation.query(structure_indices=[0]).to_dict()
    np.testing.assert_array_equal(occurrences["occurrence_indices"], [0])
    np.testing.assert_array_equal(observation.evaluated_structure_indices, [0])
    np.testing.assert_array_equal(observation.measurements["distance"], [1.5])


@pytest.mark.parametrize(
    "metadata",
    [
        '{"type": "h5msm", "version": "9.0"}',
        '{"type": "h5msm", "version": "9.0", "version": "0.5"}',
    ],
)
def test_v1_reader_rejects_invalid_migration_metadata(tmp_path, metadata):
    path = tmp_path / "invalid.h5msm"
    msm.h5msm.write_layers(path, interactions={}, format_version="1.0")
    with h5py.File(path, "r+") as file:
        file.attrs["migration_source"] = metadata
    with pytest.raises(ValueError, match="Invalid H5MSM migration source metadata"):
        msm.h5msm.read_layers(path)
