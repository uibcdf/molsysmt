"""Verify source bytes, public offline lookup and conservative regeneration."""

import hashlib
import importlib.util
import json
import socket
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm

ROOT = Path(__file__).parents[2]
DATA = ROOT / "molsysmt/data/pdb"
MANIFEST = json.loads((DATA / "course_sources.json").read_text())
CATALOG = {
    "5xjh.pdb": "PETase",
    "6eqe.pdb": "PETase",
    "6lu7.pdb": "SARS-CoV-2 main protease",
    "1k4c.pdb": "Potassium channel KcsA",
}


@pytest.mark.parametrize("name", CATALOG)
def test_original_bytes_and_native_source_labels(name, monkeypatch):
    def reject_network(*args, **kwargs):
        raise AssertionError("Bundled data must not resolve a remote host")

    monkeypatch.setattr(socket, "getaddrinfo", reject_network)
    resource = msm.systems[CATALOG[name]][name]
    data = resource.read_bytes()
    record = MANIFEST["files"][name]
    assert len(data) == record["bytes"]
    assert hashlib.sha256(data).hexdigest() == record["sha256"]
    molsys = msm.convert(resource, get_missing_bonds=False)
    # Independent fixed-column source oracle, not a second form conversion.
    lines = [
        line
        for line in data.decode().splitlines()
        if line.startswith(("ATOM  ", "HETATM")) and line[16] in (" ", "A")
    ]
    assert molsys.topology.atoms.atom_id.tolist() == [
        line[6:11].strip() for line in lines
    ]
    np.testing.assert_allclose(
        msm.pyunitwizard.get_value(molsys.structures.coordinates, to_unit="nm")[0],
        [
            [float(line[start : start + 8]) / 10 for start in (30, 38, 46)]
            for line in lines
        ],
    )
    group_index = molsys.topology.atoms.group_index.to_numpy()
    chain_index = molsys.topology.atoms.chain_index.to_numpy()
    assert molsys.topology.groups.group_id.to_numpy()[group_index].tolist() == [
        line[22:26].strip() for line in lines
    ]
    assert molsys.topology.chains.chain_id.to_numpy()[chain_index].tolist() == [
        line[21].strip() for line in lines
    ]
    assert resource.read_bytes() == data
    assert name in msm.systems.info[CATALOG[name]]["files"]


def generator():
    spec = importlib.util.spec_from_file_location(
        "course_pdb_sources", ROOT / "molsysmt/data/_make/course_pdb_sources.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_regeneration_preserves_exact_bytes_and_rejects_changed_inputs(tmp_path):
    module = generator()
    module.restore(tmp_path, MANIFEST, source_directory=DATA)
    module.restore(tmp_path, MANIFEST)  # Already complete: no network required.
    for name in CATALOG:
        assert (tmp_path / name).read_bytes() == (DATA / name).read_bytes()
    target = tmp_path / "5xjh.pdb"
    target.write_bytes(b"changed")
    with pytest.raises(ValueError, match="5xjh"):
        module.restore(tmp_path, MANIFEST, source_directory=DATA)
    assert target.read_bytes() == b"changed"


def test_missing_sources_do_not_trigger_implicit_download(tmp_path, monkeypatch):
    module = generator()

    def forbidden(*args, **kwargs):
        raise AssertionError("An explicit download flag is required")

    monkeypatch.setattr(module.urllib.request, "urlopen", forbidden)
    with pytest.raises(FileNotFoundError, match="explicitly --download"):
        module.restore(tmp_path, MANIFEST)
    assert not list(tmp_path.iterdir())
