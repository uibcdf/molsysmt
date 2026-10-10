"""Keeping standalone native probe resources alive only through child exit."""

import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

from devtools.scripts import benchmark_interactions_temporal as probe


def test_python_probe_preserves_results_without_compiling_or_spawning(
    monkeypatch, capsys
):
    monkeypatch.setattr(
        sys,
        "argv",
        [
            str(Path(probe.__file__)),
            "--frames",
            "9",
            "--relations",
            "12",
            "--active",
            "3",
        ],
    )

    def reject(*args, **kwargs):
        raise AssertionError("The Python-only probe must not compile or spawn")

    monkeypatch.setattr(probe, "_compile_rust_probe", reject)
    monkeypatch.setattr(probe.subprocess, "Popen", reject)
    probe.main()
    result = json.loads(capsys.readouterr().out)
    assert result["occurrences"] == 21
    assert result["evaluated_empty_structures"] == 2
    assert result["config"]["rust"] is False
    assert "rust_ctypes_query" not in result


@pytest.mark.parametrize(
    "error",
    [
        FileNotFoundError("compiler unavailable"),
        subprocess.CalledProcessError(1, ["rustc"], stderr="compile failed"),
    ],
)
def test_compile_failure_retires_owned_directory(monkeypatch, tmp_path, error):
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    caller_file = tmp_path / "receipt.json"
    caller_file.write_text("caller evidence")
    monkeypatch.setattr(probe.tempfile, "tempdir", str(scratch))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            str(Path(probe.__file__)),
            "--frames",
            "9",
            "--relations",
            "12",
            "--active",
            "3",
            "--rust",
        ],
    )

    def reject_compile(command, **kwargs):
        Path(command[-1]).write_bytes(b"partial native output")
        raise error

    monkeypatch.setattr(probe.subprocess, "run", reject_compile)
    with pytest.raises(type(error)) as caught:
        probe.main()
    assert caught.value is error
    assert list(scratch.iterdir()) == []
    assert caller_file.read_text() == "caller evidence"


@pytest.fixture(scope="module")
def compiled_probes(tmp_path_factory):
    if shutil.which("rustc") is None:
        pytest.skip("The standalone probe requires rustc")
    directory = tmp_path_factory.mktemp("temporal-native-inputs")
    suffix = (
        ".dll"
        if sys.platform == "win32"
        else ".dylib"
        if sys.platform == "darwin"
        else ".so"
    )
    valid = directory / f"valid{suffix}"
    probe._compile_rust_probe(valid)
    source = directory / "reject.rs"
    kernel = (
        Path(probe.__file__).with_name("interactions_temporal_kernel.rs").read_text()
    )
    original_guard = "if block_size == 0 || output_capacity < n_relations {"
    assert kernel.count(original_guard) == 1
    source.write_text(
        kernel.replace(
            original_guard,
            "if true || block_size == 0 || output_capacity < n_relations {",
        )
    )
    rejected = directory / f"rejected{suffix}"
    subprocess.run(
        [
            "rustc",
            "--edition=2021",
            "-O",
            "--crate-type=cdylib",
            str(source),
            "-o",
            str(rejected),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    batch_source = directory / "reject_batch.rs"
    batch_guard = "if n_frames\n"
    assert kernel.count(batch_guard) == 1
    batch_source.write_text(kernel.replace(batch_guard, "if true || n_frames\n"))
    batch_rejected = directory / f"batch_rejected{suffix}"
    subprocess.run(
        [
            "rustc",
            "--edition=2021",
            "-O",
            "--crate-type=cdylib",
            str(batch_source),
            "-o",
            str(batch_rejected),
        ],
        check=True,
        capture_output=True,
        text=True,
    )
    return valid, rejected, batch_rejected


@pytest.fixture
def native_owner(monkeypatch, tmp_path, compiled_probes):
    scratch = tmp_path / "scratch"
    scratch.mkdir()
    caller_file = tmp_path / "receipt.json"
    caller_file.write_text("caller evidence")
    monkeypatch.setattr(probe.tempfile, "tempdir", str(scratch))
    monkeypatch.setattr(
        sys,
        "argv",
        [
            str(Path(probe.__file__)),
            "--frames",
            "9",
            "--relations",
            "12",
            "--active",
            "3",
            "--rust",
            "--hdf",
        ],
    )
    monkeypatch.setattr(
        probe,
        "_compile_rust_probe",
        lambda path: shutil.copyfile(compiled_probes[0], path),
    )
    children = []
    original_directory = probe.tempfile.TemporaryDirectory
    original_popen = probe.subprocess.Popen

    class OwnedDirectory(original_directory):
        def cleanup(self):
            assert all(child.poll() is not None for child in children), (
                "Library directory retired before native process exit"
            )
            super().cleanup()

    def start(command, **kwargs):
        library = Path(command[command.index("--_native-library") + 1])
        assert library.is_file()
        for variable in ("TMPDIR", "TMP", "TEMP"):
            assert kwargs["env"][variable] == str(library.parent)
        child = original_popen(command, **kwargs)
        children.append(child)
        return child

    monkeypatch.setattr(probe.tempfile, "TemporaryDirectory", OwnedDirectory)
    monkeypatch.setattr(probe.subprocess, "Popen", start)
    return scratch, caller_file, children, original_popen


def test_real_native_and_hdf_results_survive_child_exit(
    monkeypatch, capsys, native_owner
):
    scratch, caller_file, children, _ = native_owner

    def reject_parent_loading(*args, **kwargs):
        raise AssertionError("The owner process must not load the probe library")

    monkeypatch.setattr(probe.ctypes, "CDLL", reject_parent_loading)
    probe.main()
    result = json.loads(capsys.readouterr().out)
    assert result["config"] == dict(
        frames=9,
        relations=12,
        active=3,
        survival=0.95,
        block_size=100,
        rust=True,
        hdf=True,
    )
    assert result["occurrences"] == 21
    assert result["evaluated_empty_structures"] == 2
    assert result["frame_major_index_bytes"] == 124
    assert set(result["hundred_structure_query_ms"]) == {
        "frame_major_python",
        "rust_single_calls",
        "rust_one_batch_call",
    }
    assert result["rust_ctypes_query"]["median_ms"] >= 0
    assert set(result["hdf_index_and_common_measures_bytes"]) == {
        "frame_major",
        "temporal_runs",
    }
    assert len(children) == 1 and children[0].returncode == 0
    assert children[0].stdout.closed and children[0].stderr.closed
    assert list(scratch.iterdir()) == []
    assert caller_file.read_text() == "caller evidence"


@pytest.mark.parametrize(
    "stage, expected",
    [
        ("load", "OSError"),
        ("query", "native temporal query rejected"),
        ("batch", "native batch temporal query rejected"),
    ],
)
def test_real_native_failure_retires_only_after_child_exit(
    monkeypatch, capsys, native_owner, compiled_probes, stage, expected
):
    scratch, caller_file, children, _ = native_owner

    def compile_input(path):
        if stage == "load":
            path.write_bytes(b"invalid native library")
        else:
            shutil.copyfile(compiled_probes[2 if stage == "batch" else 1], path)

    monkeypatch.setattr(probe, "_compile_rust_probe", compile_input)
    with pytest.raises(subprocess.CalledProcessError) as caught:
        probe.main()
    assert expected in caught.value.stderr
    output = capsys.readouterr()
    assert expected in output.err
    assert output.out == ""
    assert len(children) == 1 and children[0].returncode != 0
    assert children[0].stdout.closed and children[0].stderr.closed
    assert list(scratch.iterdir()) == []
    assert caller_file.read_text() == "caller evidence"


def test_native_child_start_failure_preserves_original_error(monkeypatch, native_owner):
    scratch, caller_file, children, _ = native_owner
    error = OSError("child start failed")

    def reject(*args, **kwargs):
        raise error

    monkeypatch.setattr(probe.subprocess, "Popen", reject)
    with pytest.raises(OSError) as caught:
        probe.main()
    assert caught.value is error
    assert children == []
    assert list(scratch.iterdir()) == []
    assert caller_file.read_text() == "caller evidence"


@pytest.mark.parametrize(
    "error", [KeyboardInterrupt(), RuntimeError("communication failed")]
)
def test_interrupted_loaded_child_is_reaped_before_retirement(
    monkeypatch, native_owner, error
):
    scratch, caller_file, children, original_popen = native_owner

    def start(command, **kwargs):
        library = command[command.index("--_native-library") + 1]
        code = "import ctypes, pathlib, sys, tempfile, time; library=ctypes.CDLL(sys.argv[1]); pathlib.Path(tempfile.gettempdir(), 'child-scratch').write_text('owned'); print('loaded', flush=True); time.sleep(60)"
        child = original_popen([sys.executable, "-c", code, library], **kwargs)
        children.append(child)

        def interrupt():
            assert child.stdout.readline().strip() == "loaded"
            assert Path(library).is_file()
            assert (Path(library).parent / "child-scratch").is_file()
            raise error

        child.communicate = interrupt
        return child

    monkeypatch.setattr(probe.subprocess, "Popen", start)
    with pytest.raises(type(error)) as caught:
        probe.main()
    assert caught.value is error
    assert len(children) == 1 and children[0].returncode != 0
    assert children[0].stdout.closed and children[0].stderr.closed
    assert list(scratch.iterdir()) == []
    assert caller_file.read_text() == "caller evidence"


def test_retirement_failure_is_visible_without_publishing_a_report(
    monkeypatch, capsys, native_owner
):
    scratch, caller_file, children, _ = native_owner

    def reject(*args, **kwargs):
        assert len(children) == 1 and children[0].returncode == 0
        raise OSError("retirement denied")

    with monkeypatch.context() as retirement:
        retirement.setattr(shutil, "rmtree", reject)
        with pytest.raises(OSError, match="retirement denied"):
            probe.main()
    assert capsys.readouterr().out == ""
    assert caller_file.read_text() == "caller evidence"
    for directory in scratch.iterdir():
        shutil.rmtree(directory)
