"""Receive a private mechanics layer; public H5MSM writing remains version 0.5."""

import json
import os
import subprocess
import sys

import h5py
import numpy as np
import pandas as pd
import pytest

import molsysmt as msm
from molsysmt._private.h5msm_storage.mechanics import read_mechanics, write_mechanics
from molsysmt._private.h5msm_storage.metadata import (
    _prepare_tree,
    _read_tree,
    _write_tree,
)
from molsysmt.native import MolecularMechanics


def _roundtrip(tmp_path, source, n_atoms=3):
    path = tmp_path / "private_layer.h5"
    with h5py.File(path, "w") as file:
        write_mechanics(file, source, n_atoms=n_atoms)
    with h5py.File(path, "r") as file:
        return read_mechanics(file, n_atoms=n_atoms)


@pytest.mark.parametrize(
    "name,series",
    [
        ("partial_charge", pd.Series([0.125, -0.25, np.nan], dtype="float32")),
        ("partial_charge", pd.Series([0.125, -0.25, np.nan], dtype="float64")),
        ("partial_charge", pd.Series([0.125, -0.25, pd.NA], dtype="Float32")),
        ("partial_charge", pd.Series([0.125, -0.25, pd.NA], dtype="Float64")),
        ("partial_charge", pd.Series([0.125, None, pd.NA], dtype=object)),
        ("partial_charge", pd.Series([np.nan, None, pd.NA], dtype=object)),
        ("formal_charge", pd.Series([0, 1, -1], dtype="int16")),
        ("formal_charge", pd.Series([0, 1, 2], dtype="uint64")),
        ("formal_charge", pd.Series([0, 1, pd.NA], dtype="Int16")),
        ("formal_charge", pd.Series([0, 1, pd.NA], dtype="UInt8")),
        ("formal_charge", pd.Series([0.0, 1.0, np.nan], dtype="float64")),
        ("formal_charge", pd.Series([0, None, pd.NA], dtype=object)),
        ("atom_ff_type", pd.Series(["Cl", "H", None], dtype=object)),
        ("atom_ff_type", pd.Series(["Cl", pd.NA, np.nan], dtype=object)),
        (
            "atom_ff_type",
            pd.Series(["Cl", "H", None], dtype=pd.StringDtype(storage="python")),
        ),
        (
            "atom_ff_type",
            pd.Series(
                ["Cl", "H", None],
                dtype=pd.StringDtype(storage="python", na_value=np.nan),
            ),
        ),
    ],
)
def test_nullable_mechanical_columns_keep_values_dtypes_and_missing_policy(
    tmp_path, name, series
):
    source = MolecularMechanics()
    source.atoms_ff = pd.DataFrame({name: series})
    restored = _roundtrip(tmp_path, source)
    pd.testing.assert_frame_equal(restored.atoms_ff, source.atoms_ff, check_exact=True)
    if series.dtype == np.dtype("object"):
        for old, new in zip(series, restored.atoms_ff[name]):
            if old is None or old is pd.NA:
                assert new is old
            elif isinstance(old, float) and np.isnan(old):
                assert isinstance(new, float) and np.isnan(new)


@pytest.mark.parametrize("table", [None, pd.DataFrame(index=pd.RangeIndex(3))])
@pytest.mark.parametrize("report", [None, {}])
def test_absence_and_present_empty_storage_remain_distinct(tmp_path, table, report):
    source = MolecularMechanics()
    source.atoms_ff = table
    source.partial_charge_assignment = report
    source.atom_type_assignment = report
    restored = _roundtrip(tmp_path, source)
    assert (restored.atoms_ff is None) == (table is None)
    if table is not None:
        pd.testing.assert_frame_equal(restored.atoms_ff, table)
    assert restored.partial_charge_assignment == report
    assert restored.atom_type_assignment == report
    with h5py.File(tmp_path / "no_layer.h5", "w") as file:
        assert read_mechanics(file) is None


def test_all_settings_preserve_requests_units_and_explicit_false_or_zero(tmp_path):
    puw = msm.pyunitwizard
    source = MolecularMechanics(
        forcefield="unresolved_model_request",
        water_model="TIP3P",
        implicit_solvent="OBC2",
        non_bonded_method="cutoff_non_periodic",
        cutoff_distance=puw.quantity(12.0, "angstrom"),
        switch_distance=puw.quantity(0.8, "nm"),
        dispersion_correction=False,
        ewald_error_tolerance=np.float32(1e-4),
        constraints="all_bonds",
        flexible_constraints=True,
        rigid_water=False,
        hydrogen_mass=puw.quantity(2.0, "Da"),
        salt_concentration=puw.quantity(0.0, "mole/liter"),
        kappa=puw.quantity(0.125, "1/angstrom"),
        solute_dielectric=1.0,
        solvent_dielectric=78.5,
    )
    with puw.context(
        standard_units=[
            "pm",
            "fs",
            "coulomb",
            "K",
            "mole",
            "dalton",
            "kJ/mol",
            "radians",
        ]
    ):
        before = puw.configure.report()
        restored = _roundtrip(tmp_path, source)
        assert puw.configure.report() == before
        for name, value in vars(source).items():
            actual = getattr(restored, name)
            if value is not None and name in {
                "cutoff_distance",
                "switch_distance",
                "hydrogen_mass",
                "salt_concentration",
                "kappa",
            }:
                assert str(puw.get_unit(actual)) == str(puw.get_unit(value))
                np.testing.assert_array_equal(
                    puw.get_value(actual), puw.get_value(value)
                )
            else:
                assert actual == value
        assert restored.dispersion_correction is False
        assert restored.rigid_water is False
        assert type(restored.ewald_error_tolerance) is np.float32


def test_metadata_arrays_are_datasets_and_text_stays_text(tmp_path):
    source = MolecularMechanics()
    source.atom_type_assignment = {
        "schema": "synthetic_codec_fixture",
        "status": "stale",
        "software": {"producer": "0.23.0", "numeric_version": "1.2", "label": "H"},
        "parent_atom_indices": np.array([2**53 + 1, 2**53 + 3], dtype=np.uint64),
        "rule_order": ("first", "second"),
        "empty": np.empty((0, 4), dtype=np.float32),
        "unicode": np.array(["π", "β"], dtype="U3"),
        "scalar": np.int32(7),
        "large": np.arange(100_000, dtype=np.int64),
        "looks_typed": {"type": "array", "index": 999, "dtype": "object", "shape": [3]},
    }
    restored = _roundtrip(tmp_path, source)
    old, new = source.atom_type_assignment, restored.atom_type_assignment
    assert new["software"] == old["software"]
    assert new["rule_order"] == old["rule_order"] and type(new["rule_order"]) is tuple
    assert type(new["scalar"]) is np.int32
    assert new["looks_typed"] == old["looks_typed"]
    for key in ("parent_atom_indices", "empty", "unicode", "large"):
        assert new[key].dtype == old[key].dtype and new[key].shape == old[key].shape
        np.testing.assert_array_equal(new[key], old[key])
    with h5py.File(tmp_path / "private_layer.h5", "r") as file:
        group = file["molecular_mechanics/snapshot"]
        assert len(group["json"]) < 10_000
        assert any(
            dataset.dtype == np.dtype("uint64") for dataset in group["arrays"].values()
        )
        assert any(dataset.shape == (100_000,) for dataset in group["arrays"].values())
        text_datasets = [
            dataset
            for dataset in group["arrays"].values()
            if h5py.check_string_dtype(dataset.dtype) is not None
        ]
        assert text_datasets
        assert all(
            h5py.check_string_dtype(dataset.dtype).length is not None
            for dataset in text_datasets
        )


@pytest.mark.parametrize(
    "damage",
    [
        "extra",
        "subclass",
        "column",
        "axis",
        "attrs",
        "dtype",
        "quantity_shape",
        "bare_quantity",
        "text_quantity",
        "wrong_dimension",
        "bad_report",
        "opaque_report",
        "cycle",
        "nonfinite",
        "fractional_formal_charge",
    ],
)
def test_unsupported_state_is_rejected_before_creating_a_layer(tmp_path, damage):
    source = MolecularMechanics()
    if damage == "extra":
        source.unrepresented = None
    elif damage == "subclass":

        class Extended(MolecularMechanics):
            pass

        source = Extended()
    elif damage in {"column", "axis", "attrs", "dtype", "fractional_formal_charge"}:
        source.partial_charge = np.array([0.1, 0.2, 0.3])
        if damage == "column":
            source.atoms_ff["unrepresented"] = 1
        elif damage == "axis":
            source.atoms_ff.index = [2, 1, 0]
        elif damage == "attrs":
            source.atoms_ff.attrs["unrepresented"] = 1
        elif damage == "dtype":
            source.atoms_ff["partial_charge"] = source.atoms_ff.partial_charge.astype(
                "float16"
            )
        else:
            source.formal_charge = [0.0, 0.5, 1.0]
    elif damage == "quantity_shape":
        source.cutoff_distance = msm.pyunitwizard.quantity([1.0], "nm")
    elif damage == "bare_quantity":
        source.cutoff_distance = 1.0
    elif damage == "text_quantity":
        source.cutoff_distance = "1 nm"
    elif damage == "wrong_dimension":
        source.cutoff_distance = msm.pyunitwizard.quantity(1.0, "ps")
    elif damage == "bad_report":
        source.atom_type_assignment = []
    elif damage == "opaque_report":
        source.atom_type_assignment = {"opaque": object()}
    elif damage == "cycle":
        source.atom_type_assignment = {}
        source.atom_type_assignment["self"] = source.atom_type_assignment
    elif damage == "nonfinite":
        source.solvent_dielectric = np.inf
    with h5py.File(tmp_path / "refused.h5", "w") as file:
        with pytest.raises(ValueError):
            write_mechanics(file, source, n_atoms=3)
        assert "molecular_mechanics" not in file


def _observation(mechanics):
    from tests.native.test_prepared_system_checkpoint import _plain

    return _plain(
        {
            "table": mechanics.atoms_ff,
            "partial_charge_assignment": mechanics.partial_charge_assignment,
            "atom_type_assignment": mechanics.atom_type_assignment,
        }
    )


@pytest.mark.parametrize("scope", ["complete", "projected", "merged"])
def test_real_preparation_reports_survive_a_fresh_reader_without_engines(
    tmp_path, scope
):
    from tests.native.test_prepared_system_checkpoint import _prepared

    source = _prepared(scope)
    path = tmp_path / "prepared_layer.h5"
    expected = _observation(source.molecular_mechanics)
    with h5py.File(path, "w") as file:
        write_mechanics(file, source.molecular_mechanics, n_atoms=source.get_n_atoms())
    (tmp_path / "expected.json").write_text(json.dumps(expected))
    script = """
import builtins, json, sys
from pathlib import Path
sys.path.insert(0,str(Path.cwd()))
original_import = builtins.__import__
def guarded(name,*args,**kwargs):
    if name.split('.')[0] in {'rdkit','openmm','ackredit'}:
        raise ImportError('Backend deliberately unavailable: '+name)
    return original_import(name,*args,**kwargs)
builtins.__import__ = guarded
import pyunitwizard as puw
with puw.context(standard_units=['angstrom','fs','coulomb','K','mole','dalton','kJ/mol','radians']):
    keys=['default_form','default_parser','standard_units','provenance']
    before={key:puw.configure.report()[key] for key in keys}
    import h5py
    import molsysmt as msm
    from molsysmt._private.h5msm_storage.mechanics import read_mechanics
    from tests.form.file_h5msm.test_mechanics_layer import _observation
    expected=json.loads(Path(sys.argv[2]).read_text())
    current=msm.__version__
    try:
        msm.__version__='999.0.0+reader.probe'
        with h5py.File(sys.argv[1],'r') as file:restored=read_mechanics(file,n_atoms=int(sys.argv[3]))
    finally:msm.__version__=current
    assert _observation(restored)==expected
    assert restored.forcefield=='AMBER14' and restored.implicit_solvent=='OBC2'
    assert float(puw.get_value(restored.cutoff_distance,to_unit='angstrom'))==12.0
    assert float(puw.get_value(restored.hydrogen_mass,to_unit='Da'))==2.0
    assert float(puw.get_value(restored.salt_concentration,to_unit='mole/liter'))==0.15
    assert {key:puw.configure.report()[key] for key in keys}==before
    assert not any(name.split('.')[0] in {'rdkit','openmm','ackredit'} for name in sys.modules)
    print(json.dumps({'restored':True,'producer_retained':True,'no_engines':True,'policy_preserved':True}))
"""
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            script,
            str(path),
            str(tmp_path / "expected.json"),
            str(source.get_n_atoms()),
        ],
        env=os.environ.copy(),
        text=True,
        capture_output=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert json.loads(result.stdout)["no_engines"]
    assert _observation(source.molecular_mechanics) == expected


@pytest.mark.parametrize("header", ["text", "bytes"])
def test_mechanics_codec_cannot_expand_a_05_file(tmp_path, header):
    with h5py.File(tmp_path / "old.h5", "w") as file:
        file.attrs["type"] = "h5msm" if header == "text" else np.bytes_("h5msm")
        file.attrs["version"] = "0.5" if header == "text" else np.bytes_("0.5")
        with pytest.raises(ValueError, match="no molecular mechanics layer"):
            write_mechanics(file, MolecularMechanics(), n_atoms=0)
        assert not list(file)


@pytest.mark.parametrize(
    "damage",
    [
        "version",
        "atom_count",
        "extra",
        "unused_array",
        "missing_array",
        "dtype",
        "shape",
        "duplicate_key",
        "unknown_node",
    ],
)
def test_malformed_layer_data_never_becomes_a_plausible_snapshot(tmp_path, damage):
    source = MolecularMechanics(partial_charge=np.array([0.1, 0.2, 0.3]))
    path = tmp_path / "damaged.h5"
    with h5py.File(path, "w") as file:
        write_mechanics(file, source, n_atoms=3)
        layer = file["molecular_mechanics"]
        tree = layer["snapshot"]
        if damage == "version":
            layer.attrs["schema_version"] = 99
        elif damage == "atom_count":
            layer.attrs["n_atoms"] = 4
        elif damage == "extra":
            layer.create_dataset("unknown", data=[1])
        elif damage == "unused_array":
            tree["arrays"].create_dataset("999", data=[1])
        elif damage == "missing_array":
            del tree["arrays/0"]
        else:
            manifest = json.loads(tree["json"][:].tobytes())
            if damage == "duplicate_key":
                manifest["items"].append(manifest["items"][0])
            elif damage == "unknown_node":
                manifest["type"] = "executable"
            else:

                def corrupt(node):
                    if isinstance(node, dict):
                        if node.get("type") == "array":
                            node[damage] = "<i8" if damage == "dtype" else [999]
                            return True
                        return any(corrupt(value) for value in node.values())
                    if isinstance(node, list):
                        return any(corrupt(value) for value in node)
                    return False

                assert corrupt(manifest)
            del tree["json"]
            tree.create_dataset(
                "json",
                data=np.frombuffer(json.dumps(manifest).encode(), dtype=np.uint8),
            )
    with h5py.File(path, "r") as file:
        with pytest.raises(ValueError):
            read_mechanics(file, n_atoms=3)


def test_private_tree_preserves_array_and_literal_mapping_identity(tmp_path):
    value = {
        "tuple": (np.float32(2.0), np.array(True)),
        "literal": {"type": "array", "index": 0},
        "text": "H",
    }
    with h5py.File(tmp_path / "tree.h5", "w") as file:
        _write_tree(file, "metadata", _prepare_tree(value))
        restored = _read_tree(file["metadata"])
    assert type(restored["tuple"]) is tuple
    assert type(restored["tuple"][0]) is np.float32
    assert (
        isinstance(restored["tuple"][1], np.ndarray)
        and restored["tuple"][1].shape == ()
    )
    assert restored["literal"] == value["literal"] and restored["text"] == "H"


@pytest.mark.parametrize("n_atoms", [True, -1, 1.5, 2**63])
def test_invalid_atom_cardinality_is_refused_before_layer_creation(tmp_path, n_atoms):
    with h5py.File(tmp_path / "invalid_count.h5", "w") as file:
        with pytest.raises(ValueError):
            write_mechanics(file, MolecularMechanics(), n_atoms=n_atoms)
        assert not list(file)


def test_zero_atom_layer_keeps_a_present_table(tmp_path):
    source = MolecularMechanics()
    source.atoms_ff = pd.DataFrame({"atom_ff_type": pd.Series([], dtype=object)})
    restored = _roundtrip(tmp_path, source, n_atoms=0)
    pd.testing.assert_frame_equal(restored.atoms_ff, source.atoms_ff)


@pytest.mark.parametrize(
    "parent", ["molecular_mechanics", "molecular_mechanics/snapshot"]
)
@pytest.mark.parametrize("version", [True, [1]])
def test_layer_versions_are_scalar_integers(tmp_path, parent, version):
    path = tmp_path / "bad_version.h5"
    with h5py.File(path, "w") as file:
        write_mechanics(file, MolecularMechanics(), n_atoms=0)
        del file[parent].attrs["schema_version"]
        file[parent].attrs["schema_version"] = version
    with h5py.File(path, "r") as file:
        with pytest.raises(ValueError):
            read_mechanics(file)


@pytest.mark.parametrize("damage", ["field", "dimension", "seal"])
def test_quantity_reader_checks_field_dimension_and_seal(tmp_path, damage):
    from pyunitwizard.record import QuantityRecord

    source = MolecularMechanics(cutoff_distance=msm.pyunitwizard.quantity(1.0, "nm"))
    path = tmp_path / "wrong_quantity.h5"
    with h5py.File(path, "w") as file:
        write_mechanics(file, source, n_atoms=0)
        group = file["molecular_mechanics/snapshot"]
        tree = json.loads(group["json"][:].tobytes())

        def change(node):
            if isinstance(node, dict):
                if node.get("type") == "quantity":
                    field = "molsysmt.MolecularMechanics/" + (
                        "hydrogen_mass" if damage == "field" else "cutoff_distance"
                    )
                    unit = "ps" if damage == "dimension" else "nm"
                    node["record"] = QuantityRecord.from_quantity(
                        msm.pyunitwizard.quantity(1.0, unit), field=field
                    ).to_dict()
                    if damage == "seal":
                        node["record"]["manifest"]["unit"] = "picosecond"
                    return True
                return any(change(item) for item in node.values())
            if isinstance(node, list):
                return any(change(item) for item in node)
            return False

        assert change(tree)
        del group["json"]
        group.create_dataset(
            "json", data=np.frombuffer(json.dumps(tree).encode(), dtype=np.uint8)
        )
    with h5py.File(path, "r") as file:
        with pytest.raises(Exception) as caught:
            read_mechanics(file)
        assert type(caught.value).__name__ == "RecordError"


def test_a_masked_array_cannot_lose_its_mask_in_an_assignment_report(tmp_path):
    source = MolecularMechanics()
    source.atom_type_assignment = {
        "evidence": np.ma.array([1.0, 2.0], mask=[False, True])
    }
    with h5py.File(tmp_path / "masked.h5", "w") as file:
        with pytest.raises(ValueError, match="subclasses"):
            write_mechanics(file, source, n_atoms=0)
        assert not list(file)


@pytest.mark.parametrize("unit", ["coulomb", None])
def test_charge_column_units_are_an_explicit_fixed_unit_protocol(tmp_path, unit):
    source = MolecularMechanics(partial_charge=np.array([0.1, 0.2, 0.3]))
    path = tmp_path / "wrong_charge_unit.h5"
    with h5py.File(path, "w") as file:
        write_mechanics(file, source, n_atoms=3)
        layer = file["molecular_mechanics"]
        payload = _read_tree(layer["snapshot"])
        payload["atoms_ff"]["columns"][0]["unit"] = unit
        del layer["snapshot"]
        _write_tree(layer, "snapshot", _prepare_tree(payload))
    with h5py.File(path, "r") as file:
        with pytest.raises(ValueError, match="wrong unit"):
            read_mechanics(file, n_atoms=3)
