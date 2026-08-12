"""Regression tests for the MolSysMT Rust-wheel contract validator."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from zipfile import ZipFile

import pytest


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "validate_rust_wheel.py"
)
SPEC = spec_from_file_location("validate_rust_wheel", SCRIPT)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

INSTALLED_SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "validate_installed_rust_wheel.py"
)
INSTALLED_SPEC = spec_from_file_location(
    "validate_installed_rust_wheel",
    INSTALLED_SCRIPT,
)
INSTALLED_MODULE = module_from_spec(INSTALLED_SPEC)
assert INSTALLED_SPEC.loader is not None
INSTALLED_SPEC.loader.exec_module(INSTALLED_MODULE)


def _write_wheel(
    path,
    *,
    extra_extensions=0,
    bytecode=False,
    legacy=False,
    missing_form_declaration=False,
):
    entries = {
        "molsysmt/_rust.abi3.so": b"extension",
        "molsysmt/py.typed": b"",
        "molsysmt/data/demo_manifest.json": b"{}",
        "molsysviewer_molsysmt/__init__.py": b"",
        "molsysmt-1.0.0.dist-info/WHEEL": (
            b"Wheel-Version: 1.0\n"
            b"Root-Is-Purelib: false\n"
            b"Tag: cp311-abi3-linux_x86_64\n"
        ),
        "molsysmt-1.0.0.dist-info/entry_points.txt": (
            b"[molsysviewer.addons]\n"
            b"molsysmt = molsysviewer_molsysmt\n"
        ),
    }
    for declaration in MODULE.expected_form_declarations():
        entries[declaration] = b"{}"
    if missing_form_declaration:
        entries.pop(MODULE.expected_form_declarations()[0])
    for index in range(extra_extensions):
        entries[f"molsysmt/_rust.extra{index}.so"] = b"stale"
    if bytecode:
        entries["molsysmt/__pycache__/__init__.pyc"] = b"cache"
    if legacy:
        entries["msm_rust_kernels/__init__.py"] = b""

    with ZipFile(path, mode="w") as archive:
        for name, content in entries.items():
            archive.writestr(name, content)


def test_valid_wheel_passes(tmp_path):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel)
    assert MODULE.validate_wheel(wheel) == []


def test_static_validator_accepts_a_directory_with_one_wheel(tmp_path):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel)
    assert MODULE.find_single_wheel(tmp_path) == wheel


def test_static_validator_rejects_an_ambiguous_directory(tmp_path):
    with pytest.raises(RuntimeError, match="exactly one wheel"):
        MODULE.find_single_wheel(tmp_path)

    first = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    second = tmp_path / "molsysmt-1.0.1-cp311-abi3-linux_x86_64.whl"
    _write_wheel(first)
    _write_wheel(second)
    with pytest.raises(RuntimeError, match="found 2"):
        MODULE.find_single_wheel(tmp_path)


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({"extra_extensions": 1}, "exactly one private"),
        ({"bytecode": True}, "bytecode/cache"),
        ({"legacy": True}, "legacy msm_rust_kernels"),
        ({"missing_form_declaration": True}, "dynamic form declarations"),
    ],
)
def test_invalid_wheel_fails_with_actionable_reason(
    tmp_path, kwargs, expected
):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel, **kwargs)
    problems = MODULE.validate_wheel(wheel)
    assert any(expected in problem for problem in problems)


def test_unexpected_top_level_package_fails(tmp_path):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel)
    with ZipFile(wheel, mode="a") as archive:
        archive.writestr("tests/test_accidental.py", b"")
    problems = MODULE.validate_wheel(wheel)
    assert any("unexpected top-level" in problem for problem in problems)


def test_installed_validator_requires_exactly_one_wheel(tmp_path):
    with pytest.raises(RuntimeError, match="exactly one wheel"):
        INSTALLED_MODULE.find_single_wheel(tmp_path)

    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel)
    assert INSTALLED_MODULE.find_single_wheel(tmp_path) == wheel


def test_rust_export_manifest_is_exact_and_includes_parallel_controls():
    exports = INSTALLED_MODULE.expected_rust_exports()
    assert len(exports) == 99
    assert {"get_available_num_threads", "probe_num_threads"} <= exports


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (None, False),
        ('{"url": "file:///tmp/wheel.whl"}', False),
        (
            '{"url": "file:///tmp/repo", '
            '"dir_info": {"editable": true}}',
            True,
        ),
    ],
)
def test_installed_validator_detects_only_editable_direct_urls(
    content,
    expected,
):
    assert INSTALLED_MODULE.is_editable_direct_url(content) is expected
