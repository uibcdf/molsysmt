from __future__ import annotations

from urllib.error import URLError

import pytest


@pytest.mark.parametrize(
    ("module_name", "pdb_id", "expected_resource", "expected_url"),
    [
        (
            "molsysmt.form.file_bcif.download",
            "pdb_id:181l",
            "181l.bcif",
            "https://models.rcsb.org/181l.bcif",
        ),
        (
            "molsysmt.form.file_bcif_gz.download",
            "pdb_181l",
            "181l.bcif.gz",
            "https://models.rcsb.org/181l.bcif.gz",
        ),
        (
            "molsysmt.form.file_cif.download",
            "181l",
            "181l.cif",
            "https://files.rcsb.org/download/181l.cif",
        ),
        (
            "molsysmt.form.file_cif_gz.download",
            "181l",
            "181l.cif.gz",
            "https://files.rcsb.org/download/181l.cif.gz",
        ),
        (
            "molsysmt.form.file_pdb.download",
            "181l",
            "181l.pdb",
            "https://files.rcsb.org/download/181l.pdb",
        ),
    ],
)
def test_download_paths_emit_structured_retry_context(
    monkeypatch, tmp_path, module_name, pdb_id, expected_resource, expected_url
):
    """Download helpers should emit structured retry diagnostics for transient failures."""
    import importlib
    import molsysmt._private.download as private_download

    module = importlib.import_module(module_name)
    events = []

    def fake_warn(message, warning_cls, extra=None):
        events.append({"message": message, "warning_cls": warning_cls, "extra": extra})

    monkeypatch.setattr(private_download, "warn", fake_warn)
    monkeypatch.setattr(private_download, "urlopen", lambda *args, **kwargs: (_ for _ in ()).throw(URLError("timed out")))
    monkeypatch.setattr(private_download.random, "uniform", lambda a, b: 0.0)
    monkeypatch.setattr(private_download.time, "sleep", lambda wait: None)

    output_path = tmp_path / expected_resource
    with pytest.raises(RuntimeError, match="Could not download"):
        module.download(
            pdb_id=pdb_id,
            output_filename=str(output_path),
            retries=1,
            timeout=1,
            backoff_base=2.0,
        )

    assert len(events) == 1
    event = events[0]
    assert expected_resource in event["message"]
    assert event["extra"]["resource"] == expected_resource
    assert event["extra"]["reason"] == "timed out"
    assert event["extra"]["attempt"] == 1
    assert event["extra"]["retries"] == 1
    assert event["extra"]["url"] == expected_url
