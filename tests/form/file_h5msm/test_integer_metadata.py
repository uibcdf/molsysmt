"""Reject coerced cardinalities before decoding, iterating or publishing a file."""

import importlib
import json

import h5py
import numpy as np
import pytest

import molsysmt as msm
from molsysmt._private.smonitor import StructuralInconsistencyError
from molsysmt.native import ChemicalStates, Structures
from tests.native.test_molsys import build_minimal_molsys


@pytest.fixture
def structural_header_file(tmp_path):
    def make(version):
        path = tmp_path / "input.h5msm"
        msm.h5msm.write_layers(
            path,
            structures=Structures(
                coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
            ),
            format_version=version,
        )
        return path

    return make


@pytest.mark.parametrize("version", ["0.5", "0.6", "1.0"])
@pytest.mark.parametrize(
    "attribute,value",
    [
        ("n_atoms", 2.5),
        ("n_structures", 1.5),
        ("n_structures", True),
        ("n_atoms", "2"),
        ("schema_version", True),
        ("schema_version", 1.0),
        ("schema_version", np.array([1], dtype=np.int64)),
    ],
)
@pytest.mark.parametrize(
    "route", ["read_layers", "read_axis_sizes", "read", "convert", "iterator", "append"]
)
def test_public_routes_reject_noninteger_structural_metadata(
    tmp_path, structural_header_file, version, attribute, value, route
):
    path = structural_header_file(version)
    with h5py.File(path, "r+") as file:
        del file["structures"].attrs[attribute]
        file["structures"].attrs[attribute] = value
    original = path.read_bytes()
    destination = tmp_path / "output.h5msm"
    with pytest.raises(ValueError):
        if route == "convert":
            msm.convert(path, to_form=destination)
        elif route == "iterator":
            with msm.Iterator(path, coordinates=True) as iterator:
                next(iterator)
        elif route == "append":
            msm.h5msm.append_structures(
                path,
                Structures(
                    coordinates=msm.pyunitwizard.quantity(np.zeros((1, 2, 3)), "nm")
                ),
            )
        else:
            getattr(msm.h5msm, route)(path)
    assert path.read_bytes() == original
    assert not destination.exists()


@pytest.fixture
def layered_file(tmp_path):
    source = build_minimal_molsys()
    source.structures.bioassembly = {
        "1": {
            "chain_indices": [0],
            "rotations": np.eye(3)[None],
            "translations": msm.pyunitwizard.quantity([[0.0, 0.0, 0.0]], "nm"),
        }
    }
    source.interactions = {
        "empty": msm.Interactions.from_records(
            [],
            n_atoms=4,
            n_structures=2,
            evaluated_structure_indices=[0],
            method="metadata_guard",
        )
    }
    path = tmp_path / "layered.h5msm"
    msm.h5msm.write(source, path)
    return path


@pytest.mark.parametrize(
    "group,attribute",
    [
        ("topology", "schema_version"),
        ("topology/atoms", "n_rows"),
        ("chemical_states", "schema_version"),
        ("chemical_states", "n_atoms"),
        ("chemical_states", "n_chemical_states"),
        ("chemical_states", "reference_chemical_state_index"),
        ("chemical_states/0", "provenance_index"),
        ("associations", "schema_version"),
        ("associations", "n_links"),
        ("structures/bioassembly", "schema_version"),
        ("structures/bioassembly", "n_assemblies"),
        ("interactions", "schema_version"),
        ("interactions", "n_analyses"),
        ("interactions/0", "schema_version"),
    ],
)
@pytest.mark.parametrize("value", [True, 1.0, "1"])
def test_layer_readers_refuse_coerced_header_values(
    layered_file, group, attribute, value
):
    with h5py.File(layered_file, "r+") as file:
        del file[group].attrs[attribute]
        file[group].attrs[attribute] = value
    original = layered_file.read_bytes()
    with pytest.raises((ValueError, StructuralInconsistencyError)):
        msm.h5msm.read_layers(layered_file)
    assert layered_file.read_bytes() == original


@pytest.mark.parametrize("dtype", [np.int8, np.int32, np.uint64])
def test_valid_integer_widths_keep_coordinates_coverage_and_units(layered_file, dtype):
    with h5py.File(layered_file, "r+") as file:
        for group in (
            "topology",
            "topology/atoms",
            "chemical_states",
            "structures",
            "associations",
            "interactions",
            "interactions/0",
            "structures/bioassembly",
        ):
            for name in (
                "schema_version",
                "n_rows",
                "n_atoms",
                "n_structures",
                "n_chemical_states",
                "n_links",
                "n_analyses",
                "n_assemblies",
            ):
                if name in file[group].attrs:
                    value = dtype(file[group].attrs[name])
                    del file[group].attrs[name]
                    file[group].attrs[name] = value
    with msm.pyunitwizard.context(standard_units=["pm", "fs", "kcal/mol", "K"]):
        restored = msm.h5msm.read(layered_file)
        coordinates = msm.pyunitwizard.get_value(
            restored.structures.coordinates, to_unit="nm"
        )
        np.testing.assert_array_equal(coordinates, np.arange(24).reshape(2, 4, 3))
        assert restored.topology.n_atoms == 4
        assert restored.chemical_states.n_chemical_states == 1
        np.testing.assert_array_equal(
            restored.interactions["empty"].query().evaluated_structure_indices, [0]
        )
    assert (
        msm.h5msm.read_axis_sizes(layered_file)[("structures", None, "structure")] == 2
    )


@pytest.mark.parametrize("value", [True, 4.0, "4", [4], -1, 2**64])
@pytest.mark.parametrize(
    "axis", ["n_atoms", "n_structures", "source_n_atoms", "source_n_structures"]
)
def test_interaction_axis_metadata_is_checked_before_loading_or_querying(
    tmp_path, axis, value
):
    from molsysmt.interactions._hdf5_query import HDF5InteractionsReader

    result = msm.Interactions.from_records(
        [],
        n_atoms=4,
        n_structures=2,
        evaluated_structure_indices=[0],
        method="metadata_guard",
    )
    standalone = tmp_path / "interactions.h5"
    result.save(standalone)
    modular = tmp_path / "analyses.h5msm"
    msm.h5msm.write_layers(modular, interactions={"empty": result})
    for path, group in ((standalone, "/"), (modular, "interactions/0")):
        with h5py.File(path, "r+") as file:
            metadata = json.loads(file[group].attrs["metadata"])
            metadata[axis] = value
            file[group].attrs["metadata"] = json.dumps(metadata)
    original = modular.read_bytes()
    with pytest.raises(ValueError):
        msm.Interactions.load(standalone)
    with pytest.raises(ValueError):
        msm.h5msm.read_layers(modular)
    with pytest.raises(ValueError):
        msm.h5msm.read_axis_sizes(modular)
    with pytest.raises(ValueError):
        with HDF5InteractionsReader(modular, "empty"):
            pytest.fail("Malformed axes must fail before a reader can be used.")
    assert modular.read_bytes() == original


@pytest.mark.parametrize("value", [True, 1.0, np.array([1], dtype=np.int64)])
def test_lazy_interaction_query_requires_integral_index_schema(layered_file, value):
    from molsysmt.interactions._hdf5_query import HDF5InteractionsReader

    with h5py.File(layered_file, "r+") as file:
        group = file["interactions/0/query_index"]
        del group.attrs["schema_version"]
        group.attrs["schema_version"] = value
    original = layered_file.read_bytes()
    with pytest.raises(ValueError):
        with HDF5InteractionsReader(layered_file, "empty"):
            pytest.fail(
                "Malformed query-index schema must fail at reader construction."
            )
    assert layered_file.read_bytes() == original


@pytest.mark.parametrize(
    "layer,attribute,module_name,options",
    [
        ("associations", "n_links", "_h5msm05_associations", {"associations": []}),
        (
            "chemical_states",
            "n_chemical_states",
            "_h5msm_chemical_states",
            {"chemical_states": ChemicalStates(n_atoms=0)},
        ),
    ],
)
def test_inconsistent_counts_refuse_before_enumerating_declared_population(
    tmp_path, monkeypatch, layer, attribute, module_name, options
):
    path = tmp_path / "empty.h5msm"
    msm.h5msm.write_layers(
        path,
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(np.zeros((1, 0, 3)), "nm")
        ),
        **options,
    )
    with h5py.File(path, "r+") as file:
        file[layer].attrs[attribute] = np.iinfo(np.int64).max
    original = path.read_bytes()
    module = importlib.import_module("molsysmt.form." + module_name)

    def reject_enumeration(*args):
        pytest.fail("A mismatched declared count must be rejected before enumeration.")

    monkeypatch.setattr(module, "range", reject_enumeration, raising=False)
    with pytest.raises((ValueError, StructuralInconsistencyError)):
        msm.h5msm.read_layers(path)
    assert path.read_bytes() == original
