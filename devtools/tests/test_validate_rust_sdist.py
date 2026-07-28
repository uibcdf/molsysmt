"""Regression tests for the MolSysMT Rust source-distribution validator."""

from importlib.util import module_from_spec, spec_from_file_location
from pathlib import Path
import tarfile


SCRIPT = (
    Path(__file__).resolve().parents[1]
    / "scripts"
    / "validate_rust_sdist.py"
)
SPEC = spec_from_file_location("validate_rust_sdist", SCRIPT)
MODULE = module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


def _write_sdist(path, *, omit=(), extras=()):
    root = "molsysmt-1.0.0"
    required = MODULE.REQUIRED_SUFFIXES - set(omit)
    with tarfile.open(path, mode="w:gz") as archive:
        for name in sorted(required | {"rust/src/geometry.rs"} | set(extras)):
            source = path.parent / name.replace("/", "_")
            source.write_bytes(b"test")
            archive.add(source, arcname=f"{root}/{name}")


def test_valid_sdist_passes(tmp_path):
    archive = tmp_path / "molsysmt-1.0.0.tar.gz"
    _write_sdist(archive)
    assert MODULE.validate_sdist(archive) == []


def test_missing_rust_manifest_fails(tmp_path):
    archive = tmp_path / "molsysmt-1.0.0.tar.gz"
    _write_sdist(archive, omit={"rust/Cargo.toml"})
    problems = MODULE.validate_sdist(archive)
    assert any("rust/Cargo.toml" in problem for problem in problems)


def test_cache_and_binary_artifacts_fail(tmp_path):
    archive = tmp_path / "molsysmt-1.0.0.tar.gz"
    _write_sdist(
        archive,
        extras={
            "molsysmt/.pytest_cache/v/cache/nodeids",
            "molsysmt/lib/__pycache__/kernel.pyc",
            "rust/target/release/libmolsysmt.so",
        },
    )
    problems = MODULE.validate_sdist(archive)
    assert any("artifacts are present" in problem for problem in problems)


def test_unexpected_top_level_source_fails(tmp_path):
    archive = tmp_path / "molsysmt-1.0.0.tar.gz"
    _write_sdist(archive, extras={"tests/test_accidental.py"})
    problems = MODULE.validate_sdist(archive)
    assert any("unexpected top-level" in problem for problem in problems)
