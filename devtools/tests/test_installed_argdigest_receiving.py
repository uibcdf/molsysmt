"""Rejecting source overlays, changed provider bytes and incomplete receiving."""

import hashlib
import io
import json
import tarfile
from pathlib import Path
from types import SimpleNamespace

import pytest
import yaml

from devtools.scripts import receive_installed_argdigest as receiving


@pytest.fixture
def public_file(tmp_path):
    archive = tmp_path / receiving.FILENAME
    contents = {
        "info/index.json": json.dumps(
            {"name": "argdigest", "version": "0.17.1", "build": "py_0"}
        ).encode(),
        "site-packages/argdigest/__init__.py": b"__version__ = '0.17.1'\n",
        "site-packages/argdigest/core.py": b"VALUE = 42\n",
    }
    purelib = tmp_path / "prefix/site-packages"
    with tarfile.open(archive, "w:bz2") as output:
        for name, value in contents.items():
            info = tarfile.TarInfo(name)
            info.size = len(value)
            output.addfile(info, io.BytesIO(value))
            if name.startswith("site-packages/"):
                destination = purelib / name.removeprefix("site-packages/")
                destination.parent.mkdir(parents=True, exist_ok=True)
                destination.write_bytes(value)
    return archive, purelib, hashlib.sha256(archive.read_bytes()).hexdigest()


def test_actual_provider_files_must_match_archive(public_file):
    archive, purelib, digest = public_file
    actual = receiving.verify_public_bytes(
        archive, purelib=purelib, expected_sha256=digest
    )
    assert len(actual) == 2
    (purelib / "argdigest/core.py").write_text("VALUE = 999\n")
    with pytest.raises(RuntimeError, match="bytes differ"):
        receiving.verify_public_bytes(archive, purelib=purelib, expected_sha256=digest)


def test_wrong_public_archive_is_not_an_installation(public_file):
    archive, purelib, _ = public_file
    with pytest.raises(RuntimeError, match="SHA-256"):
        receiving.verify_public_bytes(archive, purelib=purelib)


def test_an_extra_runtime_overlay_is_rejected(public_file):
    archive, purelib, digest = public_file
    (purelib / "argdigest/overlay.py").write_text("VALUE = 0\n")
    with pytest.raises(RuntimeError, match="inventory differs"):
        receiving.verify_public_bytes(archive, purelib=purelib, expected_sha256=digest)


@pytest.mark.parametrize("mode", ["editable", "outside", "dependencies", "valid"])
def test_installed_origins_reject_source_substitution(tmp_path, monkeypatch, mode):
    prefix = tmp_path / "prefix"
    module = (tmp_path if mode == "outside" else prefix) / "argdigest/__init__.py"
    module.parent.mkdir(parents=True)
    module.write_text("__version__ = '0.17.1'\n")
    distribution = SimpleNamespace(
        version="0.17.1",
        read_text=lambda _: json.dumps({"dir_info": {"editable": mode == "editable"}}),
    )
    monkeypatch.setattr(receiving.metadata, "distribution", lambda _: distribution)
    monkeypatch.setattr(
        receiving.importlib,
        "import_module",
        lambda _: SimpleNamespace(__file__=str(module)),
    )
    monkeypatch.setattr(
        receiving,
        "find_runtime_dependency_violations",
        lambda _: ["missing dependency"] if mode == "dependencies" else [],
    )
    if mode == "valid":
        assert receiving.installed_origins(
            modules=("argdigest",), prefix=prefix, purelib=prefix
        )["argdigest"]["origin"] == str(module)
    else:
        with pytest.raises(
            RuntimeError,
            match={
                "editable": "editable",
                "outside": "outside prefix",
                "dependencies": "dependency violations",
            }[mode],
        ):
            receiving.installed_origins(
                modules=("argdigest",), prefix=prefix, purelib=prefix
            )


@pytest.mark.parametrize(
    "bad", ["zero", "skipped", "failure", "forged_counter", "wrong_inventory"]
)
def test_receiving_cannot_pass_with_missing_or_unsuccessful_cases(tmp_path, bad):
    cases = '<testcase classname="tests.native.test_inherited_constructors" name="test_valid"/>'
    attributes = 'tests="1" failures="0" errors="0" skipped="0"'
    if bad == "zero":
        attributes = attributes.replace('tests="1"', 'tests="0"')
        cases = ""
    elif bad == "skipped":
        attributes = attributes.replace('skipped="0"', 'skipped="1"')
    elif bad == "failure":
        attributes = attributes.replace('failures="0"', 'failures="1"')
    elif bad == "wrong_inventory":
        attributes = attributes.replace('tests="1"', 'tests="2"')
    else:
        cases = cases.replace("/>", "><skipped/></testcase>")
    junit = tmp_path / "result.xml"
    junit.write_text(
        f"<testsuites><testsuite {attributes}>{cases}</testsuite></testsuites>"
    )
    with pytest.raises(RuntimeError):
        receiving.verify_junit(junit)


def test_scientific_receiving_requires_all_registered_controls():
    nodes = [
        "tests/scientific_truth/a.py::test_first",
        "tests/scientific_truth/b.py::test_second",
    ]
    cases = ["tests.scientific_truth.a::test_first[variant]"]
    with pytest.raises(RuntimeError, match="test_second"):
        receiving.verify_scientific_coverage(nodes, cases)
    receiving.verify_scientific_coverage(
        nodes, [*cases, "tests.scientific_truth.b::test_second"]
    )


def test_hosted_receiving_cannot_publish_or_run_implicitly():
    root = Path(__file__).resolve().parents[2]
    workflow = yaml.safe_load(
        (root / ".github/workflows/receive_public_argdigest.yaml").read_text()
    )
    triggers = workflow.get("on", workflow.get(True))
    assert set(triggers) == {"workflow_dispatch"}
    assert workflow["permissions"] == {"contents": "read"}
    steps = workflow["jobs"]["installed-receiving"]["steps"]
    assert not any("upload-conda" in step.get("uses", "") for step in steps)
    code = "\n".join(step.get("run", "") for step in steps)
    assert "--editable" not in code
    assert "--consumer-junit consumer.xml --scientific-junit scientific.xml" in code
    assert "--scientific-nodes scientific-nodes.json" in code
