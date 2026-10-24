"""Exercise actual process lifetime, failure rollback and temporary ownership."""

import json
import os
import subprocess
import sys
from pathlib import Path

import numpy as np
import pytest

import molsysmt as msm
from molsysmt.native import Structures


@pytest.fixture
def source(tmp_path):
    path = tmp_path / "source.h5msm"
    msm.h5msm.write_layers(
        str(path),
        structures=Structures(
            coordinates=msm.pyunitwizard.quantity(
                np.arange(18.0).reshape(2, 3, 3), "nm"
            )
        ),
    )
    return path


def run_child(code, root, *arguments):
    root.mkdir()
    environment = dict(os.environ, TMPDIR=str(root), TEMP=str(root), TMP=str(root))
    result = subprocess.run(
        [sys.executable, "-c", code, *map(str, arguments)],
        env=environment,
        capture_output=True,
        text=True,
        timeout=45,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout.strip().splitlines()[-1])


def test_normal_exit_cleans_temporaries_but_preserves_persistent_files(
    source, tmp_path
):
    persistent = tmp_path / "persistent.h5msm"
    root = tmp_path / "platform-temporaries"
    report = run_child(
        """
import gc, json, sys
from pathlib import Path
import molsysmt as msm
copies = [msm.copy(sys.argv[1]), msm.copy(sys.argv[1])]
gc.collect()
assert all(Path(str(path)).is_file() for path in copies)
assert len(set(copies)) == 2
assert msm.get_form(copies[0]) == 'file:h5msm'
msm.copy(copies[0], output_filename=sys.argv[2])
print(json.dumps(copies))
""",
        root,
        source,
        persistent,
    )
    assert persistent.read_bytes() == source.read_bytes()
    assert all(Path(path).is_relative_to(root) for path in report)
    assert all(not Path(path).exists() for path in report)
    assert list(root.iterdir()) == []


def test_persistent_destination_inside_workspace_is_never_deleted(source, tmp_path):
    root = tmp_path / "platform-temporaries"
    report = run_child(
        """
import json, sys
from pathlib import Path
import molsysmt as msm
automatic = msm.copy(sys.argv[1])
persistent = str(Path(automatic).parent / 'user-owned.h5msm')
msm.copy(sys.argv[1], output_filename=persistent)
print(json.dumps([automatic, persistent]))
""",
        root,
        source,
    )
    assert not Path(report[0]).exists()
    assert Path(report[1]).read_bytes() == source.read_bytes()


def test_explicit_destination_can_promote_a_previously_automatic_path(source, tmp_path):
    root = tmp_path / "platform-temporaries"
    report = run_child(
        """
import json, sys
from pathlib import Path
import molsysmt as msm
automatic = msm.copy(sys.argv[1])
also_automatic = msm.copy(sys.argv[1])
# Choose the same temporary as an explicit destination through a lexical alias.
path = Path(automatic)
destination = str(path.parent / '..' / path.parent.name / path.name)
msm.copy(sys.argv[1], output_filename=destination)
print(json.dumps([automatic, also_automatic]))
""",
        root,
        source,
    )
    assert Path(report[0]).read_bytes() == source.read_bytes()
    assert not Path(report[1]).exists()


def test_normal_exit_does_not_wait_on_a_daemon_holding_the_registry_lock(
    source, tmp_path
):
    root = tmp_path / "platform-temporaries"
    report = run_child(
        """
import json, sys, threading
import molsysmt as msm
from molsysmt._private import session_files
temporary = msm.copy(sys.argv[1])
ready = threading.Event()
def hold_lock():
    with session_files._lock:
        ready.set()
        threading.Event().wait()
threading.Thread(target=hold_lock, daemon=True).start()
assert ready.wait(5)
print(json.dumps(temporary))
""",
        root,
        source,
    )
    # Cleanup is deliberately best effort; it must not deadlock interpreter exit.
    path = Path(report)
    assert path.read_bytes() == source.read_bytes()
    path.unlink()
    path.parent.rmdir()


def test_failed_copy_discards_only_its_owned_partial_file(
    source, tmp_path, monkeypatch
):
    import shutil

    from molsysmt._private import session_files

    existing = msm.copy(source)
    before = set(session_files._paths)

    def broken_copy(source_path, destination):
        Path(destination).write_bytes(b"partial")
        raise OSError("Simulated copy failure")

    monkeypatch.setattr(shutil, "copyfile", broken_copy)
    with pytest.raises(OSError, match="Simulated copy failure"):
        msm.copy(source)
    assert session_files._paths == before
    assert Path(existing).read_bytes() == source.read_bytes()
    persistent = tmp_path / "user-owned.h5msm"
    with pytest.raises(OSError, match="Simulated copy failure"):
        msm.copy(source, output_filename=persistent)
    assert persistent.read_bytes() == b"partial"
    assert session_files._paths == before


def test_parallel_reservations_are_unique(source):
    from concurrent.futures import ThreadPoolExecutor

    from molsysmt.form.file_h5msm.copy import copy

    with ThreadPoolExecutor(max_workers=8) as executor:
        outputs = list(
            executor.map(lambda _: copy(str(source), skip_digestion=True), range(16))
        )
    assert len(set(outputs)) == 16
    assert len({Path(path).parent for path in outputs}) == 1
    assert all(Path(path).read_bytes() == source.read_bytes() for path in outputs)


def test_read_only_source_produces_a_private_writable_session_copy(source):
    import stat

    import h5py

    mode = source.stat().st_mode
    try:
        source.chmod(mode & ~(stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH))
        result = Path(msm.copy(source))
        assert result.stat().st_mode & stat.S_IWUSR
        with h5py.File(result, "r+") as file:
            file.attrs["temporary_copy_edit"] = "independent"
        with h5py.File(source, "r") as file:
            assert "temporary_copy_edit" not in file.attrs
    finally:
        source.chmod(mode)


def test_composite_failure_retires_completed_temporary_members(source, monkeypatch):
    from molsysmt._private import session_files
    from molsysmt.form import _dict_modules
    from molsysmt.native import Topology

    before = set(session_files._paths)
    original = source.read_bytes()

    def broken_copy(*args, **kwargs):
        raise RuntimeError("Simulated resident copy failure")

    monkeypatch.setattr(_dict_modules["molsysmt.Topology"], "copy", broken_copy)
    with pytest.raises(RuntimeError, match="Simulated resident copy failure"):
        msm.copy([str(source), Topology(n_atoms=3)])
    assert session_files._paths == before
    assert source.read_bytes() == original


@pytest.mark.skipif(
    not hasattr(os, "fork"), reason="The platform has no fork primitive"
)
def test_forked_child_cannot_delete_parent_session_files(source, tmp_path):
    root = tmp_path / "platform-temporaries"
    report = run_child(
        """
import json, os, sys
from pathlib import Path
import molsysmt as msm
from molsysmt._private import session_files
parent_copy = msm.copy(sys.argv[1])
read_fd, write_fd = os.pipe()
pid = os.fork()
if pid == 0:
    os.close(read_fd)
    session_files.cleanup()
    assert Path(parent_copy).is_file()
    child_copy = msm.copy(sys.argv[1])
    assert Path(child_copy).parent != Path(parent_copy).parent
    session_files.cleanup()
    assert not Path(child_copy).exists()
    assert Path(parent_copy).is_file()
    os.write(write_fd, json.dumps(child_copy).encode())
    os.close(write_fd)
    os._exit(0)
os.close(write_fd)
with os.fdopen(read_fd, 'rb') as stream:
    child_copy = json.loads(stream.read())
_, status = os.waitpid(pid, 0)
assert os.waitstatus_to_exitcode(status) == 0
assert Path(parent_copy).is_file()
assert not Path(child_copy).exists()
print(json.dumps([parent_copy, child_copy]))
""",
        root,
        source,
    )
    assert all(not Path(path).exists() for path in report)
    assert list(root.iterdir()) == []
