"""Protecting caller destinations and retiring failed download staging."""

import io
from importlib import import_module
from urllib.error import HTTPError, URLError

import pytest


@pytest.fixture
def download(monkeypatch):
    import molsysmt._private.download as owner

    monkeypatch.setattr(owner, "warn", lambda *args, **kwargs: None)
    monkeypatch.setattr(owner.time, "sleep", lambda wait: None)
    return owner


@pytest.mark.parametrize("extension", ["pdb", "cif", "cif_gz", "bcif", "bcif_gz"])
@pytest.mark.parametrize("status", [404, 503])
def test_http_failure_preserves_existing_destination(
    monkeypatch, tmp_path, download, extension, status
):
    destination = tmp_path / "caller.data"
    destination.write_bytes(b"caller evidence")

    def reject(*args, **kwargs):
        raise HTTPError("https://example.org", status, "failed", {}, None)

    monkeypatch.setattr(download, "urlopen", reject)
    adapter = import_module(f"molsysmt.form.file_{extension}.download")
    with pytest.raises(RuntimeError):
        adapter.download("181l", output_filename=str(destination), retries=1)
    assert destination.read_bytes() == b"caller evidence"
    assert list(tmp_path.iterdir()) == [destination]


class InterruptedResponse(io.BytesIO):
    def __init__(self, error):
        super().__init__(b"partial payload")
        self.error = error
        self.started = False

    def read(self, *args):
        if self.started:
            raise self.error
        self.started = True
        return super().read(*args)


@pytest.mark.parametrize("existing", [False, True])
@pytest.mark.parametrize(
    "error", [URLError("connection lost"), OSError("read failed"), KeyboardInterrupt()]
)
def test_stream_failure_retires_only_owned_files(
    monkeypatch, tmp_path, download, existing, error
):
    destination = tmp_path / "result.pdb"
    if existing:
        destination.write_bytes(b"caller evidence")
    monkeypatch.setattr(
        download, "urlopen", lambda *args, **kwargs: InterruptedResponse(error)
    )
    adapter = import_module("molsysmt.form.file_pdb.download")
    with pytest.raises(
        KeyboardInterrupt if isinstance(error, KeyboardInterrupt) else RuntimeError
    ):
        adapter.download("181l", output_filename=str(destination), retries=1)
    if existing:
        assert destination.read_bytes() == b"caller evidence"
        assert list(tmp_path.iterdir()) == [destination]
    else:
        assert list(tmp_path.iterdir()) == []


def test_retry_publishes_only_complete_payload(monkeypatch, tmp_path, download):
    destination = tmp_path / "result.pdb"
    destination.write_bytes(b"caller evidence")
    responses = [
        InterruptedResponse(URLError("connection lost")),
        io.BytesIO(b"complete payload"),
    ]

    def respond(*args, **kwargs):
        assert destination.read_bytes() == b"caller evidence"
        return responses.pop(0)

    monkeypatch.setattr(download, "urlopen", respond)
    adapter = import_module("molsysmt.form.file_pdb.download")
    assert adapter.download("181l", output_filename=str(destination), retries=2) == str(
        destination
    )
    assert destination.read_bytes() == b"complete payload"
    assert list(tmp_path.iterdir()) == [destination]


def test_generated_success_is_a_caller_result(monkeypatch, tmp_path, download):
    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    monkeypatch.setattr(
        download, "urlopen", lambda *args, **kwargs: io.BytesIO(b"complete payload")
    )
    adapter = import_module("molsysmt.form.file_pdb.download")
    from pathlib import Path

    result = Path(adapter.download("181l", tempfile=True))
    assert result.read_bytes() == b"complete payload"
    assert list(tmp_path.iterdir()) == [result]


@pytest.mark.parametrize("published", [False, True])
def test_retirement_failure_is_visible(monkeypatch, tmp_path, download, published):
    import shutil

    destination = tmp_path / "result.pdb"
    destination.write_bytes(b"caller evidence")
    monkeypatch.setattr(
        download,
        "urlopen",
        lambda *args, **kwargs: (
            io.BytesIO(b"complete payload")
            if published
            else InterruptedResponse(OSError("read failed"))
        ),
    )

    def reject(*args, **kwargs):
        raise OSError("retirement denied")

    with monkeypatch.context() as cleanup:
        cleanup.setattr(shutil, "rmtree", reject)
        with pytest.raises(RuntimeError, match="retirement denied"):
            import_module("molsysmt.form.file_pdb.download").download(
                "181l", output_filename=str(destination), retries=1
            )
    assert destination.read_bytes() == (
        b"complete payload" if published else b"caller evidence"
    )
    for directory in tmp_path.iterdir():
        if directory.is_dir():
            shutil.rmtree(directory)


@pytest.mark.parametrize("extension", ["pdb", "cif", "cif_gz", "bcif", "bcif_gz"])
def test_generated_download_failure_leaves_no_output(
    monkeypatch, tmp_path, download, extension
):
    monkeypatch.setattr("tempfile.tempdir", str(tmp_path))
    monkeypatch.setattr(download, "warn", lambda *args, **kwargs: None)
    monkeypatch.setattr(
        download,
        "urlopen",
        lambda *args, **kwargs: InterruptedResponse(URLError("connection lost")),
    )
    adapter = import_module(f"molsysmt.form.file_{extension}.download")
    with pytest.raises(RuntimeError, match="Could not download"):
        adapter.download("181l", tempfile=True, retries=1)
    assert list(tmp_path.iterdir()) == []
