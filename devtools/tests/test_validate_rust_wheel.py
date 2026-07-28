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


def _write_wheel(path, *, extra_extensions=0, bytecode=False, legacy=False):
    entries = {
        "molsysmt/_rust.abi3.so": b"extension",
        "molsysmt/py.typed": b"",
        "molsysmt/data/demo_manifest.json": b"{}",
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


@pytest.mark.parametrize(
    ("kwargs", "expected"),
    [
        ({"extra_extensions": 1}, "exactly one private"),
        ({"bytecode": True}, "bytecode/cache"),
        ({"legacy": True}, "legacy msm_rust_kernels"),
    ],
)
def test_invalid_wheel_fails_with_actionable_reason(
    tmp_path, kwargs, expected
):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel, **kwargs)
    problems = MODULE.validate_wheel(wheel)
    assert any(expected in problem for problem in problems)
