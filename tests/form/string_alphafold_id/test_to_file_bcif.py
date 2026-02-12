"""Tests for string_alphafold_id -> file:bcif conversion."""

import importlib
import json
from pathlib import Path


class _FakeResponse:
    def __init__(self, payload: bytes, status: int = 200):
        self._payload = payload
        self.status = status

    def read(self):
        return self._payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return False


def test_to_file_bcif_uses_bcif_url_and_default_filename(monkeypatch, tmp_path):
    module_under_test = importlib.import_module("molsysmt.form.string_alphafold_id.to_file_bcif")

    bcif_url = "https://example.org/AF-P52789-F1-model_v4.bcif"
    payload = json.dumps([{"bcifUrl": bcif_url}]).encode("utf-8")

    def fake_urlopen(request):
        return _FakeResponse(payload, status=200)

    def fake_urlretrieve(url, output_filename):
        Path(output_filename).write_bytes(b"BCIF")
        return output_filename, None

    def fake_extract(item, atom_indices, structure_indices, output_filename, copy_if_all, skip_digestion):
        assert item == output_filename
        assert output_filename.endswith(".bcif")
        return output_filename

    monkeypatch.setattr("urllib.request.urlopen", fake_urlopen)
    monkeypatch.setattr("urllib.request.urlretrieve", fake_urlretrieve)
    monkeypatch.setattr(importlib.import_module("molsysmt.form.file_bcif"), "extract", fake_extract)
    monkeypatch.chdir(tmp_path)

    output = module_under_test.to_file_bcif("AF-P52789-F1", skip_digestion=True)
    assert output.endswith("AF-P52789-F1-model_v4.bcif")
