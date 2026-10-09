"""Regression tests for the MolSysMT Rust-wheel contract validator."""

import tomllib
from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
from zipfile import ZipFile

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "validate_rust_wheel.py"
SPEC = spec_from_file_location("validate_rust_wheel", SCRIPT)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)

INSTALLED_SCRIPT = (
    Path(__file__).resolve().parents[1] / "scripts" / "validate_installed_rust_wheel.py"
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
        "molsysmt-1.0.0.dist-info/WHEEL": (
            b"Wheel-Version: 1.0\n"
            b"Root-Is-Purelib: false\n"
            b"Tag: cp311-abi3-linux_x86_64\n"
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


def test_retired_addon_package_is_rejected(tmp_path):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel)
    with ZipFile(wheel, mode="a") as archive:
        archive.writestr("molsysviewer_molsysmt/runtime.py", b"legacy")
    assert any("unexpected top-level" in item for item in MODULE.validate_wheel(wheel))


@pytest.mark.parametrize("name", ["molsysmt", "renamed-provider"])
def test_retired_addon_entry_point_is_rejected(tmp_path, name):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel)
    with ZipFile(wheel, mode="a") as archive:
        archive.writestr(
            "molsysmt-1.0.0.dist-info/entry_points.txt",
            f"[molsysviewer.addons]\n{name} = molsysviewer_molsysmt\n",
        )
    assert any("retired" in item for item in MODULE.validate_wheel(wheel))


def test_unrelated_wheel_entry_points_remain_allowed(tmp_path):
    wheel = tmp_path / "molsysmt-1.0.0-cp311-abi3-linux_x86_64.whl"
    _write_wheel(wheel)
    with ZipFile(wheel, mode="a") as archive:
        archive.writestr(
            "molsysmt-1.0.0.dist-info/entry_points.txt",
            "[console_scripts]\nother-tool = tool:main\n",
        )
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
def test_invalid_wheel_fails_with_actionable_reason(tmp_path, kwargs, expected):
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
    assert len(exports) == 101
    assert {
        "get_available_num_threads",
        "probe_num_threads",
        "get_least_squares_planes",
        "get_mic_pair_observations",
    } <= exports


def test_data_package_excludes_generated_cache_but_keeps_scientific_resources(tmp_path):
    from setuptools import Distribution
    from setuptools.command.build_py import build_py
    from setuptools.config.expand import canonic_package_data

    settings = tomllib.loads(
        (Path(__file__).resolve().parents[2] / "pyproject.toml").read_text()
    )["tool"]["setuptools"]
    source = tmp_path / "data"
    resources = {
        "demo/system.h5msm",
        "databases/residues.pkl.gz",
        "tables/parameters.json",
    }
    caches = {
        "__pycache__/module.pyc",
        "databases/__pycache__/module.cpython-313.pyc",
        "databases/__pycache__/unrelated.txt",
        "leftover.pyc",
    }
    for name in resources | caches:
        path = source / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture")
    distribution = Distribution(
        {
            "packages": ["molsysmt.data"],
            "package_dir": {"molsysmt.data": str(source)},
            "package_data": canonic_package_data(settings["package-data"]),
            "exclude_package_data": canonic_package_data(
                settings["exclude-package-data"]
            ),
        }
    )
    builder = build_py(distribution)
    builder.ensure_finalized()
    builder.analyze_manifest()
    included = {
        Path(name).relative_to(source).as_posix()
        for name in builder.find_data_files("molsysmt.data", str(source))
    }
    assert resources <= included
    assert not caches & included


@pytest.mark.parametrize(
    ("content", "expected"),
    [
        (None, False),
        ('{"url": "file:///tmp/wheel.whl"}', False),
        (
            '{"url": "file:///tmp/repo", "dir_info": {"editable": true}}',
            True,
        ),
    ],
)
def test_installed_validator_detects_only_editable_direct_urls(
    content,
    expected,
):
    assert INSTALLED_MODULE.is_editable_direct_url(content) is expected
