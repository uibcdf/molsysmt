"""Receive unchanged published 0.6 fixtures through both omitted-version routes."""

import hashlib
import importlib
import json
from pathlib import Path

import h5py
import pytest

import molsysmt as msm
from tests.form.file_h5msm.test_modular_mechanics import _hdf_snapshot

PACKET = Path(__file__).resolve().parents[3] / "devtools/data/h5msm_p5_review_20261110"


@pytest.mark.parametrize("scope", ["complete", "projected", "merged"])
@pytest.mark.parametrize("route", ["native_save", "whole_file_migration"])
@pytest.mark.parametrize("units", [["nm", "ps", "radians"], ["pm", "fs", "degrees"]])
def test_original_packet_retains_data_and_provenance_with_default_version(
    tmp_path, monkeypatch, scope, route, units
):
    manifest = json.loads((PACKET / "manifest.json").read_text())
    entry = next(item for item in manifest["fixtures"] if item["scope"] == scope)
    original_hashes = {}
    for name, identity in entry["files"].items():
        data = (PACKET / name).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        assert digest == identity["sha256"] and len(data) == identity["bytes"]
        original_hashes[name] = digest

    def forbidden(*args, **kwargs):
        raise AssertionError("Storage receiving must not recalculate assignments")

    for owner, name in [
        ("build", "assign_partial_charges"),
        ("build", "assign_autodock_atom_types"),
        ("physchem", "get_partial_charges"),
        ("physchem", "get_autodock_atom_types"),
    ]:
        module = importlib.import_module(f"molsysmt.{owner}.{name}")
        monkeypatch.setattr(module, name, forbidden)
        monkeypatch.setattr(getattr(msm, owner), name, forbidden)

    source = PACKET / f"{scope}.h5msm"
    expected = json.loads((PACKET / f"{scope}-expected.json").read_text())
    with h5py.File(source, "r") as file:
        original_metadata = dict(file.attrs)
        assert original_metadata["version"] == "0.6"
    target = tmp_path / f"{scope}-{route}.h5msm"
    with msm.pyunitwizard.context(standard_units=units):
        resident = msm.h5msm.read(source)
        assert _hdf_snapshot(resident) == expected
        if route == "native_save":
            msm.h5msm.write(resident, target)
        else:
            assert msm.convert(source, to_form=target) == target
        with h5py.File(target, "r") as file:
            assert file.attrs["version"] == "1.0"
            if route == "whole_file_migration":
                assert json.loads(file.attrs["migration_source"]) == original_metadata
            else:
                assert "migration_source" not in file.attrs
        assert _hdf_snapshot(msm.h5msm.read(target)) == expected
        assert _hdf_snapshot(resident) == expected

    for name, digest in original_hashes.items():
        assert hashlib.sha256((PACKET / name).read_bytes()).hexdigest() == digest
